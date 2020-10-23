from flask import Flask, render_template, redirect, url_for, request, Response, session
from datetime import datetime, date, timedelta
from terminos import terminos,lista_pruebas
import string
import json
from modulos import serializador
import csv
import random
import hashlib
from compilador import Compilador
from presentador import Presentador

#funciona para excel v201020

app = Flask(__name__)
app.secret_key="WakaWaka"
app.permanent_session_lifetime = timedelta(hours=1)
titulo = "Evaluaciones"

users= {
    "dsanchez" : {
        "username" : "dsanchez",
        "pass" : "23d9f302a71657cfd6b4f91519734c62f580acd3b9f4744cb776f308296500cc4852ded4f40992630abfd0a988992432d3bd2ecd77d1b1bd522f09434c5a80b4",
        "nombre":"Daniel",
        "admin": True
    },
    "agaliani" : {
        "username" : "agaliani",
        "pass" : "de9485d8858daa9e2822777b1e2ffa3a2ad959ffc2e36bf0b5b4a572fd73833a5245c173410acea8dddd7d5db0f0da364ee6f879aff5f0e24446f00d034b9212",
        "nombre":"Agostina",
        "admin": False
    },
}

def validuser(u,p):
    encontrado = False
    phasheado = hashlib.pbkdf2_hmac('sha512', p.encode('utf-8'), b'salt', 100000).hex()
    for i,usuario in users.items():        
        if usuario["username"] == u and usuario["pass"] == phasheado:
            encontrado = True
    return encontrado

presentador=Presentador()
sujetos=presentador.sujetos
evaluaciones=presentador.evaluaciones
informes=presentador.informes



#home para desplegar nombres de los sujetos evaluados
@app.route("/", methods=["POST","GET"])
def home_www():
    #esta parte es para el filtro
    listado=[]
    edad_min=request.args.get('age_min')
    if edad_min == None:
        edad_min = 16
    edad_max=request.args.get('age_max')
    if edad_max == None:
        edad_max = 100
    escolaridad_min=request.args.get('edu_min')
    if escolaridad_min == None:
        escolaridad_min = 0
    escolaridad_max=request.args.get('edu_max')
    if escolaridad_max == None:
        escolaridad_max = 25
    sexo_req=request.args.getlist('sexo')
    if sexo_req == None:
        sexo_req = []
    pruebas_req=request.args.getlist('prueba')
    if pruebas_req == None:
        pruebas_req = []
    for x in evaluaciones:
        if (evaluaciones[x].sexo in sexo_req) and int(edad_min) < evaluaciones[x].edad < int(edad_max) and int(escolaridad_min) < evaluaciones[x].escolaridad < int(escolaridad_max) and all(elem in evaluaciones[x].pruebasAdministradas for elem in pruebas_req):
            listado.append(evaluaciones[x])
    sz=serializador()
    series=sz.extraer(listado)
    
    #para consolidar como json
    #archivo=f"""{sz.nombrar()}.json
    #with open(archivo,"w") as f:
        #json.dump(series,f,indent=4)"""
    
    #para consolidad como csv
    headers=[]
    for x in series:
        for k in x:
            if k not in headers:
                headers.append(k)
    with open("datos.csv","w") as f:
        out=csv.DictWriter(f,headers)
        out.writeheader()
        for x in series:
            out.writerow(x)

    if "user" in session:
        user=session["user"]
        nombre_usuario=users[user]["nombre"]
        return render_template("index.html", titulo=titulo, usuario=nombre_usuario, sujetos=presentador.get_sujetos_alfab(), evRecientes=presentador.get_evaluaciones_fecha(),resultado=listado,edad_min=edad_min, edad_max=edad_max, edu_min=escolaridad_min, edu_max=escolaridad_max, sexo=sexo_req, pruebas=lista_pruebas, preq=pruebas_req)
    else:
        return redirect(url_for("inicio"))

