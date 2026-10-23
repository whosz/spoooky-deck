"""Styl 'płaski 16-bit' (jak All Pixel Tarot Cards): kanwa 48x72, ~10 płaskich kolorów, gruby czarny obrys,
bez ditheringu i poświat. Karty renderujemy w 48x72 i skalujemy w CSS całkowitą krotnością (pixelated)."""
import sys, math
sys.path.insert(0, 'tools')
from pixel import Canvas, rgb

W, H = 48, 72
K, WH, L, M, C, R, B, N, Y, D = (rgb(h) for h in ['#000000', '#ffffff', '#d0d0d0', '#808890', '#ffd890', '#8c0a0a', '#3b5aa0', '#5a9a64', '#e8b030', '#2a2a2a'])
PAL = dict(K=K, W=WH, L=L, M=M, C=C, R=R, B=B, N=N, Y=Y, D=D)
CLEAR = (0, 0, 0, 0)

def card(bg=C):
    c = Canvas(W, H, bg); c.frame(0, 0, W, H, K); return c

def layer(): return Canvas(W, H, CLEAR)

def rect(c, x, y, w, h, col): c.rect(round(x), round(y), round(w), round(h), col)
def ell(c, cx, cy, rx, ry, col, fill=True): c.ellipse(cx, cy, rx, ry, col, fill)
def line(c, x0, y0, x1, y1, col, t=1):
    for k in range(t): c.line(round(x0) + k, round(y0), round(x1) + k, round(y1), col)

def poly(c, pts, col):
    ys = [p[1] for p in pts]
    for y in range(int(min(ys)), int(max(ys)) + 1):
        xs = []
        for i in range(len(pts)):
            (x0, y0), (x1, y1) = pts[i], pts[(i + 1) % len(pts)]
            if (y0 <= y < y1) or (y1 <= y < y0): xs.append(x0 + (y - y0) * (x1 - x0) / (y1 - y0))
        xs.sort()
        for a, b in zip(xs[::2], xs[1::2]):
            for x in range(round(a), round(b) + 1): c.set(x, y, col)

def sprite(c, x, y, rows, flip=False, pal=None):
    """rows: napisy, '.' = przezroczyste; znaki wg PAL (K,W,L,M,C,R,B,N,Y,D)."""
    p = pal or PAL
    for j, row in enumerate(rows):
        for i, ch in enumerate(row[::-1] if flip else row):
            if ch != '.': c.set(x + i, y + j, p[ch])

def outline_to(c, lay, col=K):
    """Składa warstwę na kartę z 1 px czarnym obrysem (4-sąsiedztwo)."""
    for y in range(lay.h):
        for x in range(lay.w):
            if lay.px[y][x][3]: continue
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < lay.w and 0 <= ny < lay.h and lay.px[ny][nx][3]: c.set(x, y, col); break
    c.paste(lay, 0, 0)

# ---- tło / krajobraz ----
def star4(c, x, y, r=2, col=WH):
    for d in range(-r, r + 1): c.set(x + d, y, col); c.set(x, y + d, col)
def sun(c, x, y, r=5, col=Y, ray=K):
    for i in range(16):
        a = i * math.pi / 8; l = r + (4 if i % 2 == 0 else 2)
        line(c, x + (r + 1) * math.cos(a), y + (r + 1) * math.sin(a), x + l * math.cos(a), y + l * math.sin(a), ray)
    ell(c, x, y, r + 1, r + 1, K); ell(c, x, y, r, r, col)
def cloud(c, x, y, w=14, col=WH):
    ell(c, x, y, w / 2, 3, K); ell(c, x - w / 4, y - 2, w / 4, 3, K); ell(c, x + w / 5, y - 3, w / 4, 3, K)
    ell(c, x, y, w / 2 - 1, 2, col); ell(c, x - w / 4, y - 2, w / 4 - 1, 2, col); ell(c, x + w / 5, y - 3, w / 4 - 1, 2, col)
def mountain(c, x, base, w, h, col=B, snow=True):
    poly(c, [(x - w / 2 - 1, base), (x, base - h - 1), (x + w / 2 + 1, base)], K)
    poly(c, [(x - w / 2, base), (x, base - h), (x + w / 2, base)], col)
    if snow: poly(c, [(x - w / 6, base - h * .65), (x, base - h), (x + w / 6, base - h * .65), (x + w / 12, base - h * .5), (x, base - h * .62), (x - w / 12, base - h * .5)], WH)
