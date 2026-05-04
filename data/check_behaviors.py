import json
with open(r'G:\314\CannotMax-main\simulator\monsters.json',encoding='utf-8') as f:
    raw = f.read()

# Search for behavior-related terms
pos = raw.find('\u5de8\u5ca9\u86db')
if pos >= 0:
    # Get 2000 chars around the spider
    section = raw[pos:pos+2000]
    # Find the behavior section
    bh_pos = section.find('"行为"')
    if bh_pos >= 0:
        print(f"Behavior section at offset {bh_pos}:")
        print(repr(section[bh_pos:bh_pos+300]))
    else:
        print("No behavior section found")
else:
    print("Spider not found")
