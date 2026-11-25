"""Translate the built English site into other languages.

Every text block is turned into a 'segment' with numbered placeholders for inline tags
(e.g. 'Know what you are <0>paying for.</0>'). Translations live in tm_<lang>.json
(translation memory), so only new or changed English text ever needs translating.
"""
import copy, html, json, os, re, sys
from bs4 import BeautifulSoup, NavigableString, Tag, Comment

ROOT = '/home/claude/ricarti-drywall-website/'
SITE = 'https://ricartidrywall.ca'
HERE = os.path.dirname(os.path.abspath(__file__))

URLS = {'pt': {
 '/': '/pt/', '/homeowners': '/pt/proprietarios', '/builders': '/pt/construtoras', '/areas': '/pt/areas-atendidas',
 '/drywall-finishing-toronto': '/pt/acabamento-de-drywall-toronto', '/estimate': '/pt/orcamento', '/journal': '/pt/guias',
 '/reviews': '/pt/avaliacoes', '/search': '/pt/busca',
 '/drywall-installation-toronto': '/pt/instalacao-de-drywall-toronto', '/insulation-spray-foam-toronto': '/pt/isolamento-e-espuma-projetada-toronto',
 '/architectural-drywall-finishing-toronto': '/pt/acabamentos-arquitetonicos-toronto', '/soundproofing-toronto': '/pt/isolamento-acustico-toronto',
 '/metal-stud-framing-toronto': '/pt/estrutura-em-perfis-de-aco-toronto',
 '/journal/spray-foam-vs-batt-insulation': '/pt/guias/espuma-ou-manta-isolamento-termico',
 '/journal/questions-to-ask-a-drywall-contractor': '/pt/guias/perguntas-antes-de-contratar-drywall',
 '/journal/soundproofing-a-room': '/pt/guias/isolamento-acustico-de-um-comodo',
 '/journal/lath-and-plaster-repair-toronto': '/pt/guias/reparo-de-reboco-em-casas-antigas-toronto',
 '/journal/what-a-drywall-subcontractor-needs-to-price-your-project': '/pt/guias/o-que-o-empreiteiro-de-drywall-precisa-para-orcar',
}}
HTML_LANG = {'pt': 'pt-BR'}
OG_LOCALE = {'pt': 'pt_BR'}

BLOCK = set('html body head div section article aside header footer main nav ul ol li dl dt dd p h1 h2 h3 h4 h5 h6 figure figcaption blockquote table thead tbody tr td th form fieldset legend label select option textarea button details summary address dialog title'.split())
VOID = set('br img input hr wbr source meta link'.split())
SKIP = set('script style svg noscript'.split())
BLOCKISH_CLASSES = {'rd-card', 'rd-row', 'rd-ct', 'rd-label', 'n', 'h', 'd', 'rd-cap', 'rd-lb', 'u', 't', 's'}
ATTRS = ('alt', 'placeholder', 'aria-label', 'title')

def is_block(t):
    if t.name in BLOCK:
        return True
    st = (t.get('style') or '').replace(' ', '')
    if 'display:block' in st or 'display:grid' in st or 'display:flex' in st or 'display:inline-block' in st:
        return True
    return bool(set(t.get('class') or []) & BLOCKISH_CLASSES)

def roots(soup):
    """Elements that hold a run of translatable inline text."""
    seen, out = set(), []
    for s in soup.find_all(string=True):
        if isinstance(s, Comment) or not s.strip():
            continue
        p = s.parent
        if any(a.name in SKIP for a in [p] + list(p.parents)):
            continue
        while p is not None and not is_block(p):
            p = p.parent
        if p is None or id(p) in seen:
            continue
        seen.add(id(p)); out.append(p)
    return out

def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def key_of(el, tags):
    parts = []
    for c in el.children:
        if isinstance(c, Comment):
            continue
        if isinstance(c, NavigableString):
            parts.append(esc(str(c)))
        elif isinstance(c, Tag):
            i = len(tags); tags.append(c)
            if c.name in VOID or c.name in SKIP or not c.contents or is_block(c):
                parts.append('<%d/>' % i)
            else:
                parts.append('<%d>%s</%d>' % (i, key_of(c, tags), i))
    return ''.join(parts)

def norm_key(k):
    lead = re.match(r'^\s*', k).group(0); trail = re.search(r'\s*$', k).group(0)
    return lead, re.sub(r'\s+', ' ', k.strip()), trail

def open_close(t):
    if t.name in SKIP or (t.name not in VOID and (is_block(t) or not t.contents)):
        return str(t), ''
    t2 = copy.copy(t); t2.clear(); s = str(t2)
    if t.name in VOID:
        return s, ''
    i = s.rfind('</')
    return s[:i], s[i:]

def plain(k):
    return html.unescape(re.sub(r'</?\d+/?>', '', k)).strip()

