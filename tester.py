import csv

dics=[
    {
    "a":1,
    "b":2,
    "c":3
},
{
    "a":4,
    "b":5,
    "c":6,
    "d":6,
}
]

headers=[]

for x in dics:
    for k in x:
        if k not in headers:
            headers.append(k)

with open("archivo.csv","w") as f:
    out=csv.DictWriter(f,headers)
    out.writeheader()
    for x in dics:
        out.writerow(x)
