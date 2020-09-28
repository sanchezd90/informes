import datetime
import json

with open("evaluaciones.json","r") as f:
    diccionarioEvaluaciones = json.load(f)

with open("informes.json","r") as f:
    diccionarioInformes = json.load(f)

def convertir_PEaZ(pe):
    if pe == "":
        z=""
    else:
        z=(int(pe)-10)/3
    return z

def convertir_PEstaZ(PEst):
    if PEst == "":
        z=""
    else:
        z=(int(PEst)-100)/15
    return z

def volver_diccionario_z(diccionario):
    diccionario_z={}
    for k,v in diccionario.items():
        if v != "":
            if type(v)==str:
                v = float(v.replace(",","."))
            diccionario_z.update({k:v}) 
    return diccionario_z

class Sujeto(object):
    def __init__(self,dni,nombre,apellido,edad,fechaNac,sexo,escolaridad,pmanual,obrasocial):
        self.DNI=dni
        self.nombre=nombre
        self.apellido=apellido
        edad = edad.split(",")
        self.edad = int(edad[0])
        self.fechaNac= fechaNac
        self.sexo=sexo
        self.escolaridad=int(escolaridad)
        self.pmanual=pmanual
        self.informes = {}
        self.evaluaciones = {}

class Evaluacion():
    def __init__(self,dni,fechaEv,pruebas,datosPersonales):
        self.fechaEv = fechaEv
        self.dni = dni
        self.codigo = dni+"-"+self.fechaEv.strftime("%y")+"-"+self.fechaEv.strftime("%m")+"-"+self.fechaEv.strftime("%d")
        self.datosPersonales=datosPersonales
        self.sexo= self.datosPersonales["sexo"]
        self.edad= self.datosPersonales["edad_eval"].split(",")
        self.edad = int(self.edad[0])
        self.escolaridad= int(self.datosPersonales["años_esc"])
        self.dominancia=self.datosPersonales["pref_manual"]
        self.derivador=self.datosPersonales["derivador"]
        self.evaluador=self.datosPersonales["evaluador"]
        self.dxs=[]
        if self.datosPersonales["dx1"] != "":
            self.dxs.append({"diagnóstico":self.datosPersonales["dx1"],"fecha":self.datosPersonales["dx1_fecha"],"tratamiento":self.datosPersonales["dx1_fecha_tto"]})
        if self.datosPersonales["dx2"] != "":
            self.dxs.append({"diagnóstico":self.datosPersonales["dx2"],"fecha":self.datosPersonales["dx2_fecha"],"tratamiento":self.datosPersonales["dx2_fecha_tto"]})
        if self.datosPersonales["dx3"] != "":
            self.dxs.append({"diagnóstico":self.datosPersonales["dx3"],"fecha":self.datosPersonales["dx3_fecha"],"tratamiento":self.datosPersonales["dx3_fecha_tto"]})
        if self.datosPersonales["dx4"] != "":
            self.dxs.append({"diagnóstico":self.datosPersonales["dx4"],"fecha":self.datosPersonales["dx4_fecha"],"tratamiento":self.datosPersonales["dx4_fecha_tto"]})
        if self.datosPersonales["dx5"] != "":
            self.dxs.append({"diagnóstico":self.datosPersonales["dx5"],"fecha":self.datosPersonales["dx5_fecha"],"tratamiento":self.datosPersonales["dx5_fecha_tto"]})
        self.nombreCompleto = self.datosPersonales["apellido"]+", "+self.datosPersonales["nombre"]
        self.pruebas = pruebas
        self.pruebasAdministradas = []
        for x in self.pruebas:
            suma = 0
            for y in self.pruebas[x]:
                suma += len(self.pruebas[x][y])
            if suma > 0:
                self.pruebasAdministradas.append(x)
    def obtener_memoria_z(self):
        self.memoria_z={}
        memoria_pruebas=["Relatos","RAVLT","ROCF"]
        memoria_puntajes_estandarizados=["Z_SUMA_TRIALS","Aprendizaje total corregido_Z","Tasa de aprendizaje_Z","Z_ADQ","Z_TRIALB","Interferencia proactiva_Z","Interferencia retroactiva_Z","Z_DIFERIDO","Eficiencia de evocación_Z","Z_DIF","Retención_Z","ROCF_dif_z","Z_RECONOCIMIENTO","ROCF_rec_z"]
        for x in memoria_pruebas:
            for y in memoria_puntajes_estandarizados:
                if x in self.pruebasAdministradas and y in self.pruebas[x] and self.pruebas[x][y] != "":
                    self.memoria_z[y]=float(self.pruebas[x][y].replace(",","."))
        return self.memoria_z
    def obtener_atencion_z(self):
        self.atencion={
            "Trial 1 RAVLT":self.pruebas["RAVLT"]["Z_TRIAL 1"],
            "Span Directo":self.pruebas["Dígitos adelante"]["spanDirecto_z"],
            "TMT A":self.pruebas["TMT"]["TMT_A_z"],
            "TMT B":self.pruebas["TMT"]["TMT_B_z"],
            "Dígitos-Símbolo":convertir_PEaZ(self.pruebas["Dígitos-Símbolo"]["DigSim_PE"]),
            "Búsqueda de Símbolos":convertir_PEaZ(self.pruebas["Búsqueda de Simbolos"]["BusSim_PE"]),
            "Stroop":self.pruebas["STROOP"]["stroop_inter_z"],
        }          
        return volver_diccionario_z(self.atencion)
    def obtener_ffee_z(self):
        self.ffee={
            "IFS":self.pruebas["IFS"]["IFS_z"],
            "Span Inverso":self.pruebas["Dígitos atrás"]["spanInverso_z"],
            "Ord. N-L":convertir_PEaZ(self.pruebas["Ordenamiento N-L"]["ONL_PE"]), 
            "Aritmética":convertir_PEaZ(self.pruebas["Aritmética"]["Ar_PE"]),
            "Hayling Test":self.pruebas["Hayling Test"]["hay_anor_z"],
            "WCST":self.pruebas["WCST"]["WCST_cat_z"],
            "Hotel":self.pruebas["HOTEL"]["hotel_z_desvio"],
        }
        return volver_diccionario_z(self.ffee)

    def obtener_lenguaje_z(self):
        self.lenguaje={
            "Córdoba":self.pruebas["Córdoba"]["Z"],
            "Vocabulario":convertir_PEaZ(self.pruebas["Vocabulario"]["Escalar"]),
            "WATBA":convertir_PEstaZ(self.pruebas["WATBA_R"]["CI estimativo"]) 
        }
        return volver_diccionario_z(self.lenguaje)

    def obtener_ffve_z(self):
        self.ffve={
            "Copia ROCF":self.pruebas["ROCF"]["ROCF_copia_z"]
        }
        return volver_diccionario_z(self.ffve)   

    def obtener_cogsoc_z(self):
        self.cogsoc={
            "Emociones Faciales":self.pruebas["Caras"]["REF_z"],
            "Mind in Eyes":self.pruebas["EYES"]["RME_z"],
        }
        return volver_diccionario_z(self.cogsoc)   

