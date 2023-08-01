#def hola():
#    print ("Hola")

def decor(func):
    def wrapper(): # esta es la funcion a ser decorada
        print("Aviso: voy a decir algo")
        func()
        print("Ya he dicho algo")
    return wrapper

#hola = decor(hola)
#hola()

@decor
def hola():
    print ("Hola")
    
hola()