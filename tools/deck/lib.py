"""Biblioteka pixel art dla talii 144x216: paleta, dither Bayera 4x4, kształty, symbole kolorów, sylwetki.
Używa tools/pixel.py (Canvas). Każda karta to funkcja draw(c) rysująca na Canvas(144, 216)."""
import sys, math, random
sys.path.insert(0, 'tools')
from pixel import Canvas, rgb

W, H = 144, 216
# Wspólna paleta (nazwane odcienie, ciemne -> jasne w obrębie rodziny)
P = {k: rgb(v) for k, v in dict(
    ink='#07080f', n1='#0b0d17', n2='#131a33', n3='#1c2750', n4='#2b3a73',
    v1='#2a1740', v2='#46245f', v3='#6b3a85',
    r1='#3a0d16', r2='#7a1c2c', r3='#b3243a', r4='#e0506a',
    o1='#7a3410', o2='#c25a1a', o3='#ff8a2b', o4='#ffb347', o5='#ffe08a',
    g1='#4a3512', g2='#8a6a2e', g3='#d8aa48', g4='#f0d27a',
    cream='#e8dcc0', white='#f4efe6',
    e1='#12241b', e2='#1f4a35', e3='#2f7a52', e4='#5fa86a',
    t1='#0f3a44', t2='#1f6b7a', t3='#3fd0c9', t4='#a8f0e8',
    s1='#2a3550', s2='#506690', s3='#7fa8d8', s4='#c0d8f0',
    k1='#c89a76', k2='#e8c2a0', b1='#3a2616', b2='#6b4426', b3='#a06a3a',
    y1='#3a3d4a', y2='#6a6f80', y3='#a0a6b8').items()}

BAYER = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]
def thr(x, y): return (BAYER[y % 4][x % 4] + .5) / 16

def blend(c, x, y, col, t):
    """Wstawia col z prawdopodobieństwem t (dither Bayera)."""
    if t > thr(x, y): c.set(x, y, col)

def ramp(c, x0, y0, x1, y1, names):
    """Pionowy gradient przez kolejne kolory palety z ditheringiem między sąsiadami."""
    n = len(names) - 1
    for y in range(y0, y1):
        f = (y - y0) / max(1, y1 - y0 - 1) * n; i = min(int(f), n - 1); t = f - i
        for x in range(x0, x1): c.set(x, y, P[names[i + 1]] if t > thr(x, y) else P[names[i]])

def glow(c, cx, cy, r, name, power=1.6):
    """Okrągła poświata: gęstość maleje od środka (dither)."""
    for y in range(int(cy - r), int(cy + r) + 1):
        for x in range(int(cx - r), int(cx + r) + 1):
            d = math.hypot(x - cx, y - cy) / r
            if d < 1: blend(c, x, y, P[name], (1 - d) ** power)

def vignette(c, name='ink', strength=.55):
    for y in range(H):
        for x in range(W):
            d = max(abs(x - W / 2) / (W / 2), abs(y - H / 2) / (H / 2))
            if d > .8: blend(c, x, y, P[name], min(1, (d - .8) / .2 * strength * 1.4))

def poly(c, pts, name):
    """Wypełniony wielokąt (scanline)."""
    col = P[name] if isinstance(name, str) else name
    ys = [p[1] for p in pts]
    for y in range(int(min(ys)), int(max(ys)) + 1):
        xs = []
        for i in range(len(pts)):
            (x0, y0), (x1, y1) = pts[i], pts[(i + 1) % len(pts)]
            if (y0 <= y < y1) or (y1 <= y < y0): xs.append(x0 + (y - y0) * (x1 - x0) / (y1 - y0))
        xs.sort()
        for a, b in zip(xs[::2], xs[1::2]):
            for x in range(round(a), round(b) + 1): c.set(x, y, col)

def disc(c, cx, cy, r, name): c.ellipse(cx, cy, r, r, P[name], True)
def rect(c, x, y, w, h, name): c.rect(round(x), round(y), round(w), round(h), P[name])
def line(c, x0, y0, x1, y1, name, t=1):
    for k in range(t):
        c.line(round(x0) + k, round(y0), round(x1) + k, round(y1), P[name])

def stars(c, y0, y1, n, seed=1, names=('cream', 'o5', 's4')):
    r = random.Random(seed)
    for _ in range(n):
        x, y = r.randrange(W), r.randrange(y0, y1); col = P[r.choice(names)]
        c.set(x, y, col)
        if r.random() < .15: [c.set(x + dx, y + dy, col) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))]

def hills(c, y, amp, name, seed=1, rough=.07, x0=0, x1=W):
    r = random.Random(seed); ph = [r.random() * 6.28 for _ in range(3)]
    for x in range(x0, x1):
        h = y + amp * (math.sin(x * rough + ph[0]) + .5 * math.sin(x * rough * 2.3 + ph[1]) + .25 * math.sin(x * rough * 5 + ph[2]))
        for yy in range(round(h), H): c.set(x, yy, P[name])

