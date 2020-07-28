import os
from flask import Flask, render_template
import lector
app = Flask(__name__)
titulo = "Evaluaciones"

diccionarioInformes = lector.diccionarioInformes #diccionario con datos de todos los informes

class Sujeto(object):
    def __init__(self,dni,nombre,apellido,edad,fechaNac,sexo,escolaridad,pmanual,obrasocial,consentimiento):
        self.DNI=dni
        self.nombre=nombre
        self.apellido=apellido
        self.edad=edad
        self.fechaNac=fechaNac
        self.sexo=sexo
        self.escolaridad=escolaridad
        self.pmanual=pmanual

class Pagina():
    def mostrarSujetos():
        listaSujetos = []
        for x in sujetos:
             referencia= x.apellido+", "+x.nombre
             listaSujetos.append(referencia)
        return listaSujetos

class PaginaSujeto():
    def mostrarDatos(pos):
        return [sujetos[pos].nombre, sujetos[pos].DNI]

codigos=[]
for x in diccionarioInformes:
    codigos.append(x)

sujetos = [] #lista con las instancias de Sujeto de cada sujeto
for x in diccionarioInformes:
    dni=diccionarioInformes[x]['\ufeffDatosPersonales']["DNI"]
    nombre=diccionarioInformes[x]['\ufeffDatosPersonales']["nombre"]
    apellido=diccionarioInformes[x]['\ufeffDatosPersonales']["apellido"]
    edad=diccionarioInformes[x]['\ufeffDatosPersonales']["edad_eval"]
    fechaNac=diccionarioInformes[x]['\ufeffDatosPersonales']["fecha_nac"]
    sexo=diccionarioInformes[x]['\ufeffDatosPersonales']["sexo"]
    escolaridad=diccionarioInformes[x]['\ufeffDatosPersonales']["años_esc"]
    pmanual=diccionarioInformes[x]['\ufeffDatosPersonales']["pref_manual"]
    obrasocial=diccionarioInformes[x]['\ufeffDatosPersonales']["obra_social"]
    consentimiento=diccionarioInformes[x]['\ufeffDatosPersonales']["consent"]
    sujetos.append(Sujeto(dni,nombre,apellido,edad,fechaNac,sexo,escolaridad,pmanual,obrasocial,consentimiento))

#home para desplegar nombres de los sujetos evaluados
@app.route("/")
def home_www():
    return render_template("index.html", titulo=titulo, sujetos=Pagina.mostrarSujetos())

@app.route("/sujeto/<string:ruta>")
def sujeto_www(ruta):
    for n,x in enumerate(sujetos):
        if x.DNI == ruta:
            return render_template("sujeto.html", titulo=titulo, datos=PaginaSujeto.mostrarDatos(n))

app.run(host="localhost", port=8080, debug=True)




