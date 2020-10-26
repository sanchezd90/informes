import datetime
import json

#funcionamiento óptimo a partir de excel v201020

class Sujeto():
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
        if "versionExcel" in self.datosPersonales:
            self.versionExcel=self.datosPersonales["versionExcel"]
        else:
            self.versionExcel=None


    def convertir_PEaZ(self,pe):
        if pe == "":
            z=""
        else:
            z=(int(pe)-10)/3
        return z

    def convertir_PEstaZ(self,PEst):
        if PEst == "":
            z=""
        else:
            z=(int(PEst)-100)/15
        return z

    def volver_diccionario_z(self,diccionario):
        diccionario_z={}
        for k,v in diccionario.items():
            if v != "":
                if type(v)==str:
                    v = float(v.replace(",","."))
                diccionario_z.update({k:v}) 
        return diccionario_z
    def obtener_memoria_z(self):
        self.memoria_z={}
        memoria_pruebas=["Relatos (WMS IV)","RAVLT (Tambor50)","ROCF","RAVLT (Pasto50)","Taylor","RAVLT (Tambor60)"]
        memoria_puntajes_estandarizados=["TRIAL 1_pje_z","SUMA_TRIALS_pje_z","TRIALB_pje_z","DIFERIDO_pje_z","RECONOCIMIENTO_pje_z","Aprendizaje total corregido_pje_Z","Tasa de aprendizaje_pje_Z","Interferencia proactiva_pje_Z","Interferencia retroactiva_pje_Z","Retención_pje_Z","Eficiencia de evocación_pje_Z","ROCF_dif_z","ROCF_rec_z","Taylor_dif_z","Taylor_rec_z"]
        for x in memoria_pruebas:
            for y in memoria_puntajes_estandarizados:
                if x in self.pruebasAdministradas and y in self.pruebas[x] and self.pruebas[x][y] != "":
                    self.memoria_z[y]=float(self.pruebas[x][y].replace(",","."))
        return self.memoria_z
    def obtener_atencion_z(self):
        self.atencion={
            "RAVLT T1":self.pruebas["RAVLT (Tambor50)"]["TRIAL 1_pje_z"],
            "RAVLT T1":self.pruebas["RAVLT (Pasto50)"]["TRIAL 1_pje_z"],
            "RAVLT T1":self.pruebas["RAVLT (Tambor60)"]["TRIAL 1_pje_z"],
            "Span Directo W-IV":self.pruebas["Dígitos adelante (WAISIV)"]["DD_spanDirecto__pje_z"],
            "TMT A (escrito)":self.pruebas["TMT (escrito)"]["TMT_A_escrito_pje_z"],
            "TMT B (escrito)":self.pruebas["TMT (escrito)"]["TMT_B_escrito_pje_z"],
            "TMT A (oral)":self.pruebas["TMT (oral)"]["TMT_A_oral_pje_z"],
            "TMT B (oral)":self.pruebas["TMT (oral)"]["TMT_B_oral_pje_z"],
            "Dígitos-Símbolos W-IV":self.convertir_PEaZ(self.pruebas["Dígitos-Símbolo (WAISIV)"]["DigSim_IV_pje_es"]),
            "Búsqueda de Símbolos":self.convertir_PEaZ(self.pruebas["Búsqueda de Simbolos (WAISIV)"]["BusSim_IV_pje_es"]),
            "Símbolos-Dígitos (SDMT)":self.pruebas["SDMT"]["SDMT_pje_z"],
            "Stroop":self.pruebas["STROOP"]["stroop_inter_pje_z"]
            }                  
        return self.volver_diccionario_z(self.atencion)
    def obtener_ffee_z(self):
        self.ffee={
            "IFS":self.pruebas["IFS"]["IFS_z"],
            "Span Inverso W-IV":self.pruebas["Dígitos atrás (WAISIV)"]["DI_spanInverso_z_pje_z"],
            "Ord. N-L W-IV":self.convertir_PEaZ(self.pruebas["Ordenamiento N-L (WAISIV)"]["ONL_IV_pje_es"]), 
            "Aritmética W-IV":self.convertir_PEaZ(self.pruebas["Aritmética (WAISIV)"]["WAIS_IV_Ar_pje_es"]),
            "Hayling Test":self.pruebas["Hayling Test"]["hay_anor_pje_z"],
            "WCST (48)":self.pruebas["WCST (48)"]["WCST_cat_pje_z"],
            "Hotel":self.pruebas["HOTEL"]["hotel_desvio_pje_z"],
        }
        return self.volver_diccionario_z(self.ffee)

    def obtener_lenguaje_z(self):
        self.lenguaje={
            "Córdoba":self.pruebas["Córdoba"]["COR_pje_z"],
            "Vocabulario W-IV":self.convertir_PEaZ(self.pruebas["Vocabulario (IV)"]["VOC_IV_pje_escalar"]),
            "WATBA-R":self.convertir_PEstaZ(self.pruebas["WATBA-R"]["WA_pje_est"]),
            "Fluencia Fonológica": self.pruebas["Fluencia Fonológica (P)"]["FF_pje_Z"],
            "Fluencia Semántica": self.pruebas["Fluencia Semántica (animales)"]["FS_pje_Z"],
            "Fluencia Fonológica": self.pruebas["Fluencia Fonológica (M)"]["FF_pje_Z"],
            "Fluencia Semántica": self.pruebas["Fluencia Semántica (casa)"]["FS_pje_Z"]
        }
        return self.volver_diccionario_z(self.lenguaje)

    def obtener_ffve_z(self):
        self.ffve={
            "Copia ROCF":self.pruebas["ROCF"]["ROCF_copia_z"],
            "Copia Taylor":self.pruebas["Taylor"]["Taylor_copia_z"]
        }
        return self.volver_diccionario_z(self.ffve)   

    def obtener_cogsoc_z(self):
        self.cogsoc={
            "Caras (MINI-SEA)":self.pruebas["Caras (Mini-SEA)"]["REF_pje_z"],
            "Faux Pas (MINI-SEA)":self.pruebas["Faux Pas (Mini-SEA)"]["FP_pje_z"],
            "Mind in the Eyes (36)":self.pruebas["EYES (36)"]["RME_pje_z"],
            "Mind in the Eyes (24)":self.pruebas["EYES (24)"]["RME_pje_z"],
            "Mind in the Voice (25)":self.pruebas["VOICE (25)"]["RMV_pje_z"],
        }
        return self.volver_diccionario_z(self.cogsoc)   