def mountains(c, y, amp, name, seed=1, n=5):
    r = random.Random(seed); xs = sorted(r.sample(range(-10, W + 10), n))
    for x in range(W):
        h = H
        for px in xs:
            h = min(h, y - max(0, amp * random.Random(px + seed).uniform(.6, 1) - abs(x - px) * 1.1))
        for yy in range(round(h), H): c.set(x, yy, P[name])

def clouds(c, y0, y1, names, seed=1, n=7):
    r = random.Random(seed)
    for _ in range(n):
        cx, cy, rx, ry = r.randrange(W), r.randrange(y0, y1), r.randrange(18, 40), r.randrange(5, 10)
        for k, nm in enumerate(names): c.ellipse(cx, cy - k * 2, rx - k * 3, ry - k, P[nm], True)

# ---- symbole kolorów (środek cx, cy; s = skala 1.0 ~ 28 px wysokości) ----
def pentacle(c, cx, cy, s=1.0, hi='g4', mid='g3', lo='g2'):
    r = 11 * s; glow(c, cx, cy, r * 1.9, 'g1', 1.8)
    disc(c, cx, cy, r + 1, 'ink'); disc(c, cx, cy, r, lo); disc(c, cx, cy, r - 2, mid); disc(c, cx, cy, r - 4, lo)
    pts = [(cx + (r - 3) * math.sin(i * 4 * math.pi / 5), cy - (r - 3) * math.cos(i * 4 * math.pi / 5)) for i in range(6)]
    for a, b in zip(pts, pts[1:]): line(c, a[0], a[1], b[0], b[1], hi)
    c.set(round(cx - r * .45), round(cy - r * .5), P['white'])

def cup(c, cx, cy, s=1.0, body='t2', hi='t4', rim='g3'):
    h = 13 * s; w = 9 * s
    glow(c, cx, cy - h * .3, h * 1.6, 't1', 1.8)
    poly(c, [(cx - w, cy - h), (cx + w, cy - h), (cx + w * .8, cy), (cx + w * .3, cy + h * .35), (cx - w * .3, cy + h * .35), (cx - w * .8, cy)], 'ink')
    poly(c, [(cx - w + 1, cy - h + 1), (cx + w - 1, cy - h + 1), (cx + w * .8 - 1, cy), (cx + w * .3, cy + h * .3), (cx - w * .3, cy + h * .3), (cx - w * .8 + 1, cy)], body)
    rect(c, cx - w, cy - h, 2 * w + 1, 2, rim); rect(c, cx - w * .6, cy - h * .7, 2, h * .8, hi)
    rect(c, cx - 1, cy + h * .35, 3, h * .5, 'g2'); rect(c, cx - w * .5, cy + h * .85, w + 1, 2, 'g3')

def sword(c, cx, cy, s=1.0, blade='s4', edge='s2', up=True):
    h = 24 * s; d = -1 if up else 1
    glow(c, cx, cy, h * .9, 's1', 1.8)
    poly(c, [(cx - 2, cy + d * -h * .2), (cx + 2, cy + d * -h * .2), (cx + 1, cy + d * h), (cx - 1, cy + d * h)], 'ink') if False else None
    top, bot = (cy - h, cy + h * .35) if up else (cy + h, cy - h * .35)
    poly(c, [(cx - 3, bot), (cx + 3, bot), (cx + 1, top + (3 if up else -3)), (cx, top), (cx - 1, top + (3 if up else -3))], 'ink')
    poly(c, [(cx - 2, bot), (cx + 2, bot), (cx + 1, top + (4 if up else -4)), (cx, top + (1 if up else -1)), (cx - 1, top + (4 if up else -4))], blade)
    rect(c, cx - 1, min(top, bot) + 3, 1, abs(bot - top) - 5, edge)
    rect(c, cx - 7 * s, bot, 14 * s + 1, 3, 'g3'); rect(c, cx - 7 * s, bot, 14 * s + 1, 1, 'g4')
    rect(c, cx - 1, bot + (3 if up else -7), 3, 7, 'b2'); disc(c, cx, bot + (11 if up else -9), 2, 'g3')

def wand(c, cx, cy, s=1.0, wood='b3', leaf='e4'):
    h = 26 * s
    glow(c, cx, cy, h, 'o1', 1.8)
    for k in range(-2, 4): line(c, cx - 5 * s + k, cy + h, cx + 5 * s + k, cy - h, 'ink')
    line(c, cx - 5 * s, cy + h, cx + 5 * s, cy - h, wood, 3); line(c, cx - 5 * s + 2, cy + h, cx + 5 * s + 2, cy - h, 'b2')
    for fy, fx, dx in ((.5, .1, -1), (.1, .6, 1), (-.3, .8, -1), (-.7, 1, 1)):
        x, y = cx + (fx - .5) * 10 * s, cy - fy * h
        c.ellipse(x + dx * 4, y, 3.2, 1.8, P[leaf], True); c.ellipse(x + dx * 4, y, 1.5, .8, P['e2'], True)
    c.set(round(cx + 5 * s), round(cy - h) - 1, P['o4'])

