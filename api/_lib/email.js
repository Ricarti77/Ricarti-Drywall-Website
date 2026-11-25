// Internal notification email (English, for the office). All customer text is HTML-escaped.
const esc = (s) => String(s == null ? '' : s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const LABEL = {
  services: { insulation: 'Insulation & spray foam', 'drywall-installation': 'Drywall installation', 'taping-finishing': 'Taping & finishing (Level 4 / 5)',
    'architectural-finishing': 'Architectural details', soundproofing: 'Soundproofing', 'metal-stud-framing': 'Metal stud framing',
    'popcorn-ceiling': 'Popcorn ceiling removal', repairs: 'Repairs & plaster' },
  timeline: { asap: 'As soon as possible', '1-3-months': 'In 1–3 months', '3-6-months': 'In 3–6 months', flexible: 'Flexible', 'not-sure': 'Not sure yet',
    'under-1-month': 'Board-ready within a month', '6-12-months': 'In 6–12 months', tender: 'Pricing for a tender', 'not-scheduled': 'Not scheduled yet' },
};
const size = (b) => (b < 1048576 ? Math.max(1, Math.round(b / 1024)) + ' KB' : (b / 1048576).toFixed(1) + ' MB');

export function build(rec, flags) {
  const b = rec.customer_type === 'builder';
  const tag = rec.preferred_language === 'en-CA' ? '' : '[' + rec.preferred_language.slice(0, 2).toUpperCase() + '] ';
  const warn = flags && (flags.manyLinks || flags.nameHasLink) ? '[Possible spam] ' : '';
  const loc = rec.project.location;
  const rows = [
    ['Reference', rec.id], ['Customer type', b ? 'Builder / contractor' : 'Homeowner'], ['Name', rec.contact.name], ['Company', rec.contact.company],
    ['Email', rec.contact.email], ['Phone', rec.contact.phone], ['Project location', loc.raw],
    ['Detected', [loc.city, loc.province, loc.postal_code].filter(Boolean).join(', ') + (rec.project.routing.needs_review ? ' — outside usual service area or unclear, please check' : '')],
    ['Project type', b ? rec.project.type : ''], ['Timeline', LABEL.timeline[rec.project.timeline] || ''],
    ['Services', rec.services.map((s) => LABEL.services[s]).join(', ')], ['Description / notes', rec.project.description],
    ['Files in private storage', rec.attachments.map((a) => a.ref + ' (' + size(a.size) + ')').join('\n') || 'None'],
    ['Files NOT received', rec.attachments_not_received.map((a) => a.name + ' (' + size(a.size) + ')').join('\n') || 'None'],
    ['Language', rec.preferred_language], ['Marketing consent', rec.consent.marketing_opt_in ? 'Yes (opted in on the form)' : 'No'],
    ['Lead source', [rec.lead_source.first_touch ? rec.lead_source.first_touch.type + ' / ' + rec.lead_source.first_touch.from : 'direct', rec.lead_source.landing_page, rec.lead_source.referrer].filter(Boolean).join(' · ')],
  ].filter(([, v]) => v !== '' && v != null);
  const html = '<div style="font-family:Arial,Helvetica,sans-serif;font-size:14px;color:#161616">'
    + '<p style="margin:0 0 12px">New enquiry from the Ricarti Drywall website. Reply to this email to answer the customer directly.</p>'
    + '<table cellpadding="8" cellspacing="0" style="border-collapse:collapse;border:1px solid #D8D1C5">'
    + rows.map(([k, v]) => '<tr><th align="left" valign="top" style="background:#F1EDE6;border:1px solid #D8D1C5;white-space:nowrap">' + esc(k) + '</th><td style="border:1px solid #D8D1C5;white-space:pre-wrap">' + esc(v) + '</td></tr>').join('')
    + '</table><p style="margin:16px 0 4px;color:#5A554E;font-size:12px">CRM record (ricarti.enquiry.v2):</p>'
    + '<pre style="font-size:11px;color:#5A554E;white-space:pre-wrap">' + esc(JSON.stringify(rec, null, 1)) + '</pre></div>';
  const subject = warn + tag + (b ? 'Builder enquiry' : 'Homeowner enquiry') + ' — ' + rec.contact.name + ' — ' + rec.id;
  return { subject: subject.slice(0, 240), html, replyTo: rec.contact.email };
}
