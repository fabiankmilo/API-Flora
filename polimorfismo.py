class Coche():
    
    def desplazamiento(self):
        print("Me desplazo en cuatro ruedas")
        
class Moto():
    
    def desplazamiento(self):
        print("Me desplazo en dos ruedas")

class Camion():
    
    def desplazamiento(self):
        print("Me desplazo en seis ruedas")
        
        
# creamos un metodo que recibe vehiculo por parametro
# y utiliza el parametro para llamar a desplazamiento
def desplazamientoVehiculo(vehiculo):
    
    vehiculo.desplazamiento()

# el obejeto vehiculo tiene la capacidad de cambiar
# gracias al polimorfismo en python ejm:


# en este caso el polimorfismo consite en adaptar la clase
# a la clase moto
miVehiculo = Moto() 
desplazamientoVehiculo(miVehiculo)