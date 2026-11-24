"""New pages: editorial home, reviews, journal, articles, search. Plus the search index. Run after build.py."""
import json, re, html, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build, chrome
from articles import ARTICLES

OUT = build.OUT
GMAPS = 'https://www.google.com/maps/search/?api=1&query=Ricarti+Drywall+Toronto'

REVIEWS = [
 ('Ioana Popa', 'He completed everything on time and on budget, and the end result was flawless.'),
 ('Jennifer Petursson', 'Not only was the dry wall installed perfectly they also repaired a lath and plaster wall. Would highly recommend them.'),
 ('Mike B.', 'Cris and his crew drywalled and taped my entire house project.'),
 ('Milad Foroughi Masouleh', 'I have used Ricarti drywall service a few times, and every time we have a great experience. Highly recommended.'),
 ('Adam Tabac', 'We’ve used Ricarti for a number of projects already, and have been pleased with the work.'),
]

def shell(active, body, ig=True):
    return '<div>' + chrome.header(active) + body + (chrome.ig_strip() if ig else '') + chrome.footer() + '</div>'

def img(f, alt, cls='', style='', eager=False, w=900, h=1600):
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return '<img src="/images/%s" alt="%s" width="%d" height="%d" %s%s%s>' % (f, html.escape(alt), w, h, load, ' class="%s"' % cls if cls else '', ' style="%s"' % style if style else '')

def band(h, a=('Book a site visit', '/estimate'), b=('Get an estimate', '/estimate')):
    return '<section class="rd-band" aria-label="Get started"><div><h2>%s</h2><div style="display:flex;flex-wrap:wrap;gap:14px"><a class="rd-btn" href="%s">%s</a><a class="rd-btn-o" href="%s">%s</a></div></div></section>' % (h, a[1], a[0], b[1], b[0])

def card(a, size='m'):
    return '''<a class="rd-card" href="/journal/%(slug)s">%(img)s<span class="rd-label">%(cat)s · %(read)s read</span><span class="rd-ct">%(title)s</span></a>''' % dict(a, img=img(a['image'], a['alt']))

