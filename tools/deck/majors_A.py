"""Wielkie Arkana 0-5: Głupiec, Mag, Najwyższa Kapłanka, Cesarzowa, Cesarz, Najwyższy Kapłan."""
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
    # klif i przepaść
    poly(c, [(0, 142), (84, 142), (90, 150), (86, 216), (0, 216)], 'ink')
    ramp(c, 0, 151, 85, 216, ['b2', 'b1', 'n2', 'ink'])
    poly(c, [(0, 144), (82, 144), (86, 150), (0, 150)], 'e2'); rect(c, 0, 144, 82, 2, 'e3')
    for x in range(4, 80, 7): c.set(x, 143, P['e4']); c.set(x + 1, 142, P['e3'])
    ramp(c, 87, 160, W, H, ['n2', 'ink'])
    # postać na krawędzi, kij z węzełkiem
    line(c, 56, 100, 78, 74, 'b2', 2); disc(c, 79, 73, 4, 'v3'); disc(c, 79, 73, 3, 'r2')
    f = figure(c, 66, 143, 62, robe='v2', trim='r3', hood=True, arms='down')
    poly(c, [(60, 90), (72, 90), (76, 120), (56, 120)], 'v2'); rect(c, 58, 113, 18, 2, 'r3')
    c.set(66, 112, P['white']); line(c, 70, 91, 74, 80, 'v3')  # biała róża
    c.set(74, 79, P['white']); c.set(75, 79, P['white'])
    # pies
    poly(c, [(36, 142), (50, 142), (52, 130), (46, 126), (38, 130)], 'cream'); rect(c, 36, 142, 3, 3, 'cream')
    rect(c, 46, 121, 7, 6, 'cream'); poly(c, [(52, 121), (55, 117), (55, 124)], 'cream'); c.set(49, 123, P['ink'])
    line(c, 37, 130, 32, 123, 'cream')
    raven(c, 100, 50, 1.0)
    return finish(c)

def ar01():
    c = card(); ramp(c, 0, 0, W, 190, ['ink', 'v1', 'r1', 'r2'])
    candle_glow(c, 72, 58, 52, 2.2)
    # lemniskata nad głową
    for t in range(0, 360, 4):
        a = math.radians(t); d = 1 + math.sin(a) ** 2
        c.set(round(72 + 16 * math.cos(a) / d * 1.8), round(50 + 16 * math.sin(a) * math.cos(a) / d * 1.8), P['g4'])
    rect(c, 10, 160, 124, 40, 'ink'); ramp(c, 10, 160, 134, 190, ['r1', 'ink'])
    # kwiaty z przodu
    for x in range(16, 132, 9):
        line(c, x, 186, x, 176 - (x % 3) * 2, 'e2'); c.set(x, 175 - (x % 3) * 2, P['r4']); c.set(x + 1, 175 - (x % 3) * 2, P['r3'])
    # stół
    rect(c, 22, 140, 100, 5, 'ink'); rect(c, 23, 141, 98, 3, 'b2'); rect(c, 23, 141, 98, 1, 'b3')
    rect(c, 28, 145, 5, 38, 'ink'); rect(c, 111, 145, 5, 38, 'ink'); rect(c, 29, 145, 3, 38, 'b1'); rect(c, 112, 145, 3, 38, 'b1')
    f = figure(c, 72, 140, 88, robe='r3', trim='g3', hood=True, arms='up')
    rect(c, 62, 96, 20, 3, 'white')  # biała szata pod
    # różdżka w górze
    line(c, 98, 70, 104, 40, 'cream', 2); c.set(104, 38, P['g4']); c.set(105, 38, P['white']); glow(c, 104, 40, 8, 'g3', 1.2)
    line(c, 46, 106, 40, 120, 'cream', 1)
    # cztery symbole na stole
    pentacle(c, 38, 130, .45); cup(c, 58, 128, .5); sword(c, 86, 128, .35); wand(c, 106, 128, .35)
    raven(c, 14, 70, 1.0, 'down')
    return finish(c)

