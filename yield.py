# yield es una orden muy similar a un return, con una gran diferencia,
# yield pausará la ejecución de tu función y guardará el estado de la
# misma hasta que decidas usarla de nuevo. Ejm:
# Yield es la declaración que se utiliza para crear generadores


def squares(numbers):
  for number in numbers:
    yield number*number

#squares([1,2,3,4,5])

#for square in squares([1,2,3]):
    #print(square)
    
    
# def numeros_naturales(): # este ejemplo genera todos los numeros naturales
#     n = 1
#     while True:
#         yield n
#         n += 1
# 
# for natural in numeros_naturales():
#     print(natural)
    

def numeros_naturales(): # este ejemplo genera numeros naturales en un rango
    n = 1
    for i in range(1,7):
        #print(i)
        yield n
        n += 1
    print("FIN")
for natural in numeros_naturales():
    print(natural)
    