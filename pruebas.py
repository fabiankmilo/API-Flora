from datetime import datetime, date, time, timedelta
from time import sleep

now = datetime.now()
now_2 = date.today()
# print(now)

caudal_cuenta = 0
pulsos = 3
time_lapse = (now.second)


def resetTimer():
        # Reset Timer to 0
    caudal_cuenta = 0
    print(time_lapse)
    
def contador():
    
    global time_final
    global caudal_cuenta
    global time_lapse
    caudal_cuenta+=1
    
    return caudal_cuenta, time_lapse


for i in range(8):
    sleep(1)
    contador()
    time_final = time_lapse + 3    

#def operar():
    
    if caudal_cuenta == pulsos: #and time_lapse <= contador.time_lapse + time_final:
        print("Carga Datos")

    elif caudal_cuenta == time_lapse and time_lapse >= time_lapse + time_final:
        print("cargar cero")
    
    else:
        print("No pasa nada")


    
#operar()
print(caudal_cuenta)

print(time_lapse)
# time_final = time_lapse + 3
print(time_final)
resetTimer()


    


