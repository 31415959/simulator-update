import csv,sys,os,json
sys.path.insert(0,r'G:\314\CannotMax-main')
os.chdir(r'G:\314\CannotMax-main')
from simulator.utils import MONSTER_MAPPING
rows=list(csv.reader(open('arknights.csv',encoding='utf-8')))
r=rows[18]

# Get full names from JSON
mdata=json.load(open('simulator/monsters.json',encoding='utf-8'))['monsters']
name_by_id = {i: MONSTER_MAPPING[i] for i in range(78) if i in MONSTER_MAPPING}

l={};rt={}
for i in range(156):
    v=r[i].strip()
    if v and v not in ('','0','0.0'):
        cnt=int(float(v))
        nm=name_by_id.get(i) if i<78 else name_by_id.get(i-78)
        if nm:
            if i<78:l[nm]=l.get(nm,0)+cnt
            else:rt[nm]=rt.get(nm,0)+cnt

print(f"Row18 CSV={r[-2].strip()} SIM=L (我们的错)")
print(f"\n左方 ({sum(l.values())} 个):")
for k,v in sorted(l.items()):
    print(f"  {k} × {v}")

print(f"\n右方 ({sum(rt.values())} 个):")
for k,v in sorted(rt.items()):
    # Also show stats
    st = next((m for m in mdata if m['名字']==k), None)
    if st:
        atk=st['攻击力']['数值'];hp=st['生命值']['数值'];df=st['物理防御']['数值'];res=st['法抗']['数值']
        print(f"  {k} × {v}  [ATK={atk} HP={hp} DEF={df} RES={res}]")
    else:
        print(f"  {k} × {v}  [?]")
