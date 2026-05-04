import json
with open(r'G:\314\CannotMax-main\simulator\monsters.json',encoding='utf-8') as f:
    mdata = json.load(f)['monsters']

# Show exact hex of巨岩蛛 name
for m in mdata:
    if '\u5de8\u5ca9' in m['名字']:
        name = m['名字']
        print(f"Name: {name}")
        print(f"Hex: {name.encode('utf-8').hex()}")
        print(f"Repr: {repr(name)}")
        print(f"Len: {len(name)} chars")
        # Try exact match
        match = next((x for x in mdata if x['名字'] == name), None)
        print(f"Exact match: {match is not None}")
