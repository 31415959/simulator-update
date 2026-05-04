import sys,os,csv,json,io
sys.path.insert(0,r'G:\314\CannotMax-main')
os.chdir(r'G:\314\CannotMax-main')
from simulator.battle_field import Battlefield
from simulator.utils import Faction, MONSTER_MAPPING

with open('simulator/monsters.json',encoding='utf-8') as f:
    mdata = json.load(f)['monsters']
with open('simulator/arknights.csv',encoding='utf-8') as f:
    rows = list(csv.reader(f))

out_lines = []
for row_idx in [1,3,5,6,7,9,10,12,13,14,21,22]:
    r = rows[row_idx]
    csv_winner = r[-1].strip()
    left = {}
    right = {}
    for i in range(68):
        v = r[i].strip()
        if v and v not in ('','0','0.0'):
            try: cnt = int(float(v))
            except: continue
            name = MONSTER_MAPPING.get(i)
            if not name: continue
            if i < 34: left[name] = cnt
            else: right[name] = cnt
    out_lines.append(f"Row{row_idx} CSV={csv_winner}:")
    out_lines.append(f"  L: {dict(sorted(left.items()))}")
    out_lines.append(f"  R: {dict(sorted(right.items()))}")
    out_lines.append("")

with open(r'G:\314\CannotMax-main\data\mis_details.txt','w',encoding='utf-8') as f:
    f.write('\n'.join(out_lines))
print('done')
