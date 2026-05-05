import sys,os,json;sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import simulator.utils as u;u.VISUALIZATION_MODE=False
import logging as l;l.getLogger().setLevel(l.ERROR)
from simulator.battle_field import Battlefield,Faction
from simulator.utils import MONSTER_MAPPING
import pandas as pd

md=json.load(open("simulator/monsters.json",encoding="utf-8"))["monsters"]
df=pd.read_csv("arknights.csv",header=None,skiprows=1)
N=len(MONSTER_MAPPING)
row=df.iloc[23]
left={MONSTER_MAPPING[i]:int(row[i]) for i in range(N) if row[i]>0}
right={MONSTER_MAPPING[i]:int(row[N+i]) for i in range(N) if row[N+i]>0}

bf=Battlefield(md);bf.setup_battle(left,right,md)
print(f"Left units: {len(bf.monster_temporal_area_left)}, Right: {len(bf.monster_temporal_area_right)}")

wave=0
while True:
    r=bf.run_one_frame()
    if bf._wave_cooldown==30 and bf._wave_deployed_left==0 and bf._wave_deployed_right==0:
        wave+=1
        print(f"Wave{wave} end @f{bf.round}: L={bf.current_spawn_left}/{len(bf.monster_temporal_area_left)} R={bf.current_spawn_right}/{len(bf.monster_temporal_area_right)}")
    if r is not None:
        s="LEFT" if r==Faction.LEFT else "RIGHT"
        print(f"Result: {s} f={bf.round}")
        break
