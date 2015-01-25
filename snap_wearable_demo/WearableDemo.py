#!/usr/bin/env python

import MamaRoo_BTDetector
import ArduinoController
import OrigamiController
import time

COM_PORT_BT_DONGLE_LINUX = "/dev/ttyACM0"
COM_PORT_ARDUINO = "/dev/ttyUSB0"

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
        self.arduino = ArduinoController.ArduinoController(COM_PORT_ARDUINO, self.gesture_callback)    
        self.origami = OrigamiController.OrigamiController()        
        
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
        
        self.origami.turn_lights_off()
        self.arduino.disable_gesture_recognition()
        self.demoState = WEARABLE_NOT_FOUND_ORIGAMI_NOT_PRIMED

    def run_state_machine(self):

        while self.runProgram == True:
            
            if self.demoState == WEARABLE_NOT_FOUND_ORIGAMI_NOT_PRIMED:
                
                # Check if the wearable is within range of BT
                if self.newRSSIValue == True:
                    
                    # If wearable comes close to the Origami
                    if self.newRSSI > PROXIMITY_NEAR_THRESHOLD:
                        self.demoState = WEARABLE_FOUND_ORIGAMI_NOT_PRIMED
                        print("Wearable detected")

                    self.newRSSIValue = False

            elif self.demoState == WEARABLE_FOUND_ORIGAMI_NOT_PRIMED:
                
                # Turn Origami lights on    
                self.origami.turn_lights_on()

                # Tell Arduino to inform us if gestures are detected by sonar
                self.arduino.activate_gesture_recognition()
                self.demoState = WEARABLE_FOUND_ORIGAMI_PRIMED
            
            elif self.demoState == WEARABLE_FOUND_ORIGAMI_PRIMED:
                
                # Check if Arduino detected a gesture
                if self.gestureDetected == True:
                    self.origami.actuate()
                    self.gestureDetected = False
                    print("Arduino detected a gesture")
                
                # If wearable moves out of detection zone, restart state machine
                if self.newRSSI < PROXIMITY_FAR_THRESHOLD:
                    self.init_state_machine()
                    print("Wearable out of detection zone")
                
                # Restart state machine if wearable is no longer detected
                timeSinceLastRSSI = time.time() - self.lastRSSIUpdate
                if timeSinceLastRSSI > 10:
                    self.init_state_machine()
                    print("Wearable out of range")

    def shutdown(self):
        self.runProgram = False
        self.arduino.close()
        self.btDetector.shutdown()
        self.origami.turn_lights_off()
        print("Exiting Wearable Demo program....")

if __name__ == "__main__":

    demo = WearableDemo()
    try:
        demo.run_state_machine()
    except KeyboardInterrupt:
        demo.shutdown()
