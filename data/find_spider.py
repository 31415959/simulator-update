import json,sys
sys.stdout.reconfigure(encoding='utf-8')
d=json.load(open(r'G:\314\CannotMax-main\simulator\monsters.json',encoding='utf-8'))
for m in d['monsters']:
    if '\u5de8\u5ca9' in m.get('名字','') or '\u5ca9' in m.get('名字',''):
        print(f"FOUND: {repr(m['名字'])}")
