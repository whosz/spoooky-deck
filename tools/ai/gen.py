"""python3 tools/ai/gen.py <id> [seed ...]: generuje surowe obrazy karty przez Replicate (Flux 2 Pro) do tools/ai/raw/<id>_<seed>.png.
Token: ~/.config/spooooky/replicate.env (REPLICATE_API_TOKEN). Koszt wypisywany na koniec (ok. 0,015 USD / obraz)."""
import os, sys, json, time, urllib.request, urllib.error
sys.path.insert(0, os.path.dirname(__file__))
from prompts import prompt_for
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
    pred = call(f'https://api.replicate.com/v1/models/{MODEL}/predictions',
                {'input': {'prompt': prompt_for(card_id), 'aspect_ratio': '2:3', 'resolution': resolution, 'output_format': 'png', 'seed': seed}}, {'Prefer': 'wait=60'})
    while pred['status'] in ('starting', 'processing'):
        time.sleep(2); pred = call(pred['urls']['get'])
    if pred['status'] != 'succeeded': print(f"{card_id}/{seed}: {pred['status']} {str(pred.get('error'))[:90]}"); return None
    out = pred['output']; out = out[0] if isinstance(out, list) else out
    os.makedirs('tools/ai/raw', exist_ok=True); path = f'tools/ai/raw/{card_id}_{seed}.png'
    urllib.request.urlretrieve(out, path); return path

if __name__ == '__main__':
    cid, seeds = sys.argv[1], [int(s) for s in sys.argv[2:]] or [1]
    for s in seeds: print(generate(cid, s))
    print('approx cost USD:', round(0.015 * len(seeds), 3))
