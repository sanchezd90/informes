import os
import csv
import json

datos_evaluaciones = [] #los datos de todos las evaluaciones revisados

with open("evaluaciones.json","r") as f:
    diccionarioEvaluaciones = json.load(f) #diccionario con datos de todos los informes almacenados en JSON

#loop para revisar archivos csv y agregar datos a datos_evaluaciones
for archivo in os.listdir('.'):
    if archivo.endswith(".csv"):
        with open(file=archivo, mode="r", encoding="utf-8-sig") as csvfile:
            csvReader = csv.reader(csvfile, delimiter=';')
            datos_evaluacion = list(csvReader)
            datos_evaluaciones.append(datos_evaluacion)

#loop para armar diccionarios con la información de cada informe. La info va a diccionarioInformes
for informe in datos_evaluaciones:
    split=informe[1][11].split("/")
    for i,s in enumerate(split):
        if len(s)<2:
            split[i]="0"+split[i]
    fecha=split[2]+"-"+split[1]+"-"+split[0]
    dni=informe[1][12].replace(".","").replace(",","")
    codigo = dni+"-"+fecha
    if codigo not in diccionarioEvaluaciones:
        diccionarioEvaluaciones[codigo]={}
        #inicio un loop para explorar las celdas. comienzo explorando las filas 
        for x in range(len(informe)):
            #me fijo si la primera celda esta completa, así puedo saber que es fila de etiquetas
            if len(informe[x][0]) > 0:
                #armo el key del diccionario que va a llevar el nombre de la fila
                key = informe[x][0]
                #agrego al diccionario una key por prueba con el valor vacio
                diccionarioEvaluaciones[codigo][key]={}
                #inicio un loop para enumerar los datos de la fila de abajo de la fila que tiene las etiquetas
                for index,item in enumerate(informe[x+1]):
                    #exploro si cada celda tiene un valor
                    if index >0:
                        #si la celda tiene valor actualizo el diccionario con la etiqueta como key y el valor como value
                        k=informe[x][index]
                        diccionarioEvaluaciones[codigo][key][k]=item

with open("evaluaciones.json","w") as f:
    json.dump(diccionarioEvaluaciones,f,indent=4)