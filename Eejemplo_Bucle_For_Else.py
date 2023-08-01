email = input("introduce email: ")

for i in email:
    
    if i == "@":
    
        arroba = True
        break
# else en este caso, funciona cuando el bucle for se haya completado
else:
    
    arroba = False

print(arroba)