class Informe():
    def __init__(self,nombre,dni,fechaEv,antecedentes,conclusion):
        self.nombre = nombre
        self.dni = dni
        self.fechaEv = fechaEv
        self.codigo = dni+"-"+self.fechaEv.strftime("%y")+"-"+self.fechaEv.strftime("%m")+"-"+self.fechaEv.strftime("%d")
        self.antecedentes = antecedentes
        self.conclusion = conclusion

sujetos = {} #lista con las instancias de Sujeto de cada sujeto
for x in diccionarioEvaluaciones:
    if len(sujetos) == 0:
        dni=diccionarioEvaluaciones[x]['DatosPersonales']["DNI"]
        nombre=diccionarioEvaluaciones[x]['DatosPersonales']["nombre"]
        apellido=diccionarioEvaluaciones[x]['DatosPersonales']["apellido"]
        edad=diccionarioEvaluaciones[x]['DatosPersonales']["edad_eval"]
        splitFechaNac=diccionarioEvaluaciones[x]['DatosPersonales']["fecha_nac"].split("/")
        if splitFechaNac[2] == "00":
            splitFechaNac[2] = "1900"
        if splitFechaNac[0] == "0":
            splitFechaNac[0] = "1"
        fechaNac=datetime.datetime(int(splitFechaNac[2]),int(splitFechaNac[1]),int(splitFechaNac[0]))
        sexo=diccionarioEvaluaciones[x]['DatosPersonales']["sexo"]
        escolaridad=diccionarioEvaluaciones[x]['DatosPersonales']["años_esc"]
        pmanual=diccionarioEvaluaciones[x]['DatosPersonales']["pref_manual"]
        obrasocial=diccionarioEvaluaciones[x]['DatosPersonales']["obra_social"]
        sujetos[x[0:x.find("-")]]=Sujeto(dni,nombre,apellido,edad,fechaNac,sexo,escolaridad,pmanual,obrasocial)
    else:
        for k,v in sujetos.items():
            if diccionarioEvaluaciones[x]['DatosPersonales']["DNI"] != v.DNI:
                dni=diccionarioEvaluaciones[x]['DatosPersonales']["DNI"]
                nombre=diccionarioEvaluaciones[x]['DatosPersonales']["nombre"]
                apellido=diccionarioEvaluaciones[x]['DatosPersonales']["apellido"]
                edad=diccionarioEvaluaciones[x]['DatosPersonales']["edad_eval"]
                splitFechaNac=diccionarioEvaluaciones[x]['DatosPersonales']["fecha_nac"].split("/")
                if splitFechaNac[2] == "00":
                    splitFechaNac[2] = "1900"
                if splitFechaNac[0] == "0":
                    splitFechaNac[0] = "1"
                fechaNac=datetime.datetime(int(splitFechaNac[2]),int(splitFechaNac[1]),int(splitFechaNac[0]))
                sexo=diccionarioEvaluaciones[x]['DatosPersonales']["sexo"]
                escolaridad=diccionarioEvaluaciones[x]['DatosPersonales']["años_esc"]
                pmanual=diccionarioEvaluaciones[x]['DatosPersonales']["pref_manual"]
                obrasocial=diccionarioEvaluaciones[x]['DatosPersonales']["obra_social"]
                sujetos[x[0:x.find("-")]]=Sujeto(dni,nombre,apellido,edad,fechaNac,sexo,escolaridad,pmanual,obrasocial)
                break

