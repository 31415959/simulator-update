import json
with open(r'G:\314\CannotMax-main\simulator\monsters.json', encoding='utf-8') as f:
    mdata = json.load(f)['monsters']
names = [m['名字'] for m in mdata]
out = [f'Total: {len(names)}']
for n in names[:15]:
    out.append(f'  {n}')
for tgt in ['高级武装人员','门','炮击组长','散华骑士团学徒','庞贝','矿脉守卫','沉沙','沸血','复仇者']:
    found = any(tgt in n or n in tgt for n in names)
    out.append(f'{tgt}: found={found}')
    if not found:
        similar = [n for n in names if len(tgt)>=2 and tgt[:2] in n]
        out.append(f'  similar: {similar[:3]}')
with open(r'G:\314\CannotMax-main\data\names_check.txt','w',encoding='utf-8') as f:
    f.write('\n'.join(out))
print('done')
