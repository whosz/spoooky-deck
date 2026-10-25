"""python3 tools/build_sw.py: generates sw.js with the list of files to cache (without music) and a version taken from a content hash."""
import os, json, hashlib
ROOT = ['index.html', 'manifest.webmanifest']
DIRS = ['css', 'js', 'data', 'fonts', 'img']
files = [f for f in ROOT if os.path.exists(f)]
for d in DIRS:
    for base, _, names in os.walk(d):
        files += [os.path.join(base, n).replace(os.sep, '/') for n in sorted(names) if not n.endswith(('LICENSE', '.md'))]
files = sorted(set(files))
h = hashlib.sha1()
for f in files: h.update(f.encode()); h.update(open(f, 'rb').read())
src = open('tools/sw.template.js', encoding='utf8').read().replace('__VERSION__', h.hexdigest()[:10]).replace('__FILES__', json.dumps(['./'] + files))
open('sw.js', 'w', encoding='utf8').write(src)
print('sw.js', h.hexdigest()[:10], len(files), 'files')
