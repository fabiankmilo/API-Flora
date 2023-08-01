# -*- coding: utf-8 -*-
#!/usr/bin/python

import Adafruit_DHT
import time
import datetime
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

global humidity
global temperature

def dht():
    
    sensor = Adafruit_DHT.DHT22
    pin = 4
    timeProm = 10 #Tiempo en segundos que el sensor toma datos para promediar
    timeData = 1 #Frecuencia en segundos de toma de datos
    hora_inicial = time.time() + timeProm #Inicializar hora de referencia con desfase de timeProm segundos a comparar con hora actual
    tempSum = 0 #Inicializar suma de temperatura a promediar
    humSum = 0 #Inicializar suma de humedad a promediar
    Sum = 0 #Inicializar contador de datos tomados para promedio
    
    while True:
        
        while hora_inicial - time.time() > 0: #Mientras la hora inicial de referencia sea mayor a la hora actual
            humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
            
            if humidity is not None and temperature is not None: #Antes de tomar acciones con los ventiladores verificar efectivamente que se lea un dato correcto
                tempSum += temperature #Sumar temperaturas
                humSum += humidity #Sumar humedades
                Sum = Sum + 1 #Incrementar contador
                print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
                
            else:
                print('Failed to get reading. Try again!')
                
                GPIO.setup(19, GPIO.OUT)
                GPIO.output(19, True)
                
                GPIO.setup(26, GPIO.OUT)
                GPIO.output(26, True)
                
                print ("OFF")
            
            
            time.sleep(timeData) #Pausa aprox. de frecuencia de toma de datos
            
        hora_inicial = time.time() + timeProm #Reiniciar la hora inicial de referencia
        tempProm = tempSum/Sum #Promedio temperatura
        humProm = humSum/Sum #Promedio humedad
        print(tempProm)
        print(humProm)
        tempSum = 0 #Reiniciar sumas de temperatura, humedad, y contador de toma de datos
        humSum = 0
        Sum = 0
        
        if humProm >= 90 or tempProm >= 28: #Cumplir efectivamente con el rango de humedad especificado
            
            fecha = time.strftime("%Y-%m-%d")
            hora = time.strftime("%H:%M:%S")
            
            GPIO.setup(19, GPIO.OUT)
            GPIO.output(19, False)
            
            GPIO.setup(26, GPIO.OUT)
            GPIO.output(26, False)
            print ("ON")
            
            archivo1 = open("LOG_V.txt",'a')
            archivo1.write(fecha + "," + hora + "," + '{0:0.1f},{1:0.1f}'.format(temperature, humidity) + ",ON" + "\n")
            archivo1.close()
            #Para el caso de la temperatura, de ser mayor a 28 grados encender los ventiladores, de ser menor debido a que no
            #hay restricción mantenerlos encendidos hasta que la humedad sea menor a 85%.
            
        elif humProm < 90 or tempProm < 28:
            
            fecha = time.strftime("%Y-%m-%d")
            hora = time.strftime("%H:%M:%S")
            
            GPIO.setup(19, GPIO.OUT)
            GPIO.output(19, True)
            
            GPIO.setup(26, GPIO.OUT)
            GPIO.output(26, True)
            print ("OFF")
            
            archivo1 = open("LOG_V.txt",'a')
            archivo1.write(fecha + "," + hora + "," + '{0:0.1f},{1:0.1f}'.format(temperature, humidity) + ",OFF" + "\n")
            archivo1.close()
            
        break
    
if __name__=="__main__":
    dht()
