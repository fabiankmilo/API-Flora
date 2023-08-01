class Coche():
    
    # constructor (se usa para dar un estado
    # inicial a los objetos de esta clase
    def __init__(self):
    
        # cuatro propiedades
        self.__largoChasis = 250
        self.__anchoChasis = 120
        # (2 guiones bajos) variable encapsulada, se encapsula para protejerla
        # de cambios que puedan suceder y no sean necesarios a lo largo del
        # programa en la variable
        self.__ruedas = 4
        self.__enmarcha = False
        
    def arrancar(self, start):
        # en este caso def pertenece al metodo de la clase
        # self hace referencia al objeto de la clase 
        self.enmarcha = start
        
        if(self.enmarcha):
            return "coche en marcha"
        else:
            return "coche parado"
    
    def estado(self):
        # concatenamos el print
        print("coche con:", self.__ruedas, "ruedas",
              "un ancho de:", self.__anchoChasis,
              "un largo de:", self.__largoChasis)
        
    def chequeo(self):
        
        print("realizando chequeo interno")
        self.gasolina = "ok"
        self.aceite = "ok"
        self.puertas = "cerradas"
        
        if(self.gasolina == "ok" and self.aceite == "ok" and self.puertas == "cerradas"):
            
            return True
        else:
            return False
# instancia de la clase
miCoche = Coche()
print(miCoche.arrancar(True))
print(miCoche.estado())

print("========== Segundo Objeto ==========")

# segunda instancia para el coche 2
miCoche2 = Coche()
print(miCoche.arrancar(False))
print(miCoche2.estado())

