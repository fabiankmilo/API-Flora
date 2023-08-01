def divide():
    
    try:
        op1 = (float(input("introduce el primer numero: ")))
        op2 = (float(input("introduce el segundo numero: ")))
        
        # formatea la division con 2 decimales
        print("La division es: " + "{0:.2f}".format(op1/op2))
    
    except ValueError:
        print("Valor erroneo")
    except ZeroDivisionError:
        print("No se puede dividir entre 0")
    finally:
        print("fin")
divide()