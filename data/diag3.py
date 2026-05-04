import sys,os,csv,json,io,time
sys.path.insert(0,r'G:\314\CannotMax-main')
os.chdir(r'G:\314\CannotMax-main')
from simulator.battle_field import Battlefield
from simulator.utils import Faction, MONSTER_MAPPING

with open('simulator/monsters.json',encoding='utf-8') as f:
    mdata = json.load(f)['monsters']
with open('simulator/arknights.csv',encoding='utf-8') as f:
    rows = list(csv.reader(f))

r = rows[0]

# 用旧表列→名映射
import csv as csvmod
with open('monster_greenvine_old.csv',encoding='utf-8-sig') as f:
    id2name_old = {}
    for row in csvmod.reader(f):
        if row and row[0].isdigit():
            id2name_old[int(row[0])] = row[2]

left = {}
right = {}
for i in range(68):
    v = r[i].strip()
    if v and v not in ('','0','0.0'):
        cnt = int(float(v))
        old_id = i + 1  # col 0 = old id 1
        name = id2name_old.get(old_id, MONSTER_MAPPING.get(i, f"ID{i}"))
        if i < 34: left[name] = cnt
        else: right[name] = cnt

out = [f"L={len(left)} types, R={len(right)} types"]

bf = Battlefield(mdata)
bf.setup_battle(left, right, mdata)

# 跑直到出结果
null = io.StringIO()
old = sys.stdout
sys.stdout = null
frames = 0
t0 = time.time()
while frames < 50000:
    res = bf.run_one_frame()
    frames += 1
    if res is not None:
        sys.stdout = old
        winner = 'L' if res == Faction.LEFT else 'R'
        csv_winner = r[-1].strip()
        out.append(f"Winner=SIM:{winner} CSV:{csv_winner} frames={frames} time={time.time()-t0:.1f}s")
        break
else:
    sys.stdout = old
    alive = sum(1 for m in bf.alive_monsters if m.is_alive)
    out.append(f"TIMEOUT frames={frames} alive={alive}")

with open(r'G:\314\CannotMax-main\data\diag3.txt','w',encoding='utf-8') as f:
    f.write('\n'.join(out))
print('done')
