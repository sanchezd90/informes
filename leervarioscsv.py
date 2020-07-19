import os
from flask import Flask
import csv
app = Flask(__name__)
titulo = "Informes"

datos_informes = [] #los datos de todos los informes revisados
todos_listaDicc = []

for archivo in os.listdir('.'):
    if archivo.endswith(".csv"):
        with open(archivo) as csvfile:
            csvReader = csv.reader(csvfile, delimiter=';')
            datos_informe = list(csvReader)
            datos_informes.append(datos_informe)

for informe in datos_informes:
    #armo una lista en donde voy a incluir los diccionario
    listaDicc = []
    #inicio un loop para explorar las celdas. comienzo explorando las filas
    for x in range(len(informe)):
        #me fijo si la primera celda esta completa, así puedo saber que es fila de etiquetas
        if len(informe[x][0]) > 0:
            #armo el key del diccionario que va a llevar el nombre de la fila
            k = informe[x][0]
            #agrego a la lista el diccionario que tiene el key y asigna como valor un diccionario vacio
            listaDicc.append({informe[x][0]:{}})
            #inicio un loop para enumerar los datos de la fila de abajo de la fila que tiene las etiquetas
            for index,item in enumerate(informe[x+1]):
                #exploro si cada celda tiene un valor
                if len(item) > 0:
                    #si la celda tiene valor actualizo el diccionario con la etiqueta como key y el valor como value
                    listaDicc[-1][k].update({informe[x][index]:item})
    todos_listaDicc.append(listaDicc)

@app.route("/")
def home_www():
    listado_nombres=""
    for x in todos_listaDicc:
        nombre = (x[0]["\ufeffDatosPersonales"]["nombre"])
        apellido = (x[0]["\ufeffDatosPersonales"]["apellido"])
        listado_nombres += "<li>"+apellido+", "+nombre+"</li>"
    return (f"""
    <title>{titulo}</title> 
    <ul>{listado_nombres}</ul>
    """)

app.run(host="localhost", port=8080, debug=True)



