import json
with open(r'G:\314\CannotMax-main\simulator\monsters.json',encoding='utf-8') as f:
    data = json.load(f)

# 找投石机改成雪球投手
for m in data['monsters']:
    if '投石机' in m.get('名字',''):
        old = m['名字']
        m['名字'] = '雪球投手'
        m['攻击力']['数值'] = 1200
        m['生命值']['数值'] = 5000
        m['物理防御']['数值'] = 700
        m['法抗']['数值'] = 20
        m['攻击间隔']['数值'] = 3
        m['移速']['数值'] = 0.7
        m['攻击范围']['数值'] = 0.8
        m['类型'] = '物理'
        print(f"Fixed {old} → 雪球投手")
        print(f"  ATK=1200 HP=5000 DEF=700 RES=20 INT=3 SPD=0.7")

with open(r'G:\314\CannotMax-main\simulator\monsters.json','w',encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print('done')