SYMBOL = dict(pentacles=pentacle, cups=cup, swords=sword, wands=wand)

# ---- sylwetki ----
def figure(c, cx, base, h=60, robe='v2', trim='v3', hood=True, face='ink', arms='down', skin='k1', sym=None, hs=1.0):
    """Zakapturzona sylwetka. cx = środek, base = linia stóp, h = wysokość. arms: down/up/out."""
    w = h * .34; top = base - h
    poly(c, [(cx - w * .45, top + h * .24), (cx + w * .45, top + h * .24), (cx + w, base), (cx - w, base)], 'ink')   # kontur
    poly(c, [(cx - w * .4, top + h * .26), (cx + w * .4, top + h * .26), (cx + w * .9, base - 1), (cx - w * .9, base - 1)], robe)
    rect(c, cx - w * .9, base - 3, w * 1.8, 2, trim)                      # lamówka
    poly(c, [(cx - 1, top + h * .3), (cx + 1, top + h * .3), (cx + w * .2, base - 2), (cx - w * .2, base - 2)], trim)
    r = h * .13
    disc(c, cx, top + r + 1, r + 1, 'ink'); disc(c, cx, top + r + 1, r, robe if hood else skin)
    if hood: c.ellipse(cx, top + r + 2, r * .65, r * .8, P[face], True); c.set(round(cx - r * .3), round(top + r + 2), P['o4']); c.set(round(cx + r * .3), round(top + r + 2), P['o4'])
    else:
        c.ellipse(cx, top + r + 2, r * .7, r * .8, P[skin], True)
        c.set(round(cx - r * .3), round(top + r + 1), P['ink']); c.set(round(cx + r * .3), round(top + r + 1), P['ink']); c.rect(round(cx - 1), round(top + r + 4), 2, 1, P['r3'])
    sh = top + h * .3
    if arms == 'up':
        line(c, cx - w * .4, sh, cx - w * 1.1, sh - h * .3, robe, 3); line(c, cx + w * .4, sh, cx + w * 1.1, sh - h * .3, robe, 3)
    elif arms == 'out':
        line(c, cx - w * .4, sh, cx - w * 1.3, sh + h * .12, robe, 3); line(c, cx + w * .4, sh, cx + w * 1.3, sh + h * .12, robe, 3)
    else:
        line(c, cx - w * .45, sh, cx - w * .5, sh + h * .28, robe, 3); line(c, cx + w * .45, sh, cx + w * .5, sh + h * .28, robe, 3)
    return dict(hand_l=(cx - w * (1.1 if arms == 'up' else 1.3 if arms == 'out' else .5), sh - h * (.3 if arms == 'up' else -.12 if arms == 'out' else -.28)),
                hand_r=(cx + w * (1.1 if arms == 'up' else 1.3 if arms == 'out' else .5), sh - h * (.3 if arms == 'up' else -.12 if arms == 'out' else -.28)), head=(cx, top + r))

def crown(c, cx, cy, w=10, pts=3, name='g3'):
    rect(c, cx - w / 2, cy, w, 3, name)
    for i in range(pts):
        x = cx - w / 2 + (i + .5) * w / pts; poly(c, [(x - w / pts / 2, cy), (x + w / pts / 2, cy), (x, cy - 5)], name)
        c.set(round(x), round(cy - 5), P['white'])

def raven(c, x, y, s=1.0, wings='up'):
    poly(c, [(x, y), (x + 5 * s, y - 2 * s), (x + 9 * s, y), (x + 5 * s, y + 2 * s)], 'ink')
    poly(c, [(x + 3 * s, y - 1), (x + 5 * s, y - (7 if wings == 'up' else -6) * s), (x + 7 * s, y - 1)], 'ink'); c.set(round(x + 8 * s), round(y - 1), P['o4'])

def tower(c, x, y, w, h, wall='y2', roof='r2', lit=True):
    rect(c, x, y, w, h, 'ink'); rect(c, x + 1, y + 1, w - 2, h - 2, wall); rect(c, x + 1, y + 1, 2, h - 2, 'y3')
    poly(c, [(x - 2, y), (x + w + 2, y), (x + w / 2, y - w * .8)], 'ink'); poly(c, [(x, y - 1), (x + w, y - 1), (x + w / 2, y - w * .75)], roof)
    for k in range(3):
        wy = y + 6 + k * (h // 4)
        rect(c, x + w / 2 - 2, wy, 4, 6, 'ink'); lit and rect(c, x + w / 2 - 1, wy + 1, 2, 4, 'o4')

def finish(c, accent=None, vig=.5):
    vignette(c, 'ink', vig)
    return c

def card(): return Canvas(W, H, P['n1'])
