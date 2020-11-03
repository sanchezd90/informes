import pymongo
from mongoclient import cluster

db=cluster["ENPS"]

#funciones que son aptas para ambas colecciones

def getAll_codigos(coleccion):
    col=db[coleccion]
    return [x["codigo"] for x in col.find({},{"_id":0, "codigo":1})]

#funciones especificas para evaluaciones

def getAll_datosPersonales():
    col=db["evaluaciones"]
    return [x for x in col.find({},{"_id":0, "DatosPersonales":1})]

def getAll_nombres(datos):
    nombres=[]
    for x in datos:
        if "DatosPersonales" in x:
            nombre=x["DatosPersonales"]["nombre"]
            apellido=x["DatosPersonales"]["apellido"]
            nombres.append((nombre,apellido))
    return nombres






