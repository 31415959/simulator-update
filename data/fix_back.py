import json
with open(r'G:\314\CannotMax-main\simulator\monsters.json',encoding='utf-8') as f:
    data = json.load(f)

for m in data['monsters']:
    if '雪球投手' in m.get('名字',''):
        m['名字'] = '"投石机"'
        m['攻击力']['数值'] = 1200
        m['生命值']['数值'] = 5000
        m['物理防御']['数值'] = 700
        m['法抗']['数值'] = 20
        m['攻击间隔']['数值'] = 3
        m['移速']['数值'] = 0.7
        print(f"Renamed back to 投石机, stats updated")

with open(r'G:\314\CannotMax-main\simulator\monsters.json','w',encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print('done')
