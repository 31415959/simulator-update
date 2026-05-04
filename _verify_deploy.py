"""验证部署系统实际运行"""
import sys,os,json;sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import simulator.utils as u;u.VISUALIZATION_MODE=False
import logging as l;l.getLogger().setLevel(l.ERROR)
from simulator.battle_field import Battlefield,Faction
from simulator.utils import MONSTER_MAPPING
import pandas as pd

md=json.load(open("simulator/monsters.json",encoding="utf-8"))["monsters"]
df=pd.read_csv("arknights.csv",header=None,skiprows=1)
N=len(MONSTER_MAPPING)

row=df.iloc[9]  # Row9: 16v22
left={MONSTER_MAPPING[i]:int(row[i]) for i in range(N) if row[i]>0}
right={MONSTER_MAPPING[i]:int(row[N+i]) for i in range(N) if row[N+i]>0}
print(f"Row9: L={sum(left.values())}units R={sum(right.values())}units")

bf=Battlefield(md)
bf.setup_battle(left,right,md)

print(f"Temporal L: {len(bf.monster_temporal_area_left)} units")
print(f"Temporal R: {len(bf.monster_temporal_area_right)} units")

# 打印前几个单位的出生位置
print("First 5 LEFT spawn positions:")
for i in range(min(5, len(bf.monster_temporal_area_left))):
    m = bf.monster_temporal_area_left[i]
    print(f"  {m.name} at ({m.position.x:.2f}, {m.position.y:.2f})")
print("First 5 RIGHT spawn positions:")
for i in range(min(5, len(bf.monster_temporal_area_right))):
    m = bf.monster_temporal_area_right[i]
    print(f"  {m.name} at ({m.position.x:.2f}, {m.position.y:.2f})")

# 追踪部署
wave = 0
while True:
    r = bf.run_one_frame()
    # 检测冷却开始
    if bf._wave_cooldown == 30:
        wave += 1
        total_l = bf.current_spawn_left
        total_r = bf.current_spawn_right
        max_l = len(bf.monster_temporal_area_left)
        max_r = len(bf.monster_temporal_area_right)
        # 本波实际投放数
        print(f"  Wave{wave} end @frame{bf.round}: deployed {total_l}/{max_l}L + {total_r}/{max_r}R, cooldown=30")
    if r is not None:
        sim="LEFT" if r==Faction.LEFT else "RIGHT"
        print(f"Battle done: {sim} wins, {bf.round} frames, {bf.gameTime:.1f}s")
        break
