from datetime import datetime

class serializador():
    def extraer(self,listado):
        series=[]
        for x in listado:
            serie=[x.codigo,x.edad,x.sexo,x.escolaridad,x.dominancia,x.derivador,x.evaluador,x.dxs]
            for k,v in x.pruebas.items():
                serie.append({k:v})
            series.append(serie)
        return series
    def nombrar(self):
        now=datetime.now()
        timestamp = datetime.timestamp(now)
        t=str(timestamp).replace(".","")
        return t


