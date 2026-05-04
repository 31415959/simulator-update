import sys,io,json
sys.path.insert(0,r'G:\314\CannotMax-main')
from simulator.battle_field import Battlefield
mdata=json.load(open(r'G:\314\CannotMax-main\simulator\monsters.json',encoding='utf-8'))['monsters']

# Check behavior config for 巨岩蛛
for m in mdata:
    if '巨岩' in m.get('名字',''):
        bh = m.get('行为', [])
        print(f"JSON behaviors for {m['名字']}:")
        for b in bh:
            print(f"  {b}")

# Create and check
def n(p):
    for m in mdata:
        if p in m['名字']:return m['名字']
bf=Battlefield(mdata)
bf.setup_battle({n('杰斯顿'):1,n('畸变体'):6},{n('投石机'):6,n('巨岩蛛'):5},mdata)

spiders=[m for m in bf.monsters if '巨岩' in m.name]
for s in spiders[:1]:
    print(f"\n{s.name} behaviors at runtime: {len(s.behaviors)}")
    for b in s.behaviors:
        print(f"  {type(b).__name__} timer={getattr(b,'timer','?')}")
