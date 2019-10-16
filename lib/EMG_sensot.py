import sys,getopt
import socket
import numpy as np
import time
import struct
import os
import threading
import scipy.signal as signal
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
        self.start_command= start_command.encode("utf-8")
        self.s1.sendall(bytes(start_command))
        print("start")

        self.go_ON = False

    def process(self):

        counter = 0
    iR = 0
    iL = 0
    p = 0
    k = 1
    while 1 :
        
        #Receiving info in packages of 4 BYTES so each package is an emg
        answer = s.recv(4)
        print("Aqui")
        a = struct.unpack('f', answer)
        print(a)
        emg0.append(a)
        p += 1
        
        if(p > 1) :

            print(emg0)
            
            if(len(emg0) % 16 == 1) :
           
                k = getIndexCPWalker()
                
                kleft = k +100
                Index.append(decidePhase(k))
                IndexLeft.append(decidePhase(kleft))
                
                
                RightGluteus.append(emg0[counter])
                RightQuadriceps.append(emg0[counter+1])
                RightTriceps.append(emg0[counter+2])
                RightHamstrings.append(emg0[counter+3])
            
                LeftGluteus.append(emg0[counter+4])
                LeftQuadriceps.append(emg0[counter+5])
                LeftTriceps.append(emg0[counter+6])
                LeftHamstrings.append(emg0[counter+7])
                k += 1
               
                
                if k == 12000:
                   
                    Muscle(RightGluteus[iR:p],"RightGluteus",Index[iR:p])
                    Muscle(RightQuadriceps[iR:p],"RightQuadriceps",Index[iR:p])
                    Muscle(RightTriceps[iR:p],"RightTriceps",Index[iR:p])
                    Muscle(RightHamstrings[iR:p],"RightHamstrings",Index[iR:p])
                    iR = p
                    
                if kleft == 200:
                    Muscle(LeftGluteus[iL:p],"LeftGluteus",IndexLeft[iL:p])
                    Muscle(LeftQuadriceps[iL:p],"LeftQuadriceps",IndexLeft[iL:p])
                    Muscle(LeftTriceps[iL:p],"LeftTriceps",IndexLeft[iL:p])
                    Muscle(LeftHamstrings[iL:p],"LeftHamstrings",IndexLeft[iL:p])
                    iL = p
                   
                counter += 16
                
            if len(emg0) == 500000 :
                print("ya")
                break

    def cpWalkerSimulation(self):
        #IMPORTANT
        #This function simulates the index given by the CpWalker
        #In order to connect it to the real one. This is the place to put
        #the acquisition code

        self.index = 0

        while self.go_ON:
            # Cyclic patron generation
            self.index = self.index + 1
            if (self.index > 200):
                self.index = 0
            
            time.delay(0.015)

    def getIndexCPWalker(self):

        self.cpData = self.index
        return(self.cpData)

    def decidePhase(self, index):

        self.variablesEMG.phase = -1
        if 0<=index<40:
            self.variablesEMG.phase = 1
        if 40<=index<90:
            self.variablesEMG.phase = 2
        if 90<=index<140:
            self.variablesEMG.phase = 3
        if 140<=index<=200:
            self.variablesEMG.phase = 4
    
        return self.variablesEMG.phase

    def knowPhaseChange(self, phases):
        p = 0
        change = []
        for i in range( 0, len(phases)-2):
            if phases[i] != phases[i+1]:
                change.append(i+1)
            
                print(i)
                p+=1
        if p == 0: 
            change.append(-1)
            p = -1
        return(change,p)

    def countContractions(self, contractionlist):

        contadorContraction = 0
        for i in range (0,len(contractionlist)-1):
            if(contractionlist[i] != 0):
                contadorContraction+= 1

        contadorContraction = contadorContraction/2
        return contadorContraction

    def nocontractionWRONG(self,contractions,musclename,phase):

        self.variablesEMG.phase = phase

        if musclename == "RightQuadriceps" or musclename == "LeftQuadriceps":
            if contractions < 1 :
                
                if self.variablesEMG.counterEMG3[0] == cyclestowait-1:
                    self.Nao = '0'
                    if self.variablesEMG.phase == 1:
                        self.Nao = '1'
                    if self.variablesEMG.phase == 2:
                        self.Nao = '2'
                    if self.variablesEMG.phase == 3:
                        self.Nao = '3'
                    if self.variablesEMG.phase == 4:
                        self.Nao = '4'
                
                    self.variablesEMG.counterEMG2[0] = 0
                self.variablesEMG.counterEMG2[0] += 1
        if musclename == "RightTriceps" or musclename == "LeftTriceps" :
            if contractions < 1 :
                
                if self.variablesEMG.counterEMG3[0] == cyclestowait-1:
                    self.NAO ='5'
                    if self.variablesEMG.phase == 1:
                        self.NAO ='6'
                    if self.variablesEMG.phase == 2:
                        self.NAO ='7'
                    if self.variablesEMG.phase == 3:
                        self.NAO ='8'
                    if self.variablesEMG.phase == 4:
                        self.NAO ='9'
                    self.variablesEMG.counterEMG3[0] = 0
                self.variablesEMG.counterEMG3[0] += 1
                        
        if musclename == "RightGluteus" or musclename == "LeftGluteus":
            if contractions < 1 :
                
                if self.variablesEMG.counterEMG1[0] == cyclestowait-1:
                    print("Nao")
                    self.NAO ='10'
                    if self.variablesEMG.phase == 1:
                        self.NAO ='11'
                    if self.variablesEMG.phase == 2:
                        self.NAO ='12'
                    if self.variablesEMG.phase == 3:
                        self.NAO ='13'
                    if self.variablesEMG.phase == 4:
                        self.NAO ='14'
                    
                    self.variablesEMG.counterEMG1[0] = 0
                self.variablesEMG.counterEMG1[0] += 1
        if musclename == "RightHamstrings" or musclename == "LeftHamstrings" :
            if contractions < 1 :
            
                if self.variablesEMG.counterEMG1[0] == cyclestowait-1:
                    
                    self.NAO ='15'
                    if self.variablesEMG.phase == 1:
                        self.NAO ='16'
                    if self.variablesEMG.phase == 2:
                        self.NAO ='17'
                    if self.variablesEMG.phase == 3:
                        self.NAO ='18'
                    if self.variablesEMG.phase == 4:
                        self.NAO ='19'
                    
                    self.variablesEMG.counterEMG4[0] = 0
                self.variablesEMG.counterEMG4[0] += 1

    def contractionWRONG(contractions,musclename,phase):
        if musclename == "RightGluteus" or musclename == "LeftGluteus":
            if contractions > 1 :
                
                if self.variablesEMG.counterEMG1[0] == cyclestowait-1:
                    print("Nao")
                    self.NAO ='20'
                    if self.variablesEMG.phase == 1:
                        self.NAO ='21'
                    if self.variablesEMG.phase == 2:
                        self.NAO ='22'
                    if self.variablesEMG.phase == 3:
                        self.NAO ='23'
                    if self.variablesEMG.phase == 4:
                        self.NAO ='24'
                    
                    self.variablesEMG.counterEMG1[0] = 0
                self.variablesEMG.counterEMG1[0] += 1

        if musclename == "RightQuadriceps" or musclename == "LeftQuadriceps":
            if contractions > 1 :
                
                if self.variablesEMG.counterEMG2[0] == cyclestowait-1:
                    self.NAO ='25'
                    if self.variablesEMG.phase == 1:
                        self.NAO ='26'
                        
                    if self.variablesEMG.phase == 2:
                        self.NAO ='27'
                    if self.variablesEMG.phase == 3:
                        self.NAO ='28'
                    if self.variablesEMG.phase == 4:
                        self.NAO ='29'   
                    
                    self.variablesEMG.counterEMG2[0] = 0
                self.variablesEMG.counterEMG2[0] += 1
                
        if musclename == "RightTriceps" or musclename == "LeftTriceps" :
            if contractions > 1 :
                
                if self.variablesEMG.counterEMG3[0] == cyclestowait-1:
                    self.NAO ='30'
                    if self.variablesEMG.phase == 1:
                        self.NAO ='31'
                    if self.variablesEMG.phase == 2:
                        self.NAO ='32'
                    if self.variablesEMG.phase == 3:
                        self.NAO ='33'
                    if self.variablesEMG.phase == 4:
                        self.NAO ='34'
                       
                    self.variablesEMG.counterEMG3[0] = 0
                self.variablesEMG.counterEMG3[0] += 1
                
        if musclename == "RightHamstrings" or musclename == "LeftHamstrings" :
            if contractions > 1 :
            
                if self.variablesEMG.counterEMG4[0] == cyclestowait-1:
                    
                    self.NAO ='35'
                    if self.variablesEMG.phase == 1:
                        self.NAO ='36'              
                    if self.variablesEMG.phase == 2:
                        self.NAO ='37'
                    if self.variablesEMG.phase == 3:
                        self.NAO ='38'
                    if self.variablesEMG.phase == 4:
                        self.NAO ='39'
                    
                    self.variablesEMG.counterEMG4[0] = 0
                self.variablesEMG.counterEMG4[0] += 1

    def ApplyCPWalkerIndex(phase, muscleName, contractionlist):


        self.variablesEMG.phase = phase
        changeOfPhase, numberofChanges = self.knowPhaseChange(self.variablesEMG.phase)
        print("number of changes :")
        print(numberofChanges)
        
        
        #PHASE 1
        contractions = self.countContractions(contractionlist[0:changeOfPhase[0]-1])
        if muscleName == "RightGluteus" or muscleName == "LeftGluteus":
            self.nocontractionWRONG(contractions,muscleName,1)
        if muscleName == "RightQuadriceps" or muscleName == "LeftQuadriceps":
            self.contractionWRONG(contractions,muscleName,1)
        if muscleName == "RightTriceps" or muscleName == "LeftTriceps":
            self.contractionWRONG(contractions,muscleName,1)
        if muscleName == "RightHamstrings" or muscleName == "LeftHamstrings":
            self.nocontractionWRONG(contractions,muscleName,1)
        #PHASE 2
        contractions = self.countContractions(contractionlist[changeOfPhase[0]:changeOfPhase[1]-1])
        if muscleName == "RightGluteus" or muscleName == "LeftGluteus":
            self.nocontractionWRONG(contractions,muscleName,2)
        if muscleName == "RightQuadriceps" or muscleName == "LeftQuadriceps":
            self.nocontractionWRONG(contractions,muscleName,2)
        if muscleName == "RightTriceps" or muscleName == "LeftTriceps":
            self.contractionWRONG(contractions,muscleName,2)
        if muscleName == "RightHamstrings" or muscleName == "LeftHamstrings":
            self.contractionWRONG(contractions,muscleName,2)
                
        #PHASE 3
        contractions = self.countContractions(contractionlist[changeOfPhase[1]:changeOfPhase[2]-1])
        if muscleName == "RightGluteus" or muscleName == "LeftGluteus":
            self.contractionWRONG(contractions,muscleName,3)
        if muscleName == "RightQuadriceps" or muscleName == "LeftQuadriceps":
            self.contractionWRONG(contractions,muscleName,3)
        if muscleName == "RightTriceps" or muscleName == "LeftTriceps":
            self.nocontractionWRONG(contractions,muscleName,3)
        if muscleName == "RightHamstrings" or muscleName == "LeftHamstrings":
            self.contractionWRONG(contractions,muscleName,3)
        
        #PHASE 4
        contractions = self.countContractions(contractionlist[changeOfPhase[2]:len(self.variablesEMG.phase)-1])
        if muscleName == "RightGluteus" or muscleName == "LeftGluteus":
            self.contractionWRONG(contractions,muscleName,4)
        if muscleName == "RightQuadriceps" or muscleName == "LeftQuadriceps":
            self.nocontractionWRONG(contractions,muscleName,4)
        if muscleName == "RightTriceps" or muscleName == "LeftTriceps":
            self.contractionWRONG(contractions,muscleName,4)
        if muscleName == "RightHamstrings" or muscleName == "LeftHamstrings":
            self.contractionWRONG(contractions,muscleName,4)


    def threshold_from_data(emg):
      
        mean = 0
        for k in range(0 ,len(emg)-1):
            mean+=emg[k]
        th = (mean/len(emg)) *1.5
        return th


    def apply_threshold(self,emg):

        th = threshold_from_data(emg)
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
            else : contraction[k] = 0 
            
        return contraction,th
          

    def Muscle(self,emg,musclename,CPWalkerIndex):


        decision,th = apply_threshold(emg_filtered*10000) #0,1 value
        self.ApplyCPWalkerIndex(CPWalkerIndex, MuscleName, decision)

        return(decision)






    
















    def start(self):

        self.go_ON = True






        

    


            




        




if __name__ == '__main__':
    main2()
