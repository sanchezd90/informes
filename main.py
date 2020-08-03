from flask import Flask, render_template, redirect, url_for
from instanciador import sujetos
from instanciador import evaluaciones
from instanciador import informes
from datetime import datetime, date

app = Flask(__name__)
titulo = "Evaluaciones"

class Pagina():
    def todosSujetos():
        listaSujetos = []
        for x in sujetos:
             referencia= (sujetos[x].apellido+", "+sujetos[x].nombre,sujetos[x].DNI)
             listaSujetos.append(referencia)
        return sorted(listaSujetos)
    def evaluacionesRecientes():
        evaluacionesRecientes = []
        for x in evaluaciones:
            nombreCompleto= evaluaciones[x].datosPersonales["apellido"]+", "+evaluaciones[x].datosPersonales["nombre"]
            fecha = evaluaciones[x].fechaEv.strftime("%x")
            evaluacionesRecientes.append((fecha,nombreCompleto,x))
        return sorted(evaluacionesRecientes,reverse=True)

class PaginaSujeto():
    def __init__(self,sujeto):
        self.sujeto = sujeto
    def mostrarAbstractEvaluaciones(self):
        abstractEvaluaciones=[]
        for x in self.sujeto.evaluaciones:
            stringFecha = self.sujeto.evaluaciones[x].fechaEv.strftime("%d")+"/"+self.sujeto.evaluaciones[x].fechaEv.strftime("%m")+"/"+self.sujeto.evaluaciones[x].fechaEv.strftime("%y")
            if len(self.sujeto.informes) > 0:
                for y in self.sujeto.informes:
                        if self.sujeto.evaluaciones[y].fechaEv == self.sujeto.informes[y].fechaEv:
                            abstractEvaluaciones.append((stringFecha,self.sujeto.informes[y].conclusion,x))
                        else:
                            abstractEvaluaciones.append((stringFecha,"No hay datos de informe disponibles",x))
            else:
                abstractEvaluaciones.append((stringFecha,"No hay datos de informe disponibles",x))
        return (sorted(abstractEvaluaciones, reverse=True))

class PaginaEvaluaciones(PaginaSujeto):
    def __init__(self,sujeto,evaluacion):
        super().__init__(sujeto)
        self.evaluacion = evaluacion
        self.pruebasAdministradas = evaluacion.pruebasAdministradas
    def pruebasAdmin(self):
        lista={}
        for x in self.pruebasAdministradas:
            lista[x]=self.evaluacion.pruebas[x]
        return lista

#home para desplegar nombres de los sujetos evaluados
@app.route("/")
def home_www():
    return render_template("index.html", titulo=titulo, sujetos=Pagina.todosSujetos(), evRecientes=Pagina.evaluacionesRecientes())

@app.route("/sujetos/<string:dni>")
def sujeto_www(dni):
    for x in sujetos:
        if x == dni:
            pagina=PaginaSujeto(sujetos[x])
            return render_template("sujeto.html", titulo=titulo, datos=pagina.sujeto, abstractEvaluaciones=pagina.mostrarAbstractEvaluaciones())

@app.route("/evaluaciones/<string:codigo>")
def evaluacion_www(codigo):
    for x in evaluaciones:
        if x == codigo:
            pagina=PaginaEvaluaciones(sujetos[x[0:x.find("-")]],evaluaciones[x])
            return render_template("evaluacion.html", titulo=titulo, datosSujeto=pagina.sujeto, datosEvaluacion=pagina.evaluacion, pruebas=pagina.pruebasAdmin())

app.run(host="localhost", port=8080, debug=True)
