logg = True
usuario = " Fabiancho"

def decorador(funcion):
    
    def funcionDecorada(*args,**kwargs): # *args recibe n cantidad de parametros **kwargs diccionario que incluye los valores de los parametros n
        print("Funcion ejecutada", funcion.__name__)
        funcion(*args,**kwargs)
    return funcionDecorada

# ejemplo decorador control de acceso asi funciona django

def admin(f):
    def comprobar(*args,**kwargs):
        if logg: # depende si la variable bool (logg) es True o False
            f(*args,**kwargs)
            print("Funcion ejecutada", f.__name__)
        else:
            print("No tiene permisos para ejecutar", f.__name__) # f.__name__ llama el nombre de la funcion en este caso resta
    return comprobar

#@decorador
@admin
def resta(n,m):
    print("la resta es igual a:", n-m)
    
resta(40,3)

        
        