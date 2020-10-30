import os
import csv
import json
import docx
import datetime

class Lector():
    def leer_informes(self):
        with open("informes.json","r") as f:
            diccionarioInformes = json.load(f)
        def getText(filename):
            doc = docx.Document(filename)
            fullText = []
            nombre=""
            dni =""
            fechaEv = ""
            antecedentes=""
            inicioConclusion = ""
            finConclusion = ""
            conclusion = ""
            for para in doc.paragraphs:
                fullText.append(para.text)
            for i,x in enumerate(fullText):
                if "Nombre" in x:
                    nombre = x.lstrip("Nombre: ")
                if "DNI" in x:
                    dni = x.lstrip("DNI: ").replace(".","").replace(",","")
                if "Fecha de Evaluación: " in x:
                    fechaEv = x.lstrip("Fecha de Evaluación: ")
                    if "y" in fechaEv:
                        fechaEv=fechaEv.partition("y")[0].strip()
                if "Antecedentes" in x:
                    antecedentes= fullText[i+1]
                if "realizó sus estudios" in x:
                    antecedentes += "\n"+x
                if "antecedentes médicos" in x:
                    antecedentes += "\n"+x
                if "En la presente evaluación" in x:
                    inicioConclusion = i
                if "En el caso de existir" in x:
                    finConclusion = i
            for x in range(inicioConclusion,finConclusion):
                conclusion += fullText[x]
            split = fechaEv.split("/")
            year=split[2]
            month=split[1]
            day=split[0]
            if len(month)==1:
                month="0"+month
            if len(day)==1:
                day="0"+day
            fechaInv = split[2][-2]+split[2][-1]+"-"+month+"-"+day
            date=(year,month,day)
            codigo = dni+"-"+fechaInv
            if codigo not in diccionarioInformes:
                diccionarioInformes[codigo]={"nombre":nombre,"dni":dni,"fechaEv":date,"antecedentes":antecedentes,"conclusion":conclusion}

        #loop para revisar archivos docs y agregar datos a datos_informes
        for archivo in os.listdir('informesdocx/'):
            if archivo.endswith(".docx"):
                archivo=os.path.join("./informesdocx/",archivo)
                getText(archivo)
                os.remove(archivo)

        with open("informes.json","w") as f:
            json.dump(diccionarioInformes,f,indent=4)

    def leer_evaluaciones(self):
        datos_evaluaciones = [] #los datos de todos las evaluaciones revisados

        with open("evaluaciones.json","r") as f:
            diccionarioEvaluaciones = json.load(f) #diccionario con datos de todos los informes almacenados en JSON

        #loop para revisar archivos csv y agregar datos a datos_evaluaciones
        for archivo in os.listdir('evaluacionescsv/'):
            if archivo.endswith(".csv"):
                archivo=os.path.join("./evaluacionescsv/",archivo)
                with open(file=archivo, mode="r", encoding="utf-8-sig") as csvfile:
                    csvReader = csv.reader(csvfile, delimiter=';')
                    datos_evaluacion = list(csvReader)
                    datos_evaluaciones.append(datos_evaluacion)

        #loop para armar diccionarios con la información de cada informe. La info va a diccionarioInformes
        for informe in datos_evaluaciones:
            # informe[1][11] es la casilla en la que está la fecha de evaluacion
            split=informe[1][11].split("/")
            for i,s in enumerate(split):
                if len(s)<2:
                    split[i]="0"+split[i]
            if len(split[1])==1:
                split[1]="0"+split[1]
            if len(split[0])==1:
                split[0]="0"+split[0]
            fecha=split[2]+"-"+split[1]+"-"+split[0]
            dni=informe[1][12].replace(".","").replace(",","")
            codigo = dni+"-"+fecha
            if codigo not in diccionarioEvaluaciones:
                diccionarioEvaluaciones[codigo]={}
                #inicio un loop para explorar las celdas. comienzo explorando las filas 
                for x in range(len(informe)):
                    #me fijo si la primera celda esta completa, así puedo saber que es fila de etiquetas
                    if len(informe[x][0]) > 0:
                        #armo el key del diccionario que va a llevar el nombre de la fila
                        key = informe[x][0]
                        #agrego al diccionario una key por prueba con el valor vacio
                        diccionarioEvaluaciones[codigo][key]={}
                        #inicio un loop para enumerar los datos de la fila de abajo de la fila que tiene las etiquetas
                        for index,item in enumerate(informe[x+1]):
                            #exploro si cada celda tiene un valor
                            if index >0:
                                #si la celda tiene valor actualizo el diccionario con la etiqueta como key y el valor como value
                                k=informe[x][index]
                                diccionarioEvaluaciones[codigo][key][k]=item

        with open("evaluaciones.json","w") as f:
            json.dump(diccionarioEvaluaciones,f,indent=4)


#para crear instancia y leer datos de ambos json

lector=Lector()
#lector.leer_evaluaciones()
lector.leer_informes()

