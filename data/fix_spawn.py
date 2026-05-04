import json
with open(r'G:\314\CannotMax-main\simulator\monsters.json',encoding='utf-8') as f:
    data = json.load(f)
for m in data['monsters']:
    if '赘生物' in m.get('名字',''):
        m['攻击力']['数值'] = 150
        m['生命值']['数值'] = 1000
        m['移速']['数值'] = 1.9
        print(f"Fixed: ATK→150 HP→1000 SPD→1.9")
json.dump(data,open(r'G:\314\CannotMax-main\simulator\monsters.json','w',encoding='utf-8'),ensure_ascii=False,indent=2)
print('done')
