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
        global GPIONO
        # This LED's On Delay Time
        global DELAY_SECS
        # True = Blink at Turn Off Time
        global STATUS_BLINK
        # pass sec after Turn On
        global turnon_sec_count
        # Turn Off Timer
        global turnoff_timmer

        self.LED_STATUS_OFF = 0
        self.LED_STATUS_ON = 1
        self.LED_STATUS_BLINK = 2
        self.ledStatus = self.LED_STATUS_OFF

        GPIONO = gpiono
        DELAY_SECS = delay_secs
        STATUS_BLINK = status_blink

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(GPIONO, GPIO.OUT)

        self.setDelaySecs(DELAY_SECS)

    def setDelaySecs(self, delay_secs):
        print('%s setDelaySecs %d sec' % (self.ledName, delay_secs))
        global DELAY_SECS
        DELAY_SECS = delay_secs
        global turnoff_timmer
        turnoff_timmer = threading.Timer(DELAY_SECS, self.turnOffLed)

    def setStatusBlink(self, status_blink):
        print('%s status_blink %d' % (self.ledName, status_blink))
        global STATUS_BLINK
        STATUS_BLINK = status_blink
        
    def turnOnLed(self):
        print('%s turnOnLed ledStatus :%d ' %  (self.ledName,self.ledStatus))
        global GPIONO
        GPIO.output(GPIONO, True)    

        global turnoff_timmer
        turnoff_timmer.cancel()

        self.ledStatus = self.LED_STATUS_ON

    def turnOffLed(self):
        try:
            print('%s turnOffLed ledStatus :%d ' % (self.ledName, self.ledStatus))
            global turnoff_timmer
            turnoff_timmer.cancel()

            global GPIONO
            global STATUS_BLINK
            if STATUS_BLINK:
                self.ledStatus = self.LED_STATUS_BLINK
                for i in range(5):
                    print('%s self.LED_STATUS_BLINK :%d ' % (self.self.ledName, self.LED_STATUS_BLINK))
                    GPIO.output(GPIONO, True)
                    time.sleep(1)
                    GPIO.output(GPIONO, False)
                    time.sleep(1)
            else:
                GPIO.output(GPIONO, False)    

            self.ledStatus = self.LED_STATUS_OFF
        except Exception as Err:
            print (Err)

    def poweredTurnOffLed(self):
        print('%s poweredTurnOffLed ledStatus :%d ' % (self.ledName, self.ledStatus))
        global GPIONO
        GPIO.output(GPIONO, False)    

        global turnoff_timmer
        turnoff_timmer.cancel()
        self.ledStatus = self.LED_STATUS_OFF
        print('%s poweredTurnOffLed ledStatus :%d ' % (self.ledName, self.ledStatus))

    def turnOnLedAndAutoOff(self):
        try:
            print('%s turnOnLedAndAutoOff turnOnLed ledStatus :%d ' % (self.ledName, self.ledStatus))
            global DELAY_SECS
            global turnoff_timmer
            self.turnOnLed()
            print('%s turnOnLedAndAutoOff turnoff_timmer.start ledStatus :%d ' % (self.ledName, self.ledStatus))
            turnoff_timmer.start()
        except Exception as Err:
            print (Err)

if __name__ == "__main__":

    trafficlight = TrafficLight()
    # Adding RedLed
    trafficlight.addLed('Red', 10, 10, status_blink=False)
    # Adding YellowLed
    #trafficlight.addLed('Yellow', 9, 3, status_blink=False)
    # Adding GreenLed
    #trafficlight.addLed('Green', 11, 5, status_blink=True)

    print ('Add Complete : %s' % trafficlight.ledList[0].ledName)
    #print ('Add Complete : %s' % trafficlight.ledList[1].ledName)
    #print ('Add Complete : %s' % trafficlight.ledList[2].ledName)

    #trafficlight.startTrafficLight()
    trafficlight.test()

