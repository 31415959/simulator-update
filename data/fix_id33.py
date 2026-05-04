import csv,json

# 1. Fix monster_greenvine.csv row 33
rows = []
with open(r'G:\314\CannotMax-main\monster_greenvine.csv',encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    for row in reader:
        if row and row[0] == '33':
            row[1] = '清醒的墨魉'
            row[2] = '"阿咬"'
            print(f"Fixed CSV id33: {row[1]} / {row[2]}")
        rows.append(row)

with open(r'G:\314\CannotMax-main\monster_greenvine.csv','w',encoding='utf-8-sig',newline='') as f:
    csv.writer(f).writerows(rows)
print("CSV saved")

# 2. Fix monsters.json
with open(r'G:\314\CannotMax-main\simulator\monsters.json',encoding='utf-8') as f:
    data = json.load(f)

for m in data['monsters']:
    if '珊瑚' in m.get('名字','') or '狂躁' in m.get('名字',''):
        old = m['名字']
        m['名字'] = '"阿咬"'
        # stats already correct (HP=1500 was the Greenvine value)
        print(f"Fixed JSON: {old} → {m['名字']}")

with open(r'G:\314\CannotMax-main\simulator\monsters.json','w',encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("JSON saved")
