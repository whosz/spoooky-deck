"""python3 tools/make_back.py: card back (36x54) and the intro image (hero) in the palette from STYLE.md."""
import sys; sys.path.insert(0, 'tools')
from pixel import Canvas, rgb
BG, S1, S2, GD, G, FL, TX = map(rgb, ['#0b0d17', '#161a2a', '#222842', '#8a6a2e', '#d8aa48', '#ffb347', '#e8dcc0'])

def back():
    c = Canvas(36, 54)
    c.rect(0, 0, 36, 54, BG); c.rect(1, 1, 34, 52, GD); c.rect(2, 2, 32, 50, S1)
    c.frame(3, 3, 30, 48, GD)
    for (x, y) in [(5, 5), (30, 5), (5, 48), (30, 48)]: c.rect(x, y, 1, 1, G)
    for y in range(6, 48, 2):                      # subtle background stripes
        for x in range(6, 30): c.set(x, y, S2) if (x + y) % 4 == 0 else None
    c.ellipse(18, 27, 9, 19, GD, False); c.ellipse(18, 27, 8, 18, S1, True); c.ellipse(18, 27, 8.4, 18.4, GD, False)
    # moon (top)
    c.ellipse(18, 13, 4, 4, G, True); c.ellipse(20, 12, 3.5, 3.5, S1, True)
    # eye (middle)
    c.ellipse(18, 27, 6, 3, G, False); c.ellipse(18, 27, 2, 2, FL, True); c.set(18, 27, BG)
    # sun (bottom)
    c.ellipse(18, 41, 3, 3, G, True); c.ellipse(18, 41, 1.5, 1.5, FL, True)
    for (x, y) in [(18, 36), (18, 46), (13, 41), (23, 41)]: c.set(x, y, G)
    return c

def hero():
    c = Canvas(160, 112)
    cx, cy = 80, 60
    import math
    for i in range(48):                            # rays
        a = i * math.pi * 2 / 48; r0, r1 = 26, 60 if i % 2 else 48
        c.line(round(cx + r0 * math.cos(a)), round(cy + r0 * math.sin(a)), round(cx + r1 * math.cos(a)), round(cy + r1 * math.sin(a)), GD)
    b = back()
    for deg, dx, dy in [(-22, -30, 6), (18, 30, 2), (-3, 0, -4)]:
        r = b.rotated(deg, 56, 70); c.paste(r, cx - 28 + dx, cy - 35 + dy)
    for (x, y) in [(18, 22), (142, 30), (30, 92), (130, 94), (80, 8)]:      # sparks
        c.set(x, y, FL); c.set(x - 1, y, G); c.set(x + 1, y, G); c.set(x, y - 1, G); c.set(x, y + 1, G)
    return c

back().save('img/ui/back.png'); hero().save('img/ui/hero.png'); print('ok')
