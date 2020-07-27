import os
import csv

datos_informes = [] #los datos de todos los informes revisados
diccionarioInformes = {} #diccionario con datos de todos los informes

#loop para revisar archivos csv y agregar datos a datos_informes
for archivo in os.listdir('.'):
    if archivo.endswith(".csv"):
        with open(archivo) as csvfile:
            csvReader = csv.reader(csvfile, delimiter=';')
            datos_informe = list(csvReader)
            datos_informes.append(datos_informe)

#loop para armar diccionarios con la información de cada informe. La info va a diccionarioInformes
for informe in datos_informes:
    split=informe[1][11].split("/")
    fecha=split[2]+"-"+split[1]+"-"+split[0]
    dni=informe[1][12]
    codigo = dni+"-"+fecha
    diccionarioInformes[codigo]={}
    #inicio un loop para explorar las celdas. comienzo explorando las filas 
    for x in range(len(informe)):
        #me fijo si la primera celda esta completa, así puedo saber que es fila de etiquetas
        if len(informe[x][0]) > 0:
            #armo el key del diccionario que va a llevar el nombre de la fila
            key = informe[x][0]
            #agrego al diccionario una key por prueba con el valor vacio
            diccionarioInformes[codigo][key]={}
            #inicio un loop para enumerar los datos de la fila de abajo de la fila que tiene las etiquetas
            for index,item in enumerate(informe[x+1]):
                #exploro si cada celda tiene un valor
                if index >0:
                    #si la celda tiene valor actualizo el diccionario con la etiqueta como key y el valor como value
                    k=informe[x][index]
                    diccionarioInformes[codigo][key][k]=item
