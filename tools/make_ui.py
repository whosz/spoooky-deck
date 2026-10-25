"""python3 tools/make_ui.py: generates img/ui/* (9-slice frames, cursor, field icons) in the palette from STYLE.md."""
import sys; sys.path.insert(0, 'tools')
from pixel import Canvas, rgb
BG, S1, S2, GD, G, FL, MG, TX, BL = map(rgb, ['#0b0d17', '#161a2a', '#222842', '#8a6a2e', '#d8aa48', '#ffb347', '#f4efe6', '#e8dcc0', '#b3243a'])

def frame9(path, size, fill, accent):
    """9-slice frame: black outline, gold, an inner line and rivets in the corners; slice = 8."""
    c = Canvas(size, size, (0, 0, 0, 0))
    c.rect(2, 2, size - 4, size - 4, fill)
    c.frame(0, 0, size, size, (0, 0, 0, 0))
    for i, col in enumerate([BG, GD, accent, GD]):
        c.frame(i, i, size - 2 * i, size - 2 * i, col)
    for (x, y) in [(4, 4), (size - 6, 4), (4, size - 6), (size - 6, size - 6)]:
        c.rect(x, y, 2, 2, accent)
    # cut corners for a pixel-rounded look
    for (x, y) in [(0, 0), (size - 1, 0), (0, size - 1), (size - 1, size - 1)]: c.set(x, y, (0, 0, 0, 0))
    c.save(path)

frame9('img/ui/frame.png', 24, S1, G)
frame9('img/ui/btn.png', 24, FL, G)
frame9('img/ui/btn-alt.png', 24, S2, GD)

# cursor: a 12x12 arrow scaled x2 (24x24)
cur = Canvas(12, 12)
cur.art(0, 0, ["K...........", "KK..........", "KGK.........", "KGGK........", "KGGGK.......", "KGGGGK......", "KGGGGGK.....", "KGGGKKKK....", "KGKGK.......", "KK.KGK......", "K..KGK......", "....KK......"], {'K': BG, 'G': FL})
cur.scaled(2).save('img/ui/cursor.png')

# 16x16 field icons
def icon(path, rows, pal): c = Canvas(16, 16); c.art(0, 0, rows, pal); c.save(path)
icon('img/ui/ic-candle.png', ["................", ".......Y........", "......YOY.......", "......YOY.......", ".......O........", ".......K........", "......WWW.......", "......WWW.......", "......WWW.......", "......WWW.......", "......WWW.......", "......WWW.......", "....DDDDDDD.....", "....DGGGGGD.....", ".....DDDDD......", "................"], {'Y': FL, 'O': rgb('#ff7a2e'), 'K': BG, 'W': TX, 'D': GD, 'G': G})
icon('img/ui/ic-stars.png', ["................", "..Y.............", ".YYY.....Y......", "..Y.....YYY.....", "...M.....Y......", "....M...M.......", ".....M.M........", "......M...Y.....", "......M..YYY....", ".....M....Y.....", "....M...........", "...YM...........", "..YYY...........", "...Y............", "................", "................"], {'Y': G, 'M': GD})
icon('img/ui/ic-tower.png', ["................", "....B.B.B.B.....", "....BBBBBBB.....", "....BSSSSSB.....", "....BSWSSSB.....", "....BSSSSSB.....", "....BSSSSSB.....", "....BSSWSSB.....", "....BSSSSSB.....", "....BSSSSSB.....", "....BSDDSSB.....", "....BSDDSSB.....", "...BBBBBBBBB....", "...BGGGGGGGB....", "...BBBBBBBBB....", "................"], {'B': GD, 'S': S2, 'W': FL, 'D': BG, 'G': G})
print('ok')

# picture frame for the phone window on desktop: 36x36, slice 12, displayed at 2x (24 px)
def picture_frame(path):
    n = 36; c = Canvas(n, n)
    layers = [BG, GD, GD, G, G, GD, BG, S2, S2, GD, BG]
    for i, col in enumerate(layers): c.frame(i, i, n - 2 * i, n - 2 * i, col)
    for (cx, cy) in [(6, 6), (n - 7, 6), (6, n - 7), (n - 7, n - 7)]:   # diamonds in the corners
        for dy in range(-4, 5):
            for dx in range(-4, 5):
                if abs(dx) + abs(dy) <= 4: c.set(cx + dx, cy + dy, BG if abs(dx) + abs(dy) == 4 else (G if abs(dx) + abs(dy) >= 2 else FL))
    c.save(path)
picture_frame('img/ui/picture-frame.png')

# shine band on the card: pixel, with stepped edges and dither on the rim (moved in CSS)
def shine(path):
    W_, H_ = 216, 108; c = Canvas(W_, H_)
    for y in range(H_):
        for x in range(W_):
            d = abs(x - (108 - (y - 54) * .6))
            a = 0
            if d < 4: a = 70
            elif d < 12: a = 38
            elif d < 15 and BAYER[y % 4][x % 4] < 8 * (15 - d) / 3: a = 38
            if a: c.set(x, y, (255, 255, 255, a))
    c.save(path)
BAYER = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]
shine('img/ui/shine.png')

# emblem above the intro title: a crescent with a star and rays (32x32)
def emblem(path):
    import math
    c = Canvas(32, 32)
    for i in range(24):
        a = i * math.pi / 12; r0, r1 = 12, 15 if i % 2 else 13
        c.line(round(16 + r0 * math.cos(a)), round(16 + r0 * math.sin(a)), round(16 + r1 * math.cos(a)), round(16 + r1 * math.sin(a)), G)
    c.ellipse(16, 16, 9, 9, TX, True); c.ellipse(19, 14, 8, 8, rgb('#0b0d17'), True)
    for d in range(-2, 3): c.set(21 + d, 16, FL); c.set(21, 16 + d, FL)
    c.set(21, 16, rgb('#ffffff'))
    c.save(path)
emblem('img/ui/emblem.png')


# card front frame (64x96 grid, overlay): dark outline, gold line, gap, thin inner gold line, decorative corners
def cardframe(path):
    W_, H_ = 64, 96
    DK, G1, G2, G3 = rgb('#0b0d17'), rgb('#d8aa48'), rgb('#8a6a2e'), rgb('#f0d27a')
    c = Canvas(W_, H_)
    c.frame(0, 0, W_, H_, DK); c.frame(1, 1, W_ - 2, H_ - 2, G1); c.frame(2, 2, W_ - 4, H_ - 4, DK); c.frame(3, 3, W_ - 6, H_ - 6, G2)
    # corners: gold "steps" joining the lines
    for (x, y, sx, sy) in [(0, 0, 1, 1), (W_ - 1, 0, -1, 1), (0, H_ - 1, 1, -1), (W_ - 1, H_ - 1, -1, -1)]:
        for dx in range(1, 6): c.set(x + sx * dx, y + sy * 3, G3 if dx < 4 else G1)
        for dy in range(1, 6): c.set(x + sx * 3, y + sy * dy, G3 if dy < 4 else G1)
        c.set(x + sx * 1, y + sy * 1, G3); c.set(x + sx * 2, y + sy * 2, G3)
    # central flourishes on the edges (small diamonds)
    for (x, y) in [(W_ // 2 - 1, 1), (W_ // 2, 1), (W_ // 2 - 1, H_ - 2), (W_ // 2, H_ - 2)]: c.set(x, y, G3)
    for (x, y) in [(1, H_ // 2 - 1), (1, H_ // 2), (W_ - 2, H_ // 2 - 1), (W_ - 2, H_ // 2)]: c.set(x, y, G3)
    c.save(path)
cardframe('img/ui/cardframe.png')
