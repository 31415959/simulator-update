import csv
rows=list(csv.reader(open(r'G:\314\CannotMax-main\simulator\arknights.csv',encoding='utf-8')))
r0=rows[0]
r1=rows[1]

out=[]
out.append(f"Row0 (index): {len(r0)} cols, last={repr(r0[-1])}")
nz0=[(i,v) for i,v in enumerate(r0[:-1]) if v.strip() not in ('','0','0.0')]
out.append(f"  non-zero: {len(nz0)} entries")
for i,v in nz0[:10]:
    out.append(f"    col{i}={v}")

out.append(f"\nRow1 (battle): {len(r1)} cols, winner={r1[-1]}")
nz1=[(i,v) for i,v in enumerate(r1[:-1]) if v.strip() not in ('','0','0.0')]
out.append(f"  non-zero: {len(nz1)} entries")
for i,v in nz1:
    out.append(f"    col{i}={v}")

with open(r'G:\314\CannotMax-main\data\raw_rows.txt','w',encoding='utf-8') as f:
    f.write('\n'.join(out))
print('done')
