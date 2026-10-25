"""python3 tools/make_icons.py: PWA icons (192, 512, maskable 512, apple-touch 180) from the card back."""
import sys; sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/deck')
from pixel import Canvas, rgb
import make_back  # noqa: F401 (generates the card back as a side effect of the import, harmless)
from make_back import back, BG, GD, G, FL, S1
def icon(maskable):
    c = Canvas(64, 64, rgb('#0b0d17'))
    if not maskable:
        c.frame(0, 0, 64, 64, GD); c.frame(1, 1, 62, 62, G); c.frame(2, 2, 60, 60, GD)
    for r in range(26, 0, -1):               # soft glow behind the card (steps)
        col = rgb('#ffb347', 18) if r > 14 else rgb('#ffb347', 30)
        c.ellipse(32, 32, r + 4, r + 8, col, True) if False else None
    c.paste(back().rotated(0, 40, 60), 12, 2)
    return c
for name, k, m in (('icon-192', 3, False), ('icon-512', 8, False), ('icon-maskable-512', 8, True), ('apple-touch-icon', 3, False)):
    icon(m).scaled(k).save(f'img/icons/{name}.png')
print('ok')
