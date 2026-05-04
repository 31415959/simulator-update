import sys,os,csv,json,time,io
sys.path.insert(0,r'G:\314\CannotMax-main')
os.chdir(r'G:\314\CannotMax-main')
from simulator.battle_field import Battlefield
from simulator.utils import Faction, MONSTER_MAPPING

with open('simulator/monsters.json',encoding='utf-8') as f:
    mdata = json.load(f)['monsters']

name_by_id = {}
for mid, mname in MONSTER_MAPPING.items():
    for md in mdata:
        if mname in md['名字'] or md['名字'] in mname:
            name_by_id[mid] = md['名字']
            break
    if mid not in name_by_id:
        name_by_id[mid] = mname

with open('simulator/arknights.csv',encoding='utf-8') as f:
    rows = list(csv.reader(f))

def run_batch(start, count):
    correct = total = errors = 0
    t0 = time.time()
    for row_idx in range(start, min(start+count, len(rows))):
        r = rows[row_idx]
        winner_csv = r[-1].strip()
        left_army = {}
        right_army = {}
        for i in range(68):
            v = r[i].strip()
            if v and v not in ('', '0', '0.0'):
                try: cnt = int(float(v))
                except: continue
                name = name_by_id.get(i)
                if not name: continue
                if i < 34: left_army[name] = left_army.get(name,0)+cnt
                else: right_army[name] = right_army.get(name,0)+cnt
        if not left_army or not right_army: continue
        try:
            bf = Battlefield(mdata)
            bf.setup_battle(left_army, right_army, mdata)
            null = io.StringIO()
            old = sys.stdout
            sys.stdout = null
            while True:
                res = bf.run_one_frame()
                if res is not None:
                    sys.stdout = old
                    sim_winner = 'L' if res == Faction.LEFT else 'R'
                    if sim_winner == winner_csv: correct += 1
                    total += 1
                    break
        except Exception as e:
            errors += 1
            continue
    return correct, total, errors, time.time()-t0

# Batch 1: rows 0-4
c,t,e,el = run_batch(0,5)
line = f"Batch 0-4: {c}/{t} ({c/t*100:.0f}%) err={e} {el:.0f}s\n"
with open(r'G:\314\CannotMax-main\data\acc_result.txt','w',encoding='utf-8') as f:
    f.write(line)
print('done batch1')
