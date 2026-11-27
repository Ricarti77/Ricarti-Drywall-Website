// Office notification email (English). Human-readable only: no JSON, code or CRM metadata in the visible email.
// The structured ricarti.enquiry.v2 record (crm.js) is still built for future GoHighLevel / database use, but it is
// not printed here and is NOT stored anywhere yet. All customer text is HTML-escaped.
import { C, SANS, SERIF, esc, layout, sectionTitle, rows, paragraph, button, logoAttachment } from './brand.js';

const LABEL = {
  services: { insulation: 'Insulation & spray foam', 'drywall-installation': 'Drywall installation', 'taping-finishing': 'Taping & finishing (Level 4 / 5)',
    'architectural-finishing': 'Architectural details', soundproofing: 'Soundproofing', 'metal-stud-framing': 'Metal stud framing',
    'popcorn-ceiling': 'Popcorn ceiling removal', repairs: 'Repairs & plaster' },
  timeline: { asap: 'As soon as possible', '1-3-months': 'In 1–3 months', '3-6-months': 'In 3–6 months', flexible: 'Flexible', 'not-sure': 'Not sure yet',
    'under-1-month': 'Board-ready within a month', '6-12-months': 'In 6–12 months', tender: 'Pricing for a tender', 'not-scheduled': 'Not scheduled yet' },
  type: { 'custom-home': 'Custom home', 'detached-homes': 'Detached homes', 'semi-detached': 'Semi-detached', 'townhouse-block': 'Townhouse block',
    'low-rise-multi': 'Low-rise multi-unit', 'addition-renovation': 'Addition / renovation', 'commercial-interior': 'Commercial interior', other: 'Other' },
  lang: { 'en-CA': 'English', 'pt-BR': 'Portuguese', 'es-419': 'Spanish', 'fr-CA': 'French', 'it-IT': 'Italian' },
};
const PROV = { ON: 'Ontario', BC: 'British Columbia', QC: 'Quebec', AB: 'Alberta', MB: 'Manitoba', SK: 'Saskatchewan', NS: 'Nova Scotia',
  NB: 'New Brunswick', NL: 'Newfoundland and Labrador', PE: 'Prince Edward Island', NT: 'Northwest Territories', YT: 'Yukon' };
const size = (b) => (b < 1048576 ? Math.max(1, Math.round(b / 1024)) + ' KB' : (b / 1048576).toFixed(1) + ' MB');

export function when(iso) {
  try {
    return new Intl.DateTimeFormat('en-CA', { timeZone: 'America/Toronto', weekday: 'short', year: 'numeric', month: 'long', day: 'numeric',
      hour: 'numeric', minute: '2-digit', timeZoneName: 'short' }).format(new Date(iso));
  } catch { return String(iso || ''); }
}

// Plain-language location status. An incomplete address is "requires verification", never "outside our area".
export function locationStatus(loc, routing) {
  const where = [loc.city, PROV[loc.province] || loc.province, loc.postal_code].filter(Boolean).join(', ');
  switch (routing.location_status) {
    case 'ontario': return { text: 'Ontario' + (where ? ' — ' + where : ''), warn: false };
    case 'ontario-unconfirmed': return { text: 'Ontario (no city or postal code given) — location requires verification', warn: true };
    case 'outside-ontario': return { text: (where || 'Outside Ontario') + ' — outside Ontario, please confirm before quoting', warn: true };
    default: return { text: 'Location requires verification', warn: true };
  }
}

function source(ls) {
  if (!ls) return '';
  const t = ls.first_touch;
  const how = t && t.type ? (t.type === 'search' ? 'Search' : t.type === 'social' ? 'Social media' : t.type === 'referral' ? 'Another website' : t.type === 'campaign' ? 'Campaign link' : t.type) + (t.from ? ' (' + t.from + ')' : '') : 'Direct visit';
  return how;
}

