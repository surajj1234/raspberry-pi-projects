import time 
import os
import RPi.GPIO as GPIO

REV1 = 3
REV2 = 2
BUTTON = 17
LIGHTS = 22

GPIO.setmode(GPIO.BCM)
GPIO.setup(REV1,GPIO.OUT) #Rev 2 
GPIO.setup(REV2,GPIO.OUT) #Rev 1
GPIO.setup(BUTTON,GPIO.OUT) #Dial Switch
GPIO.setup(LIGHTS,GPIO.OUT) # Lights

GPIO.output(REV1, True)
GPIO.output(REV2, True)
GPIO.output(BUTTON, False)
GPIO.output(LIGHTS, False)

class OrigamiController():

    def __init__(self):
        '''Controls actuation and lights on an Origami'''
        pass

    def actuate(self):
        print("Actuating Origami")
        
        GPIO.output(REV1, False)
        time.sleep(0.1)
        GPIO.output(REV1, True)
        time.sleep(0.1)
        
        GPIO.output(REV2, False)
        time.sleep(0.1)
        GPIO.output(REV2, True)
        time.sleep(0.1)
        
        GPIO.output(BUTTON, True)
        time.sleep(0.1)
        GPIO.output(BUTTON, False)
        time.sleep(4)

    def turn_lights_on(self):
        print("Turning light on")
        
        GPIO.output(LIGHTS, True)
        

    def turn_lights_off(self):
        print("Turning lights off")
        
        GPIO.output(LIGHTS, False)
