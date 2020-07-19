import os
from flask import Flask
import csv
app = Flask(__name__)
titulo = "Informes"

with open('informe1.csv') as csvfile:
    csvReader = csv.reader(csvfile, delimiter=';')
    datos = list(csvReader)


def busca(clave):
    for x in range(len(datos)):
        if clave in datos[x]: 
            return datos[x+1][datos[x].index(clave)]

#armo una lista en donde voy a incluir los diccionario
listaDicc = []
#inicio un loop para explorar las celdas. comienzo explorando las filas
for x in range(len(datos)):
    #me fijo si la primera celda esta completa, así puedo saber que es fila de etiquetas
    if len(datos[x][0]) > 0:
        #armo el key del diccionario que va a llevar el nombre de la fila
        k = datos[x][0]
        #agrego a la lista el diccionario que tiene el key y asigna como valor un diccionario vacio
        listaDicc.append({datos[x][0]:{}})
        #inicio un loop para enumerar los datos de la fila de abajo de la fila que tiene las etiquetas
        for index,item in enumerate(datos[x+1]):
            #exploro si cada celda tiene un valor
            if len(item) > 0:
                #si la celda tiene valor actualizo el diccionario con la etiqueta como key y el valor como value
                listaDicc[-1][k].update({datos[x][index]:item})


datosHTML = ""
for index,item in enumerate(listaDicc):
    for key,value, in item.items():
        if len(value)>0:
            datosHTML += "<div><h1>"+key+"</h1>"
            for k,v in value.items():
                datosHTML += "<h2>"+k+": "+v+"<h2>" 
            datosHTML += "</div>"

@app.route("/")
def home_www():
    return (f"""<title>{titulo}</title> {datosHTML}""")

app.run(host="localhost", port=8080, debug=True)