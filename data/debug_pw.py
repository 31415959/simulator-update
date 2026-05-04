import sys,io,json
sys.path.insert(0,r'G:\314\CannotMax-main')
from simulator.battle_field import Battlefield
from simulator.utils import Faction
mdata=json.load(open(r'G:\314\CannotMax-main\simulator\monsters.json',encoding='utf-8'))['monsters']
def n(p):
    for m in mdata:
        if p in m['名字']:return m['名字']

bf=Battlefield(mdata)
bf.setup_battle({n('矿脉'):4},{n('破坏王'):6},mdata)

out=[]
for frame in range(5000):
    res=bf.run_one_frame()
    if frame>=200 and frame%200==0:
        L=[m for m in bf.alive_monsters if m.faction==Faction.LEFT and m.is_alive]
        R=[m for m in bf.alive_monsters if m.faction==Faction.RIGHT and m.is_alive]
        lhp=sum(m.health for m in L)
        rhp=sum(m.health for m in R)
        out.append(f"f{frame}: L={len(L)} HP={lhp:.0f} R={len(R)} HP={rhp:.0f}")
    if res is not None:
        out.append(f"\nWinner={'L' if res==Faction.LEFT else 'R'} at frame{frame}")
        for m in bf.monsters:
            s="[DEAD]" if not m.is_alive else ""
            out.append(f"  {m.name}{m.id} {s} HP={m.health:.0f}/{m.max_health:.0f}")
        break

with open(r'G:\314\CannotMax-main\data\battle_pw.txt','w',encoding='utf-8') as f:
    f.write('\n'.join(out))
print('done')
