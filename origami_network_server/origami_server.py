#!/usr/bin/env python

import socket
import sys
import OrigamiController

SERVER_IP = "10.10.10.181"
#SERVER_IP = "localhost"

SERVER_PORT = 10000
MESSAGE_SIZE = 1 

TURN_LIGHTS_ON = 'L'
TURN_LIGHTS_OFF = 'O'
STROLLER_ACTUATE = 'A'

class Origami_Server():

    def __init__(self):
        '''Creates a server which can be used to control an Origami over a network'''

        self.origami = OrigamiController.OrigamiController()
    
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to a port
        server_address = (SERVER_IP, SERVER_PORT)
        print >> sys.stderr, "Starting up server on %s port %s" % server_address
        self.sock.bind(server_address)

        # Listen for incoming connections
        self.sock.listen(1)

    def command_received(self, command):

        if command == TURN_LIGHTS_ON:
            print >> sys.stderr, "Turning origami lights on"
            self.origami.turn_lights_on()

        elif command == TURN_LIGHTS_OFF:
            print >> sys.stderr, "Turning origami lights off"
            self.origami.turn_lights_off()

        elif command == STROLLER_ACTUATE:
            print >> sys.stderr, "Actuating stroller"
            self.origami.actuate()            

        elif command == "\n":
            pass
        else:
            print >> sys.stderr, "Unknown command"


    def wait_for_connection(self):

        while True:

            # Wait for an incoming connection
            print >> sys.stderr, "Waiting for incoming connection"
            connection, client_address = self.sock.accept()

            try:
                print >> sys.stderr, "Connection from", client_address
            
                while True:

                    data = connection.recv(MESSAGE_SIZE)
                    
                    if data:
                        self.command_received(data)

                    else:
                        print >> sys.stderr, "no more data from", client_address
                        break

            finally:

                # Clean up the connection
                connection.close()
    

if __name__ == "__main__":

    server = Origami_Server()
    try:
        server.wait_for_connection()
    except KeyboardInterrupt:
        print("Shutting down server")
