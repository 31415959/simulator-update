import sys,io,json
sys.path.insert(0,r'G:\314\CannotMax-main')
from simulator.battle_field import Battlefield
from simulator.utils import Faction
mdata=json.load(open(r'G:\314\CannotMax-main\simulator\monsters.json',encoding='utf-8'))['monsters']
def n(p):
    for m in mdata:
        if p in m['名字']:return m['名字']

bf=Battlefield(mdata)
bf.setup_battle({n('杰斯顿'):1,n('畸变体'):6},{n('投石机'):6,n('巨岩蛛'):5},mdata)

out=[]
spiders=[m for m in bf.monsters if '巨岩' in m.name]
for s in spiders[:1]:
    out.append(f"{s.name}: behaviors={len(s.behaviors)}")
    for b in s.behaviors:
        cls=type(b).__name__
        d={}
        if hasattr(b,'__dict__'):
            for k,v in b.__dict__.items():
                if k != 'owner':
                    d[k]=v
        out.append(f"  {cls}: {d}")

# Run frames
null=io.StringIO();old=sys.stdout;sys.stdout=null
for f in range(300):
    bf.run_one_frame()
sys.stdout=old

spawns=[m for m in bf.alive_monsters if '赘生物' in m.name and m.is_alive]
out.append(f"After 300f: {len(spawns)}赘生物 alive, total={len(bf.monsters)}")

# Check if 畸变赘生物 exists in mdata
found=[m['名字'] for m in mdata if '赘生物' in m['名字']]
out.append(f"赘生物 in mdata: {found}")

with open(r'G:\314\CannotMax-main\data\spider_diag.txt','w',encoding='utf-8') as f:
    f.write('\n'.join(out))
print('done')
