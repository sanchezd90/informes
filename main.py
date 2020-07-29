from flask import Flask, render_template, redirect, url_for
from instanciador import sujetos as sujetos
from instanciador import evaluaciones as evaluaciones

app = Flask(__name__)
titulo = "Evaluaciones"

class Pagina():
    def mostrarSujetos():
        listaSujetos = []
        for x in sujetos:
             referencia= (x.apellido+" "+x.nombre,x.DNI)
             listaSujetos.append(referencia)
        return listaSujetos

class PaginaSujeto():
    def mostrarDatos(pos):
        return sujetos[pos]
    def mostrarEvaluaciones(pos):
        listaEvaluaciones=[]
        for x in evaluaciones:
            if x.dni == sujetos[pos].DNI:
                listaEvaluaciones.append(x.fechaSplit)
        return listaEvaluaciones

class Evaluacion():
    def __init__(self,dni,fechaEv,pruebas):
        split=fechaEv.split("/")
        self.fechaEv=split[2]+"-"+split[1]+"-"+split[0]
        self.codigo = dni+"-"+self.fechaEv
        self.pruebas = pruebas
        self.pruebasAdministradas = []
        for x in self.pruebas:
            suma = 0
            for y in self.pruebas[x]:
                suma += len(self.pruebas[x][y])
            if suma > 0:
                self.pruebasAdministradas.append(x)
    def fueAdministrada(self,pedido):
        if pedido in self.pruebasAdministradas:
            return True
        else:
            return False

#home para desplegar nombres de los sujetos evaluados
@app.route("/")
def home_www():
    return render_template("index.html", titulo=titulo, sujetos=Pagina.mostrarSujetos())

@app.route("/sujeto/<string:ruta>")
def sujeto_www(ruta):
    for n,x in enumerate(sujetos):
        if x.DNI == ruta:
            return render_template("sujeto.html", titulo=titulo, datos=PaginaSujeto.mostrarDatos(n), evaluaciones=PaginaSujeto.mostrarEvaluaciones(n))



app.run(host="localhost", port=8080, debug=True)