// Server-side validation for /api/enquiry. Everything the browser sends is re-checked here.
export const LANGS = ['en-CA', 'pt-BR', 'es-419', 'fr-CA', 'it-IT'];
export const CUSTOMER = ['homeowner', 'builder'];
export const SERVICES = ['insulation', 'drywall-installation', 'taping-finishing', 'architectural-finishing', 'soundproofing',
  'metal-stud-framing', 'popcorn-ceiling', 'repairs'];
export const PROJECT_TYPES = ['', 'custom-home', 'detached-homes', 'semi-detached', 'townhouse-block', 'low-rise-multi',
  'addition-renovation', 'commercial-interior', 'other'];
export const TIMELINES = ['', 'asap', '1-3-months', '3-6-months', 'flexible', 'not-sure', 'under-1-month', '6-12-months', 'tender', 'not-scheduled'];
export const REF = /^RD-\d{6}-[A-Z2-9]{5}$/;
const EMAIL = /^[^\s@<>"]+@[^\s@<>"]+\.[^\s@<>"]{2,}$/;
const BLOB_REF = /^enquiries\/\d{4}-\d{2}\/RD-\d{6}-[A-Z2-9]{5}\/\d{2}-[A-Za-z0-9._-]{1,80}$/;
const FILE_TYPES = ['application/pdf', 'image/jpeg', 'image/png', 'image/webp', 'image/heic', 'image/heif'];

const str = (v, max) => (typeof v === 'string' ? v.replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F\u007F]/g, '').trim().slice(0, max) : '');

export function validate(b) {
  const errors = [];
  if (!b || typeof b !== 'object') return { errors: ['body'] };
  const ref = str(b.id, 20);
  if (!REF.test(ref)) errors.push('id');
  const customer = CUSTOMER.includes(b.customer_type) ? b.customer_type : (errors.push('customer_type'), 'homeowner');
  const c = b.contact || {}, p = b.project || {};
  const contact = { name: str(c.name, 120), company: customer === 'builder' ? str(c.company, 160) : '', email: str(c.email, 160).toLowerCase(), phone: str(c.phone, 40) };
  if (!contact.name) errors.push('name');
  if (!EMAIL.test(contact.email)) errors.push('email');
  if (contact.phone && contact.phone.replace(/\D/g, '').length < 7) errors.push('phone');
  const project = { type: customer === 'builder' && PROJECT_TYPES.includes(p.type) ? p.type : '', location: str(p.location, 200),
    timeline: TIMELINES.includes(p.timeline) ? p.timeline : '', description: str(p.description, 4000) };
  const services = Array.isArray(b.services) ? [...new Set(b.services.filter((s) => SERVICES.includes(s)))] : [];
  const language = LANGS.includes(b.preferred_language) ? b.preferred_language : 'en-CA';
  const files = (arr, needRef) => (Array.isArray(arr) ? arr.slice(0, 20) : []).map((a) => ({
    ref: needRef ? str(a && a.ref, 140) : undefined, name: str(a && a.name, 200), size: Math.max(0, Math.min(Number(a && a.size) || 0, 52428800)),
    type: FILE_TYPES.includes(a && a.type) ? a.type : 'application/octet-stream', reason: needRef ? undefined : str(a && a.reason, 40),
  })).filter((a) => a.name && (!needRef || BLOB_REF.test(a.ref)));
  const ls = b.lead_source || {};
  const touch = (t) => (t && typeof t === 'object' ? { type: str(t.type, 40), from: str(t.from, 60), page: str(t.page, 200), t: Number(t.t) || 0 } : null);
  const utm = {};
  if (ls.utm && typeof ls.utm === 'object') for (const k of ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content', 'gclid', 'fbclid']) if (ls.utm[k]) utm[k] = str(ls.utm[k], 120);
  return {
    errors,
    data: {
      id: ref, customer_type: customer, contact, project, services, preferred_language: language,
      marketing_opt_in: !!(b.consent && b.consent.marketing_opt_in === true),
      attachments: files(b.attachments, true), attachments_not_received: files(b.attachments_not_received, false),
      lead_source: { channel: 'website', form: 'estimate', page: str(ls.page, 200), landing_page: str(ls.landing_page, 300), referrer: str(ls.referrer, 300),
        first_touch: touch(ls.first_touch), last_touch: touch(ls.last_touch), utm },
    },
  };
}
