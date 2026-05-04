import json
with open(r'G:\314\CannotMax-main\simulator\monsters.json',encoding='utf-8') as f:
    data = json.load(f)

for m in data['monsters']:
    if '矿脉' in m.get('名字',''):
        old_atk = m['攻击力']['数值']
        old_hp = m['生命值']['数值']
        old_def = m['物理防御']['数值']
        m['攻击力']['数值'] = 600
        m['生命值']['数值'] = 12500
        m['物理防御']['数值'] = 300
        m['法抗']['数值'] = 10
        m['攻击间隔']['数值'] = 4
        m['移速']['数值'] = 0.6
        print(f"Fixed {m['名字']}: ATK {old_atk}->600 HP {old_hp}->12500 DEF {old_def}->300")
        print(f"  + ATK_INTV=4 MOVE=0.6 RES=10")

with open(r'G:\314\CannotMax-main\simulator\monsters.json','w',encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print('done')
