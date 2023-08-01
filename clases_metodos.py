class Ejemplo:
    def __init__(self):
        self.n = 0  # Atributo de instancia

    def foo(self):
        self.n = 13

    #inst = Ejemplo()
        print(self.foo())

# class Ejemplo:
#     n = 0  # Atributo de clase
# 
#     @classmethod 
#     def foo(cls):
#         cls.n = 13
# 
# 
# 
inst = Ejemplo()  # Instancia 1
inst2 = Ejemplo() # Instancia 2
inst.foo()
print(inst2.n)