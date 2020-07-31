import lectorEvaluaciones
import lectorInformes

diccionarioEvaluaciones = lectorEvaluaciones.diccionarioEvaluaciones
diccionarioInformes = lectorInformes.diccionarioInformes

class Sujeto(object):
    def __init__(self,dni,nombre,apellido,edad,fechaNac,sexo,escolaridad,pmanual,obrasocial,consentimiento):
        self.DNI=dni
        self.nombre=nombre
        self.apellido=apellido
        edad = edad.split(",")
        self.edad = edad[0]
        self.fechaNac=fechaNac
        self.sexo=sexo
        self.escolaridad=escolaridad
        self.pmanual=pmanual

class Evaluacion():
    def __init__(self,dni,fechaEv,pruebas):
        self.fechaSplit=fechaEv.split("/")
        self.dni = dni
        self.fechaEv=self.fechaSplit[2]+"-"+self.fechaSplit[1]+"-"+self.fechaSplit[0]
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
        fechaNac=diccionarioEvaluaciones[x]['DatosPersonales']["fecha_nac"]
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
                fechaNac=diccionarioEvaluaciones[x]['DatosPersonales']["fecha_nac"]
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
    fechaEv=diccionarioEvaluaciones[x]['DatosPersonales']["fecha_ev"]
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

print(informes[0].dni)