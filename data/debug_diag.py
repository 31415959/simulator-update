import sys,os,csv,json,io,time
sys.path.insert(0,r'G:\314\CannotMax-main')
os.chdir(r'G:\314\CannotMax-main')
from simulator.battle_field import Battlefield
from simulator.utils import Faction, MONSTER_MAPPING

log = []

with open('simulator/monsters.json',encoding='utf-8') as f:
    mdata = json.load(f)['monsters']
log.append(f"Loaded {len(mdata)} monsters from JSON")

# 打印 JSON 里前几个怪物名
for i,md in enumerate(mdata[:5]):
    log.append(f"  mdata[{i}]: {md.get('名字','?')}")

with open('simulator/arknights.csv',encoding='utf-8') as f:
    rows = list(csv.reader(f))
log.append(f"Loaded {len(rows)} rows from CSV")

r = rows[0]
log.append(f"Row0: cols={len(r)} winner={r[-1]}")

# Check MONSTER_MAPPING
for i in range(34):
    name = MONSTER_MAPPING.get(i, '')
    if name:
        log.append(f"  MAPPING[{i}]={name}")

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

log.append(f"Left army: {left}")
log.append(f"Right army: {right}")

# Match names
for name in list(left.keys()) + list(right.keys()):
    found = any(name in md.get('名字','') or md.get('名字','') in name for md in mdata)
    log.append(f"  name '{name}' match={found}")

log.append("Creating Battlefield...")
bf = Battlefield(mdata)
log.append(f"  monsters={len(bf.monsters) if hasattr(bf,'monsters') else '?'}")
log.append("setup_battle...")
bf.setup_battle(left, right, mdata)
log.append(f"  alive after setup: {sum(1 for m in bf.alive_monsters if m.is_alive) if hasattr(bf,'alive_monsters') else '?'}")

log.append("Running...")
t0 = time.time()
null = io.StringIO()
old = sys.stdout
sys.stdout = null
frames = 0
result = None
try:
    while frames < 20000:
        result = bf.run_one_frame()
        frames += 1
        if result is not None:
            break
    sys.stdout = old
    if result:
        log.append(f"Winner={'L' if result==Faction.LEFT else 'R'} frames={frames} time={time.time()-t0:.1f}s")
    else:
        log.append(f"TIMEOUT at {frames} frames, {time.time()-t0:.0f}s")
except Exception as e:
    sys.stdout = old
    log.append(f"CRASH at frame {frames}: {e}")
    import traceback
    log.append(traceback.format_exc()[:500])

with open(r'G:\314\CannotMax-main\data\debug_log.txt','w',encoding='utf-8') as f:
    f.write('\n'.join(log))
print('log written')
