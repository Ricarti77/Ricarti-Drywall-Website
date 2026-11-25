"""Selected Projects section, generated from content/projects.json (the single source for projects and photos)."""
import json, os, html
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, 'content', 'projects.json')

def load():
    return json.load(open(DATA))

def esc(s):
    return html.escape(s, quote=True)

def section():
    d = load()
    projects = [p for p in d['projects'] if p.get('published')]
    cats = {c['key']: c for c in d['categories']}
    count = {k: sum(1 for p in projects if k in p['documented_work']) for k in cats}
    count['all'] = len(projects)
    # only categories supported by at least one project
    shown = [c for c in d['categories'] if count[c['key']]]
    filters = ''.join('<button type="button" data-filter="%s" aria-pressed="%s">%s<span class="rd-pf-c">%d</span></button>'
                      % (c['key'], 'true' if c['key'] == 'all' else 'false', esc(c['en']), count[c['key']]) for c in shown)
    items = []
    for i, p in enumerate(projects):
        n = len(p['photos'])
        work = ' · '.join(esc(cats[k]['en']) for k in p['documented_work'])
        loc = p['location']
        place = ', '.join(x for x in [loc.get('neighbourhood'), loc.get('city')] if x)
        meta = ''
        if p.get('project_type'):
            meta += '<div><dt>Project type</dt><dd>%s</dd></div>' % esc(p['project_type'])
        if p.get('services_performed'):
            meta += '<div><dt>Services</dt><dd>%s</dd></div>' % esc(', '.join(p['services_performed']))
        meta += '<div><dt>Work documented</dt><dd>%s</dd></div>' % work
        photos_label = '%d photos' % n if n != 1 else '1 photo'
        gl = ''.join('<li data-src="/images/%s">%s</li>' % (ph['file'], esc(ph['caption']['en'])) for ph in p['photos'])
        items.append('''<li class="rd-pf-item" data-cats="%(cats)s">
<button type="button" class="rd-pf-cover" data-gallery="%(id)s" data-gallery-title="%(name)s" aria-label="Open the %(name)s gallery, %(photos)s"><img src="/images/%(cover)s" srcset="/images/%(small)s 600w, /images/%(cover)s 1000w" sizes="(max-width: 700px) 100vw, 46vw" alt="%(alt)s" width="1000" height="1250" loading="lazy" decoding="async"><span class="rd-pf-view" aria-hidden="true">View gallery</span></button>
<div class="rd-pf-meta"><span class="rd-pf-n">%(num)02d</span><h3 class="rd-pf-h">%(name)s</h3>%(place)s<dl>%(meta)s</dl>
<button type="button" class="rd-pf-link" data-gallery="%(id)s" data-gallery-title="%(name)s">View gallery · %(photos)s</button></div>
<ul data-gallery-list="%(id)s" hidden>%(gl)s</ul>
</li>''' % dict(cats=' '.join(p['documented_work']), id=p['id'], name=esc(p['name']), photos=photos_label,
                cover=p['cover']['file'], small=p['cover']['file_small'], alt=esc(p['cover']['alt']['en']), num=i + 1,
                place=('<p class="rd-pf-place">%s</p>' % esc(place)) if place else '', meta=meta, gl=gl))
    return '''<section id="projects" class="rd-wrap rd-sec rd-pf" aria-labelledby="projects-h">
<header class="rd-exp-head">
<div><p class="rd-kicker">Selected Projects</p><h2 id="projects-h" class="rd-h2">Craftsmanship in Every Detail.</h2></div>
<p class="rd-lede">From exceptional custom homes to complex architectural spaces, our work reflects a commitment to precision, craftsmanship, and excellence.</p>
</header>
<div class="rd-pf-filters" role="group" aria-label="Filter projects" hidden>%s</div>
<p class="rd-pf-status" aria-live="polite" data-one="Showing %%d project" data-many="Showing %%d projects"></p>
<ol class="rd-pf-grid">%s</ol>
</section>''' % (filters, '\n'.join(items))

