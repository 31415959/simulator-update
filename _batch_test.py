import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import simulator.utils as u
u.VISUALIZATION_MODE = False
import logging
logging.getLogger().setLevel(logging.ERROR)

from simulator.battle_field import Battlefield, Faction
from simulator.utils import MONSTER_MAPPING, REVERSE_MONSTER_MAPPING
import pandas as pd
import concurrent.futures

monster_file = 'simulator/monsters.json'
with open(monster_file, encoding='utf-8') as f:
    monster_data = json.load(f)['monsters']
json_names = {m['名字'] for m in monster_data}

csv_path = 'arknights.csv'
df = pd.read_csv(csv_path, header=None, skiprows=1)
N = len(MONSTER_MAPPING)

total = min(100, len(df))
results = []
skipped = 0

def sim_one(idx_row):
    idx, row = idx_row
    left_army = {MONSTER_MAPPING[i]: int(row[i]) for i in range(N) if row[i] > 0}
    right_army = {MONSTER_MAPPING[i]: int(row[N+i]) for i in range(N) if row[N+i] > 0}
    
    # 跳过缺失怪物
    for name in list(left_army.keys()) + list(right_army.keys()):
        if name not in json_names:
            return None
    
    csv_winner = 'L' if str(row[N*2]).strip().upper() == 'L' else 'R'
    left_wins = 0
    for _ in range(3):
        bf = Battlefield(monster_data)
        bf.setup_battle(left_army, right_army, monster_data)
        if bf.run_battle() == Faction.LEFT:
            left_wins += 1
    sim_winner = 'L' if left_wins >= 2 else 'R'
    return (idx, sim_winner == csv_winner, sim_winner, csv_winner, left_wins)

valid = [(i, row) for i, (_, row) in enumerate(df.iterrows()) if i < total]
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
    for res in pool.map(sim_one, valid):
        if res is None:
            skipped += 1
        else:
            results.append(res)

correct = sum(1 for r in results if r[1])
acc = correct / len(results) * 100 if results else 0
print(f'总对局: {len(results)}, 跳过: {skipped}, 正确: {correct}, 准确率: {acc:.1f}%')

# 显示错误对局
for r in results:
    if not r[1]:
        print(f'  Row{r[0]}: SIM={r[2]} CSV={r[3]} ({r[4]}/3)')
