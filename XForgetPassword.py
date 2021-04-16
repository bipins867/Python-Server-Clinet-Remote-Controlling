from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import LoginScreen as lc
import XprtLoginControl as xlc
import XprtClientScript2 as xcs
import threading
import DataShare as ds
from tkinter import filedialog
import numpy as np
from PIL import Image,ImageTk
import cv2
import random
import RControl as rc
import AssembleData as ad
import KMController as km
import os
import pyperclip as pc
import GradientFrame as gf
import time
import sys
import LoginScreen as lc

class ForgetPassword():
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(274, 335)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 20, 191, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(22)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setMouseTracking(True)
        self.label.setMidLineWidth(1)
        self.label.setObjectName("label")
        self.editUserName = QtWidgets.QLineEdit(self.centralwidget)
        self.editUserName.setGeometry(QtCore.QRect(20, 70, 113, 20))
        self.editUserName.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.editUserName.setObjectName("editUserName")
        self.btnOk = QtWidgets.QPushButton(self.centralwidget)
        self.btnOk.setGeometry(QtCore.QRect(180, 280, 75, 23))
        self.btnOk.setObjectName("btnOk")
        self.labelSeqQ = QtWidgets.QLabel(self.centralwidget)
        self.labelSeqQ.setGeometry(QtCore.QRect(20, 100, 171, 61))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.labelSeqQ.setFont(font)
        self.labelSeqQ.setWordWrap(True)
        self.labelSeqQ.setObjectName("labelSeqQ")
        self.editSeqA = QtWidgets.QLineEdit(self.centralwidget)
        self.editSeqA.setGeometry(QtCore.QRect(20, 180, 113, 20))
        self.editSeqA.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.editSeqA.setObjectName("editSeqA")
        self.editPassword = QtWidgets.QLineEdit(self.centralwidget)
        self.editPassword.setGeometry(QtCore.QRect(20, 230, 113, 20))
        self.editPassword.setObjectName("editPassword")
        self.btnLoginSignUp = QtWidgets.QPushButton(self.centralwidget)
        self.btnLoginSignUp.setGeometry(QtCore.QRect(20, 280, 81, 23))
        self.btnLoginSignUp.setObjectName("btnLoginSignUp")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)



    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Forget Password"))
        self.editUserName.setPlaceholderText(_translate("MainWindow", "User Name"))
        self.btnOk.setText(_translate("MainWindow", "Ok"))
        self.labelSeqQ.setText(_translate("MainWindow", "Sequrity Question"))
        self.editSeqA.setPlaceholderText(_translate("MainWindow", "Sequrity Answer"))
        self.editPassword.setPlaceholderText(_translate("MainWindow", "Password"))
        self.btnLoginSignUp.setText(_translate("MainWindow", "Login / SignUp"))



    def funOk1(self):
        print(skdlflsdfkldslk)
        print("OK")

    def funOkOk(self):
        pass

    def funLoginSignUp(self):
        print("DLLJFDK")
        mainWindow=QMainWindow()
        lc.varStore['ForgetPassword']=mainWindow

        ui=lc.Ui_MainWindow()
        ui.setupUi(mainWindow)
        ui.init(self.c)
        mainWindow.show()
        self.mainWindow.destroy()

    def handle(self,msg):
        pass

    def init(self,c):
        self.c=c
        self.labelSeqQ.close()
        self.editSeqA.close()
        self.editPassword.close()

        self.btnOk.setText("Get SeqQ1")

