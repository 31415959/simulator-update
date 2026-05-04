import sys,json
sys.path.insert(0,r'G:\314\CannotMax-main')
from simulator.monsters import MonsterFactory
from simulator.vector2d import FastVector

mdata=json.load(open(r'G:\314\CannotMax-main\simulator\monsters.json',encoding='utf-8'))['monsters']

spider_data = None
for m in mdata:
    if '\u5de8\u5ca9\u86db' in m['名字']:
        spider_data = m
        break

if spider_data:
    print(f"Data keys: {list(spider_data.keys())}")
    bh = spider_data.get('行为', [])
    print(f"Behavior config: {len(bh)} entries")
    for b in bh:
        print(f"  {b}")
    
    # Actually create a monster with a dummy battlefield
    class DummyBF:
        map_size = (14, 14)
        gameTime = 0
        def __init__(self):
            self.monsters = []
            self.alive_monsters = []
        def append_monster_name(self, name, faction, pos):
            print(f"  append_monster_name: {name}")
            return None  # We just want to see if it's called
    
    bf = DummyBF()
    from simulator.utils import Faction
    m = MonsterFactory.create_monster(spider_data, Faction.RIGHT, FastVector(1,1), bf)
    print(f"\nCreated: {m.name}")
    print(f"Behaviors: {len(m.behaviors)}")
    for b in m.behaviors:
        print(f"  {type(b).__name__}: timer={getattr(b,'timer','?')} interval={getattr(b,'interval','?')} name={getattr(b,'monster_name','?')}")
        # Try updating a few times
        for _ in range(10):
            b.on_update(0.1)  # simulate 100ms frames
        print(f"  after 1s: timer={getattr(b,'timer','?'):.2f} total={getattr(b,'total_summoned','?')}")
