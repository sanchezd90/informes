import os
import csv
import json
import docx
import datetime

class Serializer():
    def __init__(self):
        self.keysInvalidosMongo=["Relatos","RAVLT","Relatos (WMS IV)","RAVLT (Tambor50)","RAVLT (Pasto50)","RAVLT (Tambor60)"]
    def getText(self,filename):
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
        return {"nombre":nombre,"dni":dni,"fechaEv":date,"antecedentes":antecedentes,"conclusion":conclusion, "codigo":codigo}

    def write_json_informe(self,diccionario):
        x=diccionario["codigo"]
        name=x+".json"
        path="./informesjson/"
        file_path=os.path.join(path,name)
        with open(file_path,"w") as f:
            json.dump(diccionario,f,indent=4)

    def serialize_docx(self):
        #loop para revisar archivos docs y agregar datos a datos_informes
        for archivo in os.listdir('informesdocx/'):
            try:
                if archivo.endswith(".docx"):
                    archivo=os.path.join("./informesdocx/",archivo)
                    self.write_json_informe(self.getText(archivo))
                    os.remove(archivo)
            except Exception:
                pass

    def write_json_evaluacion(self,diccionario):
        x=diccionario["codigo"]
        name=x+".json"
        path="./evaluacionesjson/"
        file_path=os.path.join(path,name)
        with open(file_path,"w") as f:
            json.dump(diccionario,f,indent=4)

    def get_data(self,archivo):
        archivo=os.path.join("./evaluacionescsv/",archivo)
        with open(file=archivo, mode="r", encoding="utf-8") as csvfile:
            csvReader = csv.reader(csvfile, delimiter=';')
            return list(csvReader)

    def serialize_csv(self):
        #loop para revisar archivos csv y agregar datos a datos_evaluaciones
        for archivo in os.listdir('evaluacionescsv/'):
            if archivo.endswith(".csv"):   
                try:
                    datos_evaluacion = self.get_data(archivo)
                    # informe[1][11] es la casilla en la que está la fecha de evaluacion
                    split=datos_evaluacion[1][11].split("/")
                    for i,s in enumerate(split):
                        if len(s)<2:
                            split[i]="0"+split[i]
                    if len(split[1])==1:
                        split[1]="0"+split[1]
                    if len(split[0])==1:
                        split[0]="0"+split[0]
                    fecha=split[2]+"-"+split[1]+"-"+split[0]
                    dni=datos_evaluacion[1][12].replace(".","").replace(",","")
                    codigo = dni+"-"+fecha
                    diccionarioEvaluacion={"codigo":codigo}
                    #inicio un loop para explorar las celdas. comienzo explorando las filas 
                    for x in range(len(datos_evaluacion)):
                        #me fijo si la primera celda esta completa, así puedo saber que es fila de etiquetas
                        if len(datos_evaluacion[x][0]) > 0:
                            #armo el key del diccionario que va a llevar el nombre de la fila
                            key = datos_evaluacion[x][0].replace('.','_')
                            #agrego al diccionario una key por prueba con el valor vacio
                            diccionarioEvaluacion[key]={}
                            #inicio un loop para enumerar los datos de la fila de abajo de la fila que tiene las etiquetas
                            for index,item in enumerate(datos_evaluacion[x+1]):
                                #exploro si cada celda tiene un valor
                                if index >0:
                                    #si la celda tiene valor actualizo el diccionario con la etiqueta como key y el valor como value
                                    k=datos_evaluacion[x][index].replace('.','_')
                                    diccionarioEvaluacion[key][k]=item
                    
                    self.write_json_evaluacion(diccionarioEvaluacion)
                    archivo=os.path.join("./evaluacionescsv/",archivo)
                    os.remove(archivo)    
                except Exception:
                    pass



#para crear instancia y leer datos de ambos json

serializer=Serializer()
serializer.serialize_docx()
serializer.serialize_csv()

