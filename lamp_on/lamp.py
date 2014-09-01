#! /usr/bin/python

import time, sys
import RPi.GPIO as GPIO
#lib_path = os.path.abspath('../TrafficLight')
sys.path.append('../traffic_light')

import TrafficLight

led = TrafficLight.Led("yellow", 18, 2, status_blink=True)

while True:
    led.turnOnLedAndAutoOff()
    while led.ledStatus != 0:
        time.sleep(1)