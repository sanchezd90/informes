import os
from flask import Flask
import csv
app = Flask(__name__)
titulo = "Informes"

estilos = """
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css" integrity="sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk" crossorigin="anonymous">
"""

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
                if item !="":
                    #si la celda tiene valor actualizo el diccionario con la etiqueta como key y el valor como value
                    k=informe[x][index]
                    diccionarioInformes[codigo][key][k]=item

#home para desplegar nombres de los sujetos evaluados
@app.route("/")
def home_www():
    listado_nombres= ""
    for x in diccionarioInformes:
        nombre = diccionarioInformes[x]["\ufeffDatosPersonales"]["nombre"]
        apellido = diccionarioInformes[x]["\ufeffDatosPersonales"]["apellido"]
        fecha_ev = diccionarioInformes[x]["\ufeffDatosPersonales"]["fecha_ev"]
        edad = (diccionarioInformes[x]["\ufeffDatosPersonales"]["edad_eval"])
        split = edad.split(",")
        edad = int(split[0])
        if edad > 60:
            grupo="adulto mayor"
        else:
            grupo="adulto joven"
        listado_nombres += "<a href=/pacientes/"+x+" class=list-group-item list-group-item-action>"+apellido+", "+nombre+" ("+fecha_ev+")<span class=badge badge-primary badge-pill>"+grupo+"</span></a>"
    return(f"""
    {estilos}
    <title>{titulo}</title>
    <div class="list-group">{listado_nombres}</div>
    """)

codigos=[]
for x in diccionarioInformes:
    codigos.append(x)



@app.route("/pacientes/<string:codigos>")
def pacientes_www(codigos):
    nombrecompleto = diccionarioInformes[codigos]["\ufeffDatosPersonales"]["apellido"]+", "+diccionarioInformes[codigos]["\ufeffDatosPersonales"]["nombre"]
    fechaeval = diccionarioInformes[codigos]["\ufeffDatosPersonales"]["fecha_ev"]
    datosHTML = ""
    for key,value, in diccionarioInformes[codigos].items():
        if len(value)>0:
            datosHTML += "<div><h1>"+key+"</h1>"
            for k,v in value.items():
                datosHTML += "<h2>"+k+": "+v+"<h2>" 
            datosHTML += "</div>"
    return(f"""
    <title>{titulo}</title>
    <ul>{datosHTML}</ul>
    <h4><a href="/">Volver a inicio</a></h4>
    """)

app.run(host="localhost", port=8080, debug=True)




