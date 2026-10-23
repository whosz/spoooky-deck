"""Wielkie Arkana B: ar06 Kochankowie, ar07 Rydwan, ar08 Sila, ar09 Pustelnik, ar10 Kolo Fortuny, ar11 Sprawiedliwosc."""
import sys; sys.path.insert(0, 'tools/deck'); sys.path.insert(0, 'tools')
from lib import *

def sky(c, names, y1=170): ramp(c, 0, 0, W, y1, names)

def ground(c, y, a, b, seed=3):
    hills(c, y, 5, a, seed, .08); ramp(c, 0, y + 10, W, H, [a, b, 'ink'])

def pillar(c, x, y0, y1, w=10, body='y1', hi='y2'):
    rect(c, x - 1, y0, w + 2, y1 - y0, 'ink'); rect(c, x, y0, w, y1 - y0, body); rect(c, x, y0, 2, y1 - y0, hi)
    rect(c, x - 3, y0, w + 6, 3, hi); rect(c, x - 3, y1 - 3, w + 6, 3, hi)

def ar06():
    c = card(); sky(c, ['n1', 'v1', 'r1', 'r2'], 160); stars(c, 28, 80, 24, 6)
    mountains(c, 150, 55, 'n2', 6, 3); ground(c, 156, 'e1', 'ink', 6)
    glow(c, 72, 58, 46, 'o4', 1.8); glow(c, 72, 58, 24, 'o5', 1.4)
    for s in (-1, 1):   # skrzydla anioła
        poly(c, [(72, 54), (72 + s * 44, 38), (72 + s * 36, 62), (72 + s * 26, 66), (72, 66)], 'ink')
        poly(c, [(72, 55), (72 + s * 41, 41), (72 + s * 33, 61), (72 + s * 24, 64), (72, 64)], 'g3')
        for k in range(4): line(c, 72 + s * 10, 56 + k * 2, 72 + s * (38 - k * 3), 44 + k * 5, 'g4')
    figure(c, 72, 88, 46, robe='r3', trim='o4', hood=False, arms='out', skin='k2')
    # postacie
    figure(c, 34, 176, 74, robe='n4', trim='s3', hood=False, arms='down', skin='k1')
    figure(c, 110, 176, 74, robe='r2', trim='r4', hood=False, arms='down', skin='k1')
    rect(c, 66, 100, 12, 60, 'ink')  # gora miedzy nimi
    poly(c, [(60, 156), (72, 108), (84, 156)], 'n3'); poly(c, [(66, 156), (72, 118), (78, 156)], 'n4')
    # drzewa: ogniste i zgnile
    for x, col in ((12, 'e2'), (128, 'r3')):
        rect(c, x, 110, 3, 50, 'b1'); disc(c, x + 1, 108, 10, 'ink'); disc(c, x + 1, 108, 8, col); disc(c, x - 2, 105, 3, 'e3' if col == 'e2' else 'o3')
    # kruk
    raven(c, 20, 52); raven(c, 112, 66, .8)
    return finish(c)

