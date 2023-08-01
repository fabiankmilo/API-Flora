
# usar yield con next nos permite iterar sobre cada valor de la variable o de una lista uno por uno
# este entra en estado de suspension entre las llamadas

def generaPares(limite):
    num = 1
    lista = []
    
    while num < limite:
        yield num * 2
        num = num + 1

devuelve_pares = generaPares(10)

# con este for devuelve todos los valores
#for i in devuelve_pares:
#    print(i)
    
print(next(devuelve_pares))
print("primer valor que devuelve")
print(next(devuelve_pares))
print("segundo valor que devuelve")