# ---------------------------------------------------------------- HOME
HOME_CSS = '''
.rd-cover{display:grid;grid-template-columns:minmax(0,7fr) minmax(0,5fr);gap:clamp(32px,5vw,80px);align-items:end;padding-top:clamp(40px,6vw,88px)}
.rd-cover h1{margin:0 0 28px;font-size:12px;letter-spacing:.16em;font-weight:500;color:var(--spruce);text-transform:uppercase}
.rd-display{margin:0;font:300 clamp(52px,8.4vw,132px)/.94 var(--serif);letter-spacing:-.025em}
.rd-cover .rd-lede{max-width:560px;margin:36px 0 32px}
.rd-cover figure{margin:0}
.rd-cover figure img{width:100%;aspect-ratio:4/5;object-fit:cover;display:block}
.rd-byline{display:flex;flex-wrap:wrap;gap:8px 28px;margin-top:44px;padding-top:18px;border-top:1px solid var(--hair);font-size:13px;color:var(--muted)}
.rd-byline b{font-weight:500;color:var(--ink)}
.rd-toc{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));border-top:1px solid var(--ink);border-bottom:1px solid var(--hair);margin-top:clamp(56px,7vw,96px)}
.rd-toc a{display:block;padding:18px 18px 20px 0;text-decoration:none;border-right:1px solid var(--hair);margin-right:18px}
.rd-toc a:last-child{border-right:0}
.rd-toc span{display:block;font:300 28px/1 var(--serif);color:var(--spruce);margin-bottom:10px}
.rd-toc b{font-weight:500;font-size:15px}
.rd-toc i{display:block;font-style:normal;font-size:13px;color:var(--muted);margin-top:4px}
.rd-feature{margin-top:clamp(80px,9vw,128px)}
.rd-feature>figure{margin:0;position:relative}
.rd-feature>figure img{width:100%;height:clamp(380px,56vw,780px);object-fit:cover;display:block}
.rd-feature>figure figcaption{position:absolute;left:var(--pad);bottom:clamp(24px,4vw,56px);right:var(--pad);color:#fff;max-width:900px}
.rd-feature>figure figcaption p{margin:0 0 12px;font-size:11px;letter-spacing:.16em;font-weight:500}
.rd-feature>figure figcaption h2{margin:0;font:300 clamp(36px,5.4vw,80px)/1 var(--serif);letter-spacing:-.02em;text-shadow:0 2px 30px rgba(0,0,0,.35)}
.rd-feature>figure::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,0) 45%,rgba(0,0,0,.55));pointer-events:none}
.rd-feature>figure figcaption{z-index:1}
.rd-story{display:grid;grid-template-columns:minmax(0,3fr) minmax(0,6fr) minmax(0,3fr);gap:clamp(28px,4vw,64px);padding-top:clamp(48px,6vw,80px);align-items:start}
.rd-story aside{font-size:13px;color:var(--muted);border-top:1px solid var(--hair);padding-top:14px}
.rd-story aside dl{margin:0;display:grid;gap:12px}
.rd-story aside dt{font-size:11px;letter-spacing:.14em;font-weight:500}
.rd-story aside dd{margin:2px 0 0;color:var(--ink);font-size:14px}
.rd-story .rd-prose{max-width:none}
.rd-story .rd-side img{width:100%;aspect-ratio:3/4;object-fit:cover;display:block}
.rd-pull{margin:0;padding:clamp(56px,7vw,96px) 0;text-align:center;border-bottom:1px solid var(--hair)}
.rd-pull p{margin:0 auto;max-width:1100px;font:300 clamp(30px,4vw,58px)/1.1 var(--serif);letter-spacing:-.015em}
.rd-pull footer{margin-top:22px;font-size:11px;letter-spacing:.16em;font-weight:500;color:var(--muted)}
.rd-two{display:grid;grid-template-columns:1fr 1fr;margin-top:clamp(80px,9vw,128px)}
.rd-two article{padding:clamp(36px,5vw,80px);display:flex;flex-direction:column;gap:20px}
.rd-two h3{margin:0;font:300 clamp(30px,3vw,44px)/1.06 var(--serif)}
.rd-two ul{margin:0;padding:0;list-style:none;border-top:1px solid var(--hair);font-size:15px}
.rd-two li{padding:12px 0;border-bottom:1px solid var(--hair)}
.rd-two .rd-dark{background:var(--deep);color:#fff}
.rd-two .rd-dark .rd-kicker{color:var(--soft)}
.rd-two .rd-dark p{color:#C9D3CD}
.rd-two .rd-dark li{border-color:#3A5247}
.rd-two .rd-dark ul{border-color:#3A5247}
.rd-two .rd-dark .rd-btn{background:#fff;color:var(--deep)}.rd-two .rd-dark .rd-btn:hover{background:var(--soft)}
.rd-two .rd-dark .rd-link{color:#fff;border-color:#fff}
.rd-row{display:grid;grid-template-columns:64px minmax(0,1fr) minmax(0,1.4fr) 24px;gap:8px 32px;padding:28px 0;border-bottom:1px solid var(--hair);text-decoration:none;align-items:baseline}
.rd-row:hover{color:var(--spruce)}
.rd-row .n{font:300 30px var(--serif);color:var(--spruce)}
.rd-row .h{font:300 clamp(22px,2.2vw,30px)/1.1 var(--serif)}
.rd-row .d{font-size:15px;color:var(--muted)}
.rd-notes{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:clamp(32px,5vw,80px);align-items:center}
.rd-notes img{width:100%;aspect-ratio:4/5;object-fit:cover;display:block}
.rd-notes dl{margin:28px 0 0;display:grid;grid-template-columns:auto minmax(0,1fr);gap:0 24px;border-top:1px solid var(--hair);font-size:15px}
.rd-notes dt,.rd-notes dd{padding:14px 0;border-bottom:1px solid var(--hair);margin:0}
.rd-notes dt{color:var(--spruce);font-weight:500}
.rd-cards{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:40px 28px}
.rd-card{display:block;text-decoration:none}
.rd-card img{width:100%;aspect-ratio:4/3;object-fit:cover;display:block;margin-bottom:16px;transition:opacity .3s}
.rd-card:hover img{opacity:.85}
.rd-ct{display:block;font:300 24px/1.2 var(--serif);margin-top:8px}
.rd-quotes{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:32px 48px;margin-top:48px}
.rd-quotes blockquote{margin:0;border-top:1px solid var(--hair);padding-top:20px}
.rd-quotes p{margin:0;font:300 21px/1.4 var(--serif)}
.rd-quotes footer{margin-top:14px;font-size:11px;letter-spacing:.14em;font-weight:500;color:var(--muted)}
.rd-letter{display:grid;grid-template-columns:minmax(0,4fr) minmax(0,7fr);gap:clamp(32px,5vw,80px);border-top:1px solid var(--hair);padding-top:64px;align-items:start}
.rd-letter img{width:100%;aspect-ratio:3/4;object-fit:cover;display:block;max-width:440px}
.rd-letter blockquote{margin:0;font:300 clamp(23px,2.1vw,29px)/1.42 var(--serif)}
.rd-sig{margin-top:28px;font:italic 300 30px var(--serif);color:var(--spruce)}
@media (max-width:1000px){.rd-toc{grid-template-columns:repeat(2,minmax(0,1fr))}.rd-toc a{border-right:0;border-bottom:1px solid var(--hair)}.rd-quotes,.rd-cards{grid-template-columns:1fr 1fr}}
@media (max-width:820px){.rd-cover,.rd-story,.rd-two,.rd-notes,.rd-letter{grid-template-columns:1fr}.rd-cover figure img{aspect-ratio:4/3}.rd-story aside{order:3}.rd-quotes,.rd-cards{grid-template-columns:1fr}}
@media (max-width:700px){.rd-row{grid-template-columns:48px minmax(0,1fr)}.rd-row .d{grid-column:2}.rd-row>span:last-child{display:none}}
'''

