import pickle

# serializers
# con estas lineas de codigo creamos y guardamos en un fichero permanente tipo binario 
# una lista de personas con los atributos nombre, genero y edad creado un archivo externo
# y mostrando la informacion leyendo el archivo externo
class Persona:
    
    def __init__(self, nombre, genero, edad):
        self.nombre = nombre
        self.genero = genero
        self.edad = edad
        print("Se ha creado una persona con el nombre: ", nombre)

# metodo para __str__ se usa para convertir en cadena de texto la info de un objeto
# aplicando el formato {} nos devuelve los 3 datos, nombre,genero, edad
    def __str__(self):
        return "{} {} {}".format(self.nombre, self.genero, self.edad)
    
class ListaPersonas:
    
    personas = [] # en esta lista se almacena las personas que se van creando
    
    def __init__(self):
        
        # agregamos la lista al fichero externo con ab+ (append binary)
        lista_de_personas = open("ficheroExterno", "ab+")
        # seek desplaza el cursor en el archivo externo ala posicion 0
        lista_de_personas.seek(0)
        
        try:
            # con pickle creamos el archivo externo
            self.personas = pickle.load(lista_de_personas)
            # este print imprime el numero de personas en la lista usando len
            print("Se han cargado {} personas".format(len(self.personas)))
        except:
            print("Fichero vacio")
            
        finally:
            lista_de_personas.close()
           # del(lista_de_peronas)
        
    def agregar(self, p):
        # agrega persona
        self.personas.append(p)
        self.guardar_en_fichero()
        
    def mostrar(self):
        for p in self.personas:
            print(p)
        
    def guardar_en_fichero(self):
        # abrimos en modo escritura
        lista_de_personas = open("ficheroExterno", "wb")
        # volcamos la informacion en el archivo externo
        pickle.dump(self.personas, lista_de_personas)
        lista_de_personas.close()
        del(lista_de_personas)
        
    def mostrar_en_fichero(self):
        print("La info del fichero externo es: ")
        for p in persona:
            print(p)
            
# intancias
lista = ListaPersonas()
persona = Persona("Andres","M","38")
lista.agregar(persona)
lista.mostrar()
