import json

"""
with open("nuevojson.json","r") as f:
    tmp=json.load(f)

tmp.update({"cod3":{"nombre":"pedro"}})

with open("nuevojson.json","w") as f:
    json.dump(tmp,f, indent=4)
"""

dic={
    "1":{"a":"aa"},
    "2":{"b":"bb"},
    "3":{"c":"cc"}
}

print(dic)

if "3" not in dic:
    dic.update({"3":{"c":"cc"}})
else:
    print("Ya está")

print(dic)