SERVICES = [
 ('Insulation & air sealing', 'Batt, blown-in and spray foam, open and closed cell, with the air barrier and vapour control your inspector checks for.', '/journal/spray-foam-vs-batt-insulation'),
 ('Steel stud framing', 'Bulkheads, ceilings, partitions and basement walls, framed straight and plumb so the board goes on flat.', '/#services'),
 ('Drywall installation', 'Standard, moisture-resistant, fire-rated and sound board, hung to keep joints out of the light.', '/#services'),
 ('Taping & finishing', 'Level 4 as standard for painted walls. A Level 5 skim coat for raking light, tall walls, and dark or glossy paint.', '/drywall-finishing-toronto'),
 ('Small renovations', 'Basements, ceiling repairs, soundproofing a room, plaster repair, patching after other trades.', '/journal/lath-and-plaster-repair-toronto'),
]

FAQ = [
 ('Do you work for homeowners or only for builders?', 'Both. We take projects directly from homeowners who are building or renovating, and we work as the insulation and drywall trade for builders and general contractors on detached homes, semis and townhouses.'),
 ('Which areas do you serve?', 'The whole Greater Toronto Area, plus Hamilton, Kitchener–Cambridge and the Muskoka region.'),
 ('Are you insured and registered with the WSIB?', 'Yes. We carry [$X million] in liability insurance and are registered with the WSIB. Builders receive our clearance certificate and certificate of insurance before work starts.'),
 ('What is the difference between a Level 4 and a Level 5 finish?', 'Level 4 is three coats over the joints and screws, and suits most painted rooms. Level 5 adds a skim coat over the entire wall or ceiling, so joints do not show under raking light, gloss paint or dark colours.'),
 ('How long does drywall take on a new house?', 'It depends on size, ceiling height and finish level. For a typical [size] home, plan on [X] weeks from board delivery to paint-ready. You get a schedule with your quote.'),
 ('How do I get an estimate?', 'Send photos or drawings through the estimate form, or book a site visit. Requests go straight to cris@ricartidrywall.ca and we reply within [one business day].'),
]

def faq_html():
    return ''.join('<details%s><summary>%s<span class="rd-plus" aria-hidden="true">+</span></summary><p>%s</p></details>' % (' open' if i == 0 else '', q, a) for i, (q, a) in enumerate(FAQ))

