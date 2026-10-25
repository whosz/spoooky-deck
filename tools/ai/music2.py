"""python3 tools/ai/music2.py minimax|lyria <name> [seed]: alternative music models (MiniMax Music 2.6, Google Lyria 2) to tools/ai/music/<name>.mp3. Note: the commercial terms of these models are less clear than ACE-Step's (MIT), see docs/licensing.md."""
import os, sys, json, time, urllib.request, urllib.error
env = dict(l.strip().split('=', 1) for l in open(os.path.expanduser('~/.config/spooooky/replicate.env')) if '=' in l)
TOKEN = env['REPLICATE_API_TOKEN']
STYLE = ("Dark mystical instrumental for a candlelit tarot reading: slow, hypnotic, warm detuned analog synthesizer pads with a slow drunken pitch wobble, deep warm bass, soft tape hiss, "
         "gentle music box and celesta bell arpeggios, distant reverb, minor key, very soft percussion, no vocals, calm and atmospheric, loopable")
def call(url, data=None):
    for _ in range(10):
        req = urllib.request.Request(url, data=json.dumps(data).encode() if data else None, headers={'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json', 'Prefer': 'wait=60'})
        try: return json.load(urllib.request.urlopen(req, timeout=300))
        except urllib.error.HTTPError as e:
            if e.code == 429: time.sleep(12); continue
            print('HTTP', e.code, e.read()[:200]); sys.exit(2 if e.code == 402 else 3)
kind, name = sys.argv[1], sys.argv[2]
if kind == 'minimax': url, inp = 'https://api.replicate.com/v1/models/minimax/music-2.6/predictions', {'prompt': STYLE, 'is_instrumental': True, 'audio_format': 'mp3', 'bitrate': 256000, 'sample_rate': 44100}
else: url, inp = 'https://api.replicate.com/v1/models/google/lyria-2/predictions', {'prompt': STYLE, 'negative_prompt': 'vocals, singing, drums, fast tempo, loud, distortion'}
if len(sys.argv) > 3 and kind == 'lyria': inp['seed'] = int(sys.argv[3])
pred = call(url, {'input': inp})
while pred['status'] in ('starting', 'processing'): time.sleep(3); pred = call(pred['urls']['get'])
if pred['status'] != 'succeeded': print(name, pred['status'], str(pred.get('error'))[:150]); sys.exit(1)
out = pred['output']; out = out[0] if isinstance(out, list) else out
os.makedirs('tools/ai/music', exist_ok=True); path = f'tools/ai/music/{name}.mp3'; urllib.request.urlretrieve(out, path)
print(path, 'predict_time', (pred.get('metrics') or {}).get('predict_time'))
