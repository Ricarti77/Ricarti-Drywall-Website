"""For Builders — premium B2B landing page (Task 005)."""
FAQ = [
 ('Do you supply materials or labour only?', 'Either. We price supply-and-install or labour only, and say which on the quote.'),
 ('Can you run several houses at once?', 'Yes. Tell us your phasing and we will staff to it. [Confirm current capacity: number of houses at once.]'),
 ('Do you work on high-rise towers or commercial projects?', 'We do not work on high-rise towers. Our focus is custom homes and low-rise residential (detached homes, semis and townhouses), and we take on selected commercial projects.'),
 ('What are your payment terms?', "[Your terms: deposit, progress draws, invoicing schedule.] Statutory holdback under Ontario's Construction Act applies as usual."),
 ('How do you handle deficiencies?', 'We walk the house with your site supervisor at handover and close the list. Touch-ups after other trades are priced per visit. [Confirm your usual turnaround.]'),
 ('Which areas do you cover?', 'Toronto and the whole Greater Toronto Area, plus Hamilton, Kitchener–Cambridge and the Muskoka region. <a href="/areas">See where we work</a>.'),
]
STRENGTHS = [
 ('Technical Expertise', 'Specialized knowledge of insulation, drywall systems, architectural details, and premium finishing.'),
 ('Precision &amp; Quality', 'Attention to detail, from the initial installation to the final paint-ready surface.'),
 ('Integrated Services', 'Coordinated insulation, drywall, taping, metal framing, and architectural finishing services.'),
 ('Project Coordination', 'Clear communication and coordination with builders, site supervisors, and other trades.'),
 ('Professional Standards', 'Professional crews, workplace safety, insurance, and documented project scopes.'),
 ('Long-Term Partnerships', 'A commitment to building lasting professional relationships through consistency, accountability, and craftsmanship.'),
]
CAPS = [
 ('Insulation', ['Closed-cell spray foam insulation', 'Batt and mineral wool insulation', 'Blown-in attic insulation']),
 ('Acoustics', ['Acoustic and soundproofing systems']),
 ('Drywall &amp; finishing', ['Custom drywall installation', 'Level 4 and Level 5 finishing', 'Curved walls and ceilings']),
 ('Architectural details', ['Architectural shadow reveals', 'Trimless and integrated ventilation systems', 'Frameless lighting details']),
 ('Framing', ['Metal stud framing']),
]
STEPS = [
 ('Drawing &amp; Scope Review', 'We review your architectural drawings, energy specification and finish requirements, and confirm the scope with you before pricing.'),
 ('Detailed Estimate', 'A written price per unit, per block or per project that names the insulation, board and finish levels, with inclusions and exclusions.'),
 ('Scheduling &amp; Coordination', 'Crews and start dates planned around your insulation-ready and board-ready dates, coordinated with your site supervisor and other trades.'),
 ('Professional Execution', 'Insulation installed ready for inspection, then board, tape and finish by one coordinated crew.'),
 ('Quality Review &amp; Completion', 'A walkthrough with your site supervisor before handover, with any deficiencies listed and closed.'),
]
SEND = [('Drawings', 'Floor plans, sections and reflected ceiling plans (PDF)'), ('Energy spec', 'SB-12 compliance package or insulation schedule'),
        ('Finish spec', 'Finish level by area, corner details, fire and sound ratings'), ('Schedule', 'Insulation-ready and board-ready dates, phasing'),
        ('Supply', 'Labour only, or supply and install')]
AREAS = ['Toronto', 'Greater Toronto Area', 'Hamilton', 'Kitchener-Cambridge', 'Muskoka']

def img(src, alt, w, h, srcset='', sizes='', eager=False, cls=''):
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    ss = ' srcset="%s" sizes="%s"' % (srcset, sizes) if srcset else ''
    return '<img src="/images/%s"%s alt="%s" width="%d" height="%d" %s%s>' % (src, ss, alt, w, h, load, ' class="%s"' % cls if cls else '')

