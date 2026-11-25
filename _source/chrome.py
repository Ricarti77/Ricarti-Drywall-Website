"""Shared header, search dialog, Instagram strip and footer for every page."""
import json as _jn, os as _on
_json_nav = _jn.load(open(_on.path.join(_on.path.dirname(_on.path.abspath(__file__)), 'content', 'navigation.json')))

IG = 'https://www.instagram.com/ricarti_drywall/'
SEARCH_SVG = '<svg class="rd-ico" viewBox="0 0 24 24" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5 21 21"/></svg>'
IG_SVG = '<svg class="rd-ico" viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.3" cy="6.7" r=".6" fill="currentColor"/></svg>'

# Concept D. Only languages that have pages are ever shown; Spanish and French are prepared but not published.
LANGS = [('en', 'EN', 'English'), ('pt', 'PT', 'Português'), ('es', 'ES', 'Español'), ('fr', 'FR', 'Français'), ('it', 'IT', 'Italiano')]
MENU_SVG = '<svg viewBox="0 0 24 9" aria-hidden="true"><path d="M0 .6h24M0 8.4h15"/></svg>'
CARET_SVG = '<svg viewBox="0 0 9 6" aria-hidden="true"><path d="M.5.8l4 4 4-4"/></svg>'
PHONE_SVG = '<svg class="rd-ico" viewBox="0 0 14 14" aria-hidden="true"><path d="M3 1h2.5l1 3-1.5 1a7 7 0 0 0 4 4l1-1.5 3 1V11a2 2 0 0 1-2 2A11 11 0 0 1 1 3a2 2 0 0 1 2-2z"/></svg>'
SVC_LINES = {
 'drywall': 'Type X · moisture-resistant · multi-layer',
 'insulation': 'Closed-cell · batt · mineral wool · attic',
 'finishing': 'Taping · skim coat · smooth ceilings',
 'architectural': 'Curves · reveals · flush vents · trimless',
 'acoustic': 'Resilient channel · acoustic batts · layers',
 'framing': 'Non-load-bearing · bulkheads · partitions',
}

T = {
 'en': dict(
   nav=[('/#projects', 'Projects', ''), ('/builders', 'Builders', 'rd-hl-x'), ('/homeowners', 'Homeowners', 'rd-hl-x')],
   main=[('/#services', 'Services'), ('/#projects', 'Projects'), ('/builders', 'For builders'), ('/homeowners', 'For homeowners')],
   sub=[('/#about', 'About'), ('/reviews', 'Reviews'), ('/journal', 'Journal'), ('/areas', 'Service areas'), ('#contact', 'Contact'), ('/', 'Home')],
   svc_label='Services', svc_all='All services', who='Who we work with',
   who_links=[('/builders', 'For builders'), ('/homeowners', 'For homeowners'), ('/#projects', 'Selected projects'), ('/estimate', 'Request an Estimate')],
   areas='Service areas', search='Search the site', search_ph='Search: spray foam, Level 5, soundproofing…', close='CLOSE', menu='Menu', menu_close='Close',
   sugg='Popular:', sugg_list=['Level 5 finish', 'Spray foam', 'Soundproofing', 'Plaster repair', 'Builders', 'WSIB'],
   est='Request an Estimate', enq='Enquire', call='Call', est_short='Estimate', skip='Skip to content', home='Ricarti Drywall, home',
   lang_label='Language', slogan='Perfection Starts Here!', region='Toronto · GTA · Hamilton · Kitchener–Cambridge · Muskoka',
   ig_k='On Instagram', ig_h='Fresh off the trowel.', ig_follow='Follow @ricarti_drywall',
   f_blurb='Insulation, steel framing, drywall and architectural finishing for homes across the GTA, Hamilton, Kitchener–Cambridge and Muskoka. Family-owned since 2009.',
   f_services='Services', f_company='Company', f_contact='Contact',
   services=[(x['url'], x['label']) for x in _json_nav['services']],
   company=[('/homeowners', 'For homeowners'), ('/builders', 'For builders'), ('/areas', 'Service areas'), ('/journal', 'Journal'), ('/reviews', 'Reviews'), ('/estimate', 'Estimate & site visit')],
   hours='[Mon–Fri hours]', legal='© 2026 [Legal company name] · WSIB [account no.] · [$X M] liability',
   disclaimer='Translations of this site are provided for convenience and have not been professionally reviewed. If a translated page differs from the English, the English version applies. All content is general information, not a quote or contract.'),
}

