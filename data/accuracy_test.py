import sys,os,csv,json,time,io
sys.path.insert(0,r'G:\314\CannotMax-main')
os.chdir(r'G:\314\CannotMax-main')
from simulator.battle_field import Battlefield
from simulator.utils import Faction, MONSTER_MAPPING, REVERSE_MONSTER_MAPPING

with open('simulator/monsters.json',encoding='utf-8') as f:
    mdata = json.load(f)['monsters']

# Build name lookup
name_by_id = {}
for mid, mname in MONSTER_MAPPING.items():
    # Find matching entry in mdata
    for md in mdata:
        if mname in md['名字'] or md['名字'] in mname:
            name_by_id[mid] = md['名字']
            break
    if mid not in name_by_id:
        name_by_id[mid] = mname  # fallback

with open('simulator/arknights.csv',encoding='utf-8') as f:
    rows = list(csv.reader(f))

print(f"Total matches: {len(rows)}")

# Test first 30 matches
correct = 0
total = 0
errors = 0
t0 = time.time()

for row_idx in range(min(15, len(rows))):
    r = rows[row_idx]
    winner_csv = r[-1].strip()  # last column = L or R
    
    left_army = {}
    right_army = {}
    
    for i in range(68):
        v = r[i].strip()
        if v and v not in ('', '0', '0.0'):
            try:
                cnt = int(float(v))
            except:
                continue
            name = name_by_id.get(i)
            if not name:
                continue
            if i < 34:
                left_army[name] = left_army.get(name, 0) + cnt
            else:
                right_army[name] = right_army.get(name, 0) + cnt
    
    if not left_army or not right_army:
        continue
    
    # Run simulation once
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
                if sim_winner == winner_csv:
                    correct += 1
                total += 1
                break
    except Exception as e:
        errors += 1
        if errors <= 2:
            print(f"  Row {row_idx} ERROR: {e}")
        continue

elapsed = time.time() - t0
rate = correct/total*100 if total else 0
print(f"\n准确率: {correct}/{total} = {rate:.1f}%")
print(f"耗时: {elapsed:.0f}s ({elapsed/total:.1f}s/局)" if total else "")
print(f"崩溃: {errors}")
