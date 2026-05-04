import csv

def load_id_name(path):
    m = {}
    with open(path, encoding='utf-8-sig') as f:
        for row in csv.DictReader(f):
            m[int(row['id'])] = row['原始名称']
    return m

old = load_id_name(r'G:\314\CannotMax-main\monster_greenvine_old.csv')
new = load_id_name(r'G:\314\CannotMax-main\monster_greenvine.csv')

# 比较 id 50-60 的新旧映射
out = []
for i in range(48, 62):
    o = old.get(i+1, '?')
    n = new.get(i+1, '?')
    match = '✓' if o == n else '✗ MISMATCH'
    out.append(f"  id{i+1}: OLD={o} NEW={n} {match}")

with open(r'G:\314\CannotMax-main\data\id_check.txt','w',encoding='utf-8') as f:
    f.write('\n'.join(out))
print('done')