def home():
    rows = ''.join('<a class="rd-row" href="%s"><span class="n">%02d</span><span class="h">%s</span><span class="d">%s</span><span aria-hidden="true">→</span></a>' % (u, i + 1, h.replace('&', '&amp;'), d) for i, (h, d, u) in enumerate(SERVICES))
    quotes = ''.join('<blockquote><p>“%s”</p><footer>%s · GOOGLE REVIEW</footer></blockquote>' % (q, n.upper()) for n, q in REVIEWS[1:4])
    body = '''
<main id="main">
<div class="rd-wrap">
<section class="rd-cover" aria-label="Introduction">
<div>
<h1>Drywall, insulation &amp; finishing contractor — Toronto &amp; the GTA</h1>
<p class="rd-display">Good walls go <em>unnoticed.</em></p>
<p class="rd-lede">That is the whole job. Ricarti Drywall insulates, boards and finishes custom homes, additions and townhouses across Toronto and the GTA, Hamilton, Kitchener–Cambridge and Muskoka, for the homeowners who live in them and the builders who build them.</p>
<div style="display:flex;flex-wrap:wrap;gap:14px 20px;align-items:center"><a class="rd-btn" href="/estimate">Book a site visit</a><a class="rd-btn-o" href="/estimate?type=builder">Builders: send drawings</a><a class="rd-link" href="tel:+16474821139">or call (647) 482-1139</a></div>
<div class="rd-byline"><span><b>Est. 2009</b> · family-owned</span><span><b>Level 4</b> standard · Level 5 on request</span><span><b>WSIB</b> clearance on request</span></div>
</div>
<figure>%(cover)s<figcaption class="rd-cap">Brule, Toronto — an arched dormer nook, boarded and ready for tape.</figcaption></figure>
</section>

<nav class="rd-toc" aria-label="On this page">
<a href="/homeowners"><span>01</span><b>For homeowners</b><i>Building or renovating your house</i></a>
<a href="/builders"><span>02</span><b>For builders</b><i>Your insulation &amp; drywall trade</i></a>
<a href="/drywall-finishing-toronto"><span>03</span><b>The finish levels</b><i>Level 4 or Level 5?</i></a>
<a href="/journal"><span>04</span><b>The Journal</b><i>Guides for owners and builders</i></a>
<a href="/reviews"><span>05</span><b>Reviews</b><i>What clients say</i></a>
</nav>
</div>

<article class="rd-feature" aria-labelledby="feat-h">
<figure>%(hero)s<figcaption><p>FEATURE · KENT, TORONTO</p><h2 id="feat-h">One house, every wall, three coats.</h2></figcaption></figure>
<div class="rd-wrap rd-story">
<aside><dl><dt>PROJECT</dt><dd>Full house, Kent, Toronto</dd><dt>SCOPE</dt><dd>Board, tape and finish throughout, stair hall included</dd><dt>FINISH</dt><dd>Level 4, painted</dd><dt>YEAR</dt><dd>2026</dd></dl></aside>
<div class="rd-prose">
<p>Nobody walks into a finished room and admires the drywall. They notice the light from the window, the colour of the paint, the height of the ceiling. If they notice the wall, something has gone wrong: a joint catching the afternoon sun, a ridge along the ceiling, a corner that is not quite straight.</p>
<p>On Kent we boarded, taped and finished the whole house, from the bedrooms to the long stair hall where light runs down the wall from above. Stair halls are where shortcuts show first. Every joint got its coats, every screw was set and filled, and every wall was checked at the end with a work light held flat to the surface, the way low winter sun will hit it.</p>
<p>Then the painters came, and the walls disappeared into the rooms. Which is exactly the point.</p>
<p><a class="rd-link" href="/drywall-finishing-toronto">How we finish, and what Level 4 and 5 mean</a></p>
</div>
<div class="rd-side">%(kent2)s<p class="rd-cap">The stair hall on Kent, boarded and finished before paint.</p></div>
</div>
</article>

<div class="rd-wrap">
<blockquote class="rd-pull"><p>“%(q0)s”</p><footer>%(n0)s · GOOGLE REVIEW</footer></blockquote>
</div>

<section class="rd-two" aria-label="Two ways we work">
<article style="background:#fff">
<p class="rd-kicker">For homeowners</p>
<h3>Building or renovating the house you will live in.</h3>
<p class="rd-muted" style="margin:0;max-width:520px">You deal with the person whose name is on the company. We visit, measure, and give you a written scope that names the insulation, the board and the finish level for each room.</p>
<ul><li>A site visit before any price</li><li>Written scope with the finish level spelled out</li><li>Site swept and bagged at the end of every day</li><li>Final walkthrough under a work light, with you</li></ul>
<div style="margin-top:auto;padding-top:8px;display:flex;flex-wrap:wrap;gap:16px 24px;align-items:center"><a class="rd-btn" href="/estimate">Book a site visit</a><a class="rd-link" href="/homeowners">More for homeowners</a></div>
</article>
<article class="rd-dark">
<p class="rd-kicker">For builders &amp; developers</p>
<h3>Your insulation and drywall trade, on schedule.</h3>
<p style="margin:0;max-width:520px">Detached homes, semis and townhouse blocks. We price from drawings, staff to your schedule, and send the paperwork before the first board goes up.</p>
<ul><li>WSIB clearance and insurance certificate with the quote</li><li>Pricing from drawings, per unit or per block</li><li>One lead hand on site who answers to your super</li><li>Photo updates at insulation inspection and board-ready</li></ul>
<div style="margin-top:auto;padding-top:8px;display:flex;flex-wrap:wrap;gap:16px 24px;align-items:center"><a class="rd-btn" href="/estimate?type=builder">Send drawings for pricing</a><a class="rd-link" href="/builders">More for builders</a></div>
</article>
</section>

<section id="services" class="rd-wrap rd-sec" aria-labelledby="services-h">
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:24px 64px;align-items:end;margin-bottom:36px">
<div><p class="rd-kicker">The index</p><h2 id="services-h" class="rd-h2">Everything between the framing and the <em>paint.</em></h2></div>
<p class="rd-muted" style="margin:0;max-width:460px">One crew from insulation to paint-ready walls. Fewer trades on site, no gap waiting for the next one.</p>
</div>
<div style="border-top:1px solid var(--ink)">%(rows)s</div>
</section>

<section class="rd-wrap rd-sec" aria-labelledby="notes-h">
<div class="rd-notes">
<figure style="margin:0">%(stanton)s<figcaption class="rd-cap">Stanton, Toronto — mineral wool and steel channel, before board.</figcaption></figure>
<div>
<p class="rd-kicker">Field notes · under the board</p>
<h2 id="notes-h" class="rd-h2">The best work on a job is the work you <em>never see.</em></h2>
<p class="rd-lede" style="margin-top:24px;max-width:560px">Before a single sheet goes up, the wall is insulated, sealed and inspected. Get this layer right and the house is warmer, quieter and drier for decades. Get it wrong and no amount of finishing will fix it.</p>
<dl><dt>Warmth</dt><dd>Closed-cell foam at rim joists and sloped ceilings, batts in the walls</dd><dt>Quiet</dt><dd>Mineral wool, resilient channel and sealed penetrations</dd><dt>Dry</dt><dd>A continuous air and vapour barrier, checked before it is covered</dd></dl>
<p style="margin-top:28px"><a class="rd-link" href="/journal/soundproofing-a-room">Read: soundproofing a room</a></p>
</div>
</div>
</section>

<section class="rd-wrap rd-sec" aria-labelledby="journal-h">
<div style="display:flex;flex-wrap:wrap;justify-content:space-between;align-items:end;gap:20px;margin-bottom:36px"><div><p class="rd-kicker">The Journal</p><h2 id="journal-h" class="rd-h2">Know what you are <em>paying for.</em></h2></div><a class="rd-link" href="/journal">All articles</a></div>
<div class="rd-cards">%(cards)s</div>
</section>

<section class="rd-wrap rd-sec" aria-labelledby="reviews-h">
<p class="rd-kicker">Client words</p>
<h2 id="reviews-h" class="rd-h2">In their words, not ours.</h2>
<div class="rd-quotes">%(quotes)s</div>
<p style="margin-top:40px;display:flex;flex-wrap:wrap;gap:16px 28px"><a class="rd-link" href="/reviews">All reviews</a><a class="rd-link" href="%(gmaps)s" rel="noopener">See us on Google</a></p>
</section>

<section class="rd-wrap rd-sec" aria-label="From the owner">
<div class="rd-letter">
<figure style="margin:0">%(thompson)s<figcaption class="rd-cap">On site on Thompson, Toronto.</figcaption></figure>
<div style="max-width:680px">
<p class="rd-kicker">A note from the owner</p>
<blockquote>[Draft — rewrite in your own words.] I want to be judged on the last coat, not the quote. Every house we finish carries our name, so I walk every room with you before we leave, and I tell you plainly if a wall needs more work than you were told.</blockquote>
<p class="rd-sig">Cris</p>
<p style="margin:0;font-size:14px">Cris Ricarti · Owner, Ricarti Drywall · <a href="mailto:cris@ricartidrywall.ca">cris@ricartidrywall.ca</a></p>
</div>
</div>
</section>

<section class="rd-wrap rd-sec" aria-labelledby="faq-h">
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:40px 64px;align-items:start">
<div><p class="rd-kicker">Questions</p><h2 id="faq-h" class="rd-h2">What people ask before they call.</h2></div>
<div class="rd-faq" style="border-top:1px solid var(--hair)">%(faq)s</div>
</div>
</section>
</main>
''' % dict(cover=img('brule-01.jpg', 'An arched dormer nook boarded in moisture-resistant drywall, Brule, Toronto', eager=True),
           hero=img('hero-kent.jpg', 'A finished bedroom on Kent, Toronto: smooth painted walls and ceiling with a wide window', w=2160, h=1215),
           kent2=img('kent-02.jpg', 'Long stair hall with finished drywall walls, Kent, Toronto'),
           stanton=img('stanton-03.jpg', 'Mineral wool insulation behind steel resilient channel, Stanton, Toronto'),
           thompson=img('thompson-01.jpg', 'A finisher on stilts skimming a ceiling, Thompson, Toronto'),
           q0=REVIEWS[0][1], n0=REVIEWS[0][0].upper(), rows=rows, cards=''.join(card(a) for a in ARTICLES[:3]),
           quotes=quotes, gmaps=GMAPS, faq=faq_html())
    body += band('Start with a site visit, not a <em>guess.</em>', ('Book a site visit', '/estimate'), ('Builders: send drawings', '/estimate?type=builder'))
    build.write_page('', 'Ricarti Drywall | Drywall, insulation and finishing in Toronto and the GTA',
        'Family-owned since 2009. Insulation, steel framing, drywall and Level 4 or Level 5 finishing for homeowners and builders across Toronto, the GTA, Hamilton, Kitchener-Cambridge and Muskoka.',
        shell('/', body), css=HOME_CSS, image='hero-kent.jpg')

