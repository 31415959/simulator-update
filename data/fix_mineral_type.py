import json
with open(r'G:\314\CannotMax-main\simulator\monsters.json',encoding='utf-8') as f:
    data = json.load(f)

for m in data['monsters']:
    if '矿脉' in m.get('名字',''):
        old_type = m.get('类型', '未设置')
        m['类型'] = '法术'
        print(f"{m['名字']}: 攻击类型 {old_type} → 法术")

with open(r'G:\314\CannotMax-main\simulator\monsters.json','w',encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print('done')
