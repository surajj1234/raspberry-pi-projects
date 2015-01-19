#!/usr/bin/env python

import MamaRoo_BTDetector
import ArduinoController
import OrigamiController
import time

COM_PORT_BT_DONGLE_LINUX = "/dev/ttyACM0"
COM_PORT_ARDUINO = "/dev/ttyAMA0"

WEARABLE_NOT_FOUND_ORIGAMI_NOT_PRIMED = 1
WEARABLE_FOUND_ORIGAMI_NOT_PRIMED = 2
WEARABLE_FOUND_ORIGAMI_PRIMED = 3
WEARABLE_NOT_FOUND_ORIGAMI_PRIMED =4

class WearableDemo():

    def __init__(self):
        
        self.runProgram = True
        self.btDetector = MamaRoo_BTDetector.MamaRoo_BTDetector(COM_PORT_BT_DONGLE_LINUX, "mamaRoo", self.rssi_update_callback)        
        self.arduino = ArduinoController.ArduinoController(COM_PORT_ARDUINO, self.gesture_callback)    
        self.origami = OrigamiController.OrigamiController()        

    def rssi_update_callback(self, rssi): 
        
        print("RSSI = %.1f") % rssi        

    def gesture_callback(self):
        
        print("Gesture detected by sonar")    

    def run_state_machine(self):

        while self.runProgram == True:
            pass

    def shutdown(self):
        self.runProgram = False
        self.arduino.close()
        self.btDetector.shutdown()
        print("Exiting Wearable Demo program....")

if __name__ == "__main__":

    demo = WearableDemo()
    try:
        demo.run_state_machine()
    except KeyboardInterrupt:
        demo.shutdown()
