import sys,os,json;sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import simulator.utils as u;u.VISUALIZATION_MODE=False
import logging as l;l.getLogger().setLevel(l.WARNING)
from simulator.battle_field import Battlefield,Faction
from simulator.utils import MONSTER_MAPPING
import pandas as pd

md=json.load(open("simulator/monsters.json",encoding="utf-8"))["monsters"]
df=pd.read_csv("arknights.csv",header=None,skiprows=1)
N=len(MONSTER_MAPPING)
row=df.iloc[9]

left={MONSTER_MAPPING[i]:int(row[i]) for i in range(N) if row[i]>0}
right={MONSTER_MAPPING[i]:int(row[N+i]) for i in range(N) if row[N+i]>0}
csv_w="R" if str(row[N*2]).strip().upper()=="R" else "L"

print(f"Row9: L={left} R={right} CSV={csv_w}")
bf=Battlefield(md)
bf.setup_battle(left,right,md)

# 记录每个单位死亡时的信息
death_log=[]
class TrackedBattlefield(Battlefield):
    pass

while True:
    result = bf.run_one_frame()
    if result is not None:
        sim_w = "L" if result==Faction.LEFT else "R"
        print(f"RESULT: CSV={csv_w} SIM={sim_w} frames={bf.round} time={bf.gameTime:.1f}s")
        la=len([m for m in bf.alive_monsters if m.is_alive and m.faction==Faction.LEFT])
        ra=len([m for m in bf.alive_monsters if m.is_alive and m.faction==Faction.RIGHT])
        print(f"Alive: L={la} R={ra}")
        
        # 列出存活单位
        print("Survivors:")
        for m in bf.alive_monsters:
            if m.is_alive:
                hp_pct=m.health/m.max_health*100
                print(f"  [{m.faction.name}] {m.name}#{m.id} HP={m.health:.0f}/{m.max_health:.0f} ({hp_pct:.0f}%) pos=({m.position.x:.1f},{m.position.y:.1f})")
        break
