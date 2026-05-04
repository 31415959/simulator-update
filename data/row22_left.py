import csv
rows=list(csv.reader(open(r'G:\314\CannotMax-main\arknights.csv',encoding='utf-8')))
r=rows[22]
print("Row22 non-zero LEFT (cols 0-77):")
for i in range(78):
    v=r[i].strip()
    if v and v not in ('','0','0.0'):
        print(f"  col{i} = {v}")
