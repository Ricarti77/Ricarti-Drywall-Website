"""For Homeowners — premium landing page (Task 006). All text is plain markup so the translation memory can localize it (PT now; ES/FR later)."""
SERVICES = [
 ('Home renovations &amp; drywall installation', 'New walls and ceilings for renovations and additions, hung and finished to match the rest of your home.', None),
 ('Basement finishing', 'Framing, insulation for warmth and quiet, moisture-resistant drywall and bulkheads, finished ready for paint.', None),
 ('Attic insulation upgrades', 'Blown-in insulation topped up and air leaks sealed, so upstairs rooms stay warmer in winter and cooler in summer.', '/journal/spray-foam-vs-batt-insulation'),
 ('Spray foam insulation', 'Closed-cell spray foam where it works best: rim joists, sloped ceilings and below-grade walls.', '/journal/spray-foam-vs-batt-insulation'),
 ('Soundproofing', 'Quieter bedrooms, home offices and entertainment rooms with mineral wool, resilient channel and sealed gaps.', '/journal/soundproofing-a-room'),
 ('Popcorn ceiling removal', 'Textured ceilings removed or covered and refinished smooth. Older ceilings are tested for asbestos first.', None),
 ('Drywall repairs &amp; restoration', 'Cracks, water damage, patches after other trades, and lath-and-plaster walls in older homes.', '/journal/lath-and-plaster-repair-toronto'),
 ('Level 4 &amp; Level 5 finishing', 'Smooth, paint-ready walls, with a full skim coat where strong light or dark paint would show the joints.', '/drywall-finishing-toronto'),
 ('Custom architectural features', 'Arches, curved walls, niches, bulkheads and recessed details, built and finished with care.', None),
]
WHY = [
 ('Experience since 2009', 'A family-owned company focused on insulation, drywall and finishing for more than fifteen years.'),
 ('Professional craftsmanship', 'Every wall and ceiling checked under a work light before paint.'),
 ('Clear communication', 'One point of contact from the first visit to the final walkthrough, and straight answers about your options.'),
 ('Detailed written estimates', 'Materials, the finish level for each room, protection and clean-up, itemized so you can compare.'),
 ('Respect for your property', 'Floors, windows and finished surfaces covered before work begins.'),
 ('Clean, organized work', 'Sanding dust controlled, debris bagged and the work area swept at the end of each day.'),
 ('Comfort you can feel', 'Insulation and sound control chosen for how you use each room: warmer, quieter and more efficient.'),
 ('Attention to detail', 'Crisp corners, true curves, and original mouldings protected and preserved.'),
]
STEPS = [
 ('Tell Us About Your Project', 'Send a few photos and a short description through the estimate form, or call or email us.'),
 ('Project Assessment', 'We visit your home, take measurements and talk through what you want each room to look and feel like.'),
 ('Detailed Estimate', 'You receive a written estimate listing the materials, the finish level for each room, protection and clean-up.'),
 ('Professional Installation', 'Rooms are protected, the work is done in clear stages, and the work area is cleaned every day.'),
 ('Final Quality Review', 'We walk every room with you under a work light and fix anything it shows before you paint.'),
]
PRICE = [('Size', 'Square footage of wall and ceiling, not just floor area'), ('Height', 'Ceilings over 9 ft, foyers and stair walls need scaffolding or lifts'),
         ('Finish level', 'Level 5 adds a full skim coat; we use it only where it pays'), ('Insulation', 'Batts, blown-in or spray foam, and how much of each'),
         ('Details', 'Bulkheads, curved walls, arches, recessed details'), ('Access', 'Occupied home, stairs, parking and board delivery')]
