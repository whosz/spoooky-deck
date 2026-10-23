"""python3 tools/make_ui.py: generuje img/ui/* (ramki 9-slice, kursor, ikony pol) w palecie z STYLE.md."""
import sys; sys.path.insert(0, 'tools')
from pixel import Canvas, rgb
BG, S1, S2, GD, G, FL, MG, TX, BL = map(rgb, ['#0b0d17', '#161a2a', '#222842', '#8a6a2e', '#d8aa48', '#ffb347', '#b794f6', '#e8dcc0', '#b3243a'])

def frame9(path, size, fill, accent):
    """Ramka 9-slice: czarny kontur, zloto, wewnetrzna linia i nity w rogach; slice = 8."""
    c = Canvas(size, size, (0, 0, 0, 0))
    c.rect(2, 2, size - 4, size - 4, fill)
    c.frame(0, 0, size, size, (0, 0, 0, 0))
    for i, col in enumerate([BG, GD, accent, GD]):
        c.frame(i, i, size - 2 * i, size - 2 * i, col)
    for (x, y) in [(4, 4), (size - 6, 4), (4, size - 6), (size - 6, size - 6)]:
        c.rect(x, y, 2, 2, accent)
    # scieta narozniki dla wrazenia pikselowego zaokraglenia
    for (x, y) in [(0, 0), (size - 1, 0), (0, size - 1), (size - 1, size - 1)]: c.set(x, y, (0, 0, 0, 0))
    c.save(path)

frame9('img/ui/frame.png', 24, S1, G)
frame9('img/ui/btn.png', 24, FL, G)
frame9('img/ui/btn-alt.png', 24, S2, GD)
frame9('img/ui/btn-magic.png', 24, MG, G)

# kursor: strzalka 12x12 skalowana x2 (24x24)
cur = Canvas(12, 12)
cur.art(0, 0, ["K...........", "KK..........", "KGK.........", "KGGK........", "KGGGK.......", "KGGGGK......", "KGGGGGK.....", "KGGGKKKK....", "KGKGK.......", "KK.KGK......", "K..KGK......", "....KK......"], {'K': BG, 'G': FL})
cur.scaled(2).save('img/ui/cursor.png')

# ikony pol 16x16
def icon(path, rows, pal): c = Canvas(16, 16); c.art(0, 0, rows, pal); c.save(path)
icon('img/ui/ic-candle.png', ["................", ".......Y........", "......YOY.......", "......YOY.......", ".......O........", ".......K........", "......WWW.......", "......WWW.......", "......WWW.......", "......WWW.......", "......WWW.......", "......WWW.......", "....DDDDDDD.....", "....DGGGGGD.....", ".....DDDDD......", "................"], {'Y': FL, 'O': rgb('#ff7a2e'), 'K': BG, 'W': TX, 'D': GD, 'G': G})
icon('img/ui/ic-stars.png', ["................", "..Y.............", ".YYY.....Y......", "..Y.....YYY.....", "...M.....Y......", "....M...M.......", ".....M.M........", "......M...Y.....", "......M..YYY....", ".....M....Y.....", "....M...........", "...YM...........", "..YYY...........", "...Y............", "................", "................"], {'Y': G, 'M': GD})
icon('img/ui/ic-tower.png', ["................", "....B.B.B.B.....", "....BBBBBBB.....", "....BSSSSSB.....", "....BSWSSSB.....", "....BSSSSSB.....", "....BSSSSSB.....", "....BSSWSSB.....", "....BSSSSSB.....", "....BSSSSSB.....", "....BSDDSSB.....", "....BSDDSSB.....", "...BBBBBBBBB....", "...BGGGGGGGB....", "...BBBBBBBBB....", "................"], {'B': GD, 'S': S2, 'W': FL, 'D': BG, 'G': G})
print('ok')

# ramka obrazu dla okna telefonu na desktopie: 36x36, slice 12, wyswietlana 2x (24 px)
def picture_frame(path):
    n = 36; c = Canvas(n, n)
    layers = [BG, GD, GD, G, G, GD, BG, S2, S2, GD, BG]
    for i, col in enumerate(layers): c.frame(i, i, n - 2 * i, n - 2 * i, col)
    for (cx, cy) in [(6, 6), (n - 7, 6), (6, n - 7), (n - 7, n - 7)]:   # romby w rogach
        for dy in range(-4, 5):
            for dx in range(-4, 5):
                if abs(dx) + abs(dy) <= 4: c.set(cx + dx, cy + dy, BG if abs(dx) + abs(dy) == 4 else (G if abs(dx) + abs(dy) >= 2 else FL))
    c.save(path)
picture_frame('img/ui/picture-frame.png')
