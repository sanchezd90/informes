from flask import Flask, render_template, redirect, url_for, request
from instanciador import sujetos
from instanciador import evaluaciones
from instanciador import informes
from datetime import datetime, date
from terminos import terminos
import string

app = Flask(__name__)
titulo = "Evaluaciones"

class Pagina():
    def todosSujetos():
        listaSujetos = []
        sujetos_alfabeto = {}
        for x in string.ascii_uppercase:
            sujetos_alfabeto[x]=[]
        for x in sujetos:
             referencia= (sujetos[x].apellido+", "+sujetos[x].nombre,sujetos[x].DNI)
             for y in sujetos_alfabeto:
                if referencia[0].startswith(y):
                     sujetos_alfabeto[y].append(referencia)
                sujetos_alfabeto[y].sort()
        return sujetos_alfabeto
    def get_sujetos():
        lista_sujetos=[]
        for k,v in sujetos.items():
            lista_sujetos.append(v)
        return lista_sujetos
    def evaluacionesRecientes():
        evaluacionesRecientes = []
        for x in evaluaciones:
            nombreCompleto= evaluaciones[x].datosPersonales["apellido"]+", "+evaluaciones[x].datosPersonales["nombre"]
            fecha = f"""({evaluaciones[x].fechaEv.day}/{evaluaciones[x].fechaEv.month}/{evaluaciones[x].fechaEv.year})"""
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
    def mostrarAntecedentes(self):
        antecedentes = ""
        for x in self.sujeto.informes:
            if self.evaluacion.codigo == self.sujeto.informes[x].codigo:
                antecedentes += self.sujeto.informes[x].antecedentes
        return antecedentes

class PaginaResultados(Pagina):
    def __init__(self,termino,sujetos,informes,evaluaciones):
        self.termino = termino.lower()
        self.sujetos=sujetos
        self.evaluaciones = evaluaciones
        self.informes = informes
    def filtroPruebas(self):
        for x in terminos:
            if terminos[x].find(self.termino) > -1:
                self.termino = x
        resultadosP = []
        for x in self.evaluaciones:
            contiene = False
            lista_de_pruebas = [x.lower() for x in self.evaluaciones[x].pruebasAdministradas]
            for y in lista_de_pruebas:
                if y.find(self.termino) > -1:
                    contiene=True
            if contiene:
                resultadosP.append(self.evaluaciones[x])
        return resultadosP
    def filtroSujetos(self):
        resultadosS = []
        for x in self.evaluaciones:
            if self.evaluaciones[x].nombreCompleto.lower().find(self.termino)>-1:
                resultadosS.append(self.evaluaciones[x])
        return resultadosS
    def filtroInformes(self):
        resultadosI = []
        for x in self.informes:
            if self.informes[x].antecedentes.lower().find(self.termino)>-1:
                resultadosI.append(self.informes[x])
        return resultadosI


#home para desplegar nombres de los sujetos evaluados
@app.route("/", methods=["POST","GET"])
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
            return render_template("evaluacion.html", titulo=titulo, datosSujeto=pagina.sujeto, datosEvaluacion=pagina.evaluacion, pruebas=pagina.pruebasAdmin(), antecedentes=pagina.mostrarAntecedentes())

@app.route("/resultados", methods=["POST","GET"])
def resultados_www():
    termino = request.form["busquedaNav"]
    pagina = PaginaResultados(termino,sujetos,informes,evaluaciones)
    filtroPruebas = pagina.filtroPruebas()
    filtroSujetos = pagina.filtroSujetos()
    filtroInformes = pagina.filtroInformes()
    return render_template("resultados.html", titulo=titulo, pruebas= filtroPruebas, sujetos = filtroSujetos, antecedentes=filtroInformes)

@app.route("/avanzado", methods=["POST","GET"])
def avanzado_www():
    listado=[]
    sexo_request=request.args.get('sexo')
    for x in sujetos:
        if sujetos[x].sexo=="1" and any([sexo_request=="0",sexo_request=="1"]):
            listado.append(sujetos[x])
        elif sujetos[x].sexo=="2" and any([sexo_request=="0",sexo_request=="2"]):
            listado.append(sujetos[x])
    return render_template("avanzado.html", sujetos=listado)

@app.route("/todos")
def todos_www():
    return render_template("todos.html", titulo=titulo, sujetos=Pagina.todosSujetos()) 

@app.route("/edad")
def edad_www():
    return render_template("edad.html", titulo=titulo, sujetos=Pagina.get_sujetos()) 

app.run(host="localhost", port=8080, debug=True)