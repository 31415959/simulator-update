import sys,os,csv,json,io
sys.path.insert(0,r'G:\314\CannotMax-main')
os.chdir(r'G:\314\CannotMax-main')
from simulator.battle_field import Battlefield
from simulator.utils import Faction, MONSTER_MAPPING

with open('simulator/monsters.json',encoding='utf-8') as f:
    mdata = json.load(f)['monsters']
with open('simulator/arknights.csv',encoding='utf-8') as f:
    rows = list(csv.reader(f))

r = rows[0]
left = {}
right = {}
for i in range(68):
    v = r[i].strip()
    if v and v not in ('', '0', '0.0'):
        cnt = int(float(v))
        name = MONSTER_MAPPING.get(i, f"ID{i}")
        if i < 34: left[name] = cnt
        else: right[name] = cnt

out = [f"L={left}", f"R={right}"]

bf = Battlefield(mdata)
bf.setup_battle(left, right, mdata)

alive = [(m.name, m.health, m.faction) for m in bf.alive_monsters if m.is_alive]
out.append(f"alive={len(alive)} first={alive[:5]}")

null = io.StringIO()
old = sys.stdout
sys.stdout = null
for frame in range(10):
    res = bf.run_one_frame()
    if res is not None:
        out.append(f"winner at frame {frame}: {'L' if res==Faction.LEFT else 'R'}")
        break
else:
    out.append("no winner after 10 frames")
sys.stdout = old

with open(r'G:\314\CannotMax-main\data\diag2.txt','w',encoding='utf-8') as f:
    f.write('\n'.join(out))
print('done')