# ---------------------------------------------------------------- REVIEWS
def reviews():
    big = REVIEWS[0]
    rest = ''.join('<blockquote><p>“%s”</p><footer>%s · GOOGLE REVIEW</footer></blockquote>' % (q, n.upper()) for n, q in REVIEWS[1:])
    body = '''<main id="main" class="rd-wrap">
<section style="padding-top:clamp(48px,7vw,96px)">
<p class="rd-kicker">Reviews</p>
<h1 class="rd-h2" style="font-size:clamp(44px,6vw,88px);max-width:1000px">What our clients say about the <em>finished walls.</em></h1>
<p class="rd-lede" style="margin-top:28px;max-width:640px">Homeowners and builders across Toronto and the GTA, in their own words. These reviews come from our Google Business Profile.</p>
</section>
<blockquote class="rd-pull" style="border-top:1px solid var(--hair);margin-top:56px"><p>“%s”</p><footer>%s · GOOGLE REVIEW</footer></blockquote>
<div class="rd-quotes" style="grid-template-columns:repeat(2,minmax(0,1fr))">%s</div>
<section class="rd-sec" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:32px 64px;align-items:center">
<div><p class="rd-kicker">Worked with us?</p><h2 class="rd-h2">A review helps the next family find a good crew.</h2></div>
<div style="display:flex;flex-wrap:wrap;gap:14px"><a class="rd-btn" href="%s" rel="noopener">Leave a Google review</a><a class="rd-btn-o" href="%s" rel="noopener">Tag us on Instagram</a></div>
</section>
</main>''' % (big[1], big[0].upper(), rest, GMAPS, chrome.IG)
    body += band('Your project could be <em>next.</em>')
    build.write_page('/reviews', 'Reviews | Ricarti Drywall, Toronto',
        'Google reviews from homeowners and builders who hired Ricarti Drywall for insulation, drywall, taping and plaster repair in Toronto and the GTA.',
        shell('/reviews', body), css=HOME_CSS, crumbs=[('Home', '/'), ('Reviews', '/reviews')])

