import sys,io,json,traceback
sys.path.insert(0,r'G:\314\CannotMax-main')
from simulator.battle_field import Battlefield

mdata=json.load(open(r'G:\314\CannotMax-main\simulator\monsters.json',encoding='utf-8'))['monsters']

with open(r'G:\314\CannotMax-main\data\spider_log.txt','w',encoding='utf-8') as log:
    def pl(msg):
        log.write(str(msg)+'\n')
        print(msg)
    
    # Find names by exact matching
    spider_jname = None
    bug_jname = None
    for m in mdata:
        n = m['名字']
        if '\u5de8\u5ca9\u86db' in n:  # 巨岩蛛
            spider_jname = n
        if '\u7578\u53d8\u4f53' in n:  # 畸变体
            bug_jname = n
    
    pl(f"Spider JSON name: {repr(spider_jname)}")
    pl(f"Bug JSON name: {repr(bug_jname)}")
    
    if not spider_jname or not bug_jname:
        pl("Names not found!")
        exit()
    
    try:
        bf = Battlefield(mdata)
        bf.setup_battle({bug_jname:1}, {spider_jname:1}, mdata)
        
        pl(f"Monsters after setup: {len(bf.monsters)}")
        for m in bf.monsters:
            pl(f"  {m.name} alive={m.is_alive} behaviors={len(m.behaviors)}")
            for b in m.behaviors:
                pl(f"    {type(b).__name__}: timer={getattr(b,'timer','?')} total={getattr(b,'total_summoned','?')}")
        
        # Run frames
        pl("\nRunning 500 frames...")
        null = io.StringIO()
        old = sys.stdout
        sys.stdout = null
        for _ in range(500):
            bf.run_one_frame()
        sys.stdout = old
        
        spawns = [m for m in bf.monsters if '\u8d58\u751f\u7269' in m.name]  # 赘生物
        pl(f"Spawns: {len(spawns)} total, {sum(1 for s in spawns if s.is_alive)} alive")
        
        # Behavior state
        for m in bf.monsters:
            if spider_jname in m.name:
                for b in m.behaviors:
                    pl(f"  Final {type(b).__name__}: timer={getattr(b,'timer','?')} total={getattr(b,'total_summoned','?')}")
    except Exception as e:
        pl(f"ERROR: {e}")
        pl(traceback.format_exc())
