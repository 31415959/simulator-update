import sys,io,json
sys.path.insert(0,r'G:\314\CannotMax-main')
from simulator.battle_field import Battlefield
from simulator.utils import Faction
mdata=json.load(open(r'G:\314\CannotMax-main\simulator\monsters.json',encoding='utf-8'))['monsters']
def n(p):
    for m in mdata:
        if p in m['名字']:return m['名字']
wl=0
for _ in range(5):
    bf=Battlefield(mdata);bf.setup_battle({n('杰斯顿'):1,n('畸变体'):6},{n('投石机'):6,n('巨岩蛛'):5},mdata)
    null=io.StringIO();old=sys.stdout;sys.stdout=null
    while True:
        res=bf.run_one_frame()
        if res is not None:
            if res==Faction.LEFT:wl+=1
            break
    sys.stdout=old
with open(r'G:\314\CannotMax-main\data\test_row8.txt','w') as f:
    f.write(f'Row8: LEFT {wl}/5')
print('done')
