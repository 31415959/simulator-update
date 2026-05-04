"""Row17 详细日志：门x5 vs 百夫长x4+阿咬x32"""
import sys,os,json;sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import simulator.utils as u;u.VISUALIZATION_MODE=False
import logging as l;l.getLogger().setLevel(l.WARNING)
from simulator.battle_field import Battlefield,Faction
from simulator.utils import MONSTER_MAPPING
import pandas as pd

md=json.load(open("simulator/monsters.json",encoding="utf-8"))["monsters"]
df=pd.read_csv("arknights.csv",header=None,skiprows=1)
N=len(MONSTER_MAPPING)
row=df.iloc[17]

left={MONSTER_MAPPING[i]:int(row[i]) for i in range(N) if row[i]>0}
right={MONSTER_MAPPING[i]:int(row[N+i]) for i in range(N) if row[N+i]>0}
csv_w="R" if str(row[N*2]).strip().upper()=="R" else "L"

print(f"Row17: L={left} R={right} CSV={csv_w}")
bf=Battlefield(md)
bf.setup_battle(left,right,md)

# 追踪关键事件
death_log=[]

# Monkey-patch on_death to log
orig_od = {}
for m in bf.monster_temporal_area_left + bf.monster_temporal_area_right:
    orig_od[m] = m.on_death
    def make_logger(mon):
        orig = mon.on_death
        def logged():
            print(f"[DEATH@{bf.gameTime:.1f}s] {mon.name}#{mon.id} [{mon.faction.name}] HP={mon.health:.0f} pos=({mon.position.x:.1f},{mon.position.y:.1f})")
            orig()
        return logged
    m.on_death = make_logger(m)

# 每60帧打印战场概况
while True:
    result = bf.run_one_frame()
    if bf.round % 180 == 0:
        la=len([m for m in bf.alive_monsters if m.is_alive and m.faction==Faction.LEFT])
        ra=len([m for m in bf.alive_monsters if m.is_alive and m.faction==Faction.RIGHT])
        print(f"[{bf.gameTime:.0f}s] frame={bf.round} L_alive={la} R_alive={ra}")
    if result is not None:
        sim_w="LEFT" if result==Faction.LEFT else "RIGHT"
        la=len([m for m in bf.alive_monsters if m.is_alive and m.faction==Faction.LEFT])
        ra=len([m for m in bf.alive_monsters if m.is_alive and m.faction==Faction.RIGHT])
        print(f"\nRESULT: CSV={csv_w} SIM={sim_w} frames={bf.round} gameTime={bf.gameTime:.1f}s L_alive={la} R_alive={ra}")
        for m in bf.alive_monsters:
            if m.is_alive:
                pct=m.health/m.max_health*100
                print(f"  [{m.faction.name}] {m.name}#{m.id} HP={m.health:.0f}/{m.max_health:.0f} ({pct:.0f}%)")
        break
