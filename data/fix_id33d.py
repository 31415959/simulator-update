import csv,json

# Fix CSV
rows = []
with open(r'G:\314\CannotMax-main\monster_greenvine.csv',encoding='utf-8-sig') as f:
    for row in csv.reader(f):
        if row and row[0] == '33':
            row[1] = '清醒的墨魉'
            row[2] = '"阿咬"'
        rows.append(row)
with open(r'G:\314\CannotMax-main\monster_greenvine.csv','w',encoding='utf-8-sig',newline='') as f:
    csv.writer(f).writerows(rows)
print("CSV saved")

# Fix JSON HP (1750 → 1500)
with open(r'G:\314\CannotMax-main\simulator\monsters.json',encoding='utf-8') as f:
    data = json.load(f)
for m in data['monsters']:
    if '"阿咬"' in m.get('名字',''):
        m['生命值']['数值'] = 1500
        print(f"HP fixed to 1500")
        break
with open(r'G:\314\CannotMax-main\simulator\monsters.json','w',encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("JSON saved")
