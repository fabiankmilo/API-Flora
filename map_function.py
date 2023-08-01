numbers = [1,2,3,4,5,6,7,8,9,10]
sums = map(lambda x: 'Sum of x+5 is: ' + str(x+5), numbers)
# This prints something similar to: <map object at 0x10ed93cc0>
print(sums)
# Recall, that map returns an iterator 
# We can print all names in a for loop
for sum in sums:
    print(sum)