import sys,io,json,traceback
sys.path.insert(0,r'G:\314\CannotMax-main')
from simulator.battle_field import Battlefield
mdata=json.load(open(r'G:\314\CannotMax-main\simulator\monsters.json',encoding='utf-8'))['monsters']
def n(p):
    for m in mdata:
        if p in m['名字']:return m['名字']
try:
    bf=Battlefield(mdata)
    bf.setup_battle({n('杰斯顿'):1,n('畸变体'):6},{n('投石机'):6,n('巨岩蛛'):5},mdata)
    spiders=[m for m in bf.monsters if '巨岩' in m.name]
    for s in spiders[:1]:
        print(f"{s.name} behaviors={len(s.behaviors)}")
        for b in s.behaviors:
            print(f"  {type(b).__name__} timer={getattr(b,'timer','?')} total={getattr(b,'total_summoned','?')}")
    null=io.StringIO();old=sys.stdout;sys.stdout=null
    for f in range(600):
        bf.run_one_frame()
    sys.stdout=old
    for s in spiders[:1]:
        for b in s.behaviors:
            print(f"  After 600f: {type(b).__name__} timer={getattr(b,'timer','?')} total={getattr(b,'total_summoned','?')}")
    spawns=[m for m in bf.alive_monsters if '赘生物' in m.name]
    print(f"赘生物: {len(spawns)} alive/{sum(1 for m in bf.monsters if '赘生物' in m.name)} total")
except Exception as e:
    traceback.print_exc()
