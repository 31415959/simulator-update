import sys,os,csv,json,io,time
sys.path.insert(0,r'G:\314\CannotMax-main')
os.chdir(r'G:\314\CannotMax-main')
from simulator.battle_field import Battlefield
from simulator.utils import Faction, MONSTER_MAPPING

with open('simulator/monsters.json',encoding='utf-8') as f:
    mdata = json.load(f)['monsters']

rows = list(csv.reader(open('arknights.csv',encoding='utf-8')))
print(f"CSV: {len(rows)} rows x {len(rows[0])} cols")

correct = total = errors = 0
t0 = time.time()
MAX_FRAMES = 50000
out_path = r'data\acc_real.txt'

with open(out_path, 'w', encoding='utf-8') as out_f:
    out_f.write(f"Testing rows 1-30 (skip row0=header)...\n")
    for row_idx in range(1, min(31, len(rows))):
        r = rows[row_idx]
        csv_winner = r[-2].strip()  # col 156 = winner, col 157 = img
        
        left = {}; right = {}
        for i in range(156):
            v = r[i].strip()
            if v and v not in ('','0','0.0'):
                try: cnt = int(float(v))
                except: continue
                name = MONSTER_MAPPING.get(i) if i < 78 else MONSTER_MAPPING.get(i - 78)
                if not name: continue
                if i < 78: left[name] = left.get(name,0) + cnt
                else: right[name] = right.get(name,0) + cnt
        
        if not left or not right: continue
        
        try:
            bf = Battlefield(mdata)
            bf.setup_battle(left, right, mdata)
            null = io.StringIO()
            old = sys.stdout
            sys.stdout = null
            frames = 0
            while frames < MAX_FRAMES:
                res = bf.run_one_frame()
                frames += 1
                if res is not None:
                    sys.stdout = old
                    sim_winner = 'L' if res == Faction.LEFT else 'R'
                    match = sim_winner == csv_winner
                    if match: correct += 1
                    total += 1
                    out_f.write(f"Row{row_idx} {'OK' if match else 'MIS'} SIM={sim_winner} CSV={csv_winner} f={frames}\n")
                    out_f.flush()
                    break
            else:
                sys.stdout = old
                out_f.write(f"Row{row_idx} TIMEOUT f={frames}\n")
        except Exception as e:
            errors += 1
            out_f.write(f"Row{row_idx} ERR: {e}\n")
    
    out_f.write(f"\nAccuracy: {correct}/{total} = {correct/total*100:.1f}% err={errors} time={time.time()-t0:.0f}s\n")

print('done')