def _a(href, text, active, attrs=''):
    cur = ' aria-current="page"' if active == href else ''
    return '<a href="%s"%s%s>%s</a>' % (href, cur, attrs, text)

def lang_links(lang, alts, short=False):
    """alts: dict lang -> url, only for pages that exist in that language (i18n.relink rewrites these per page)."""
    out = []
    for code, sh, name in LANGS:
        href = alts.get(code)
        if not href:
            continue
        cur = ' aria-current="true"' if code == lang else ''
        out.append('<a href="%s" lang="%s" hreflang="%s" data-short="%s"%s>%s</a>' % (href, code, code, sh, cur, sh if short else name))
    return ''.join(out)

HEADER = '''<div><a class="rd-skip" href="#main">%(skip)s</a></div>
<header class="rd-head%(over)s"><div>
<div class="rd-hl">
<details class="rd-menu"><summary aria-label="%(menu)s">%(msvg)s<span class="rd-m-open rd-m-t">%(menu)s</span><span class="rd-m-close rd-m-t">%(mclose)s</span></summary>
<div class="rd-panel-m" role="dialog" aria-modal="true" aria-label="%(menu)s">
<div class="rd-pm-top"><a href="%(home)s" aria-label="%(home_l)s"><img src="/images/lockup-plaster-refined.png" alt="Ricarti Drywall" width="264" height="52"></a></div>
<div class="rd-pm-body">
<nav class="rd-pm-main" aria-label="%(menu)s">
<button type="button" class="rd-pm-search" data-open-search data-cta="search" data-cta-loc="menu">%(ssvg)s<span>%(search)s</span></button>
%(main)s<div class="rd-pm-sub">%(sub)s</div></nav>
<details class="rd-pm-svcd" open><summary><span>%(svc_l)s</span>%(caret)s</summary><ol class="rd-pm-svc">%(svc)s</ol><a class="rd-pm-all" href="/#services">%(svc_all)s →</a></details>
<div class="rd-pm-side">
<img src="/images/svc-architectural-480.jpg" alt="" width="480" height="600" loading="lazy" decoding="async">
<address><a href="tel:+16474821139" data-cta="call" data-cta-loc="menu">(647) 482-1139</a><br><a href="mailto:cris@ricartidrywall.ca" data-cta="email" data-cta-loc="menu">cris@ricartidrywall.ca</a><br><a href="%(ig)s" rel="noopener">Instagram · @ricarti_drywall</a></address>
<nav class="rd-mlangs" aria-label="%(lang_l)s">%(langs_s)s</nav>
<a class="rd-pm-est" href="/estimate" data-cta="estimate" data-cta-loc="menu">%(est)s</a>
</div>
</div>
<div class="rd-pm-foot"><div><em>%(slogan)s</em><span>%(region)s</span></div></div>
</div>
</details>
<details class="rd-svcdd"><summary%(svc_cur)s>%(svc_l)s%(caret)s</summary><div class="rd-svcdd-p"><div>
<ol class="rd-pm-svc">%(svc)s</ol>
<nav class="rd-svcdd-side" aria-label="%(svc_l)s"><p>%(who)s</p>%(who_links)s<a class="rd-pm-all" href="/#services">%(svc_all)s →</a></nav>
</div></div></details>
%(nav)s
</div>
<a href="%(home)s" class="rd-logo" aria-label="%(home_l)s"><img src="/images/lockup-plaster-refined.png" alt="Ricarti Drywall" width="264" height="52"></a>
<div class="rd-hr">
<details class="rd-lang"><summary aria-label="%(lang_l)s: %(cur)s"><span class="rd-lang-cur">%(cur)s</span>%(caret)s</summary><nav class="rd-lang-list" aria-label="%(lang_l)s">%(langs)s</nav></details>
<button type="button" class="rd-hsearch" data-open-search data-cta="search" data-cta-loc="header" aria-label="%(search)s">%(ssvg)s</button>
<a class="rd-enq" href="mailto:cris@ricartidrywall.ca" data-cta="email" data-cta-loc="header">%(enq)s</a>
<a class="rd-est" href="/estimate" data-cta="estimate" data-cta-loc="header"><span class="rd-est-l">%(est)s</span><span class="rd-est-s">%(est_s)s</span></a>
</div>
</div></header>
<dialog id="rd-search" class="rd-dlg" aria-label="%(search)s"><div class="rd-panel">
<form class="rd-sform" action="/search" role="search">%(ssvg)s<input id="rd-q" name="q" type="search" autocomplete="off" placeholder="%(sph)s" aria-label="%(search)s"><button type="button" id="rd-sclose">%(close)s</button></form>
<div id="rd-sugg" class="rd-sugg">%(sugg)s %(sugglinks)s</div>
<ul id="rd-res" class="rd-res" aria-live="polite"></ul>
</div></dialog>
'''

