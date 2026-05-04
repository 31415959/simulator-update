import sys,os,csv,json,io,time
sys.path.insert(0,r'G:\314\CannotMax-main')
os.chdir(r'G:\314\CannotMax-main')
from simulator.battle_field import Battlefield
from simulator.utils import Faction, MONSTER_MAPPING

with open('simulator/monsters.json',encoding='utf-8') as f:
    mdata = json.load(f)['monsters']

with open('simulator/arknights.csv',encoding='utf-8') as f:
    rows = list(csv.reader(f))

r = rows[0]  # first match
print(f"Row 0 winner={r[-1]}")
print(f"Row 0 len={len(r)}")

left = {}
right = {}
for i in range(68):
    v = r[i].strip()
    if v and v not in ('', '0', '0.0'):
        cnt = int(float(v))
        mname = MONSTER_MAPPING.get(i, f"ID{i}")
        if i < 34:
            left[mname] = cnt
        else:
            right[mname] = cnt

print(f"Left: {left}")
print(f"Right: {right}")

# Try to match names to mdata
for name in list(left.keys()) + list(right.keys()):
    found = False
    for md in mdata:
        if name in md['名字'] or md['名字'] in name:
            found = True
            break
    if not found:
        print(f"  NO MATCH: {name}")

# Run battle
try:
    bf = Battlefield(mdata)
    bf.setup_battle(left, right, mdata)
    t0 = time.time()
    null = io.StringIO()
    old = sys.stdout
    sys.stdout = null
    frames = 0
    while frames < 100000:
        res = bf.run_one_frame()
        frames += 1
        if res is not None:
            break
    sys.stdout = old
    winner = 'L' if res == Faction.LEFT else 'R'
    print(f"Winner={winner} frames={frames} time={time.time()-t0:.1f}s")
except Exception as e:
    import traceback
    print(f"ERROR: {e}")
    traceback.print_exc()
