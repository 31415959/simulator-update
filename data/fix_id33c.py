import json
with open(r'G:\314\CannotMax-main\simulator\monsters.json',encoding='utf-8') as f:
    data = json.load(f)

# idx31 should be "阿咬" (was 狂躁珊瑚)
# idx40 should be 酸液源石虫·α (was renamed incorrectly)
# idx91 should be 风情街"星术师" (was renamed incorrectly)

data['monsters'][40]['名字'] = '酸液源石虫·α'
data['monsters'][91]['名字'] = '风情街"星术师"'
print(f"Restored idx40: {data['monsters'][40]['名字']}")
print(f"Restored idx91: {data['monsters'][91]['名字']}")
print(f"Kept idx31: {data['monsters'][31]['名字']}")

with open(r'G:\314\CannotMax-main\simulator\monsters.json','w',encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("saved")
