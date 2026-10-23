"""Małe Arkana: 4 kolory x 14 kart z jednego generatora parametrycznego (tło zależne od koloru, pipsy, figury dworskie)."""
import sys; sys.path.insert(0, 'tools/deck'); sys.path.insert(0, 'tools')
from lib import *

SUITS = {  # prefix -> (nazwa, rampa nieba, kolor wzgórz, robe/trim figury, akcent glow)
    'wa': ('wands', ['v1', 'r2', 'o2', 'o4'], ('o1', 'r1'), ('r3', 'o4')),
    'cu': ('cups', ['n1', 'n3', 't1', 't2'], ('t1', 'n2'), ('t2', 't4')),
    'sw': ('swords', ['n1', 's1', 's2', 's3'], ('s1', 'y1'), ('s2', 's4')),
    'pe': ('pentacles', ['n2', 'e1', 'e2', 'g2'], ('e2', 'e1'), ('e3', 'g4')),
}
PIPS = {1: [(.5, .5)], 2: [(.5, .27), (.5, .73)], 3: [(.5, .2), (.5, .5), (.5, .8)],
        4: [(.28, .3), (.72, .3), (.28, .7), (.72, .7)], 5: [(.28, .27), (.72, .27), (.5, .5), (.28, .73), (.72, .73)],
        6: [(.28, .2), (.72, .2), (.28, .5), (.72, .5), (.28, .8), (.72, .8)],
        7: [(.28, .2), (.72, .2), (.28, .5), (.72, .5), (.28, .8), (.72, .8), (.5, .35)],
        8: [(.28, .15), (.72, .15), (.28, .38), (.72, .38), (.28, .62), (.72, .62), (.28, .85), (.72, .85)],
        9: [(.22, .2), (.5, .2), (.78, .2), (.22, .5), (.5, .5), (.78, .5), (.22, .8), (.5, .8), (.78, .8)],
        10: [(.28, .12), (.72, .12), (.28, .31), (.72, .31), (.28, .5), (.72, .5), (.28, .69), (.72, .69), (.28, .88), (.72, .88)]}

def background(c, suit, seed):
    name, sky, (hill, hill2), _ = SUITS[suit]
    ramp(c, 0, 0, W, 150, sky)
    if name == 'wands': glow(c, 72, 120, 70, 'o3', 2); disc(c, 72, 128, 14, 'o5'); disc(c, 72, 128, 11, 'o4'); mountains(c, 150, 40, 'o1', seed)
    elif name == 'cups': stars(c, 5, 80, 30, seed); disc(c, 104, 40, 10, 't4'); disc(c, 108, 38, 9, 't1'); mountains(c, 150, 26, 'n2', seed)
    elif name == 'swords': clouds(c, 10, 70, ['s1', 's2'], seed, 6); mountains(c, 150, 55, 'y1', seed, 4)
    else: stars(c, 5, 70, 22, seed); glow(c, 30, 40, 26, 'g3', 2); hills(c, 130, 10, 'e1', seed, .05)
    hills(c, 150, 7, hill, seed + 1, .09)
    ramp(c, 0, 158, W, H, [hill, hill2, 'ink'])

def pips(c, suit, n):
    name = SUITS[suit][0]; fn = SYMBOL[name]
    if n == 1:
        glow(c, 72, 100, 60, SUITS[suit][3][0], 2.2)
        for i in range(24):   # promienie
            a = i * math.pi / 12; line(c, 72 + 22 * math.cos(a), 100 + 22 * math.sin(a), 72 + 52 * math.cos(a), 100 + 52 * math.sin(a), SUITS[suit][3][1])
        fn(c, 72, 100, 2.0 if name != 'swords' else 1.7); return
    s = {2: 1.35, 3: 1.2, 4: 1.2, 5: 1.1, 6: 1.0, 7: .95, 8: .9, 9: .9, 10: .85}[n]
    for fx, fy in PIPS[n]: fn(c, 24 + fx * 96, 40 + fy * 136, s)

COURT = {11: ('page', 72, 'cap'), 12: ('knight', 92, 'plume'), 13: ('queen', 106, 'crown3'), 14: ('king', 114, 'crown5')}
def court(c, suit, n):
    name, (robe, trim) = SUITS[suit][0], SUITS[suit][3]
    role, h, hat = COURT[n]
    if n >= 13: rect(c, 34, 46, 76, 126, 'ink'); rect(c, 37, 48, 70, 124, 'v1' if n == 14 else 'n3'); c.ellipse(72, 54, 35, 12, P['n3' if n == 13 else 'v1'], True)
    f = figure(c, 72, 172, h, robe=robe, trim=trim, hood=False, arms='up' if n < 13 else 'down', skin='k2')
    hx, hy = f['head']
    if hat == 'cap': poly(c, [(hx - 6, hy - 3), (hx + 6, hy - 3), (hx + 1, hy - 9)], trim); line(c, hx + 1, hy - 9, hx + 9, hy - 14, 'o4')
    elif hat == 'plume': rect(c, hx - 6, hy - 5, 12, 5, 'y3'); rect(c, hx - 6, hy - 5, 12, 1, 'white'); poly(c, [(hx, hy - 5), (hx + 4, hy - 14), (hx + 10, hy - 8)], 'r3')
    elif hat == 'crown3': crown(c, hx, hy - 5, 12, 3)
    else: crown(c, hx, hy - 5, 14, 5)
    sx, sy = f['hand_r'] if n < 13 else (f['hand_r'][0] + 6, f['hand_r'][1] - 4)
    SYMBOL[name](c, sx + (3 if n < 13 else 4), sy - 8, .8 if n < 13 else .75)
    if n == 12:   # płaszcz rycerza
        poly(c, [(60, 128), (50, 172), (62, 172)], robe)

def render(card_id):
    suit, n = card_id[:2], int(card_id[2:]); c = card()
    background(c, suit, n * 7 + ord(suit[0]))
    (pips if n <= 10 else court)(c, suit, n)
    return finish(c)

IDS = [f'{p}{n:02d}' for p in ('wa', 'cu', 'sw', 'pe') for n in range(1, 15)]
if __name__ == '__main__':
    from sheet import sheet
    pick = sys.argv[1:] or IDS[:14]
    sheet([render(i) for i in pick], 'tools/deck/_minors.png', cols=7)
