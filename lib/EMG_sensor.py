from __future__ import division
import binascii
import sys,getopt
import socket
import numpy as np
import time
import struct
import os
import threading
import scipy.signal as signal
import resources.variablesEMG as variablesEMG
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from matplotlib import style
import CpWalker_index as cp


#object to aquire and analyze the EMG delsys data

class EMG_Sensor(object):

    def __init__(self, settings = {'MuscletoUse': None}):

        #load settings
        self.settings = settings
        self.MuscletoUse = self.settings['MuscletoUse']
        print(self.MuscletoUse)

        self.variablesEMG = variablesEMG.EMG_Variables()
        self.variablesEMG.load_variables()
        self.phase_Gait = 0
        self.cp = cp.CpWalkerAquisition()

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
        plt.axis([0,0.0005,0,0.0003])
        im=0
        init=0
        init1=0

        #self.s1.send(bytes(self.start_command))
        #print("start")
        while True:
        #for i in range(1000000):
            #Receiving info in packages of 4 BYTES so each package is an emg
            self.variablesEMG.answer = self.s.recv(4)
            a = struct.unpack('f', self.variablesEMG.answer)
            self.variablesEMG.emg0.append(a)
            p += 1
            #print(self.variablesEMG.emg0)
            if(p > 1) :

                #print(self.variablesEMG.emg0)
                
                if(len(self.variablesEMG.emg0) % 16 == 1) :

                    k = self.getIndexCpWalker()
                    #print('getIndexCpWalker')
                    #print(k)
                    kleft = k + 100

                    self.variablesEMG.Index.append(self.decidePhase(k))
                    self.variablesEMG.IndexLeft.append(self.decidePhase(kleft))

                    '''    
                    print('Index cpWalker_Data')
                    print(self.variablesEMG.IndexLeft)
                    print(kleft)
                    '''
                    self.phase_Gait = self.decidePhase(k)

                    

                    self.variablesEMG.RightGluteus.append(self.variablesEMG.emg0[counter][0])
                    self.variablesEMG.RightQuadriceps.append(self.variablesEMG.emg0[counter+1][0])
                    self.variablesEMG.RightTriceps.append(self.variablesEMG.emg0[counter+2][0])
                    self.variablesEMG.RightHamstrings.append(self.variablesEMG.emg0[counter+3][0])
                
                    self.variablesEMG.LeftGluteus.append(self.variablesEMG.emg0[counter+4][0])
                    self.variablesEMG.LeftQuadriceps.append(self.variablesEMG.emg0[counter+5][0])
                    self.variablesEMG.LeftTriceps.append(self.variablesEMG.emg0[counter+6][0])
                    self.variablesEMG.LeftHamstrings.append(self.variablesEMG.emg0[counter+7][0])
                    k += 1

                    #print('------len-------')
                    #print(len(self.variablesEMG.LeftQuadriceps))
                    #print(self.variablesEMG.LeftQuadriceps)
                    #print('------------------')
                    

                    if k == 200:

                        p_0 = len(self.variablesEMG.RightGluteus)

                        if (self.MuscletoUse == "1"):
                            self.Muscle(self.variablesEMG.RightGluteus[init:p_0],"RightGluteus",self.variablesEMG.Index[init:p_0])
                        #self.Muscle(self.variablesEMG.RightQuadriceps[init:p_0],"RightQuadriceps")
                        #self.Muscle(self.variablesEMG.RightTriceps[init:p_0],"RightTriceps",self.variablesEMG.Index[init:p_0])
                        #self.Muscle(RightHamstrings[iR:p],"RightHamstrings",Index[iR:p])
                        init = p_0
                    
                    if kleft == 200:
                        p_1 = len(self.variablesEMG.LeftQuadriceps)

                        #print('here kleft')
                        #print(len(self.variablesEMG.LeftQuadriceps))
                        #print('here kleft')
                        if (self.MuscletoUse == "1"):
                            self.Muscle(self.variablesEMG.LeftGluteus[init1:p_1],"LeftGluteus",self.variablesEMG.IndexLeft[init1:p_1])
                        #self.Muscle(self.variablesEMG.LeftQuadriceps[init1:p_1],"LeftQuadriceps", self.variablesEMG.Index[init:p_1])
                        #self.Muscle(LeftTriceps[iL:p],"LeftTriceps",IndexLeft[iL:p])
                        #self.Muscle(LeftHamstrings[iL:p],"LeftHamstrings",IndexLeft[iL:p])

                        init1 =p_1

                    counter += 16

                if len(self.variablesEMG.emg0) == 5000000:
                    print("ya")
                    break
  


    
        #print(self.variablesEMG.RightGluteus)


    def plot_emg(self,emg):

        plt.figure()
        plt.title("EMG")
        plt.plot(emg) 
        plt.show()

    def getIndexCpWalker(self):

        m =self.cp.cpWalker_Data()

        return(m)

    def start(self):

        self.cp.start()
        self.cp.launch_CPthread()
        time.sleep(0.1)
        self.go_ON = True

    def stop(self):
        self.cp.stop()
        self.go_ON = False

    def decidePhase(self,index):

        phase = -1
        if 0<=index<40:
            phase = 1
        if 40<=index<90:
            phase = 2
        if 90<=index<140:
            phase = 3
        if 140<=index<=200:
            phase = 4
        
        return phase


    def launch_EMGsensor(self):

        self.p = threading.Thread(target = self.process)
        self.p.start()



    def Muscle(self,emg,MuscleName, CpWalkerIndex):
        print('Muscle')
        #print(len(CpWalkerIndex))
        window = signal.get_window('hann',80)
        RMSemg, time = self.rollapply(emg,window, by=1, fs=1.)
        fs = 2000 
        fc = 10/(fs/2)
        b = signal.firwin(100,fc)
        self.emg_filtered = signal.lfilter(b,1,RMSemg)
        #print(self.emg_filtered)
        decision, contraction = self.apply_threshold(self.emg_filtered*10000)

        print("Contractions in the time")
        #print(len(decision))
        print(decision)
        for u in range(len(decision)):
            if decision[u] > 0:
                print u


    def rollapply(self,x, window, by=1, fs=1.):


    #    """
    #    Applies a function to a signal in a moving window.
    #    :param x: The input signal.
    #    :param fun: The function to be applied in each of the windows. It should take an input signal as argument.
    #    :param window: A window function as returned by scipy.signal.get_window
    #    :param by: calculate 'fun' at every 'by'-th time point
    #    :param fs: sampling frequency of 'x'
    #    :return: a tuple consisting of time, result
    #    """
        result = []
        time = []
        for j in range(0, len(x)-len(window)-1,by):
            a = x[j:(j+len(window))]*window
            b = self.RMS(a)
            result.append(b)
            
            c = (j+j+len(window))/2
            time.append(c)
            
        return (result,time)



        

    def RMS(self,x):

        M = len(x)
        suma = np.sum(x*x)
        return np.sqrt(suma/M)

    def threshold_from_data(self,emg):
  
        mean = 0
        for k in range(0 ,len(emg)-1):
            mean+=emg[k]
        th = (mean/len(emg)) *1.5
        return th

    def apply_threshold(self,emg):

        th = self.threshold_from_data(emg)
        contraction_position = []
        contraction = []
        for j in range(0,len(emg)-1):
            contraction_position.append(0)
            contraction.append(0)
            
        contraction_position[0] = 1000
        
        for k in range(0,len(emg)-1):
            if (((emg[k]>th) and (emg[k+1]<th)) or (((emg[k]<th) and (emg[k+1]>th)))):
                contraction[k] = 1*th
                print("CONTRACTION")
                self.contraction = 1
            else : 
                contraction[k] = 0 
                self.contraction = 0
         
        return contraction, self.contraction

    def muscleGaitAnalysis(self, contractionList, CpWalkerIndex, MuscleName):

        self.phaseConstant = 0
        self.phaseConstant2 = 0
        self.contractionList = np.array(contractionList)
        self.CpWalkerIndex = np.array(CpWalkerIndex)
        self.contractionList.resize(self.CpWalkerIndex.shape)
        self.maskMatrix = self.contractionList*self.CpWalkerIndex


        # Gait Analysis

        if MuscleName == "RightGluteus" or MuscleName == "LeftGluteus":

            self.phaseConstant = 1

        elif MuscleName == "RightHamstrings" or MuscleName =="LeftHamstrings":

            self.phaseConstant = 1

        elif MuscleName == "RightQuadriceps" or MuscleName == "LeftQuadriceps":

            self.phaseConstant = 2
            self.phaseConstant2= 4

        elif MuscleName == "RightTriceps" or MuscleName == "LeftTriceps":

            self.phaseConstant = 3

        





    
def main():
    emg = EMG_Sensor(settings = {'MuscletoUse': "1"})
    emg.start()
    emg.process()
    emg.stop()
    
    

A= main()



        

    


            




        




#if __name__ == '__main__':
    #main()
