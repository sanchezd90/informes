import os
from flask import Flask, render_template
import lector
app = Flask(__name__)
titulo = "Informes"

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

codigos=[]
for x in diccionarioInformes:
    codigos.append(x)

sujetos = []
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

app.run(host="localhost", port=8080, debug=True)




