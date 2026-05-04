import sys,os,csv,json,io,time
sys.path.insert(0,r'G:\314\CannotMax-main')
os.chdir(r'G:\314\CannotMax-main')
from simulator.battle_field import Battlefield
from simulator.utils import Faction, MONSTER_MAPPING

with open('simulator/monsters.json',encoding='utf-8') as f:
    mdata = json.load(f)['monsters']
with open('simulator/arknights.csv',encoding='utf-8') as f:
    rows = list(csv.reader(f))

MAX_FRAMES = 50000
out_path = r'G:\314\CannotMax-main\data\acc_stream.txt'

def test_one(row_idx):
    r = rows[row_idx]
    csv_winner = r[-1].strip()
    left = {}; right = {}
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
        return f"SKIP", None, 0
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
            return ('L' if res==Faction.LEFT else 'R'), csv_winner, frames
    sys.stdout = old
    return None, csv_winner, frames

correct = 0
total = 0
with open(out_path, 'w', encoding='utf-8') as f:
    f.write("Starting...\n")
    f.flush()
    for row_idx in range(1, min(31, len(rows))):  # skip row 0, rows 1-30
        sim, csv_w, frames = test_one(row_idx)
        if sim is None:
            line = f"Row{row_idx} TIMEOUT f={frames}\n"
        elif sim == 'SKIP':
            line = f"Row{row_idx} SKIP\n"
        else:
            match = sim == csv_w
            if match: correct += 1
            total += 1
            line = f"Row{row_idx} {'OK' if match else 'MIS'} SIM={sim} CSV={csv_w} f={frames}\n"
        f.write(line)
        f.flush()
    f.write(f"\nAccuracy: {correct}/{total} = {correct/total*100:.0f}%\n" if total else "\nNo results\n")

print('done')
