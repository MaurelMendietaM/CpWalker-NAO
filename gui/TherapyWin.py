# -*- coding: utf-8 -*-import sys
import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import*
from PyQt4.QtGui import*
import ctypes

class TherapyWindow(QtGui.QMainWindow):

    onClose = QtCore.pyqtSignal()

    def __init__(self):
        super(TherapyWindow,self).__init__()
        self.init_ui()
         
    def init_ui(self):
        #Window Title
        self.setWindowTitle("NAO-CPWalker TherapyWindow")
        #Window Size
        self.user32=ctypes.windll.user32
        self.screensize=self.user32.GetSystemMetrics(0), self.user32.GetSystemMetrics(1),
        #Resizing MainWindoe to a percentage of the total
        self.winsize_h=int(self.screensize[0])
        self.winsize_v=int(self.screensize[1])
        self.resize(self.winsize_h,self.winsize_v)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        # Setting the Background Image

        #setting backgroung image
        self.label_background=QtGui.QLabel(self)
        self.label_background.setGeometry(QtCore.QRect(0,0,self.winsize_h,self.winsize_v))
        self.label_background.setScaledContents(True)
        self.label_background.setPixmap(QtGui.QPixmap("gui/img/Back.png"))

        #Setting Close Image 
        self.close1=QtGui.QLabel(self)
        self.close1.setGeometry(QtCore.QRect(self.winsize_h*0.93,self.winsize_v*0.05,self.winsize_h*0.045,self.winsize_h*0.045))
        Icon1=QtGui.QPixmap("gui/img/closebtn.PNG")
        Icon_resize1= Icon1.scaled(self.winsize_h*0.045,self.winsize_h*0.045,QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
        self.close1.setPixmap(Icon_resize1)

       

        self.connectCloseButton();
        self.connectVolumeSlider(self.get_Volume)

    def connectSpeechButton(self,f):
        self.controlButtons['speech'].clicked.connect(f) 

    def connectCloseButton(self):
        self.controlButtons['close'].clicked.connect(self.close)
        self.onClose.emit()

    def connectVolumeSlider(self,f):
        self.volume.valueChanged.connect(f)

    def get_Volume(self):
        self.volume_data = self.volume.value()
        self.VolumeText['lcd'].display(self.volume_data)

    def send_Volume(self):
        self.volume_data = self.volume.value()
        return(self.volume_data)

    def connectElephantButton(self,f): 
        self.controlButtons['Elephant'].clicked.connect(f) 

    def connectMouseButton(self,f): 
        self.controlButtons['Mouse'].clicked.connect(f)

    def connectButterflyButton(self,f): 
        self.controlButtons['butterfly'].clicked.connect(f)

    def connectMonkeyButton(self,f): 
        self.controlButtons['monkey'].clicked.connect(f)

    def get_speech(self):

        speech  = str(self.SpeechText['read'].text())
        return(speech)

    def connectRightButton(self,f):
        self.controlButtons['yes'].clicked.connect(f)


def test():
    app=QtGui.QApplication(sys.argv)
    GUI=PlayWindow()
    sys.exit(app.exec_())
#A=test()       


