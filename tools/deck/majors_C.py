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

# ---------------------------------------------------------------- 12
def ar12():
    c = card(); ramp(c, 0, 0, W, 190, ['n1', 'n2', 'n3', 'v1']); stars(c, 5, 60, 24, 12)
    glow(c, 72, 112, 48, 'g2', 1.7)
    ground(c, 172, ['e1', 'ink'], 4)
    for x in (24, 112): rect(c, x - 3, 40, 7, 134, 'ink'); rect(c, x - 2, 40, 2, 134, 'b2')
    rect(c, 20, 38, 104, 8, 'ink'); rect(c, 21, 39, 102, 5, 'b2'); rect(c, 21, 39, 102, 1, 'b3')
    for x, y in ((34, 48), (50, 47), (96, 48), (108, 47)): c.ellipse(x, y, 4, 2, P['e2'], True); c.set(x, y, P['e3'])
    line(c, 72, 46, 72, 68, 'cream')
    # nogi (jedna zgieta), tulow, glowa w dol
    poly(c, [(69, 66), (75, 66), (77, 84), (67, 84)], 'ink'); poly(c, [(70, 67), (74, 67), (75, 84), (69, 84)], 'v3')
    poly(c, [(60, 66), (66, 66), (70, 74), (76, 78), (73, 81), (66, 76), (62, 72)], 'ink')
    poly(c, [(61, 67), (65, 67), (69, 74), (74, 78), (73, 79), (66, 75)], 'v2')
    poly(c, [(62, 84), (82, 84), (80, 112), (64, 112)], 'ink'); poly(c, [(64, 85), (80, 85), (78, 111), (66, 111)], 'r2')
    rect(c, 64, 85, 16, 2, 'g3'); poly(c, [(66, 90), (78, 90), (76, 108), (68, 108)], 'r1')
    poly(c, [(64, 90), (52, 100), (56, 104), (66, 98)], 'ink'); poly(c, [(80, 90), (92, 100), (88, 104), (78, 98)], 'ink')  # rece za plecami
    disc(c, 72, 120, 9, 'ink'); disc(c, 72, 120, 8, 'k1'); poly(c, [(64, 114), (80, 114), (78, 111), (66, 111)], 'b2')
    rect(c, 68, 121, 3, 1, 'ink'); rect(c, 74, 121, 3, 1, 'ink')  # zamkniete oczy
    for r in (14, 15): c.ellipse(72, 120, r, r - 2, P['g3'], False)   # aureola
    return finish(c)

