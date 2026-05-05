import sys,os,json;sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
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

from collections import Counter
types = Counter()
for m in bf.monster_temporal_area_right:
    types[m.name] += 1
print(f"Right total: {len(bf.monster_temporal_area_right)}")
print(f"Types: {dict(types)}")
print()

for i, m in enumerate(bf.monster_temporal_area_right):
    if i == 0:
        print(f"--- Wave 1 ---")
    elif i == 18:
        print(f"--- Wave 2 ---")
    elif i == 36:
        print(f"--- Wave 3 ---")
    print(f"  [{i}] {m.name}")
