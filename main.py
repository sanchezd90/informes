from flask import Flask, render_template, redirect, url_for
from instanciador import sujetos as sujetos
from instanciador import evaluaciones as evaluaciones

app = Flask(__name__)
titulo = "Evaluaciones"

class Pagina():
    def mostrarSujetos():
        listaSujetos = []
        for x in sujetos:
             referencia= (x.apellido+", "+x.nombre,x.DNI)
             listaSujetos.append(referencia)
        return sorted(listaSujetos)

class PaginaSujeto():
    def mostrarDatos(pos):
        return sujetos[pos]
    def mostrarEvaluaciones(pos):
        listaEvaluaciones=[]
        listaPruebas=[]
        for x in evaluaciones:
            if x.dni == sujetos[pos].DNI:
                listaEvaluaciones.append(x.fechaSplit)
                listaPruebas=x.pruebasAdministradas
        return (sorted(listaEvaluaciones, reverse=True),listaPruebas)
    def mostrarInformes(pos):
        listaInformes=[]
        for x in informes:
            if x.dni = sujetos[pos].DNI:
                listaInformes.append()

"""
class PaginaEvaluaciones:
    def mostrarPruebas(dni,codigo):
        self.dni = dni
        for x in evaluaciones:
            if x.DNI == self.dni:
"""


#home para desplegar nombres de los sujetos evaluados
@app.route("/")
def home_www():
    return render_template("index.html", titulo=titulo, sujetos=Pagina.mostrarSujetos())

@app.route("/sujeto/<string:ruta>")
def sujeto_www(ruta):
    for n,x in enumerate(sujetos):
        if x.DNI == ruta:
            return render_template("sujeto.html", titulo=titulo, datos=PaginaSujeto.mostrarDatos(n), evaluaciones=PaginaSujeto.mostrarEvaluaciones(n)[0], pruebas=PaginaSujeto.mostrarEvaluaciones(n)[1])
"""
@app.route("/sujeto/<string:ruta>/<string:codigo>")
def evaluacion_www(ruta,codigo):
    return render_template("evaluacion.html", titulo=titulo, pruebas=PaginaEvaluacion.mostrarPruebas(n))
"""

app.run(host="localhost", port=8080, debug=True)