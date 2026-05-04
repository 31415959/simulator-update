import sys,io,json
sys.path.insert(0,r'G:\314\CannotMax-main')
from simulator.battle_field import Battlefield
from simulator.utils import Faction

mdata=json.load(open(r'G:\314\CannotMax-main\simulator\monsters.json',encoding='utf-8'))['monsters']
def n(p):
    for m in mdata:
        if p in m['名字']:return m['名字']

# Only put巨岩蛛 vs nothing on other side
bf=Battlefield(mdata)
bf.setup_battle({n('畸变体'):1},{n('巨岩蛛'):1},mdata)

spider=[m for m in bf.monsters if '巨岩蛛' in m.name or '巨岩' in m.name][0]
print(f"Spider behaviors: {len(spider.behaviors)}")
for b in spider.behaviors:
    print(f"  {type(b).__name__} timer={getattr(b,'timer','?')} total={getattr(b,'total_summoned','?')} name={getattr(b,'monster_name','?')}")

null=io.StringIO();old=sys.stdout;sys.stdout=null
for f in range(500):
    bf.run_one_frame()
    if f==400:
        for b in spider.behaviors:
            print(f"  f400: timer={getattr(b,'timer','?')} total={getattr(b,'total_summoned','?')}")
sys.stdout=old

for b in spider.behaviors:
    print(f"  final: {type(b).__name__} timer={getattr(b,'timer','?')} total={getattr(b,'total_summoned','?')}")

spawns=[m for m in bf.monsters if '赘生物' in m.name]
print(f"Spawns: {len(spawns)} ({sum(1 for s in spawns if s.is_alive)} alive)")
