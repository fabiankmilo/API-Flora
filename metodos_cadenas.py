# input siempre recibe caracteres
edad = input("introduce tu edad: ")

# isdigit se usa para confirmar (bool) digitos o numeros
while edad.isdigit() == False:
    print("ingrese datos numericos")
    edad = input("introduce tu edad")

# convertimos a entero
if(int(edad) >= 18):
    print("puedes pasar")
else:
    print("no puedes pasar")
    