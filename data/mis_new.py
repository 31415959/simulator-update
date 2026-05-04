import csv,sys,os
sys.path.insert(0,r'G:\314\CannotMax-main')
os.chdir(r'G:\314\CannotMax-main')
from simulator.utils import MONSTER_MAPPING
rows=list(csv.reader(open('arknights.csv',encoding='utf-8')))
for ri in [8,9,12,16,22,24,25,27,29,30]:
    r=rows[ri];cw=r[-2].strip()
    l={};rt={}
    for i in range(156):
        v=r[i].strip()
        if v and v not in ('','0','0.0'):
            cnt=int(float(v));nm=MONSTER_MAPPING.get(i) if i<78 else MONSTER_MAPPING.get(i-78)
            if nm:
                if i<78:l[nm]=l.get(nm,0)+cnt
                else:rt[nm]=rt.get(nm,0)+cnt
    with open(r'G:\314\CannotMax-main\data\mis_new.txt','a',encoding='utf-8') as f:
        f.write(f"Row{ri} CSV={cw}: L={dict(sorted(l.items()))} R={dict(sorted(rt.items()))}\n")
print('done')