@app.route("/sujetos/<string:dni>")
def sujeto_www(dni):
    for x in sujetos:
        if x == dni:
            sujeto=presentador.get_sujeto(dni)
            if "user" in session:
                user=session["user"]
                admin=users[user]["admin"]
                return render_template("sujeto.html", titulo=titulo, admin=admin, datos=sujeto, abstractEvaluaciones=presentador.get_abstract_evaluaciones(sujeto))
            else:
                return redirect(url_for("inicio"))

@app.route("/evaluaciones/<string:codigo>", methods=["POST","GET"])
def evaluacion_www(codigo):
    evaluacion=presentador.get_evaluacion(codigo)
    dni=evaluacion.dni
    sujeto=presentador.get_sujeto(dni)
    if request.args.get('chart_dominio') == None:
        dominio="todos"
    else:
        dominio=request.args.get('chart_dominio')
    if dominio == "atencion":
        labels=presentador.get_atencion_z(evaluacion)[0]
        valores=presentador.get_atencion_z(evaluacion)[1]
    elif dominio == "funciones ejecutivas":
        labels=presentador.get_ffee_z(evaluacion)[0]
        valores=presentador.get_ffee_z(evaluacion)[1]
    elif dominio == "lenguaje":
        labels=presentador.get_lenguaje_z(evaluacion)[0]
        valores=presentador.get_lenguaje_z(evaluacion)[1]
    elif dominio == "funciones visuoperceptivas":
        labels=presentador.get_ffve_z(evaluacion)[0]
        valores=presentador.get_ffve_z(evaluacion)[1] 
    elif dominio == "cognicion social":
        labels=presentador.get_cogsoc_z(evaluacion)[0]
        valores=presentador.get_cogsoc_z(evaluacion)[1] 
    elif dominio == "memoria":
        labels=presentador.get_memoria_z(evaluacion)[0]
        valores=presentador.get_memoria_z(evaluacion)[1]  
    else:
        labels=presentador.get_todos_z(evaluacion)[0]
        valores=presentador.get_todos_z(evaluacion)[1]
    codigo_url=codigo
    if "user" in session:
        return render_template("evaluacion.html", titulo=titulo, datosSujeto=sujeto, datosEvaluacion=evaluacion, pruebas=presentador.get_pruebas_admin(evaluacion), antecedentes=presentador.get_antecedentes(sujeto,evaluacion),labels=labels,valores=valores,codigo=codigo_url,titulo_chart=dominio)
    else:
        return redirect(url_for("inicio"))
    
@app.route("/resultados", methods=["POST","GET"])
def resultados_www():
    termino = request.form["busquedaNav"]
    filtroPruebas = presentador.filtrar_pruebas(termino)
    filtroSujetos = presentador.filtrar_sujetos(termino)
    filtroInformes = presentador.filtrar_informes(termino)
    if "user" in session:
        return render_template("resultados.html", titulo=titulo, pruebas= filtroPruebas, sujetos = filtroSujetos, antecedentes=filtroInformes)
    else:
        return redirect(url_for("inicio"))
 
@app.route("/todos")
def todos_www():
    if "user" in session:
        return render_template("todos.html", titulo=titulo, sujetos=presentador.get_sujetos_alfab()) 
    else:
        return redirect(url_for("inicio"))
    
@app.route("/descargar")
def getPlotCSV():
    with open("datos.csv") as fp:
         csv = fp.read()
    return Response(
        csv,
        headers={"Content-disposition":
                 "attachment; filename=datos.csv"})

@app.route("/inicio")
def inicio():
    return render_template("home.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        session.permanent = True
        u= request.form["usuario"]
        p= request.form["contra"]
        if validuser(u,p):
            session["user"] = u
            return redirect(url_for("home_www"))
        else:
            return "Usuario o contraseña incorrectos"
    else:
        if "user" in session:
            return redirect(url_for("home_www"))
        else:
            return redirect(url_for("inicio"))

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("inicio"))

app.run(host="localhost", port=8080, debug=True)

