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
    def evaluacionesSemana():
        evaluacionesSemana = []
        for x in evaluaciones:
            if (datetime.now() - evaluaciones[x].fechaEv).days <= 7:
                nombreCompleto= evaluaciones[x].datosPersonales["apellido"]+", "+evaluaciones[x].datosPersonales["nombre"]
                fecha = evaluaciones[x].fechaEv.strftime("%x")
                evaluacionesSemana.append((nombreCompleto,fecha,x))
        return evaluacionesSemana
    def evaluacionesMes():
        evaluacionesMes = []
        for x in evaluaciones:
            if (datetime.now() - evaluaciones[x].fechaEv).days <=30:
                nombreCompleto= evaluaciones[x].datosPersonales["apellido"]+", "+evaluaciones[x].datosPersonales["nombre"]
                fecha = evaluaciones[x].fechaEv.strftime("%x")
                evaluacionesMes.append((nombreCompleto,fecha,x))
        return evaluacionesMes

class PaginaSujeto():
    def __init__(self,sujeto):
        self.sujeto = sujeto
    def mostrarAbstractEvaluaciones(self):
        abstractEvaluaciones=[]
        for i,x in enumerate(self.sujeto.evaluaciones):
            stringFecha = self.sujeto.evaluaciones[i].fechaEv.strftime("%d")+"/"+self.sujeto.evaluaciones[i].fechaEv.strftime("%m")+"/"+self.sujeto.evaluaciones[i].fechaEv.strftime("%y")
            if len(self.sujeto.informes) > 0:
                for j,y in enumerate(self.sujeto.informes):
                        if self.sujeto.evaluaciones[i].fechaEv == self.sujeto.informes[j].fechaEv:
                            abstractEvaluaciones.append((stringFecha,self.sujeto.informes[j].conclusion))
                        else:
                            abstractEvaluaciones.append((stringFecha,"No hay datos de informe disponibles"))
            else:
                abstractEvaluaciones.append((stringFecha,"No hay datos de informe disponibles"))
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
    return render_template("index.html", titulo=titulo, sujetos=Pagina.todosSujetos(), evSemana=Pagina.evaluacionesSemana(), evMes=Pagina.evaluacionesMes())

@app.route("/sujetos/<string:dni>")
def sujeto_www(dni):
    for x in sujetos:
        if sujetos[x].DNI == dni:
            pagina=PaginaSujeto(sujetos[x])
            return render_template("sujeto.html", titulo=titulo, datos=pagina.sujeto, abstractEvaluaciones=pagina.mostrarAbstractEvaluaciones(), codigo=x)

@app.route("/evaluaciones/<string:codigo>")
def evaluacion_www(codigo):
    for x in evaluaciones:
        if x == codigo:
            pagina=PaginaEvaluaciones(sujetos[x],evaluaciones[x])
            return render_template("evaluacion.html", titulo=titulo, datosSujeto=pagina.sujeto, datosEvaluacion=pagina.evaluacion, pruebas=pagina.pruebasAdmin())

app.run(host="localhost", port=8080, debug=True)
