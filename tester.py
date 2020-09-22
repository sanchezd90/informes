

def prueba(x):
    def aux(y):
        z=y+1
        return z
    a=x+1
    return aux(a)

print(prueba(1))