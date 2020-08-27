class Redaccion():
    def encadenar(self,items=[]):
        if len(items) == 0:
            return None
        elif len(items) == 1:
            return items[0]
        elif len(items) == 2:
            return f"""{items[0]} y {items[1]}"""
        else:
            cadena=""
            i=0
            while i < len(items)-2:
                cadena += items[i]+", "
                i += 1
            cadena += items[-2]+" y "+items[-1]
            return cadena
    def set_genero(self,texto,sexo="masculino"):
        self.sexo = sexo.lower()
        self.texto = texto
        variables = [("El paciente"," La paciente"),(" el paciente"," la paciente"),(" al paciente"," a la paciente"),(" del paciente"," de la paciente"),("El Sr.","La Sra."),(" el Sr."," la Sra."),(" del Sr."," de la Sra."),("@","a")]
        for x in variables:
            if self.sexo=="femenino":
                self.texto = self.texto.replace(x[0],x[1])
            elif "$" in self.texto:
                self.texto = self.texto.replace("@","o")
        return self.texto

redaccion1=Redaccion()
print(redaccion1.encadenar(["a","b","c"]))
print(redaccion1.set_genero("El paciente viene. Dice que se siente cómod@. Luego el Sr. Ariel come. La camisa del paciente. Se le pregunta al paciente el nombre del Sr. Emi","femenino"))


