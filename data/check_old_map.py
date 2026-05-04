import csv
# 旧怪物表：col0=id1, col1=id2, ...
with open(r'G:\314\CannotMax-main\monster_greenvine_old.csv', encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    header = next(reader)
    print(f"old CSV header: {header}")
    cols = {}
    for row in reader:
        if len(row) > 1:
            cid = row[0]
            name = row[2]  # 原始名称
            if cid.isdigit():
                cols[int(cid)] = name
    # Column 0 in arknights.csv = monster ID 1
    for i in range(1, min(10, max(cols.keys())+1)):
        print(f"  col{i-1} = id{i} = {cols.get(i, '???')}")

print(f"\n总: {len(cols)} monsters")
