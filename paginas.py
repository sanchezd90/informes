from datetime import datetime, date, timedelta
from terminos import terminos,lista_pruebas
import string
import compilador


class Pagina():
    def __init__(self,datos):
        self.sujetos=datos["sujetos"]
        self.evaluaciones=datos["evaluaciones"]
        self.informes=datos["informes"]
    def todosSujetos(self):
        listaSujetos = []
        sujetos_alfabeto = {}
        for x in string.ascii_uppercase:
            sujetos_alfabeto[x]=[]
        for x in self.sujetos:
             referencia= (self.sujetos[x].apellido+", "+self.sujetos[x].nombre,self.sujetos[x].DNI)
             for y in sujetos_alfabeto:
                if referencia[0].startswith(y):
                     sujetos_alfabeto[y].append(referencia)
                sujetos_alfabeto[y].sort()
        return sujetos_alfabeto
    def get_sujetos(self):
        lista_sujetos=[]
        for k,v in self.sujetos.items():
            lista_sujetos.append(v)
        return lista_sujetos
    def evaluacionesRecientes(self):
        evaluacionesRecientes = []
        for x in self.evaluaciones:
            nombreCompleto= self.evaluaciones[x].datosPersonales["apellido"]+", "+self.evaluaciones[x].datosPersonales["nombre"]
            fecha = f"""({self.evaluaciones[x].fechaEv.day}/{self.evaluaciones[x].fechaEv.month}/{self.evaluaciones[x].fechaEv.year})"""
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
                abstractEvaluaciones.append((stringFecha,"No hay datos de informe disponibles para esta evaluación",x))
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
    def mostrar_memoria_z(self):
        diccionario_memoria_z=self.evaluacion.obtener_memoria_z()
        labels_memoria=[]
        valores_memoria=[]
        for x in diccionario_memoria_z:
            labels_memoria.append(x)
            valores_memoria.append(diccionario_memoria_z[x])
        return(labels_memoria,valores_memoria)
    def mostrar_atencion_z(self):
        diccionario_atencion_z=self.evaluacion.obtener_atencion_z()
        labels_atencion=[]
        valores_atencion=[]
        for x in diccionario_atencion_z:
            labels_atencion.append(x)
            valores_atencion.append(diccionario_atencion_z[x])
        return(labels_atencion,valores_atencion)
    def mostrar_ffee_z(self):
        diccionario_ffee_z=self.evaluacion.obtener_ffee_z()
        labels_ffee=[]
        valores_ffee=[]
        for x in diccionario_ffee_z:
            labels_ffee.append(x)
            valores_ffee.append(diccionario_ffee_z[x])
        return(labels_ffee,valores_ffee)
    def mostrar_lenguaje_z(self):
        diccionario_lenguaje_z=self.evaluacion.obtener_lenguaje_z()
        labels_lenguaje=[]
        valores_lenguaje=[]
        for x in diccionario_lenguaje_z:
            labels_lenguaje.append(x)
            valores_lenguaje.append(diccionario_lenguaje_z[x])
        return(labels_lenguaje,valores_lenguaje)
    def mostrar_ffve_z(self):
        diccionario_ffve_z=self.evaluacion.obtener_ffve_z()
        labels_ffve=[]
        valores_ffve=[]
        for x in diccionario_ffve_z:
            labels_ffve.append(x)
            valores_ffve.append(diccionario_ffve_z[x])
        return(labels_ffve,valores_ffve)
    
    def mostrar_cogsoc_z(self):
        diccionario_cogsoc_z=self.evaluacion.obtener_cogsoc_z()
        labels_cogsoc=[]
        valores_cogsoc=[]
        for x in diccionario_cogsoc_z:
            labels_cogsoc.append(x)
            valores_cogsoc.append(diccionario_cogsoc_z[x])
        return(labels_cogsoc,valores_cogsoc)

    def mostrar_todos_z(self):
        diccionario_todos_z={
            **self.evaluacion.obtener_memoria_z(),
            **self.evaluacion.obtener_atencion_z(),
            **self.evaluacion.obtener_ffee_z(),
            **self.evaluacion.obtener_lenguaje_z(),
            **self.evaluacion.obtener_ffve_z(),
            **self.evaluacion.obtener_cogsoc_z(),
        }
        labels_todos=[]
        valores_todos=[]
        for x in diccionario_todos_z:
            labels_todos.append(x)
            valores_todos.append(diccionario_todos_z[x])
        return(labels_todos,valores_todos)

class PaginaResultados(Pagina):
    def __init__(self,termino,datos):
        self.termino = termino.lower()
        self.sujetos=datos["sujetos"]
        self.evaluaciones=datos["evaluaciones"]
        self.informes=datos["informes"]
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


