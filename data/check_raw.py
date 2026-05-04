import json
with open(r'G:\314\CannotMax-main\simulator\monsters.json',encoding='utf-8') as f:
    raw = f.read()

# Find the巨岩蛛 section
idx = raw.find('\u5de8\u5ca9\u86db')
if idx >= 0:
    section = raw[idx:idx+500]
    print("Raw JSON section:")
    print(repr(section[:300]))
    # Check for周期召唤
    for term in ['\u5468\u671f\u53ec\u5524', '\u5b9a\u65f6\u53ec\u5524']:
        if term in section:
            print(f"  Found: {term}")
        else:
            print(f"  Not found: {term}")
