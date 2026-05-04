import json
with open(r'G:\314\CannotMax-main\simulator\monsters.json',encoding='utf-8') as f:
    data = json.load(f)

for m in data['monsters']:
    if '萨克斯手' in m.get('名字',''):
        old_atk = m['攻击力']['数值']
        old_hp = m['生命值']['数值']
        old_def = m['物理防御']['数值']
        m['攻击力']['数值'] = 1200
        m['生命值']['数值'] = 8750
        m['物理防御']['数值'] = 650
        m['法抗']['数值'] = 20
        m['攻击间隔']['数值'] = 4.5
        m['移速']['数值'] = 0.8
        print(f"Fixed {m['名字']}: ATK {old_atk}→1200 HP {old_hp}→8750 DEF {old_def}→650")

with open(r'G:\314\CannotMax-main\simulator\monsters.json','w',encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print('done')
