import sys,io,json
sys.path.insert(0,r'G:\314\CannotMax-main')
from simulator.battle_field import Battlefield
from simulator.utils import Faction
mdata=json.load(open(r'G:\314\CannotMax-main\simulator\monsters.json',encoding='utf-8'))['monsters']
def n(p):
    for m in mdata:
        if p in m['名字']:return m['名字']

# Check key stats
for name in ['杰斯顿','源石畸变体','投石机','变异巨岩蛛']:
    for m in mdata:
        if name in m.get('名字',''):
            atk=m.get('攻击力',{}).get('数值')
            hp=m.get('生命值',{}).get('数值')
            df=m.get('物理防御',{}).get('数值')
            res=m.get('法抗',{}).get('数值')
            rng=m.get('攻击范围',{}).get('数值')
            iv=m.get('攻击间隔',{}).get('数值')
            print(f"{m['名字']}: ATK={atk} HP={hp} DEF={df} RES={res} RNG={rng} INT={iv}")

# Run battle
bf=Battlefield(mdata)
bf.setup_battle({n('杰斯顿'):1,n('畸变体'):6},{n('投石机'):6,n('巨岩蛛'):5},mdata)
out=[]
for f in range(10000):
    res=bf.run_one_frame()
    if res is not None:
        out.append(f"Winner={'L' if res==Faction.LEFT else 'R'} at frame{f}")
        for m in bf.monsters:
            s="[DEAD]" if not m.is_alive else f"HP={m.health:.0f}/{m.max_health:.0f}"
            out.append(f"  {m.name}{m.id} {s}")
        break
with open(r'G:\314\CannotMax-main\data\battle_row8.txt','w',encoding='utf-8') as f:
    f.write('\n'.join(out))
print('done')