def body():
    strengths = ''.join('<li><span class="rd-b-n">%02d</span><h3>%s</h3><p>%s</p></li>' % (i + 1, h, d) for i, (h, d) in enumerate(STRENGTHS))
    caps = ''.join('<div class="rd-cap-g"><h3>%s</h3><ul>%s</ul></div>' % (g, ''.join('<li>%s</li>' % x for x in items)) for g, items in CAPS)
    steps = ''.join('<li><span class="rd-b-n">%02d</span><h3>%s</h3><p>%s</p></li>' % (i + 1, h, d) for i, (h, d) in enumerate(STEPS))
    send = ''.join('<div><dt>%s</dt><dd>%s</dd></div>' % (a, b) for a, b in SEND)
    areas = ''.join('<li>%s</li>' % a for a in AREAS)
    faq = ''.join('<details%s><summary>%s<span class="rd-plus" aria-hidden="true">+</span></summary><p>%s</p></details>' % (' open' if i == 0 else '', q, a) for i, (q, a) in enumerate(FAQ))
    return '''<main id="main">
<div class="rd-wrap">
<nav aria-label="Breadcrumb" class="rd-muted" style="font-size:13px;padding-top:28px"><a href="/">Home</a> / For builders</nav>
<section class="rd-cover rd-b-hero" aria-label="Introduction">
<div class="rd-cover-txt">
<p class="rd-eyebrow">Built for Builders</p>
<h1><span class="rd-display">Your Vision. <em>Our Precision.</em></span></h1>
<p class="rd-lede">Since 2009, Ricarti Drywall has partnered with builders and construction professionals to deliver precision, reliability, and exceptional craftsmanship across every stage of insulation, drywall, and architectural finishing.</p>
<div class="rd-cover-cta"><a class="rd-btn" href="/estimate?type=builder">Send Your Drawings</a><a class="rd-btn-o" href="tel:+16474821139">Discuss Your Project</a><a class="rd-link" href="mailto:cris@ricartidrywall.ca">cris@ricartidrywall.ca</a></div>
<div class="rd-short rd-b-short"><b>IN SHORT</b>Ricarti Drywall is the insulation, drywall and architectural finishing partner for custom home builders, general contractors, architects, interior designers and residential developers, and for selected commercial contractors, across Toronto, the GTA, Hamilton, Kitchener-Cambridge and Muskoka. Family-owned, since 2009.</div>
</div>
<figure>%(hero)s<figcaption class="rd-cap">Stanton — open floor before insulation and board.</figcaption></figure>
</section>
</div>

<section class="rd-wrap rd-sec" aria-labelledby="why-h">
<header class="rd-exp-head"><div><p class="rd-kicker">Why builders choose Ricarti</p><h2 id="why-h" class="rd-h2">A Partner You Can <em>Build With.</em></h2></div>
<p class="rd-lede">More than a drywall subcontractor: one accountable team for insulation, drywall and architectural finishing, from drawings to paint-ready handover.</p></header>
<ol class="rd-b-grid">%(strengths)s</ol>
<blockquote class="rd-b-quote"><p>“We’ve used Ricarti for a number of projects already, and have been pleased with the work.”</p><footer>ADAM TABAC · GOOGLE REVIEW</footer></blockquote>
</section>

<section class="rd-wrap rd-sec" aria-labelledby="caps-h">
<div class="rd-caps">
<div class="rd-caps-img">
<figure class="rd-caps-main">%(img_arch)s<figcaption class="rd-cap">Brule — arched doorway with corner bead.</figcaption></figure>
<div class="rd-caps-pair"><figure>%(img_ins)s<figcaption class="rd-cap">Stanton — spray foam.</figcaption></figure><figure>%(img_ac)s<figcaption class="rd-cap">Stanton — mineral wool and resilient channel.</figcaption></figure></div>
</div>
<div class="rd-caps-txt">
<p class="rd-kicker">Specialized capabilities</p>
<h2 id="caps-h" class="rd-h2">The systems behind a <em>flawless finish.</em></h2>
<div class="rd-caps-list">%(caps)s</div>
</div>
</div>
</section>

<section class="rd-wrap rd-sec" aria-labelledby="process-h">
<header class="rd-exp-head"><div><p class="rd-kicker">Our process</p><h2 id="process-h" class="rd-h2">From drawings to <em>paint-ready.</em></h2></div>
<p class="rd-lede">Five clear stages, so you always know what happens next and who is responsible.</p></header>
<ol class="rd-steps">%(steps)s</ol>
</section>

<section class="rd-wrap rd-sec" aria-labelledby="area-h">
<div class="rd-b-area">
<div><p class="rd-kicker">Service area</p><h2 id="area-h" class="rd-h2">Where we <em>build.</em></h2><p class="rd-muted" style="margin:20px 0 0;max-width:380px">Based in Toronto, working with builders across the region. <a href="/areas">See all service areas</a>.</p></div>
<ul class="rd-b-areas">%(areas)s</ul>
</div>
</section>

<section class="rd-wrap rd-sec" aria-labelledby="faq-h">
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:40px 64px;align-items:start">
<div><p class="rd-kicker">Questions</p><h2 id="faq-h" class="rd-h2">Builders usually ask.</h2></div>
<div class="rd-faq" style="border-top:1px solid var(--hair)">%(faq)s</div>
</div>
</section>
</main>

<section class="rd-b-cta" aria-labelledby="cta-h"><div>
<div class="rd-b-cta-l">
<p class="rd-kicker">Start a project</p>
<h2 id="cta-h">Let's Build Something <em>Exceptional.</em></h2>
<p class="rd-b-cta-p">Send us your architectural drawings and project details. Our team will review your requirements and discuss the right solutions for your next project.</p>
<div class="rd-cover-cta"><a class="rd-btn" href="/estimate?type=builder">Send Your Drawings</a><a class="rd-btn-o" href="mailto:cris@ricartidrywall.ca?subject=Builder%%20project%%20inquiry">Contact Our Team</a></div>
<p class="rd-b-contact"><a href="tel:+16474821139">(647) 482-1139</a><a href="mailto:cris@ricartidrywall.ca">cris@ricartidrywall.ca</a></p>
</div>
<div class="rd-b-cta-r"><h3>What to send for the sharpest price</h3><dl>%(send)s</dl></div>
</div></section>
''' % dict(hero=img('stanton-01.jpg', 'Open floor with exposed joists and a timber staircase before insulation and board, Stanton', 900, 1600, eager=True),
           img_arch=img('pf-brule.jpg', 'Arched doorway with corner bead opening onto an arched window, Brule', 1000, 1250, '/images/pf-brule-600.jpg 600w, /images/pf-brule.jpg 1000w', '(max-width: 820px) 100vw, 40vw'),
           img_ins=img('svc-insulation-480.jpg', 'Spray foam insulation sealing the walls around a window, Stanton', 480, 600),
           img_ac=img('svc-acoustic-480.jpg', 'A long wall of mineral wool sound insulation behind steel resilient channels, Stanton', 480, 600),
           strengths=strengths, caps=caps, steps=steps, areas=areas, faq=faq, send=send)

