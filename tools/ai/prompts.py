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

SCENES.update({'wa01': 'Ace of Wands: a hand coming out of a cloud holding a sprouting wooden staff with green leaves, a castle on a hill and a river valley below', 'wa02': 'Two of Wands: a man in a red robe standing on a castle wall holding a small globe in one hand and a wooden staff in the other, a second staff fixed beside him, sea and mountains in the distance', 'wa03': 'Three of Wands: a man in a green cloak seen from behind standing on a cliff with three wooden staffs planted in the ground, looking at ships on a golden sea at sunset', 'wa04': 'Four of Wands: four tall wooden staffs holding up a garland of flowers, two people celebrating with raised bouquets in front of a castle', 'wa06': 'Six of Wands: a rider on a white horse wearing a laurel wreath holding a staff with a wreath, a crowd of people with staffs around him', 'wa07': 'Seven of Wands: a man standing on a hilltop defending himself with one wooden staff against six staffs rising from below', 'wa08': 'Eight of Wands: eight wooden staffs flying diagonally through the sky over a green landscape and a river', 'wa09': 'Nine of Wands: a weary bandaged man leaning on a staff in front of a row of eight staffs, looking back warily', 'wa10': 'Ten of Wands: a man bent over carrying a heavy bundle of ten wooden staffs toward a village in the distance', 'wa11': 'Page of Wands: a young page in a tunic and feathered hat standing in a desert holding a tall staff and looking at its sprouting top, pyramids behind', 'wa12': 'Knight of Wands: a knight in armor with a plume riding a rearing horse and holding a staff, desert and pyramids behind', 'wa13': 'Queen of Wands: a queen on a throne decorated with lions holding a sunflower and a staff, a black cat at her feet, a crown', 'wa14': 'King of Wands: a king on a throne decorated with lions and salamanders, holding a flowering staff, red robes, a crown', 'cu02': 'Two of Cups: a man and a woman facing each other exchanging golden cups, a winged lion head above them, a house on a hill behind', 'cu03': 'Three of Cups: three women in colorful dresses with flower wreaths dancing in a circle raising golden cups, fruit and flowers at their feet', 'cu04': 'Four of Cups: a young man sitting under a tree with crossed arms looking at three cups on the ground, a hand from a cloud offering a fourth cup', 'cu06': 'Six of Cups: two children in the courtyard of an old village, a boy offering a cup full of white flowers to a girl, five more cups with flowers around', 'cu07': 'Seven of Cups: a silhouette of a person looking at seven floating golden cups in clouds each holding a different vision: a castle, jewels, a dragon, a snake, a laurel wreath, a veiled figure and a face', 'cu08': 'Eight of Cups: a cloaked figure with a staff walking away from eight stacked golden cups toward mountains under a moon and sun', 'cu09': 'Nine of Cups: a happy wealthy man seated on a bench with crossed arms in front of a curved table with nine golden cups on a blue cloth', 'cu10': 'Ten of Cups: a happy couple with two children dancing under a rainbow of ten golden cups, a cottage and trees', 'cu11': 'Page of Cups: a young page in a patterned tunic holding a golden cup with a little fish popping out, standing by the sea', 'cu12': 'Knight of Cups: a knight in a winged helmet and armor riding a calm white horse and holding out a golden cup, a river and mountains', 'cu14': 'King of Cups: a king on a throne floating on the sea holding a cup and a scepter, a fish leaping and a ship in the background', 'sw01': 'Ace of Swords: a hand from a cloud holding a sword upright with a crown and a laurel wreath on its tip, mountains below', 'sw02': 'Two of Swords: a woman in a white dress with a blindfold seated on a bench holding two crossed swords, a calm sea and a crescent moon', 'sw03': 'Three of Swords: a large red heart pierced by three swords against stormy clouds and rain', 'sw04': 'Four of Swords: a stone knight statue lying on a tomb in a church with three swords on the wall above and one below, a stained glass window', 'sw05': 'Five of Swords: a smug man in front holding a sword, two other men walking away dejected, two swords on the ground, windy sky', 'sw06': 'Six of Swords: a ferryman poling a boat carrying a cloaked woman and a child with six swords standing upright in the boat, calm water', 'sw08': 'Eight of Swords: a woman in a long dress with a cloth over her eyes standing among eight swords planted in wet ground, a castle on a cliff behind', 'sw09': 'Nine of Swords: a person sitting up in bed with face in hands in the dark, nine swords hanging on the wall behind, a quilt with roses', 'sw10': 'Ten of Swords: a figure lying on the ground in a red cloak with ten swords standing upright in the ground around them, a black sky giving way to dawn over a calm sea', 'sw11': 'Page of Swords: a young page standing on a windy hilltop holding a sword up with both hands, clouds and blowing hair', 'sw12': 'Knight of Swords: a knight in armor charging on a galloping white horse with his sword raised, trees bent by the wind, clouds', 'sw13': 'Queen of Swords: a queen seated on a throne with butterflies, holding a raised sword and one hand extended, clouds and birds', 'sw14': 'King of Swords: a king on a throne holding a sword upright, blue robes, carved butterflies on the throne, clouds behind', 'pe01': 'Ace of Pentacles: a hand from a cloud holding a golden pentacle coin, a garden with lilies and an arch of flowers leading to mountains', 'pe02': 'Two of Pentacles: a young man juggling two pentacle coins connected by an infinity loop of ribbon, ships on rough waves behind', 'pe03': 'Three of Pentacles: a craftsman working on a stone arch in a cathedral, two monks and an architect watching with plans, three pentacles carved in the arch', 'pe04': 'Four of Pentacles: a man seated wearing a crown, holding a pentacle against his chest with another on his head and two under his feet, a city behind him', 'pe06': 'Six of Pentacles: a rich merchant in a red robe holding scales and giving coins to two kneeling beggars', 'pe07': 'Seven of Pentacles: a farmer leaning on a hoe looking at a bush growing seven golden pentacles', 'pe08': 'Eight of Pentacles: a craftsman carving a pentacle at a bench, eight pentacles displayed on a post and on the ground, a town in the distance', 'pe09': 'Nine of Pentacles: an elegant woman in a vineyard with a falcon on her gloved hand, nine pentacles among the grapevines, a castle', 'pe10': 'Ten of Pentacles: an old man with dogs sitting under a stone arch, a couple and a child, ten pentacles arranged in a pattern, a town', 'pe11': 'Page of Pentacles: a young page standing in a green field holding up a golden pentacle and gazing at it, a plowed field and trees', 'pe12': 'Knight of Pentacles: a knight in dark armor on a calm black horse holding a pentacle, plowed fields', 'pe13': 'Queen of Pentacles: a queen on a throne in a garden of roses holding a pentacle in her lap, a small rabbit, a throne decorated with fruit', 'pe14': 'King of Pentacles: a king on a throne decorated with bulls surrounded by grapevines holding a scepter and a pentacle, a castle behind'})

