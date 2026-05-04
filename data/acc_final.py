import sys,os,csv,json,io,time
sys.path.insert(0,r'G:\314\CannotMax-main')
os.chdir(r'G:\314\CannotMax-main')
from simulator.battle_field import Battlefield
from simulator.utils import Faction, MONSTER_MAPPING

with open('simulator/monsters.json',encoding='utf-8') as f:
    mdata = json.load(f)['monsters']
with open('simulator/arknights.csv',encoding='utf-8') as f:
    rows = list(csv.reader(f))

correct = total = errors = 0
t0 = time.time()
out_lines = []
MAX_FRAMES = 50000

sample_n = min(30, len(rows))
for row_idx in range(sample_n):
    r = rows[row_idx]
    csv_winner = r[-1].strip()
    
    left = {}
    right = {}
    for i in range(68):
        v = r[i].strip()
        if v and v not in ('','0','0.0'):
            try: cnt = int(float(v))
            except: continue
            name = MONSTER_MAPPING.get(i)
            if not name: continue
            if i < 34: left[name] = left.get(name,0) + cnt
            else: right[name] = right.get(name,0) + cnt
    
    if not left or not right:
        out_lines.append(f"Row{row_idx} SKIP empty")
        continue
    
    try:
        bf = Battlefield(mdata)
        bf.setup_battle(left, right, mdata)
        null = io.StringIO()
        old_out = sys.stdout
        sys.stdout = null
        frames = 0
        while frames < MAX_FRAMES:
            res = bf.run_one_frame()
            frames += 1
            if res is not None:
                sys.stdout = old_out
                sim_winner = 'L' if res == Faction.LEFT else 'R'
                match = 'OK' if sim_winner == csv_winner else 'MIS'
                if sim_winner == csv_winner: correct += 1
                total += 1
                out_lines.append(f"{match} Row{row_idx} SIM={sim_winner} CSV={csv_winner} f={frames}")
                break
        else:
            sys.stdout = old_out
            out_lines.append(f"TIMEOUT Row{row_idx} frames={frames}")
            continue
    except Exception as e:
        out_lines.append(f"ERR Row{row_idx}: {e}")
        errors += 1
        if errors <= 2:
            import traceback
            out_lines.append(traceback.format_exc()[:300])

elapsed = time.time() - t0
rate = correct/total*100 if total else 0
out_lines.append(f"\nAccuracy: {correct}/{total} = {rate:.1f}% err={errors} time={elapsed:.0f}s")

with open(r'G:\314\CannotMax-main\data\acc_final.txt','w',encoding='utf-8') as f:
    f.write('\n'.join(out_lines))
print('done')
