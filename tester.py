pruebasAdministradas=[1,2,3,4,5,6,7,8]
pruebas_req=[]

if (all(elem in pruebasAdministradas for elem in pruebas_req)):
    print("Ok")
else:
    print("Not ok")