# ---------------------------------------------------------------- JOURNAL
def journal():
    lead = ARTICLES[0]
    others = ''.join(card(a) for a in ARTICLES[1:])
    body = '''<main id="main" class="rd-wrap">
<section style="padding-top:clamp(48px,7vw,96px);display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:24px 64px;align-items:end">
<div><p class="rd-kicker">The Journal</p><h1 class="rd-h2" style="font-size:clamp(48px,7vw,104px)">Notes from <em>the site.</em></h1></div>
<p class="rd-lede">Plain-language guides on insulation, drywall, finishing and sound, for homeowners planning a project and builders pricing one. Written by the people who do the work.</p>
</section>
<a class="rd-card" href="/journal/%(slug)s" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:24px 56px;align-items:center;margin-top:56px;border-top:1px solid var(--ink);padding-top:40px">
%(img)s
<span><span class="rd-label">Featured · %(cat)s · %(read)s read</span><span class="rd-ct" style="font-size:clamp(32px,3.4vw,48px);line-height:1.08;margin:14px 0 18px">%(title)s</span><span class="rd-muted" style="display:block;font-size:17px">%(desc)s</span><span class="rd-link" style="display:inline-block;margin-top:22px">Read the article</span></span>
</a>
<div class="rd-cards rd-sec" style="grid-template-columns:repeat(auto-fit,minmax(260px,1fr))">%(others)s
<a class="rd-card" href="/drywall-finishing-toronto">%(fimg)s<span class="rd-label">Finishing · 7 min read</span><span class="rd-ct">Level 4 or Level 5? The drywall finish levels in plain words</span></a>
</div>
</main>''' % dict(lead, img=img(lead['image'], lead['alt'], eager=True, style='width:100%;aspect-ratio:4/3;object-fit:cover;display:block'), others=others,
                  fimg=img('kent-01.jpg', 'Finished, painted bedroom walls, Kent, Toronto'))
    body += band('Questions about your project? <em>Ask us.</em>')
    build.write_page('/journal', 'Journal: drywall, insulation and finishing guides | Ricarti Drywall',
        'Guides on spray foam vs batts, drywall finish levels, soundproofing, lath and plaster repair, and pricing drywall for builders. From a Toronto drywall contractor.',
        shell('/journal', body), css=HOME_CSS, ptype='CollectionPage', crumbs=[('Home', '/'), ('Journal', '/journal')])
    for a in ARTICLES:
        article(a)

