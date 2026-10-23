"""python3 tools/ai/run_all.py: generuje (wznawialnie) wszystkie karty i zasoby w stylu 5 (retro 16 kolorów, 0.5 MP, 1 wariant).
Pomija istniejące pliki s5_<id>_1.png; przy 402 (brak środków) kończy z komunikatem; filtr bezpieczeństwa: ponawia z innym ziarnem (do 3 prób)."""
import os, sys, json
sys.path.insert(0, 'tools/ai'); os.environ['STYLE'] = '5'; os.environ['RES'] = '0.5 MP'
import gen, urllib.error
ids = [f'ar{i:02d}' for i in range(22)] + [f'{p}{n:02d}' for p in ('wa', 'cu', 'sw', 'pe') for n in range(1, 15)]
assets = ['back', 'intro', 'bg_form', 'bg_pick', 'bg_card', 'bg_read']
done = 0
for cid in assets + ids:
    if os.path.exists(f'tools/ai/raw/s5_{cid}_1.png') and cid not in ('ar01',): continue
    for seed in (1, 2, 3):
        try: r = gen.generate(cid, seed if seed > 1 else 1)
        except urllib.error.HTTPError as e:
            print('HTTP', e.code, cid); sys.exit(2 if e.code == 402 else 3)
        if r:
            if seed != 1: os.replace(r, f'tools/ai/raw/s5_{cid}_1.png')
            done += 1; print('ok', cid, flush=True); break
        print('retry', cid, seed, flush=True)
print('ALL_DONE', done)