def ar02():
    c = card(); ramp(c, 0, 0, W, 190, ['ink', 'n2', 'n3', 't1'])
    stars(c, 28, 100, 20, 11, ('s4', 'cream'))
    pillar(c, 14, 14, 40, 186, 'ink', 'n3'); pillar(c, 116, 14, 40, 186, 'y2', 'y3')
    # zasłona z granatów
    rect(c, 36, 52, 72, 134, 'ink'); rect(c, 38, 54, 68, 132, 't1')
    for x in range(38, 106, 4): line(c, x, 54, x, 185, 't2' if x % 8 == 0 else 'n3')
    for y in range(64, 180, 12):
        for x in range(42, 104, 10): c.set(x + (y // 12 % 2) * 4, y, P['r3'])
    glow(c, 72, 78, 40, 't3', 2.2)
    # sylwetka kapłanki
    f = figure(c, 72, 178, 98, robe='n4', trim='t3', hood=True, arms='down')
    poly(c, [(60, 100), (84, 100), (96, 178), (48, 178)], 'n4'); rect(c, 66, 110, 12, 40, 'n3')
    # korona: rogi i księżyc
    disc(c, 72, 68, 7, 'cream'); disc(c, 75, 67, 6, 'n3') ; c.set(71, 68, P['white'])
    disc(c, 61, 76, 3, 'cream'); disc(c, 83, 76, 3, 'cream'); disc(c, 62, 76, 2, 'n3'); disc(c, 82, 76, 2, 'n3')
    # zwój i półksiężyc u stóp
    rect(c, 62, 128, 20, 12, 'ink'); rect(c, 63, 129, 18, 10, 'cream'); rect(c, 66, 132, 10, 1, 'y2'); rect(c, 66, 135, 8, 1, 'y2')
    disc(c, 72, 176, 9, 'cream'); disc(c, 76, 174, 8, 'ink')
    candle_glow(c, 72, 140, 20, 2.5)
    return finish(c)

def ar03():
    c = card(); ramp(c, 0, 0, W, 190, ['ink', 'e1', 'e2', 'e1'])
    stars(c, 28, 80, 16, 4, ('o5', 'e4'))
    # las
    for i, x in enumerate(range(6, 144, 17)):
        h = 70 + (i * 23) % 40
        rect(c, x, 190 - h, 6, h, 'ink'); disc(c, x + 3, 190 - h, 13, 'e1'); disc(c, x + 3, 188 - h, 9, 'e2')
    candle_glow(c, 72, 90, 56, 2.0)
    # pole zboża
    ramp(c, 0, 150, W, H, ['e2', 'e1', 'ink'])
    for x in range(4, 144, 6):
        h = 12 + (x * 7) % 8; line(c, x, 190, x, 190 - h, 'g2'); c.set(x, 190 - h - 1, P['g3']); c.set(x + 1, 190 - h, P['g4']); c.set(x - 1, 190 - h, P['g3'])
    # tron-poduszki
    poly(c, [(40, 160), (104, 160), (112, 186), (32, 186)], 'ink'); poly(c, [(42, 162), (102, 162), (108, 184), (36, 184)], 'r2')
    # sylwetka
    f = figure(c, 72, 172, 88, robe='e3', trim='g3', hood=False, arms='down', skin='k2')
    poly(c, [(64, 98), (80, 98), (90, 172), (54, 172)], 'e3')
    for k in range(5): c.set(66 + k * 3, 120 + (k % 2) * 8, P['r3']); c.set(62 + k * 4, 140 + (k % 2) * 6, P['r4'])
    # korona z gwiazd (12 gwiazdek)
    hx, hy = f['head']
    for k in range(7):
        a = math.pi + k * math.pi / 6; x, y = hx + 11 * math.cos(a), hy - 4 + 8 * math.sin(a)
        c.set(round(x), round(y), P['g4']); c.set(round(x), round(y) + 1, P['g3'])
    rect(c, hx - 7, hy - 8, 14, 2, 'g3')
    # włosy
    rect(c, hx - 8, hy - 3, 2, 10, 'g2'); rect(c, hx + 6, hy - 3, 2, 10, 'g2')
    # tarcza z sercem
    poly(c, [(38, 128), (58, 128), (58, 144), (48, 154), (38, 144)], 'ink'); poly(c, [(40, 130), (56, 130), (56, 143), (48, 151), (40, 143)], 'r2')
    disc(c, 45, 137, 3, 'r3'); disc(c, 51, 137, 3, 'r3'); poly(c, [(42, 139), (54, 139), (48, 147)], 'r3'); c.set(44, 135, P['r4'])
    # berło
    line(c, 98, 100, 104, 150, 'g3', 2); disc(c, 97, 98, 4, 'g4'); disc(c, 97, 98, 2, 'white')
    raven(c, 112, 48, 1.0)
    return finish(c)

def ar04():
    c = card(); ramp(c, 0, 0, W, 190, ['r1', 'r2', 'o1', 'ink'])
    glow(c, 72, 80, 60, 'o3', 2.2); candle_glow(c, 72, 80, 48, 1.8)
    mountains(c, 150, 70, 'r1', 8, 4); mountains(c, 175, 40, 'ink', 4, 4)
    # tron
    rect(c, 30, 52, 84, 134, 'ink'); rect(c, 33, 55, 78, 131, 'y1'); rect(c, 33, 55, 4, 131, 'y2')
    rect(c, 30, 52, 84, 4, 'y3'); rect(c, 24, 120, 14, 66, 'ink'); rect(c, 106, 120, 14, 66, 'ink')
    rect(c, 26, 122, 10, 64, 'y1'); rect(c, 108, 122, 10, 64, 'y1')
    # głowy baranów na podłokietnikach
    for x in (24, 112):
        disc(c, x + 4, 116, 6, 'ink'); disc(c, x + 4, 116, 4, 'y2'); c.set(x + 3, 116, P['o4']); c.set(x + 6, 116, P['o4'])
        for d in (-6, 14): c.ellipse(x + d + 2, 116, 3, 2, P['g3'], True)
    f = figure(c, 72, 176, 100, robe='r3', trim='g3', hood=False, arms='down', skin='k2')
    poly(c, [(60, 98), (84, 98), (96, 176), (48, 176)], 'r3'); rect(c, 66, 100, 12, 74, 'r2')
    hx, hy = f['head']
    crown(c, hx, hy - 5, 14, 5)
    poly(c, [(hx - 7, hy + 4), (hx + 7, hy + 4), (hx + 4, hy + 16), (hx - 4, hy + 16)], 'cream')  # broda
    rect(c, hx - 3, hy + 2, 6, 3, 'k2')
    # berło ankh i kula
    line(c, 36, 100, 38, 160, 'g3', 2); disc(c, 36, 96, 4, 'ink'); disc(c, 36, 96, 3, 'g4'); disc(c, 36, 96, 1, 'ink')
    disc(c, 106, 130, 6, 'ink'); disc(c, 106, 130, 5, 'g3'); rect(c, 104, 125, 4, 1, 'g4'); rect(c, 105, 123, 2, 4, 'g4'); rect(c, 103, 124, 6, 1, 'g4')
    rect(c, 66, 176, 12, 4, 'g2')
    return finish(c)

def ar05():
    c = card(); ramp(c, 0, 0, W, 190, ['ink', 'v1', 'v2', 'n3'])
    candle_glow(c, 72, 70, 52, 2.0)
    pillar(c, 14, 14, 40, 186, 'y1', 'y2'); pillar(c, 116, 14, 40, 186, 'y1', 'y2')
    rect(c, 30, 176, 84, 10, 'ink'); rect(c, 32, 176, 80, 4, 'y2')  # podest
    # postać na tronie
    rect(c, 50, 70, 44, 110, 'ink'); rect(c, 52, 72, 40, 108, 'v1')
    f = figure(c, 72, 178, 92, robe='r2', trim='g3', hood=False, arms='down', skin='k2')
    poly(c, [(62, 96), (82, 96), (92, 178), (52, 178)], 'r2'); rect(c, 69, 96, 6, 80, 'g2')
    hx, hy = f['head']
    poly(c, [(hx - 8, hy + 2), (hx - 6, hy - 11), (hx, hy - 15), (hx + 6, hy - 11), (hx + 8, hy + 2), (hx + 5, hy - 6), (hx - 5, hy - 6)], 'ink')
    poly(c, [(hx - 6, hy - 6), (hx - 4, hy - 11), (hx, hy - 14), (hx + 4, hy - 11), (hx + 6, hy - 6)], 'g3')  # tiara
    rect(c, hx - 1, hy - 12, 2, 4, 'r3')
    # laska z potrójnym krzyżem
    line(c, 98, 70, 100, 168, 'g3', 2)
    for y in (66, 74, 82): rect(c, 94 + (y == 82) * 0 - (y == 66) * 0 + 0, y, 12 - (y - 66) // 4 * 2, 2, 'g4')
    rect(c, 98, 62, 2, 30, 'g4')
    # dwaj akolici
    for x, rc in ((30, 'n4'), (114, 'n4')):
        poly(c, [(x - 8, 178), (x + 8, 178), (x + 4, 150), (x - 4, 150)], 'ink'); poly(c, [(x - 6, 177), (x + 6, 177), (x + 3, 152), (x - 3, 152)], rc)
        disc(c, x, 147, 5, 'ink'); disc(c, x, 147, 4, 'n4'); c.set(x - 1, 148, P['ink']); c.set(x + 1, 148, P['ink'])
    # klucze
    for x in (62, 80):
        disc(c, x, 168, 3, 'g3'); disc(c, x, 168, 1, 'ink'); line(c, x, 171, x, 180, 'g3'); rect(c, x, 177, 3, 1, 'g3')
    raven(c, 112, 40, 1.0, 'down')
    return finish(c)

CARDS = {'ar00': ar00, 'ar01': ar01, 'ar02': ar02, 'ar03': ar03, 'ar04': ar04, 'ar05': ar05}
