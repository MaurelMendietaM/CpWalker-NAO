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
        self.label_background.setPixmap(QtGui.QPixmap("img/Back.png"))

        #Setting Close Image 
        self.close1=QtGui.QLabel(self)
        self.close1.setGeometry(QtCore.QRect(self.winsize_h*0.93,self.winsize_v*0.05,self.winsize_h*0.045,self.winsize_h*0.045))
        Icon1=QtGui.QPixmap("img/closebtn.PNG")
        Icon_resize1= Icon1.scaled(self.winsize_h*0.045,self.winsize_h*0.045,QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
        self.close1.setPixmap(Icon_resize1)

        #Setting HR Image

        self.heart=QtGui.QLabel(self)
        self.heart.setGeometry(QtCore.QRect(self.winsize_h*0.05,self.winsize_v*0.33,self.winsize_h*0.04,self.winsize_h*0.04))
        heart=QtGui.QPixmap("img/heart.PNG")
        heart= heart.scaled(self.winsize_h*0.04,self.winsize_h*0.04,QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
        self.heart.setPixmap(heart)

        self.heart_label=QtGui.QLabel(self)
        self.heart_label.setGeometry(QtCore.QRect(self.winsize_h*0.24,self.winsize_v*0.34,self.winsize_h*0.25,self.winsize_h*0.03))
        heart_label=QtGui.QPixmap("img/rect5562.PNG")
        heart_label= heart_label.scaled(self.winsize_h*0.3,self.winsize_h*0.04,QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
        self.heart_label.setPixmap(heart_label)

        #Setting posture Image

        self.posture=QtGui.QLabel(self)
        self.posture.setGeometry(QtCore.QRect(self.winsize_h*0.05,self.winsize_v*0.43,self.winsize_h*0.04,self.winsize_h*0.04))
        posture =QtGui.QPixmap("img/posture.PNG")
        posture = posture.scaled(self.winsize_h*0.04,self.winsize_h*0.04,QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
        self.posture.setPixmap(posture)

        self.posture_label=QtGui.QLabel(self)
        self.posture_label.setGeometry(QtCore.QRect(self.winsize_h*0.24,self.winsize_v*0.44,self.winsize_h*0.25,self.winsize_h*0.03))
        posture_label=QtGui.QPixmap("img/rect5562.PNG")
        posture_label= heart_label.scaled(self.winsize_h*0.3,self.winsize_h*0.04,QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
        self.posture_label.setPixmap(posture_label)

        # Settings patient name
        self.Patient = {}
        self.Patient['name'] = QtGui.QLabel(self)
        self.Patient['name'].setText("Nombre del paciente :")
        self.Patient['name'].setStyleSheet("font-size:30px; Arial")
        self.Patient['name'].setGeometry(QtCore.QRect(self.winsize_h*0.05,self.winsize_v*0.90,self.winsize_h*0.25 ,self.winsize_h*0.02))

        self.Patient = {}
        self.Patient['id'] = QtGui.QLabel(self)
        self.Patient['id'].setText("ID del paciente :")
        self.Patient['id'].setStyleSheet("font-size:30px; Arial")
        self.Patient['id'].setGeometry(QtCore.QRect(self.winsize_h*0.05,self.winsize_v*0.93,self.winsize_h*0.25 ,self.winsize_h*0.02))

        
        #Setting priority texts
        self.PriorityText = {}
        self.PriorityText['name'] = QtGui.QLabel(self)
        self.PriorityText['name'].setText("Ingresa prioridad de realimentacion :")
        self.PriorityText['name'].setStyleSheet("font-size:40px; Arial")
        self.PriorityText['name'].setGeometry(QtCore.QRect(self.winsize_h*0.05,self.winsize_v*0.1,self.winsize_h*0.25 ,self.winsize_h*0.02))

        self.Options = {}
        self.Options['name_first'] = QtGui.QLabel(self)
        self.Options['name_first'].setText("1:")
        self.Options['name_first'].setStyleSheet("font-size:40px; Arial")
        self.Options['name_first'].setGeometry(QtCore.QRect(self.winsize_h*0.05,self.winsize_v*0.15,self.winsize_h*0.05 ,self.winsize_h*0.02))

        self.Options = {}
        self.Options['name_second'] = QtGui.QLabel(self)
        self.Options['name_second'].setText("2:")
        self.Options['name_second'].setStyleSheet("font-size:40px; Arial")
        self.Options['name_second'].setGeometry(QtCore.QRect(self.winsize_h*0.05,self.winsize_v*0.20,self.winsize_h*0.05 ,self.winsize_h*0.02))

        #Priority Options
        self.Options['read_first'] = QtGui.QComboBox(self)
        self.Options['read_first'].setStyleSheet("font-size:35px; Arial")
        self.Options['read_first'].setGeometry(QtCore.QRect(self.winsize_h*0.067,self.winsize_v*0.15,self.winsize_h*0.15 ,self.winsize_h*0.02))   
        self.Options['read_first'].addItem("EMG")
        self.Options['read_first'].addItem("Postura") 

        self.Options['read_second'] = QtGui.QComboBox(self)
        self.Options['read_second'].setStyleSheet("font-size:35px; Arial")
        self.Options['read_second'].setGeometry(QtCore.QRect(self.winsize_h*0.067,self.winsize_v*0.20,self.winsize_h*0.15 ,self.winsize_h*0.02))   
        self.Options['read_second'].addItem("Postura")
        self.Options['read_second'].addItem("EMG") 

        # Sensor labels and text

        self.ECG = {}
        self.ECG['name'] = QtGui.QLabel(self)
        self.ECG['name'].setText("Ritmo Cardiaco:")
        self.ECG['name'].setStyleSheet("font-size:40px; Arial")
        self.ECG['name'].setGeometry(QtCore.QRect(self.winsize_h*0.1,self.winsize_v*0.35,self.winsize_h*0.3 ,self.winsize_h*0.02))

        self.ECG['lcd'] = QtGui.QLCDNumber(self)
        self.ECG['lcd'].setGeometry(QtCore.QRect(self.winsize_h*0.26,self.winsize_v*0.34,self.winsize_h*0.1 ,self.winsize_h*0.03))

        self.Inclination = {}
        self.Inclination['name'] = QtGui.QLabel(self)
        self.Inclination['name'].setText("Grado de inclinacion:")
        self.Inclination['name'].setStyleSheet("font-size:40px; Arial")
        self.Inclination['name'].setGeometry(QtCore.QRect(self.winsize_h*0.1,self.winsize_v*0.45,self.winsize_h*0.3 ,self.winsize_h*0.02))

        self.Inclination['lcd'] = QtGui.QLCDNumber(self)
        self.Inclination['lcd'].setGeometry(QtCore.QRect(self.winsize_h*0.26,self.winsize_v*0.44,self.winsize_h*0.1 ,self.winsize_h*0.03))

        # Setting the buttons of the interface:
        self.controlButtons={}
        #Close Button
        self.controlButtons['close'] = QtGui.QCommandLinkButton(self)
        self.controlButtons['close'].setIconSize(QSize(0,0))
        self.controlButtons['close'].setGeometry(QtCore.QRect(self.winsize_h*0.93,self.winsize_v*0.05,self.winsize_h*0.045,self.winsize_h*0.045)) 
        


       
        self.show()
        self.setPatientName("Nathalia Cespedes Gomez", "1026295355")

        self.connectCloseButton();
        

    def connectSpeechButton(self,f):
        self.controlButtons['speech'].clicked.connect(f) 

    def connectCloseButton(self):
        self.controlButtons['close'].clicked.connect(self.close)
        self.onClose.emit()

    def setPatientName(self, value, id_patient):

        value =str(value) 
        self.SetPatient = {}
        self.SetPatient['name'] = QtGui.QLabel(self)
        self.SetPatient['name'].setText(value)
        self.SetPatient['name'].setStyleSheet("font-size:30px; Arial")
        self.SetPatient['name'].setGeometry(QtCore.QRect(self.winsize_h*0.18,self.winsize_v*0.90,self.winsize_h*0.25 ,self.winsize_h*0.02))
        self.SetPatient['name'].show()

        id_patient =str(id_patient)
        self.SetPatient['id'] = QtGui.QLabel(self)
        self.SetPatient['id'].setText(id_patient)
        self.SetPatient['id'].setStyleSheet("font-size:30px; Arial")
        self.SetPatient['id'].setGeometry(QtCore.QRect(self.winsize_h*0.18,self.winsize_v*0.93,self.winsize_h*0.25 ,self.winsize_h*0.02))
        self.SetPatient['id'].show()





def test():
    app=QtGui.QApplication(sys.argv)
    GUI=TherapyWindow()
    sys.exit(app.exec_())
A=test()       


