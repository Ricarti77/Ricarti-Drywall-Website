// Resend transactional email (https://resend.com/docs/api-reference/emails/send-email).
// The API key comes only from the server-side environment variable RESEND_API_KEY. It is never logged, returned
// to the browser or written to the repository.
const env = (k) => (process.env[k] || '').trim();
const API = 'https://api.resend.com/emails';

export const FROM_DEFAULT = 'Ricarti Drywall <estimates@notifications.ricartidrywall.ca>';
export const TO_DEFAULT = 'cris@ricartidrywall.ca';

export function configured() { return /^re_[A-Za-z0-9_]{8,}$/.test(env('RESEND_API_KEY')); }
export const sender = () => env('RD_MAIL_FROM') || FROM_DEFAULT;
export const officeAddress = () => env('RD_MAIL_TO') || TO_DEFAULT;

// Outcome mapping, kept identical in meaning to the Graph module:
//   'accepted'  – Resend returned an email id (accepted for delivery; NOT proof it reached the inbox).
//   'failed'    – definitely not sent (validation, auth, domain, quota or rate-limit refusal): safe to try again later.
//   'uncertain' – the request left us but the answer is unknown (timeout, network, 5xx, idempotency conflict):
//                 Resend may still deliver it, so the visitor must not resend.
// `key` is the Idempotency-Key. Owner notifications and customer acknowledgements use different prefixes
// ('owner/<ref>', 'ack/<ref>') so one can never suppress the other; Resend ignores a repeat of the same key
// for 24 hours, so a network retry cannot send a second copy.
export async function send({ to, subject, html, text, replyTo, key, tags }, fetchImpl = fetch) {
  if (!configured()) return { outcome: 'failed', code: 'not-configured' };
  const body = { from: sender(), to: [].concat(to), subject, html };
  if (text) body.text = text;
  if (replyTo) body.reply_to = replyTo;
  if (tags) body.tags = tags;
  let r;
  try {
    r = await fetchImpl(API, {
      method: 'POST',
      headers: { Authorization: 'Bearer ' + env('RESEND_API_KEY'), 'Content-Type': 'application/json',
        'User-Agent': 'ricarti-drywall-website/1.0', ...(key ? { 'Idempotency-Key': key } : {}) },
      body: JSON.stringify(body),
      signal: AbortSignal.timeout(10000),
    });
  } catch (e) {
    return { outcome: 'uncertain', code: e && e.name === 'TimeoutError' ? 'timeout' : 'network' };
  }
  const j = await r.json().catch(() => ({}));
  if (r.ok && j && j.id) return { outcome: 'accepted', code: 'resend-' + r.status, id: j.id };
  const name = String((j && j.name) || 'http-' + r.status).slice(0, 60);
  if (r.status === 409 || r.status >= 500 || (r.ok && !(j && j.id))) return { outcome: 'uncertain', code: name };
  return { outcome: 'failed', code: name };                // 400/401/403/404/422/429: Resend did not send it
}
