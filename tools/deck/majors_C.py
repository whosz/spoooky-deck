"""Wielkie Arkana 12-17: Wisielec, Smierc, Umiarkowanie, Diabel, Wieza, Gwiazda."""
import sys; sys.path.insert(0, 'tools/deck'); sys.path.insert(0, 'tools')
from lib import *

def star(c, cx, cy, r, name, pts=8, inner=.32, core='white'):
    v = []
    for i in range(pts * 2):
        a = i * math.pi / pts - math.pi / 2; rr = r if i % 2 == 0 else r * inner
        v.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    poly(c, v, name); disc(c, cx, cy, max(1, r * .18), core)

def ground(c, y, names, seed):
    hills(c, y, 5, names[0], seed, .06); ramp(c, 0, y + 12, W, H, [names[0], names[1], 'ink'])

def stream(c, a, b, sag, name, n=26):
    for i in range(n + 1):
        t = i / n; x = a[0] + (b[0] - a[0]) * t; y = a[1] + (b[1] - a[1]) * t + sag * 4 * t * (1 - t)
        c.set(round(x), round(y), P[name]); i % 2 or c.set(round(x), round(y) + 1, P['g3'])

def _layer_person(**kw):
    t = Canvas(W, H); f = person(t, **kw); return t, f

def paste_xf(c, t, fn):
    """Wkleja warstwe t po przeksztalceniu fn(x,y)->(sx,sy) (mapowanie wsteczne)."""
    o = Canvas(W, H)
    for y in range(H):
        for x in range(W):
            sx, sy = fn(x, y)
            if 0 <= sx < W and 0 <= sy < H and t.px[sy][sx][3]: o.px[y][x] = t.px[sy][sx]
    c.paste(o, 0, 0)

# ---------------------------------------------------------------- 12
def ar12():
    c = card(); ramp(c, 0, 0, W, 190, ['n1', 'n2', 'n3', 'v1']); stars(c, 5, 60, 24, 12)
    glow(c, 72, 112, 48, 'g2', 1.7)
    ground(c, 172, ['e1', 'ink'], 4)
    for x in (24, 112): rect(c, x - 3, 40, 7, 134, 'ink'); rect(c, x - 2, 40, 2, 134, 'b2')
    rect(c, 20, 38, 104, 8, 'ink'); rect(c, 21, 39, 102, 5, 'b2'); rect(c, 21, 39, 102, 1, 'b3')
    for x, y in ((34, 48), (50, 47), (96, 48), (108, 47)): c.ellipse(x, y, 4, 2, P['e2'], True); c.set(x, y, P['e3'])
    line(c, 72, 46, 72, 68, 'cream')
    t, f = _layer_person(cx=72, base=147, h=92, robe='r3', trim='g3', hair='b2', lh=(-8, -16), rh=(8, -16))
    paste_xf(c, t, lambda x, y: (x, H - 1 - y))
    hx, hy = f['head']; hy = H - 1 - hy
    rect(c, 70, 66, 5, 3, 'cream'); rect(c, 63, 69, 7, 3, 'ink'); rect(c, 75, 69, 7, 3, 'ink'); rect(c, 64, 69, 5, 2, 'b2'); rect(c, 76, 69, 5, 2, 'b2')
    for r in (13, 14): c.ellipse(hx, hy, r, r, P['g3'], False)   # aureola
    return finish(c)

# ---------------------------------------------------------------- 13
def ar13():
    c = card(); ramp(c, 0, 0, W, 150, ['ink', 'n2', 'v1', 'r1']); stars(c, 5, 70, 16, 13)
    glow(c, 72, 128, 62, 'o2', 2); disc(c, 72, 126, 22, 'o3'); disc(c, 72, 126, 18, 'o4'); disc(c, 72, 126, 12, 'o5')
    hills(c, 150, 6, 'n2', 3, .08); ground(c, 162, ['e1', 'ink'], 7)
    # kosa
    # kruk
    raven(c, 100, 62, 1.2, 'up')
    f = person(c, 72, 182, 122, robe='v2', trim='g3', hood=True, eyes='o5', lh=(34, 38), rh=(-2, 12))
    line(c, 90, 40, 90, 182, 'ink', 3); line(c, 91, 40, 91, 182, 'b2')
    poly(c, [(90, 38), (66, 36), (48, 48), (70, 45), (90, 47)], 'ink'); poly(c, [(89, 40), (68, 39), (56, 46), (70, 43), (89, 44)], 's4')
    for k in ('hand_l', 'hand_r'): c.ellipse(f[k][0], f[k][1], 2.2, 2.2, P['k2'], True)
    for x in range(10, 134, 9): c.set(x, 172 + x % 5, P['white']); c.set(x, 171 + x % 5, P['y2'])
    return finish(c)