def ar07():
    c = card(); sky(c, ['ink', 'n2', 'n3', 'v1'], 150); stars(c, 28, 100, 40, 7)
    glow(c, 72, 84, 50, 'o1', 2)
    for x, y, w, h in ((8, 100, 18, 60), (118, 96, 18, 64), (30, 120, 12, 40)): tower(c, x, y, w, h, 'y1', 'r2')
    rect(c, 0, 158, W, 8, 'n2'); ground(c, 165, 'n3', 'ink', 7)
    # rydwan
    rect(c, 36, 130, 72, 30, 'ink'); rect(c, 38, 132, 68, 26, 'n4'); rect(c, 38, 132, 68, 3, 'g3')
    for x in range(42, 104, 8): rect(c, x, 140, 4, 12, 'n3')
    disc(c, 72, 146, 8, 'ink'); disc(c, 72, 146, 6, 'g3'); disc(c, 72, 146, 2, 'g1')
    for x in (38, 102):  # kola
        disc(c, x, 162, 9, 'ink'); disc(c, x, 162, 7, 'g2'); disc(c, x, 162, 4, 'ink')
        for a in range(0, 180, 45): line(c, x + 7 * math.cos(math.radians(a)), 162 + 7 * math.sin(math.radians(a)), x - 7 * math.cos(math.radians(a)), 162 - 7 * math.sin(math.radians(a)), 'g3')
    # baldachim
    for x in (40, 100): rect(c, x, 60, 4, 72, 'ink'); rect(c, x + 1, 60, 2, 72, 'g2')
    rect(c, 36, 50, 72, 12, 'ink'); rect(c, 38, 52, 68, 8, 'n4')
    for i in range(7): c.set(44 + i * 9, 56, P['o5']); c.set(43 + i * 9, 56, P['g4'])
    poly(c, [(36, 62), (108, 62), (102, 70), (42, 70)], 'ink')
    # woznica
    f = figure(c, 72, 134, 58, robe='r3', trim='g3', hood=False, arms='out', skin='k1')
    hx, hy = map(round, f['head']); crown(c, hx, hy - 5, 10, 3); rect(c, 62, 112, 20, 5, 'g3')
    glow(c, 72, 102, 16, 'o3', 2.2)
    # sfinksy (czarny i bialy)
    for x, col, d in ((22, 'ink', -1), (122, 'y3', 1)):
        rect(c, x - 16, 118, 32, 14, 'ink') if col == 'ink' else None
        poly(c, [(x - 14, 134), (x - 14, 148), (x + 14, 148), (x + 14, 134), (x + 8, 128), (x - 8, 128)], 'ink')
        poly(c, [(x - 12, 136), (x - 12, 146), (x + 12, 146), (x + 12, 136), (x + 7, 130), (x - 7, 130)], 'y1' if col == 'ink' else 'y3')
        disc(c, x + d * 9, 124, 6, 'ink'); disc(c, x + d * 9, 124, 4, 'y1' if col == 'ink' else 'y3'); c.set(x + d * 10, 123, P['o4'])
        poly(c, [(x + d * 5, 118), (x + d * 9, 112), (x + d * 13, 118)], 'ink')
        rect(c, x - 10, 148, 3, 14, 'ink'); rect(c, x + 7, 148, 3, 14, 'ink')
    raven(c, 14, 40); raven(c, 120, 36, .8)
    return finish(c)

def ar08():
    c = card(); sky(c, ['n1', 'e1', 'e2', 'n3'], 150); stars(c, 28, 70, 20, 8)
    mountains(c, 140, 40, 'e1', 8, 4); ground(c, 150, 'e1', 'ink', 8)
    glow(c, 38, 82, 30, 'o4', 2)
    # nieskonczonosc
    for dx in (-8, 8): c.ellipse(38 + dx, 40, 8, 5, P['o5']); c.ellipse(38 + dx, 40, 6, 3, P['o4'])
    # lew
    glow(c, 90, 150, 40, 'r1', 2)
    poly(c, [(84, 140), (130, 140), (132, 170), (120, 174), (92, 174), (80, 170)], 'ink')
    poly(c, [(86, 142), (128, 142), (129, 168), (120, 171), (94, 171), (84, 168)], 'o1')
    rect(c, 88, 160, 38, 4, 'r1'); poly(c, [(130, 146), (138, 138), (136, 158)], 'o1')
    rect(c, 90, 170, 6, 12, 'ink'); rect(c, 120, 170, 6, 12, 'ink'); rect(c, 91, 170, 4, 10, 'o2'); rect(c, 121, 170, 4, 10, 'o2')
    disc(c, 92, 150, 17, 'ink'); disc(c, 92, 150, 15, 'o1'); disc(c, 92, 150, 12, 'o2')   # grzywa
    for a in range(0, 360, 30): line(c, 92, 150, 92 + 18 * math.cos(math.radians(a)), 150 + 18 * math.sin(math.radians(a)), 'o1')
    disc(c, 92, 152, 9, 'ink'); disc(c, 92, 152, 8, 'o3'); rect(c, 86, 150, 3, 2, 'ink'); rect(c, 95, 150, 3, 2, 'ink'); c.set(87, 150, P['r4']); c.set(96, 150, P['r4'])
    rect(c, 89, 156, 6, 2, 'r3'); poly(c, [(86, 138), (90, 133), (94, 140)], 'o2'); poly(c, [(92, 138), (98, 133), (100, 141)], 'o2')
    # kobieta
    f = figure(c, 38, 160, 84, robe='y3', trim='e4', hood=False, arms='down', skin='k2')
    hx, hy = map(round, f['head'])
    for i in range(4): c.set(hx - 4 + i * 3, hy - 6, P['e4']); c.set(hx - 3 + i * 3, hy - 7, P['e3'])
    line(c, 46, 130, 58, 146, 'k2', 2)
    raven(c, 112, 70, .9)
    return finish(c)

