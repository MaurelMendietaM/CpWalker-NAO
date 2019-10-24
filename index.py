#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 17:23:31 2017

@author: pi
"""

import threading

import gui.IntroductionWin as Introduction   
import gui.SettingsWin as Settings  
import gui.PlayWin as Play
import gui.TherapyWin as MainTherapy
import robotController.NAO_controller as controller
import lib.SensorManager as manager 
from PyQt4 import QtCore, QtGui
import time
import sys
import random


class NAO_CpWalker(object):
    
    def __init__(self, settings = {'UseSensors': True,
                                   'UseRobot'  : False,
                                   'RobotIp'   : "192.168.1.75.",
                                   'RobotPort' : 9559
                                   
                                  }):

        #load settings
        self.settings = settings
        self.mode = None
        #Interface Objects
        self.settingsWin = Settings.SettingsWindow()
        self.IntroductionWin = Introduction.IntroductionWindow()
        self.PlayWin = Play.PlayWindow()
        self.therapyWin = MainTherapy.TherapyWindow()

        


        # Load signals

        #therapy win interface object
        

        self.settingsWin.connectIntroductionButton(self.go_to_Introduction) 
        self.settingsWin.connectTherapyButton(self.start_sessionSettings)

        self.therapyWin.connectStartButton(self.onStartThreads)
        self.therapyWin.connectStopButton(self.shutdown)
        self.settingsWin.show()  

        
        

    def go_to_Introduction(self):

        
        
        m = self.settingsWin.get_settings_data()


        self.settings['RobotIp'] = m['ip']

        if self.settings['UseRobot']:
            #self.RobotCaptureThread = RobotCaptureThread(interface = self)
            self.robotController = controller.RobotController({
                                                                 'name'       : "NAO",
                                                                 'ip'         : self.settings['RobotIp'],
                                                                 'port'       : self.settings['RobotPort'],
                                                                 'UseSpanish' : True,
                                                                 'MotivationTime': 300000000,
                                                                 'HeartRate_Lim': 120,
                                                                 'Cerv_Lim': 0,
                                                                 'Thor_Lim': 0
                                                              })

        self.IntroductionWin.show()
        self.settingsWin.hide()
        self.IntroductionWin.connectIntroductionButton(self.on_startIntroduction)

    def on_startIntroduction(self):

        patient = self.IntroductionWin.get_patient_data()
        self.robotController.patient = patient
        self.robotController.tracking_faces()
        self.robotController.start_Introduction()
        self.robotController.launch_SoundTracker()
        self.robotController.load_selfPresentation()
        self.PlayWin.show()
        self.robotController.load_patientPresentation()

        # Set Volume of the robot
        self.IntroductionWin.hide()
        #self.shutdown()

        #Set animals game
        self.PlayWin.connectElephantButton(self.elephant_Game)
        self.PlayWin.connectMouseButton(self.mouse_Game)
        self.PlayWin.connectButterflyButton(self.butterfly_Game)
        self.PlayWin.connectMonkeyButton(self.monkey_Game)

        #Speech production
        self.PlayWin.connectSpeechButton(self.speech_Production)

        # Set behaviors to right answer
        self.PlayWin.connectRightButton(self.robotController.load_Right)

    
    def speech_Production(self):
        volume = self.PlayWin.send_Volume()
        volume = ((float(volume))/100)*1.45

        print(volume)

        self.robotController.setVolume(volume)

        say = self.PlayWin.get_speech()

        self.robotController.load_Speech(say)


    def elephant_Game(self):

        self.robotController.load_ElephantBehavior()

    def mouse_Game(self):

        self.robotController.load_MouseBehavior()

    def monkey_Game(self):

        self.robotController.load_gorillaBehavior()

    def butterfly_Game(self):

        self.robotController.load_butterflyBehavior()


    def load_Speech(self):
        pass

    def start_sessionSettings(self):
    	print('Here')
        m = self.settingsWin.get_settings_data()
        battery = "85%"

        self.settings['RobotIp'] = m['ip']

        if self.settings['UseRobot']:
            self.RobotCaptureThread = RobotCaptureThread(interface = self)
            self.robotController = controller.RobotController({
                                                                 'name'       : "NAO",
                                                                 'ip'         : self.settings['RobotIp'],
                                                                 'port'       : self.settings['RobotPort'],
                                                                 'UseSpanish' : True,
                                                                 'MotivationTime': 300000000,
                                                                 'HeartRate_Lim': 120,
                                                                 'Cerv_Lim': 0,
                                                                 'Thor_Lim': 0
                                                              })
        self.therapyWin.show()
        self.therapyWin.sensorsData(m['ip'], battery)

        self.sensor_Settings()

    def onStartThreads(self):

    	self.SensorUpdateThread.start()
    	self.SensorAcquisitionThread.start()

    def sensor_Settings(self):

        self.SensorUpdateThread  = SensorUpdateThread(f =self.sensor_update, sample = 1)

        self.Manager = manager.SensorManager( ecg   = {"port":'COM3', "sample":1},
                                              EMG   = {"MuscletoUse": "1"})

        self.SensorAcquisitionThread = SensorAcquisitionThread(f=self.Manager.update_data, sample =1)

        if self.settings['UseSensors']:
            
            # set sensors
            self.Manager.set_sensors(ecg = True, emg=True)
            self.Manager.launch_Sensors()
            time.sleep(5)

    def sensor_update(self):

    	if self.settings['UseSensors']:
    		self.data = self.Manager.get_Data()
    		print('Index')
    		print(self.data)
    		self.therapyWin.update_display_data(d = { 'hr' :self.data['ecg'],
                                                      'Inclination' : self.data['emg']['contractions']
                                                      }
                                    			)
    		self.therapyWin.onSensorUpdate.emit()

    	else:
    		self.data = self.Manager.get_data()
    		self.therapyWin.update_display_data(d = {
                                                        'hr' :self.data['ecg'],
                                                        'Inclination' : self.data['emg']['contractions']
                                                      })
    		self.therapyWin.onSensorUpdate.emit()
        





        



    def shutdown(self):
    	self.SensorUpdateThread.shutdown()
    	self.SensorAcquisitionThread.shutdown()
        self.robotController.shutdown()


      

class RobotCaptureThread(QtCore.QThread):
    def __init__(self, parent = None, sample = 10, interface = None):
        super(RobotCaptureThread,self).__init__()
        self.Ts = sample
        self.ON = True
        self.interface = interface
        
        
        
    def run(self):
        #self.interface.robotController.posture.goToPosture("StandZero", 1.0)
        while self.ON:
            d = self.interface.ManagerRx.get_data()
            self.interface.robotController.set_data(d)
            time.sleep(self.Ts)
            
                
    def shutdown(self):
        self.ON = False

class SensorUpdateThread(QtCore.QThread):

     def __init__(self, parent = None, f = None, sample = 1):
        super(SensorUpdateThread,self).__init__()
        self.f = f
        self.Ts = sample
        self.ON = True
        
     def run(self):

        if self.f:
            while self.ON:
                self.f()
                time.sleep(self.Ts)

     def shutdown(self):
        self.ON = False

class SensorAcquisitionThread(QtCore.QThread):

	def __init__(self, parent = None, f = None, sample = 1):
		super(SensorAcquisitionThread,self).__init__()
		self.f = f
		self.Ts = sample
		self.ON = True

	def run(self):
		if self.f:
			while self.ON:
				self.f()
				time.sleep(self.Ts)

	def shutdown(self):
		self.ON = False

    #def shutdown(self):
    	#self.ON = False

if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	a =NAO_CpWalker()
	sys.exit(app.exec_())
