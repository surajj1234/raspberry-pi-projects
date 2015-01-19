#Imports
import serial
import threading
import os
import time

BAUDRATE = 9600 
TIMEOUT = 0                 # Timeout for serial read, in seconds, 0 for non-blocking reads

class ArduinoController():

    def __init__(self, comPort, gesture_detected_cb = None):
        '''Initialize serial module'''

        self.terminate = False
        self.baudRate = BAUDRATE

        self.comms = serial.Serial(comPort, self.baudRate, timeout = TIMEOUT, rtscts = 0)
        self.gesture_detected_callback = gesture_detected_cb
    
        self.start_threads()

    def start_threads(self):
        
        self.thread_list = []

        # Create threads
        self.thread_list.append(threading.Thread(target = self.com_rx_thread))
        
        # Set threads as daemons
        for thread in self.thread_list:
            thread.daemon = True

        # Start threads
        for thread in self.thread_list:
            thread.start()

    def close(self):
        ''' Shutdown serial module'''

        self.terminate = True
        time.sleep(0.1)
        self.comms.close()
        
    def com_rx_thread(self):

        while self.terminate == False:

            # Do a non-blocking read on the serial port
            byteChar = self.comms.read(1)
            
            # Check if a byte was read
            if(byteChar != b''):

                # Check if a valid gesture was detected by the Arduino
                self.valid_gesture_check(byteChar)

    def activate_gesture_recognition(self):

        packet = bytearray()
        byteChar = 0x41     # 'A' 
        packet.append(byteChar)       
        self.comms.write(packet)

    def disable_gesture_recognition(self):

        packet = bytearray()
        byteChar = 0x44     # 'D'
        packet.append(byteChar)        
        self.comms.write(packet)

    def valid_gesture_check(self, byteRx):
      
        if byteRx == 'V':  # 'V'
            if self.gesture_detected_callback is not None:
                self.gesture_detected_callback()

