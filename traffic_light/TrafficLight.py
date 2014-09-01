#! /usr/bin/python

import time
import RPi.GPIO as GPIO
import threading

class TrafficLight:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.ledList = []

    def addLed(self, ledname, gpiono, delay_secs, status_blink=False):
        self.ledList.append(Led(ledname, gpiono, delay_secs, status_blink))
        return len(self.ledList)

    def startTrafficLight(self):
        for led in self.ledList:
            print ('startTrafficLight %s led off status : %d' % (led.ledName, led.ledStatus))
            led.poweredTurnOffLed()

        for led in self.ledList:
            led.turnOnLedAndAutoOff()
            while led.ledStatus != 0:
                print ('startTrafficLight %s led run status : %d' % (led.ledName, led.ledStatus))
                time.sleep(1)

class Led:
    def __init__(self, ledname, gpiono, delay_secs, status_blink=False):
        # 
        self.ledName = ledname
        # This LED's RaspberryPi GPIO BCM No.
        self.GPIONO = -1

        self.LED_STATUS_OFF = 0
        self.LED_STATUS_ON = 1
        self.LED_STATUS_BLINK = 2
        self.ledStatus = self.LED_STATUS_OFF

        self.GPIONO = gpiono
        self.DELAY_SECS = delay_secs
        self.STATUS_BLINK = status_blink

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.GPIONO, GPIO.OUT)

        self.setDelaySecs(self.DELAY_SECS)

        self.poweredTurnOffLed()

    def setDelaySecs(self, delay_secs):
        #print('%s setDelaySecs %d sec' % (self.ledName, delay_secs))
        self.DELAY_SECS = delay_secs

    def setStatusBlink(self, status_blink):
        #print('%s status_blink %d' % (self.ledName, status_blink))
        self.STATUS_BLINK = status_blink
        
    def turnOnLed(self):
        GPIO.output(self.GPIONO, True)    

        #print('%s turnOnLed ledStatus :%d, GPIO:%d' %  (self.ledName, self.ledStatus, self.GPIONO))

        if self.ledStatus == self.LED_STATUS_ON:
            turnoff_timmer.cancel()

        self.ledStatus = self.LED_STATUS_ON

        self.turnoff_timmer = threading.Timer(self.DELAY_SECS, self.turnOffLed)
        self.turnoff_timmer.start()

    def turnOffLed(self):
        try:
            #print('%s turnOffLed ledStatus :%d, GPIO:%d' %  (self.ledName, self.ledStatus, self.GPIONO))

            if self.STATUS_BLINK:
                self.ledStatus = self.LED_STATUS_BLINK
                for i in range(5):
                    #print('%s self.LED_STATUS_BLINK :%d, GPIO:%d' %  (self.ledName, self.ledStatus, self.GPIONO))
                    GPIO.output(self.GPIONO, True)
                    time.sleep(0.7)
                    GPIO.output(self.GPIONO, False)
                    time.sleep(0.7)
            else:
                GPIO.output(self.GPIONO, False)    

            self.ledStatus = self.LED_STATUS_OFF
            #print('%s turnOffLed change ledStatus :%d, GPIO:%d' %  (self.ledName, self.ledStatus, self.GPIONO))
        except Exception as Err:
            print (Err)

    def poweredTurnOffLed(self):
        #print('%s poweredTurnOffLed ledStatus :%d ' % (self.ledName, self.ledStatus))
        GPIO.output(self.GPIONO, False)    

        if self.ledStatus == self.LED_STATUS_ON:
            self.turnoff_timmer.cancel()
        self.ledStatus = self.LED_STATUS_OFF
        #print('%s poweredTurnOffLed ledStatus :%d ' % (self.ledName, self.ledStatus))

    def turnOnLedAndAutoOff(self):
        try:
            #print('%s turnOnLedAndAutoOff turnOnLed ledStatus :%d, GPIO:%d ' % (self.ledName, self.ledStatus, self.GPIONO))
            self.turnOnLed()
            #print('%s turnOnLedAndAutoOff turnoff_timmer.start ledStatus :%d, GPIO:%d' % (self.ledName, self.ledStatus, self.GPIONO))
        except Exception as Err:
            print (Err)

if __name__ == "__main__":

    trafficlight = TrafficLight()
    # Adding RedLed
    trafficlight.addLed('Red', 10, 10, status_blink=False)
    # Adding GreenLed
    trafficlight.addLed('Green', 11, 5, status_blink=False)
    # Adding YellowLed
    trafficlight.addLed('Yellow', 9, 2, status_blink=False)

    trafficlight2 = TrafficLight()
    # Adding RedLed
    trafficlight2.addLed('Red', 25, 10, status_blink=False)
    # Adding GreenLed
    trafficlight2.addLed('Green', 7, 5, status_blink=False)
    # Adding GreenLed
    trafficlight2.addLed('Green2', 24, 5, status_blink=False)
    # Adding YellowLed
    trafficlight2.addLed('Yellow', 8, 2, status_blink=False)

    while True:
        trafficlight.startTrafficLight()
        trafficlight2.startTrafficLight()
    #trafficlight.test()

