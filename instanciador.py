import lectorEvaluaciones
import lectorInformes
import datetime

diccionarioEvaluaciones = lectorEvaluaciones.diccionarioEvaluaciones
diccionarioInformes = lectorInformes.diccionarioInformes

class Sujeto(object):
    def __init__(self,dni,nombre,apellido,edad,fechaNac,sexo,escolaridad,pmanual,obrasocial,consentimiento):
        self.DNI=dni
        self.nombre=nombre
        self.apellido=apellido
        edad = edad.split(",")
        self.edad = edad[0]
        self.fechaNac= fechaNac
        self.sexo=sexo
        self.escolaridad=escolaridad
        self.pmanual=pmanual
        self.informes = []
        self.evaluaciones = []

class Evaluacion():
    def __init__(self,dni,fechaEv,pruebas,datosPersonales):
        self.fechaEv = fechaEv
        self.dni = dni
        self.codigo = dni+"-"+self.fechaEv.strftime("%y")+"-"+self.fechaEv.strftime("%m")+"-"+self.fechaEv.strftime("%d")
        self.datosPersonales=datosPersonales
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

class Informe():
    def __init__(self,nombre,dni,fechaEv,antecedentes,conclusion):
        self.nombre = nombre
        self.dni = dni
        self.fechaEv = fechaEv
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
        consentimiento=diccionarioEvaluaciones[x]['DatosPersonales']["consent"]
        sujetos[x]=Sujeto(dni,nombre,apellido,edad,fechaNac,sexo,escolaridad,pmanual,obrasocial,consentimiento)
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
                consentimiento=diccionarioEvaluaciones[x]['DatosPersonales']["consent"]
                sujetos[x]=Sujeto(dni,nombre,apellido,edad,fechaNac,sexo,escolaridad,pmanual,obrasocial,consentimiento)
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
    codigo=dni+"-"+fechaEv.strftime("%y")+"-"+fechaEv.strftime("%m")+"-"+fechaEv.strftime("%d")
    antecedentes = diccionarioInformes[x]["antecedentes"]
    conclusion = diccionarioInformes[x]["conclusion"]
    informes[codigo]=Informe(nombre,dni,fechaEv,antecedentes,conclusion)

for x in sujetos:
    for y in informes:
        if sujetos[x].DNI == informes[y].dni:
            sujetos[x].informes.append(informes[y])
    for z in evaluaciones:
        if sujetos[x].DNI == evaluaciones[z].dni:
            sujetos[x].evaluaciones.append(evaluaciones[z])