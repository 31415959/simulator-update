import sys,io,json
sys.path.insert(0,r'G:\314\CannotMax-main')
from simulator.battle_field import Battlefield

mdata=json.load(open(r'G:\314\CannotMax-main\simulator\monsters.json',encoding='utf-8'))['monsters']
def n(p):
    for m in mdata:
        if p in m['名字']:return m['名字']

bf=Battlefield(mdata)
spider_name = n('巨岩蛛')
print(f"Spider name: {spider_name}")
bf.setup_battle({n('畸变体'):1},{spider_name:1},mdata)

# Find spider
spider = None
for m in bf.monsters:
    if spider_name in m.name:
        spider = m
        break

if spider:
    print(f"Behaviors: {len(spider.behaviors)}")
    for b in spider.behaviors:
        print(f"  {type(b).__name__}: timer={getattr(b,'timer','?')} total={getattr(b,'total_summoned','?')}")
    
    null=io.StringIO();old=sys.stdout;sys.stdout=null
    for f in range(500):
        bf.run_one_frame()
    sys.stdout=old
    
    for b in spider.behaviors:
        print(f"  final: {type(b).__name__} timer={getattr(b,'timer','?')} total={getattr(b,'total_summoned','?')}")
    
    spawns=[m for m in bf.monsters if '赘生物' in m.name]
    print(f"Spawns: {len(spawns)} ({sum(1 for s in spawns if s.is_alive)} alive)")
else:
    print("Spider not found!")
    for m in bf.monsters:
        print(f"  {m.name}")