def pages():
    for d, _, files in os.walk(ROOT):
        rel = '/' + os.path.relpath(d, ROOT).strip('.').strip('/')
        rel = '/' if rel == '/' else rel
        if 'index.html' in files and rel in URLS['pt']:
            yield rel, os.path.join(d, 'index.html')

def extract():
    """Collect every English segment and attribute string from the built pages."""
    segs, attrs = {}, {}
    for rel, path in pages():
        soup = BeautifulSoup(open(path).read(), 'lxml')
        for r in roots(soup):
            tags = []; _, k, _ = norm_key(key_of(r, tags))
            if k and re.search(r'[A-Za-z]', plain(k)):
                segs.setdefault(k, rel)
        for a in ATTRS:
            for t in soup.find_all(attrs={a: True}):
                v = t[a].strip()
                if v and re.search(r'[A-Za-z]{2}', v):
                    attrs.setdefault(v, rel)
        for m in soup.find_all('meta', attrs={'name': 'description'}) + soup.find_all('meta', attrs={'property': ['og:title', 'og:description']}):
            attrs.setdefault(m['content'].strip(), rel)
    return segs, attrs

def load_tm(lang):
    p = os.path.join(HERE, 'tm_%s.json' % lang)
    return json.load(open(p)) if os.path.exists(p) else {}

def map_url(href, lang):
    if not href or href.startswith(('http', 'mailto:', 'tel:', '#', '/images/', '/assets/')):
        return href
    m = re.match(r'^([^?#]*)(.*)$', href)
    path, rest = m.group(1).rstrip('/') or '/', m.group(2)
    if path in URLS[lang]:
        return URLS[lang][path] + rest
    return href

def fill(k_tr, tags):
    def rep(m):
        i = int(m.group(2)); t = tags[i]; o, c = open_close(t)
        if m.group(3):
            return o + c
        return c if m.group(1) else o
    return re.sub(r'<(/?)(\d+)(/?)>', rep, k_tr)

def translate_page(rel, path, lang, tm, missing):
    src = open(path).read()
    soup = BeautifulSoup(src, 'lxml')
    segs, attrs = tm.get('segments', {}), tm.get('attrs', {})
    for r in sorted(roots(soup), key=lambda e: -len(list(e.parents))):
        tags = []; lead, k, trail = norm_key(key_of(r, tags))
        if not k or not re.search(r'[A-Za-z]', plain(k)):
            continue
        tr = segs.get(k)
        if tr is None:
            missing['segments'][k] = rel; continue
        new = BeautifulSoup('<x>%s%s%s</x>' % (lead, fill(tr, tags), trail), 'lxml').x
        r.clear()
        for c in list(new.contents):
            r.append(c)
    for a in ATTRS:
        for t in soup.find_all(attrs={a: True}):
            v = t[a].strip()
            if v and re.search(r'[A-Za-z]{2}', v):
                if v in attrs: t[a] = attrs[v]
                else: missing['attrs'][v] = rel
    for m in soup.find_all('meta', attrs={'name': 'description'}) + soup.find_all('meta', attrs={'property': ['og:title', 'og:description']}):
        v = m['content'].strip()
        if v in attrs: m['content'] = attrs[v]
        else: missing['attrs'][v] = rel
    # links, forms
    for t in soup.find_all(['a', 'link', 'form']):
        att = 'action' if t.name == 'form' else 'href'
        if t.name == 'link' or t.get('hreflang') is not None:
            continue
        if t.get(att):
            t[att] = map_url(t[att], lang)
    for a in soup.select('.rd-sugg a, #rd-psugg a'):
        a['href'] = URLS[lang]['/search'] + '?q=' + a.get_text().strip().replace(' ', '+')
    for a in soup.select('a[hreflang]'):
        if a.has_attr('aria-current'): del a['aria-current']
        if a['hreflang'] == lang: a['aria-current'] = 'true'
    # head
    soup.html['lang'] = HTML_LANG.get(lang, lang)
    newurl = URLS[lang][rel]
    soup.find('link', rel='canonical')['href'] = SITE + newurl
    soup.find('meta', property='og:url')['content'] = SITE + newurl
    soup.find('meta', property='og:locale')['content'] = OG_LOCALE[lang]
    # JSON-LD: translate strings we know, swap URLs and language
    plain_map = {plain(k): plain(v) for k, v in segs.items()}
    plain_map.update(attrs)
    def walk(o):
        if isinstance(o, dict):
            return {k: walk(v) for k, v in o.items()}
        if isinstance(o, list):
            return [walk(v) for v in o]
        if isinstance(o, str):
            if o.startswith(SITE):
                p = o[len(SITE):]; q = map_url(p, lang)
                return SITE + q if q != p else o
            return plain_map.get(o.strip(), o)
        return o
    for s in soup.find_all('script', type='application/ld+json'):
        data = walk(json.loads(s.string))
        for g in data.get('@graph', []):
            if 'inLanguage' in g: g['inLanguage'] = HTML_LANG.get(lang, lang)
        s.string = '\n' + json.dumps(data, ensure_ascii=False, indent=1) + '\n'
    title = soup.find('title')
    if title.get_text() in attrs: title.string = attrs[title.get_text()]
    elif title.get_text() not in attrs.values(): missing['attrs'][title.get_text()] = rel
    for m in soup.find_all('meta', property='og:title'):
        m['content'] = title.get_text()
    out = str(soup)
    out = out.replace('/search-index.json', '/%s/search-index.json' % lang)
    # page-specific scripts (estimate form, search page)
    for en, tr in tm.get('scripts', {}).items():
        out = out.replace(en, tr)
    dest = ROOT + newurl.strip('/') + '/index.html'
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    open(dest, 'w').write(out)
    return dest

