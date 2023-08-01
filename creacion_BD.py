import sqlite3

connection = sqlite3.connect("db_Prueba")
cursor = connection.cursor()

# con esta linea creamos la base de datos con la tabla PRODUCTOS
# e insterta 3 campos de la tabla
#cursor.execute("CREATE TABLE PRODUCTOS('NOMBRE VARCHAR(30)', 'PRECIO INTEGER', 'SECCION VARCHAR(20)')")

# con esta linea insertamos valores
#cursor.execute("INSERT INTO PRODUCTOS VALUES('BALON', 15, 'DEPORTES')")

# podemos insertar listas y tuplas en la BD
# asi es mas facil insertar datos en la BD

#productos = [
#    ("Camiseta", 10, "Deportes"),
#    ("Balon", 18, "Deportes"),
#    ("Carrito", 20, "Jugueteria")
#]

# se ponen tantos interrogantes como campos de la tabla en la BD

#cursor.executemany("INSERT INTO PRODUCTOS VALUES(?,?,?)", productos)

cursor.execute("SELECT * FROM PRODUCTOS")

# fetchall() muestra los datos en tuplas o listas de la BD
productos = cursor.fetchall()

# con un for podemos recorrer los datos y verlos ordenados en tuplas

for p in productos:

# podemos trabajar las tuplas con indices
    print(p[0])


connection.commit()
connection.close()


