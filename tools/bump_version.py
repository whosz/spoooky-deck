"""python3 tools/bump_version.py: podnosi numer wersji ?v=N w index.html (css, js) i w importach modułów w js/app.js.
Numer w adresie sprawia, że po aktualizacji przeglądarka nigdy nie miesza nowego app.js ze starymi modułami z cache. Uruchom przed deployem."""
import re, sys
html = open('index.html').read()
n = int(re.search(r'app\.js\?v=(\d+)', html).group(1)) + 1
html = re.sub(r'(\.(?:css|js))\?v=\d+', rf'\1?v={n}', html)
app = re.sub(r"(from '\./\w+\.js)\?v=\d+'", rf"\1?v={n}'", open('js/app.js').read())
open('index.html', 'w').write(html); open('js/app.js', 'w').write(app)
print('wersja', n)