evaluaciones = {}
for x in diccionarioEvaluaciones:
    dni=diccionarioEvaluaciones[x]['DatosPersonales']["DNI"]
    splitfechaEv=diccionarioEvaluaciones[x]['DatosPersonales']["fecha_ev"].split("/")
    for i,s in enumerate(splitfechaEv):
        if len(s)<2:
            splitfechaEv[i]="0"+splitfechaEv[i]
    codigo=dni+"-"+splitfechaEv[2]+"-"+splitfechaEv[1]+"-"+splitfechaEv[0]
    fechaEv=datetime.datetime(int("20"+splitfechaEv[2]),int(splitfechaEv[1]),int(splitfechaEv[0]))
    pruebas={}
    for y in diccionarioEvaluaciones[x]:
        pruebas.update({y:diccionarioEvaluaciones[x][y]})
    pruebas.pop('DatosPersonales')
    datosPersonales=diccionarioEvaluaciones[x]['DatosPersonales']
    evaluaciones[codigo]=Evaluacion(dni,fechaEv,pruebas,datosPersonales)

informes = {}
for x in diccionarioInformes:
    nombre=diccionarioInformes[x]["nombre"]
    dni=diccionarioInformes[x]["dni"]
    fechaEv= diccionarioInformes[x]["fechaEv"]
    fechaEv= datetime.datetime(int(fechaEv[0]),int(fechaEv[1]),int(fechaEv[2]))
    codigo=dni+"-"+fechaEv.strftime("%y")+"-"+fechaEv.strftime("%m")+"-"+fechaEv.strftime("%d")
    antecedentes = diccionarioInformes[x]["antecedentes"]
    conclusion = diccionarioInformes[x]["conclusion"]
    informes[codigo]=Informe(nombre,dni,fechaEv,antecedentes,conclusion)

for x in sujetos:
    for y in informes:
        if sujetos[x].DNI == informes[y].dni:
            sujetos[x].informes.update({y:informes[y]})
    for z in evaluaciones:
        if sujetos[x].DNI == evaluaciones[z].dni:
            sujetos[x].evaluaciones.update({z:evaluaciones[z]})

#pruebas aca abajo
"""for x in evaluaciones:
    print(evaluaciones[x].obtener_ffee_z())"""