import csv
with open(r'G:\314\CannotMax-main\monster_greenvine.csv',encoding='utf-8-sig') as f:
    for row in csv.reader(f):
        if '破坏王' in str(row):
            print(f"id={row[0]} name={row[1]} HP={row[3]} ATK={row[4]} DEF={row[6]} RES={row[7]} rng={row[8]} spd={row[9]} mv={row[10]}")
            print(f"  desc={row[13]}")
with open(r'G:\314\CannotMax-main\simulator\monsters.json',encoding='utf-8') as f:
    import json
    for m in json.load(f)['monsters']:
        if '破坏王' in m.get('名字',''):
            atk=m.get('攻击力',{}).get('数值')
            hp=m.get('生命值',{}).get('数值')
            df=m.get('物理防御',{}).get('数值')
            print(f"JSON: ATK={atk} HP={hp} DEF={df}")
