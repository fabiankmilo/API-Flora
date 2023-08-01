def run():
##    my_dict ={}
##    
##    for i in range(1, 101):
##        if i % 3 != 0:
##            my_dict[i] = i**3
##    print(my_dict)
    
    ## keys: todos los numeros menos la susecion de 3 en 3 (3-6-9-12-15)
    ## sucesion numerica: numeros elevados al cubo
    ## i: i**3 representa las llaves y valores a poner en el diccionario
    ## for i in range (1, 101) representa el ciclo a patir del cual se extraen los elementos iterables
    ## if condicion opcional para filtrar los elementos del ciclo
    
    my_dict = {i: i**3 for i in range(1, 20) if i % 2 !=0}
    print(my_dict)
    #print(my_dict.keys()) # muestra llaves
    #print(my_dict.values()) # muestra valores
    #print(my_dict.get(1)) # obtiene un valor dependiendo la llave
    #print(my_dict.pop(1)) # recibe como parámetro una clave, elimina esta y devuelve su valor. Si no lo encuentra, devuelve error.
    
    
if __name__=='__main__':
    run()