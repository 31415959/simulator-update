import json
with open(r'G:\314\CannotMax-main\simulator\monsters.json',encoding='utf-8') as f:
    for m in json.load(f)['monsters']:
        if '破坏王' in m.get('名字',''):
            print(f"ATK={m.get('攻击力',{})} HP={m.get('生命值',{})}")
            print(f"DEF={m.get('物理防御',{})} RES={m.get('法术抗性',{})}")
            print(f"SPD={m.get('攻击速度',{})} RNG={m.get('攻击范围',{})}")
            print(f"TYPE={m.get('攻击类型',{})} MV={m.get('移动速度',{})}")
