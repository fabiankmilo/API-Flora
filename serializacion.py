# seriaizacion: guarda un archivo o fichero externo codificado en binario
# puede ser un diccionario, un objeto, o una coleccion de datos. 
# Esto sirve para trasportar o distribuir datos codificados o guardarlos
# en una base de datos
import pickle

# este codigo serializa en binario la lista creando un fichero
# externo

lista = ["Pedro", "Ana", "Maria", "Salome", "Fabian", "Camilo"]
fichero_bin = open("lista", "wb") # wb write binary
pickle.dump(lista, fichero_bin)
fichero_bin.close
del(fichero_bin)

# este codigo decodifica el fichero en binario y nos muestra
# la lista decodificada

#fichero = open("lista", "rb") # rb read binary
#lista = pickle.load(fichero)
#print(lista)
