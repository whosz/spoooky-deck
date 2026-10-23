"""Wspólny prompt stylu i sceny kart. Styl opisany słowami (bez nazwisk autorów)."""
STYLE = ("16-bit pixel art tarot card illustration, classic Rider-Waite tarot composition, very low resolution look with big chunky pixels, "
         "flat colors only, limited palette of black, white, light grey, cream, dark red, blue and green, thick black outlines around every shape, "
         "no gradients, no soft shading, simple blocky shapes, faces left blank or minimal, full-bleed scene, no text, no border, no frame, no letters, no numbers, no signature, no watermark")
SCENES = {
    'ar00': "The Fool: a carefree young traveler with a bundle on a stick walking toward a cliff edge, small white dog at his feet, big sun, snowy mountains behind, cream sky",
    'ar16': "The Tower: a tall stone tower struck by lightning from a dark sky, crown blown off the top, flames in the windows, two figures falling headfirst, dark blue background",
    'cu01': "Ace of Cups: a hand coming out of a cloud holding a golden chalice overflowing with water, a dove above, lily pads on a pond below, blue sky",
}
def prompt_for(card_id):
    if card_id in ASSETS: return ASSETS[card_id][0]
    return f"{STYLE}. Scene: {SCENES[card_id]}."
def aspect_for(card_id): return ASSETS[card_id][1] if card_id in ASSETS else '2:3'
def refs_for(card_id): return (ASSETS[card_id][2] if card_id in ASSETS and len(ASSETS[card_id]) > 2 else [])

# Zasoby specjalne: (pełny prompt, proporcje). Bez nazwisk autorów; styl opisany słowami.
ASSETS = {
    'back': ("16-bit pixel art tarot card back design, perfectly symmetrical, portrait orientation, deep navy blue background with a subtle star pattern, "
             "an ornate golden oval in the center containing a crescent moon on top, a mystical eye in the middle and a small sun at the bottom, "
             "decorative golden border with corner ornaments, flat colors, limited palette of navy blue, gold, cream and black, thick dark outlines, "
             "chunky pixels, no gradients, no text, no letters, no signature, no watermark, the card fills the whole image edge to edge", '2:3'),
    'candle': ("16-bit pixel art of a single tall white wax candle in a small golden candlestick holder, unlit with a short black wick and no flame, "
               "side view, centered, drips of wax, flat colors, thick black outlines, chunky pixels, no gradients, "
               "on a plain solid pure bright green (#00ff00) background with nothing else, no shadow, no text, no signature", '2:3'),
}

ASSETS['hero'] = ("16-bit pixel art illustration: three tarot cards fanned out in a row, showing their card backs which are identical to the reference card back image, "
                  "slightly tilted left and right, golden light rays radiating behind them, a few small golden sparkles, dark navy blue background, "
                  "flat colors, thick dark outlines, chunky pixels, no gradients, no text, no letters, no signature, no watermark", '3:2', ['tools/ai/raw/back_1.png'])