def search_index(lang):
    items = json.load(open(ROOT + 'search-index.json'))
    out = []
    for it in items:
        u = URLS[lang].get(it['u'])
        if not u: continue
        s = open(ROOT + u.strip('/') + '/index.html').read()
        soup = BeautifulSoup(s, 'lxml')
        main = soup.find('main')
        for x in main.find_all(['script', 'style', 'nav']): x.decompose()
        k = main.find('p', class_='rd-kicker')
        if k: k.decompose()
        txt = re.sub(r'\s+', ' ', main.get_text(' ')).strip()
        title = soup.title.get_text().split(' | ')[0]
        if it['u'] == '/': title = 'Ricarti Drywall — início'
        kinds = {'Home': 'Início', 'Service': 'Serviço', 'Homeowners': 'Proprietários', 'Builders': 'Construtoras', 'Journal': 'Guias', 'Service areas': 'Áreas atendidas', 'Contact': 'Contato', 'Reviews': 'Avaliações', 'Page': 'Página'}
        out.append({'u': u, 't': title, 'd': soup.find('meta', attrs={'name': 'description'})['content'], 'k': kinds.get(it['k'], it['k']), 'x': txt[:6000]})
    json.dump(out, open(ROOT + '%s/search-index.json' % lang, 'w'), ensure_ascii=False, separators=(',', ':'))

LANG_NAMES = [('en', 'EN', 'English'), ('pt', 'PT', 'Português')]

def relink(lang_list=('en', 'pt')):
    """Put matching language switches and hreflang tags on every English page and its translations."""
    for en, pt in URLS['pt'].items():
        alts = {'en': en, 'pt': pt}
        for lang in lang_list:
            path = ROOT + alts[lang].strip('/') + ('/' if alts[lang] != '/' else '') + 'index.html'
            path = path.replace('//', '/')
            if not os.path.exists(path):
                continue
            soup = BeautifulSoup(open(path).read(), 'lxml')
            def links(short):
                out = []
                for code, sh, name in LANG_NAMES:
                    a = soup.new_tag('a', href=alts[code], lang=HTML_LANG.get(code, code), hreflang=HTML_LANG.get(code, code))
                    a.string = sh if short else name
                    if code == lang: a['aria-current'] = 'true'
                    out.append(a)
                return out
            for box, short in [(soup.select_one('.rd-top .rd-langs'), True), (soup.select_one('.rd-mlangs'), False), (soup.select_one('.rd-foot nav[aria-label="Language"]'), False)]:
                if box is None: continue
                box.clear()
                for a in links(short): box.append(a)
            for l in soup.find_all('link', rel='alternate'):
                l.decompose()
            canon = soup.find('link', rel='canonical')
            for code in ('en', 'pt', 'x-default'):
                l = soup.new_tag('link', rel='alternate', hreflang=HTML_LANG.get(code, code), href=SITE + alts['en' if code == 'x-default' else code])
                canon.insert_after(l)
            open(path, 'w').write(str(soup))

if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'extract':
        segs, attrs = extract()
        tm = load_tm('pt')
        todo = {'segments': {k: v for k, v in segs.items() if k not in tm.get('segments', {})},
                'attrs': {k: v for k, v in attrs.items() if k not in tm.get('attrs', {})}}
        json.dump(todo, open(os.path.join(HERE, 'todo_pt.json'), 'w'), ensure_ascii=False, indent=1)
        print('segments', len(segs), 'attrs', len(attrs), '| to translate:', len(todo['segments']), len(todo['attrs']),
              '| words', sum(len(plain(k).split()) for k in todo['segments']) + sum(len(k.split()) for k in todo['attrs']))
    elif cmd == 'build':
        lang = sys.argv[2]; tm = load_tm(lang); missing = {'segments': {}, 'attrs': {}}
        for rel, path in list(pages()):
            translate_page(rel, path, lang, tm, missing)
        search_index(lang)
        json.dump(missing, open(os.path.join(HERE, 'missing_%s.json' % lang), 'w'), ensure_ascii=False, indent=1)
        print('missing', len(missing['segments']), len(missing['attrs']))
        relink()
