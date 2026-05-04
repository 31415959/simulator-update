import csv,sys,os
sys.path.insert(0,r'G:\314\CannotMax-main')
os.chdir(r'G:\314\CannotMax-main')
from simulator.utils import MONSTER_MAPPING
rows=list(csv.reader(open('arknights.csv',encoding='utf-8')))
r=rows[18]
print("Row 18 non-zero columns on RIGHT side:")
for i in range(78, 156):
    v=r[i].strip()
    if v and v not in ('','0','0.0'):
        idx = i - 78
        name = MONSTER_MAPPING.get(idx, f'MISSING_{idx}')
        print(f"  col{i} (idx{idx}) = {v} → {name}")
