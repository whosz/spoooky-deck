"""Wielkie Arkana 18-21: Księżyc, Słońce, Sąd Ostateczny, Świat."""
import sys; sys.path.insert(0, 'tools/deck'); sys.path.insert(0, 'tools')
from lib import *

def beast(c, x, y, s, col, tail_up=True, face=1):
    """Czworonóg (pies/wilk/koń uproszczony): x,y = podstawa. face=1 w prawo."""
    f = face
    c.ellipse(x, y - 6 * s, 7 * s, 3.5 * s, P[col], True)
    poly(c, [(x + f * 5 * s, y - 8 * s), (x + f * 9 * s, y - 13 * s), (x + f * 13 * s, y - 11 * s), (x + f * 13 * s, y - 8 * s), (x + f * 8 * s, y - 6 * s)], col)
    poly(c, [(x + f * 8 * s, y - 12 * s), (x + f * 8 * s, y - 16 * s), (x + f * 10 * s, y - 13 * s)], col)
    for dx in (-5, -3, 3, 5): rect(c, x + dx * s, y - 5 * s, max(1, s), 5 * s, col)
    line(c, x - f * 6 * s, y - 7 * s, x - f * 10 * s, y - (13 if tail_up else 6) * s, col, 2)
    c.set(round(x + f * 11 * s), round(y - 11 * s), P['o4'])

def ar18():
    c = card(); ramp(c, 0, 0, W, 150, ['ink', 'n2', 'v1', 'n3']); stars(c, 24, 100, 40, 18)
    glow(c, 72, 66, 56, 'g1', 1.5); glow(c, 72, 66, 36, 'g2', 2.2)
    disc(c, 72, 66, 22, 'g2'); disc(c, 72, 66, 20, 'g4'); disc(c, 66, 68, 17, 'g3')   # tarcza + cień (sierp)
    disc(c, 72, 66, 11, 'g4'); disc(c, 74, 64, 8, 'g3')
    for dx, dy in ((-4, 4), (3, 8), (6, 1)): c.set(72 + dx, 66 + dy, P['g2'])
    for i in range(16):   # krople/promienie
        a = i * math.pi / 8; line(c, 72 + 26 * math.cos(a), 66 + 26 * math.sin(a), 72 + 31 * math.cos(a), 66 + 31 * math.sin(a), 'g2')
    hills(c, 120, 6, 'n2', 3, .06); hills(c, 128, 5, 'e1', 5, .08)
    tower(c, 14, 96, 18, 44, 'y1', 'r1', True); tower(c, 112, 96, 18, 44, 'y1', 'r1', True)
    poly(c, [(66, 128), (78, 128), (100, 186), (44, 186)], 'n3')          # ścieżka
    poly(c, [(69, 128), (75, 128), (80, 186), (64, 186)], 'g1')
    beast(c, 36, 172, 1.3, 'ink', True, 1); beast(c, 112, 172, 1.3, 'y1', False, -1)
    c.rect(0, 174, W, 12, P['t1'])
    ramp(c, 0, 168, W, 186, ['n3', 't1', 't1'])
    for x in range(W): blend(c, x, 170, P['t2'], .6 if x % 3 else .2)
    c.ellipse(72, 178, 8, 3, P['r3'], True); c.ellipse(72, 177, 6, 2, P['r4'], True)   # rak
    for dx in (-1, 1): line(c, 72 + dx * 7, 177, 72 + dx * 11, 172, 'r3'); disc(c, 72 + dx * 11, 171, 2, 'r3')
    for dx in (-5, 5): c.set(72 + dx, 180, P['r2'])
    c.set(70, 175, P['o4']); c.set(74, 175, P['o4'])
    return finish(c)

