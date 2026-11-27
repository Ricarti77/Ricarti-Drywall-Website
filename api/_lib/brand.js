// Shared Concept D email shell: charcoal header with the lockup, warm-white body, bronze accents, English slogan.
// Built for Outlook (Word engine), Gmail and mobile: table layout, inline styles, bgcolor attributes, no web fonts,
// no background images, no CSS the major clients strip.
//
// Logo: the header is an HTML wordmark (live text, no image), so it renders in every client, with images blocked, and
// never depends on the password-protected preview. An inline Content-ID image was tried first (commit 20d451e) and
// showed as a broken image in Outlook. Once the logo is on a public HTTPS address (e.g. the production domain at
// launch), set RD_EMAIL_LOGO_URL to it: the header then shows that image, and Outlook shows styled alt text if
// images are blocked.

export const C = { charcoal: '#1E1D1B', ink: '#161616', warm: '#F1EDE6', paper: '#FBF9F5', bronze: '#A8865A', line: '#D8D1C5', stone: '#6B665E', soft: '#8F8A82' };
export const SERIF = "Georgia,'Times New Roman',Times,serif";
export const SANS = 'Arial,Helvetica,sans-serif';

export const esc = (s) => String(s == null ? '' : s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const nl2br = (s) => esc(s).replace(/\r?\n/g, '<br>');

const LOGO_URL = () => { const u = String(process.env.RD_EMAIL_LOGO_URL || '').trim(); return /^https:\/\/[^\s"'<>]+\.png$/i.test(u) ? u : ''; };
const LOGO_W = 220, LOGO_H = 43;   // lockup-plaster-refined.png is 895 x 176

function wordmark() {
  // Letter-spaced text echoing the lockup. padding-left equals the letter-spacing so the spaced word stays centred.
  return '<table role="presentation" cellpadding="0" cellspacing="0" border="0" align="center"><tr><td align="center" style="padding:0 0 0 14px">'
    + '<p style="margin:0;font-family:' + SANS + ';font-size:28px;line-height:32px;letter-spacing:14px;color:#EDE6DA;font-weight:normal;mso-line-height-rule:exactly">RICARTI</p>'
    + '</td></tr><tr><td align="center" style="padding:10px 0 0 24px">'
    + '<p style="margin:0;font-family:' + SANS + ';font-size:9px;line-height:11px;letter-spacing:24px;color:#EDE6DA;font-weight:bold;mso-line-height-rule:exactly">DRYWALL</p>'
    + '</td></tr></table>';
}
function headerMark() {
  const u = LOGO_URL();
  if (!u) return wordmark();
  return '<img src="' + esc(u) + '" width="' + LOGO_W + '" height="' + LOGO_H + '" alt="RICARTI DRYWALL" style="display:block;margin:0 auto;width:' + LOGO_W + 'px;height:' + LOGO_H
    + 'px;border:0;outline:none;text-decoration:none;color:#EDE6DA;font-family:' + SANS + ';font-size:18px;line-height:43px;letter-spacing:6px;text-align:center">';
}

// Small uppercase bronze section label followed by a thin rule.
export function sectionTitle(text) {
  return '<tr><td style="padding:28px 32px 0 32px">'
    + '<p style="margin:0 0 10px 0;font-family:' + SANS + ';font-size:11px;line-height:14px;letter-spacing:2px;text-transform:uppercase;color:' + C.bronze + ';font-weight:bold">' + esc(text) + '</p>'
    + '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td height="1" style="height:1px;line-height:1px;font-size:1px;background:' + C.line + '" bgcolor="' + C.line + '">&nbsp;</td></tr></table>'
    + '</td></tr>';
}

// Label / value rows; values may contain pre-built safe HTML when `html` is true.
export function rows(list) {
  const r = list.filter((x) => x && x[1] !== '' && x[1] != null).map(([k, v, html]) =>
    '<tr><td valign="top" width="34%" class="rd-k" style="padding:9px 12px 9px 0;font-family:' + SANS + ';font-size:13px;line-height:19px;color:' + C.stone + '">' + esc(k) + '</td>'
    + '<td valign="top" class="rd-v" style="padding:9px 0;font-family:' + SANS + ';font-size:15px;line-height:21px;color:' + C.ink + '">' + (html ? v : nl2br(v)) + '</td></tr>').join('');
  return '<tr><td style="padding:6px 32px 0 32px"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">' + r + '</table></td></tr>';
}

export function paragraph(html, opts = {}) {
  return '<tr><td style="padding:' + (opts.pad || '14px 32px 0 32px') + '"><p style="margin:0;font-family:' + SANS + ';font-size:' + (opts.size || 15) + 'px;line-height:' + (opts.lh || 23) + 'px;color:' + (opts.color || C.ink) + '">' + html + '</p></td></tr>';
}

// Bulletproof button (a link inside a coloured table cell: renders in Outlook without VML).
export function button(href, label) {
  return '<tr><td style="padding:28px 32px 0 32px"><table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr>'
    + '<td bgcolor="' + C.charcoal + '" style="background:' + C.charcoal + ';border:1px solid ' + C.bronze + '">'
    + '<a href="' + esc(href) + '" style="display:inline-block;padding:14px 26px;font-family:' + SANS + ';font-size:14px;line-height:18px;font-weight:bold;letter-spacing:1px;color:#FFFFFF;text-decoration:none">' + esc(label) + '</a>'
    + '</td></tr></table></td></tr>';
}

export function layout({ lang = 'en', title, preheader = '', body, footerNote = '' }) {
  return '<!DOCTYPE html><html lang="' + esc(lang) + '" xmlns="http://www.w3.org/1999/xhtml"><head><meta charset="utf-8">'
    + '<meta name="viewport" content="width=device-width,initial-scale=1"><meta name="x-apple-disable-message-reformatting">'
    + '<meta name="color-scheme" content="light"><meta name="supported-color-schemes" content="light"><title>' + esc(title) + '</title>'
    + '<!--[if mso]><style>table,td,p,a{font-family:Arial,Helvetica,sans-serif!important}</style><![endif]-->'
    + '<style>@media only screen and (max-width:620px){.rd-wrap{width:100%!important}.rd-pad td{padding-left:20px!important;padding-right:20px!important}'
    + '.rd-pad .rd-k,.rd-pad .rd-v{display:block!important;width:100%!important;padding:0!important}.rd-pad .rd-k{padding-top:12px!important}.rd-pad .rd-v{padding-bottom:4px!important}'
    + '.rd-ref{font-size:24px!important;line-height:30px!important}}</style></head>'
    + '<body style="margin:0;padding:0;background:' + C.warm + ';-webkit-text-size-adjust:100%">'
    + '<div style="display:none;max-height:0;overflow:hidden;opacity:0;color:' + C.warm + '">' + esc(preheader) + '</div>'
    + '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="' + C.warm + '" style="background:' + C.warm + '"><tr><td align="center" style="padding:24px 12px">'
    + '<!--[if mso]><table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0"><tr><td><![endif]-->'
    + '<table role="presentation" class="rd-wrap" width="600" cellpadding="0" cellspacing="0" border="0" style="width:600px;max-width:600px">'
    // header
    + '<tr><td bgcolor="' + C.charcoal + '" align="center" style="background:' + C.charcoal + ';padding:30px 32px 26px 32px">'
    + headerMark()
    + '</td></tr>'
    + '<tr><td height="3" bgcolor="' + C.bronze + '" style="height:3px;line-height:3px;font-size:3px;background:' + C.bronze + '">&nbsp;</td></tr>'
    // body
    + '<tr><td bgcolor="' + C.paper + '" style="background:' + C.paper + ';padding:0 0 34px 0"><table role="presentation" class="rd-pad" width="100%" cellpadding="0" cellspacing="0" border="0">' + body + '</table></td></tr>'
    // footer
    + '<tr><td bgcolor="' + C.charcoal + '" align="center" style="background:' + C.charcoal + ';padding:24px 32px">'
    + '<p style="margin:0 0 4px 0;font-family:' + SANS + ';font-size:11px;letter-spacing:3px;color:#EDE6DA">RICARTI DRYWALL</p>'
    + '<p style="margin:0;font-family:' + SERIF + ';font-size:15px;font-style:italic;color:' + C.bronze + '">Perfection Starts Here!</p>'
    + (footerNote ? '<p style="margin:14px 0 0 0;font-family:' + SANS + ';font-size:11px;line-height:16px;color:' + C.soft + '">' + footerNote + '</p>' : '')
    + '</td></tr></table>'
    + '<!--[if mso]></td></tr></table><![endif]-->'
    + '</td></tr></table></body></html>';
}
