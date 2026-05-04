import sys,io,json,traceback
sys.path.insert(0,r'G:\314\CannotMax-main')
from simulator.battle_field import Battlefield

mdata=json.load(open(r'G:\314\CannotMax-main\simulator\monsters.json',encoding='utf-8'))['monsters']

# Find names
spider_name = None
bug_name = None
for m in mdata:
    n = m['名字']
    if '\u5de8\u5ca9\u86db' in n: spider_name = n
    if '\u7578\u53d8\u4f53' in n: bug_name = n

with open(r'G:\314\CannotMax-main\data\spider_log2.txt','w',encoding='utf-8') as log:
    try:
        bf = Battlefield(mdata)
        log.write(f"setup with {repr(bug_name)} vs {repr(spider_name)}\n")
        bf.setup_battle({bug_name: 1}, {spider_name: 1}, mdata)
        log.write(f"monsters: {len(bf.monsters)}\n")
        for m in bf.monsters:
            log.write(f"  [{m.name}] behaviors={len(m.behaviors)} alive={m.is_alive}\n")
            for b in m.behaviors:
                log.write(f"    {type(b).__name__}: timer={getattr(b,'timer','?')} total={getattr(b,'total_summoned','?')}\n")
        
        log.write("\nRunning 1000 frames...\n")
        null = io.StringIO()
        old = sys.stdout
        sys.stdout = null
        for _ in range(1000):
            bf.run_one_frame()
        sys.stdout = old
        
        spawns = [m for m in bf.monsters if '\u8d58\u751f\u7269' in m.name]
        log.write(f"Spawns: {len(spawns)} ({sum(1 for s in spawns if s.is_alive)} alive)\n")
        
        for m in bf.monsters:
            if spider_name in m.name:
                for b in m.behaviors:
                    log.write(f"  Final {type(b).__name__}: timer={getattr(b,'timer','?')} total={getattr(b,'total_summoned','?')}\n")
    except Exception as e:
        log.write(f"ERROR: {e}\n{traceback.format_exc()}\n")
