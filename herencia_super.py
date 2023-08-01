class Persona():
    
    def __init__(self, nombre, edad, residencia):
        
        self.nombre = nombre
        self.edad = edad
        self.residencia = residencia
        
    def descripcion(self):
        
        print("Nombre:", self.nombre,
              "Edad:", self.edad,
              "Residencia:", self.residencia)
 
# ereda los atributos o propiedades de la clase Persona 
class Empleado(Persona):
        
    def __init__(self, salario, antiguedad, nombre_empleado, edad_empleado, residencia_empleado):
        
        # instruccion super llama al metodo de la clase padre en este caso
        # al metodo __init__ de la clase Persona, lo ejecuta pasandole los parametros
        super().__init__(nombre_empleado, edad_empleado, residencia_empleado)
            
        self.salario = salario
        self.antiguedad = antiguedad
    
    def descripcion(self):
        
        super().descripcion()
        print("Salario:", self.salario, "Antiguedad:", self.antiguedad)
        
# instancia

Antonio = Empleado(1500, 10, "Antonio", 55, "Colombia")
Antonio.descripcion()

# isinstance es una funcion de comprobacion para saber si un objeto pertenece
# a alguna clase especifica ejm:
# en este caso verifica si el objeto Antonio pertenece a la clase Empleado
# devuelve True o False

print(isinstance(Antonio, Empleado))