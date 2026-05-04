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

# Find巨岩蛛 and check behaviors
spiders=[m for m in bf.monsters if '巨岩' in m.name]
for s in spiders[:1]:
    print(f"{s.name} behaviors: {len(s.behaviors)}")
    for b in s.behaviors:
        print(f"  {type(b).__name__}: {vars(b) if hasattr(b,'__dict__') else '?'}")

# Run 30 frames and check for summons
null=io.StringIO();old=sys.stdout;sys.stdout=null
for f in range(300):
    bf.run_one_frame()
sys.stdout=old

# Count畸变赘生物
spawns=[m for m in bf.alive_monsters if '赘生物' in m.name and m.is_alive]
print(f"After 300 frames: {len(spawns)} 赘生物 alive")
print(f"Total monsters: {len(bf.monsters)}")