SVC_URLS = [x['url'] for x in _json_nav['services']]

def header(active='', lang='en', alts=None, over=False):
    t = T[lang]; alts = alts or {'en': active or '/'}
    home = '/' if lang == 'en' else '/%s/' % lang
    cur_short = [s for c, s, _ in LANGS if c == lang][0]
    svc = ''.join('<li><a href="%s"%s><span class="n">%02d</span><span><span class="h">%s</span><span class="d">%s</span></span></a></li>'
                  % (x['url'], ' aria-current="page"' if active == x['url'] else '', i + 1, x['label'].replace('&', '&amp;'), SVC_LINES.get(x['id'], ''))
                  for i, x in enumerate(_json_nav['services']))
    main = ''.join(_a(h, x, active, ' class="rd-pm-svclink"' if h == '/#services' else '') for h, x in t['main'])
    return HEADER % dict(skip=t['skip'], over=' rd-over' if over else '', menu=t['menu'], mclose=t['menu_close'], msvg=MENU_SVG, home=home, home_l=t['home'],
           main=main, sub=''.join(_a(h, x, active) for h, x in t['sub']),
           search=t['search'], svc=svc, ig=IG, lang_l=t['lang_label'], langs_s=lang_links(lang, alts, True),
           langs=lang_links(lang, alts), est=t['est'], slogan=t['slogan'], region=t['region'], cur=cur_short, caret=CARET_SVG,
           svc_l=t['svc_label'], svc_all=t['svc_all'], who=t['who'], who_links=''.join(_a(h, x, active) for h, x in t['who_links']),
           svc_cur=' class="is-active"' if active in SVC_URLS else '', est_s=t['est_short'],
           nav=''.join(_a(h, x, active, ' class="%s"' % c if c else '') for h, x, c in t['nav']), enq=t['enq'], ssvg=SEARCH_SVG, sph=t['search_ph'], close=t['close'], sugg=t['sugg'],
           sugglinks=''.join('<a href="/search?q=%s">%s</a>' % (s.replace(' ', '+'), s) for s in t['sugg_list']))

# Project album: every photo, grouped by project (street and city only, never house numbers).
import json as _json, os as _os
_PROJ = _json.load(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), 'content', 'projects.json')))
# Album = every published project photo, in project order (single source of truth: content/projects.json)
ALBUM = [(ph['file'], ph['caption']['en']) for pr in _PROJ['projects'] if pr.get('published') for ph in pr['photos']]
TILES = ['brule-04.jpg', 'kent-03.jpg', 'stanton-02.jpg', 'brule-07.jpg', 'lauther-02.jpg', 'stanton-04.jpg']
T['en'].update(album_k='Project album', album_h='Fresh off the trowel.', album_all='View all %d photos')