FAQ = [
 ('How do I request an estimate?', 'Use the <a href="/estimate">estimate form</a> to send photos or plans, call <a href="tel:+16474821139">(647) 482-1139</a> or email <a href="mailto:cris@ricartidrywall.ca">cris@ricartidrywall.ca</a>. We will arrange a visit and give you a written estimate.'),
 ("Can you help improve my home's insulation?", 'Yes. We install batt, mineral wool, blown-in and spray foam insulation and seal air leaks, and we recommend which material belongs where in your home. <a href="/journal/spray-foam-vs-batt-insulation">Read our insulation guide</a>.'),
 ('Can you remove popcorn ceilings?', "Yes. Textured ceilings can be removed and refinished smooth, or covered with new drywall. Ceilings installed before the 1990s may contain asbestos, so the texture should be tested by a qualified lab before any work. If it tests positive, removal must follow Ontario's asbestos regulations."),
 ('Can you help soundproof existing rooms?', 'Yes. Typical upgrades add mineral wool in the walls or ceiling, resilient channel and an extra layer of drywall, with acoustic sealant at every gap. <a href="/journal/soundproofing-a-room">Read our soundproofing guide</a>.'),
 ('Do you work on occupied homes?', 'Yes. We seal off the rooms we are working in, cover floors and control sanding dust, and we let you know in advance which days will be noisiest.'),
 ('Which areas do you serve?', 'Toronto and the whole Greater Toronto Area, plus Hamilton, Kitchener–Cambridge and the Muskoka region. <a href="/areas">See where we work</a>.'),
]
GUIDES = [('/drywall-finishing-toronto', 'Level 4 or Level 5: what you are paying for'), ('/journal/questions-to-ask-a-drywall-contractor', 'Seven questions to ask a drywall contractor'),
          ('/journal/spray-foam-vs-batt-insulation', 'Spray foam or batts: which goes where')]

