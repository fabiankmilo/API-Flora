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

    # create the I2C shared bus
    i2c = busio.I2C(board.SCL, board.SDA)
    am = adafruit_am2320.AM2320(i2c)

    temp = float(am.temperature)
    hum = float(am.relative_humidity)

    return(temp,hum)

def datasensor():

    temp, hum = am()

    fecha = time.strftime("%Y/%m/%d")
    hora = time.strftime("%H:%M:%S")
    url = 'http://sensor.agroyautomatizacion.com/api/sensor'


    if temp <= 100 and hum <= 100:

        try:
            postdata = {"Hora":hora,"Fecha":fecha,"Sensor": 1,"Valor":temp}
            print(postdata)

            headers = {'content-type':'application/json'}
            response = requests.post(url,data=json.dumps(postdata),headers =headers)

            print(requests.post)
            print(response)

            postdata1 = {"Hora":hora,"Fecha":fecha,"Sensor": 2,"Valor":hum}
            print(postdata1)

            headers = {'content-type':'application/json'}
            response1 = requests.post(url,data=json.dumps(postdata1),headers =headers)

            print(requests.post)
            print(str(response1))

        except:

            archivo = open("LOG_EXCEPT.txt",'a')
            archivo.write(fecha + "," + hora + ",TEMP," + str(temp) + "\n")
            archivo.write(fecha + "," + hora + ",RHUM," + str(hum) + "\n")
            archivo.close()
            print ("Datos perdidos, sin red")
            print ("error de request")


if __name__ == '__main__':
#am()
    datasensor()




