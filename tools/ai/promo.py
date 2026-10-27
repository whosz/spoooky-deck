"""python3 tools/ai/promo.py <a|b|c> [seed]: generates a promo scene (Flux 2 Pro via Replicate, 4:5) into tools/ai/raw/promo_<name>_<seed>.png.
Token: ~/.config/spooooky/replicate.env. About 0.03 USD per image at 1 MP."""
import os, sys, json, time, urllib.request, urllib.error
env = dict(l.strip().split('=', 1) for l in open(os.path.expanduser('~/.config/spooooky/replicate.env')) if '=' in l)
TOKEN = env['REPLICATE_API_TOKEN']
STYLE = ("Early 1990s retro video game pixel art, chunky large pixels, very limited palette of about 16 colors dominated by deep navy blue, purple and warm gold with orange accents, "
         "thick dark outlines, flat color fills with a little ordered dithering, dark moody atmosphere with glowing candlelight, vertical poster composition, "
         "the top fifth and the bottom fifth of the image are calm dark empty space, no text, no letters, no numbers, no border, no frame, no signature, no watermark")
SCENES = {
 'a': "a mysterious round fortune teller's table in the middle of a dark room, a glowing crystal ball and a fan of tarot cards on it, tall melting candles on both sides, a huge pale full moon in a round window behind, a small black cat sitting on the table",
 'b': "a dark cozy start-up office at night, a laptop and a coffee mug on a wooden desk, five glowing golden tarot cards floating in the air above the desk, candles on the desk, a huge pale full moon outside a big window, mysterious purple fog",
 'c': "a hooded fortune teller without a visible face sitting at a table and holding up one glowing golden tarot card towards the viewer, swirling purple fog, tall candles, stars and a crescent moon in the dark sky behind",
 'd': "a designer's desk in a dark cozy room at night: a monitor showing a colorful website layout, a sketchbook, a coffee mug and a pencil jar, five glowing golden tarot cards floating in an arc above the desk, tall candles on both sides, a huge pale full moon in the window behind",
 'e': "a hooded fortune teller without a visible face seen from the front, hands spread over a table with a fan of glowing golden tarot cards, a lit crystal ball, candles, swirling purple fog and a starry sky with a crescent moon behind",
 'f': "a small pixel town at night with a tall glowing company building in the middle, a gigantic glowing golden tarot card rising in the sky above the building like a sun, rays of golden light, a huge pale full moon beside it, purple clouds, small lit windows",
}
def call(url, data=None):
    for _ in range(10):
        req = urllib.request.Request(url, data=json.dumps(data).encode() if data else None, headers={'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json', 'Prefer': 'wait=60'})
        try: return json.load(urllib.request.urlopen(req, timeout=300))
        except urllib.error.HTTPError as e:
            if e.code == 429: time.sleep(12); continue
            print('HTTP', e.code, e.read()[:200]); sys.exit(2 if e.code == 402 else 3)
name, seed = sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 1
inp = {'prompt': f"{STYLE}. Scene: {SCENES[name]}.", 'aspect_ratio': '4:5', 'resolution': '1 MP', 'output_format': 'png', 'seed': seed}
pred = call('https://api.replicate.com/v1/models/black-forest-labs/flux-2-pro/predictions', {'input': inp})
while pred['status'] in ('starting', 'processing'): time.sleep(2); pred = call(pred['urls']['get'])
if pred['status'] != 'succeeded': print(name, pred['status'], str(pred.get('error'))[:200]); sys.exit(1)
out = pred['output']; out = out[0] if isinstance(out, list) else out
os.makedirs('tools/ai/raw', exist_ok=True); path = f'tools/ai/raw/promo_{name}_{seed}.png'; urllib.request.urlretrieve(out, path); print(path)
