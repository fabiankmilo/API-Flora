# recordar que en las Clases la funciones def se convierten en métodos

class Vehiculos():
    
    # constructor (se usa para dar un estado
    # inicial a los objetos de esta clase
    def __init__(self, marca, modelo):
    
        # cuatro propiedades
        self.marca = marca
        self.modelo = modelo
        self.enmarcha = False
        self.acelera = False
        self.frena = False
    
    def arrancar(self):
        self.enmarcha = True
    
    def acelerar(self):
        self.acelera = True
        
    def frenar(self):
        self.frena = True
    
    def estado(self):
        print("Marca: ", self.marca, "\n",
              "Modelo: ", self.modelo, "\n",
              "En Marcha: ", self.enmarcha, "\n",
              "Acelerando: ", self.acelera, "\n",
              "Frenando: ", self.frena, "\n")

#clase Moto hereda de la clase Vehiculo
class Moto(Vehiculos):
    
    hcaballito = ""
    
    # trae los atributos de la clase vehiculo mas el atributo hcaballito
    def caballito(self):
        
        self.hcaballito = "Voy haciendo cross en una rueda"
        
    def estado(self): # este metodo estado es el mismo de la clase Vehiculos pero incluye el hcaballito
                      # se conoce como sobre escritura de metodos
        print("Marca: ", self.marca, "\n",
              "Modelo: ", self.modelo, "\n",
              "En Marcha: ", self.enmarcha, "\n",
              "Acelerando: ", self.acelera, "\n",
              "Frenando: ", self.frena, "\n",
               self.hcaballito)

class Furgoneta(Vehiculos):
    
    def carga(self, cargar):
        
        self.cargado = cargar
        if(self.cargado):
            return "Furgoneta cargada"
        else:
            return "Furgoneta vacía"
        
class VElectricos(Vehiculos):
    
    def __init__(self, marca, modelo):
        
        super().__init__(marca, modelo)
        
        self.autonomia = 100
        
    def cargarEnergia(self):
        
        self.cargando = True

class BiciElectrica(VElectricos, Vehiculos):
    pass

# instancias

miMoto = Moto("Honda", "CBR")
miMoto.caballito() # esta instancia llama el metodo caballito
miMoto.estado()

# en constructor hereda de la clase Vehiculos def __init__(self, marca, modelo)
# por lo tanto recibe 2 parametros marca y modelo
miFurgoneta = Furgoneta("Renault", "Kangoo" )
miFurgoneta.arrancar()
miFurgoneta.estado()
print(miFurgoneta.carga(True))

miBici = BiciElectrica("GW", "Piranha")
