import sys,os
sys.path.insert(0,r'G:\314\CannotMax-main')
os.chdir(r'G:\314\CannotMax-main')
from simulator.utils import MONSTER_MAPPING, REVERSE_MONSTER_MAPPING

out = []
for i in range(68):
    name = MONSTER_MAPPING.get(i, '-')
    if name != '-':
        out.append(f'{i}: {name}')

with open(r'G:\314\CannotMax-main\data\mapping_check.txt','w',encoding='utf-8') as f:
    f.write(f'Total entries: {len(MONSTER_MAPPING)}\n')
    f.write('\n'.join(out[:30]))
print('done')