def body():
    from builders_page import img
    svc = ''.join('<li><span class="rd-b-n">%02d</span><h3>%s</h3><p>%s</p>%s</li>' % (i + 1, h, d, ('<a class="rd-h-more" href="%s">Learn more<span aria-hidden="true"> →</span></a>' % u) if u else '') for i, (h, d, u) in enumerate(SERVICES))
    why = ''.join('<li><h3>%s</h3><p>%s</p></li>' % (h, d) for h, d in WHY)
    steps = ''.join('<li><span class="rd-b-n">%02d</span><h3>%s</h3><p>%s</p></li>' % (i + 1, h, d) for i, (h, d) in enumerate(STEPS))
    price = ''.join('<div><dt>%s</dt><dd>%s</dd></div>' % (a, b) for a, b in PRICE)
    faq = ''.join('<details%s><summary>%s<span class="rd-plus" aria-hidden="true">+</span></summary><p>%s</p></details>' % (' open' if i == 0 else '', q, a) for i, (q, a) in enumerate(FAQ))
    guides = ''.join('<li><a href="%s">%s<span aria-hidden="true"> →</span></a></li>' % (u, t) for u, t in GUIDES)
    return '''<main id="main">
<div class="rd-wrap">
<nav aria-label="Breadcrumb" class="rd-muted" style="font-size:13px;padding-top:28px"><a href="/">Home</a> / For homeowners</nav>
<section class="rd-cover rd-b-hero rd-h-hero" aria-label="Introduction">
<div class="rd-cover-txt">
<p class="rd-eyebrow">Built Around Your Home</p>
<h1><span class="rd-display">Your Home. <em>Our Commitment.</em></span></h1>
<p class="rd-lede">Your home deserves exceptional craftsmanship. Since 2009, Ricarti Drywall has helped homeowners create more comfortable, beautiful, and energy-efficient living spaces through professional insulation, drywall, and architectural finishing solutions.</p>
<div class="rd-cover-cta"><a class="rd-btn" href="/estimate">Request an Estimate</a><a class="rd-btn-o" href="#services">Explore Our Services</a><a class="rd-link" href="tel:+16474821139">or call (647) 482-1139</a></div>
<div class="rd-short rd-b-short"><b>IN SHORT</b>Ricarti Drywall helps homeowners across Toronto, the GTA, Hamilton, Kitchener-Cambridge and Muskoka with renovations, basements, insulation upgrades, soundproofing, repairs and premium drywall finishing. A visit, a detailed written estimate, a clean and protected home, and a final walkthrough with you. Family-owned, since 2009.</div>
</div>
<figure>%(hero)s<figcaption class="rd-cap">Kent — stair wall with panel mouldings, painted.</figcaption></figure>
</section>
</div>

<section id="services" class="rd-wrap rd-sec" aria-labelledby="svc-h">
<header class="rd-exp-head"><div><p class="rd-kicker">Services for homeowners</p><h2 id="svc-h" class="rd-h2">Everything your walls and ceilings <em>need.</em></h2></div>
<p class="rd-lede">From a single repair to a whole-home renovation, one experienced team for insulation, drywall and finishing.</p></header>
<ol class="rd-b-grid rd-h-svc">%(svc)s</ol>
</section>

<section class="rd-wrap rd-sec" aria-labelledby="why-h">
<header class="rd-exp-head"><div><p class="rd-kicker">Why homeowners choose Ricarti</p><h2 id="why-h" class="rd-h2">Quality You Can See. <em>Comfort You Can Feel.</em></h2></div></header>
<div class="rd-h-why">
<ul class="rd-h-why-list">%(why)s</ul>
<div class="rd-h-why-img">
<div class="rd-h-pair"><figure>%(before)s<figcaption class="rd-cap">Before · Lauther Ave — the old lath-and-plaster ceiling comes down; chandelier wrapped, walls covered.</figcaption></figure>
<figure>%(after)s<figcaption class="rd-cap">After · the same room — new ceiling taped, original medallion and crown kept.</figcaption></figure></div>
<blockquote class="rd-b-quote"><p>“Not only was the dry wall installed perfectly they also repaired a lath and plaster wall. Would highly recommend them.”</p><footer>JENNIFER PETURSSON · GOOGLE REVIEW</footer></blockquote>
</div>
</div>
</section>

<section class="rd-wrap rd-sec" aria-labelledby="process-h">
<header class="rd-exp-head"><div><p class="rd-kicker">Our process</p><h2 id="process-h" class="rd-h2">Simple, clear, <em>step by step.</em></h2></div>
<p class="rd-lede">You always know what happens next, and who to call.</p></header>
<ol class="rd-steps">%(steps)s</ol>
<div class="rd-h-price">
<figure>%(thompson)s<figcaption class="rd-cap">Thompson — ceiling work with floors covered.</figcaption></figure>
<div><h3>What affects your estimate</h3><p class="rd-muted" style="margin:0 0 20px">Every home is different, so we price after we have seen it. These are the things that move the number.</p><dl>%(price)s</dl></div>
</div>
</section>

<section class="rd-wrap rd-sec" aria-labelledby="faq-h">
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:40px 64px;align-items:start">
<div><p class="rd-kicker">Questions</p><h2 id="faq-h" class="rd-h2">Homeowners usually ask.</h2>
<h3 class="rd-h-guides-h">Read before you hire</h3><ul class="rd-h-guides">%(guides)s</ul></div>
<div class="rd-faq" style="border-top:1px solid var(--hair)">%(faq)s</div>
</div>
</section>
</main>

<section class="rd-b-cta" aria-labelledby="cta-h"><div>
<div class="rd-b-cta-l">
<p class="rd-kicker">Start your project</p>
<h2 id="cta-h">Let's Make Your Home <em>Exceptional.</em></h2>
<p class="rd-b-cta-p">Whether you are renovating, improving energy efficiency, or creating a more refined living space, our team is here to help.</p>
<div class="rd-cover-cta"><a class="rd-btn" href="/estimate">Request an Estimate</a><a class="rd-btn-o" href="mailto:cris@ricartidrywall.ca?subject=Home%%20project%%20inquiry">Contact Our Team</a></div>
<p class="rd-b-contact"><a href="tel:+16474821139">(647) 482-1139</a><a href="mailto:cris@ricartidrywall.ca">cris@ricartidrywall.ca</a></p>
</div>
<div class="rd-b-cta-r"><h3>To get started, send us</h3><dl><div><dt>Photos</dt><dd>A few photos of each room or area</dd></div><div><dt>Address</dt><dd>Your street or postal code</dd></div><div><dt>Plans</dt><dd>Drawings, if you have them</dd></div><div><dt>Timing</dt><dd>When you would like to start</dd></div></dl></div>
</div></section>
''' % dict(hero=img('kent-08.jpg', 'Staircase wall with panel mouldings and seamless painted walls, Kent', 900, 1600, eager=True),
           before=img('lauther-01.jpg', 'Crew taking down a failing lath-and-plaster ceiling, chandelier wrapped and walls protected, Lauther Ave', 900, 1600),
           after=img('lauther-02.jpg', 'New drywall ceiling taped around the original plaster medallion and crown moulding, Lauther Ave', 900, 1600),
           thompson=img('thompson-01.jpg', 'Finisher on stilts skimming a ceiling with floors covered, Thompson', 900, 1600),
           svc=svc, why=why, steps=steps, price=price, faq=faq, guides=guides)

