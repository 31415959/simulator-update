import sys,os,json,csv
sys.path.insert(0,r'G:\314\CannotMax-main')
os.chdir(r'G:\314\CannotMax-main')

with open('simulator/monsters.json',encoding='utf-8') as f:
    mdata = json.load(f)['monsters']

# 看门的所有变体
for m in mdata:
    if '门' in m['名字']:
        print(f"  JSON name={repr(m['名字'])}")

# 看旧表门
with open('monster_greenvine_old.csv',encoding='utf-8-sig') as f:
    for row in csv.reader(f):
        if row and row[0]=='2':
            print(f"  OLD id2: repr原始名称={repr(row[2])}")
            break

# 看新表门
with open('monster_greenvine.csv',encoding='utf-8-sig') as f:
    for row in csv.reader(f):
        if '门' in row[1] or '门' in row[2]:
            print(f"  NEW: id={row[0]} name={repr(row[1])} orig={repr(row[2])}")

# setup_battle查名逻辑
print("\n=== Name matching test ===")
for tgt_name in ['门', '"门"', '“门”', '高级武装人员', '散华骑士团学徒']:
    found = False
    for md in mdata:
        mn = md['名字']
        if tgt_name == mn or tgt_name in mn or mn in tgt_name:
            found = True
            print(f"  '{tgt_name}' MATCHES '{mn}' via")
            if tgt_name == mn: print("    exact ==")
            elif tgt_name in mn: print(f"    tgt in mn")
            else: print(f"    mn in tgt")
            break
    if not found:
        print(f"  '{tgt_name}' NO MATCH")