# Ekran startowy (pełny kadr 9:16) i tła kolejnych kroków (stonowane, niedominujące)
_PX = "chunky pixels, limited color palette, no text, no letters, no signature, no watermark"
ASSETS['intro'] = ("16-bit pixel art illustration, portrait orientation: a mystical young woman with long dark wavy hair and closed eyes holding a fan of tarot cards in front of her, "
                   "behind her a large glowing full moon surrounded by an arc of moon phases, deep purple and violet night sky with stars and soft clouds, "
                   "two lit candles with flames and small crystals at the bottom corners, dreamy mystical atmosphere, the lower third darker and mostly empty, " + _PX + ", purple violet gold and cream colors", '9:16')
for _id, _scene in {
    'bg_form': "a candlelit fortune teller's room with a round table, a crystal ball and candles, draped purple curtains and a starry window",
    'bg_pick': "a quiet night desert under a huge moon and thousands of stars with the silhouette of a distant temple",
    'bg_card': "a mystical stone altar with floating candles and golden sparkles in an arched hall with moonlight",
    'bg_read': "an old occult library with tall bookshelves, a glowing hanging lantern and cobwebs",
}.items():
    ASSETS[_id] = ("16-bit pixel art atmospheric background, portrait orientation, dark and moody, soft low contrast, no people: " + _scene + ", deep navy and violet tones with small warm golden light accents, " + _PX, '9:16')

