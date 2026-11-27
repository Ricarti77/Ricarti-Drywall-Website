// POST /api/enquiry — validates an estimate enquiry, emails it to the office through Resend (Reply-To = the customer)
// and, once the office copy is accepted, sends the customer a short acknowledgement in their language.
// Microsoft Graph is kept as a disabled alternative (MAIL_PROVIDER=graph).
// Responds { status: 'accepted' | 'failed' | 'uncertain', ref, code }. Logs carry only the reference, outcome and codes.
import { allowedOrigin } from './uploads/_rules.js';
import { validate, REF } from './_lib/validate.js';
import { clientKey, rateLimited, previous, remember, spamSignals } from './_lib/guard.js';
import { record, dispatch } from './_lib/crm.js';
import { build } from './_lib/email.js';
import { sendMail as graphSend, configured as graphConfigured } from './_lib/graph.js';
import { send as resendSend, configured as resendConfigured, officeAddress } from './_lib/resend.js';
import { buildAck } from './_lib/ack.js';

const provider = () => (String(process.env.MAIL_PROVIDER || 'resend').trim().toLowerCase() === 'graph' ? 'graph' : 'resend');
const switchedOff = () => String(process.env.RD_ENQUIRY_ENABLED || '').trim().toLowerCase() === 'false';
const ackOn = () => String(process.env.RD_ACK_ENABLED || '').trim().toLowerCase() !== 'false';

const reply = (res, http, status, ref, code) => { res.status(http).json({ status, ref: ref || null, code }); };

export default async function handler(req, res, deps = {}) {
  res.setHeader('Cache-Control', 'no-store');
  res.setHeader('X-Robots-Tag', 'noindex');
  const mailer = deps.mailer || provider();
  const rsend = deps.resendSend || resendSend;
  const gsend = deps.graphSend || graphSend;
  const ready = mailer === 'graph' ? graphConfigured() : resendConfigured();
  if (req.method !== 'POST') return reply(res, 405, 'failed', null, 'method');
  if (!allowedOrigin(req.headers.origin)) return reply(res, 403, 'failed', null, 'origin');
  if (!String(req.headers['content-type'] || '').includes('application/json')) return reply(res, 415, 'failed', null, 'content-type');
  let b = req.body;
  if (typeof b === 'string') { if (b.length > 24000) return reply(res, 413, 'failed', null, 'too-large'); try { b = JSON.parse(b); } catch { return reply(res, 400, 'failed', null, 'json'); } }
  if (JSON.stringify(b || {}).length > 24000) return reply(res, 413, 'failed', null, 'too-large');
  const ref = b && REF.test(String(b.id || '')) ? b.id : null;

  if (b && b._honey) return reply(res, 400, 'failed', ref, 'rejected');
  if (switchedOff() || !ready) return reply(res, 503, 'failed', ref, 'not-configured');

  const { errors, data } = validate(b);
  if (errors.length) return reply(res, 422, 'failed', ref, 'invalid:' + errors.join(','));

  const prev = previous(data.id);
  if (prev && prev.outcome !== 'failed') { console.log(JSON.stringify({ ref: data.id, event: 'duplicate', outcome: prev.outcome })); return reply(res, 200, prev.outcome, data.id, 'duplicate'); }

  if (rateLimited(clientKey(req))) return reply(res, 429, 'failed', data.id, 'rate-limited');
  const flags = spamSignals(data, Number(b.elapsed_ms));
  if (flags.tooFast) return reply(res, 400, 'failed', data.id, 'too-fast');

  const rec = record(data, { channel: mailer === 'graph' ? 'microsoft-graph' : 'resend' });
  const mail = build(rec, flags);
  remember(data.id, 'uncertain');                       // a parallel retry of the same reference must not send twice
  const t0 = Date.now();
  const out = mailer === 'graph'
    ? await gsend({ subject: mail.subject, html: mail.html, replyTo: mail.replyTo, ref: data.id })
    : await rsend({ to: officeAddress(), subject: mail.subject, html: mail.html, replyTo: mail.replyTo,
        key: 'owner/' + data.id, tags: [{ name: 'kind', value: 'owner' }] });
  remember(data.id, out.outcome);

  // Customer acknowledgement: only after the office copy was accepted, never for spam-flagged enquiries, and with
  // its own idempotency key so it can never suppress (or be suppressed by) the office notification.
  let ack = 'skipped';
  if (out.outcome === 'accepted' && mailer === 'resend' && ackOn() && !flags.manyLinks && !flags.nameHasLink) {
    const a = buildAck(rec);
    try {
      const r = await rsend({ to: rec.contact.email, subject: a.subject, html: a.html, text: a.text, replyTo: officeAddress(),
        key: 'ack/' + data.id, tags: [{ name: 'kind', value: 'ack' }] });
      ack = r.outcome + ':' + r.code;
    } catch { ack = 'error'; }
  }
  let crm = { crm: 'skipped' };
  if (out.outcome === 'accepted') { try { crm = await dispatch(rec); } catch { crm = { crm: 'error' }; } }
  console.log(JSON.stringify({ ref: data.id, event: 'enquiry', outcome: out.outcome, code: out.code, ms: Date.now() - t0, type: data.customer_type,
    lang: data.preferred_language, region: rec.project.routing.region, files: data.attachments.length, crm: crm.crm, ack, provider: mailer }));
  const http = out.outcome === 'accepted' ? 200 : out.outcome === 'uncertain' ? 202 : 502;
  return reply(res, http, out.outcome, data.id, out.code);
}
