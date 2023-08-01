class Humano:
    def __init__(self, edad):
       self.edad = edad
       print('edad:', edad)
       
    def hablar(self, mensaje):
        print(mensaje)

class IngSistemas(): # no hereda
    def __init__(self):
        print('hola')
        
    def programar(self, lenguaje):
        print('progamo en', lenguaje)
        
class LicDerecho(Humano): # hereda de la clase humano
    def estudiarCaso(self, derecho):
        print('Debo estudiar', derecho)
        
class estudioso(IngSistemas, LicDerecho):
    pass


pedro = IngSistemas() # accedo a la clase IngSistemas aca esta el metodo de inicio __init__ es lo primero que se ejecuta
raul = LicDerecho(24) # accedo a la clase LicDerecho lleva el atributo de la clase humano "edad"

pedro.programar('python') # accedo al metodo programar de la clase IngSistemas con el atributo "lenguaje" 
raul.estudiarCaso('pedro') # accedo al metodo estudiarCaso con el atributo "derecho"

pepe = estudioso() # accedo a la clase estudioso que tiene 2 atributos IngSistemas y LicDerecho