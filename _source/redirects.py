"""301 redirect map: old WordPress site (ricartidrywall.ca) -> new site.

    python3 redirects.py            check every destination exists in the built site, print the table
    python3 redirects.py --apply    LAUNCH ONLY, with owner approval: write the confirmed rules into vercel.json

Rules marked 'pending' are proposals and are never written to vercel.json. The 61 blog posts are added from the
WordPress export with wp_inventory.py (it prints rows in this format) after the owner reviews the classification.
Each old path is listed with and without the trailing slash, so a visitor reaches the new page in one hop.
"""
import json, os, sys

ROOT = '/home/claude/ricarti-drywall-website/'

# (old path, new path, status, note)  status: confirmed | pending
RULES = [
    # pages found on the live site
    ('/about-us', '/#about', 'confirmed', 'About page -> About section on the new home page'),
    ('/services-ricarti-drywall', '/#services', 'confirmed', 'Services overview -> Services section'),
    ('/projects', '/#projects', 'confirmed', 'Projects page -> Selected projects'),
    ('/contact-us', '/estimate', 'confirmed', 'Contact -> estimate and contact page'),
    ('/landing-page', '/', 'confirmed', 'Old landing page'),
    # blog posts found so far (the rest need the WordPress export)
    ('/how-to-reduce-room-echo', '/journal/soundproofing-a-room', 'pending', 'Consolidate: same topic (echo vs noise transfer); owner to confirm'),
    ('/spray-foam-reviews-what-actually-matters', '/insulation-spray-foam-toronto', 'pending', 'Owner review: migrate as a Journal article or redirect to the spray foam service page'),
    # WordPress archives and machine URLs
    ('/category/:slug*', '/journal', 'confirmed', 'Category archives'),
    ('/tag/:slug*', '/journal', 'confirmed', 'Tag archives'),
    ('/author/:slug*', '/', 'confirmed', 'Author archives'),
    ('/blog', '/journal', 'pending', 'Only if the old site used /blog as its posts page'),
    ('/feed', '/journal', 'confirmed', 'RSS feed'),
    ('/sitemap_index.xml', '/sitemap.xml', 'confirmed', 'Yoast sitemap index'),
    ('/wp-sitemap.xml', '/sitemap.xml', 'confirmed', 'WordPress core sitemap'),
    ('/post-sitemap.xml', '/sitemap.xml', 'confirmed', 'Yoast post sitemap'),
    ('/page-sitemap.xml', '/sitemap.xml', 'confirmed', 'Yoast page sitemap'),
]

def exists(dest):
    p = dest.split('#')[0].split('?')[0].strip('/')
    return p == '' or os.path.exists(ROOT + p + '/index.html') or os.path.exists(ROOT + p)

def expand(rules, only_confirmed=True):
    out = []
    for src, dst, status, _ in rules:
        if only_confirmed and status != 'confirmed':
            continue
        srcs = [src] if ':' in src or src.endswith('.xml') else [src, src + '/']
        for s in srcs:
            out.append({'source': s, 'destination': dst, 'permanent': True})
    return out

if __name__ == '__main__':
    bad = [(s, d) for s, d, _, _ in RULES if not exists(d)]
    for s, d, st, n in RULES:
        print('%-48s -> %-34s %-9s %s' % (s, d, st, n))
    print('destinations missing:', bad or 'none')
    if '--apply' in sys.argv:
        if bad: sys.exit('refusing: missing destinations')
        vj = json.load(open(ROOT + 'vercel.json'))
        vj['redirects'] = expand(RULES)
        json.dump(vj, open(ROOT + 'vercel.json', 'w'), indent=2)
        print('vercel.json: %d redirect rules written' % len(vj['redirects']))
