# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI.ui'
#
# Created: Mon Nov 24 23:34:30 2014
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

import os
import sys
import time
#import moreTesting
from PyQt4 import QtCore, QtGui
import testingtime 
#import temperature
#import countdown

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s
    


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(320, 240)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.Yes = QtGui.QPushButton(self.centralwidget)
        self.Yes.setGeometry(QtCore.QRect(20, 170, 81, 31))
        self.Yes.setObjectName(_fromUtf8("Yes"))
        self.Welcome = QtGui.QLabel(self.centralwidget)
        self.Welcome.setGeometry(QtCore.QRect(70, 0, 181, 21))
        self.Welcome.setObjectName(_fromUtf8("Welcome"))
        self.No = QtGui.QPushButton(self.centralwidget)
        self.No.setGeometry(QtCore.QRect(120, 170, 81, 31))
        self.No.setObjectName(_fromUtf8("No"))
        self.START = QtGui.QLabel(self.centralwidget)
        self.START.setGeometry(QtCore.QRect(230, 140, 71, 20))
        self.START.setObjectName(_fromUtf8("START"))
        self.CurrentTemp = QtGui.QLabel(self.centralwidget)
        self.CurrentTemp.setGeometry(QtCore.QRect(210, 20, 111, 20))
        self.CurrentTemp.setObjectName(_fromUtf8("CurrentTemp"))
        self.StartTime_Display = QtGui.QLineEdit(self.centralwidget)
        self.StartTime_Display.setGeometry(QtCore.QRect(210, 160, 101, 31))
        self.StartTime_Display.setObjectName(_fromUtf8("StartTime_Display"))
        self.CurrentTemp_Display = QtGui.QLineEdit(self.centralwidget)
        self.CurrentTemp_Display.setGeometry(QtCore.QRect(210, 40, 101, 31))
        self.CurrentTemp_Display.setObjectName(_fromUtf8("CurrentTemp_Display"))
        self.RemainingTime_Display = QtGui.QLineEdit(self.centralwidget)
        self.RemainingTime_Display.setGeometry(QtCore.QRect(210, 100, 101, 31))
        self.RemainingTime_Display.setObjectName(_fromUtf8("RemainingTime_Display"))
        self.RemainingTime = QtGui.QLabel(self.centralwidget)
        self.RemainingTime.setGeometry(QtCore.QRect(210, 80, 111, 20))
        self.RemainingTime.setObjectName(_fromUtf8("RemainingTime"))
        self.Results_Display = QtGui.QPlainTextEdit(self.centralwidget)
        self.Results_Display.setGeometry(QtCore.QRect(10, 30, 191, 121))
        self.Results_Display.setObjectName(_fromUtf8("plainTextEdit"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
		
		
        self.retranslateUi(MainWindow,'')
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

	#self.update_current_temp()
	self.update_start_time()
	#self.update_remaining_time()
	#self.update_Results_Display()

    def retranslateUi(self, MainWindow, instructions):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.Yes.setText(QtGui.QApplication.translate("MainWindow", "Yes", None, QtGui.QApplication.UnicodeUTF8))
        self.Welcome.setText(QtGui.QApplication.translate("MainWindow", "Welcome SpartanBrew User", None, QtGui.QApplication.UnicodeUTF8))
        self.No.setText(QtGui.QApplication.translate("MainWindow", "No", None, QtGui.QApplication.UnicodeUTF8))
        self.START.setText(QtGui.QApplication.translate("MainWindow", "Start Time", None, QtGui.QApplication.UnicodeUTF8))
        self.CurrentTemp.setText(QtGui.QApplication.translate("MainWindow", "Current Temp(F)", None, QtGui.QApplication.UnicodeUTF8))
        self.RemainingTime.setText(QtGui.QApplication.translate("MainWindow", "Remaining Time", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("MainWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
	
	self.StartTime_Display.setText(str(0))
	self.CurrentTemp_Display.setText(str(0))
	self.RemainingTime_Display.setText(str(0))
	#self.Results_Display.insertPlainText(instructions)
	self.Results_Display.insertPlainText(instructions)
        self.Yes.clicked.connect(self.Yesbutton_clicked)
	a = self.askforloop()
		
    def askforloop(self):
	questions = ['Add 6 Gallons of Water', 
		'Add Rice Extract', 
		'Add Willamette Hops', 
		'Add Malt Extract',
		'Add Whirlfloc Tablet',
		'Please Remove Hops Bag',
		'Please Remove Yeast']
	for i in range(0,7):
		retranslateUi(self, MainWindow, 'hi')
	

    def update_start_time(self):
	    self.StartTime_Display.setText(testingtime.timeString)	
    def Yesbutton_clicked(self):
	    sender = self.Results_Display
	    sender.clear()
	    sender.insertPlainText("+ You added water")
	    

'''
    def update_printInstruction(self):
		self.Results_Display.setText(moreTesting.printInstruction.acknowledgement)

    def update_current_temp(self):
	    self.CurrentTemp_Display.setText(temperature.x)

    def update_remaining_time(self):
	    self.RemainingTime_Display.setText(countdown.cd)
'''
  
class ControlMainWindow(QtGui.QMainWindow):
	def __init__(self, parent=None):
		super(ControlMainWindow, self).__init__(parent)
		self.ui = Ui_MainWindow()
		#self.showFullScreen()
		self.ui.setupUi(self)


if __name__=="__main__":
	app = QtGui.QApplication(sys.argv)
	mySW = ControlMainWindow()
	mySW.show()
	sys.exit(app.exec_())


