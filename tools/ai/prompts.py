"""Wspólny prompt stylu i sceny kart. Styl opisany słowami (bez nazwisk autorów)."""
STYLE = ("16-bit pixel art tarot card illustration, classic Rider-Waite tarot composition, very low resolution look with big chunky pixels, "
         "flat colors only, limited palette of black, white, light grey, cream, dark red, blue and green, thick black outlines around every shape, "
         "no gradients, no soft shading, simple blocky shapes, faces left blank or minimal, full-bleed scene, no text, no border, no frame, no letters, no numbers, no signature, no watermark")
SCENES = {
    'ar00': "The Fool: a carefree young traveler with a bundle on a stick walking toward a cliff edge, small white dog at his feet, big sun, snowy mountains behind, cream sky",
    'ar16': "The Tower: a tall stone tower struck by lightning from a dark sky, crown blown off the top, flames in the windows, two figures falling headfirst, dark blue background",
    'cu01': "Ace of Cups: a hand coming out of a cloud holding a golden chalice overflowing with water, a dove above, lily pads on a pond below, blue sky",
}
def prompt_for(card_id): return f"{STYLE}. Scene: {SCENES[card_id]}."
