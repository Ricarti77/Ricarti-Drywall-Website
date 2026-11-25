// Microsoft Graph mail delivery (application permission Mail.Send, scoped in Exchange Online to ONE mailbox with
// RBAC for Applications). Credentials come only from Vercel environment variables and are never logged or returned.
import crypto from 'node:crypto';

const env = (k) => (process.env[k] || '').trim();
export function configured() {
  return !!(env('MS_TENANT_ID') && env('MS_CLIENT_ID') && (env('MS_CLIENT_SECRET') || (env('MS_CERT_PRIVATE_KEY') && env('MS_CERT_THUMBPRINT'))) && env('RD_MAIL_SENDER'));
}

const b64url = (buf) => Buffer.from(buf).toString('base64').replace(/=+$/, '').replace(/\+/g, '-').replace(/\//g, '_');
function clientAssertion(tenant, clientId) {
  // Certificate credentials (recommended over a client secret): RS256 JWT signed with the private key.
  const thumb = Buffer.from(env('MS_CERT_THUMBPRINT').replace(/[^0-9a-f]/gi, ''), 'hex');
  const now = Math.floor(Date.now() / 1000);
  const head = b64url(JSON.stringify({ alg: 'RS256', typ: 'JWT', x5t: b64url(thumb) }));
  const body = b64url(JSON.stringify({ aud: `https://login.microsoftonline.com/${tenant}/oauth2/v2.0/token`, iss: clientId, sub: clientId,
    jti: crypto.randomUUID(), nbf: now - 30, exp: now + 300 }));
  const key = env('MS_CERT_PRIVATE_KEY').replace(/\\n/g, '\n');
  const sig = crypto.createSign('RSA-SHA256').update(head + '.' + body).sign(key);
  return head + '.' + body + '.' + b64url(sig);
}

let cache = { token: '', exp: 0 };
async function token(fetchImpl) {
  if (cache.token && Date.now() < cache.exp - 60000) return cache.token;
  const tenant = env('MS_TENANT_ID'), clientId = env('MS_CLIENT_ID');
  const form = new URLSearchParams({ client_id: clientId, scope: 'https://graph.microsoft.com/.default', grant_type: 'client_credentials' });
  if (env('MS_CERT_PRIVATE_KEY')) { form.set('client_assertion_type', 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer'); form.set('client_assertion', clientAssertion(tenant, clientId)); }
  else form.set('client_secret', env('MS_CLIENT_SECRET'));
  const r = await fetchImpl(`https://login.microsoftonline.com/${encodeURIComponent(tenant)}/oauth2/v2.0/token`,
    { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: form, signal: AbortSignal.timeout(6000) });
  const j = await r.json().catch(() => ({}));
  if (!r.ok || !j.access_token) { const e = new Error('token'); e.stage = 'token'; e.code = j.error || 'http-' + r.status; throw e; }
  cache = { token: j.access_token, exp: Date.now() + (Number(j.expires_in) || 3000) * 1000 };
  return cache.token;
}

// Outcome: 'accepted' (Graph 202: Microsoft accepted it for delivery; NOT proof it reached the inbox),
// 'failed' (definitely not sent: config, auth, permission or request errors), 'uncertain' (timeout, throttling or
// server error after the request left us: Microsoft may still deliver it, so the visitor must not resend).
export async function sendMail({ subject, html, replyTo, ref }, fetchImpl = fetch) {
  if (!configured()) return { outcome: 'failed', code: 'not-configured' };
  let t;
  try { t = await token(fetchImpl); }
  catch (e) { return { outcome: 'failed', code: 'auth-' + (e.code || 'error') }; }   // no mail request was made
  const sender = env('RD_MAIL_SENDER'), to = env('RD_MAIL_TO') || 'cris@ricartidrywall.ca';
  const message = {
    subject, body: { contentType: 'HTML', content: html },
    toRecipients: [{ emailAddress: { address: to } }],
    replyTo: replyTo ? [{ emailAddress: { address: replyTo } }] : [],
    internetMessageHeaders: [{ name: 'X-Ricarti-Enquiry', value: ref }],
  };
  let r;
  try {
    r = await fetchImpl(`https://graph.microsoft.com/v1.0/users/${encodeURIComponent(sender)}/sendMail`, {
      method: 'POST', headers: { Authorization: 'Bearer ' + t, 'Content-Type': 'application/json', 'client-request-id': crypto.randomUUID() },
      body: JSON.stringify({ message, saveToSentItems: true }), signal: AbortSignal.timeout(9000),
    });
  } catch (e) {
    return { outcome: 'uncertain', code: e && e.name === 'TimeoutError' ? 'timeout' : 'network' };
  }
  if (r.status === 202) return { outcome: 'accepted', code: 'graph-202' };
  let code = 'http-' + r.status;
  try { const j = await r.json(); if (j && j.error && j.error.code) code += '-' + String(j.error.code).slice(0, 60); } catch {}
  if (r.status === 401) cache = { token: '', exp: 0 };
  if (r.status === 429 || r.status >= 500) return { outcome: 'uncertain', code };   // Microsoft documents cases where mail still goes out
  return { outcome: 'failed', code };
}
