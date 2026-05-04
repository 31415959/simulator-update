import sys,io,json
sys.path.insert(0,r'G:\314\CannotMax-main')
from simulator.battle_field import Battlefield

mdata=json.load(open(r'G:\314\CannotMax-main\simulator\monsters.json',encoding='utf-8'))['monsters']
def n(p):
    for m in mdata:
        if p in m['名字']:return m['名字']

bf=Battlefield(mdata)
spider_name = n('巨岩蛛')
print(f"Spider name: {repr(spider_name)}")
bf.setup_battle({n('畸变体'):1},{spider_name:1},mdata)

# List all
for m in bf.monsters:
    print(f"  [{repr(m.name)}] behaviors={len(m.behaviors)} alive={m.is_alive}")
    for b in m.behaviors:
        print(f"    {type(b).__name__} timer={getattr(b,'timer','?')} total={getattr(b,'total_summoned','?')}")
