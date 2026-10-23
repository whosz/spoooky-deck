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

SCENES.update({
    'ar01': "The Magician: a magician standing at a table with one hand raising a wand to the sky and the other pointing down, an infinity symbol above his head, a cup, a sword, a pentacle and a wand lying on the table, red roses and white lilies",
    'ar02': "The High Priestess: a veiled priestess seated between a black pillar and a white pillar, a crescent moon at her feet, holding a scroll, a tapestry of pomegranates behind her",
    'ar03': "The Empress: a queen seated on cushions in a lush wheat field with trees and a stream, a crown of stars, a heart-shaped shield, a flowing gown with pomegranates",
    'ar04': "The Emperor: an emperor on a stone throne decorated with ram heads, red and orange robes, holding an ankh scepter and a golden orb, barren mountains behind him",
    'ar05': "The Hierophant: a high priest in red robes with a triple crown seated between two pillars, one hand raised in blessing, two kneeling monks in front of him, crossed keys at his feet",
    'ar06': "The Lovers: a man and a woman standing in a garden in simple robes, a large winged angel above them in front of the sun, a mountain behind, a tree behind each of them",
    'ar07': "The Chariot: a warrior in armor standing in a chariot with a starry canopy, drawn by two sphinxes one black and one white, a walled city behind",
    'ar08': "Strength: a woman in white with a flower crown gently closing the mouth of a friendly lion, an infinity symbol above her head, mountains behind",
    'ar09': "The Hermit: an old hooded hermit with a long grey beard standing on a snowy mountain peak holding a lantern with a star inside and a wooden staff",
    'ar10': "Wheel of Fortune: a large golden wheel with mystic symbols in the sky, a blue sphinx holding a sword on top, a snake on one side and a jackal figure on the other, four winged creatures in the corners holding books among clouds",
    'ar11': "Justice: a crowned figure in red robes seated on a throne between two pillars, holding a raised sword in one hand and golden scales in the other, a purple curtain behind",
    'ar12': "The Hanged Man: a man hanging upside down by one foot from a wooden T-shaped frame, the other leg crossed, hands behind his back, a calm expression and a golden halo around his head",
    'ar13': "Death card: a tall dark hooded figure in black armor riding a white horse and carrying a black flag with a white rose, a sunrise between two towers on the horizon, a king, a child and a bishop standing before the horse",
    'ar14': "Temperance: a tall angel with large wings pouring water from one golden cup into another, one foot in a pond and one on land, irises growing, a path leading to a mountain with a glow",
    'ar15': "The Devil card: a large horned goat-headed creature with bat wings perched on a black stone pedestal holding a torch, two small horned imps chained to the pedestal, dark red background",
    'ar17': "The Star: a kneeling woman by a pond pouring water from two jugs onto the land and the water, one huge eight-pointed golden star and seven smaller white stars in the night sky, a bird in a tree",
    'ar18': "The Moon: a full moon with a face between two towers, a dog and a wolf howling at it, a crayfish crawling out of a pond, a winding path leading to distant mountains, night sky",
    'ar19': "The Sun: a huge smiling sun with rays above a stone wall with tall sunflowers, a happy child riding a white horse and holding a red banner",
    'ar20': "Judgement: a large angel in the clouds blowing a golden trumpet with a flag, below people with raised arms rising from boats on a calm sea, mountains behind",
    'ar21': "The World: a dancing figure wrapped in a scarf inside a large green laurel wreath holding two wands, in the four corners a winged man, an eagle, a lion and a bull, blue sky",
})

SCENES.update({
    'wa05': "Five of Wands: five young men in a field playfully clashing wooden staffs against each other in a friendly mock fight, blue sky",
    'cu05': "Five of Cups: a cloaked figure in black standing with head bowed looking at three spilled golden cups on the ground, two upright cups standing behind him, a river and a bridge and a castle in the distance",
    'sw07': "Seven of Swords: a man in a hat tiptoeing away from a camp carrying five swords in his arms, two swords stuck in the ground behind him, tents in the background",
    'pe05': "Five of Pentacles: two poor travelers in ragged clothes walking in the snow past a lit stained glass church window with five golden pentacles",
    'cu13': "Queen of Cups: a queen seated on an ornate throne by the sea holding an ornate golden covered cup, a crown, the waves behind her",
})
