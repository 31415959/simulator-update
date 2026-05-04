import sys,io,json
sys.path.insert(0,r'G:\314\CannotMax-main')
from simulator.battle_field import Battlefield
from simulator.utils import Faction
mdata=json.load(open(r'G:\314\CannotMax-main\simulator\monsters.json',encoding='utf-8'))['monsters']
def n(p):
    for m in mdata:
        if p in m['名字']:return m['名字']

wl=0
for _ in range(10):
    bf=Battlefield(mdata)
    bf.setup_battle({n('沙滩车'):5,n('散华'):6,n('沉沙'):5},{n('R-11'):4,n('枯朽之种'):29,n('志愿者'):12},mdata)
    null=io.StringIO();old=sys.stdout;sys.stdout=null
    while True:
        res=bf.run_one_frame()
        if res is not None:
            if res==Faction.LEFT:wl+=1
            break
    sys.stdout=old
print(f'Row24: LEFT {wl}/10 RIGHT {10-wl}/10')
