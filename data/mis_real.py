import csv,sys,os
sys.path.insert(0,r'G:\314\CannotMax-main')
os.chdir(r'G:\314\CannotMax-main')
from simulator.utils import MONSTER_MAPPING

rows=list(csv.reader(open('arknights.csv',encoding='utf-8')))

for row_idx in [1,8,14,22,24,27,29,30]:
    r=rows[row_idx]
    csv_w=r[-2].strip()
    left={};right={}
    for i in range(156):
        v=r[i].strip()
        if v and v not in ('','0','0.0'):
            cnt=int(float(v))
            name=MONSTER_MAPPING.get(i) if i<78 else MONSTER_MAPPING.get(i-78,'?')
            if not name:continue
            if i<78:left[name]=left.get(name,0)+cnt
            else:right[name]=right.get(name,0)+cnt
    with open(r'G:\314\CannotMax-main\data\mis_real.txt','a',encoding='utf-8') as f:
        f.write(f"Row{row_idx} CSV={csv_w}:\n")
        f.write(f"  L: {dict(sorted(left.items()))}\n")
        f.write(f"  R: {dict(sorted(right.items()))}\n\n")
print('done')