def ig_strip(lang='en'):
    t = T[lang]; idx = {f: i for i, (f, _) in enumerate(ALBUM)}
    tiles = ''.join('<a href="/images/%s" data-lb="%d"><img src="/images/%s" alt="%s" loading="lazy" decoding="async" width="300" height="300"><span>%s</span></a>'
                    % (f, idx[f], f, ALBUM[idx[f]][1], ALBUM[idx[f]][1].split(',')[0].upper()) for f in TILES)
    album = ''.join('<li data-src="/images/%s">%s</li>' % (f, c) for f, c in ALBUM)
    return ('<section class="rd-ig" aria-labelledby="ig-h"><header><div><p class="rd-kicker">%s</p><h2 id="ig-h">%s</h2></div>'
            '<div style="display:flex;flex-wrap:wrap;gap:12px"><button type="button" class="rd-btn" data-lb="0">%s</button><a class="rd-btn-o" href="%s" rel="noopener">%s %s</a></div></header>'
            '<div class="rd-grid">%s</div><ul class="rd-album" hidden>%s</ul></section>\n'
            % (t['album_k'], t['album_h'], t['album_all'] % len(ALBUM), IG, IG_SVG, t['ig_follow'], tiles, album))

FOOTER = '''<footer class="rd-foot"><div><div class="rd-cols">
<div class="rd-f-brand"><img src="/images/lockup-plaster-refined.png" alt="Ricarti Drywall" width="203" height="40" loading="lazy" style="height:40px;width:auto;display:block"><em>%(slogan)s</em><p>%(blurb)s</p></div>
<div><h2>%(fs)s</h2><ul>%(services)s</ul></div>
<div><h2>%(fc)s</h2><ul>%(company)s</ul></div>
<address id="contact" style="font-style:normal"><h2>%(fct)s</h2><p style="margin:0;line-height:1.8">56 Hartley Ave<br>York, ON M6E 4E8<br><a href="tel:+16474821139" data-cta="call" data-cta-loc="footer">(647) 482-1139</a><br><a href="mailto:cris@ricartidrywall.ca" data-cta="email" data-cta-loc="footer">cris@ricartidrywall.ca</a><br><a href="%(ig)s" rel="noopener">Instagram</a> · <a href="https://www.facebook.com/ricartidrywall" rel="noopener">Facebook</a> · <a href="https://wa.me/16474821139" rel="noopener" data-cta="whatsapp" data-cta-loc="footer">WhatsApp</a><br><span>%(hours)s</span></p></address>
</div>
<div class="rd-fine"><span>%(legal)s</span><span>%(region)s</span></div>
<div class="rd-fine" style="border:0;margin-top:0"><nav class="rd-flangs" aria-label="Language">%(langs)s</nav><p>%(disc)s</p></div>
</div></footer>
<nav class="rd-mbar" aria-label="Contact"><a href="tel:+16474821139" data-cta="call" data-cta-loc="mobile-bar">%(psvg)s%(call)s</a><a href="/estimate" data-cta="estimate" data-cta-loc="mobile-bar">%(est)s</a></nav>
'''

def footer(lang='en', alts=None, note=None):
    t = T[lang]; alts = alts or {'en': '/'}
    li = lambda items: ''.join('<li><a href="%s">%s</a></li>' % (h, x.replace('&', '&amp;')) for h, x in items)
    return FOOTER % dict(blurb=t['f_blurb'], fs=t['f_services'], fc=t['f_company'], fct=t['f_contact'], services=li(t['services']), company=li(t['company']),
           ig=IG, hours=t['hours'], legal=t['legal'], langs=lang_links(lang, alts), disc=note or t['disclaimer'], call=t['call'], est=t['est_short'],
           slogan=t['slogan'], region=t['region'], psvg=PHONE_SVG)
