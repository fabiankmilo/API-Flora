#for letter in 'banana':
#    print(letter)

# funcion para encontrar con que palabra o letra comienza, salida True or False
line = 'Please have nice day'
line.startswith('Please')
line.startswith('P')

#for l in line:
#    print(l)

#x = '40'
#y = int(x) + 2
#print(y)

#x = 'From marquard@uct.ac.za'
#print(x[8])

#print(len('banana')*7)

data = 'From stephen.marquard@uct.ac.za Sat Jan  5 09:14:16 2008'
pos = data.find('.')
print(data[pos:pos+3])