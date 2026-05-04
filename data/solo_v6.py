import sys,io,json
sys.path.insert(0,r'G:\314\CannotMax-main')
from simulator.battle_field import Battlefield

mdata=json.load(open(r'G:\314\CannotMax-main\simulator\monsters.json',encoding='utf-8'))['monsters']

spider_name = None
for m in mdata:
    if '\u5de8\u5ca9\u86db' in m['名字']: spider_name = m['名字']

with open(r'G:\314\CannotMax-main\data\spider_log4.txt','w',encoding='utf-8') as log:
    bf = Battlefield(mdata)
    bf.setup_battle({}, {spider_name: 1}, mdata)
    log.write(f"Monsters: {len(bf.monsters)}, temporal L={len(bf.monster_temporal_area_left)} R={len(bf.monster_temporal_area_right)}\n")
    
    null = io.StringIO()
    old = sys.stdout
    sys.stdout = null
    for f in range(3000):
        res = bf.run_one_frame()
        if res is not None:
            log.write(f"Battle ended at f{f}: {res}\n")
            break
        if f % 500 == 0:
            for m in bf.alive_monsters:
                if spider_name in m.name:
                    for b in m.behaviors:
                        t = getattr(b, 'timer', '?')
                        tot = getattr(b, 'total_summoned', '?')
                        log.write(f"f{f}: {type(b).__name__} timer={t} total={tot}\n")
    sys.stdout = old
    
    spawns = [m for m in bf.alive_monsters if '\u8d58\u751f\u7269' in m.name and m.is_alive]
    log.write(f"\nAlive spawns: {len(spawns)}\n")
    all_spawns = [m for m in bf.monsters if '\u8d58\u751f\u7269' in m.name]
    log.write(f"Total spawns ever: {len(all_spawns)}\n")
