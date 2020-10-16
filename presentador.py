from datetime import datetime, date, timedelta
from terminos import terminos,lista_pruebas
import string
from compilador import Compilador

class Presentador():
    def __init__(self):
        compilador=Compilador()
        self.datos=compilador.activar()
        self.sujetos=self.datos["sujetos"]
        self.evaluaciones=self.datos["evaluaciones"]
        self.informes=self.datos["informes"]
    def get_sujetos_alfab(self):
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
    def get_evaluaciones_fecha(self):
        evaluacionesRecientes = []
        for x in self.evaluaciones:
            nombreCompleto= self.evaluaciones[x].datosPersonales["apellido"]+", "+self.evaluaciones[x].datosPersonales["nombre"]
            fecha = f"""({self.evaluaciones[x].fechaEv.day}/{self.evaluaciones[x].fechaEv.month}/{self.evaluaciones[x].fechaEv.year})"""
            evaluacionesRecientes.append((fecha,nombreCompleto,x))
        return sorted(evaluacionesRecientes,reverse=True)
    def get_sujeto(self,dni):
        if dni in self.sujetos:
            return self.sujetos[dni]
        else:
            return None
    def get_evaluacion(self,codigo):
        if codigo in self.evaluaciones:
            return self.evaluaciones[codigo]
        else:
            return None
    def get_abstract_evaluaciones(self,sujeto):
        abstractEvaluaciones=[]
        for x in sujeto.evaluaciones:
            stringFecha = sujeto.evaluaciones[x].fechaEv.strftime("%d")+"/"+sujeto.evaluaciones[x].fechaEv.strftime("%m")+"/"+sujeto.evaluaciones[x].fechaEv.strftime("%y")
            if len(sujeto.informes) > 0:
                for y in sujeto.informes:
                        if sujeto.evaluaciones[y].fechaEv == sujeto.informes[y].fechaEv:
                            abstractEvaluaciones.append((stringFecha,sujeto.informes[y].conclusion,x))
                        else:
                            abstractEvaluaciones.append((stringFecha,"No hay datos de informe disponibles",x))
            else:
                abstractEvaluaciones.append((stringFecha,"No hay datos de informe disponibles para esta evaluación",x))
        return (sorted(abstractEvaluaciones, reverse=True))
    def get_pruebas_admin(self,evaluacion):
        lista={}
        for x in evaluacion.pruebasAdministradas:
            lista[x]=evaluacion.pruebas[x]
        return lista
    def get_antecedentes(self,sujeto,evaluacion):
        antecedentes = ""
        for x in sujeto.informes:
            if evaluacion.codigo == sujeto.informes[x].codigo:
                antecedentes += sujeto.informes[x].antecedentes
        return antecedentes
    def get_memoria_z(self,evaluacion):
        diccionario_memoria_z=evaluacion.obtener_memoria_z()
        labels_memoria=[]
        valores_memoria=[]
        for x in diccionario_memoria_z:
            labels_memoria.append(x)
            valores_memoria.append(diccionario_memoria_z[x])
        return(labels_memoria,valores_memoria)
    def get_atencion_z(self,evaluacion):
        diccionario_atencion_z=evaluacion.obtener_atencion_z()
        labels_atencion=[]
        valores_atencion=[]
        for x in diccionario_atencion_z:
            labels_atencion.append(x)
            valores_atencion.append(diccionario_atencion_z[x])
        return(labels_atencion,valores_atencion)
    def get_ffee_z(self,evaluacion):
        diccionario_ffee_z=evaluacion.obtener_ffee_z()
        labels_ffee=[]
        valores_ffee=[]
        for x in diccionario_ffee_z:
            labels_ffee.append(x)
            valores_ffee.append(diccionario_ffee_z[x])
        return(labels_ffee,valores_ffee)
    def get_lenguaje_z(self,evaluacion):
        diccionario_lenguaje_z=evaluacion.obtener_lenguaje_z()
        labels_lenguaje=[]
        valores_lenguaje=[]
        for x in diccionario_lenguaje_z:
            labels_lenguaje.append(x)
            valores_lenguaje.append(diccionario_lenguaje_z[x])
        return(labels_lenguaje,valores_lenguaje)
    def get_ffve_z(self,evaluacion):
        diccionario_ffve_z=evaluacion.obtener_ffve_z()
        labels_ffve=[]
        valores_ffve=[]
        for x in diccionario_ffve_z:
            labels_ffve.append(x)
            valores_ffve.append(diccionario_ffve_z[x])
        return(labels_ffve,valores_ffve)
    def get_cogsoc_z(self,evaluacion):
        diccionario_cogsoc_z=evaluacion.obtener_cogsoc_z()
        labels_cogsoc=[]
        valores_cogsoc=[]
        for x in diccionario_cogsoc_z:
            labels_cogsoc.append(x)
            valores_cogsoc.append(diccionario_cogsoc_z[x])
        return(labels_cogsoc,valores_cogsoc)
    def get_todos_z(self,evaluacion):
        diccionario_todos_z={
            **evaluacion.obtener_memoria_z(),
            **evaluacion.obtener_atencion_z(),
            **evaluacion.obtener_ffee_z(),
            **evaluacion.obtener_lenguaje_z(),
            **evaluacion.obtener_ffve_z(),
            **evaluacion.obtener_cogsoc_z(),
        }
        labels_todos=[]
        valores_todos=[]
        for x in diccionario_todos_z:
            labels_todos.append(x)
            valores_todos.append(diccionario_todos_z[x])
        return(labels_todos,valores_todos)
    def filtrar_pruebas(self,termino):
        termino = termino.lower()
        for x in terminos:
            if terminos[x].find(termino) > -1:
                termino = x
        resultadosP = []
        for x in self.evaluaciones:
            contiene = False
            lista_de_pruebas = [x.lower() for x in self.evaluaciones[x].pruebasAdministradas]
            for y in lista_de_pruebas:
                if y.find(termino) > -1:
                    contiene=True
            if contiene:
                resultadosP.append(self.evaluaciones[x])
        return resultadosP
    def filtrar_sujetos(self,termino):
        termino = termino.lower()
        resultadosS = []
        for x in self.evaluaciones:
            if self.evaluaciones[x].nombreCompleto.lower().find(termino)>-1:
                resultadosS.append(self.evaluaciones[x])
        return resultadosS
    def filtrar_informes(self,termino):
        termino = termino.lower()
        resultadosI = []
        for x in self.informes:
            if self.informes[x].antecedentes.lower().find(termino)>-1:
                resultadosI.append(self.informes[x])
        return resultadosI
