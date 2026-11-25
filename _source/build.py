"""Turn the Ricarti design artboards (.dc.html) into static site pages."""
import re, json, html, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import chrome

SRC = '/mnt/user-data/outputs/artifacts/5078cdd0-42b9-4fdb-9994-bd2a51044395/project/'
OUT = '/home/claude/ricarti-drywall-website/'
SITE = 'https://ricartidrywall.ca'

assets = json.load(open('/home/claude/photos/assets.json'))
BLOB = {v: k for k, v in assets.items()}
NAMES = {'hero': 'hero-kent.jpg'}
LOGOS = {
    '8f18e82e41c96b8822b5f013aa22b872': 'lockup-graphite.png',
    '6bcd78f61c0c3284734eb3518b7d95be': 'lockup-plaster.png',
    'b36d7fe08a5e00e321a00bf43658ad19': 'lockup-boxed-graphite.png',
    '31f71d7494217e17e2ba3d5008adb31b': 'lockup-boxed-plaster.png',
    'f651a7ab6da38a2fd262b66102a1b4fe': 'monogram-spruce.png',
    '36a5cd53d3dc37a487c2d15e1777acff': 'monogram-graphite.png',
}

def img_name(blob_id):
    if blob_id in LOGOS:
        return LOGOS[blob_id]
    k = BLOB[blob_id]
    if k in NAMES:
        return NAMES[k]
    m = re.match(r'([a-z]+)(\d+)$', k)
    return '%s-%s.jpg' % (m.group(1), m.group(2))

LINKS = {
    'Main.dc.html': '/',
    'Homeowners.dc.html': '/homeowners',
    'Builders.dc.html': '/builders',
    'Areas.dc.html': '/areas',
    'Finishing.dc.html': '/drywall-finishing-toronto',
    '#guides': '/journal',
    'Estimate.dc.html': '/estimate',
}


BASE_CSS = ''

BUSINESS = {
    "@type": "HomeAndConstructionBusiness",
    "@id": SITE + "/#business",
    "name": "Ricarti Drywall",
    "url": SITE + "/",
    "logo": SITE + "/images/lockup-graphite-refined.png",
    "image": SITE + "/images/hero-kent.jpg",
    "telephone": "+1-647-482-1139",
    "email": "cris@ricartidrywall.ca",
    "foundingDate": "2009",
    "founder": {"@type": "Person", "name": "Cris Ricarti", "jobTitle": "Owner"},
    "description": "Family-owned insulation, steel framing, drywall and finishing contractor for homeowners and builders across the Greater Toronto Area, Hamilton, Kitchener-Cambridge and Muskoka.",
    "address": {"@type": "PostalAddress", "streetAddress": "56 Hartley Ave", "addressLocality": "York", "addressRegion": "ON", "postalCode": "M6E 4E8", "addressCountry": "CA"},
    "areaServed": ["Toronto", "Greater Toronto Area", "Hamilton", "Kitchener", "Waterloo", "Cambridge", "Muskoka"],
    "sameAs": ["https://www.instagram.com/ricarti_drywall/", "https://www.facebook.com/ricartidrywall"],
    "knowsAbout": ["Drywall installation", "Drywall taping and finishing", "Level 5 drywall finish", "Spray foam insulation", "Batt insulation", "Steel stud framing", "Soundproofing", "Lath and plaster repair"],
}

def swap_chrome(body, out_path, ig=True):
    active = out_path or '/'
    body = body.replace('<!--HDR-->', chrome.header(active), 1)
    body = body.replace('<main ', '<main id="main" ', 1)
    cut = [i for i in (body.find('<footer style="max-width: 1440px'), body.find('<div class="rd-mob" style="position: sticky')) if i > -1]
    end = body.rstrip()
    body = body[:min(cut)] if cut else end[:end.rfind('</div>')]
    return body + (chrome.ig_strip() if ig and out_path != '/estimate' else '') + chrome.footer() + '</div>'