def ar09():
    c = card(); sky(c, ['ink', 'n2', 'n3', 's1'], 160); stars(c, 28, 110, 55, 9)
    mountains(c, 168, 78, 'n2', 9, 3); mountains(c, 176, 55, 'y1', 10, 4)
    for x in range(0, W):   # snieg na szczytach
        for y in range(90, 176):
            if c.px[y][x] == P['y1'] and y < 130 and (x + y) % 3: c.set(x, y, P['s3'] if (x + y) % 2 else P['s4'])
        ramp(c, 0, 176, W, H, ['y1', 'n2', 'ink'])
    f = figure(c, 72, 180, 82, robe='y2', trim='y3', hood=True, face='ink', arms='down')
    poly(c, [(72 - 3, 100), (72 + 14, 118), (72 + 6, 180), (72 - 6, 180)], 'y3')  # plaszcz
    # laska
    rect(c, 50, 96, 3, 86, 'ink'); rect(c, 51, 96, 1, 86, 'b3'); disc(c, 51, 94, 3, 'g3')
    # latarnia
    lx, ly = 100, 112
    line(c, 80, 118, lx, ly - 6, 'y1', 2); glow(c, lx, ly, 34, 'o3', 1.5); glow(c, lx, ly, 18, 'o5', 1.3)
    rect(c, lx - 6, ly - 8, 12, 17, 'ink'); rect(c, lx - 4, ly - 6, 8, 13, 'o4'); rect(c, lx - 2, ly - 3, 4, 7, 'o5')
    poly(c, [(lx - 7, ly - 8), (lx + 7, ly - 8), (lx, ly - 15)], 'ink'); disc(c, lx, ly - 17, 2, 'g3')
    line(c, lx - 3, ly - 6, lx + 3, ly + 6, 'g3'); line(c, lx + 3, ly - 6, lx - 3, ly + 6, 'g3')
    raven(c, 14, 70, .9)
    return finish(c)

def ar10():
    c = card(); sky(c, ['ink', 'v1', 'n3', 'v2'], 170); stars(c, 26, 190, 50, 11)
    cx, cy = 72, 108
    glow(c, cx, cy, 70, 'o1', 2); glow(c, cx, cy, 44, 'o3', 2.4)
    for r, col in ((46, 'ink'), (44, 'g2'), (41, 'g3'), (38, 'ink'), (36, 'n3'), (20, 'ink'), (18, 'g2'), (12, 'g3')): disc(c, cx, cy, r, col)
    disc(c, cx, cy, 8, 'ink'); disc(c, cx, cy, 5, 'o4'); disc(c, cx, cy, 2, 'o5')
    for a in range(0, 360, 45):
        t = math.radians(a + 22)
        line(c, cx + 12 * math.cos(t), cy + 12 * math.sin(t), cx + 37 * math.cos(t), cy + 37 * math.sin(t), 'ink', 3)
        line(c, cx + 12 * math.cos(t), cy + 12 * math.sin(t), cx + 37 * math.cos(t), cy + 37 * math.sin(t), 'g3')
    for a in range(0, 360, 45):   # klejnoty na obreczy
        t = math.radians(a); disc(c, cx + 39.5 * math.cos(t), cy + 39.5 * math.sin(t), 2, 'r3' if a % 90 == 0 else 'o4')
    # sfinks na gorze, waz po lewej, szakal po prawej
    poly(c, [(60, 66), (84, 66), (84, 58), (78, 52), (70, 52), (64, 58)], 'ink'); poly(c, [(62, 65), (82, 65), (82, 59), (77, 54), (71, 54), (65, 59)], 'y3'); c.set(75, 56, P['o4'])
    poly(c, [(24, 130), (30, 118), (34, 124), (36, 140), (30, 146), (24, 142)], 'ink'); poly(c, [(26, 130), (30, 122), (32, 126), (33, 138), (29, 143), (26, 140)], 'r3'); c.set(30, 121, P['o5'])
    poly(c, [(112, 132), (118, 124), (122, 112), (126, 120), (124, 140), (114, 144)], 'ink'); poly(c, [(114, 134), (118, 128), (122, 118), (123, 138), (116, 141)], 'e3')
    # cztery rogi: znaki
    for x, y, col in ((18, 44, 'o4'), (126, 44, 't3'), (18, 176, 'e4'), (126, 176, 'r4')):
        glow(c, x, y, 12, 'v2', 1.5); disc(c, x, y, 5, 'ink'); disc(c, x, y, 4, 'v1'); disc(c, x, y, 2, col)
    raven(c, 100, 36, .8)
    return finish(c)

