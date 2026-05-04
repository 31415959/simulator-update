import csv
with open(r'G:\314\CannotMax-main\monster_greenvine.csv',encoding='utf-8-sig') as f:
    rows = list(csv.reader(f))

# Find rows with id=33 and id=2
for row in rows:
    if row and row[0] in ('33', '2'):
        print(f"id={row[0]}:")
        for i,v in enumerate(row):
            print(f"  col{i}={v}")
        print()
