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
    def __init__(self,dni,fechaEv,pruebas):
        self.fechaEv = fechaEv
        self.dni = dni
        self.codigo = dni+"-"+self.fechaEv.strftime("%y")+"-"+self.fechaEv.strftime("%m")+"-"+self.fechaEv.strftime("%d")
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

sujetos = [] #lista con las instancias de Sujeto de cada sujeto
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
        sujetos.append(Sujeto(dni,nombre,apellido,edad,fechaNac,sexo,escolaridad,pmanual,obrasocial,consentimiento))
    else:
        for y in sujetos:
            if diccionarioEvaluaciones[x]['DatosPersonales']["DNI"] != y.DNI:
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
                sujetos.append(Sujeto(dni,nombre,apellido,edad,fechaNac,sexo,escolaridad,pmanual,obrasocial,consentimiento))
                break

evaluaciones = []
for x in diccionarioEvaluaciones:
    dni=diccionarioEvaluaciones[x]['DatosPersonales']["DNI"]
    splitfechaEv=diccionarioEvaluaciones[x]['DatosPersonales']["fecha_ev"].split("/")
    fechaEv=datetime.datetime(int("20"+splitfechaEv[2]),int(splitfechaEv[1]),int(splitfechaEv[0]))
    pruebas={}
    for y in diccionarioEvaluaciones[x]:
        pruebas.update({y:diccionarioEvaluaciones[x][y]})
    pruebas.pop('DatosPersonales')
    evaluaciones.append(Evaluacion(dni,fechaEv,pruebas))

informes = []
for x in diccionarioInformes:
    nombre=diccionarioInformes[x]["nombre"]
    dni=diccionarioInformes[x]["dni"]
    fechaEv= diccionarioInformes[x]["fechaEv"]
    antecedentes = diccionarioInformes[x]["antecedentes"]
    conclusion = diccionarioInformes[x]["conclusion"]
    informes.append(Informe(nombre,dni,fechaEv,antecedentes,conclusion))

for x in sujetos:
    for y in informes:
        if x.DNI == y.dni:
            x.informes.append(y)
    for z in evaluaciones:
        if x.DNI == z.dni:
            x.evaluaciones.append(z)