def ar19():
    c = card(); ramp(c, 0, 0, W, 150, ['n3', 'v2', 'r2', 'o2'])
    glow(c, 72, 60, 70, 'o3', 2); glow(c, 72, 60, 38, 'o5', 2.5)
    for i in range(32):
        a = i * math.pi / 16; r2 = 46 if i % 2 else 38
        line(c, 72 + 24 * math.cos(a), 60 + 24 * math.sin(a), 72 + r2 * math.cos(a), 60 + r2 * math.sin(a), 'o4' if i % 2 else 'o3')
    disc(c, 72, 60, 23, 'o2'); disc(c, 72, 60, 21, 'o4'); disc(c, 72, 60, 17, 'o5')
    c.rect(66, 58, 3, 2, P['o2']); c.rect(76, 58, 3, 2, P['o2']); c.rect(68, 66, 9, 1, P['o3'])
    mountains(c, 130, 24, 'r1', 9, 4); hills(c, 134, 4, 'v1', 2, .1)
    rect(c, 0, 118, W, 30, 'ink'); rect(c, 0, 120, W, 26, 'y1')   # mur
    for x in range(0, W, 12): rect(c, x, 112, 8, 8, 'y1'); rect(c, x, 112, 8, 1, 'y2')
    for x in range(0, W, 8): rect(c, x, 130 + (x // 8 % 2) * 6, 7, 1, 'ink')
    ramp(c, 0, 146, W, H, ['e1', 'e1', 'ink'])
    for x in (14, 34, 108, 128):   # słoneczniki
        h = 112 + (x * 7 % 9); line(c, x, h, x, 160, 'e2', 2)
        poly(c, [(x, 142), (x - 7, 138), (x - 3, 146)], 'e3'); poly(c, [(x + 1, 150), (x + 8, 145), (x + 4, 154)], 'e3')
        for a in range(8): disc(c, x + 5 * math.cos(a * .785) - 0, h + 5 * math.sin(a * .785), 2, 'o3')
        disc(c, x, h, 3, 'b1'); c.set(x - 1, h - 1, P['b2'])
    # koń (blady) i dziecko
    w = 'y3'
    c.ellipse(72, 150, 20, 9, P['ink'], True); c.ellipse(72, 150, 19, 8, P[w], True); c.ellipse(70, 153, 14, 4, P['y2'], True)
    poly(c, [(86, 146), (96, 124), (106, 128), (104, 140), (92, 152)], 'ink'); poly(c, [(88, 146), (97, 127), (104, 130), (102, 139), (92, 150)], w)
    poly(c, [(96, 126), (99, 118), (101, 128)], w); c.set(102, 131, P['ink']); c.set(103, 131, P['o4'])
    poly(c, [(86, 142), (84, 126), (94, 130)], 'y2')   # grzywa
    for dx in (-14, -8, 8, 14): rect(c, 72 + dx, 156, 3, 20, 'ink'); rect(c, 73 + dx, 156, 1, 18, 'y3')
    line(c, 52, 146, 46, 166, 'y2', 2)
    # dziecko
    disc(c, 72, 120, 6, 'ink'); disc(c, 72, 120, 5, 'k2'); c.set(70, 120, P['ink']); c.set(74, 120, P['ink'])
    poly(c, [(72, 114), (79, 112), (76, 118)], 'o3'); disc(c, 72, 114, 2, 'o4')   # wianek
    poly(c, [(66, 127), (78, 127), (80, 142), (64, 142)], 'ink'); poly(c, [(67, 128), (77, 128), (78, 141), (66, 141)], 'k2')
    line(c, 66, 129, 54, 116, 'k2', 2); line(c, 78, 129, 88, 118, 'k2', 2)
    line(c, 54, 116, 54, 96, 'b2'); poly(c, [(55, 96), (68, 99), (55, 106)], 'r3'); rect(c, 55, 96, 13, 1, 'r4')   # sztandar
    return finish(c)

def angel(c, cx, cy):
    glow(c, cx, cy, 44, 'g3', 2)
    for d in (-1, 1):   # skrzydła
        poly(c, [(cx + d * 5, cy - 4), (cx + d * 40, cy - 22), (cx + d * 44, cy - 4), (cx + d * 36, cy + 10), (cx + d * 5, cy + 12)], 'ink')
        poly(c, [(cx + d * 6, cy - 3), (cx + d * 38, cy - 19), (cx + d * 41, cy - 5), (cx + d * 34, cy + 8), (cx + d * 6, cy + 10)], 's3')
        for k in range(5): line(c, cx + d * 8, cy + 6, cx + d * (36 + k), cy - 14 + k * 5, 's4' if k % 2 else 's2')
    poly(c, [(cx - 7, cy - 2), (cx + 7, cy - 2), (cx + 12, cy + 24), (cx - 12, cy + 24)], 'ink')
    poly(c, [(cx - 6, cy - 1), (cx + 6, cy - 1), (cx + 10, cy + 23), (cx - 10, cy + 23)], 'cream')
    rect(c, cx - 1, cy, 2, 22, 's3')
    disc(c, cx, cy - 8, 6, 'ink'); disc(c, cx, cy - 8, 5, 'k2'); disc(c, cx, cy - 12, 5, 'g3'); rect(c, cx - 5, cy - 13, 10, 2, 'g4')
    c.set(cx - 2, cy - 8, P['ink']); c.set(cx + 2, cy - 8, P['ink'])
    line(c, cx - 6, cy + 2, cx - 20, cy - 4, 'cream', 2)   # ręka z trąbą
    poly(c, [(cx - 19, cy - 6), (cx - 52, cy - 14), (cx - 52, cy - 2), (cx - 19, cy - 2)], 'ink')
    poly(c, [(cx - 20, cy - 5), (cx - 50, cy - 12), (cx - 50, cy - 3), (cx - 20, cy - 3)], 'g3'); rect(c, cx - 50, cy - 12, 3, 9, 'g4')
    poly(c, [(cx - 50, cy - 8), (cx - 50, cy + 14), (cx - 22, cy + 14), (cx - 22, cy - 6)], 'r3')   # sztandar
    rect(c, cx - 50, cy - 8, 28, 1, 'r4'); rect(c, cx - 38, cy, 4, 12, 'g3'); rect(c, cx - 42, cy + 4, 12, 3, 'g3')

def ar20():
    c = card(); ramp(c, 0, 0, W, 190, ['ink', 'n3', 'v2', 'n3', 'n1'])
    glow(c, 72, 52, 60, 'g1', 1.8)
    clouds(c, 28, 72, ['s1', 'y2', 'y3'], 20, 8); clouds(c, 70, 90, ['n3', 's1', 's2'], 21, 6)
    angel(c, 78, 50)
    for x, y in ((20, 100), (122, 104)): raven(c, x, y, 1, 'up')
    mountains(c, 142, 30, 'n2', 6, 5); ramp(c, 0, 142, W, H, ['n2', 'e1', 'ink'])
    for gx, h in ((14, 28), (48, 36), (90, 36), (124, 28)):   # groby
        rect(c, gx - 8, 162, 20, 20, 'ink'); rect(c, gx - 7, 163, 18, 4, 'y1'); rect(c, gx - 7, 163, 18, 1, 'y2')
    for fx, hh, rb in ((24, 40, 'y2'), (72, 52, 'cream'), (118, 40, 'y2')):
        f = figure(c, fx, 170, hh, robe=rb, trim='y3', hood=False, arms='up', skin='y3'); 
    glow(c, 72, 120, 26, 'g2', 2.5)
    return finish(c)

def leaf(c, x, y, a):
    ex, ey = x + 4 * math.cos(a), y + 4 * math.sin(a)
    c.ellipse(x, y, 4.5, 2.4, P['ink'], True); c.ellipse(x, y, 3.8, 1.8, P['e3'], True); c.set(round(x - 1), round(y - 1), P['e4'])

def ar21():
    c = card(); ramp(c, 0, 0, W, H, ['ink', 'n2', 'v1', 'n2', 'ink']); stars(c, 24, 190, 40, 21)
    glow(c, 72, 106, 62, 'g1', 1.6)
    cx, cy, rx, ry = 72, 106, 33, 56
    for i in range(64):   # wieniec
        a = i * 2 * math.pi / 64
        x, y = cx + rx * math.cos(a), cy + ry * math.sin(a); leaf(c, x, y, a)
        if i % 4 == 0: c.set(round(x), round(y) - 1, P['r3'])
    for dy, d in ((-ry - 1, 1), (ry + 1, 1)):   # wstęgi
        rect(c, cx - 10, cy + dy - 1, 21, 3, 'r3'); rect(c, cx - 10, cy + dy - 1, 21, 1, 'r4')
    for a in (0, math.pi / 2, math.pi, -math.pi / 2): pass
    glow(c, 72, 106, 28, 'g2', 2.2)
    # tancerka
    poly(c, [(72, 82), (80, 98), (76, 118), (62, 126), (66, 106)], 'ink')
    poly(c, [(72, 84), (78, 98), (75, 116), (63, 124), (67, 106)], 'v3'); poly(c, [(76, 100), (88, 108), (78, 114)], 'cream')   # szarfa
    line(c, 72, 92, 58, 80, 'k1', 2); line(c, 74, 94, 88, 104, 'k1', 2); line(c, 60, 80, 54, 78, 'g3', 1)
    line(c, 70, 124, 62, 140, 'k1', 2); line(c, 66, 120, 80, 128, 'k1', 2)
    disc(c, 72, 79, 6, 'ink'); disc(c, 72, 79, 5, 'k2'); disc(c, 72, 75, 4, 'b1'); c.set(70, 80, P['ink']); c.set(74, 80, P['ink'])
    # różdżki
    line(c, 52, 76, 54, 82, 'g3', 2); line(c, 88, 108, 94, 112, 'g3', 2)
    # cztery żywioły w rogach
    for x, y in ((24, 46), (120, 46), (24, 166), (120, 166)): disc(c, x, y, 13, 'ink'); disc(c, x, y, 12, 'n3'); c.ellipse(x, y, 12, 12, P['g2'])
    x, y = 24, 46    # ogień
    poly(c, [(x, y - 9), (x + 6, y + 2), (x + 3, y + 8), (x - 3, y + 8), (x - 6, y + 2), (x - 2, y - 2)], 'o3'); poly(c, [(x, y), (x + 3, y + 6), (x - 3, y + 6)], 'o5')
    x, y = 120, 46   # powietrze
    for k, w in ((-6, 9), (-1, 11), (4, 8)): c.ellipse(x + (k % 3) - 1, y + k, w, 1.2, P['s4'], True)
    c.ellipse(x + 8, y - 1, 3, 3, P['s3']); c.ellipse(x - 8, y + 4, 2.5, 2.5, P['s3'])
    x, y = 24, 166   # woda
    for k in (-6, 0, 6):
        for dx in range(-8, 9): c.set(x + dx, y + k + round(1.5 * math.sin(dx * .8)), P['t3'])
    x, y = 120, 166  # ziemia
    poly(c, [(x - 9, y + 7), (x - 3, y - 8), (x + 2, y), (x + 5, y - 5), (x + 10, y + 7)], 'e3'); poly(c, [(x - 3, y - 8), (x + 1, y - 1), (x - 5, y + 4)], 'e4')
    return finish(c)

CARDS = {'ar18': ar18, 'ar19': ar19, 'ar20': ar20, 'ar21': ar21}
