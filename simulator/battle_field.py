import json
import math
import random
import time
import numpy as np
from enum import Enum
import logging

from typing import TYPE_CHECKING

from .vector2d import FastVector

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from .monsters import Monster
    
from .monsters import MonsterFactory
from .utils import VIRTUAL_TIME_DELTA, BuffEffect, BuffType, Faction, SpatialHash
from .zone import PoisonZone

# 场景参数
MAP_SIZE = np.array([13, 9])  # 场景宽度（单位：格）

# 分批投放参数
WAVE_SIZE = 18           # 每波每边投放数
WAVE_COOLDOWN = 30       # 波间冷却帧数 (1秒 @30fps)
DEPLOY_INTERVAL = 1      # 波内每帧投放一个（18帧≈0.6s出完一波）

# 出生门配置（每边9个门，均匀分布在y轴）
DOOR_COUNT = 9
DOOR_SPAWN_RADIUS = 0.2  # 门中心半径0.2范围内随机出生
LEFT_DOORS = [FastVector(0.5, 0.5 + i) for i in range(DOOR_COUNT)]
RIGHT_DOORS = [FastVector(12.5, 0.5 + i) for i in range(DOOR_COUNT)]


from collections import defaultdict
from .projectiles import ProjectileManager

class Battlefield:
    def __init__(self, monster_data):
        self.monsters : list[Monster] = []
        self.alive_monsters : list[Monster] = []
        self.hash_grid : SpatialHash = SpatialHash(self, cell_size=0.5)
        self.HIT_BOX_RADIUS = 0.2

        self.round = 0
        self.map_size = MAP_SIZE
        self.monster_data = monster_data
        self.globalId = 0
        self.effect_zones = []
        self.dead_count = {Faction.LEFT: 0, Faction.RIGHT: 0}
        self.gameTime = 0

        self.effect_zones.append(PoisonZone(self))
        self.projectiles_manager = ProjectileManager(self)

        # 开始前把怪物放在待定区域，逐步放入场地
        self.monster_temporal_area_left = []
        self.monster_temporal_area_right = []
        self.current_spawn_left = 0
        self.current_spawn_right = 0
        # 分批投放状态
        self._wave_deployed_left = 0
        self._wave_deployed_right = 0
        self._wave_cooldown = 0

    @staticmethod
    def _random_door_pos(faction):
        """从对应阵营的9个门中随机选一个，在半径0.2范围内随机出生"""
        doors = LEFT_DOORS if faction == Faction.LEFT else RIGHT_DOORS
        door = random.choice(doors)
        angle = random.uniform(0, 2 * math.pi)
        r = random.uniform(0, DOOR_SPAWN_RADIUS)
        return FastVector(door.x + r * math.cos(angle), door.y + r * math.sin(angle))

    def query_monster(self, target_position, radius) -> list['Monster']:
        results = []
        if len(self.alive_monsters) < (radius / self.hash_grid.cell_size) ** 2:
            for m in self.alive_monsters:
                if m.is_alive and (m.position - target_position).magnitude <= radius:
                    results.append(m)
        else:
            for id in self.hash_grid.query_neighbors(target_position, radius):
                m = self.get_monster_with_id(id)
                if m.is_alive and (m.position - target_position).magnitude <= radius:
                    results.append(m)
        return results

    def append_monster(self, monster : 'Monster'):
        """添加一个怪物到战场"""
        id = self.globalId
        monster.id = id
        self.globalId += 1
        self.monsters.append(monster)
        self.hash_grid.insert(monster.position, monster.id)
    
    def append_monster_name(self, name, faction, pos) -> 'Monster':
        """添加一个怪物到战场，仅需名字。找不到时从 MONSTER_MAPPING 回退"""
        data = next((m for m in self.monster_data if m["名字"] == name), None)
        if data is None:
            # 回退：尝试 MONSTER_MAPPING 反向查找
            from .utils import REVERSE_MONSTER_MAPPING
            alt_name = REVERSE_MONSTER_MAPPING.get(name)
            if alt_name:
                data = next((m for m in self.monster_data if m["名字"] == alt_name), None)
            if data is None:
                data = next((m for m in self.monster_data if m["名字"].replace('"','').replace('"','') == name.replace('"','').replace('"','')), None)
        if data is None:
            return None
        id = self.globalId
        monster = MonsterFactory.create_monster(data, faction, pos, self)
        monster.id = id
        self.globalId += 1
        self.monsters.append(monster)
        self.hash_grid.insert(monster.position, monster.id)
        return monster

    def get_monster_with_id(self, id) -> 'Monster':
        return self.monsters[id]
    
    def setup_battle(self, left_army, right_army, monster_data):
        """二维战场初始化（使用 self.monster_data 以应用绿藤城规则）"""
        from .utils import REVERSE_MONSTER_MAPPING
        md = self.monster_data  # 使用已调整的数据
        # 左阵营生成在左侧门区域
        for (name, count) in left_army.items():
            data = next((m for m in md if m["名字"] == name), None)
            if data is None:
                alt = REVERSE_MONSTER_MAPPING.get(name)
                if alt:
                    data = next((m for m in md if m["名字"] == alt), None)
            if data is None:
                # 模糊匹配：处理弯引号差异（如 "屠谕者" vs 屠谕者）
                data = next((m for m in md if m["名字"].replace('"','').replace('\u201c','').replace('\u201d','') == name.replace('"','').replace('\u201c','').replace('\u201d','')), None)
            if data is None:
                raise ValueError(f"左侧怪物 {name} 在 monster_data 中未找到!")
            allies = data.get("协同", [])
            for _ in range(count):
                pos = self._random_door_pos(Faction.LEFT)
                self.monster_temporal_area_left.append( MonsterFactory.create_monster(data, Faction.LEFT, pos, self))
                for ally_name in allies:
                    ally_data = next((m for m in md if m["名字"] == ally_name), None)
                    if ally_data:
                        pos = self._random_door_pos(Faction.LEFT)
                        self.monster_temporal_area_left.append( MonsterFactory.create_monster(ally_data, Faction.LEFT, pos, self))

        # 右阵营生成在右侧门区域
        for (name, count) in right_army.items():
            data = next((m for m in md if m["名字"] == name), None)
            if data is None:
                alt = REVERSE_MONSTER_MAPPING.get(name)
                if alt:
                    data = next((m for m in md if m["名字"] == alt), None)
            if data is None:
                # 模糊匹配：处理弯引号差异
                data = next((m for m in md if m["名字"].replace('"','').replace('\u201c','').replace('\u201d','') == name.replace('"','').replace('\u201c','').replace('\u201d','')), None)
            if data is None:
                raise ValueError(f"右侧怪物 {name} 在 monster_data 中未找到!")
            allies = data.get("协同", [])
            for _ in range(count):
                pos = self._random_door_pos(Faction.RIGHT)
                self.monster_temporal_area_right.append(MonsterFactory.create_monster(data, Faction.RIGHT, pos, self))
                for ally_name in allies:
                    ally_data = next((m for m in md if m["名字"] == ally_name), None)
                    if ally_data:
                        pos = self._random_door_pos(Faction.RIGHT)
                        self.monster_temporal_area_right.append(MonsterFactory.create_monster(ally_data, Faction.RIGHT, pos, self))

        self.alive_monsters = self.monsters
        self.gameTime = 0
        self.current_spawn = 0
        # 每波内各类型均分名额，波内打乱顺序
        self._interleave_deployment(self.monster_temporal_area_left)
        self._interleave_deployment(self.monster_temporal_area_right)
        return True

    @staticmethod
    def _interleave_deployment(units):
        """每波内各类型均分名额，波内随机打乱"""
        from collections import defaultdict
        by_name = defaultdict(list)
        for u in units:
            by_name[u.name].append(u)
        remaining = {n: len(g) for n, g in by_name.items()}
        types = list(by_name.keys())
        result = []
        while any(remaining.values()):
            active = [t for t in types if remaining[t] > 0]
            if not active:
                break
            per_type = max(1, WAVE_SIZE // len(active))
            wave_units = []
            for t in active:
                take = min(per_type, remaining[t])
                for _ in range(take):
                    wave_units.append(by_name[t].pop())
                remaining[t] -= take
            random.shuffle(wave_units)
            result.extend(wave_units)
        units.clear()
        units.extend(result)


    def check_victory(self):
        """检查胜利条件"""
        if self.current_spawn_left < len(self.monster_temporal_area_left) or self.current_spawn_right < len(self.monster_temporal_area_right):
            return None
        alive_factions = set()
        for m in self.alive_monsters:
            if m.is_alive:
                alive_factions.add(m.faction)
        
        if len(alive_factions) == 1:
            return list(alive_factions)[0]
        elif len(alive_factions) == 0:
            return Faction.LEFT
        return None
    
    def check_zone(self):
        new_zone = []
        # 检查场地效果
        for zone in self.effect_zones:
            zone.update(VIRTUAL_TIME_DELTA)
            if zone.should_clear(VIRTUAL_TIME_DELTA):
                continue
            for m in self.alive_monsters:
                if zone.contains(m):
                    zone.apply_effect(m)
            new_zone.append(zone)
        self.effect_zones = new_zone

    def run_one_frame(self):
        self.round += 1

        # === 分批投放：每波≤18/边，波间冷却1秒（30帧），波内每帧1只 ===
        if self._wave_cooldown > 0:
            self._wave_cooldown -= 1
        else:
            has_left = self.current_spawn_left < len(self.monster_temporal_area_left)
            has_right = self.current_spawn_right < len(self.monster_temporal_area_right)
            if has_left or has_right:
                if self.round % DEPLOY_INTERVAL == 0:
                    if has_left:
                        self.append_monster(self.monster_temporal_area_left[self.current_spawn_left])
                        self.current_spawn_left += 1
                        self._wave_deployed_left += 1
                    if has_right:
                        self.append_monster(self.monster_temporal_area_right[self.current_spawn_right])
                        self.current_spawn_right += 1
                        self._wave_deployed_right += 1

                    # 两边都达到波次上限（或无剩余单位）→ 进入冷却
                    left_done = (self.current_spawn_left >= len(self.monster_temporal_area_left)
                                 or self._wave_deployed_left >= WAVE_SIZE)
                    right_done = (self.current_spawn_right >= len(self.monster_temporal_area_right)
                                  or self._wave_deployed_right >= WAVE_SIZE)
                    if left_done and right_done:
                        self._wave_cooldown = WAVE_COOLDOWN
                        self._wave_deployed_left = 0
                        self._wave_deployed_right = 0

        self.check_zone()
        self.projectiles_manager.update_all(VIRTUAL_TIME_DELTA)
        # 更新所有单位
        for m in self.monsters:
            m.update(VIRTUAL_TIME_DELTA)
        for m in self.monsters:
            m.do_move(VIRTUAL_TIME_DELTA)
            if m.is_alive:
                self.hash_grid.insert(m.position, m.id)
        # 检查胜利条件
        self.alive_monsters = [m for m in self.monsters if m.is_alive]
        winner = self.check_victory()
        if winner:
            logger.info(f"\nVictory for {winner.name}!")
            left = len([m for m in self.alive_monsters if m.is_alive and m.faction == Faction.LEFT])
            logger.info(f"左边存活{left} / 右边存活{len(self.alive_monsters) - left}")
            return winner
        
        self.gameTime += VIRTUAL_TIME_DELTA
        return None
    
    def run_battle(self, visualize=False):
        """运行战斗直到决出胜负"""
        while True:
            if visualize and self.round % 30 == 0:
                self.print_battlefield()
                time.sleep(1)
            
            result = self.run_one_frame()
            if result != None:
                return result

    def danger_zone_size(self):
        if self.gameTime < 40:
            return 0
        return int((self.gameTime - 40) / 20) + 1
    
    def add_new_zone(self, zone):
        self.effect_zones.append(zone)

    def print_battlefield(self):
        """二维战场可视化"""
        grid = np.full((MAP_SIZE[1] * 2, MAP_SIZE[0] * 2), '.', dtype='U2')
        
        for m in self.alive_monsters:
            if m.is_alive:
                x = np.minimum(np.maximum(0, int(m.position.x * 2)), MAP_SIZE[0]*2-1)
                y = np.minimum(np.maximum(0, int(m.position.y * 2)), MAP_SIZE[1]*2-1)
                symbol = 'L' if m.faction == Faction.LEFT else 'R'
                if grid[y, x] != '.' and symbol != grid[y, x]:
                    symbol = 'X'
                if m.char_icon != "":
                    symbol = m.char_icon
                grid[y, x] = symbol
        
        logger.info(f"\nRound {self.round}")
        for row in grid:
            logger.info(' '.join(row))

    def get_grid(self, target):
        x, y = int(target.position.x), int(target.position.y)
        return x, y
