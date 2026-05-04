import sys,os,json,io,time
sys.path.insert(0,r'G:\314\CannotMax-main')
os.chdir(r'G:\314\CannotMax-main')
from simulator.battle_field import Battlefield
from simulator.utils import Faction

with open('simulator/monsters.json',encoding='utf-8') as f:
    mdata = json.load(f)['monsters']

t0=time.time()
bf=Battlefield(mdata)
bf.setup_battle({'炮击组长':3},{'散华骑士团学徒':3},mdata)
null=io.StringIO()
old=sys.stdout
sys.stdout=null
frames=0
while True:
    res=bf.run_one_frame()
    frames+=1
    if res is not None:
        break
sys.stdout=old
winner='L' if res==Faction.LEFT else 'R'
with open(r'G:\314\CannotMax-main\data\quick1.txt','w') as f:
    f.write(f'winner={winner} frames={frames} time={time.time()-t0:.1f}s')
print('done')