export function build(rec, flags) {
  const b = rec.customer_type === 'builder';
  const spam = !!(flags && (flags.manyLinks || flags.nameHasLink));
  const tag = rec.preferred_language === 'en-CA' ? '' : '[' + rec.preferred_language.slice(0, 2).toUpperCase() + '] ';
  const kind = b ? 'Builder enquiry' : 'Homeowner enquiry';
  const subject = ((spam ? '[Possible spam] ' : '') + tag + kind + ' — ' + rec.contact.name + ' — ' + rec.id).slice(0, 240);
  const date = when(rec.received_at);
  const loc = rec.project.location, st = locationStatus(loc, rec.project.routing);
  const services = rec.services.map((s) => LABEL.services[s]).filter(Boolean);
  const notRec = rec.attachments_not_received || [], got = rec.attachments || [];

  const replySubject = 'Your estimate request — ' + rec.id;
  const replyHref = 'mailto:' + encodeURIComponent(rec.contact.email).replace(/%40/g, '@') + '?subject=' + encodeURIComponent(replySubject);

  let h = '';
  if (spam) h += '<tr><td style="padding:22px 32px 0 32px"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td bgcolor="#F6E7E2" style="background:#F6E7E2;border-left:3px solid #A4442C;padding:12px 14px;font-family:' + SANS + ';font-size:13px;line-height:19px;color:#5C2416">This enquiry contains several links and may be spam. Check it before replying. No confirmation was sent to the customer.</td></tr></table></td></tr>';
  h += '<tr><td style="padding:30px 32px 0 32px">'
    + '<p style="margin:0 0 6px 0;font-family:' + SANS + ';font-size:11px;letter-spacing:2px;text-transform:uppercase;color:' + C.bronze + ';font-weight:bold">New ' + esc(kind.toLowerCase()) + '</p>'
    + '<p class="rd-ref" style="margin:0;font-family:' + SERIF + ';font-size:28px;line-height:34px;color:' + C.ink + '">' + esc(rec.id) + '</p>'
    + '<p style="margin:6px 0 0 0;font-family:' + SANS + ';font-size:13px;line-height:19px;color:' + C.stone + '">Received ' + esc(date) + '</p></td></tr>';

  h += sectionTitle('Customer');
  h += rows([
    ['Name', rec.contact.name], ['Company', rec.contact.company],
    ['Email', '<a href="mailto:' + esc(rec.contact.email) + '" style="color:' + C.ink + ';text-decoration:underline">' + esc(rec.contact.email) + '</a>', true],
    ['Phone', rec.contact.phone ? '<a href="tel:' + esc(rec.contact.phone.replace(/[^\d+]/g, '')) + '" style="color:' + C.ink + ';text-decoration:underline">' + esc(rec.contact.phone) + '</a>' : '', true],
    ['Customer type', b ? 'Builder / contractor' : 'Homeowner'],
    ['Language', LABEL.lang[rec.preferred_language] || rec.preferred_language],
    ['Marketing emails', rec.consent.marketing_opt_in ? 'Yes — opted in on the form' : 'No'],
  ]);

  h += sectionTitle('Project');
  h += rows([
    ['Location (as typed)', loc.raw || '—'],
    ['Location check', st.warn ? '<span style="color:#8A5A1E">' + esc(st.text) + '</span>' : esc(st.text), true],
    ['Project type', b ? LABEL.type[rec.project.type] || '' : ''],
    ['Timeline', LABEL.timeline[rec.project.timeline] || 'Not specified'],
    ['How they found us', source(rec.lead_source)],
  ]);

  h += sectionTitle('Requested services');
  h += services.length
    ? '<tr><td style="padding:10px 32px 0 32px">' + services.map((s) => '<p style="margin:0 0 6px 0;font-family:' + SANS + ';font-size:15px;line-height:21px;color:' + C.ink + '"><span style="color:' + C.bronze + '">&#9632;</span>&nbsp;&nbsp;' + esc(s) + '</p>').join('') + '</td></tr>'
    : paragraph('No specific service selected.', { color: C.stone });

  if (rec.project.description) {
    h += sectionTitle('Project description');
    h += '<tr><td style="padding:12px 32px 0 32px"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td bgcolor="#FFFFFF" style="background:#FFFFFF;border-left:2px solid ' + C.bronze + ';padding:14px 16px;font-family:' + SANS + ';font-size:15px;line-height:23px;color:' + C.ink + '">'
      + esc(rec.project.description).replace(/\r?\n/g, '<br>') + '</td></tr></table></td></tr>';
  }

  h += sectionTitle('Drawings & attachments');
  if (got.length) h += paragraph(esc(got.length + ' file(s) received in private storage.'));
  if (notRec.length) {
    h += paragraph('The customer selected ' + notRec.length + ' file(s), but online drawing upload is not enabled yet, so <strong>no files were received</strong>. Ask the customer to email them if needed:');
    h += '<tr><td style="padding:8px 32px 0 32px">' + notRec.map((a) => '<p style="margin:0 0 4px 0;font-family:' + SANS + ';font-size:13px;line-height:19px;color:' + C.stone + '">' + esc(a.name) + ' &middot; ' + esc(size(a.size)) + '</p>').join('') + '</td></tr>';
  }
  if (!got.length && !notRec.length) h += paragraph('No drawings or files were attached.', { color: C.stone });

  h += button(replyHref, 'REPLY TO CUSTOMER');
  h += paragraph('Or simply press <strong>Reply</strong> — your answer goes to ' + esc(rec.contact.email) + '.', { size: 13, lh: 19, color: C.stone, pad: '12px 32px 0 32px' });
  h += paragraph('Keep this email: it is currently the only copy of this enquiry. Permanent enquiry storage has not been set up yet.', { size: 12, lh: 18, color: C.soft, pad: '22px 32px 0 32px' });

  const html = layout({ lang: 'en', title: subject, preheader: kind + ' from ' + rec.contact.name + ' · ' + (loc.raw || 'location not given') + ' · ' + rec.id, body: h,
    footerNote: 'Sent by the estimate form on ricartidrywall.ca' });

  const line = (k, v) => (v ? k + ': ' + v : null);
  const text = [
    (spam ? 'WARNING: this enquiry contains several links and may be spam. No confirmation was sent to the customer.\n' : '') + 'NEW ' + kind.toUpperCase(),
    rec.id, 'Received ' + date, '',
    'CUSTOMER', line('Name', rec.contact.name), line('Company', rec.contact.company), line('Email', rec.contact.email), line('Phone', rec.contact.phone),
    line('Customer type', b ? 'Builder / contractor' : 'Homeowner'), line('Language', LABEL.lang[rec.preferred_language]),
    line('Marketing emails', rec.consent.marketing_opt_in ? 'Yes — opted in on the form' : 'No'), '',
    'PROJECT', line('Location (as typed)', loc.raw || '—'), line('Location check', st.text), line('Project type', b ? LABEL.type[rec.project.type] : ''),
    line('Timeline', LABEL.timeline[rec.project.timeline] || 'Not specified'), line('How they found us', source(rec.lead_source)), '',
    'REQUESTED SERVICES', ...(services.length ? services.map((s) => '- ' + s) : ['No specific service selected.']), '',
    ...(rec.project.description ? ['PROJECT DESCRIPTION', rec.project.description, ''] : []),
    'DRAWINGS & ATTACHMENTS',
    ...(got.length ? [got.length + ' file(s) received in private storage.'] : []),
    ...(notRec.length ? ['The customer selected ' + notRec.length + ' file(s), but online drawing upload is not enabled yet, so no files were received:', ...notRec.map((a) => '- ' + a.name + ' (' + size(a.size) + ')')] : []),
    ...(!got.length && !notRec.length ? ['No drawings or files were attached.'] : []), '',
    'Reply to this email to answer the customer (' + rec.contact.email + ').',
    'Keep this email: it is currently the only copy of this enquiry.', '',
    'RICARTI DRYWALL — Perfection Starts Here!',
  ].filter((x) => x !== null).join('\n');

  return { subject, html, text, replyTo: rec.contact.email, attachments: [logoAttachment()] };
}
