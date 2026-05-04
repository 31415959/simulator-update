import json
with open(r'G:\314\CannotMax-main\simulator\monsters.json',encoding='utf-8') as f:
    data = json.load(f)

for i,m in enumerate(data['monsters']):
    atk = m['攻击力']['数值']
    if 430 <= atk <= 440:
        print(f"idx{i}: name={m['名字']} ATK={atk} HP={m['生命值']['数值']}")
        # Rename to阿咬
        m['名字'] = '"阿咬"'
        print(f"  → renamed to: {m['名字']}")

with open(r'G:\314\CannotMax-main\simulator\monsters.json','w',encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("saved")
