"""Shared header, search dialog, Instagram strip and footer for every page."""

IG = 'https://www.instagram.com/ricarti_drywall/'
SEARCH_SVG = '<svg class="rd-ico" viewBox="0 0 24 24" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5 21 21"/></svg>'
IG_SVG = '<svg class="rd-ico" viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.3" cy="6.7" r=".6" fill="currentColor"/></svg>'

LANGS = [('en', 'EN', 'English'), ('fr', 'FR', 'Français'), ('it', 'IT', 'Italiano'), ('pt', 'PT', 'Português'), ('he', 'עב', 'עברית')]

T = {
 'en': dict(
   nav=[('/', 'Home'), ('/homeowners', 'For homeowners'), ('/builders', 'For builders'), ('/drywall-finishing-toronto', 'Services'), ('/journal', 'Journal'), ('/reviews', 'Reviews')],
   extra=[('/areas', 'Service areas'), ('/estimate', 'Get an estimate')],
   tag='Family-owned since 2009 · GTA · Hamilton · Kitchener–Cambridge · Muskoka', areas='Service areas',
   search='Search the site', search_ph='Search: spray foam, Level 5, soundproofing…', close='CLOSE', menu='Menu',
   sugg='Popular:', sugg_list=['Level 5 finish', 'Spray foam', 'Soundproofing', 'Plaster repair', 'Builders', 'WSIB'],
   est='Get an estimate', call='Call', skip='Skip to content', home='Ricarti Drywall, home',
   ig_k='On Instagram', ig_h='Fresh off the trowel.', ig_follow='Follow @ricarti_drywall',
   f_blurb='Insulation, steel framing, drywall and finishing for homes across the GTA, Hamilton, Kitchener–Cambridge and Muskoka.',
   f_services='Services', f_company='Company', f_contact='Contact',
   services=[('/drywall-finishing-toronto', 'Taping & finishing'), ('/#services', 'Insulation & spray foam'), ('/#services', 'Steel stud framing'), ('/#services', 'Drywall installation'), ('/#services', 'Small renovations')],
   company=[('/homeowners', 'For homeowners'), ('/builders', 'For builders'), ('/areas', 'Service areas'), ('/journal', 'Journal'), ('/reviews', 'Reviews'), ('/estimate', 'Estimate & site visit')],
   hours='[Mon–Fri hours]', legal='© 2026 [Legal company name] · WSIB [account no.] · [$X M] liability',
   disclaimer='Translations of this site are provided for convenience and have not been professionally reviewed. If a translated page differs from the English, the English version applies. All content is general information, not a quote or contract.'),
}

def _a(href, text, active, attrs=''):
    cur = ' aria-current="page"' if active == href else ''
    return '<a href="%s"%s%s>%s</a>' % (href, cur, attrs, text)

def lang_links(lang, alts, cls_current=True):
    """alts: dict lang -> url for pages that exist in that language."""
    out = []
    for code, short, _ in LANGS:
        href = alts.get(code)
        if not href:
            continue
        cur = ' aria-current="true"' if code == lang else ''
        out.append('<a href="%s" lang="%s" hreflang="%s"%s>%s</a>' % (href, code, code, cur, short))
    return ''.join(out)

def header(active='', lang='en', alts=None):
    t = T[lang]; alts = alts or {'en': active or '/'}
    nav = ''.join(_a(h, x, active) for h, x in t['nav'])
    mnav = ''.join('<li>%s</li>' % _a(h, x, active) for h, x in t['nav'] + t['extra'])
    home = '/' if lang == 'en' else '/%s/' % lang
    return '''<a class="rd-skip" href="#main">%(skip)s</a>
<div class="rd-top"><div>
<span class="rd-hide">%(tag)s</span>
<nav aria-label="Utility"><a class="rd-hide" href="%(areas_u)s">%(areas)s</a><a class="rd-hide rd-speak" href="/pt/" lang="pt" hreflang="pt-BR">Falamos português</a><span class="rd-langs" aria-label="Language">%(langs)s</span><a href="%(ig)s" aria-label="Instagram @ricarti_drywall" rel="noopener">%(igsvg)s</a><a href="mailto:cris@ricartidrywall.ca" class="rd-hide">cris@ricartidrywall.ca</a><a href="tel:+16474821139">(647) 482-1139</a></nav>
</div></div>
<header class="rd-head"><div>
<nav aria-label="Main" class="rd-nav">%(nav)s</nav>
<details class="rd-mnav"><summary>%(menu)s</summary><ul>%(mnav)s<li><a href="tel:+16474821139">(647) 482-1139</a></li><li><a href="%(ig)s" rel="noopener">Instagram · @ricarti_drywall</a></li><li class="rd-mlangs">%(langs)s</li></ul></details>
<a href="%(home)s" class="rd-logo" aria-label="%(home_l)s"><img src="/images/lockup-graphite.png" alt="Ricarti Drywall" width="264" height="52"></a>
<div class="rd-right">
<button type="button" class="rd-sbtn" data-open-search aria-label="%(search)s">%(ssvg)s<span>%(search)s</span><kbd>/</kbd></button>
<a href="/estimate" class="rd-cta">%(est)s</a>
</div>
</div></header>
<dialog id="rd-search" class="rd-dlg" aria-label="%(search)s"><div class="rd-panel">
<form class="rd-sform" action="/search" role="search">%(ssvg)s<input id="rd-q" name="q" type="search" autocomplete="off" placeholder="%(sph)s" aria-label="%(search)s"><button type="button" id="rd-sclose">%(close)s</button></form>
<div id="rd-sugg" class="rd-sugg">%(sugg)s %(sugglinks)s</div>
<ul id="rd-res" class="rd-res" aria-live="polite"></ul>
</div></dialog>
''' % dict(skip=t['skip'], tag=t['tag'], areas=t['areas'], areas_u='/areas', langs=lang_links(lang, alts), ig=IG, igsvg=IG_SVG,
           nav=nav, menu=t['menu'], mnav=mnav, home=home, home_l=t['home'], search=t['search'], ssvg=SEARCH_SVG, est=t['est'],
           sph=t['search_ph'], close=t['close'], sugg=t['sugg'],
           sugglinks=''.join('<a href="/search?q=%s">%s</a>' % (s.replace(' ', '+'), s) for s in t['sugg_list']))

