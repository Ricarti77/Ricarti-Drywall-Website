# Ricarti Drywall website — development roadmap

Official cumulative branch: `preview/ricarti-dev` (backup: `preview/ricarti-website-development`).
Every task builds on the latest version of that branch. Nothing is merged into `main` without the owner's approval.
The live WordPress site (ricartidrywall.ca), DNS and Vercel security settings are never touched.

## Completed (awaiting approval to merge)
| Task | What | Status |
|---|---|---|
| 001 | Homepage hero: "Perfection Starts Here!", eyebrow, sub-headline, CTAs, vertical photo | Done |
| 002 | Original logo 30% larger, centred between nav and search | Done |
| 003 | Our Expertise — six services | Done |
| 004 | Selected Projects portfolio, filters, per-project galleries, `content/projects.json` | Done |
| 005 | Premium For Builders landing page | Done |
| 006 | Premium For Homeowners landing page | Done |
| 007 | Six individual service pages (EN + PT), shared navigation data | Done, awaiting approval |

---

## A. Advanced website navigation (planned, dedicated task)

**Requirements**
- Sticky header that stays reachable while scrolling.
- Elegant dropdown menus.
- Direct links to each service page and each project category.
- Section navigation (in-page) on longer pages.
- Responsive mobile navigation with expandable submenus.
- Keep the enlarged original logo exactly as it is (lettering, proportions, identity).
- Keep the existing site search.

**Already in place**
- Sticky header on every page (since the first build) with the search box and `/` or Ctrl+K shortcut.
- Mobile menu (single level) and a sticky Call / Estimate bar on phones.
- Logo enlarged and centred (Task 002).

**Dependencies — do first**
- ~~Individual service pages~~ — done in Task 007 (six pages, EN + PT). Spanish and French versions to follow.
- Shared navigation definition ready: `_source/content/navigation.json` (primary items, service children, project categories). Footer already uses it; Task 008 renders dropdowns from it.
- Project category pages or anchors (`/projects?category=…` or `/projects/<category>`), fed by `content/projects.json`.

**Architecture plan**
- One navigation definition (single data file) used by the desktop dropdowns, the mobile menu, the footer and every language.
- Desktop: hover **and** click/keyboard to open (Enter/Space, Escape closes, arrow keys), `aria-expanded`, no hover-only menus.
- Mobile: expandable sections (`<details>`/buttons with `aria-expanded`), large tap targets, works without JavaScript.
- Section navigation: generated from each long page's `h2` headings (sticky sub-nav on desktop, collapsed on phones).
- Header height and the centred-logo rule stay as they are; dropdown panels open below the header without shifting the logo.

---

## B. Multilingual website (planned, dedicated tasks)

**Languages (final list — replaces the earlier five-language plan)**
| Language | Variant | URL prefix | `hreflang` / `lang` | `og:locale` | Status |
|---|---|---|---|---|---|
| English | Canadian English — **default** | `/` | `en-CA` | `en_CA` | Live in preview |
| Portuguese | Brazilian Portuguese | `/pt/` | `pt-BR` | `pt_BR` | Live in preview |
| Spanish | Latin American Spanish | `/es/` | `es-419` | `es_LA` | Planned |
| French | Canadian French | `/fr/` | `fr-CA` | `fr_CA` | Planned |

Italian and Hebrew are no longer planned. `x-default` points to the English page.

**Requirements**
- Complete content in all four languages: pages, navigation, service pages, forms, buttons, SEO metadata (titles, descriptions, structured data, alt text) and form validation messages.
- Dedicated language URLs with reciprocal `hreflang` tags on every page.
- Elegant language selector in the header.
- Remember the visitor's language preference.
- Professionally written localized content (not word-for-word translation).

