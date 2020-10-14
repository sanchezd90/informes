
info=["ao","ab","bc","bd"]

class Cadena():
    def __init__(self,texto):
        self.cadena=texto+"c"

class Waka():
    def __init__(self,info):
        self.a=[]
        self.b=[]
    def crear_a(self):
        for x in info:
            if x.startswith("a"):
                self.a.append(Cadena(x))
    def crear_b(self):
        for x in info:
            if x.startswith("b"):
                self.b.append(Cadena(x))
    def activar(self):
        self.crear_a()
        self.crear_b()
        return (self.a,self.b)

w1=Waka(info)
print(w1.activar())


            
            