# ---------------------------------------------------------------- 14
def ar14():
    c = card(); ramp(c, 0, 0, W, 150, ['n1', 'n3', 'v1', 'v2']); stars(c, 5, 50, 20, 14)
    mountains(c, 138, 40, 'n2', 5, 4); glow(c, 72, 130, 34, 'g3', 2)
    for x, y in ((100, 126), (108, 122)): c.set(x, y, P['g4'])
    hills(c, 150, 4, 'e1', 2, .07); ramp(c, 0, 158, W, H, ['e1', 'e1', 'ink'])
    c.ellipse(72, 178, 46, 10, P['t1'], True); c.ellipse(72, 178, 36, 7, P['t2'], True)
    for x in range(40, 105, 3): blend(c, x, 176 + x % 3, P['t4'], .7)
    # skrzydla
    for s in (-1, 1):
        poly(c, [(72 + s * 8, 66), (72 + s * 44, 38), (72 + s * 40, 70), (72 + s * 30, 100), (72 + s * 10, 110)], 'ink')
        poly(c, [(72 + s * 9, 68), (72 + s * 40, 43), (72 + s * 36, 70), (72 + s * 28, 96), (72 + s * 10, 106)], 's2')
        for k in range(4): line(c, 72 + s * 12, 72 + k * 8, 72 + s * (36 - k * 3), 56 + k * 12, 's4')
    glow(c, 72, 52, 26, 'g3', 1.8)
    f = person(c, 72, 172, 112, robe='s4', trim='g3', hair='y3', lh=(-14, 30), rh=(14, 14))
    hx, hy = f['head']
    for r in (9, 10): c.ellipse(hx, hy, r, r, P['g4'], False)
    star(c, 72, hy + 20, 4, 'g3', 4, .35, 'white')
    (lx, ly), (rx, ry) = f['hand_l'], f['hand_r']
    cup(c, round(lx) - 1, round(ly) - 6, .55); cup(c, round(rx) + 1, round(ry) + 8, .55)
    stream(c, (lx, ly - 12), (rx, ry + 2), -16, 'o5', 40)
    return finish(c)

# ---------------------------------------------------------------- 15
def ar15():
    c = card(); ramp(c, 0, 0, W, H, ['ink', 'r1', 'r1', 'ink']); glow(c, 72, 72, 56, 'r2', 1.6)
    for s in (-1, 1):   # skrzydla
        poly(c, [(72 + s * 12, 62), (72 + s * 64, 30), (72 + s * 52, 62), (72 + s * 60, 92), (72 + s * 40, 84), (72 + s * 30, 104), (72 + s * 14, 92)], 'ink')
        line(c, 72 + s * 14, 64, 72 + s * 62, 32, 'r2'); line(c, 72 + s * 16, 72, 72 + s * 54, 62, 'r2'); line(c, 72 + s * 16, 80, 72 + s * 58, 90, 'r2')
    rect(c, 46, 150, 52, 36, 'ink'); rect(c, 48, 152, 48, 32, 'n2'); rect(c, 48, 152, 48, 2, 'y1'); rect(c, 46, 150, 52, 1, 'r3')
    f = person(c, 72, 150, 108, robe='n3', trim='r2', skin='r2', eyes='o5', lh=(-12, 24), rh=(16, -22), belt=True)
    hx, hy = f['head']
    for s in (-1, 1):
        poly(c, [(hx + s * 5, hy - 5), (hx + s * 8, hy - 8), (hx + s * 13, hy - 22), (hx + s * 3, hy - 9)], 'ink'); poly(c, [(hx + s * 5, hy - 6), (hx + s * 8, hy - 9), (hx + s * 11, hy - 19), (hx + s * 5, hy - 9)], 'y2')
    star(c, 72, 116, 3, 'r3', 5, .4, 'r4')
    lx, ly = f['hand_l']; line(c, lx, ly + 10, lx, ly - 2, 'b2'); poly(c, [(lx - 2, ly - 2), (lx + 2, ly - 2), (lx, ly - 8)], 'o4'); c.set(lx, ly - 4, P['o5'])
    for s in (-1, 1):   # lancuchy i malutkie postacie
        px = 72 + s * 46; hx, hy = 72 + s * 24, 160
        for i in range(11):
            t = i / 10; c.set(round(hx + (px - hx) * t), round(hy + 6 * t + 3 * math.sin(t * 3.14)), P['y3'])
        g = person(c, px, 186, 36, robe='v2', trim='r3', skin='k2', hair='b1', belt=False)
        line(c, px, g['head'][1] + 5, hx, hy + 6, 'y2')
    ramp(c, 0, 176, W, H, ['r1', 'ink', 'ink'])
    return finish(c)

