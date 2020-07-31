import os
import docx

diccionarioInformes = {}

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
            dni = x.lstrip("DNI: ")
        if "Fecha de Evaluación: " in x:
            fechaEv = x.lstrip("Fecha de Evaluación: ")
        if "Antecedentes" in x:
            antecedentes= fullText[i+1]
        if "En la presente evaluación" in x:
            inicioConclusion = i
        if "En el caso de existir" in x:
            finConclusion = i
    for x in range(inicioConclusion,finConclusion):
        conclusion += fullText[x]
    split = fechaEv.split("/")
    fechaInv = split[2][-2]+split[2][-1]+"-"+split[1]+"-"+split[0]
    codigo = dni+"-"+fechaInv
    diccionarioInformes[codigo]={"nombre":nombre,"dni":dni,"fechaEv":fechaEv,"antecedentes":antecedentes,"conclusion":conclusion}

#loop para revisar archivos csv y agregar datos a datos_informes
for archivo in os.listdir('.'):
    if archivo.endswith(".docx"):
        getText(archivo)
