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


class XMainWindow():
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(476, 376)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.labelProfilePic = QtWidgets.QLabel(self.centralwidget)
        self.labelProfilePic.setGeometry(QtCore.QRect(30, 30, 120, 140))
        self.labelProfilePic.setStyleSheet("background-color: rgb(255, 0, 0);")
        self.labelProfilePic.setText("")
        self.labelProfilePic.setObjectName("labelProfilePic")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(180, 30, 91, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(180, 60, 101, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.btnEditProfile = QtWidgets.QPushButton(self.centralwidget)
        self.btnEditProfile.setGeometry(QtCore.QRect(180, 100, 75, 23))
        self.btnEditProfile.setObjectName("btnEditProfile")
        self.btnLogOut = QtWidgets.QPushButton(self.centralwidget)
        self.btnLogOut.setGeometry(QtCore.QRect(180, 140, 75, 23))
        self.btnLogOut.setStyleSheet("background-color: rgb(255, 0, 0);")
        self.btnLogOut.setObjectName("btnLogOut")
        self.labelFullName = QtWidgets.QLabel(self.centralwidget)
        self.labelFullName.setGeometry(QtCore.QRect(280, 30, 161, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.labelFullName.setFont(font)
        self.labelFullName.setObjectName("labelFullName")
        self.labelUserName = QtWidgets.QLabel(self.centralwidget)
        self.labelUserName.setGeometry(QtCore.QRect(280, 60, 161, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.labelUserName.setFont(font)
        self.labelUserName.setObjectName("labelUserName")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(160, 30, 21, 131))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(30, 180, 421, 16))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setGeometry(QtCore.QRect(180, 80, 271, 20))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.btnNotification = QtWidgets.QPushButton(self.centralwidget)
        self.btnNotification.setGeometry(QtCore.QRect(270, 100, 75, 23))
        self.btnNotification.setObjectName("btnNotification")
        self.btnSequrity = QtWidgets.QPushButton(self.centralwidget)
        self.btnSequrity.setGeometry(QtCore.QRect(270, 140, 75, 23))
        self.btnSequrity.setObjectName("btnSequrity")
        self.btnBlockUnblock = QtWidgets.QPushButton(self.centralwidget)
        self.btnBlockUnblock.setGeometry(QtCore.QRect(360, 100, 91, 23))
        self.btnBlockUnblock.setObjectName("btnBlockUnblock")
        self.btnFriendRequest = QtWidgets.QPushButton(self.centralwidget)
        self.btnFriendRequest.setGeometry(QtCore.QRect(360, 140, 91, 23))
        self.btnFriendRequest.setObjectName("btnFriendRequest")
        self.btnFindFriends = QtWidgets.QPushButton(self.centralwidget)
        self.btnFindFriends.setGeometry(QtCore.QRect(360, 210, 75, 23))
        self.btnFindFriends.setObjectName("btnFindFriends")
        self.btnGroupMeet = QtWidgets.QPushButton(self.centralwidget)
        self.btnGroupMeet.setGeometry(QtCore.QRect(360, 250, 75, 23))
        self.btnGroupMeet.setObjectName("btnGroupMeet")
        self.btnGroupChat = QtWidgets.QPushButton(self.centralwidget)
        self.btnGroupChat.setGeometry(QtCore.QRect(360, 290, 75, 23))
        self.btnGroupChat.setObjectName("btnGroupChat")
        self.line_4 = QtWidgets.QFrame(self.centralwidget)
        self.line_4.setGeometry(QtCore.QRect(330, 200, 20, 151))
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_2.setText(_translate("MainWindow", "Full Name  :"))
        self.label_3.setText(_translate("MainWindow", "User Name :"))
        self.btnEditProfile.setText(_translate("MainWindow", "Edit Profile"))
        self.btnLogOut.setText(_translate("MainWindow", "Log Out"))
        self.labelFullName.setText(_translate("MainWindow", "My name is"))
        self.labelUserName.setText(_translate("MainWindow", "My userName is"))
        self.btnNotification.setText(_translate("MainWindow", "Notification"))
        self.btnSequrity.setText(_translate("MainWindow", "Sequrity"))
        self.btnBlockUnblock.setText(_translate("MainWindow", "Block Unblock"))
        self.btnFriendRequest.setText(_translate("MainWindow", "Friend Request"))
        self.btnFindFriends.setText(_translate("MainWindow", "Find Friends"))
        self.btnGroupMeet.setText(_translate("MainWindow", "Group Meet"))
        self.btnGroupChat.setText(_translate("MainWindow", "Group Chat"))

    def init(self,c):
        self.c=c

