"""python3 tools/ai/music.py <nazwa> <seed> [czas_s=100] [bpm=72]: generuje instrumentalną muzykę (ACE-Step 1.5, licencja MIT, wyniki do użytku komercyjnego) do tools/ai/music/<nazwa>.mp3."""
import os, sys, json, time, urllib.request, urllib.error
env = dict(l.strip().split('=', 1) for l in open(os.path.expanduser('~/.config/spooooky/replicate.env')) if '=' in l)
TOKEN = env['REPLICATE_API_TOKEN']
PROMPT = ("Dark mystical ambient instrumental for a candlelit tarot reading, slow and hypnotic. Warm detuned analog synthesizer pads with a slow drunken pitch wobble, "
          "deep warm sub bass, soft tape hiss and vinyl texture, gentle music box and celesta bell arpeggios, distant reverb, low minor key, "
          "no drums or very soft brushed percussion, no vocals, seamless loopable ending")
def call(url, data=None):
    for _ in range(10):
        req = urllib.request.Request(url, data=json.dumps(data).encode() if data else None, headers={'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json', 'Prefer': 'wait=60'})
        try: return json.load(urllib.request.urlopen(req, timeout=180))
        except urllib.error.HTTPError as e:
            if e.code == 429: time.sleep(12); continue
            print('HTTP', e.code, e.read()[:200]); sys.exit(2 if e.code == 402 else 3)
name, seed = sys.argv[1], int(sys.argv[2]); dur = int(sys.argv[3]) if len(sys.argv) > 3 else 100; bpm = int(sys.argv[4]) if len(sys.argv) > 4 else 72
pred = call('https://api.replicate.com/v1/predictions', {'version': '74e3a7d383b18815e277de5223f5fe9d53d38832de15aa567fe729fa129d0d85', 'input': {'prompt': PROMPT, 'lyrics': '[Instrumental]', 'duration': dur, 'bpm': bpm, 'key_scale': 'D minor', 'seed': seed, 'audio_format': 'mp3', 'inference_steps': 50}})
while pred['status'] in ('starting', 'processing'):
    time.sleep(3); pred = call(pred['urls']['get'])
if pred['status'] != 'succeeded': print(name, pred['status'], str(pred.get('error'))[:120]); sys.exit(1)
out = pred['output']; out = out[0] if isinstance(out, list) else out
os.makedirs('tools/ai/music', exist_ok=True); path = f'tools/ai/music/{name}.mp3'; urllib.request.urlretrieve(out, path)
print(path, 'predict_time', (pred.get('metrics') or {}).get('predict_time'), 's')
