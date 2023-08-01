txt = " Hello World "
x = txt.strip()
x1 = txt.upper()
x2 = txt.replace('H','J')
print(x1)
print(x2)

age = 36
txt = "My name is John, and I am {}" # to add a placeholder for the age parameter txr.format {}
print(txt.format(age))

#fruits = ["apple", "banana", "cherry"] # listas
#fruits = ("apple", "banana", "cherry") # tuplas
#print(fruits[0])

fruits = {"apple", "banana", "cherry"} # sets
more_fruits = ["orange", "mango", "grapes"]
fruits.update(more_fruits)
print(fruits)