CSS = '''
.rd-h-hero .rd-display{font-size:clamp(46px,6.2vw,100px)}
.rd-h-svc{grid-template-columns:repeat(3,minmax(0,1fr))}
.rd-h-svc li{display:flex;flex-direction:column}
.rd-h-more{margin-top:14px;align-self:flex-start;font-size:11px;letter-spacing:.16em;text-transform:uppercase;font-weight:500;color:var(--spruce);text-decoration:none;border-bottom:1px solid transparent;padding-bottom:3px}
.rd-h-more:hover{border-bottom-color:var(--spruce)}
.rd-h-why{display:grid;grid-template-columns:minmax(0,6fr) minmax(0,6fr);gap:48px clamp(40px,6vw,104px);align-items:start}
.rd-h-why-list{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:36px 40px}
.rd-h-why-list li{border-top:1px solid var(--hair);padding-top:16px}
.rd-h-why-list h3{margin:0 0 8px;font:300 clamp(21px,1.7vw,25px)/1.2 var(--serif)}
.rd-h-why-list p{margin:0;font-size:15px;line-height:1.6;color:var(--muted)}
.rd-h-pair{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.rd-h-pair figure,.rd-h-price figure{margin:0}
.rd-h-pair img{width:100%;aspect-ratio:4/5;object-fit:cover;display:block}
.rd-h-why .rd-b-quote{margin-top:40px}
.rd-h-why .rd-b-quote p{font-size:clamp(21px,1.9vw,26px)}
.rd-h-price{display:grid;grid-template-columns:minmax(0,4fr) minmax(0,8fr);gap:40px clamp(40px,6vw,104px);align-items:center;margin-top:clamp(64px,7vw,104px)}
.rd-h-price img{width:100%;aspect-ratio:4/5;object-fit:cover;display:block;max-width:420px}
.rd-h-price h3{margin:0 0 12px;font:300 clamp(28px,2.6vw,38px)/1.1 var(--serif)}
.rd-h-price dl{margin:0;border-top:1px solid var(--ink)}
.rd-h-price dl>div{display:grid;grid-template-columns:140px 1fr;gap:12px;padding:14px 0;border-bottom:1px solid var(--hair);font-size:15px}
.rd-h-price dt{font-weight:500}.rd-h-price dd{margin:0;color:var(--muted)}
.rd-h-guides-h{margin:40px 0 12px;font-size:11px;letter-spacing:.16em;text-transform:uppercase;font-weight:500;color:var(--muted)}
.rd-h-guides{list-style:none;margin:0;padding:0;border-top:1px solid var(--hair)}
.rd-h-guides a{display:block;padding:14px 0;border-bottom:1px solid var(--hair);text-decoration:none;font:300 19px/1.3 var(--serif)}
.rd-h-guides a:hover{color:var(--spruce)}
@media (max-width:1100px){.rd-h-svc{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:900px){.rd-h-why,.rd-h-price{grid-template-columns:1fr}}
@media (max-width:640px){.rd-h-svc,.rd-h-why-list{grid-template-columns:1fr}.rd-h-price dl>div{grid-template-columns:1fr;gap:2px}}
'''
