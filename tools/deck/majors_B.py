"""Major arcana B: ar06 The Lovers, ar07 The Chariot, ar08 Strength, ar09 The Hermit, ar10 Wheel of Fortune, ar11 Justice."""
import sys; sys.path.insert(0, 'tools/deck'); sys.path.insert(0, 'tools')
from lib import *

def sky(c, names, y1=170): ramp(c, 0, 0, W, y1, names)

def ground(c, y, a, b, seed=3):
    hills(c, y, 5, a, seed, .08); ramp(c, 0, y + 10, W, H, [a, b, 'ink'])

def pillar(c, x, y0, y1, w=10, body='y1', hi='y2'):
    rect(c, x - 1, y0, w + 2, y1 - y0, 'ink'); rect(c, x, y0, w, y1 - y0, body); rect(c, x, y0, 2, y1 - y0, hi)
    rect(c, x - 3, y0, w + 6, 3, hi); rect(c, x - 3, y1 - 3, w + 6, 3, hi)

def part(c, shapes, col, o='ink'):
    """Shapes ('e',cx,cy,rx,ry) / ('r',x,y,w,h) with a 1 px outline."""
    for g, cc in ((1, o), (0, col)):
        for s in shapes:
            if s[0] == 'e': c.ellipse(s[1], s[2], s[3] + g, s[4] + g, P[cc], True)
            else: c.rect(round(s[1] - g), round(s[2] - g), round(s[3] + 2 * g), round(s[4] + 2 * g), P[cc])

