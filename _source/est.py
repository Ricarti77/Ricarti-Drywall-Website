"""Estimate page (Task 010): two enquiry paths, private drawing/photo upload, CRM-ready payload.

Delivery: POST to /api/enquiry (Vercel Function), which validates it and emails cris@ricartidrywall.ca via Resend (Graph kept as a disabled alternative). Was FormSubmit until Task 010-A; its JSON
endpoint, so the page only shows success when the service confirms it. Files go to a private Vercel Blob store through
short-lived presigned URLs issued by /api/uploads/sign — only when that store has been created and switched on
(see /api/uploads/config). Until then the page says so plainly and sends the enquiry without the files.
"""
import os, sys, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build, chrome, pages


def opt(v, t):
    return '<option value="%s">%s</option>' % (v, t)

def chk(name, v, t, path='both'):
    return ('<label class="rd-chip" data-path="%s"><input type="checkbox" name="%s" value="%s"><span>%s</span></label>' % (path, name, v, t))

SERVICES = [
    ('insulation', 'Insulation &amp; spray foam', 'both'),
    ('drywall-installation', 'Drywall installation', 'both'),
    ('taping-finishing', 'Taping &amp; finishing (Level 4 / Level 5)', 'both'),
    ('architectural-finishing', 'Architectural details (curves, reveals, trimless)', 'both'),
    ('soundproofing', 'Soundproofing', 'both'),
    ('metal-stud-framing', 'Metal stud framing', 'both'),
    ('popcorn-ceiling', 'Popcorn ceiling removal', 'home'),
    ('repairs', 'Repairs &amp; plaster', 'home'),
]

