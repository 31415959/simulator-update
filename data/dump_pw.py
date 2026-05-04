import json
with open(r'G:\314\CannotMax-main\simulator\monsters.json',encoding='utf-8') as f:
    mdata = json.load(f)['monsters']
for m in mdata:
    if '破坏王' in m.get('名字',''):
        print(json.dumps(m, ensure_ascii=False, indent=2))
        break
