import csv,json,sys,os
sys.path.insert(0,r'G:\314\CannotMax-main')
os.chdir(r'G:\314\CannotMax-main')
from simulator.utils import MONSTER_MAPPING

with open('simulator/arknights.csv',encoding='utf-8') as f:
    rows = list(csv.reader(f))

# 看前3行各有多少怪物
for row_idx in range(3):
    r = rows[row_idx]
    left_count = 0; right_count = 0
    left_types = []; right_types = []
    for i in range(68):
        v = r[i].strip()
        if v and v not in ('','0','0.0'):
            cnt = int(float(v))
            name = MONSTER_MAPPING.get(i, f"?{i}")
            if i < 34:
                left_count += cnt
                left_types.append(f"{name}x{cnt}")
            else:
                right_count += cnt
                right_types.append(f"{name}x{cnt}")
    with open(r'G:\314\CannotMax-main\data\row_stats.txt','a',encoding='utf-8') as f:
        f.write(f"Row{row_idx}: L={left_count}unit/{len(left_types)}type R={right_count}unit/{len(right_types)}type winner={r[-1]}\n")
        f.write(f"  L: {', '.join(left_types[:5])}...\n")
        f.write(f"  R: {', '.join(right_types[:5])}...\n\n")
print('done')
