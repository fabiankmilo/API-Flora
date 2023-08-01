contador = 0

ingresa_email = input("ingresa email: ")

#email = False

# este for recorre todo el string ingresado en el input
for i in ingresa_email:
    if (i == "@" or i == "."): # confirma si el email tiene una @ y un punto
        contador = contador + 1
# no es necesario poner email == True en ya que python reconoce que el booleano email es True 
#if email == True:
if contador == 2:
    print("es correcto")
else:
    print("no es correcto")