def article(a):
    url = '/journal/' + a['slug']
    related = ''.join(card(b) for b in ARTICLES if b is not a)[:]
    rel = [b for b in ARTICLES if b is not a][:3]
    body = '''<main id="main">
<article>
<header class="rd-wrap" style="padding-top:clamp(40px,6vw,80px);max-width:1100px;margin:0 auto">
<nav aria-label="Breadcrumb" style="font-size:13px;margin-bottom:28px" class="rd-muted"><a href="/">Home</a> / <a href="/journal">Journal</a> / %(cat)s</nav>
<p class="rd-kicker">%(cat)s · %(read)s read</p>
<h1 style="margin:0;font:300 clamp(40px,5.6vw,80px)/1.02 var(--serif);letter-spacing:-.02em">%(title)s</h1>
<p class="rd-lede" style="margin-top:24px;max-width:720px">%(desc)s</p>
<p style="margin:24px 0 0;font-size:13px" class="rd-muted">By Ricarti Drywall · <time datetime="%(date)s">%(dated)s</time></p>
</header>
<figure class="rd-wrap" style="margin:48px auto 0;max-width:1300px">%(img)s<figcaption class="rd-cap">%(alt)s.</figcaption></figure>
<div class="rd-wrap" style="max-width:780px;margin:0 auto;padding-top:56px">
<div class="rd-short"><b>IN SHORT</b>%(short)s</div>
<div class="rd-prose">%(body)s</div>
<div style="margin-top:48px;padding:28px;background:var(--gypsum);display:flex;flex-wrap:wrap;gap:16px 24px;align-items:center;justify-content:space-between"><span style="font:300 22px/1.3 var(--serif);max-width:420px">Planning a project? We will walk it with you and put it in writing.</span><span style="display:flex;flex-wrap:wrap;gap:12px"><a class="rd-btn" href="/estimate">Book a site visit</a><a class="rd-btn-o" href="/estimate?type=builder">Builders: pricing</a></span></div>
</div>
</article>
<section class="rd-wrap rd-sec" aria-labelledby="more-h"><h2 id="more-h" class="rd-h2" style="font-size:clamp(28px,3vw,40px);margin-bottom:32px">Keep reading</h2><div class="rd-cards">%(rel)s</div></section>
</main>''' % dict(a, dated='24 November 2026', img=img(a['image'], a['alt'], eager=True, style='width:100%;height:clamp(300px,48vw,640px);object-fit:cover;display:block'),
                  rel=''.join(card(b) for b in rel))
    schema = [{"@type": "BlogPosting", "headline": a['title'], "description": a['desc'], "image": build.SITE + '/images/' + a['image'],
               "datePublished": a['date'], "dateModified": a['date'], "inLanguage": "en", "mainEntityOfPage": build.SITE + url,
               "author": {"@id": build.SITE + "/#business"}, "publisher": {"@id": build.SITE + "/#business"}, "articleSection": a['cat']}]
    build.write_page(url, a['title'] + ' | Ricarti Drywall', a['desc'], shell('/journal', body), css=HOME_CSS + PROSE_FIX,
                     extra_schema=schema, image=a['image'], ptype='BlogPosting', crumbs=[('Home', '/'), ('Journal', '/journal'), (a['title'], url)])