BODY = '''
<main id="main" class="rd-eq">
<div class="rd-eq-in">
<section class="rd-eq-intro" aria-labelledby="est-h">
<p class="rd-eq-k">ESTIMATE · SITE VISIT</p>
<h1 id="est-h">Tell us about the <em>job.</em></h1>
<p class="rd-eq-lede">Homeowners: a few details and some photos are enough to start. Builders and contractors: send your drawings for pricing.</p>
<p class="rd-eq-alt">Rather talk? <a href="tel:+16474821139" data-cta="call" data-cta-loc="estimate">Call (647) 482-1139</a> or <a href="mailto:cris@ricartidrywall.ca" data-cta="email" data-cta-loc="estimate">email cris@ricartidrywall.ca</a>.</p>
<ol class="rd-eq-steps">
<li><span>01</span><span>We read your enquiry and contact you to confirm the details.</span></li>
<li><span>02</span><span>A site visit, or a first look at your photos and drawings.</span></li>
<li><span>03</span><span>A written scope and price: materials, finish level and schedule.</span></li>
</ol>
</section>

<section class="rd-eq-card" aria-labelledby="est-form-h">
<h2 id="est-form-h" class="rd-vh">Enquiry form</h2>

<div id="rd-done" class="rd-eq-done" hidden tabindex="-1">
<p class="rd-eq-k">ENQUIRY SENT</p>
<h2>Thank you. Your enquiry has been sent.</h2>
<p>It went straight to Cris Ricarti at cris@ricartidrywall.ca. We will review it and contact you to discuss the next step.</p>
<p class="rd-done-ref">Reference: <b id="rd-done-id"></b></p>
<p id="rd-done-files" class="rd-done-files" hidden></p>
<p id="rd-done-nofiles" class="rd-done-warn" hidden>Your files were not uploaded. Please email them to <a href="mailto:cris@ricartidrywall.ca">cris@ricartidrywall.ca</a> and mention your reference.</p>
<p><button type="button" class="rd-ef-link" id="rd-again">Send another enquiry</button></p>
</div>

<form id="rd-form" class="rd-ef" novalidate>
<fieldset class="rd-ef-who">
<legend>I am</legend>
<div class="rd-seg">
<label class="rd-seg-o"><input type="radio" name="customer_type" value="homeowner" checked><span class="rd-seg-t">A homeowner</span><span class="rd-seg-s">A home you live in, are building or renovating</span></label>
<label class="rd-seg-o"><input type="radio" name="customer_type" value="builder"><span class="rd-seg-t">A builder or contractor</span><span class="rd-seg-s">Pricing from drawings, per unit or per project</span></label>
</div>
</fieldset>

<div class="rd-ef-grid">
<div class="rd-f" data-path="both"><label for="f-name"><span data-path="home">Full name</span><span data-path="builder">Contact name</span> <span class="rd-req">required</span></label><input id="f-name" name="name" type="text" autocomplete="name" required maxlength="120"><p class="rd-err" id="e-name" hidden></p></div>
<div class="rd-f" data-path="builder"><label for="f-company">Company name</label><input id="f-company" name="company" type="text" autocomplete="organization" maxlength="160"></div>
<div class="rd-f"><label for="f-email">Email <span class="rd-req">required</span></label><input id="f-email" name="email" type="email" autocomplete="email" inputmode="email" required maxlength="160"><p class="rd-err" id="e-email" hidden></p></div>
<div class="rd-f"><label for="f-phone">Phone</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" maxlength="40"><p class="rd-err" id="e-phone" hidden></p></div>
<div class="rd-f rd-f-wide"><label for="f-address"><span data-path="home">Project location</span><span data-path="builder">Project address</span></label><input id="f-address" name="address" type="text" autocomplete="street-address" maxlength="200" aria-describedby="h-address"><p class="rd-hint" id="h-address"><span data-path="home">Street and city, or postal code</span><span data-path="builder">Street and city, lot or site name</span></p></div>
<div class="rd-f" data-path="builder"><label for="f-ptype">Project type</label><select id="f-ptype" name="project_type">
%(ptypes)s
</select></div>
<div class="rd-f"><label for="f-timeline" id="l-timeline"><span data-path="home">Preferred timeline</span><span data-path="builder">Construction timeline</span></label>
<select id="f-timeline" name="timeline" data-path="home">
%(htimes)s
</select>
<select id="f-btimeline" name="timeline" data-path="builder" aria-labelledby="l-timeline">
%(btimes)s
</select></div>
</div>

<fieldset class="rd-ef-svc">
<legend>Services needed <span class="rd-hint-i">choose any that apply</span></legend>
<div class="rd-chips">
%(services)s
</div>
</fieldset>

<div class="rd-f rd-f-wide"><label for="f-notes"><span data-path="home">Project description</span><span data-path="builder">Project notes</span></label><textarea id="f-notes" name="notes" rows="5" maxlength="4000" aria-describedby="h-notes"></textarea><p class="rd-hint" id="h-notes"><span data-path="home">Rooms, ceiling heights, the finish you have in mind, anything we should know.</span><span data-path="builder">Units, phasing, board-ready dates, finish level by area, site access.</span></p></div>

<div class="rd-f rd-f-wide rd-up">
<p class="rd-up-l" id="up-l"><span data-path="home">Photos <span class="rd-opt">optional</span></span><span data-path="builder">Architectural drawings <span class="rd-opt">optional</span></span></p>
<div class="rd-drop" id="rd-drop">
<input id="f-files" class="rd-drop-in" type="file" multiple accept=".pdf,.jpg,.jpeg,.png,.webp,.heic,.heif,application/pdf,image/jpeg,image/png,image/webp,image/heic,image/heif" aria-labelledby="up-l" aria-describedby="up-h up-off">
<label for="f-files" class="rd-drop-t"><span class="rd-drop-ico" aria-hidden="true"></span><span><b>Drag and drop files here</b> or <u>choose files</u></span></label>
<p class="rd-hint" id="up-h">PDF drawings, JPG, PNG, WebP or HEIC photos. Up to 20 files, 50 MB each.</p>
</div>
<p class="rd-up-off" id="up-off" hidden>Secure file upload is not switched on yet. Your enquiry will be sent without the files, and we will ask you to email them.</p>
<ul class="rd-files" id="rd-files" aria-live="polite"></ul>
</div>

<fieldset class="rd-ef-consent">
<legend class="rd-vh">Privacy and consent</legend>
<p class="rd-privacy" id="rd-privacy">We use the details you send only to reply to your enquiry and to prepare your estimate. Your enquiry is sent through our website's secure server and our email delivery provider (Resend, United States) to Ricarti Drywall's business email, and we email you a confirmation; files you upload are kept in private storage and are not publicly accessible. We do not sell your information. To see, correct or delete it, email <a href="mailto:cris@ricartidrywall.ca">cris@ricartidrywall.ca</a>.</p>
<label class="rd-check"><input type="checkbox" name="marketing_opt_in" value="yes"><span>Optional: I would like to receive occasional project news and seasonal tips from Ricarti Drywall by email. I can unsubscribe at any time.</span></label>
</fieldset>

<div class="rd-hp" aria-hidden="true"><label for="f-hp">Leave this field empty</label><input id="f-hp" name="_honey" type="text" tabindex="-1" autocomplete="off"></div>

<div class="rd-ef-send">
<button type="submit" class="rd-ef-btn" id="rd-submit" data-cta="estimate-submit" data-cta-loc="estimate-form"><span data-path="home">Send enquiry</span><span data-path="builder">Request pricing</span></button>
<p class="rd-hint">By sending, you agree to the use of your details described above.</p>
</div>
<div class="rd-status" id="rd-status" role="status" aria-live="polite"></div>
<div class="rd-alert" id="rd-alert" role="alert" hidden><p id="rd-alert-t"></p><p id="rd-alert-unk" hidden>Please do not send it again yet. Email <a href="mailto:cris@ricartidrywall.ca">cris@ricartidrywall.ca</a> or call <a href="tel:+16474821139">(647) 482-1139</a> and mention your reference, and we will check whether it arrived.</p><p id="rd-alert-none">Nothing was sent. Please try again, or email <a href="mailto:cris@ricartidrywall.ca">cris@ricartidrywall.ca</a> or call <a href="tel:+16474821139">(647) 482-1139</a>.</p></div>
</form>
</section>
</div>
</main>
'''

