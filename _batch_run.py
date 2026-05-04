"""分批模拟：每次12局，逐批累加结果，避免超时"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import simulator.utils as u
u.VISUALIZATION_MODE = False
import logging; logging.getLogger().setLevel(logging.ERROR)

from simulator.battle_field import Battlefield, Faction
from simulator.utils import MONSTER_MAPPING
import pandas as pd

md = json.load(open("simulator/monsters.json", encoding="utf-8"))["monsters"]
df = pd.read_csv("arknights.csv", header=None, skiprows=1)
N = len(MONSTER_MAPPING)

TOTAL = 100
BATCH = 12
correct = 0
done = 0

for start in range(0, TOTAL, BATCH):
    end = min(start + BATCH, TOTAL)
    batch_results = []
    
    for idx in range(start, end):
        row = df.iloc[idx]
        left_army = {MONSTER_MAPPING[i]: int(row[i]) for i in range(N) if row[i] > 0}
        right_army = {MONSTER_MAPPING[i]: int(row[N+i]) for i in range(N) if row[N+i] > 0}
        csv_winner = "L" if str(row[N*2]).strip().upper() == "L" else "R"
        
        bf = Battlefield(md)
        bf.setup_battle(left_army, right_army, md)
        sim_winner = "L" if bf.run_battle() == Faction.LEFT else "R"
        
        ok = sim_winner == csv_winner
        if ok:
            correct += 1
        done += 1
        batch_results.append(f"  Row{idx}: CSV={csv_winner} SIM={sim_winner} {'OK' if ok else 'MISS'}")
    
    print(f"[{start+1}-{end}] 本批正确: {sum(1 for r in batch_results if 'OK' in r)}/{len(batch_results)}")
    for r in batch_results:
        if "MISS" in r:
            print(r)
    print(f"累计: {correct}/{done} = {correct/done*100:.1f}%\n")

print(f"\n=== 最终: {correct}/{TOTAL} = {correct/TOTAL*100:.1f}% ===")
