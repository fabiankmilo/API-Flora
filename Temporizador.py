from datetime import datetime, date, time, timedelta
#from time import sleep
import time

now = datetime.now()
time_lapse = (now.second)

#global seconds

def timer():
    global seconds
    seconds = 0    
    
    while seconds != 180:
        # Sleep for a minute
        time.sleep(1)
        # Increment the minute total
        seconds += 1
        print(seconds)
        counter()

    return seconds

def counter():
    
    if seconds <= 5:
        print ("Hecho")
        
    else:
        print("Reset")
        reset()

def reset():
    global seconds
    seconds = 0

timer()
