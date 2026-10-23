"""python3 tools/deck/build.py [id ...]: renderuje karty do img/cards/<id>.png i sprawdza rozmiar oraz liczbę kolorów.
Małe Arkana z minors.py, Wielkie z majors_*.py (słownik CARDS). Dodatkowo arkusze przeglądowe tools/deck/_sheet_*.png."""
import sys, glob, importlib
sys.path.insert(0, 'tools/deck'); sys.path.insert(0, 'tools')
from lib import W, H
import minors
from sheet import sheet

draws = {i: (lambda i=i: minors.render(i)) for i in minors.IDS}
for f in sorted(glob.glob('tools/deck/majors_*.py')):
    draws.update(importlib.import_module(f.split('/')[-1][:-3]).CARDS)
ids = sys.argv[1:] or sorted(draws)
done, bad = [], []
for i in ids:
    c = draws[i]()
    colors = {tuple(p) for row in c.px for p in row}
    if (c.w, c.h) != (W, H) or len(colors) > 90: bad.append((i, c.w, c.h, len(colors)))
    c.save(f'img/cards/{i}.png'); done.append(c)
print('rendered', len(done), 'problems', bad)
if not sys.argv[1:]:
    for n, (a, b) in enumerate([(0, 22), (22, 36), (36, 50), (50, 64), (64, 78)]):
        sheet(done[a:b], f'tools/deck/_sheet_{n}.png', cols=7)
