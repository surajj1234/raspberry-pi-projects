#!/usr/bin/env python

import BTDongle
import MySerial
import time
import numpy as np
import threading

AVG_WINDOW_SIZE = 5 

# mamaRoo RSSI scanner State machine states
DEVICE_INIT = 1
DISCOVER = 2


class MamaRoo_BTDetector():

    def __init__(self, comPort, detectTarget = "mamaRoo", wearable_detected_cb = None):
        """Detect if a device is close by using RSSI values"""

        self.comPort = comPort
        self.detectTarget = detectTarget
        self.wearable_detected_callback = wearable_detected_cb

        self.filterSamples = []

        self.init_BT()
        self.start_threads()        
 
    def init_BT(self):

        self.serial = MySerial.MySerial(self.comPort)
        self.dongle = BTDongle.BTDongle(self.serial.comms)

        self.dongle.setup_device_init_callback(self.device_init_callback)
        self.dongle.setup_device_info_callback(self.device_info_callback)
        self.dongle.setup_discovery_done_callback(self.discovery_done_callback)

        self.runProgram = True
        self.state = DEVICE_INIT
        self.testUnitFound = False

      # BT Dongle callbacks-------------------------------------
    
    def device_init_callback(self, status):
        
        if status == 0:     # Success
           
            print("Device Init done")
            self.state = DISCOVER
            self.start_scan()
        else:
            print("Device Init failure !")
            self.shutdown()

    def device_info_callback(self, status):
        
        # Check if device discovered is a debug mamaRoo unit
        for i in range(0, len(self.dongle.peripheral_list)):
            if self.dongle.peripheral_list[i].localName == self.detectTarget:
                self.testUnitFound = True
                self.testUnitID = i

                # Cancel scan since unit has been found
                self.dongle.do_cancel_discovery()

    def discovery_done_callback(self, status):
        
        if self.testUnitFound == True:
            avgRSSI =  self.averaged_RSSI(self.dongle.peripheral_list[self.testUnitID].RSSI)

            # Update callback to notify other threads
            if self.wearable_detected_callback is not None:
                self.wearable_detected_callback(avgRSSI)
         
        self.start_scan()       
 
    def start_scan(self):
       
        # start scanning for devices
        self.testUnitFound = False
        self.dongle.do_discovery()
        self.scanStartTime = time.time()
    
    def averaged_RSSI(self, newValue):
        
        self.filterSamples.append(newValue)
        
        avgValue = -100
        if len(self.filterSamples) >= AVG_WINDOW_SIZE:
            avgValue = np.mean(self.filterSamples)
            del self.filterSamples[0]
        
        return avgValue

    def run_state_machine(self):

        while self.runProgram == True:
            
            self.mamaRoo_rssi_sm()
            
    def mamaRoo_rssi_sm(self):

        # State machine to continuously scan for a mamaRoo, and update RSSI values
        if self.state == DEVICE_INIT:       # Wait until the BT dongle initialization is complete
            time.sleep(0.1) 
        if self.state == DISCOVER:          # Wait until the BT dongle completes a scan
            time.sleep(0.1)
            scanDuration = time.time() - self.scanStartTime
            
            if(scanDuration > 2):
               # Cancel scan and start a fresh scan
                self.dongle.do_cancel_discovery()

    def shutdown(self):
        self.runProgram = False
        
        time.sleep(0.5)
            
        # Shutdown serial and BT dongle modules
        self.serial.close()
        self.dongle.close()

    #Thread handling--------------------------------------------
    
    def start_threads(self):
        
        self.thread_list = []
        
        # Create threads
        self.thread_list.append(threading.Thread(target = self.run_state_machine))
        
        # Set threads as daemons
        for thread in self.thread_list:
            thread.daemon = True

        # Start threads
        for thread in self.thread_list:
            thread.start()