CSS = '''
.rd-b-hero{padding-top:clamp(28px,4vw,56px)}
.rd-b-short{margin:40px 0 0;font-size:15px;max-width:620px}
.rd-b-grid{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:56px clamp(28px,4vw,64px)}
.rd-b-grid li{border-top:1px solid var(--hair);padding-top:20px}
.rd-b-n{display:block;font:300 15px/1 var(--serif);color:var(--spruce);margin-bottom:14px}
.rd-b-grid h3,.rd-steps h3{margin:0 0 10px;font:300 clamp(22px,1.9vw,27px)/1.15 var(--serif)}
.rd-b-grid p,.rd-steps p{margin:0;font-size:15px;line-height:1.6;color:var(--muted)}
.rd-b-quote{margin:clamp(56px,6vw,88px) 0 0;padding:28px 0 0;border-top:1px solid var(--ink);max-width:900px}
.rd-b-quote p{margin:0;font:300 clamp(24px,2.4vw,34px)/1.3 var(--serif)}
.rd-b-quote footer{margin-top:14px;font-size:11px;letter-spacing:.16em;font-weight:500;color:var(--muted)}
.rd-caps{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:clamp(40px,6vw,104px);align-items:start}
.rd-caps-img figure{margin:0}
.rd-caps-img img{width:100%;aspect-ratio:4/5;object-fit:cover;display:block}
.rd-caps-pair{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:16px}
.rd-caps-txt{position:sticky;top:120px}
.rd-caps-list{margin-top:clamp(36px,4vw,56px);display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:36px 48px}
.rd-cap-g h3{margin:0 0 12px;padding-top:14px;border-top:1px solid var(--hair);font-size:11px;letter-spacing:.16em;text-transform:uppercase;font-weight:500;color:var(--spruce)}
.rd-cap-g ul{list-style:none;margin:0;padding:0;display:grid;gap:10px}
.rd-cap-g li{font:300 clamp(19px,1.6vw,22px)/1.3 var(--serif)}
.rd-steps{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:40px 28px;counter-reset:s}
.rd-steps li{border-top:1px solid var(--ink);padding-top:20px}
.rd-steps .rd-b-n{font-size:clamp(34px,3vw,46px);margin-bottom:22px}
.rd-b-area{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:40px clamp(40px,6vw,104px);align-items:start}
.rd-b-areas{list-style:none;margin:0;padding:0;border-top:1px solid var(--ink)}
.rd-b-areas li{font:300 clamp(28px,3.2vw,46px)/1.1 var(--serif);padding:18px 0;border-bottom:1px solid var(--hair)}
.rd-b-cta{background:var(--deep);color:#fff;margin-top:clamp(80px,9vw,128px)}
.rd-b-cta>div{max-width:1440px;margin:0 auto;padding:clamp(64px,8vw,112px) var(--pad);display:grid;grid-template-columns:minmax(0,7fr) minmax(0,5fr);gap:56px clamp(40px,6vw,104px);align-items:start}
.rd-b-cta .rd-kicker{color:var(--soft)}
.rd-b-cta h2{margin:0;font:300 clamp(40px,5vw,72px)/1.02 var(--serif);letter-spacing:-.02em}
.rd-b-cta h2 em{display:block;color:var(--soft)}
.rd-b-cta-p{margin:28px 0 36px;max-width:560px;font-size:18px;line-height:1.6;color:var(--dim)}
.rd-b-cta .rd-btn{background:#fff;color:var(--deep)}.rd-b-cta .rd-btn:hover{background:var(--soft)}
.rd-b-cta .rd-btn-o{border-color:var(--bronze);color:#fff}.rd-b-cta .rd-btn-o:hover{border-color:#fff;color:#fff}
.rd-b-contact{display:flex;flex-wrap:wrap;gap:8px 28px;margin:28px 0 0;font-size:15px}
.rd-b-contact a{color:#fff;text-decoration:none;border-bottom:1px solid var(--bronze);padding-bottom:2px}
.rd-b-cta-r h3{margin:0 0 18px;font-size:11px;letter-spacing:.16em;text-transform:uppercase;font-weight:500;color:var(--soft)}
.rd-b-cta-r dl{margin:0;border-top:1px solid var(--line-d)}
.rd-b-cta-r dl>div{display:grid;grid-template-columns:120px 1fr;gap:12px;padding:14px 0;border-bottom:1px solid var(--line-d);font-size:15px}
.rd-b-cta-r dt{color:#fff;font-weight:500}.rd-b-cta-r dd{margin:0;color:var(--dim)}
@media (max-width:1100px){.rd-steps{grid-template-columns:repeat(3,minmax(0,1fr))}.rd-b-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:900px){.rd-caps,.rd-b-area,.rd-b-cta>div{grid-template-columns:1fr}.rd-caps-txt{position:static}.rd-caps-txt{order:-1}}
@media (max-width:640px){.rd-b-grid,.rd-steps,.rd-caps-list{grid-template-columns:1fr}.rd-b-cta-r dl>div{grid-template-columns:1fr;gap:2px}}
'''
