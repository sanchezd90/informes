import lector

diccionarioInformes = lector.diccionarioInformes

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


sujetos = [] #lista con las instancias de Sujeto de cada sujeto
for x in diccionarioInformes:
    dni=diccionarioInformes[x]['\ufeffDatosPersonales']["DNI"]
    nombre=diccionarioInformes[x]['\ufeffDatosPersonales']["nombre"]
    apellido=diccionarioInformes[x]['\ufeffDatosPersonales']["apellido"]
    edad=diccionarioInformes[x]['\ufeffDatosPersonales']["edad_eval"]
    fechaNac=diccionarioInformes[x]['\ufeffDatosPersonales']["fecha_nac"]
    sexo=diccionarioInformes[x]['\ufeffDatosPersonales']["sexo"]
    escolaridad=diccionarioInformes[x]['\ufeffDatosPersonales']["años_esc"]
    pmanual=diccionarioInformes[x]['\ufeffDatosPersonales']["pref_manual"]
    obrasocial=diccionarioInformes[x]['\ufeffDatosPersonales']["obra_social"]
    consentimiento=diccionarioInformes[x]['\ufeffDatosPersonales']["consent"]
    sujetos.append(Sujeto(dni,nombre,apellido,edad,fechaNac,sexo,escolaridad,pmanual,obrasocial,consentimiento))

evaluaciones = []
for x in diccionarioInformes:
    dni=diccionarioInformes[x]['\ufeffDatosPersonales']["DNI"]
    fechaEv=diccionarioInformes[x]['\ufeffDatosPersonales']["fecha_ev"]
    pruebas={}
    for y in diccionarioInformes[x]:
        pruebas.update({y:diccionarioInformes[x][y]})
    pruebas.pop('\ufeffDatosPersonales')
    evaluaciones.append(Evaluacion(dni,fechaEv,pruebas))