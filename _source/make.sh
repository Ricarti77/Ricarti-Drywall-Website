#!/bin/sh
# Rebuild the whole site: English pages, then translations, then language links.
set -e
cd /home/claude/ricarti-drywall-website
python3 /home/claude/build/build.py > /dev/null
python3 /home/claude/build/est.py > /dev/null
python3 /home/claude/build/pages.py > /tmp/pages.log; tail -1 /tmp/pages.log
for l in pt es fr it; do python3 /home/claude/build/i18n.py build $l; done
python3 /home/claude/build/i18n.py relink
