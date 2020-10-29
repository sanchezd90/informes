import os
import json


def evs2json():
    #cargo toda la info de evaluaciones que arroja el lector
    diccionarioInformes=None
    with open("evaluaciones.json","r") as f:
        diccionarioInformes = json.load(f)
    
    #para cada entrada hago este proceso
    for x in diccionarioInformes:
        #agrego el codigo como un k:v
        diccionarioInformes[x]["codigo"]=x
        
        #corrijo los keys que tienen "." en su nombre. 
        # La lista de los conocidos es la siguiente: 
        keysInvalidosMongo=["Relatos","RAVLT","Relatos (WMS IV)","RAVLT (Tambor50)","RAVLT (Pasto50)","RAVLT (Tambor60)"]
        for key in keysInvalidosMongo:
            if key in diccionarioInformes[x]:
                ori_dict=diccionarioInformes[x][key]
                corrected_dict = { k.replace('.','_'): v for k, v in ori_dict.items() }
                diccionarioInformes[x][key]=corrected_dict
        
        #creo un json independiente por cada evaluacion
        #y lo guardo dentro de evaluacionesjson
        name=x+".json"
        path="./evaluacionesjson/"
        file_path=os.path.join(path,name)
        #en caso que el directorio ya tenga contenido reviso que 
        #no se agregue nuevamente la misma evaluacion
        if len(os.listdir('./evaluacionesjson')) >0:
            for archivo in os.listdir('./evaluacionesjson'):
                if name != archivo:
                    with open(file_path,"w") as f:
                        json.dump(diccionarioInformes[x],f,indent=4)
        else:#en caso que el directorio este vacio
            with open(file_path,"w") as f:
                json.dump(diccionarioInformes[x],f,indent=4)


def infos2json():
    #cargo toda la info de evaluaciones que arroja el lector
    diccionarioInformes=None
    with open("informes.json","r") as f:
        diccionarioInformes = json.load(f)
    
    #para cada entrada hago este proceso
    for x in diccionarioInformes:
        #agrego el codigo como un k:v
        diccionarioInformes[x]["codigo"]=x
              
        #creo un json independiente por cada informe
        #y lo guardo dentro de informesjson
        name=x+".json"
        path="./informesjson/"
        file_path=os.path.join(path,name)
        #en caso que el directorio ya tenga contenido reviso que 
        #no se agregue nuevamente la misma evaluacion
        if len(os.listdir('./informesjson')) >0:
            for archivo in os.listdir('./informesjson'):
                if name != archivo:
                    with open(file_path,"w") as f:
                        json.dump(diccionarioInformes[x],f,indent=4)
        else:#en caso que el directorio este vacio
            with open(file_path,"w") as f:
                json.dump(diccionarioInformes[x],f,indent=4)

