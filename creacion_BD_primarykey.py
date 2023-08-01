import sqlite3


connection = sqlite3.connect("GestionProductos") # nombre de la DB
cursor = connection.cursor()

# la triple comilla se usa para las instrucciones muy largas
# se pueden dividir en varias secciones
# el campo clave en la base de datos sera el ID primary key

# con el parametro AUTOINCREMENT el campo clave se crea automatico
# y se va incrementando

# con UNIQUE hacemos que los campos no se repitan
cursor.execute('''
    CREATE TABLE PRODUCTOS(
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    NOMBRE_ARTICULO VARCHAR UNIQUE(50),
    PRECIO INTEGER,
    SECCION VARCHAR(20))
''')

# se crea la lista con la info que se va almacenar en la DB
#productos = [
    
    # cuando usamos PARIMARY KEY en la DB, el ID no se puede repetir
#    ("Pelota", 20, "Jugueteria"),
#    ("Pantalon", 20, "Confeccion"),
#    ("Taladro", 20, "Ferreteria"),
#    ("Jarron", 20, "Ceramica")
    
#    ]

# el campo ID por ser primarykey para insertar info en la BD
# no debe ir interrogante (?) debe ir la palabra null

# CRUD !!! CREATE, READ, UPDATE, DELETE
 
# ojo con DELETE pq puede borrar toda la DB hay que usar la calusula
# where para corrar algun registro en la DB

cursor.execute("UPDATE PRODUCTOS SET PRECIO=20 WHERE NOMBRE_ARTICULO = 'Pelota'")

cursor.execute("DELETE FROM PRODUCTOS WHERE ID=3")

cursor.executemany("INSERT INTO PRODUCTOS VALUES(null,?,?,?)", productos)

connection.commit()
connection.close()