# ---------------------------------------------------------------- 13
def ar13():
    c = card(); ramp(c, 0, 0, W, 150, ['ink', 'n2', 'v1', 'r1']); stars(c, 5, 70, 16, 13)
    glow(c, 72, 128, 62, 'o2', 2); disc(c, 72, 126, 22, 'o3'); disc(c, 72, 126, 18, 'o4'); disc(c, 72, 126, 12, 'o5')
    hills(c, 150, 6, 'n2', 3, .08); ground(c, 162, ['e1', 'ink'], 7)
    # kosa
    line(c, 104, 40, 104, 182, 'ink', 3); line(c, 105, 40, 105, 182, 'b2')
    poly(c, [(104, 38), (80, 36), (62, 46), (84, 44), (104, 46)], 'ink'); poly(c, [(103, 40), (82, 39), (70, 44), (84, 43), (103, 44)], 's4')
    # kruk
    raven(c, 108, 62, 1.2, 'up')
    # postac
    poly(c, [(54, 182), (60, 84), (84, 84), (92, 182)], 'ink'); poly(c, [(60, 182), (64, 90), (80, 90), (86, 182)], 'n2')
    poly(c, [(70, 100), (74, 100), (76, 182), (70, 182)], 'v1')
    poly(c, [(56, 70), (72, 56), (88, 70), (92, 100), (52, 100)], 'ink')     # kaptur i barki
    c.ellipse(72, 72, 8, 10, P['ink'], True); disc(c, 72, 74, 6, 'y3'); rect(c, 69, 73, 2, 3, 'ink'); rect(c, 74, 73, 2, 3, 'ink'); rect(c, 71, 78, 3, 1, 'ink')
    line(c, 66, 70, 72, 62, 'n3'); line(c, 78, 62, 78, 72, 'n3')
    line(c, 88, 96, 102, 100, 'ink', 3); rect(c, 100, 98, 6, 5, 'y3')      # dlon na kosie
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
    f = figure(c, 72, 172, 100, robe='s4', trim='g3', hood=False, arms='out', skin='k2')
    hx, hy = f['head']; disc(c, hx, hy, 5, 'ink'); disc(c, hx, hy, 4, 'k2')
    for r in (9, 10): c.ellipse(hx, hy, r, r, P['g4'], False)
    star(c, 72, 98, 4, 'g3', 4, .35, 'white')
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
    rect(c, 46, 134, 52, 50, 'ink'); rect(c, 48, 136, 48, 46, 'n2'); rect(c, 48, 136, 48, 2, 'y1'); rect(c, 46, 134, 52, 1, 'r3')
    poly(c, [(52, 130), (92, 130), (96, 86), (48, 86)], 'ink'); poly(c, [(56, 130), (88, 130), (90, 90), (54, 90)], 'n3')   # ciala
    poly(c, [(64, 90), (80, 90), (80, 130), (64, 130)], 'v1')
    for s in (-1, 1): poly(c, [(72 + s * 16, 88), (72 + s * 30, 100), (72 + s * 24, 112), (72 + s * 14, 100)], 'ink')
    disc(c, 72, 70, 13, 'ink'); disc(c, 72, 71, 11, 'n3'); rect(c, 62, 68, 20, 2, 'ink')
    for s in (-1, 1):
        poly(c, [(72 + s * 6, 62), (72 + s * 16, 60), (72 + s * 20, 38), (72 + s * 11, 48), (72 + s * 5, 58)], 'ink')   # rogi
        poly(c, [(72 + s * 8, 60), (72 + s * 15, 59), (72 + s * 19, 42), (72 + s * 12, 50)], 'y2')
        c.rect(72 + s * 6 - (3 if s < 0 else 0), 70, 3, 2, P['o4'])     # oczy
    rect(c, 69, 77, 7, 2, 'ink'); rect(c, 70, 77, 1, 1, 'white'); rect(c, 74, 77, 1, 1, 'white')
    star(c, 72, 58, 3, 'r3', 5, .4, 'r4')
    for s in (-1, 1):   # lancuchy i malutkie postacie
        px = 72 + s * 46; hx, hy = 72 + s * 24, 140
        for i in range(11):
            t = i / 10; c.set(round(hx + (px - hx) * t), round(hy + 6 * t + 3 * math.sin(t * 3.14)), P['y3'])
        poly(c, [(px - 5, 184), (px + 5, 184), (px + 3, 160), (px - 3, 160)], 'ink'); poly(c, [(px - 4, 183), (px + 4, 183), (px + 2, 161), (px - 2, 161)], 'v2')
        disc(c, px, 155, 5, 'ink'); disc(c, px, 155, 4, 'v3'); rect(c, px - 3, 150, 2, 3, 'ink'); rect(c, px + 2, 150, 2, 3, 'ink')
        c.set(px - 2, 155, P['r3']); c.set(px + 2, 155, P['r3']); line(c, px, 163, hx - s * 2 + (px - hx) // 12 * 0, hy + 6, 'y2')
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
    crown(c, 112, 46, 12, 3, 'g3'); line(c, 108, 36, 118, 56, 'g2')
    # piorun
    pts = [(118, 22), (104, 44), (112, 46), (94, 70), (100, 70), (86, 92)]
    for a, b in zip(pts, pts[1:]): line(c, a[0], a[1], b[0], b[1], 'white', 2); line(c, a[0] + 3, a[1], b[0] + 3, b[1], 's4')
    glow(c, 100, 56, 28, 's4', 2.4)
    # spadajace postacie i okruchy
    for x, y, a in ((30, 92, 1), (112, 128, -1)):
        disc(c, x, y, 3, 'k1'); poly(c, [(x - 2, y + 3), (x + 2, y + 3), (x + 4 * a, y + 14), (x, y + 12)], 'r3'); line(c, x, y + 4, x - 5 * a, y - 4 + 8, 'r3'); line(c, x, y + 4, x + 6 * a, y + 8, 'r3')
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
    # klecząca postac
    poly(c, [(58, 160), (62, 112), (82, 112), (92, 160)], 'ink'); poly(c, [(62, 160), (65, 114), (80, 114), (88, 160)], 'v2'); poly(c, [(70, 120), (74, 120), (76, 160), (70, 160)], 'v3')
    disc(c, 72, 104, 8, 'ink'); disc(c, 72, 104, 7, 'k2'); poly(c, [(64, 100), (80, 100), (82, 118), (62, 118)], 'ink') if False else None
    poly(c, [(63, 102), (66, 94), (78, 94), (81, 102), (82, 118), (80, 108), (64, 108), (62, 118)], 'b1')
    rect(c, 68, 105, 2, 1, 'ink'); rect(c, 74, 105, 2, 1, 'ink')
    line(c, 64, 118, 48, 134, 'v2', 3); line(c, 80, 118, 98, 130, 'v2', 3)
    for jx, jy in ((44, 138), (100, 134)):
        poly(c, [(jx - 5, jy - 6), (jx + 5, jy - 6), (jx + 6, jy + 3), (jx - 6, jy + 3)], 'ink'); poly(c, [(jx - 4, jy - 5), (jx + 4, jy - 5), (jx + 5, jy + 2), (jx - 5, jy + 2)], 'g2'); rect(c, jx - 4, jy - 5, 2, 7, 'g3')
    stream(c, (44, 140), (40, 166), 3, 'g4', 14); stream(c, (100, 136), (100, 150), 2, 'g4', 10)
    for x in range(10, 134, 6): c.set(x, 150 + x % 4, P['e3'])
    return finish(c)

CARDS = {'ar12': ar12, 'ar13': ar13, 'ar14': ar14, 'ar15': ar15, 'ar16': ar16, 'ar17': ar17}
