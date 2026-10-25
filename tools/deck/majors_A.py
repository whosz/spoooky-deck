"""Major arcana 0-5: The Fool, The Magician, The High Priestess, The Empress, The Emperor, The Hierophant."""
import sys; sys.path.insert(0, 'tools/deck'); sys.path.insert(0, 'tools')
from lib import *

def pillar(c, x, w, y0, y1, name='y2', hi='y3'):
    rect(c, x - 1, y0, w + 2, y1 - y0, 'ink'); rect(c, x, y0, w, y1 - y0, name); rect(c, x, y0, 2, y1 - y0, hi)
    rect(c, x - 3, y0, w + 6, 4, 'ink'); rect(c, x - 2, y0 + 1, w + 4, 2, hi)
    rect(c, x - 3, y1 - 4, w + 6, 4, 'ink'); rect(c, x - 2, y1 - 3, w + 4, 2, hi)

def candle_glow(c, x, y, r=60, p=2.0):
    glow(c, x, y, r, 'g2', p); glow(c, x, y, r * .5, 'g3', p)

def ar00():
    c = card(); ramp(c, 0, 0, W, 150, ['n1', 'n3', 'v1', 'v2'])
    stars(c, 5, 90, 26, 3)
    candle_glow(c, 98, 78, 56); disc(c, 98, 78, 11, 'g3'); disc(c, 98, 78, 8, 'g4')
    mountains(c, 150, 60, 'n3', 5, 4); mountains(c, 165, 45, 'n2', 9, 4)
    # cliff and abyss
    poly(c, [(0, 142), (84, 142), (90, 150), (86, 216), (0, 216)], 'ink')
    ramp(c, 0, 151, 85, 216, ['b2', 'b1', 'n2', 'ink'])
    poly(c, [(0, 144), (82, 144), (86, 150), (0, 150)], 'e2'); rect(c, 0, 144, 82, 2, 'e3')
    for x in range(4, 80, 7): c.set(x, 143, P['e4']); c.set(x + 1, 142, P['e3'])
    ramp(c, 87, 160, W, H, ['n2', 'ink'])
    glow(c, 66, 100, 46, 'v1', 1.6)
    f = person(c, 66, 143, 92, robe='v2', trim='r3', hair='y3', hat='cap', lh=(-5, 12), rh=(14, -10))
    hx, hy = f['hand_r']; line(c, hx - 12, hy + 34, hx + 10, hy - 22, 'b2', 2)
    disc(c, hx + 11, hy - 23, 4, 'v3'); disc(c, hx + 11, hy - 23, 3, 'r2')
    lx, ly = f['hand_l']; c.set(lx, ly - 2, P['white']); c.set(lx + 1, ly - 3, P['white']); line(c, lx, ly, lx + 1, ly - 4, 'e3')
    # dog
    poly(c, [(36, 142), (50, 142), (52, 130), (46, 126), (38, 130)], 'cream'); rect(c, 36, 142, 3, 3, 'cream')
    rect(c, 46, 121, 7, 6, 'cream'); poly(c, [(52, 121), (55, 117), (55, 124)], 'cream'); c.set(49, 123, P['ink'])
    line(c, 37, 130, 32, 123, 'cream')
    raven(c, 100, 50, 1.0)
    return finish(c)

def ar01():
    c = card(); ramp(c, 0, 0, W, 190, ['ink', 'v1', 'r1', 'r2'])
    candle_glow(c, 72, 58, 52, 2.2)
    # lemniscate over the head
    for t in range(0, 360, 4):
        a = math.radians(t); d = 1 + math.sin(a) ** 2
        c.set(round(72 + 16 * math.cos(a) / d * 1.8), round(50 + 16 * math.sin(a) * math.cos(a) / d * 1.8), P['g4'])
    rect(c, 10, 160, 124, 40, 'ink'); ramp(c, 10, 160, 134, 190, ['r1', 'ink'])
    # flowers in front
    for x in range(16, 132, 9):
        line(c, x, 186, x, 176 - (x % 3) * 2, 'e2'); c.set(x, 175 - (x % 3) * 2, P['r4']); c.set(x + 1, 175 - (x % 3) * 2, P['r3'])
    # table
    rect(c, 22, 140, 100, 5, 'ink'); rect(c, 23, 141, 98, 3, 'b2'); rect(c, 23, 141, 98, 1, 'b3')
    rect(c, 28, 145, 5, 38, 'ink'); rect(c, 111, 145, 5, 38, 'ink'); rect(c, 29, 145, 3, 38, 'b1'); rect(c, 112, 145, 3, 38, 'b1')
    glow(c, 72, 90, 46, 'r2', 1.6)
    f = person(c, 72, 140, 98, robe='r3', trim='g3', hair='b1', beard=False, skin='k2', lh=(-6, 20), rh=(14, -26))
    hx, hy = f['hand_r']; line(c, hx - 2, hy + 6, hx + 3, hy - 14, 'cream', 2); c.set(hx + 3, hy - 16, P['g4']); c.set(hx + 4, hy - 16, P['white']); glow(c, hx + 3, hy - 16, 8, 'g3', 1.2)
    lx, ly = f['hand_l']; line(c, lx, ly, lx - 3, ly + 12, 'cream', 1)
    # four symbols on the table
    pentacle(c, 38, 130, .45); cup(c, 58, 128, .5); sword(c, 86, 128, .35); wand(c, 106, 128, .35)
    raven(c, 14, 70, 1.0, 'down')
    return finish(c)

