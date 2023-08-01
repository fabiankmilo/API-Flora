def suma(n1, n2):
    return n1 + n2

def resta(n1, n2):
    return n1 - n2

def multiplica(n1, n2):
    return n1 * n2

def divide(n1, n2):
    
    try:
        return n1 / n2
    
    # ZeroDivisionError es un error por dividir entre cero, 
    # con la excepcion podemos continuar con el programa
    except ZeroDivisionError:
        print("No se puede dividir entre 0")
        return "Operacion erronea"

# este bulce se usa para pedir los numeros de la division
# si no son numericos hece el except de ValueError y se devuelve
# de nuevo al bucle hasta que los valores sean numericos
while True:
    
    try:
    
        op1 = (int(input("introduce el primer numero: ")))
        op2 = (int(input("introduce el segundo numero: ")))
        break

    except ValueError:
        
        print("Los valores no son numericos, intenta de nuevo !")
        
operacion = input("Introduce operacion a realizar (suma, resta, multiplica, divide): ")

if operacion == "suma":
    print(suma(op1, op2))

elif operacion == "resta":
    print(resta(op1, op2))

elif operacion == "multiplica":
    print(multiplica(op1, op2))

elif operacion == "divide":
    print(divide(op1, op2))
    
else:
    print("operacion invalida")