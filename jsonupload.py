import pymongo
import json
import os
from mongoclient import cluster


db=cluster["ENPS"]

def add_new_eval():
    col=db["evaluaciones"]
    codigos=[x["codigo"]+".json" for x in col.find({},{"_id":0,"codigo":1}) ]

    #recorro los archivos que hay en la carpeta local de evaluacionesjson
    for x in os.listdir("./evaluacionesjson"):
        name=x
        path="./evaluacionesjson/"
        file_path=os.path.join(path,name)
        #si no está ya subido en mongo lo subo
        if x not in codigos:
            diccionario=None
            with open(file_path,"r") as f:
                diccionario=json.load(f)
            y=col.insert_one(diccionario)
        os.remove(file_path)

def add_new_info():
    col=db["informes"]
    codigos=[x["codigo"]+".json" for x in col.find({},{"_id":0,"codigo":1}) ]

    #recorro los archivos que hay en la carpeta local de informesjson
    for x in os.listdir("./informesjson"):
        name=x
        path="./informesjson/"
        file_path=os.path.join(path,name)
        #si no está ya subido en mongo lo subo
        if x not in codigos:
            diccionario=None
            with open(file_path,"r") as f:
                diccionario=json.load(f)
            y=col.insert_one(diccionario)
        os.remove(file_path)

add_new_info()
add_new_eval()