def ar02():
    c = card(); ramp(c, 0, 0, W, 190, ['ink', 'n2', 'n3', 't1'])
    stars(c, 28, 100, 20, 11, ('s4', 'cream'))
    pillar(c, 14, 14, 40, 186, 'ink', 'n3'); pillar(c, 116, 14, 40, 186, 'y2', 'y3')
    # pomegranate curtain
    rect(c, 36, 52, 72, 134, 'ink'); rect(c, 38, 54, 68, 132, 't1')
    for x in range(38, 106, 4): line(c, x, 54, x, 185, 't2' if x % 8 == 0 else 'n3')
    for y in range(64, 180, 12):
        for x in range(42, 104, 10): c.set(x + (y // 12 % 2) * 4, y, P['r3'])
    glow(c, 72, 78, 40, 't3', 2.2)
    glow(c, 72, 100, 40, 'n3', 1.6)
    f = person(c, 72, 178, 104, robe='n4', trim='t3', hair='n2', skin='k1', lh=(-4, 12), rh=(4, 14), belt=False, hat='crown3')
    hx, hy = f['head']
    disc(c, hx, hy - 12, 5, 'cream'); disc(c, hx + 2, hy - 13, 4, 'n3'); c.set(hx - 1, hy - 12, P['white'])
    # scroll and crescent at the feet
    rect(c, 62, 128, 20, 12, 'ink'); rect(c, 63, 129, 18, 10, 'cream'); rect(c, 66, 132, 10, 1, 'y2'); rect(c, 66, 135, 8, 1, 'y2')
    disc(c, 72, 176, 9, 'cream'); disc(c, 76, 174, 8, 'ink')
    candle_glow(c, 72, 140, 20, 2.5)
    return finish(c)

def ar03():
    c = card(); ramp(c, 0, 0, W, 190, ['ink', 'e1', 'e2', 'e1'])
    stars(c, 28, 80, 16, 4, ('o5', 'e4'))
    # forest
    for i, x in enumerate(range(6, 144, 17)):
        h = 70 + (i * 23) % 40
        rect(c, x, 190 - h, 6, h, 'ink'); disc(c, x + 3, 190 - h, 13, 'e1'); disc(c, x + 3, 188 - h, 9, 'e2')
    candle_glow(c, 72, 90, 56, 2.0)
    # wheat field
    ramp(c, 0, 150, W, H, ['e2', 'e1', 'ink'])
    for x in range(4, 144, 6):
        h = 12 + (x * 7) % 8; line(c, x, 190, x, 190 - h, 'g2'); c.set(x, 190 - h - 1, P['g3']); c.set(x + 1, 190 - h, P['g4']); c.set(x - 1, 190 - h, P['g3'])
    # throne cushions
    poly(c, [(40, 160), (104, 160), (112, 186), (32, 186)], 'ink'); poly(c, [(42, 162), (102, 162), (108, 184), (36, 184)], 'r2')
    glow(c, 72, 120, 44, 'e2', 1.6)
    f = person(c, 72, 172, 100, robe='e3', trim='g3', hair='g2', skin='k2', lh=(-8, 12), rh=(12, -6))
    hx, hy = f['head']
    for k in range(7):
        a = math.pi + k * math.pi / 6; x, y = hx + 11 * math.cos(a), hy - 4 + 8 * math.sin(a)
        c.set(round(x), round(y), P['g4']); c.set(round(x), round(y) + 1, P['g3'])
    rect(c, hx - 6, hy - 8, 12, 2, 'g3')
    # shield with a heart
    poly(c, [(38, 128), (58, 128), (58, 144), (48, 154), (38, 144)], 'ink'); poly(c, [(40, 130), (56, 130), (56, 143), (48, 151), (40, 143)], 'r2')
    disc(c, 45, 137, 3, 'r3'); disc(c, 51, 137, 3, 'r3'); poly(c, [(42, 139), (54, 139), (48, 147)], 'r3'); c.set(44, 135, P['r4'])
    hx2, hy2 = f['hand_r']; line(c, hx2, hy2 + 14, hx2 + 1, hy2 - 16, 'g3', 2); disc(c, hx2 + 1, hy2 - 18, 4, 'g4'); disc(c, hx2 + 1, hy2 - 18, 2, 'white')
    raven(c, 112, 48, 1.0)
    return finish(c)

def ar04():
    c = card(); ramp(c, 0, 0, W, 190, ['r1', 'r2', 'o1', 'ink'])
    glow(c, 72, 80, 60, 'o3', 2.2); candle_glow(c, 72, 80, 48, 1.8)
    mountains(c, 150, 70, 'r1', 8, 4); mountains(c, 175, 40, 'ink', 4, 4)
    # throne
    rect(c, 30, 52, 84, 134, 'ink'); rect(c, 33, 55, 78, 131, 'y1'); rect(c, 33, 55, 4, 131, 'y2')
    rect(c, 30, 52, 84, 4, 'y3'); rect(c, 24, 120, 14, 66, 'ink'); rect(c, 106, 120, 14, 66, 'ink')
    rect(c, 26, 122, 10, 64, 'y1'); rect(c, 108, 122, 10, 64, 'y1')
    # ram heads on the armrests
    for x in (24, 112):
        disc(c, x + 4, 116, 6, 'ink'); disc(c, x + 4, 116, 4, 'y2'); c.set(x + 3, 116, P['o4']); c.set(x + 6, 116, P['o4'])
        for d in (-6, 14): c.ellipse(x + d + 2, 116, 3, 2, P['g3'], True)
    glow(c, 72, 100, 40, 'o3', 1.6)
    f = person(c, 72, 176, 110, robe='r3', trim='g3', hair='cream', beard=True, skin='k2', hat='crown5', lh=(-10, 8), rh=(10, 8))
    lx, ly = f['hand_l']; line(c, lx, ly + 12, lx, ly - 18, 'g3', 2); disc(c, lx, ly - 21, 4, 'ink'); disc(c, lx, ly - 21, 3, 'g4'); disc(c, lx, ly - 21, 1, 'ink')
    rx, ry = f['hand_r']; disc(c, rx, ry - 5, 6, 'ink'); disc(c, rx, ry - 5, 5, 'g3'); rect(c, rx - 2, ry - 10, 4, 1, 'g4'); rect(c, rx - 1, ry - 12, 2, 4, 'g4'); rect(c, rx - 3, ry - 11, 6, 1, 'g4')
    rect(c, 66, 176, 12, 4, 'g2')
    return finish(c)

def ar05():
    c = card(); ramp(c, 0, 0, W, 190, ['ink', 'v1', 'v2', 'n3'])
    candle_glow(c, 72, 70, 52, 2.0)
    pillar(c, 14, 14, 40, 186, 'y1', 'y2'); pillar(c, 116, 14, 40, 186, 'y1', 'y2')
    rect(c, 30, 176, 84, 10, 'ink'); rect(c, 32, 176, 80, 4, 'y2')  # platform
    # figure on the throne
    rect(c, 50, 70, 44, 110, 'ink'); rect(c, 52, 72, 40, 108, 'v1')
    glow(c, 72, 110, 40, 'v2', 1.6)
    f = person(c, 72, 178, 104, robe='r2', trim='g3', hair='cream', beard=True, skin='k2', hat='mitre', lh=(-8, 8), rh=(14, -4))
    hx, hy = f['hand_r']; line(c, hx, hy + 40, hx, hy - 26, 'g3', 2)
    for y, w in ((hy - 24, 5), (hy - 19, 7), (hy - 14, 9)): rect(c, hx - w // 2, y, w, 2, 'g4')
    rect(c, hx, hy - 30, 2, 8, 'g4')
    lx, ly = f['hand_l']; line(c, lx, ly, lx - 3, ly + 8, 'g4', 1)
    # two acolytes
    for x in (34, 110): person(c, x, 178, 58, robe='n4', trim='t3', hood=True, belt=False, lh=(0, 8), rh=(0, 8))
    raven(c, 112, 40, 1.0, 'down')
    return finish(c)

CARDS = {'ar00': ar00, 'ar01': ar01, 'ar02': ar02, 'ar03': ar03, 'ar04': ar04, 'ar05': ar05}
