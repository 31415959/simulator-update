import sys,os,json;sys.path.insert(0,os.path.dirname(__file__))
import simulator.utils as u;u.VISUALIZATION_MODE=False
import logging as l;l.getLogger().setLevel(l.ERROR)
from simulator.battle_field import Battlefield,Faction
from simulator.utils import MONSTER_MAPPING
import pandas as pd

md=json.load(open("simulator/monsters.json",encoding="utf-8"))["monsters"]
df=pd.read_csv("arknights.csv",header=None,skiprows=1)
N=len(MONSTER_MAPPING)

wrong=[]
for idx in range(15):
    row=df.iloc[idx]
    left={MONSTER_MAPPING[i]:int(row[i]) for i in range(N) if row[i]>0}
    right={MONSTER_MAPPING[i]:int(row[N+i]) for i in range(N) if row[N+i]>0}
    csv_w="L" if str(row[N*2]).strip().upper()=="L" else "R"
    bf=Battlefield(md);bf.setup_battle(left,right,md)
    sim_w="L" if bf.run_battle()==Faction.LEFT else "R"
    ok="OK" if sim_w==csv_w else "MISS"
    lt=sum(left.values());rt=sum(right.values())
    lnames="+".join(f"{n}x{c}" for n,c in left.items())[:80]
    rnames="+".join(f"{n}x{c}" for n,c in right.items())[:80]
    print(f"Row{idx}: {lt}v{rt} CSV={csv_w} SIM={sim_w} {ok}")
    if ok=="MISS":
        print(f"  L: {lnames}")
        print(f"  R: {rnames}")
        wrong.append(idx)
print(f"\nMISS: {len(wrong)}/15")
