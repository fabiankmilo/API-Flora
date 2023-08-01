def area_triangulo(base, altura):
    return (base * altura)/2
triangulo = area_triangulo(5,7)
print(triangulo)

# ejemplo

area_triangulo_lambda = lambda base, altura:(base*altura)/2 # se simplifica la funcion
print(area_triangulo_lambda(5,7))


#s = lambda n,m: n+m ## funcion lambda: funcion oculta para simplificar sintaxis diseñada para funciones sencillas
#print(s(4,7))