PROSE_FIX = '.rd-prose blockquote{margin:40px 0}'

# ---------------------------------------------------------------- SEARCH
def search_page():
    body = '''<main id="main" class="rd-wrap" style="max-width:900px;padding-top:clamp(48px,7vw,96px);min-height:60vh">
<p class="rd-kicker">Search</p>
<h1 class="rd-h2">Find a guide, a service or an answer.</h1>
<form class="rd-sform" action="/search" role="search" style="margin-top:36px"><svg class="rd-ico" viewBox="0 0 24 24" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5 21 21"/></svg><input id="rd-pq" name="q" type="search" placeholder="Spray foam, Level 5, soundproofing…" aria-label="Search the site"><button type="submit">SEARCH</button></form>
<div id="rd-psugg" class="rd-sugg">Popular: <a href="/search?q=Level+5">Level 5 finish</a><a href="/search?q=spray+foam">Spray foam</a><a href="/search?q=soundproofing">Soundproofing</a><a href="/search?q=plaster">Plaster repair</a><a href="/search?q=WSIB">WSIB</a></div>
<ul id="rd-pres" class="rd-res" aria-live="polite"></ul>
</main>
<script>
document.addEventListener("DOMContentLoaded",function(){var i=document.getElementById("rd-pq"),u=document.getElementById("rd-pres"),s=document.getElementById("rd-psugg"),q=new URLSearchParams(location.search).get("q")||"";i.value=q;
function go(){rdSearch.load().then(function(){rdSearch.render(i.value,u,s);});}
i.addEventListener("input",go);if(q)go();else i.focus();});
</script>'''
    build.write_page('/search', 'Search | Ricarti Drywall', 'Search the Ricarti Drywall site: services, guides, service areas and answers about drywall, insulation and finishing.',
                     shell('/search', body, ig=False))

# ---------------------------------------------------------------- INDEX
def search_index():
    items = []
    for root, dirs, files in os.walk(OUT):
        if '.git' in root or 'images' in root or 'assets' in root:
            continue
        if 'index.html' not in files:
            continue
        rel = '/' + os.path.relpath(root, OUT).replace('.', '').strip('/')
        rel = '/' if rel == '/' else rel
        if rel in ('/search',) or rel.startswith(('/pt', '/fr', '/it', '/he')):
            continue
        s = open(os.path.join(root, 'index.html')).read()
        title = html.unescape(re.search(r'<title>(.*?)</title>', s).group(1)).split(' | ')[0]
        if rel == '/':
            title = 'Ricarti Drywall — home'
        desc = html.unescape(re.search(r'<meta name="description" content="(.*?)"', s).group(1))
        m = re.search(r'<main\b.*?</main>', s, re.S)
        txt = m.group(0) if m else ''
        txt = re.sub(r'<(script|style|nav)\b.*?</\1>', ' ', txt, flags=re.S)
        txt = re.sub(r'<p class="rd-kicker">.*?</p>', ' ', txt, count=1, flags=re.S)
        txt = re.sub(r'<[^>]+>', ' ', txt)
        txt = re.sub(r'\s+', ' ', html.unescape(txt)).strip()
        kind = 'Journal' if rel.startswith('/journal/') else {'/homeowners': 'Homeowners', '/builders': 'Builders', '/areas': 'Service areas', '/estimate': 'Contact',
                                                                '/reviews': 'Reviews', '/journal': 'Journal', '/drywall-finishing-toronto': 'Service', '/': 'Home'}.get(rel, 'Page')
        items.append({'u': rel, 't': title, 'd': desc, 'k': kind, 'x': txt[:6000]})
    order = {'Home': 0, 'Service': 1, 'Homeowners': 1, 'Builders': 1, 'Journal': 2}
    items.sort(key=lambda i: (order.get(i['k'], 3), i['u']))
    json.dump(items, open(OUT + 'search-index.json', 'w'), ensure_ascii=False, separators=(',', ':'))
    print('search index', len(items), 'pages')

if __name__ == '__main__':
    home(); reviews(); journal(); search_page()
    search_index()
