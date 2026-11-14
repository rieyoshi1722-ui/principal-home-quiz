"""Build the standalone site (index.html + only the assets it uses) from builder.html.

usage: python3 tools/build_site.py <output folder>
The result works from any folder or URL path: every file is referenced relatively.
"""
import os, re, shutil, sys

out = sys.argv[1]
body = open('builder.html', encoding='utf-8').read()

head = '''<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="robots" content="noindex">
<style>
/* base reset */
:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}
body{margin:0}
img{max-width:100%}
[hidden]{display:none!important}
</style>
'''
body = body.replace('<meta charset="utf-8">\n', '', 1)
body = re.sub(r'<meta name="claude:viewport-fit-sides"[^>]*>\n', '', body)
i = body.index('</style>') + len('</style>')
html = head + body[:i] + '\n</head>\n<body>\n' + body[i:] + '\n</body>\n</html>\n'

# which asset files does the page use? literal names, plus the ones it builds from a pattern
names = set(re.findall(r'[A-Za-z0-9_\-]+\.(?:png|jpg|webp|mp3)', html))
names |= {'quiz_%d.png' % n for n in range(1, 6)}
names |= {n + '.png' for n in re.findall(r'label:"(plank_[a-z]+)"', html)}
used = []
for root, _, files in os.walk('assets'):
    for f in files:
        if f in names:
            used.append(os.path.join(root, f))

if os.path.exists(out): shutil.rmtree(out)
os.makedirs(out)
open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(html)
for f in used:
    dst = os.path.join(out, f); os.makedirs(os.path.dirname(dst), exist_ok=True); shutil.copy(f, dst)
total = sum(os.path.getsize(os.path.join(out, f)) for f in used) + len(html.encode())
print('built %s: %d asset files, %.1f MB' % (out, len(used), total / 1048576))
