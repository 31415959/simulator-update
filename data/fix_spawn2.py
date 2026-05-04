import json
with open(r'G:\314\CannotMax-main\simulator\monsters.json',encoding='utf-8') as f:
    data = json.load(f)
for m in data['monsters']:
    if '赘生物' in m.get('名字',''):
        # Greenvine: HP×0.5 = 500, ATK×1.5 = 225
        m['攻击力']['数值'] = 225
        m['生命值']['数值'] = 500
        print(f"Fixed 畸变赘生物: ATK=225 HP=500 (Greenvine applied)")
json.dump(data,open(r'G:\314\CannotMax-main\simulator\monsters.json','w',encoding='utf-8'),ensure_ascii=False,indent=2)
print('done')