CSS = '''
.rd-pf-filters{display:flex;flex-wrap:wrap;gap:4px 30px;margin:0 0 clamp(40px,5vw,64px);padding-bottom:14px;border-bottom:1px solid var(--hair)}
.rd-pf-filters[hidden]{display:none}
.rd-pf-filters button{background:none;border:0;padding:8px 0;font:inherit;font-size:14px;letter-spacing:.02em;color:var(--muted);cursor:pointer;border-bottom:1px solid transparent;transition:color .25s,border-color .25s}
.rd-pf-filters button:hover{color:var(--ink)}
.rd-pf-filters button[aria-pressed="true"]{color:var(--ink);border-bottom-color:var(--spruce)}
.rd-pf-c{font-size:11px;color:var(--spruce);margin-left:6px;vertical-align:2px}
.rd-pf-status{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
.rd-pf-grid{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:clamp(64px,8vw,120px) clamp(32px,6vw,112px);align-items:start}
.rd-pf-grid:not(.is-filtered) .rd-pf-item:nth-child(even){margin-top:clamp(80px,11vw,176px)}
.rd-pf-item[hidden]{display:none}
.rd-pf-cover{display:block;position:relative;width:100%;padding:0;border:0;background:var(--gypsum);cursor:zoom-in;overflow:hidden}
.rd-pf-cover img{display:block;width:100%;aspect-ratio:4/5;object-fit:cover;transition:transform 1.1s cubic-bezier(.2,.6,.2,1),filter .6s ease;filter:saturate(.9)}
.rd-pf-cover:hover img,.rd-pf-cover:focus-visible img{transform:scale(1.03);filter:saturate(1)}
.rd-pf-view{position:absolute;left:20px;bottom:18px;color:#fff;font-size:13px;font-weight:500;opacity:0;transform:translateY(6px);transition:opacity .4s,transform .4s;text-shadow:0 1px 8px rgba(0,0,0,.45)}
.rd-pf-cover:hover .rd-pf-view,.rd-pf-cover:focus-visible .rd-pf-view{opacity:1;transform:none}
.rd-pf-meta{display:grid;grid-template-columns:auto 1fr;gap:0 22px;padding-top:24px}
.rd-pf-n{grid-row:span 4;font-size:13px;font-weight:500;color:var(--spruce);padding-top:16px;font-variant-numeric:tabular-nums}
.rd-pf-h{margin:0;font:300 clamp(34px,3.3vw,52px)/1.02 var(--serif);letter-spacing:-.01em}
.rd-pf-place{margin:6px 0 0;font-size:14px;color:var(--muted)}
.rd-pf-meta dl{margin:16px 0 0;display:grid;gap:10px}
.rd-pf-meta dt{font-size:12.5px;font-weight:500;color:var(--muted)}
.rd-pf-meta dd{margin:3px 0 0;font-size:15px}
.rd-pf-link{justify-self:start;margin-top:18px;background:none;border:0;padding:0 0 4px;font:inherit;font-size:14px;font-weight:600;color:var(--ink);border-bottom:1px solid var(--bronze);cursor:pointer;min-height:32px}
.rd-pf-link:hover,.rd-pf-link:focus-visible{color:var(--spruce)}
@media (max-width:700px){.rd-pf-grid{display:flex;overflow-x:auto;scroll-snap-type:x mandatory;gap:14px;margin:0 calc(-1 * var(--pad));padding:0 var(--pad) 8px;scrollbar-width:none}.rd-pf-item{flex:0 0 80%;scroll-snap-align:start}.rd-pf-grid .rd-pf-item:nth-child(even){margin-top:0}.rd-pf-filters{gap:2px 20px;flex-wrap:nowrap;overflow-x:auto;scrollbar-width:none}.rd-pf-filters button{white-space:nowrap;min-height:44px}.rd-pf-meta dl{display:none}.rd-pf-meta{padding-top:14px}.rd-pf-h{font-size:30px}}
@media (prefers-reduced-motion:reduce){.rd-pf-cover img,.rd-pf-view{transition:none}.rd-pf-cover:hover img{transform:none}}
'''

def pt_strings():
    """Portuguese for everything generated from the data file (fed into the translation memory)."""
    d = load(); seg, att = {}, {}
    cats = {c['key']: c for c in d['categories']}
    for p in d['projects']:
        for ph in p['photos']:
            seg[esc(ph['caption']['en'])] = esc(ph['caption']['pt'])
        att[p['cover']['alt']['en']] = p['cover']['alt']['pt']
        n = len(p['photos'])
        en_ph, pt_ph = ('%d photos' % n, '%d fotos' % n) if n != 1 else ('1 photo', '1 foto')
        att['Open the %s gallery, %s' % (p['name'], en_ph)] = 'Abrir a galeria %s, %s' % (p['name'], pt_ph)
        seg['View gallery · %s' % en_ph] = 'Ver galeria · %s' % pt_ph
        seg[' · '.join(esc(cats[k]['en']) for k in p['documented_work'])] = ' · '.join(esc(cats[k]['pt']) for k in p['documented_work'])
    return {k: v for k, v in seg.items() if v}, att
