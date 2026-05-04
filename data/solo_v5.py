import sys,io,json
sys.path.insert(0,r'G:\314\CannotMax-main')
from simulator.battle_field import Battlefield, Faction

mdata=json.load(open(r'G:\314\CannotMax-main\simulator\monsters.json',encoding='utf-8'))['monsters']

spider_name = None
dummy_name = None
for m in mdata:
    n = m['名字']
    if '\u5de8\u5ca9\u86db' in n: spider_name = n
    if '\u9ad8\u666e' in n: dummy_name = n  # 高普尼克 as harmless dummy

with open(r'G:\314\CannotMax-main\data\spider_log3.txt','w',encoding='utf-8') as log:
    bf = Battlefield(mdata)
    # Just spider on right, nothing on left
    bf.setup_battle({}, {spider_name: 1}, mdata)
    log.write(f"Monsters after setup: {len(bf.monsters)}\n")
    
    null = io.StringIO()
    old = sys.stdout
    sys.stdout = null
    for f in range(3000):
        bf.run_one_frame()
        if f % 500 == 0:
            # Check spider behavior state
            for m in bf.alive_monsters:
                if spider_name in m.name:
                    for b in m.behaviors:
                        if 'Summon' in type(b).__name__:
                            log.write(f"f{f}: {type(b).__name__} timer={getattr(b,'timer','?'):.1f} total={getattr(b,'total_summoned','?')}\n")
    sys.stdout = old
    
    spawns = [m for m in bf.alive_monsters if '\u8d58\u751f\u7269' in m.name]
    log.write(f"\nFinal spawns: {len(spawns)} alive\n")
