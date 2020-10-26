import os
import json

def evs2json():
    diccionarioEvaluaciones=None
    diccionarioInformes=None
    with open("evaluaciones.json","r") as f:
        diccionarioEvaluaciones = json.load(f)
    with open("informes.json","r") as f:
        diccionarioInformes = json.load(f)
    for x in diccionarioInformes:
        if x in diccionarioEvaluaciones:
            diccionarioEvaluaciones[x]["informe"]=diccionarioInformes[x]
    for x in diccionarioEvaluaciones:
        name=x+".json"
        path="./colecciones/"
        file_path=os.path.join(path,name)
        if len(os.listdir('./colecciones')) >0:
            for archivo in os.listdir('./colecciones'):
                if name != archivo:
                    with open(file_path,"w") as f:
                        json.dump(diccionarioEvaluaciones[x],f,indent=4)
        else:
            with open(file_path,"w") as f:
                json.dump(diccionarioEvaluaciones[x],f,indent=4)