def sphinx(c, x, y, d, col, hi):
    def R(u, v, w, h): return ('r', min(x + d * u, x + d * (u + w)), y + v, abs(w), h)
    def E(u, v, rx, ry): return ('e', x + d * u, y + v, rx, ry)
    line(c, x - d * 18, y - 6, x - d * 23, y - 14, 'ink', 3); line(c, x - d * 18, y - 6, x - d * 23, y - 14, col, 1)
    part(c, [E(-3, -8, 16, 8), E(-12, -8, 8, 8), E(8, -12, 5, 9)], col)
    part(c, [R(6, -5, 15, 5), R(-14, -3, 12, 3)], col)
    for u in (11, 16): c.set(round(x + d * u), round(y - 2), P['ink'])
    for k in range(10): c.set(round(x - d * (12 - k * 2)), round(y - 16 + (k * 4) // 10 * 0), P[hi]) if k < 6 else None
    for i in range(8): c.set(round(x + d * (-10 + i * 2)), round(y - 16 + (1 if i < 2 else 0)), P[hi])
    part(c, [R(3, -22, 4, 10)], 'g3'); part(c, [E(9, -25, 6, 7)], 'g3'); part(c, [E(11, -25, 3, 4)], 'k1')
    for k in range(3): c.set(round(x + d * 4), y - 21 + k * 3, P['g2'])
    c.set(round(x + d * 12), y - 26, P['o4']); c.set(round(x + d * 13), y - 23, P['r3'])

def lion(c):
    for dx, dy in ((0, 0),):
        part(c, [('r', 77, 150, 6, 22), ('r', 86, 152, 5, 20)], 'o2')   # front paws
        part(c, [('r', 113, 156, 7, 16), ('r', 123, 158, 6, 14)], 'o1')
        part(c, [('e', 80, 172, 5, 2), ('e', 88, 172, 5, 2), ('e', 116, 172, 5, 2), ('e', 126, 172, 5, 2)], 'o3')
    line(c, 130, 144, 138, 138, 'ink', 4); line(c, 130, 144, 138, 138, 'o2', 2); line(c, 138, 138, 138, 128, 'ink', 4); line(c, 138, 138, 138, 128, 'o2', 2)
    part(c, [('e', 138, 124, 3, 4)], 'o1')
    part(c, [('e', 102, 142, 26, 12), ('e', 118, 148, 12, 11), ('e', 82, 144, 12, 12)], 'o2')
    part(c, [('e', 102, 150, 22, 5)], 'o1')                              # belly shadow
    for x in range(78, 128, 2): c.set(x, 131 + (x // 2) % 2, P['o3'])      # light on the back
    for y in (142, 148, 154): line(c, 112, y, 122, y + 2, 'o1')
    # mane: a serrated disc
    mx, my = 66, 136
    for a in range(0, 360, 20):
        t = math.radians(a); line(c, mx, my, mx + 22 * math.cos(t), my + 21 * math.sin(t), 'ink', 4)
    disc(c, mx, my, 19, 'ink')
    for a in range(0, 360, 20):
        t = math.radians(a); line(c, mx, my, mx + 21 * math.cos(t), my + 20 * math.sin(t), 'o1', 2)
    disc(c, mx, my, 17, 'o1'); disc(c, mx - 1, my - 1, 14, 'o2')
    for a in range(0, 360, 24):
        t = math.radians(a); line(c, mx + 8 * math.cos(t), my + 8 * math.sin(t), mx + 16 * math.cos(t), my + 15 * math.sin(t), 'o3')
    part(c, [('e', 62, 138, 11, 10)], 'o3')                               # face
    part(c, [('e', 54, 143, 7, 5)], 'o4')                                 # muzzle
    part(c, [('e', 62, 124, 3, 3), ('e', 72, 125, 3, 3)], 'o2')           # ears
    rect(c, 49, 139, 4, 3, 'r1'); c.set(50, 139, P['r4'])                 # nose
    rect(c, 51, 145, 8, 1, 'ink'); rect(c, 52, 146, 6, 2, 'r2'); c.set(53, 146, P['white']); c.set(57, 146, P['white'])
    rect(c, 56, 133, 5, 2, 'ink'); rect(c, 63, 133, 5, 2, 'ink')           # eyebrows
    rect(c, 57, 135, 3, 2, 'o5'); rect(c, 64, 135, 3, 2, 'o5'); c.set(57, 136, P['ink']); c.set(64, 136, P['ink'])

def ar06():
    c = card(); sky(c, ['n1', 'v1', 'r1', 'r2'], 160); stars(c, 28, 80, 24, 6)
    mountains(c, 150, 55, 'n2', 6, 3); ground(c, 156, 'e1', 'ink', 6)
    glow(c, 72, 58, 46, 'o4', 1.8); glow(c, 72, 58, 24, 'o5', 1.4)
    for s in (-1, 1):   # angel's wings
        poly(c, [(72, 54), (72 + s * 44, 38), (72 + s * 36, 62), (72 + s * 26, 66), (72, 66)], 'ink')
        poly(c, [(72, 55), (72 + s * 41, 41), (72 + s * 33, 61), (72 + s * 24, 64), (72, 64)], 'g3')
        for k in range(4): line(c, 72 + s * 10, 56 + k * 2, 72 + s * (38 - k * 3), 44 + k * 5, 'g4')
    rect(c, 66, 100, 12, 60, 'ink')  # mountain between them
    poly(c, [(60, 156), (72, 108), (84, 156)], 'n3'); poly(c, [(66, 156), (72, 118), (78, 156)], 'n4')
    for x, col in ((12, 'e2'), (128, 'r3')):   # trees: fiery and rotten
        rect(c, x, 110, 3, 50, 'b1'); disc(c, x + 1, 108, 10, 'ink'); disc(c, x + 1, 108, 8, col); disc(c, x - 2, 105, 3, 'e3' if col == 'e2' else 'o3')
    raven(c, 20, 52); raven(c, 112, 66, .8)
    person(c, 72, 92, 46, robe='r3', trim='o4', skin='k2', hair='o3', lh=(-20, -8), rh=(20, -8), belt=False)   # angel
    person(c, 34, 178, 94, robe='n4', trim='s3', skin='k1', hair='b2', lh=(-4, 30), rh=(12, 14))              # man
    person(c, 110, 178, 94, robe='r2', trim='r4', skin='k2', hair='o2', lh=(-12, 14), rh=(4, 30))             # woman
    return finish(c)

def ar07():
    c = card(); sky(c, ['ink', 'n2', 'n3', 'v1'], 150); stars(c, 28, 100, 40, 7)
    glow(c, 72, 84, 50, 'o1', 2)
    for x, y, w, h in ((8, 100, 18, 60), (118, 96, 18, 64), (30, 120, 12, 40)): tower(c, x, y, w, h, 'y1', 'r2')
    rect(c, 0, 158, W, 8, 'n2'); ground(c, 165, 'n3', 'ink', 7)
    # canopy
    for x in (40, 100): rect(c, x, 60, 4, 72, 'ink'); rect(c, x + 1, 60, 2, 72, 'g2')
    rect(c, 36, 50, 72, 12, 'ink'); rect(c, 38, 52, 68, 8, 'n4')
    for i in range(7): c.set(44 + i * 9, 56, P['o5']); c.set(43 + i * 9, 56, P['g4'])
    poly(c, [(36, 62), (108, 62), (102, 70), (42, 70)], 'ink')
    glow(c, 72, 102, 16, 'o3', 2.2)
    f = person(c, 72, 140, 66, robe='r3', trim='g3', skin='k2', hair='b2', beard=True, hat='crown3', lh=(-14, 12), rh=(16, -4))
    hx, hy = f['hand_r']; line(c, hx, hy - 14, hx, hy + 8, 'ink', 3); line(c, hx, hy - 14, hx, hy + 8, 'g3'); disc(c, hx, hy - 16, 2, 'o5'); disc(c, hx, hy, 2, 'k2')
    # chariot (the front covers the lower body)
    rect(c, 36, 130, 72, 30, 'ink'); rect(c, 38, 132, 68, 26, 'n4'); rect(c, 38, 132, 68, 3, 'g3')
    for x in range(42, 104, 8): rect(c, x, 140, 4, 12, 'n3')
    disc(c, 72, 146, 8, 'ink'); disc(c, 72, 146, 6, 'g3'); disc(c, 72, 146, 2, 'g1')
    for x in (38, 102):  # wheels
        disc(c, x, 162, 9, 'ink'); disc(c, x, 162, 7, 'g2'); disc(c, x, 162, 4, 'ink')
        for a in range(0, 180, 45): line(c, x + 7 * math.cos(math.radians(a)), 162 + 7 * math.sin(math.radians(a)), x - 7 * math.cos(math.radians(a)), 162 - 7 * math.sin(math.radians(a)), 'g3')
    sphinx(c, 30, 192, 1, 'y2', 'y3'); sphinx(c, 114, 192, -1, 'y3', 'white')
    raven(c, 14, 40); raven(c, 120, 36, .8)
    return finish(c)

def ar08():
    c = card(); sky(c, ['n1', 'e1', 'e2', 'n3'], 150); stars(c, 28, 70, 20, 8)
    mountains(c, 140, 40, 'e1', 8, 4); ground(c, 150, 'e1', 'ink', 8)
    glow(c, 38, 82, 30, 'o4', 2); glow(c, 90, 150, 40, 'r1', 2)
    for dx in (-8, 8): c.ellipse(38 + dx, 40, 8, 5, P['o5']); c.ellipse(38 + dx, 40, 6, 3, P['o4'])   # infinity
    lion(c)
    f = person(c, 30, 172, 100, robe='y3', trim='e4', skin='k2', hair='b1', lh=(-12, 14), rh=(14, 40))
    hx, hy = f['head']
    for i in range(5): c.set(hx - 5 + i * 2, hy - 8, P['e4']); c.set(hx - 4 + i * 2, hy - 9, P['o4'] if i % 2 else P['e3'])   # wreath
    raven(c, 112, 70, .9)
    return finish(c)

def ar09():
    c = card(); sky(c, ['ink', 'n2', 'n3', 's1'], 160); stars(c, 28, 110, 55, 9)
    mountains(c, 168, 78, 'n2', 9, 3); mountains(c, 176, 55, 'y1', 10, 4)
    for x in range(0, W):   # snow on the peaks
        for y in range(90, 176):
            if c.px[y][x] == P['y1'] and y < 130 and (x + y) % 3: c.set(x, y, P['s3'] if (x + y) % 2 else P['s4'])
    ramp(c, 0, 176, W, H, ['y1', 'n2', 'ink'])
    lx, ly = 106, 128
    glow(c, lx, ly, 40, 'o2', 1.5); glow(c, lx, ly, 22, 'o4', 1.4); glow(c, lx, ly, 10, 'o5', 1.2)
    f = person(c, 68, 184, 120, robe='s2', trim='y3', hood=True, lh=(-8, 24), rh=(24, 34), belt=True)
    x0, y0 = f['hand_l']; hx, hy = f['head']
    rect(c, x0 - 2, y0 - 66, 4, 130, 'ink'); rect(c, x0 - 1, y0 - 66, 2, 130, 'b3'); disc(c, x0, y0 - 68, 3, 'g3')   # staff
    disc(c, x0, y0, 2, 'k1')
    poly(c, [(hx - 7, hy + 8), (hx + 7, hy + 8), (hx + 3, hy + 26), (hx - 3, hy + 26)], 'y3')                       # beard
    x1, y1 = f['hand_r']                                                                                            # lantern
    ly = y1 + 14; lx = x1
    line(c, lx, y1, lx, ly - 8, 'g2')
    rect(c, lx - 6, ly - 8, 12, 17, 'ink'); rect(c, lx - 4, ly - 6, 8, 13, 'o4'); rect(c, lx - 2, ly - 3, 4, 7, 'o5')
    poly(c, [(lx - 7, ly - 8), (lx + 7, ly - 8), (lx, ly - 15)], 'ink'); disc(c, lx, ly - 17, 2, 'g3')
    line(c, lx - 3, ly - 6, lx + 3, ly + 6, 'g3'); line(c, lx + 3, ly - 6, lx - 3, ly + 6, 'g3')
    disc(c, x1, y1, 2, 'k1')
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
    for a in range(0, 360, 45):   # gems on the rim
        t = math.radians(a); disc(c, cx + 39.5 * math.cos(t), cy + 39.5 * math.sin(t), 2, 'r3' if a % 90 == 0 else 'o4')
    # sphinx on top, snake on the left, jackal on the right
    poly(c, [(60, 66), (84, 66), (84, 58), (78, 52), (70, 52), (64, 58)], 'ink'); poly(c, [(62, 65), (82, 65), (82, 59), (77, 54), (71, 54), (65, 59)], 'y3'); c.set(75, 56, P['o4'])
    poly(c, [(24, 130), (30, 118), (34, 124), (36, 140), (30, 146), (24, 142)], 'ink'); poly(c, [(26, 130), (30, 122), (32, 126), (33, 138), (29, 143), (26, 140)], 'r3'); c.set(30, 121, P['o5'])
    poly(c, [(112, 132), (118, 124), (122, 112), (126, 120), (124, 140), (114, 144)], 'ink'); poly(c, [(114, 134), (118, 128), (122, 118), (123, 138), (116, 141)], 'e3')
    # four corners: signs
    for x, y, col in ((18, 44, 'o4'), (126, 44, 't3'), (18, 176, 'e4'), (126, 176, 'r4')):
        glow(c, x, y, 12, 'v2', 1.5); disc(c, x, y, 5, 'ink'); disc(c, x, y, 4, 'v1'); disc(c, x, y, 2, col)
    raven(c, 100, 36, .8)
    return finish(c)


def ar11():
    c = card(); sky(c, ['ink', 'r1', 'n3', 'n2'], 170)
    rect(c, 0, 26, W, 150, 'ink'); rect(c, 4, 30, 136, 144, 'r1')
    for x in range(6, 140, 8): rect(c, x, 30, 2, 144, 'r2' if x % 16 == 6 else 'r1')   # curtain
    ramp(c, 4, 30, 140, 70, ['ink', 'r1'])
    pillar(c, 20, 40, 176, 12, 'y1', 'y2'); pillar(c, 112, 40, 176, 12, 'y1', 'y2')
    glow(c, 72, 96, 48, 'o2', 2.2)
    rect(c, 0, 176, W, 40, 'ink'); rect(c, 14, 174, 116, 4, 'y2')
    rect(c, 46, 70, 52, 108, 'ink'); rect(c, 48, 72, 48, 104, 'b1'); rect(c, 48, 72, 48, 3, 'g2'); rect(c, 46, 70, 3, 108, 'g2'); rect(c, 95, 70, 3, 108, 'g2')   # tron
    glow(c, 34, 96, 22, 'o3', 2)
    f = person(c, 72, 176, 112, robe='r3', trim='g3', skin='k2', hair='b2', hat='crown3', lh=(-24, 6), rh=(22, 6))
    x, y = f['hand_r']; sword(c, x, y - 18, 1.4); disc(c, x, y, 2, 'k2')
    wx, wy = f['hand_l']; by = wy - 16
    rect(c, wx - 1, by - 8, 3, 28, 'ink'); rect(c, wx, by - 8, 1, 28, 'g3'); disc(c, wx, by - 10, 2, 'g4'); line(c, wx - 13, by, wx + 13, by, 'g3', 1)
    for dx in (-13, 13):
        line(c, wx + dx, by, wx + dx - 5, by + 14, 'g2'); line(c, wx + dx, by, wx + dx + 5, by + 14, 'g2')
        poly(c, [(wx + dx - 7, by + 14), (wx + dx + 7, by + 14), (wx + dx + 4, by + 18), (wx + dx - 4, by + 18)], 'g3')
    disc(c, wx, wy, 2, 'k2')
    return finish(c)

CARDS = {'ar06': ar06, 'ar07': ar07, 'ar08': ar08, 'ar09': ar09, 'ar10': ar10, 'ar11': ar11}
if __name__ == '__main__':
    from sheet import sheet
    sheet([f() for f in CARDS.values()], 'tools/deck/_majors_B.png', cols=6)
