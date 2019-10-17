import binascii
import sys,getopt
import socket
import numpy as np
import time
import struct
import os
import threading
#import scipy.signal as signal
import resources.variablesEMG as variablesEMG

#object to aquire and analyze the EMG delsys data

class EMG_Sensor(object):

    def __init__(self):

        self.variablesEMG = variablesEMG.EMG_Variables()
        self.variablesEMG.load_variables()

        #Create the sockets to initiate the communication with EMG delsys system
        #creates general connection with EMG Delsys
        self.s1 = socket.socket()
        self.s1.connect(('localhost', 50040))
        #Opening the specific port to get EMG signal
        self.s = socket.socket()
        self.s.connect(('localhost',50041))
        #Command to start, always ends with \r\n\r\n

        self.start_command="START\r\n\r\n"
        self.s1.sendall(self.start_command)


        
        

        
        

        self.go_ON = False

    def process(self):

        counter = 0
        iR = 0
        iL = 0
        p = 0
        k = 1

        #self.s1.send(bytes(self.start_command))
        #print("start")
        for i in range(1000) :
            #Receiving info in packages of 4 BYTES so each package is an emg
            self.variablesEMG.answer = self.s.recv(4)
            a = struct.unpack('>f', self.variablesEMG.answer)
            print(a)
            #self.variablesEMG.emg0.append(a)
            #print(self.variablesEMG.emg0)
            
    def start(self):

        self.go_ON = True


def main():
    emg = EMG_Sensor()
    emg.process()

A= main()



        

    


            




        




#if __name__ == '__main__':
    #main()
