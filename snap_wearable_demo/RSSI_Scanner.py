#!/usr/bin/env python

import MamaRoo_BTDetector
import time

COM_PORT_BT_DONGLE_LINUX = "/dev/ttyACM0"

WEARABLE_NOT_FOUND_ORIGAMI_NOT_PRIMED = 1
WEARABLE_FOUND_ORIGAMI_NOT_PRIMED = 2
WEARABLE_FOUND_ORIGAMI_PRIMED = 3
WEARABLE_NOT_FOUND_ORIGAMI_PRIMED =4

PROXIMITY_NEAR_THRESHOLD = -70
PROXIMITY_FAR_THRESHOLD = -80

class WearableDemo():

    def __init__(self):
        
        self.runProgram = True
        self.btDetector = MamaRoo_BTDetector.MamaRoo_BTDetector(COM_PORT_BT_DONGLE_LINUX, "X2-Wrbl", self.rssi_update_callback)        
        
        self.demoState = WEARABLE_NOT_FOUND_ORIGAMI_NOT_PRIMED
        self.gestureDetected = False
        self.newRSSIValue = False
        self.lastRSSIUpdate = time.time()

        self.init_state_machine()

    def rssi_update_callback(self, rssi): 
        
        self.newRSSIValue = True
        self.newRSSI = rssi    
        self.lastRSSIUpdate = time.time()
        print("RSSI = %.1f") % rssi        

    def gesture_callback(self):
     
        self.gestureDetected = True

    def init_state_machine(self):
        
        self.demoState = WEARABLE_NOT_FOUND_ORIGAMI_NOT_PRIMED

    def run_state_machine(self):

        while self.runProgram == True:
            
            pass

    def shutdown(self):
        self.runProgram = False
        self.btDetector.shutdown()
        print("Exiting Wearable Demo program....")

if __name__ == "__main__":

    demo = WearableDemo()
    try:
        demo.run_state_machine()
    except KeyboardInterrupt:
        demo.shutdown()