PTYPES = [('', 'Select…'), ('custom-home', 'Custom home'), ('detached-homes', 'Detached homes'), ('semi-detached', 'Semi-detached homes'),
          ('townhouse-block', 'Townhouse block'), ('low-rise-multi', 'Low-rise multi-unit'), ('addition-renovation', 'Addition or renovation'),
          ('commercial-interior', 'Commercial interior'), ('other', 'Other')]
HTIMES = [('', 'Select…'), ('asap', 'As soon as possible'), ('1-3-months', 'In 1–3 months'), ('3-6-months', 'In 3–6 months'), ('flexible', 'Flexible'), ('not-sure', 'Not sure yet')]
BTIMES = [('', 'Select…'), ('under-1-month', 'Board-ready within a month'), ('1-3-months', 'In 1–3 months'), ('3-6-months', 'In 3–6 months'),
          ('6-12-months', 'In 6–12 months'), ('tender', 'Pricing for a tender'), ('not-scheduled', 'Not scheduled yet')]

CSS = '''
.rd-vh{position:absolute!important;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.rd-eq{background:var(--plaster);color:var(--ink)}
.rd-eq-in{max-width:1440px;margin:0 auto;padding:clamp(28px,5vw,72px) var(--pad) 96px;display:flex;flex-wrap:wrap;gap:48px clamp(40px,6vw,88px);align-items:flex-start}
.rd-eq-intro{flex:1 1 320px;max-width:500px}
.rd-eq-k{margin:0 0 14px;font-size:11px;letter-spacing:.16em;font-weight:600;color:var(--spruce)}
.rd-eq-intro h1{margin:0;font-family:'Cormorant Garamond',Georgia,serif;font-weight:300;font-size:clamp(42px,5vw,68px);line-height:1;letter-spacing:-.02em}
.rd-eq-intro h1 em{color:var(--spruce)}
.rd-eq-lede{margin:22px 0 0;font-size:18px;line-height:1.55;color:var(--muted)}
.rd-eq-alt{margin:16px 0 0;font-size:15px}
.rd-eq-alt a{color:inherit;text-decoration:none;border-bottom:1px solid var(--bronze);display:inline-block;padding:10px 0 2px;margin:-10px 0 0}
.rd-eq-steps{margin:40px 0 0;padding:0;list-style:none;border-top:1px solid var(--hair);font-size:15px}
.rd-eq-steps li{display:grid;grid-template-columns:40px minmax(0,1fr);padding:15px 0;border-bottom:1px solid var(--hair)}
.rd-eq-steps li span:first-child{font-family:'Cormorant Garamond',Georgia,serif;color:var(--spruce);font-size:17px}
.rd-eq-card{flex:999 1 520px;min-width:0;max-width:780px;background:#fff;padding:clamp(22px,4vw,48px);box-sizing:border-box;border:1px solid var(--hair)}
.rd-ef{display:flex;flex-direction:column;gap:30px}
.rd-ef[hidden],.rd-eq-done[hidden],.rd-alert[hidden],.rd-alert p[hidden],.rd-up-off[hidden]{display:none!important}
.rd-ef fieldset{border:0;margin:0;padding:0;min-width:0}
.rd-ef legend,.rd-ef label:not(.rd-chip):not(.rd-seg-o):not(.rd-check):not(.rd-drop-t),.rd-up-l{display:block;margin:0 0 10px;padding:0;font-size:11px;letter-spacing:.14em;font-weight:600;text-transform:uppercase;color:var(--ink)}
.rd-req,.rd-opt,.rd-hint-i{font-size:10.5px;letter-spacing:.08em;font-weight:500;color:var(--spruce);margin-left:6px;text-transform:uppercase}
.rd-opt,.rd-hint-i{color:var(--stone)}
.rd-seg{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.rd-seg-o{position:relative;display:flex;flex-direction:column;gap:4px;padding:16px 18px 16px 46px;border:1px solid var(--hair);cursor:pointer;min-height:44px;transition:border-color .2s,background-color .2s}
.rd-seg-o input{position:absolute;left:18px;top:19px;width:18px;height:18px;margin:0;accent-color:var(--ink)}
.rd-seg-t{font-size:16px;font-weight:600}
.rd-seg-s{font-size:13.5px;color:var(--muted);line-height:1.4}
.rd-seg-o:has(input:checked){border-color:var(--ink);background:var(--plaster)}
.rd-seg-o:has(input:focus-visible){outline:2px solid var(--bronze);outline-offset:2px}
.rd-ef-grid{display:grid;grid-template-columns:1fr 1fr;gap:24px 22px}
.rd-f{min-width:0}
.rd-f-wide{grid-column:1/-1}
.rd-ef input[type=text],.rd-ef input[type=email],.rd-ef input[type=tel],.rd-ef select,.rd-ef textarea{width:100%;box-sizing:border-box;font:inherit;font-size:16px;color:var(--ink);background:#fff;border:1px solid var(--hair);border-radius:0;padding:12px 14px;min-height:48px;transition:border-color .2s}
.rd-ef textarea{resize:vertical;min-height:120px;line-height:1.5}
.rd-ef select{appearance:none;background-image:linear-gradient(45deg,transparent 50%,var(--ink) 50%),linear-gradient(135deg,var(--ink) 50%,transparent 50%);background-position:calc(100% - 19px) 21px,calc(100% - 14px) 21px;background-size:5px 5px;background-repeat:no-repeat;padding-right:38px}
.rd-ef input:focus,.rd-ef select:focus,.rd-ef textarea:focus{outline:none;border-color:var(--ink);box-shadow:0 0 0 2px rgba(168,134,90,.45)}
.rd-ef [aria-invalid=true]{border-color:#9A3B2E!important}
.rd-err{margin:6px 0 0;font-size:13.5px;color:#9A3B2E}
.rd-hint{margin:6px 0 0;font-size:13px;line-height:1.45;color:var(--muted)}
.rd-chips{display:flex;flex-wrap:wrap;gap:8px}
.rd-chip{position:relative;display:inline-flex}
.rd-chip input{position:absolute;opacity:0;inset:0;margin:0;cursor:pointer}
.rd-chip span{display:inline-flex;align-items:center;min-height:44px;box-sizing:border-box;padding:10px 16px;border:1px solid var(--hair);font-size:14.5px;cursor:pointer;transition:border-color .2s,background-color .2s,color .2s}
.rd-chip input:checked+span{background:var(--ink);border-color:var(--ink);color:var(--warm)}
.rd-chip input:checked+span::before{content:"✓";margin-right:8px;font-size:13px}
.rd-chip input:focus-visible+span{outline:2px solid var(--bronze);outline-offset:2px}
.rd-drop{position:relative;border:1px dashed var(--stone);background:var(--plaster);padding:26px 20px;text-align:center;transition:border-color .2s,background-color .2s}
.rd-drop.is-over{border-color:var(--ink);background:var(--gypsum)}
.rd-drop-in{position:absolute;inset:0;width:100%;height:100%;opacity:0;cursor:pointer}
.rd-drop-in:focus-visible+.rd-drop-t{outline:2px solid var(--bronze);outline-offset:4px}
.rd-drop-t{display:inline-flex;align-items:center;gap:12px;font-size:15.5px;cursor:pointer;min-height:44px}
.rd-drop-t u{text-decoration-color:var(--bronze);text-underline-offset:4px}
.rd-drop-ico{width:22px;height:22px;border:1.5px solid var(--ink);border-top:0;position:relative;flex:none}
.rd-drop-ico::before{content:"";position:absolute;left:50%;top:-6px;width:1.5px;height:16px;background:var(--ink);transform:translateX(-50%)}
.rd-drop-ico::after{content:"";position:absolute;left:50%;top:-6px;width:8px;height:8px;border-left:1.5px solid var(--ink);border-top:1.5px solid var(--ink);transform:translateX(-50%) rotate(45deg)}
.rd-up-off{margin:10px 0 0;font-size:13.5px;line-height:1.45;color:var(--ink);background:var(--gypsum);border-left:3px solid var(--bronze);padding:10px 12px}
.rd-files{list-style:none;margin:12px 0 0;padding:0}
.rd-files li{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:4px 12px;align-items:center;padding:10px 0;border-bottom:1px solid var(--hair);font-size:14px}
.rd-files .n{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.rd-files .m{color:var(--muted);font-size:12.5px;grid-column:1}
.rd-files .x{grid-row:1/3;grid-column:2;background:none;border:1px solid var(--hair);font:inherit;font-size:13px;min-height:44px;min-width:44px;padding:0 12px;cursor:pointer;color:var(--ink)}
.rd-files .bar{grid-column:1/-1;height:3px;background:var(--gypsum);overflow:hidden}
.rd-files .bar i{display:block;height:100%;width:0;background:var(--bronze);transition:width .2s}
.rd-files li.is-bad{color:#9A3B2E}
.rd-files li.is-bad .m{color:#9A3B2E}
.rd-files li.is-done .bar i{background:var(--ink)}
.rd-privacy{margin:0 0 14px;font-size:13.5px;line-height:1.55;color:var(--muted)}
.rd-privacy a,.rd-alert a,.rd-eq-done a{color:inherit}
.rd-check{display:flex;gap:12px;align-items:flex-start;font-size:14.5px;line-height:1.5;cursor:pointer;min-height:44px}
.rd-check input{width:20px;height:20px;margin:2px 0 0;flex:none;accent-color:var(--ink)}
.rd-hp{position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden}
.rd-ef-send{display:flex;flex-wrap:wrap;align-items:center;gap:12px 20px}
.rd-ef-send .rd-hint{margin:0;flex:1 1 220px}
.rd-ef-btn{font:inherit;font-size:15px;font-weight:600;background:var(--ink);color:var(--warm);border:1px solid var(--ink);padding:16px 30px;min-height:52px;cursor:pointer;transition:background-color .25s}
.rd-ef-btn:hover{background:#000}
.rd-ef-btn[disabled]{opacity:.55;cursor:progress}
.rd-ef-btn:focus-visible,.rd-ef-link:focus-visible{outline:2px solid var(--bronze);outline-offset:3px}
.rd-status{font-size:14px;color:var(--muted);min-height:1px}
.rd-alert{border-left:3px solid #9A3B2E;background:#F6ECE8;padding:12px 16px;font-size:14.5px;line-height:1.5}
.rd-alert p{margin:0}.rd-alert p+p{margin-top:6px}
.rd-eq-done h2{margin:0;font-family:'Cormorant Garamond',Georgia,serif;font-weight:300;font-size:clamp(32px,4vw,44px);line-height:1.05}
.rd-eq-done p{margin:16px 0 0;color:var(--muted);line-height:1.55;max-width:520px}
.rd-eq-done:focus{outline:none}
.rd-done-ref b{color:var(--ink);letter-spacing:.04em}
.rd-done-warn{border-left:3px solid var(--bronze);background:var(--gypsum);padding:10px 12px;color:var(--ink)!important}
.rd-ef-link{background:none;border:0;padding:12px 0;font:inherit;font-weight:600;color:var(--ink);border-bottom:1px solid var(--bronze);cursor:pointer}
.rd-ef [data-path][hidden],.rd-eq-card [data-path][hidden]{display:none!important}
@media (max-width:640px){.rd-seg,.rd-ef-grid{grid-template-columns:1fr}.rd-ef-btn{width:100%}.rd-seg-o{padding:14px 14px 14px 44px}}
@media (prefers-reduced-motion:reduce){.rd-files .bar i{transition:none}}
'''

def main():
    body = BODY % dict(
        ptypes='\n'.join(opt(v, t) for v, t in PTYPES),
        htimes='\n'.join(opt(v, t) for v, t in HTIMES),
        btimes='\n'.join(opt(v, t) for v, t in BTIMES),
        services='\n'.join(chk('services', v, t, p) for v, t, p in SERVICES))
    js = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'estimate.js')).read()
    body = body + '<script>\n' + js + '\n</script>\n'
    build.write_page('/estimate', 'Request an estimate or send drawings | Ricarti Drywall',
                     'Homeowners: send a few details and photos. Builders and contractors: send drawings for pricing. Insulation, drywall and finishing across the GTA, Hamilton, Kitchener-Cambridge and Muskoka.',
                     pages.shell('/estimate', body, ig=False), css=pages.HOME_CSS + CSS,
                     crumbs=[('Home', '/'), ('Estimate', '/estimate')])

if __name__ == '__main__':
    main()