def tree(c, x, base, h=14, col=N):
    rect(c, x - 1, base - 5, 2, 5, K); ell(c, x, base - h + 5, 4, 6, K); ell(c, x, base - h + 5, 3, 5, col)
def ground(c, y, col=N, edge=K):
    rect(c, 1, y, W - 2, H - y - 1, edge); rect(c, 1, y + 1, W - 2, H - y - 2, col)
def stripes(c, x0, x1, y0, y1, a, b, w=2):
    for x in range(x0, x1):
        rect(c, x, y0, 1, y1 - y0, a if ((x - x0) // w) % 2 == 0 else b)
def checker(c, x0, y0, x1, y1, a, b, s=2):
    for y in range(y0, y1):
        for x in range(x0, x1): c.set(x, y, a if ((x - x0) // s + (y - y0) // s) % 2 == 0 else b)
def pillar(c, x, y0, y1, w=5, col=L):
    rect(c, x - 1, y0, w + 2, y1 - y0, K); rect(c, x, y0, w, y1 - y0, col); rect(c, x + w - 1, y0, 1, y1 - y0, M)
def arch(c, cx, y0, w, h, col=B):
    rect(c, cx - w / 2 - 1, y0 + h / 2, w + 2, h / 2 + 1, K); ell(c, cx, y0 + h / 2, w / 2 + 1, h / 2 + 1, K)
    rect(c, cx - w / 2, y0 + h / 2, w, h / 2, col); ell(c, cx, y0 + h / 2, w / 2, h / 2, col)

FONT = {'I': ['###', '.#.', '.#.', '.#.', '###'], 'V': ['#.#', '#.#', '#.#', '#.#', '.#.'], 'X': ['#.#', '#.#', '.#.', '#.#', '#.#']}
def numeral(c, text, y=3, col=K):
    """Rzymska liczba (I, V, X) wyśrodkowana u góry."""
    w = len(text) * 4 - 1; x0 = (W - w) // 2
    for k, ch in enumerate(text):
        for j, row in enumerate(FONT[ch]):
            for i, px in enumerate(row):
                if px == '#': c.set(x0 + k * 4 + i, y + j, col)

# ---- symbole kolorów ----
def pentacle(c, x, y, r=5):
    ell(c, x, y, r + 1, r + 1, K); ell(c, x, y, r, r, C)
    pts = [(x + (r - 1.5) * math.sin(i * 4 * math.pi / 5), y - (r - 1.5) * math.cos(i * 4 * math.pi / 5)) for i in range(6)]
    for a, b in zip(pts, pts[1:]): c.line(round(a[0]), round(a[1]), round(b[0]), round(b[1]), K)
def cup(c, x, y, s=1):
    rows = ["KKKKKKK", "KCCCCCK", "KCWCCCK", ".KCCCK.", "..KCK..", "..KCK..", ".KKKKK."]
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            if ch != '.': rect(c, x - 3 * s + i * s, y - 3 * s + j * s, s, s, PAL[ch])
def sword(c, x, y, ln=16, up=True):
    top = y - ln if up else y
    rect(c, x - 2, top - (1 if up else 0), 5, ln + 4, K); rect(c, x - 1, top, 3, ln + 2, L); rect(c, x + 1, top, 1, ln + 2, M)
    if up: c.set(x, top - 1, K)
    gy = y + 2 if up else y - 1
    rect(c, x - 4, gy, 9, 3, K); rect(c, x - 3, gy + 1, 7, 1, R)
    rect(c, x - 1, gy + 3, 3, 4, K); rect(c, x, gy + 3, 1, 4, R)
def wand(c, x, y, ln=18):
    rect(c, x - 2, y - ln, 5, ln + 2, K); rect(c, x - 1, y - ln + 1, 3, ln, R)
    for k, dx in ((3, -1), (7, 1), (11, -1)):
        rect(c, x + dx * 2 - (1 if dx < 0 else 0), y - ln + k, 3, 2, K); rect(c, x + dx * 2 - (0 if dx < 0 else -1), y - ln + k, 2, 1, N)
SYMBOL = dict(pentacles=pentacle, cups=cup, swords=sword, wands=wand)

# ---- ludzie ----
def man(c, cx, base, h=36, robe=R, trim=WH, hat=None, hair=K, skin=C, lh=None, rh=None, legs=False, beard=False, hood=False, long_hair=False):
    """Postać w stylu 16-bit: bez twarzy (jak we wzorze), włosy/kaptur/czapka, szata, ręce 2 px, obrys 1 px.
    lh/rh = (dx, dy) położenie dłoni względem barku (None = opuszczona). Zwraca {'l':(x,y),'r':(x,y),'head':(x,y)}."""
    lay = layer()
    hh = 8; top = base - h; sy = top + hh + 1; sw = 11
    # tułów/szata
    if legs:
        rect(lay, cx - 5, sy, 11, int(h * .38), robe); rect(lay, cx - 4, sy + int(h * .38), 4, base - sy - int(h * .38), C); rect(lay, cx + 1, sy + int(h * .38), 4, base - sy - int(h * .38), C)
        rect(lay, cx - 4, base - 3, 4, 3, B if robe != B else R); rect(lay, cx + 1, base - 3, 4, 3, B if robe != B else R)
    else:
        poly(lay, [(cx - 5, sy), (cx + 6, sy), (cx + 9, base), (cx - 8, base)], robe)
        rect(lay, cx - 8, base - 2, 18, 2, trim)
    rect(lay, cx - 5, sy + 5, 11, 1, trim)                                   # pas
    line(lay, cx, sy, cx, sy + 9, trim)                                      # rozcięcie szaty / dekolt
    # głowa
    ell(lay, cx, top + 4, 3.5, 4, hood and robe or skin)
    if hood: rect(lay, cx - 2, top + 3, 5, 4, K)
    if hair is not None and not hood:
        rect(lay, cx - 3, top, 7, 2, hair); rect(lay, cx - 4, top + 1, 1, 5 if long_hair else 3, hair); rect(lay, cx + 4, top + 1, 1, 5 if long_hair else 3, hair)
    if beard: poly(lay, [(cx - 3, top + 6), (cx + 3, top + 6), (cx + 1, top + 11), (cx - 1, top + 11)], WH if hair is None else hair)
    rect(lay, cx - 1, top + 8, 3, 2, skin)                                   # szyja
    # ręce
    out = {'head': (cx, top + 4)}
    for side, tgt, key in ((-1, lh, 'l'), (1, rh, 'r')):
        sx, sy2 = cx + side * 5, sy + 1
        ex, ey = (sx + tgt[0], sy2 + tgt[1]) if tgt else (sx + side * 3, sy2 + 12)
        line(lay, sx, sy2, ex, ey, robe, 2); rect(lay, round(ex) - 1, round(ey) - 1, 2, 2, skin); out[key] = (round(ex), round(ey))
    if hat == 'crown':
        rect(lay, cx - 3, top - 2, 7, 3, Y); [lay.set(cx - 3 + i * 2, top - 3, Y) for i in range(4)]
    elif hat == 'cap': rect(lay, cx - 3, top - 1, 7, 3, trim); lay.set(cx + 4, top - 2, trim)
    elif hat == 'mitre': poly(lay, [(cx - 3, top + 1), (cx + 4, top + 1), (cx, top - 8)], Y)
    elif hat == 'wide': rect(lay, cx - 6, top, 13, 2, hair if hair is not None else K); rect(lay, cx - 3, top - 3, 7, 3, hair if hair is not None else K)
    outline_to(c, lay)
    return out

def horse(c, x, base, flip=False, col=WH):
    rows = ["..........KKK...........", ".........KCCCK..........", "........KCCCCCK.........", "......KKKCCCCCCKK.......",
            "....KKCCCCCCCCCCCKK.....", "...KCCCCCCCCCCCCCCCK....", "..KCCCCCCCCCCCCCCCCCK...", "..KCCCCCCCCCCCCCCCCCK...",
            "..KCCCCCCCCCCCCCCCCCK...", "...KCCCCCCCCCCCCCCCK....", "...KCK.KCK....KCK.KCK...", "...KCK.KCK....KCK.KCK...", "...KKK.KKK....KKK.KKK..."]
    p = dict(PAL); p['C'] = col
    sprite(c, x - 12, base - 13, rows, flip, p)

def finish(c): return c