HEAD_COMMON = """<link rel="preload" href="/assets/fonts/cormorant-garamond.woff" as="font" type="font/woff" crossorigin>
<link rel="preload" href="/assets/fonts/archivo.woff" as="font" type="font/woff" crossorigin>
<link rel="stylesheet" href="/assets/site.css">"""
LOC = {'en': 'en_CA', 'pt': 'pt_BR', 'fr': 'fr_CA', 'it': 'it_IT', 'he': 'he_IL'}

def write_page(out_path, title, desc, body, helmet='', css='', extra_schema=None, lang='en', alts=None, image='hero-kent.jpg', ptype='WebPage', crumbs=None):
    body = d_palette(body); css = d_palette(css); helmet = d_palette(helmet)
    url = SITE + (out_path or '/')
    graph = [BUSINESS, {"@type": "WebPage" if ptype == 'BlogPosting' else ptype, "url": url, "name": title, "description": desc, "inLanguage": {'pt': 'pt-BR'}.get(lang, lang), "publisher": {"@id": SITE + "/#business"}}]
    if crumbs:
        graph.append({"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (n, u) in enumerate(crumbs)]})
    f = faq_schema(body)
    if f:
        graph.append(f)
    if extra_schema:
        graph.extend(extra_schema)
    schema = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)
    alts = alts or {'en': out_path or '/'}
    hl = ''.join('<link rel="alternate" hreflang="%s" href="%s%s">\n' % ({'pt': 'pt-BR'}.get(k, k), SITE, v) for k, v in alts.items())
    if 'en' in alts:
        hl += '<link rel="alternate" hreflang="x-default" href="%s%s">\n' % (SITE, alts['en'])
    page = """<!doctype html>
<html lang="%(lang)s"%(dir)s>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(title)s</title>
<meta name="description" content="%(desc)s">
<meta name="robots" content="noindex, nofollow">
<link rel="canonical" href="%(url)s">
%(hl)s<meta property="og:type" content="%(ogtype)s">
<meta property="og:site_name" content="Ricarti Drywall">
<meta property="og:title" content="%(title)s">
<meta property="og:description" content="%(desc)s">
<meta property="og:url" content="%(url)s">
<meta property="og:image" content="%(site)s/images/%(image)s">
<meta property="og:locale" content="%(locale)s">
<meta name="theme-color" content="#161616">
<link rel="icon" type="image/png" href="/images/monogram-graphite.png">
<link rel="apple-touch-icon" href="/images/monogram-graphite.png">
%(common)s
%(helmet)s
<style>%(css)s</style>
<script type="application/ld+json">
%(schema)s
</script>
<script src="/assets/site.js" defer></script>
</head>
<body>
%(body)s
</body>
</html>
""" % dict(lang={'pt': 'pt-BR'}.get(lang, lang), dir=' dir="rtl"' if lang == 'he' else '', title=html.escape(title), desc=html.escape(desc), url=url, site=SITE, hl=hl,
           ogtype='article' if ptype == 'BlogPosting' else 'website', image=image, locale=LOC[lang],
           common=HEAD_COMMON, helmet=helmet.strip(), css=BASE_CSS + css, schema=schema, body=body.strip())
    d = OUT + (out_path.strip('/') + '/' if out_path else '')
    os.makedirs(d, exist_ok=True)
    open(d + 'index.html', 'w').write(page)
    print('wrote', d + 'index.html', len(page))

D_MAP = [('#1E3129', '#161616'), ('#2E4A3F', '#7A5C38'), ('#24272A', '#161616'), ('#F7F5F0', '#F1EDE6'), ('#DDD7CB', '#D8D1C5'),
         ('#5E615F', '#5A554E'), ('#CBD8D0', '#D9BF95'), ('#5E7A6E', '#A8865A'), ('#EDE9E1', '#E8E2D8'),
         ("'Hanken Grotesk'", 'Archivo'), ('"Hanken Grotesk"', 'Archivo'), ('Hanken Grotesk', 'Archivo'), ('Literata', "'Cormorant Garamond'")]

def d_palette(s):
    """Concept D: map the old palette and fonts left in converted artboards (Areas, Estimate) to the new tokens."""
    for a, b in D_MAP:
        s = re.sub(re.escape(a), b, s, flags=re.I)
    return s

def faq_schema(body):
    items = []
    # Only real FAQ items (a summary with the + marker followed by one answer paragraph), never menus or toggles.
    for block in re.findall(r'<details\b[^>]*>(?:(?!<details\b).)*?</details>', body, re.S):
        m = re.match(r'<details[^>]*>\s*<summary[^>]*>((?:(?!</summary>).)*?rd-plus(?:(?!</summary>).)*)</summary>\s*<p[^>]*>(.*?)</p>\s*</details>$', block, re.S)
        if not m:
            continue
        q = re.sub(r'<[^>]+>', '', m.group(1)).replace('+', '').strip()
        a = re.sub(r'<[^>]+>', '', m.group(2)).strip()
        items.append({"@type": "Question", "name": html.unescape(q), "acceptedAnswer": {"@type": "Answer", "text": html.unescape(a)}})
    return {"@type": "FAQPage", "mainEntity": items} if items else None

def convert(src_name, out_path, title, desc, extra_schema=None):
    s = open(SRC + src_name).read()
    helmet = re.search(r'<helmet>(.*?)</helmet>', s, re.S).group(1)
    body = re.search(r'</helmet>(.*?)</x-dc>', s, re.S).group(1)
    helmet = re.sub(r'<link rel="stylesheet" href="https://fonts.googleapis.com[^>]*>', '', helmet)
    # hover attributes -> classes
    css = []
    def hov(m):
        tag = m.group(0)
        hv = re.search(r' style-hover="([^"]*)"', tag).group(1)
        n = len(css)
        rule = ';'.join(d.strip() + ' !important' for d in hv.split(';') if d.strip())
        css.append('.hv%d:hover{%s}' % (n, rule))
        tag = tag.replace(' style-hover="%s"' % hv, '')
        if ' class="' in tag:
            tag = tag.replace(' class="', ' class="hv%d ' % n, 1)
        else:
            tag = tag.replace('<a ', '<a class="hv%d" ' % n, 1).replace('<button ', '<button class="hv%d" ' % n, 1)
        return tag
    body = re.sub(r'<(?:a|button)\b[^>]*style-hover="[^"]*"[^>]*>', hov, body)
    body = body.replace('[Your name]', 'Cris Ricarti')
    for k, v in LINKS.items():
        body = body.replace('href="%s' % k, 'href="%s' % v)
    body = re.sub(r'/_blob/([0-9a-f]{32})', lambda m: '/images/' + img_name(m.group(1)), body)
    body = re.sub(r'<header\b.*?</header>', '<!--HDR-->', body, count=1, flags=re.S)
    # lazy-load images below the first one
    first = [True]
    def lazy(m):
        if first[0]:
            first[0] = False
            return m.group(0).replace('<img ', '<img fetchpriority="high" ', 1)
        return m.group(0).replace('<img ', '<img loading="lazy" decoding="async" ', 1)
    body = re.sub(r'<img [^>]*>', lazy, body)
    body = swap_chrome(body, out_path)
    write_page(out_path, title, desc, body, helmet, '\n'.join(css), extra_schema)


PAGES = [
    # Home page now comes from pages.py (editorial version)
    # /homeowners is now generated by pages.py (Task 006)
    # /builders is now generated by pages.py (Task 005)
    ('Areas.dc.html', '/areas', 'Service areas: GTA, Hamilton, Kitchener-Cambridge, Muskoka | Ricarti Drywall',
     'Ricarti Drywall works across Toronto and the Greater Toronto Area, plus Hamilton, Kitchener-Cambridge and the Muskoka region, for homeowners and builders.'),
    # /drywall-finishing-toronto is now generated by pages.py (Task 007)
]

if __name__ == '__main__':
    for p in PAGES:
        convert(*p)
