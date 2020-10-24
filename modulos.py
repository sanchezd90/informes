from datetime import datetime

class serializador():
    def extraer(self,listado):
        series=[]
        for x in listado:
            serie={"codigo":x.codigo,"edad":x.edad,"sexo":x.sexo,"escolaridad":x.escolaridad,"dominancia":x.dominancia,"derivador":x.derivador,"evaluador":x.evaluador}
            for key,value in x.pruebas.items():
                for k,v in value.items():
                    if v != "":
                        k=str(key)+"_"+k
                        serie[k]=v
            series.append(serie)
        return series
    def nombrar(self):
        now=datetime.now()
        timestamp = datetime.timestamp(now)
        t=str(timestamp).replace(".","")
        return t