**Already in place**
- Translation memory system (`_source/i18n.py` + `tm_<lang>.json`): every English sentence is translated once; edits only need the changed sentences translated. Adding a language = adding its URL map, locale codes and `tm_<lang>.json`.
- Portuguese URLs are localized (e.g. `/pt/construtoras`, `/pt/orcamento`); Spanish and French will follow the same pattern.
- `hreflang` + `x-default` generated automatically; language links in the top bar, mobile menu and footer.
- Per-language search index and accent-aware site search.
- Portuguese form emails tagged `[PT]` so the owner knows which language to reply in.

**Changes needed when implementing**
- English tags: switch `en` → `en-CA` (and Canadian spelling check across English copy).
- Language selector: replace the plain "EN · PT" links with a compact selector (current language + menu), visible on desktop and mobile.
- Language preference: save the visitor's explicit choice (cookie/localStorage, no personal data). On later visits to an English page, offer or apply the saved language. Never auto-redirect search engines or first-time visitors by IP or browser language (Google guidance) — every language stays crawlable at its own URL.
- Form validation messages: replace the browser's default messages with localized messages for all four languages (required fields, email format, file size/type).
- Footer translation note: adjust per language; English remains the reference version.
- Remove the unused `it` and `he` entries from the old language list in `chrome.py`.
- Localized URL slugs for `/es/` and `/fr/`, localized structured data (`inLanguage`, `areaServed`), and per-language sitemaps at launch.
- Professional review: each language reviewed by a native speaker before launch (Brazilian Portuguese, Latin American Spanish, Canadian French).

---

## Pending owner confirmations (collected from earlier tasks)
- Project cities/neighbourhoods, project types, years, services actually performed (Task 004).
- WSIB registration and insurance amount; or remove those mentions (Tasks 001–005).
- Builder FAQ figures: capacity, payment terms, deficiency turnaround (Task 005).
- Crew face permission (Thompson photo held back).
- Final photo selection — all current photos are provisional.
- Form activation: first test submission + click the "Activate" email at cris@ricartidrywall.ca.
- Header/phone-bar button wording ("Get an estimate" vs "Request an Estimate").
- Known SEO bug to fix: the phone menu is picked up as an FAQ question in structured data.

## Future (mentioned, not scheduled)
- Full drawing upload (multiple/large files) and CRM integration for builder leads.
- Content management system for projects and photos (structure ready in `content/projects.json`).
- Professional photography of finished high-end projects.
- Old blog posts migration (needs the WordPress export) and 301 redirects at launch.
- Launch checklist: remove `noindex`, add sitemap, connect domain (only with owner approval).

---

## Service page URLs (Task 007) and WordPress migration plan

| Service | English URL | Portuguese URL |
|---|---|---|
| 01 Drywall Systems | `/drywall-installation-toronto` | `/pt/instalacao-de-drywall-toronto` |
| 02 Insulation & Spray Foam | `/insulation-spray-foam-toronto` | `/pt/isolamento-e-espuma-projetada-toronto` |
| 03 Level 4 & Level 5 Finishing | `/drywall-finishing-toronto` (unchanged) | `/pt/acabamento-de-drywall-toronto` (unchanged) |
| 04 Architectural Finishing | `/architectural-drywall-finishing-toronto` | `/pt/acabamentos-arquitetonicos-toronto` |
| 05 Acoustic & Soundproofing | `/soundproofing-toronto` | `/pt/isolamento-acustico-toronto` |
| 06 Metal Stud Framing | `/metal-stud-framing-toronto` | `/pt/estrutura-em-perfis-de-aco-toronto` |

Spanish (`/es/…`) and French (`/fr/…`) service URLs will use localized slugs in the same pattern.

**Proposed 301 redirects at launch (old WordPress URL → new URL)**
| Old URL (ricartidrywall.ca) | New URL |
|---|---|
| `/services-ricarti-drywall/` | `/#services` (or `/drywall-installation-toronto`) |
| `/about-us/` | `/` (until an About page exists) |
| `/projects/` | `/#projects` |
| `/contact-us/` | `/estimate` |
| `/landing-page/` | `/` |
| 61 old blog posts | matching Journal articles where they exist, otherwise `/journal` — needs the WordPress export to map one by one |

