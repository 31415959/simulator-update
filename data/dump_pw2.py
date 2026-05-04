import json,sys,io
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
with open(r'G:\314\CannotMax-main\simulator\monsters.json',encoding='utf-8') as f:
    for m in json.load(f)['monsters']:
        if '破坏王' in m.get('名字',''):
            for k,v in m.items():
                print(f'{k}: {v}')
