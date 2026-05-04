import sys,io,time,json
sys.path.insert(0,r'G:\314\CannotMax-main')
from simulator.battle_field import Battlefield
from simulator.utils import Faction
mdata=json.load(open(r'G:\314\CannotMax-main\simulator\monsters.json',encoding='utf-8'))['monsters']
def n(p):
    for m in mdata:
        if p in m['名字']:return m['名字']
wl=wr=0;t0=time.time()
for _ in range(10):
    bf=Battlefield(mdata);bf.setup_battle({n('矿脉'):4},{n('破坏王'):6},mdata)
    null=io.StringIO();old=sys.stdout;sys.stdout=null
    while True:
        res=bf.run_one_frame()
        if res is not None:
            if res==Faction.LEFT:wl+=1
            else:wr+=1
            break
    sys.stdout=old
with open(r'G:\314\CannotMax-main\data\test_row1.txt','w') as f:
    f.write(f'矿脉4vs破坏王6: LEFT {wl}/10 RIGHT {wr}/10')
print('done')
