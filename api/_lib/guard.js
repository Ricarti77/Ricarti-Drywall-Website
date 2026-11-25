// Abuse protection that needs no paid service. Per function instance only (instances are short-lived and several may
// run at once), so this is a first line of defence; a Vercel Firewall rate-limit rule is recommended in addition.
import crypto from 'node:crypto';

const hits = new Map();      // hashed client -> timestamps
const seen = new Map();      // enquiry reference -> { outcome, at }
const WINDOW = 10 * 60 * 1000, MAX_PER_WINDOW = 5, SEEN_TTL = 24 * 3600 * 1000;

export function clientKey(req) {
  const ip = String(req.headers['x-forwarded-for'] || req.headers['x-real-ip'] || '').split(',')[0].trim() || 'unknown';
  return crypto.createHash('sha256').update(ip + '|' + (process.env.RD_RATE_SALT || 'ricarti')).digest('hex').slice(0, 16);   // never store raw IPs
}
export function rateLimited(key, now = Date.now()) {
  const list = (hits.get(key) || []).filter((t) => now - t < WINDOW);
  list.push(now); hits.set(key, list);
  if (hits.size > 5000) hits.clear();
  return list.length > MAX_PER_WINDOW;
}
export function previous(ref, now = Date.now()) {
  const s = seen.get(ref);
  return s && now - s.at < SEEN_TTL ? s : null;
}
export function remember(ref, outcome, now = Date.now()) {
  seen.set(ref, { outcome, at: now });
  if (seen.size > 5000) seen.clear();
}
export function spamSignals(d, elapsed) {
  const text = [d.contact.name, d.project.description, d.project.location, d.contact.company].join(' ');
  const links = (text.match(/https?:\/\/|www\./gi) || []).length;
  return { tooFast: Number.isFinite(elapsed) && elapsed < 2500, manyLinks: links >= 3, nameHasLink: /https?:\/\/|www\./i.test(d.contact.name) };
}
