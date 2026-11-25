// POST /api/enquiry — validates an estimate enquiry and emails it to the office through Microsoft 365 (Graph).
// Responds { status: 'accepted' | 'failed' | 'uncertain', ref, code }. Logs carry only the reference, outcome and codes.
import { allowedOrigin } from './uploads/_rules.js';
import { validate, REF } from './_lib/validate.js';
import { clientKey, rateLimited, previous, remember, spamSignals } from './_lib/guard.js';
import { record, dispatch } from './_lib/crm.js';
import { build } from './_lib/email.js';
import { sendMail, configured } from './_lib/graph.js';

const reply = (res, http, status, ref, code) => { res.status(http).json({ status, ref: ref || null, code }); };

export default async function handler(req, res, deps = {}) {
  res.setHeader('Cache-Control', 'no-store');
  res.setHeader('X-Robots-Tag', 'noindex');
  const send = deps.sendMail || sendMail;
  if (req.method !== 'POST') return reply(res, 405, 'failed', null, 'method');
  if (!allowedOrigin(req.headers.origin)) return reply(res, 403, 'failed', null, 'origin');
  if (!String(req.headers['content-type'] || '').includes('application/json')) return reply(res, 415, 'failed', null, 'content-type');
  let b = req.body;
  if (typeof b === 'string') { if (b.length > 24000) return reply(res, 413, 'failed', null, 'too-large'); try { b = JSON.parse(b); } catch { return reply(res, 400, 'failed', null, 'json'); } }
  if (JSON.stringify(b || {}).length > 24000) return reply(res, 413, 'failed', null, 'too-large');
  const ref = b && REF.test(String(b.id || '')) ? b.id : null;

  if (b && b._honey) return reply(res, 400, 'failed', ref, 'rejected');
  if (String(process.env.RD_ENQUIRY_ENABLED || '').toLowerCase() !== 'true' || !configured()) return reply(res, 503, 'failed', ref, 'not-configured');

  const { errors, data } = validate(b);
  if (errors.length) return reply(res, 422, 'failed', ref, 'invalid:' + errors.join(','));

  const prev = previous(data.id);
  if (prev && prev.outcome !== 'failed') { console.log(JSON.stringify({ ref: data.id, event: 'duplicate', outcome: prev.outcome })); return reply(res, 200, prev.outcome, data.id, 'duplicate'); }

  if (rateLimited(clientKey(req))) return reply(res, 429, 'failed', data.id, 'rate-limited');
  const flags = spamSignals(data, Number(b.elapsed_ms));
  if (flags.tooFast) return reply(res, 400, 'failed', data.id, 'too-fast');

  const rec = record(data, { channel: 'microsoft-graph' });
  const mail = build(rec, flags);
  remember(data.id, 'uncertain');                       // a parallel retry of the same reference must not send twice
  const t0 = Date.now();
  const out = await send({ subject: mail.subject, html: mail.html, replyTo: mail.replyTo, ref: data.id });
  remember(data.id, out.outcome);
  let crm = { crm: 'skipped' };
  if (out.outcome === 'accepted') { try { crm = await dispatch(rec); } catch { crm = { crm: 'error' }; } }
  console.log(JSON.stringify({ ref: data.id, event: 'enquiry', outcome: out.outcome, code: out.code, ms: Date.now() - t0, type: data.customer_type,
    lang: data.preferred_language, region: rec.project.routing.region, files: data.attachments.length, crm: crm.crm }));
  const http = out.outcome === 'accepted' ? 200 : out.outcome === 'uncertain' ? 202 : 502;
  return reply(res, http, out.outcome, data.id, out.code);
}
