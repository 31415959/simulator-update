import csv,sys,os
sys.path.insert(0,r'G:\314\CannotMax-main')
os.chdir(r'G:\314\CannotMax-main')
from simulator.utils import MONSTER_MAPPING

with open('simulator/arknights.csv',encoding='utf-8') as f:
    rows = list(csv.reader(f))

# Row 1: 直接看非零列和对应MONSTER_MAPPING
r = rows[1]
out = []
out.append(f"Row1 winner={r[-1]}")
for i in range(68):
    v = r[i].strip()
    if v and v not in ('','0','0.0'):
        name = MONSTER_MAPPING.get(i, f"?")
        side = "L" if i < 34 else "R"
        out.append(f"  col{i}={v} → {side} {name}")

with open(r'G:\314\CannotMax-main\data\row1_check.txt','w',encoding='utf-8') as f:
    f.write('\n'.join(out))
print('done')
