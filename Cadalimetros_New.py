import RPi.GPIO as GPIO
from datetime import time, date, timedelta
from datetime import datetime as dt
GPIO.setmode(GPIO.BCM)
from threading import Thread


class Caudalimetro:
    
    caudalCounter = 0
    caudalAcum = 0
    datetime = None
    _id = None
    factor = 0
    timelapse = 0
    started = False
    value = 0
    N = 8
    devices_name = 'caudales'

    def __init__(self,channel=None,id=None,factor=None,ubi=None):

        self.channel = channel
        self._id = id
        self.factor = factor
        self.ubi = ubi

        #Setting channel
        GPIO.setup(self.channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.remove_event_detect(self.channel)
        GPIO.add_event_detect(self.channel, GPIO.RISING, bouncetime=500,callback=self.inc_caudal)

    def inc_caudal(self,ch):
        now = dt.now()
        if not self.started:

            self.datetime = now
            print('start',ch,now)
            self.started = True
            return None
                
        self.caudalCounter += 1
        self.caudalAcum += 1
        self.timelapse = (now-self.datetime)
        self.timelapse_delta = time(0,3,0)
        self.value = self.factor*self.caudalCounter/round((self.timelapse.total_seconds()))
        print(self)
        print(self.datetime)
        print(self.timelapse)
        print(self.timelapse_delta)

        if self.caudalCounter >= self.N:  
            id_tmp = self._id
            value_tmp = self.value
            thread = Thread(target = self.ubi.send_value, args = ({'id':id_tmp,'value':value_tmp},self.devices_name,))
            thread.start()
            self.resetTimer()
            self.resetCounter()
        
        elif self.timelapse == self.timelapse_delta:
            print("Ha caducado el tiempo")
            
        # nueva linea para que no pare esperando el octavo pulso y reporte cero
        
    def resetCounter(self):
        # Reset caudal to 0
        self.caudalCounter = 0

    def resetTimer(self):
        # Reset Timer to 0-
        self.timelapse = 0
        self.datetime = dt.now()

    def get_id(self):
        return self._id

    def __repr__(self):
        return '{0}:{1}({2}) at {3:%d-%m-%Y %H:%M:%S}//lapse {4}//value {5}'.format(self.channel,
                    self.caudalCounter,self.caudalAcum,
                    self.datetime,self.timelapse,self.value)


class Caudalimetros:

    allowed_channels = list(range(2,28))
    CaudalGroup = None

    def __init__(self,channels=[],ids=[],factors=[],ubi=None):

        self.channels = channels
        self._ids = ids
        self.factors = factors
        self.ubi = ubi

        if len(self.channels)<1 or len((set(self.channels)-set(self.allowed_channels)))>0:
            print("Error in channels")
            GPIO.cleanup()
            exit()
        elif len(self._ids)!=len(self.channels) or len(self._ids)!=len(self.factors):
            print("Error in config file")
            GPIO.cleanup()
            exit()

        self.caudalGroup = {self.channels[i]:Caudalimetro(self.channels[i],self._ids[i],self.factors[i],ubi) for i in range(len(self.channels))}


    def __repr__(self):
        return '{0}'.format(self.caudalGroup.values())

 