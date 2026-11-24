import sys; sys.path.insert(0,'/home/claude/build')
import build
build.SRC='/home/claude/build/'
build.convert('Estimate.static.dc.html','/estimate','Get an estimate or book a site visit | Ricarti Drywall','Send photos or drawings for a ballpark, or book a site visit for a written price. Homeowners and builders across the GTA, Hamilton, Kitchener-Cambridge and Muskoka.')
p='/home/claude/ricarti-drywall-website/estimate/index.html'
s=open(p).read()
js=open('/home/claude/build/estimate.js').read()
s=s.replace('</body>','<script>\n'+js+'\n</script>\n</body>',1)
open(p,'w').write(s)
b='/home/claude/ricarti-drywall-website/builders/index.html'
t=open(b).read(); n=t.count('href="/estimate"'); t=t.replace('href="/estimate"','href="/estimate?type=builder"'); open(b,'w').write(t); print('builder links',n)