def ar11():
    c = card(); sky(c, ['ink', 'r1', 'n3', 'n2'], 170)
    rect(c, 0, 26, W, 150, 'ink'); rect(c, 4, 30, 136, 144, 'r1')
    for x in range(6, 140, 8): rect(c, x, 30, 2, 144, 'r2' if x % 16 == 6 else 'r1')   # kotara
    ramp(c, 4, 30, 140, 70, ['ink', 'r1'])
    pillar(c, 20, 40, 176, 12, 'y1', 'y2'); pillar(c, 112, 40, 176, 12, 'y1', 'y2')
    glow(c, 72, 96, 48, 'o2', 2.2)
    rect(c, 0, 176, W, 40, 'ink'); rect(c, 14, 174, 116, 4, 'y2')
    # tron
    rect(c, 46, 70, 52, 108, 'ink'); rect(c, 48, 72, 48, 104, 'b1'); rect(c, 48, 72, 48, 3, 'g2'); rect(c, 46, 70, 3, 108, 'g2'); rect(c, 95, 70, 3, 108, 'g2')
    # postac
    f = figure(c, 72, 176, 92, robe='r3', trim='g3', hood=False, arms='down', skin='k2')
    hx, hy = map(round, f['head']); crown(c, hx, hy - 5, 12, 3); rect(c, 66, 100, 12, 3, 'g3'); disc(c, 72, 103, 2, 'o5')
    # miecz w prawej, waga w lewej
    sword(c, 106, 92, 1.5)
    line(c, 80, 118, 100, 112, 'r3', 3)
    wx, wy = 32, 92
    glow(c, wx, wy, 22, 'o3', 2)
    rect(c, wx - 1, wy - 8, 3, 26, 'ink'); rect(c, wx, wy - 8, 1, 26, 'g3'); disc(c, wx, wy - 10, 2, 'g4'); line(c, wx - 12, wy - 2, wx + 12, wy - 2, 'g3', 1)
    for dx in (-12, 12):
        line(c, wx + dx, wy - 2, wx + dx - 5, wy + 12, 'g2'); line(c, wx + dx, wy - 2, wx + dx + 5, wy + 12, 'g2')
        poly(c, [(wx + dx - 7, wy + 12), (wx + dx + 7, wy + 12), (wx + dx + 4, wy + 16), (wx + dx - 4, wy + 16)], 'g3')
    line(c, 66, 120, 42, 118, 'r3', 3)
    raven(c, 16, 192, .01) if False else None
    return finish(c)

CARDS = {'ar06': ar06, 'ar07': ar07, 'ar08': ar08, 'ar09': ar09, 'ar10': ar10, 'ar11': ar11}
if __name__ == '__main__':
    from sheet import sheet
    sheet([f() for f in CARDS.values()], 'tools/deck/_majors_B.png', cols=6)