# Project album: every photo, grouped by project (street and city only, never house numbers).
ALBUM = [
 ('brule-01.jpg', 'Brule, Toronto — arched dormer nook boarded in moisture-resistant drywall'),
 ('brule-02.jpg', 'Brule, Toronto — the same nook in daylight, ready for tape'),
 ('brule-04.jpg', 'Brule, Toronto — arched doorway boarded, with corner bead'),
 ('brule-05.jpg', 'Brule, Toronto — bedroom boarded around a row of three windows'),
 ('brule-07.jpg', 'Brule, Toronto — room boarded around French doors'),
 ('brule-08.jpg', 'Brule, Toronto — arched niche and framing before board'),
 ('brule-03.jpg', 'Brule, Toronto — insulated ceiling on resilient channel, board stocked by type'),
 ('brule-06.jpg', 'Brule, Toronto — closed-cell spray foam between roof rafters'),
 ('hero-kent.jpg', 'Kent, Toronto — finished bedroom after paint'),
 ('kent-01.jpg', 'Kent, Toronto — smooth walls and ceiling, painted'),
 ('kent-02.jpg', 'Kent, Toronto — the long stair hall, finished before paint'),
 ('kent-03.jpg', 'Kent, Toronto — painted bedroom under window light'),
 ('kent-04.jpg', 'Kent, Toronto — kitchen and living area, finished drywall'),
 ('kent-05.jpg', 'Kent, Toronto — finish coats done, floors protected'),
 ('kent-06.jpg', 'Kent, Toronto — bedroom ready for paint'),
 ('kent-07.jpg', 'Kent, Toronto — open main floor during finishing'),
 ('lauther-01.jpg', 'Lauther Ave, Toronto — old lath-and-plaster ceiling coming down'),
 ('lauther-02.jpg', 'Lauther Ave, Toronto — new ceiling taped around the original medallion'),
 ('stanton-01.jpg', 'Stanton, Toronto — open joists before insulation and board'),
 ('stanton-02.jpg', 'Stanton, Toronto — mineral wool and steel channel on an exterior wall'),
 ('stanton-03.jpg', 'Stanton, Toronto — mineral wool behind resilient channel, close up'),
 ('stanton-04.jpg', 'Stanton, Toronto — spray foam around a window opening'),
 ('stanton-05.jpg', 'Stanton, Toronto — sound insulation under a sloped ceiling'),
 ('thompson-01.jpg', 'Thompson, Toronto — finisher on stilts, floors covered'),
]
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

def footer(lang='en', alts=None, note=None):
    t = T[lang]; alts = alts or {'en': '/'}
    langs = ''.join('<a href="%s" lang="%s" hreflang="%s">%s</a>' % (alts[c], c, c, name) for c, _, name in LANGS if c in alts)
    li = lambda items: ''.join('<li><a href="%s">%s</a></li>' % (h, x.replace('&', '&amp;')) for h, x in items)
    return '''<footer class="rd-foot"><div class="rd-cols">
<div><img src="/images/lockup-boxed-graphite.png" alt="Ricarti Drywall" width="200" height="80" loading="lazy" style="width:200px;height:auto;display:block"><p class="rd-muted" style="margin:16px 0 0;max-width:260px">%(blurb)s</p></div>
<div><h2>%(fs)s</h2><ul>%(services)s</ul></div>
<div><h2>%(fc)s</h2><ul>%(company)s</ul></div>
<address style="font-style:normal"><h2>%(fct)s</h2><p style="margin:0;line-height:1.7">56 Hartley Ave<br>York, ON M6E 4E8<br><a href="tel:+16474821139">(647) 482-1139</a><br><a href="mailto:cris@ricartidrywall.ca">cris@ricartidrywall.ca</a><br><a href="%(ig)s" rel="noopener">Instagram</a> · <a href="https://www.facebook.com/ricartidrywall" rel="noopener">Facebook</a> · <a href="https://wa.me/16474821139" rel="noopener">WhatsApp</a><br><span class="rd-muted">%(hours)s</span></p></address>
</div>
<div class="rd-fine"><span>%(legal)s</span><span>Toronto · North York · Etobicoke · Vaughan · Richmond Hill · Markham · Mississauga · Oakville · Hamilton · Kitchener–Cambridge · Muskoka</span></div>
<div class="rd-fine" style="border:0;margin-top:0"><nav aria-label="Language">%(langs)s</nav><p>%(disc)s</p></div>
</footer>
<div class="rd-mbar"><a href="tel:+16474821139">%(call)s</a><a class="rd-dark" href="/estimate">%(est)s</a></div>
''' % dict(blurb=t['f_blurb'], fs=t['f_services'], fc=t['f_company'], fct=t['f_contact'], services=li(t['services']), company=li(t['company']),
           ig=IG, hours=t['hours'], legal=t['legal'], langs=langs, disc=note or t['disclaimer'], call=t['call'], est=t['est'])
