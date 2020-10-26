from compilador import Compilador
import json

compilador=Compilador()
datos=compilador.activar()

def compilarTODOaJSON(sujetos):
    #PASO 1: volver la lista de objetos una lista de diccionarios
    lista_sujetos=[]
    for x in sujetos:
        lista_sujetos.append(datos["sujetos"][x].__dict__)
    #PASO 2: hacer un diccionario por sujeto con todos sus datos con tipo compatible con JSON
    dicc_sujetos={}
    for x in lista_sujetos:
        dicc_sujetos[x["DNI"]]={
            "DNI":x["DNI"],
            "nombre":x["nombre"],
            "apellido":x["apellido"],
            "edad":x["edad"],
            "fechaNac":str(x["fechaNac"]),
            "sexo":x["sexo"],
            "escolaridad":x["escolaridad"],
            "pmanual":x["pmanual"],
            "informes":{},
            "evaluaciones":{},
            }
        for k,v in x["informes"].items():
            dicc_sujetos[x["DNI"]]["informes"][k]=v.__dict__
        for k,v in x["evaluaciones"].items():
            dicc_sujetos[x["DNI"]]["evaluaciones"][k]=v.__dict__
        for y in x["informes"]:
            dicc_sujetos[x["DNI"]]["informes"][y].pop("fechaEv",None)
        for y in x["evaluaciones"]:
            dicc_sujetos[x["DNI"]]["evaluaciones"][y].pop("fechaEv",None)
    #PASO 3:convertir el diccionario en JSON
    with open("bd.json","w") as f:
        json.dump(dicc_sujetos,f,indent=4)




