# -*- coding: utf-8 -*-import sys
import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import*
from PyQt4.QtGui import*
import ctypes

class IntroductionWindow(QtGui.QMainWindow):


    def __init__(self):
        super(IntroductionWindow,self).__init__()
        self.init_ui()
         
    def init_ui(self):
        #Window Title
        self.setWindowTitle("NAO-CPWalker Therapy")
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
        self.label_background.setPixmap(QtGui.QPixmap("gui/img/Introduction_background.png"))
        self.label_background.setScaledContents(True)

        #Setting Close Image 
        self.close1=QtGui.QLabel(self)
        self.close1.setGeometry(QtCore.QRect(self.winsize_h*0.93,self.winsize_v*0.05,self.winsize_h*0.045,self.winsize_h*0.045))
        Icon1=QtGui.QPixmap("gui/img/closebtn.PNG")
        Icon_resize1= Icon1.scaled(self.winsize_h*0.045,self.winsize_h*0.045,QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
        self.close1.setPixmap(Icon_resize1)
        # Setting Intruction Image
        self.start=QtGui.QLabel(self)
        self.start.setGeometry(QtCore.QRect(self.winsize_h*0.83,self.winsize_v*0.815,self.winsize_h*0.1,self.winsize_h*0.1))
        start=QtGui.QPixmap("gui/img/start.png")
        start_resized= start.scaled(self.winsize_h*0.1,self.winsize_h*0.1,QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
        self.start.setPixmap(start_resized)

        # Setting the buttons of the interface:
        self.controlButtons={}
        #Close Button
        self.controlButtons['close'] = QtGui.QCommandLinkButton(self)
        self.controlButtons['close'].setIconSize(QSize(0,0))
        self.controlButtons['close'].setGeometry(QtCore.QRect(self.winsize_h*0.93,self.winsize_v*0.05,self.winsize_h*0.045,self.winsize_h*0.045)) 
        
        # Introduction Button:

        self.controlButtons['Introduction'] = QtGui.QCommandLinkButton(self)
        self.controlButtons['Introduction'].setIconSize(QSize(0,0))
        self.controlButtons['Introduction'].setGeometry(QtCore.QRect(self.winsize_h*0.83,self.winsize_v*0.815,self.winsize_h*0.1,self.winsize_h*0.1)) 



        # Setting the input text for Patient data
        self.DataDisplay = {}
        #Name Display
        self.DataDisplay['name'] = QtGui.QLineEdit(self)
        self.DataDisplay['name'].setStyleSheet("font-size:35px; Arial")
        self.DataDisplay['name'].setGeometry(QtCore.QRect(self.winsize_h*0.615,self.winsize_v*0.435,self.winsize_h*0.3 ,self.winsize_h*0.03))
        #Age display
        self.DataDisplay['Age'] = QtGui.QLineEdit(self)
        self.DataDisplay['Age'].setStyleSheet("font-size:35px; Arial")
        self.DataDisplay['Age'].setGeometry(QtCore.QRect(self.winsize_h*0.615,self.winsize_v*0.515,self.winsize_h*0.3 ,self.winsize_h*0.03))   
        # Gender display
        self.DataDisplay['Gender'] = QtGui.QComboBox(self)
        self.DataDisplay['Gender'].setStyleSheet("font-size:35px; Arial")
        self.DataDisplay['Gender'].setGeometry(QtCore.QRect(self.winsize_h*0.615,self.winsize_v*0.605,self.winsize_h*0.3 ,self.winsize_h*0.03))   
        self.DataDisplay['Gender'].addItem("Masculino")
        self.DataDisplay['Gender'].addItem("Femenino")
        # Pathology Display
        self.DataDisplay['Pathology'] = QtGui.QLineEdit(self)
        self.DataDisplay['Pathology'].setStyleSheet("font-size:35px; Arial")
        self.DataDisplay['Pathology'].setGeometry(QtCore.QRect(self.winsize_h*0.615,self.winsize_v*0.695,self.winsize_h*0.3 ,self.winsize_h*0.03))   
        # ID Display
        self.DataDisplay['ID'] = QtGui.QLineEdit(self)
        self.DataDisplay['ID'].setStyleSheet("font-size:35px; Arial")
        self.DataDisplay['ID'].setGeometry(QtCore.QRect(self.winsize_h*0.615,self.winsize_v*0.775,self.winsize_h*0.3 ,self.winsize_h*0.03))   
        

        #self.show()
        self.connectCloseButton();
        #self.connectBWSButton()
        
    def connectCloseButton(self):
        self.controlButtons['close'].clicked.connect(self.close)       
        
    def connectIntroductionButton(self,f):
        self.controlButtons['Introduction'].clicked.connect(f)

    def get_patient_data(self):

        name      = str(self.DataDisplay['name'].text())
        age       = str(self.DataDisplay['Age'].text())
        gender    = str(self.DataDisplay['Gender'].currentText())
        pathology = str(self.DataDisplay['Pathology'].text())
        id_number = str(self.DataDisplay['ID'].text())

        self.patient = {'name' : name ,'id' : id_number,'age':age,'gender':gender,'pathology': pathology}
        return(self.patient)



def test():
    app=QtGui.QApplication(sys.argv)
    GUI=IntroductionWindow()
    sys.exit(app.exec_())
#A=test()

if __name__ == '__main__':
    app=QtGui.QApplication(sys.argv)
    GUI=ModalityWindow()
    sys.exit(app.exec_())
