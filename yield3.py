# el * en el parametro de la funcion se usa para indicar que
# ciudades tendrá n argumentos

def dev_ciudades(*ciudades):
    for elemento in ciudades:
        yield from elemento
        
# yield from devuelve los sub-elementos de la tupla
        
ciudades_devueltas = dev_ciudades("Madrid", "Barcelona", "Paris", "Lisboa")

# en este caso devuelve Mad las 3 primeras letras de Madrid
# ya que usamos el next 3 veces

print(next(ciudades_devueltas))
print(next(ciudades_devueltas))
print(next(ciudades_devueltas))
