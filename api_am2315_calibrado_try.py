#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import board
import busio
import adafruit_am2320
import json
import datetime
import requests

def am():

    timeProm = 10 #Tiempo en segundos que el sensor toma datos para promediar
    timeData = 1 #Frecuencia en segundos de toma de datos
    hora_inicial = time.time() + timeProm #Inicializar hora de referencia con desfase de timeProm segundos a comparar con hora actual
    tempSum = 0 #Inicializar suma de temperatura a promediar
    humSum = 0 #Inicializar suma de humedad a promediar
    Sum = 0 #Inicializar contador de datos tomados para promedio

    while True:

        fecha = time.strftime("%Y/%m/%d")
        hora = time.strftime("%H:%M:%S")
        url = 'http://10.99.0.41:4343/api/Sensores'

        while hora_inicial - time.time() > 0: #Mientras la hora inicial de referencia sea mayor a la hora actual

            i2c = busio.I2C(board.SCL, board.SDA)
            am = adafruit_am2320.AM2320(i2c)
            temp = float(am.temperature)
            hum = float(am.relative_humidity)

            if temp is not None and hum is not None:
                tempSum += temp #Sumar temperaturas
                humSum += hum #Sumar humedades
                Sum = Sum + 1 #Incrementar contador
                print(temp, hum)

            else:
                print('Failed to get reading. Try again!')


            time.sleep(timeData) #Pausa aprox. de frecuencia de toma de datos

        hora_inicial = time.time() + timeProm #Reiniciar la hora inicial de referencia
        tempProm = tempSum/Sum #Promedio temperatura
        humProm = humSum/Sum #Promedio humedad
        
        if humProm > 90 and humProm < 92:

            humProm = humProm - 1
            
            print("{0:.2f}".format(tempProm))
            print("{0:.2f}".format(humProm))

        elif humProm > 92 and humProm < 95:

            humProm = humProm - 2.5

            print("{0:.2f}".format(tempProm))
            print("{0:.2f}".format(humProm))

        elif humProm > 95 and humProm < 100:

            humProm = humProm - 3
            
            print("{0:.2f}".format(tempProm))
            print("{0:.2f}".format(humProm))
            
        else:
            
            humProm = humSum/Sum #Promedio humedad

            print("{0:.2f}".format(tempProm))
            print("{0:.2f}".format(humProm))
            
        tempProm1 = "{0:.1f}".format(tempProm)
        humProm1 = "{0:.1f}".format(humProm)
        

        tempSum = 0 #Reiniciar sumas de temperatura, humedad, y contador de toma de datos
        humSum = 0
        Sum = 0
            
        if tempProm <= 100 and humProm <= 100:
            
            try:

                postdata = {"DeviceId":231371,"Value":"TEMP","Data":tempProm1,"BusinessUnitId":486,"GreenHouseID":1137,"Time":fecha + " " + hora,"Sensor":"AM2315"}
                print(postdata)

                headers = {'content-type':'application/json'}
                response = requests.post(url,data=json.dumps(postdata),headers =headers)
                
                print(requests.post)
                print(response)

                postdata1 = {"DeviceId":231371,"Value":"TEMP","Data":tempProm1,"BusinessUnitId":486,"GreenHouseID":1137,"Time":fecha + " " + hora,"Sensor":"AM2315"}
                print(postdata1)

                headers = {'content-type':'application/json'}
                response1 = requests.post(url,data=json.dumps(postdata1),headers =headers)

                print(requests.post)
                print(response1)

                archivo = open("LOG_RESPONSE2.txt",'a')
                archivo.write(fecha + "," + hora + ",TEMP," + str(tempProm1) + "," + str(response) + "\n" )
                archivo.write(fecha + "," + hora + ",RHUM," + str(humProm1) + "," + str(response1) + "\n" )
                archivo.close()
                print ("OK !")

            except:

                archivo = open("LOG_EXCEPT.txt",'a')
                archivo.write(fecha + "," + hora + ",TEMP," + str(tempProm1) + "\n")
                archivo.write(fecha + "," + hora + ",RHUM," + str(humProm1) + "\n")
                archivo.close()
                print ("Datos perdidos, sin red")
        break


if __name__ == '__main__':
    am()