ASSETS['intro2'] = ("16-bit pixel art illustration, portrait orientation: a mystical night landscape, a huge glowing golden full moon surrounded by an arc of moon phases, "
                    "a fan of tarot cards floating in the air in front of the moon glowing with golden light, below it a silhouette of mountains and a calm lake reflecting the moon, "
                    "small ringed planets and many stars in a deep purple and violet sky with soft clouds, two lit candles with crystals at the bottom corners, "
                    "no people, no humans, no characters, the lower third darker and mostly empty, " + _PX + ", purple violet gold and cream colors", '9:16')
ASSETS['bg_card2'] = ("16-bit pixel art atmospheric background, portrait orientation, dark and moody, soft low contrast, no people: a cosmic scene with large ringed planets, a swirling purple nebula, "
                      "many stars and a small floating stone island with a glowing lantern, deep navy and violet tones with small warm golden light accents, " + _PX, '9:16')
ASSETS['bg_read2'] = ("16-bit pixel art atmospheric background, portrait orientation, dark and moody, soft low contrast, no people: an old observatory interior with a large brass telescope pointing through an open dome toward planets and stars, "
                      "astrolabes and star charts on the walls, deep navy and violet tones with small warm golden light accents, " + _PX, '9:16')

# Styl 2 ("bogaty pixel art"): opis wyłącznie słowami (bez obrazów referencyjnych); wyższa rozdzielczość
STYLE2 = ("Rich detailed modern high-resolution pixel art illustration, painterly atmospheric lighting, a glowing light source with a soft luminous halo, "
          "dramatic dusk color palette of deep purple, magenta, pink, orange and gold, smooth color gradients built from many small pixel bands, "
          "layered dark silhouettes in the foreground for depth, fine pixel details, clean crisp pixel edges, renaissance tarot card composition filling the whole image, "
          "no text, no letters, no numbers, no border, no frame, no signature, no watermark")
def prompt2_for(card_id): return f"{STYLE2}. Scene: {SCENES[card_id]}."

# Styl 3 ("16-bit z ditheringiem"): opis słowami, bez obrazów referencyjnych
STYLE3 = ("16-bit video game pixel art tarot card illustration in classic Rider-Waite composition, bold saturated colors (orange, red, yellow, sky blue, purple, green), "
          "gradients and glowing light made with visible ordered dithering patterns of tiny dots, thick dark outlines around figures, figures with blank faceless skin-colored faces, "
          "rich detailed backgrounds, crisp pixel edges, filling the whole image, no text, no letters, no numbers, no border, no frame, no signature, no watermark")
def prompt3_for(card_id): return f"{STYLE3}. Scene: {SCENES[card_id]}."

SCENES.setdefault('cu07', "Seven of Cups: a silhouette of a person looking at seven floating golden cups in clouds each holding a different vision: a castle, jewels, a dragon, a snake, a laurel wreath, a veiled figure and a face")

# Styl 4 ("ziemisty, malarski pixel art"): opis słowami, bez obrazów referencyjnych
STYLE4 = ("Detailed painterly pixel art tarot card illustration in classic Rider-Waite composition, muted earthy color palette of ochre, sepia brown, dusty teal, olive green, burgundy and cream, "
          "soft warm lighting and gentle shading built from a limited palette, figures with simple expressive faces and clear hands, ornamental details and textures, "
          "clean crisp pixel edges, filling the whole image, no text, no letters, no numbers, no border, no frame, no signature, no watermark")
def prompt4_for(card_id): return f"{STYLE4}. Scene: {SCENES[card_id]}."
