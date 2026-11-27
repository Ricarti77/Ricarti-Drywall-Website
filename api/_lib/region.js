// Location parsing and regional routing (Ontario / British Columbia). Best effort: the raw text is always kept.
const PROV_BY_FSA = { A: 'NL', B: 'NS', C: 'PE', E: 'NB', G: 'QC', H: 'QC', J: 'QC', K: 'ON', L: 'ON', M: 'ON', N: 'ON', P: 'ON',
  R: 'MB', S: 'SK', T: 'AB', V: 'BC', X: 'NT', Y: 'YT' };
const PROV_WORDS = [['ON', /\b(ontario|ont\.?|on)\b/i], ['BC', /\b(british columbia|b\.c\.|bc)\b/i], ['QC', /\b(quebec|québec|qc)\b/i], ['AB', /\b(alberta|ab)\b/i]];
const CITIES = [
  ['Toronto', 'ON'], ['North York', 'ON'], ['Etobicoke', 'ON'], ['Scarborough', 'ON'], ['East York', 'ON'], ['York', 'ON'],
  ['Mississauga', 'ON'], ['Brampton', 'ON'], ['Caledon', 'ON'], ['Vaughan', 'ON'], ['Richmond Hill', 'ON'], ['Markham', 'ON'],
  ['King City', 'ON'], ['Aurora', 'ON'], ['Newmarket', 'ON'], ['Oakville', 'ON'], ['Burlington', 'ON'], ['Milton', 'ON'],
  ['Halton Hills', 'ON'], ['Pickering', 'ON'], ['Ajax', 'ON'], ['Whitby', 'ON'], ['Oshawa', 'ON'], ['Hamilton', 'ON'],
  ['Ancaster', 'ON'], ['Dundas', 'ON'], ['Stoney Creek', 'ON'], ['Waterdown', 'ON'], ['Kitchener', 'ON'], ['Waterloo', 'ON'],
  ['Cambridge', 'ON'], ['Huntsville', 'ON'], ['Bracebridge', 'ON'], ['Gravenhurst', 'ON'], ['Port Carling', 'ON'], ['Lake of Bays', 'ON'],
  ['Vancouver', 'BC'], ['North Vancouver', 'BC'], ['West Vancouver', 'BC'], ['Burnaby', 'BC'], ['Surrey', 'BC'], ['Richmond', 'BC'],
  ['Coquitlam', 'BC'], ['Port Coquitlam', 'BC'], ['Port Moody', 'BC'], ['New Westminster', 'BC'], ['Langley', 'BC'], ['Delta', 'BC'],
].sort((a, b) => b[0].length - a[0].length);

export function parseLocation(text) {
  const raw = String(text || '');
  const m = raw.match(/\b([ABCEGHJ-NPRSTVXY])(\d)([ABCEGHJ-NPRSTV-Z])[ -]?(\d)([ABCEGHJ-NPRSTV-Z])(\d)\b/i);
  const postal = m ? (m[1] + m[2] + m[3] + ' ' + m[4] + m[5] + m[6]).toUpperCase() : '';
  let province = postal ? PROV_BY_FSA[postal[0]] || '' : '';
  let city = '';
  for (const [name, prov] of CITIES) {
    if (new RegExp('\\b' + name.replace(/ /g, '\\s+') + '\\b', 'i').test(raw)) { city = name; if (!province) province = prov; break; }
  }
  if (!province) for (const [code, re] of PROV_WORDS) if (re.test(raw)) { province = code; break; }
  return { raw, city, province, postal_code: postal, country: province ? 'CA' : '', confidence: postal ? 'postal-code' : city ? 'city-name' : province ? 'province-name' : 'none' };
}

export function route(loc) {
  const region = loc.province === 'ON' ? 'ontario' : loc.province === 'BC' ? 'british-columbia' : loc.province ? 'other-canada' : 'unknown';
  // location_status keeps "we could not tell" apart from "outside Ontario": an incomplete address only needs verifying.
  const location_status = loc.province === 'ON' ? (loc.city || loc.postal_code ? 'ontario' : 'ontario-unconfirmed')
    : loc.province ? 'outside-ontario' : 'requires-verification';
  return { region, location_status, served: region === 'ontario' ? true : region === 'unknown' ? null : false, needs_review: location_status !== 'ontario' };
}