class Informe():
    def __init__(self,nombre,dni,fechaEv,antecedentes,conclusion):
        self.nombre = nombre
        self.dni = dni
        self.fechaEv = fechaEv
        self.codigo = dni+"-"+self.fechaEv.strftime("%y")+"-"+self.fechaEv.strftime("%m")+"-"+self.fechaEv.strftime("%d")
        self.antecedentes = antecedentes
        self.conclusion = conclusion

class Compilador():
    def __init__(self):
        self.sujetos={}
        self.evaluaciones={}
        self.informes={}
        self.diccionarioEvaluaciones=None
        with open("evaluaciones.json","r") as f:
            self.diccionarioEvaluaciones = json.load(f)
        self.diccionarioInformes=None
        with open("informes.json","r") as f:
            self.diccionarioInformes = json.load(f)
    def compilar_sujetos(self):
        for x in self.diccionarioEvaluaciones:
            if len(self.sujetos) == 0:
                dni=self.diccionarioEvaluaciones[x]['DatosPersonales']["DNI"]
                nombre=self.diccionarioEvaluaciones[x]['DatosPersonales']["nombre"]
                apellido=self.diccionarioEvaluaciones[x]['DatosPersonales']["apellido"]
                edad=self.diccionarioEvaluaciones[x]['DatosPersonales']["edad_eval"]
                splitFechaNac=self.diccionarioEvaluaciones[x]['DatosPersonales']["fecha_nac"].split("/")
                if splitFechaNac[2] == "00":
                    splitFechaNac[2] = "1900"
                if splitFechaNac[0] == "0":
                    splitFechaNac[0] = "1"
                fechaNac=datetime.datetime(int(splitFechaNac[2]),int(splitFechaNac[1]),int(splitFechaNac[0]))
                sexo=self.diccionarioEvaluaciones[x]['DatosPersonales']["sexo"]
                escolaridad=self.diccionarioEvaluaciones[x]['DatosPersonales']["años_esc"]
                pmanual=self.diccionarioEvaluaciones[x]['DatosPersonales']["pref_manual"]
                obrasocial=self.diccionarioEvaluaciones[x]['DatosPersonales']["obra_social"]
                self.sujetos[x[0:x.find("-")]]=Sujeto(dni,nombre,apellido,edad,fechaNac,sexo,escolaridad,pmanual,obrasocial)
            else:
                for k,v in self.sujetos.items():                    
                    if  self.diccionarioEvaluaciones[x]['DatosPersonales']["DNI"] != v.DNI:
                        dni=self.diccionarioEvaluaciones[x]['DatosPersonales']["DNI"]
                        nombre=self.diccionarioEvaluaciones[x]['DatosPersonales']["nombre"]
                        apellido=self.diccionarioEvaluaciones[x]['DatosPersonales']["apellido"]
                        edad=self.diccionarioEvaluaciones[x]['DatosPersonales']["edad_eval"]
                        splitFechaNac=self.diccionarioEvaluaciones[x]['DatosPersonales']["fecha_nac"].split("/")
                        if splitFechaNac[2] == "00":
                            splitFechaNac[2] = "1900"
                        if splitFechaNac[0] == "0":
                            splitFechaNac[0] = "1"
                        fechaNac=datetime.datetime(int(splitFechaNac[2]),int(splitFechaNac[1]),int(splitFechaNac[0]))
                        sexo=self.diccionarioEvaluaciones[x]['DatosPersonales']["sexo"]
                        escolaridad=self.diccionarioEvaluaciones[x]['DatosPersonales']["años_esc"]
                        pmanual=self.diccionarioEvaluaciones[x]['DatosPersonales']["pref_manual"]
                        obrasocial=self.diccionarioEvaluaciones[x]['DatosPersonales']["obra_social"]
                        self.sujetos[x[0:x.find("-")]]=Sujeto(dni,nombre,apellido,edad,fechaNac,sexo,escolaridad,pmanual,obrasocial)
                        break
    def compilar_evaluaciones(self):
        for x in self.diccionarioEvaluaciones:
            dni=self.diccionarioEvaluaciones[x]['DatosPersonales']["DNI"]
            splitfechaEv=self.diccionarioEvaluaciones[x]['DatosPersonales']["fecha_ev"].split("/")
            if splitfechaEv[2] == "2020":
                splitfechaEv[2] = "20"
            for i,s in enumerate(splitfechaEv):
                if len(s)<2:
                    splitfechaEv[i]="0"+splitfechaEv[i]
            codigo=dni+"-"+splitfechaEv[2]+"-"+splitfechaEv[1]+"-"+splitfechaEv[0]
            fechaEv=datetime.datetime(int("20"+splitfechaEv[2]),int(splitfechaEv[1]),int(splitfechaEv[0]))
            pruebas={}
            for y in self.diccionarioEvaluaciones[x]:
                pruebas.update({y:self.diccionarioEvaluaciones[x][y]})
            pruebas.pop('DatosPersonales')
            datosPersonales=self.diccionarioEvaluaciones[x]['DatosPersonales']
            self.evaluaciones[codigo]=Evaluacion(dni,fechaEv,pruebas,datosPersonales)
    def compilar_informes(self):
        for x in self.diccionarioInformes:
            nombre=self.diccionarioInformes[x]["nombre"]
            dni=self.diccionarioInformes[x]["dni"]
            fechaEv= self.diccionarioInformes[x]["fechaEv"]
            fechaEv= datetime.datetime(int(fechaEv[0]),int(fechaEv[1]),int(fechaEv[2]))
            codigo=dni+"-"+fechaEv.strftime("%y")+"-"+fechaEv.strftime("%m")+"-"+fechaEv.strftime("%d")
            antecedentes = self.diccionarioInformes[x]["antecedentes"]
            conclusion = self.diccionarioInformes[x]["conclusion"]
            self.informes[codigo]=Informe(nombre,dni,fechaEv,antecedentes,conclusion)
    def activar(self):
        self.compilar_sujetos()
        self.compilar_evaluaciones()
        self.compilar_informes()
        for x in self.sujetos:
            for y in self.informes:
                if self.sujetos[x].DNI == self.informes[y].dni:
                    self.sujetos[x].informes.update({y:self.informes[y]})
            for z in self.evaluaciones:
                if self.sujetos[x].DNI == self.evaluaciones[z].dni:
                    self.sujetos[x].evaluaciones.update({z:self.evaluaciones[z]})
        return {"sujetos":self.sujetos,"evaluaciones":self.evaluaciones,"informes":self.informes}







