import json
with open(r'G:\314\CannotMax-main\simulator\monsters.json',encoding='utf-8') as f:
    data = json.load(f)

for m in data['monsters']:
    name = m.get('名字','')
    if name == '投石机':  # 没引号的版本
        m['攻击力']['数值'] = 1200
        m['生命值']['数值'] = 5000
        m['物理防御']['数值'] = 700
        m['法抗']['数值'] = 20
        m['攻击间隔']['数值'] = 3
        m['移速']['数值'] = 0.7
        print(f"Fixed: {name} ATK=1200 HP=5000 DEF=700 RES=20")
    elif '投石机' in name:
        print(f"Kept: {name} ATK={m['攻击力']['数值']} HP={m['生命值']['数值']}")

with open(r'G:\314\CannotMax-main\simulator\monsters.json','w',encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print('done')
