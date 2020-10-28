import pymongo
import json
import os

cluster=pymongo.MongoClient("mongodb+srv://sanchezd90:dbuser-L6H6@cluster0.wwnbb.mongodb.net/?retryWrites=true&w=majority")

db=cluster["ENPS"]
col=db["evaluaciones"]
codigos=[x["codigo"]+".json" for x in col.find({},{"_id":0,"codigo":1}) ]

def add_new():
    #recorro los archivos que hay en la carpeta local de colecciones
    for x in os.listdir("./colecciones"):
        #si no está ya subido en mongo lo subo
        if x not in codigos:
            diccionario=None
            name=x
            path="./colecciones/"
            file_path=os.path.join(path,name)
            with open(file_path,"r") as f:
                diccionario=json.load(f)
            y=col.insert_one(diccionario)

add_new()