Redirects go in `vercel.json` (`redirects`, permanent) at launch only, with owner approval.

## CRM entry points (prepared in Task 008, not connected)
- `window.RD_CRM = {provider:'gohighlevel', enabled:false}` in assets/site.js. Nothing is sent externally.
- CTAs carry `data-cta` (estimate, builder-inquiry, call, email, whatsapp) and `data-cta-loc` (header, menu, footer, mbar…).
- Clicks push to `window.rdLeadEvents` and dispatch a `rd:lead` CustomEvent; first/last touch, landing page and referrer kept in sessionStorage `rd_lead`.
- The estimate form (#rd-form) adds hidden fields: lead_type (estimate-request | builder-inquiry | drawing-upload), lead_entry, landing_page, referrer.
- To connect later: listen for `rd:lead`, set enabled:true and map the hidden fields to the GoHighLevel form/webhook.

## Languages
- Live: EN-CA (default, x-default), PT-BR (/pt/), ES-419 (/es/), FR-CA (/fr/), IT-IT (/it/). 19 pages per language.
- Pipeline: build English → `i18n.py build <lang>` from tm_<lang>.json (translation memory) → `i18n.py relink` (language switchers, hreflang, sitemap.xml).
- Adding a language: add a URL map in i18n.URLS, HTML_LANG/OG_LOCALE/KINDS/HOME_TITLE, LANG_NAMES, chrome.LANGS, the site.js string tables (search, lightbox, stemming), and a tm_<lang>.json.
- Language preference: stored only when a visitor clicks a language link (localStorage rd_lang). Only the bare English homepage, on a fresh visit from outside the site, sends that visitor to their chosen homepage; ?lang=en always shows English. No location or browser-language redirects.
- Terminology flagged for human review: see the Task 009 report.

## Enquiries and private uploads (Task 010)
- /estimate (and /pt/orcamento, /es/cotizacion, /fr/soumission, /it/preventivo): two paths (homeowner / builder), built by build/est.py + build/estimate.js.
- Delivery: JSON POST to FormSubmit's AJAX endpoint for cris@ricartidrywall.ca (same destination as before). Success is shown only when FormSubmit answers success:true.
  FormSubmit must be activated for this address and domain (first submission sends an activation email to cris@).
- Payload: schema ricarti.enquiry.v1 (customer_type, contact, project, services, preferred_language, lead_source incl. Task 008 first/last touch + UTM,
  consent, attachments[] private references, attachments_not_received[]). Sent as the "CRM payload (JSON)" field and dispatched as rd:lead after success.
- Uploads: api/uploads/config.js + api/uploads/sign.js (Vercel Functions). OFF until the owner:
  1. creates a PRIVATE Vercel Blob store (Storage > Create > Blob > access Private) and connects it to this project (adds BLOB_READ_WRITE_TOKEN);
  2. sets RD_UPLOADS_ENABLED=true (Preview and/or Production) and redeploys;
  3. sends one real test enquiry with a PDF and confirms it under Storage > enquiries/.
  Files go browser -> private store through one 10-minute presigned PUT per file (type and exact size enforced). Never in GitHub, never public.
- GoHighLevel later: send the same payload to an inbound webhook from a server function; attach files by issuing short signed GET URLs or copying into GHL.

## SEO and WordPress migration (Task 011)
- Language home URLs have no trailing slash (/pt, /es, /fr, /it), matching vercel.json trailingSlash:false, so canonicals, hreflang and the sitemap point at final URLs.
- noindex is a build switch: preview builds always carry <meta name="robots" content="noindex, nofollow">; RD_LAUNCH=1 ./make.sh drops it (owner-approved launch only).
  Search pages stay noindex, follow and out of the sitemap. Titles over 65 characters lose the " | Ricarti Drywall" suffix.
- Redirects: build/redirects.py (map + checker; --apply writes vercel.json at launch only). Blog inventory: build/wp_inventory.py export.xml [gsc.csv] > inventory.csv.
- Launch files: _source/robots.launch.txt replaces robots.txt; remove the X-Robots-Tag header block from vercel.json; .vercelignore keeps _source out of deployments.

## Enquiry delivery (Task 010-A): Vercel Function + Microsoft 365
- FormSubmit removed. The form POSTs JSON to /api/enquiry (same origin). The function validates everything again, applies
  honeypot / minimum fill time / link heuristics / per-instance rate limit (5 per 10 min per hashed IP) / per-reference
  duplicate guard, then sends ONE email to cris@ricartidrywall.ca through Microsoft Graph sendMail (no automatic retries).
- Replies: accepted (Graph 202 — accepted by Microsoft, not proof of inbox delivery), failed (definitely not sent),
  uncertain (timeout / 429 / 5xx: may still arrive; visitor keeps the same reference and is asked not to resend).
- Logs: reference, outcome, codes, timing, type, language, region only. No names, emails, phone numbers or text.
- Environment (Vercel, Sensitive): RD_ENQUIRY_ENABLED=true, MS_TENANT_ID, MS_CLIENT_ID, MS_CLIENT_SECRET (or
  MS_CERT_PRIVATE_KEY + MS_CERT_THUMBPRINT), RD_MAIL_SENDER=cris@ricartidrywall.ca, optional RD_MAIL_TO, RD_RATE_SALT.
- Exchange Online: RBAC for Applications, role "Application Mail.Send" scoped to the one mailbox; no Mail.Send consent in Entra.
- CRM prep: api/_lib/crm.js builds ricarti.enquiry.v2 (classification, province/city/postal code, ON/BC routing,
  consent) and GoHighLevel / JobTread shapes. dispatch() does nothing until CRM_PROVIDER is set in Task 012+.


## Task 010-A — Resend integration (2026-11-27)
- /api/enquiry now sends through Resend (server-side RESEND_API_KEY only). From: Ricarti Drywall <estimates@notifications.ricartidrywall.ca>; To: cris@ricartidrywall.ca (RD_MAIL_TO overrides); Reply-To: the customer's validated email.
- Customer acknowledgement in EN/PT/ES/FR/IT after the office copy is accepted; skipped for spam-flagged enquiries; RD_ACK_ENABLED=false turns it off.
- Separate idempotency keys: owner/<ref> and ack/<ref>.
- Enabled automatically when RESEND_API_KEY is present; RD_ENQUIRY_ENABLED=false is the kill switch (needs a redeploy). Microsoft Graph kept, used only if MAIL_PROVIDER=graph.
- Privacy notice on /estimate (all 5 languages) now names Resend (United States) and the confirmation email.
- Still pending (approved architecture): DynamoDB record-before-send with durable retries, Turnstile, Vercel WAF rate-limit rule, owner page with Microsoft sign-in. Uploads stay disabled (Task 010-B).
- NOT complete until the owner confirms a real enquiry arrived in cris@ricartidrywall.ca.
- 2026-11-26: first real enquiry delivered (RD-261126-GXY5A). Office email redesigned (Concept D, inline CID logo, sections, Reply to Customer button, plain-text part); raw CRM JSON removed from the email (record still built internally, not stored). Location status: ontario / ontario-unconfirmed / outside-ontario / requires-verification. Branded acknowledgement in 5 languages.
- 2026-11-26: logo showed broken in Outlook (inline CID image). Header is now an HTML wordmark (no image); RD_EMAIL_LOGO_URL can point to a public PNG later. Phones formatted 647-482-1139. Outlook's 3-hour difference = mailbox time zone set to Pacific (body time is correct Toronto time).

---

## Pre-launch sequence (owner, 2026-11-27)
- 2026-11-28: exclusive priority — move ricartidrywall.ca from the brother's GoDaddy account to the Ricarti Drywall GoDaddy account (DNS records preserved; no nameserver or record changes).
- Then: Task 014 (review original photographs), then Task 016 (after approval).
- Task 010-A stays paused at Infrastructure Verification V1 (AWS Budget alerts). Launch-critical reliability/security items must still be completed before publication.
- Targets: visually complete preview 2026-12-02; launch around 2026-12-10, subject to approval and testing.
- No production changes, DNS changes, merges into main or paid services without explicit owner approval.

## Task 014 — Photography & content (direction approved in principle, 2026-11-27)
- Spec: "Task 014 — Creative Direction & Photography Checklist" (Claude doc), revision 2 + approved decisions.
- Positioning: premium construction contractor; "our craftsmanship helps make those homes beautiful". Audience: custom home builders, architects, general contractors, discerning homeowners.
- Balance: 50% construction process / 30% technical detail / 20% completed architecture.
- Homepage hero: cinematic transition of the same space across construction stages where authentic matching photos exist; otherwise one exceptional authentic construction photo.
- Preview targets: 30–40 authentic photos; 3–5 project galleries; 5–10 photos per project; Frame-to-Finish galleries wherever matching photos exist. Layouts must stay sophisticated with fewer images.
- Never fabricate construction stages or alter photos to represent work not performed; no stock/AI images presented as Ricarti work.
- Concept D, original logo, typography, palette and 5 languages unchanged.
- After launch: full photo library, advanced before/after galleries, professional photography.
- Future operational initiative: Project Documentation Standard (anchor views + stage photos on every job), potentially integrated with JobTread.

## Task 016 — Social media & direct communication (documented 2026-11-27; implement after the domain transfer and owner approval)
- Goal: visitors can reach the official profiles and contact Ricarti Drywall directly.
- Channels:
  - WhatsApp Business — click-to-chat (wa.me) with pre-filled message. EN source: "Hello Ricarti Drywall! I would like to discuss an upcoming project." Translated per page language (PT/ES/FR/IT), brand name unchanged.
  - Instagram — official business profile.
  - Facebook — official business page.
  - LinkedIn — official company page.
- Placement: footer, contact section/estimate page, mobile navigation; plus a discreet floating WhatsApp button (desktop + mobile; must not cover the cookie notice, form buttons or the mobile call bar; hidden while the estimate form is focused on small screens).
- Design: elegant monochrome icons (inline SVG, no third-party scripts or icon fonts) in Concept D charcoal/bronze; bronze on hover/focus; 44×44 px minimum touch targets.
- Accessibility: accessible names per language (e.g. "Ricarti Drywall on Instagram (opens in a new tab)"), visible focus states, decorative SVGs aria-hidden, rel="noopener noreferrer".
- Single source of truth: one central config (e.g. `_source/content/social.json`) read by chrome.py and every page template; also feeds Organization `sameAs` structured data.
- Verified URLs only — owner must confirm each before publishing. Currently in the site (unverified): Instagram https://www.instagram.com/ricarti_drywall/, Facebook https://www.facebook.com/ricartidrywall, WhatsApp +1 647-482-1139 (confirm it is the WhatsApp Business number). LinkedIn: URL needed.
- Analytics: keep existing data-cta attributes (whatsapp, instagram, facebook, linkedin) for click tracking; no personal data.
- Out of scope now: GoHighLevel, paid APIs (WhatsApp Cloud API), chat widgets, AI automation, automated replies. CRM integration and centralized communications come in a later phase (Task 012+).
- Acceptance: links verified on desktop/iOS/Android in all 5 languages; WhatsApp opens the app (mobile) or WhatsApp Web (desktop) with the pre-filled message; no layout shift; Lighthouse accessibility unchanged or better.
