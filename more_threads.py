from threading import Thread

def func_simple(length):
    sum_f1 = 0
    for x in range(0, length):
        sum_f1 += x
    print("Normal sum is {}".format(sum_f1))
    
def func_square(length):
    sum_f2 = 0
    for x in range(0, length):
        sum_f2 += x*x
    print("Square sum is {}".format(sum_f2))
    
def func_cubes(length):
    sum_f3 = 0
    for x in range(0, length):
        sum_f3 += x*x*x
    print("Cube sum is {}".format(sum_f3))
    
def do_threading():
    
    #length = int(input('escoje un #'))
    length = 4
    
    thread_simple = Thread(target=func_simple, args=(length,))
    thread_square = Thread(target=func_square, args=(length,))
    thread_cube = Thread(target=func_cubes, args=(length,))
    
    # start execution
    thread_simple.start()
    thread_square.start()
    thread_cube.start()
    
    # wait for the threads to finish
    thread_simple.join()
    thread_square.join()
    thread_cube.join()
    
do_threading()