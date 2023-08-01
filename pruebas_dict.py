def dicci():

    my_dict = {'a': 1, 'b': 2}
    for k, _ in my_dict.items(): #estalinea con underscore muestra las llaves del diccionario (buena practica)
        print(f"The keys are: {k}")
    
if __name__=='__main__':
    dicci()