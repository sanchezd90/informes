import os
import json


def evs2json():
    #cargo toda la info de evaluaciones e informes que arroja el lector
    diccionarioEvaluaciones=None
    diccionarioInformes=None
    with open("evaluaciones.json","r") as f:
        diccionarioEvaluaciones = json.load(f)
    with open("informes.json","r") as f:
        diccionarioInformes = json.load(f)
    for x in diccionarioInformes:
        if x in diccionarioEvaluaciones:
            diccionarioEvaluaciones[x]["informe"]=diccionarioInformes[x]
    
    #para cada entrada hago este proceso
    for x in diccionarioEvaluaciones:
        #agrego el codigo como un k:v
        diccionarioEvaluaciones[x]["codigo"]=x
        
        #corrijo los keys que tienen "." en su nombre. 
        # La lista de los conocidos es la siguiente: 
        keysInvalidosMongo=["Relatos","RAVLT","Relatos (WMS IV)","RAVLT (Tambor50)","RAVLT (Pasto50)","RAVLT (Tambor60)"]
        for key in keysInvalidosMongo:
            if key in diccionarioEvaluaciones[x]:
                ori_dict=diccionarioEvaluaciones[x][key]
                corrected_dict = { k.replace('.','_'): v for k, v in ori_dict.items() }
                diccionarioEvaluaciones[x][key]=corrected_dict
        
        #creo un json independiente por cada evaluacion
        #y lo guardo dentro de colecciones
        name=x+".json"
        path="./colecciones/"
        file_path=os.path.join(path,name)
        #en caso que el directorio ya tenga contenido reviso que 
        #no se agregue nuevamente la misma evaluacion
        if len(os.listdir('./colecciones')) >0:
            for archivo in os.listdir('./colecciones'):
                if name != archivo:
                    with open(file_path,"w") as f:
                        json.dump(diccionarioEvaluaciones[x],f,indent=4)
        else:#en caso que el directorio este vacio
            with open(file_path,"w") as f:
                json.dump(diccionarioEvaluaciones[x],f,indent=4)


