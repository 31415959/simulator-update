import csv,sys,os,json
sys.path.insert(0,r'G:\314\CannotMax-main')
os.chdir(r'G:\314\CannotMax-main')
from simulator.utils import MONSTER_MAPPING
rows=list(csv.reader(open('arknights.csv',encoding='utf-8')))
mdata=json.load(open('simulator/monsters.json',encoding='utf-8'))['monsters']

r=rows[22]
l={};rt={}
for i in range(156):
    v=r[i].strip()
    if v and v not in ('','0','0.0'):
        cnt=int(float(v))
        nm=MONSTER_MAPPING.get(i) if i<78 else MONSTER_MAPPING.get(i-78)
        if nm:
            if i<78:l[nm]=l.get(nm,0)+cnt
            else:rt[nm]=rt.get(nm,0)+cnt

print(f"Row22 CSV={r[-2].strip()} SIM=L (错了)")
print(f"\n左方:")
for k,v in sorted(l.items()):
    st=next((m for m in mdata if m['名字']==k),None)
    if st:
        a=st['攻击力']['数值'];h=st['生命值']['数值'];d=st['物理防御']['数值'];r=st['法抗']['数值']
        print(f"  {k} ×{v} [ATK={a} HP={h} DEF={d} RES={r}]")
    else:
        print(f"  {k} ×{v} [?]")
print(f"\n右方:")
for k,v in sorted(rt.items()):
    st=next((m for m in mdata if m['名字']==k),None)
    if st:
        a=st['攻击力']['数值'];h=st['生命值']['数值'];d=st['物理防御']['数值'];r=st['法抗']['数值']
        print(f"  {k} ×{v} [ATK={a} HP={h} DEF={d} RES={r}]")
    else:
        print(f"  {k} ×{v} [?]")