# ---------------------------------------------------------------- 16
def ar16():
    c = card(); ramp(c, 0, 0, W, 190, ['ink', 'n2', 'v1', 'n3']); clouds(c, 28, 80, ['n1', 'n2'], 16, 9)
    glow(c, 72, 60, 54, 'o2', 2.2)
    mountains(c, 168, 14, 'n2', 6, 3); poly(c, [(36, 190), (48, 160), (96, 160), (110, 190)], 'ink'); ramp(c, 0, 176, W, H, ['ink', 'ink'])
    tower(c, 54, 72, 36, 88, 'y1', 'ink', lit=False); rect(c, 52, 72, 40, 4, 'y2'); rect(c, 52, 72, 40, 1, 'y3')
    for k in range(3): rect(c, 66, 84 + k * 22, 12, 12, 'ink'); rect(c, 67, 86 + k * 22, 10, 9, 'o3'); rect(c, 69, 86 + k * 22, 6, 5, 'o5')
    glow(c, 72, 78, 24, 'o3', 1.2)
    poly(c, [(54, 74), (90, 74), (84, 56), (78, 62), (72, 42), (66, 60), (60, 54)], 'o2'); poly(c, [(60, 74), (84, 74), (78, 62), (72, 52), (66, 64)], 'o4'); poly(c, [(66, 74), (78, 74), (72, 62)], 'o5')
    poly(c, [(88, 70), (108, 62), (98, 52)], 'ink') if False else None
    crown(c, 100, 30, 12, 3, 'g3'); rect(c, 100, 33, 12, 1, 'g2'); c.set(96, 40, P['o5']); c.set(112, 38, P['o5']); c.set(104, 22, P['y3'])
    pts = [(22, 0), (44, 22), (36, 24), (60, 46), (54, 48), (72, 68)]   # piorun: ostry zygzak w szczyt wiezy
    for a, b in zip(pts, pts[1:]): line(c, a[0] - 1, a[1], b[0] - 1, b[1], 'y3', 5); line(c, a[0], a[1], b[0], b[1], 'white', 3)
    for x, y, a in ((28, 96, 1), (114, 132, -1)):
        t, _ = _layer_person(cx=x, base=y + 17, h=36, robe='r3', trim='g3', hair='b2', belt=False, lh=(-6, -14), rh=(6, -14))
        ca, sa = math.cos(a * .6), math.sin(a * .6)
        paste_xf(c, t, lambda X, Y: (round(x + (X - x) * ca - (Y - y) * sa), round(y + (X - x) * sa + (Y - y) * ca)))
    r = random.Random(16)
    for _ in range(34):
        x, y = r.randrange(26, 118), r.randrange(80, 186); k = r.choice(['y3', 'o4', 'y2', 'o3']); c.set(x, y, P[k]); r.random() < .4 and c.set(x + 1, y, P[k])
    return finish(c)

# ---------------------------------------------------------------- 17
def ar17():
    c = card(); ramp(c, 0, 0, W, 150, ['n1', 'n2', 'n3', 'v1']); stars(c, 5, 90, 20, 17, ('cream', 's4'))
    glow(c, 72, 54, 44, 'g2', 1.6)
    for k, (x, y) in enumerate(((28, 44), (116, 44), (18, 76), (126, 78), (40, 98), (104, 100), (72, 112))): star(c, x, y, 5 if k < 6 else 4, 'g4', 8, .3)
    star(c, 72, 54, 20, 'g3', 8, .3, 'white'); star(c, 72, 54, 11, 'g4', 8, .4, 'white')
    hills(c, 128, 4, 'n2', 8, .06); mountains(c, 138, 20, 'n1', 3, 3)
    ramp(c, 0, 138, W, H, ['n2', 'e1', 'ink'])
    c.ellipse(72, 168, 52, 14, P['t1'], True); c.ellipse(72, 168, 44, 10, P['t2'], True)
    for x in range(34, 112): blend(c, x, 168 + (x * 7) % 5 - 2, P['g4'], max(0, .8 - abs(x - 72) / 30))
    f = person(c, 72, 164, 92, robe='v2', trim='g3', hair='b1', skin='k2', lh=(-26, 36), rh=(26, 30))
    (lx, ly), (rx, ry) = f['hand_l'], f['hand_r']
    for jx, jy in ((lx - 1, ly + 1), (rx + 1, ry + 1)):
        poly(c, [(jx - 5, jy - 6), (jx + 5, jy - 6), (jx + 6, jy + 3), (jx - 6, jy + 3)], 'ink'); poly(c, [(jx - 4, jy - 5), (jx + 4, jy - 5), (jx + 5, jy + 2), (jx - 5, jy + 2)], 'g2'); rect(c, jx - 4, jy - 5, 2, 7, 'g3')
    stream(c, (lx - 1, ly + 3), (lx - 4, 168), 3, 'g4', 14); stream(c, (rx + 1, ry + 3), (rx + 3, 156), 2, 'g4', 10)
    for x in range(10, 134, 6): c.set(x, 150 + x % 4, P['e3'])
    return finish(c)

CARDS = {'ar12': ar12, 'ar13': ar13, 'ar14': ar14, 'ar15': ar15, 'ar16': ar16, 'ar17': ar17}
