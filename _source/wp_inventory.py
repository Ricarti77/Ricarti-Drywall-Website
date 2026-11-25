"""Read a WordPress export (WXR .xml from Tools > Export > All content) and produce the migration inventory.

    python3 wp_inventory.py export.xml [search-console-pages.csv] > inventory.csv

For every published post and page it records URL, title, date, word count, categories, the SEO title/description
(Yoast or Rank Math, when present), the media it uses, and a SUGGESTED classification:

  migrate      substantive (600+ words), on a core service topic, no overlap with an existing Journal article
  consolidate  overlaps an existing Journal article or service page: merge any useful points there, 301 to it
  owner-review thin (<300 words), off-topic, or contains claims that need checking (prices, certifications,
               reviews/testimonials, locations outside the service area such as Vancouver/BC)
  retire       thin AND no clicks/links in the Search Console file (when supplied): 301 to /journal

The suggestion is only a starting point; the owner decides. Nothing is published or redirected by this script.
"""
import csv, html, re, sys, xml.etree.ElementTree as ET
from urllib.parse import urlparse

NS = {'wp': 'http://wordpress.org/export/1.2/', 'content': 'http://purl.org/rss/1.0/modules/content/',
      'dc': 'http://purl.org/dc/elements/1.1/', 'excerpt': 'http://wordpress.org/export/1.2/excerpt/'}

# topic -> new destination, with the words that signal it
TOPICS = [
    ('/journal/spray-foam-vs-batt-insulation', ['spray foam', 'batt', 'closed-cell', 'open-cell', 'r-value', 'insulat']),
    ('/journal/soundproofing-a-room', ['soundproof', 'acoustic', 'echo', 'noise', 'stc', 'resilient channel', 'mineral wool']),
    ('/journal/lath-and-plaster-repair-toronto', ['plaster', 'lath', 'older home', 'heritage']),
    ('/journal/questions-to-ask-a-drywall-contractor', ['hire', 'hiring', 'contractor', 'quote', 'review', 'choose']),
    ('/journal/what-a-drywall-subcontractor-needs-to-price-your-project', ['builder', 'subcontract', 'townhouse', 'bid', 'drawings']),
    ('/drywall-finishing-toronto', ['level 5', 'level 4', 'taping', 'skim', 'finish', 'popcorn', 'ceiling']),
    ('/metal-stud-framing-toronto', ['steel stud', 'metal stud', 'framing', 'bulkhead']),
    ('/architectural-drywall-finishing-toronto', ['curved', 'arch', 'reveal', 'trimless', 'niche']),
    ('/drywall-installation-toronto', ['drywall', 'gypsum', 'type x', 'moisture']),
]
RISKY = re.compile(r'\$\s?\d|\bprice[sd]?\b|\bcost[s]?\b|certif|licensed|award|guarantee|warrant|\breview(s|ed)?\b|testimonial|vancouver|british columbia|\bbc\b|burnaby|coquitlam', re.I)

def text(el):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', el or ''))).strip()

def topic(t):
    t = t.lower(); best, score = '/journal', 0
    for dest, words in TOPICS:
        s = sum(t.count(w) for w in words)
        if s > score: best, score = dest, s
    return best, score

def main():
    tree = ET.parse(sys.argv[1]); ch = tree.getroot().find('channel')
    gsc = {}
    if len(sys.argv) > 2:
        for r in csv.DictReader(open(sys.argv[2], encoding='utf-8-sig')):
            u = r.get('Top pages') or r.get('Page') or r.get('URL') or ''
            gsc[urlparse(u).path.rstrip('/') or '/'] = (int(float(r.get('Clicks', 0) or 0)), int(float(r.get('Impressions', 0) or 0)))
    out = csv.writer(sys.stdout)
    out.writerow(['type', 'old_path', 'title', 'date', 'words', 'categories', 'seo_title', 'seo_description', 'images',
                  'clicks', 'impressions', 'suggested', 'suggested_destination', 'flags'])
    for it in ch.findall('item'):
        ptype = it.findtext('wp:post_type', namespaces=NS); status = it.findtext('wp:status', namespaces=NS)
        if ptype not in ('post', 'page') or status != 'publish':
            continue
        link = it.findtext('link') or ''; path = urlparse(link).path.rstrip('/') or '/'
        body = it.findtext('content:encoded', namespaces=NS) or ''; words = len(text(body).split())
        title = text(it.findtext('title')); cats = [text(c.text) for c in it.findall('category') if c.get('domain') == 'category']
        meta = {m.findtext('wp:meta_key', namespaces=NS): m.findtext('wp:meta_value', namespaces=NS) for m in it.findall('wp:postmeta', namespaces=NS)}
        seo_t = meta.get('_yoast_wpseo_title') or meta.get('rank_math_title') or ''
        seo_d = meta.get('_yoast_wpseo_metadesc') or meta.get('rank_math_description') or ''
        imgs = len(re.findall(r'<img\b', body))
        dest, score = topic(title + ' ' + text(body)[:4000])
        clicks, impr = gsc.get(path, ('', ''))
        flags = []
        if RISKY.search(text(body)): flags.append('claims-to-check')
        if words < 300: flags.append('thin')
        if score == 0: flags.append('off-topic')
        if ptype == 'page': sug = 'page (map by hand)'
        elif words < 300 and gsc and not clicks: sug = 'retire'
        elif 'thin' in flags or 'off-topic' in flags or 'claims-to-check' in flags: sug = 'owner-review'
        elif dest.startswith('/journal/') and score >= 4: sug = 'consolidate'
        elif words >= 600: sug = 'migrate'
        else: sug = 'consolidate'
        out.writerow([ptype, path, title, (it.findtext('wp:post_date', namespaces=NS) or '')[:10], words, '; '.join(cats),
                      seo_t, seo_d, imgs, clicks, impr, sug, dest if sug != 'migrate' else '/journal/' + path.strip('/').split('/')[-1], ' '.join(flags)])

if __name__ == '__main__':
    main()
