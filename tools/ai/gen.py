"""python3 tools/ai/gen.py <id> [seed ...]: generuje surowe obrazy karty przez Replicate (Flux 2 Pro) do tools/ai/raw/<id>_<seed>.png.
Token: ~/.config/spooooky/replicate.env (REPLICATE_API_TOKEN). Koszt wypisywany na koniec (ok. 0,015 USD / obraz)."""
import os, sys, json, time, urllib.request, urllib.error
sys.path.insert(0, os.path.dirname(__file__))
from prompts import prompt_for, aspect_for, refs_for, prompt2_for, prompt3_for, prompt4_for, prompt5_for
import prompts as _P
import base64
MODEL = 'black-forest-labs/flux-2-pro'
env = dict(l.strip().split('=', 1) for l in open(os.path.expanduser('~/.config/spooooky/replicate.env')) if '=' in l)
TOKEN = env['REPLICATE_API_TOKEN']

def call(url, data=None, headers=None):
    for attempt in range(10):   # limit zapytań (429) przy małym saldzie: czekamy i ponawiamy
        req = urllib.request.Request(url, data=json.dumps(data).encode() if data else None, headers={'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json', **(headers or {})})
        try: return json.load(urllib.request.urlopen(req, timeout=120))
        except urllib.error.HTTPError as e:
            if e.code != 429: raise
            wait = 11
            try: wait = float(json.loads(e.read()).get('retry_after', 10)) + 2
            except Exception: pass
            time.sleep(wait)
    raise SystemExit('429 za dlugo')

def generate(card_id, seed, resolution='0.5 MP'):
    style3 = os.environ.get('STYLE') == '3'
    style4 = os.environ.get('STYLE') == '4'
    style5 = os.environ.get('STYLE') == '5'
    style2 = os.environ.get('STYLE') in ('2', '3', '4', '5')
    if style2: resolution = os.environ.get('RES', '1 MP')
    inp = {'prompt': ((_P.prompt5_asset(card_id) if card_id in _P.ASSETS5 else prompt5_for(card_id)) if style5 else prompt4_for(card_id) if style4 else prompt3_for(card_id) if style3 else prompt2_for(card_id)) if style2 else prompt_for(card_id), 'aspect_ratio': (_P.ASSETS5[card_id][1] if style5 and card_id in _P.ASSETS5 else aspect_for(card_id)), 'resolution': resolution, 'output_format': 'png', 'seed': seed}
    refs = [f"data:image/png;base64,{base64.b64encode(open(r, 'rb').read()).decode()}" for r in refs_for(card_id)]   # styl 2 opisany wyłącznie słowami, bez obrazów referencyjnych cudzych prac
    if refs: inp['input_images'] = refs
    pred = call(f'https://api.replicate.com/v1/models/{MODEL}/predictions', {'input': inp}, {'Prefer': 'wait=60'})
    while pred['status'] in ('starting', 'processing'):
        time.sleep(2); pred = call(pred['urls']['get'])
    if pred['status'] != 'succeeded': print(f"{card_id}/{seed}: {pred['status']} {str(pred.get('error'))[:90]}"); return None
    out = pred['output']; out = out[0] if isinstance(out, list) else out
    os.makedirs('tools/ai/raw', exist_ok=True); path = f'tools/ai/raw/{card_id}_{seed}.png' if not style2 else (f'tools/ai/raw/s5_{card_id}_{seed}.png' if style5 else f'tools/ai/raw/s4_{card_id}_{seed}.png' if style4 else f'tools/ai/raw/s3_{card_id}_{seed}.png' if style3 else f'tools/ai/raw/s2_{card_id}_{seed}.png')
    urllib.request.urlretrieve(out, path); return path

if __name__ == '__main__':
    cid, seeds = sys.argv[1], [int(s) for s in sys.argv[2:]] or [1]
    for s in seeds: print(generate(cid, s))
    print('approx cost USD:', round(0.015 * len(seeds), 3))
