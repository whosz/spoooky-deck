"""python3 tools/bump_version.py: bumps the ?v=N version in index.html (css, js) and in the module imports in js/app.js.
The number in the URL means that after an update the browser never mixes the new app.js with old cached modules. Run it before deploying."""
import re, sys
html = open('index.html').read()
n = int(re.search(r'app\.js\?v=(\d+)', html).group(1)) + 1
html = re.sub(r'(\.(?:css|js))\?v=\d+', rf'\1?v={n}', html)
app = re.sub(r"(from '\./\w+\.js)\?v=\d+'", rf"\1?v={n}'", open('js/app.js').read())
open('index.html', 'w').write(html); open('js/app.js', 'w').write(app)
print('wersja', n)
