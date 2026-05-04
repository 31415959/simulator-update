import json,sys
sys.path.insert(0,r'G:\314\CannotMax-main')
from simulator.behaviors import BEHAVIOR_REGISTRY

with open(r'G:\314\CannotMax-main\simulator\monsters.json',encoding='utf-8') as f:
    d = json.load(f)

with open(r'G:\314\CannotMax-main\data\bh_check.txt','w',encoding='utf-8') as out:
    for m in d['monsters']:
        if '\u5de8\u5ca9\u86db' in m['名字']:
            for b in m.get('\u884c\u4e3a',[]):
                t = b['\u7c7b\u578b']
                out.write(f"config type: {repr(t)}\n")
                out.write(f"hex: {t.encode('utf-8').hex()}\n")
                out.write(f"in registry: {t in BEHAVIOR_REGISTRY}\n")
                for k in list(BEHAVIOR_REGISTRY.keys())[:5]:
                    out.write(f"  reg key: {repr(k)} hex={k.encode('utf-8').hex()}\n")
                    out.write(f"  match: {k == t}\n")
