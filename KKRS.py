
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import KKRS as lc
import sys



#frameFileContainerChat={}
colorDict={'red':(250,0,0)}


def qTimerRefressFun(timerFunList):
    funList=timerFunList
    if len(funList)>0:
        funList[0]()
        timerFunList.pop(0)

def handleOnRecvStart(recv,fName):

    if fName in lc.funListRecvEnd:
        fun=lc.funListRecvEnd[fName][0]
        fun()

def handleOnRecvEnd(recv,fName,cond):

    if fName in lc.funListRecvEnd:
        fun=lc.funListRecvEnd[fName][1]
        size=recv.fileSize[fName]
        fun(cond,size)

def showResult(statusbar,msg,error=True):
    statusbar.showMessage(msg)
    if error:
        statusbar.setStyleSheet('background-color: rgb(250, 0, 0);')
    else:
        statusbar.setStyleSheet('background-color: rgb(0, 250, 0);')

def colorButton(widget,text='',color=(250,0,0)):

    if text!='':
        widget.setText(text)
    if color==None:
        back=''
    else:
        back='background-color:rgb{0};'.format(str(color))
    widget.setStyleSheet(back)



class ForgetPassword():
    def setupUi(self, MainWindow):
        self.mainWindow=MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(289, 288)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 10, 191, 31))
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
        self.editUserName.setGeometry(QtCore.QRect(30, 60, 113, 20))
        self.editUserName.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.editUserName.setObjectName("editUserName")
        self.labelSeqQ = QtWidgets.QLabel(self.centralwidget)
        self.labelSeqQ.setGeometry(QtCore.QRect(30, 100, 241, 61))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.labelSeqQ.setFont(font)
        self.labelSeqQ.setWordWrap(True)
        self.labelSeqQ.setObjectName("labelSeqQ")
        self.editPassword = QtWidgets.QLineEdit(self.centralwidget)
        self.editPassword.setGeometry(QtCore.QRect(30, 230, 113, 20))
        self.editPassword.setObjectName("editPassword")
        self.btnLoginSignUp = QtWidgets.QPushButton(self.centralwidget)
        self.btnLoginSignUp.setGeometry(QtCore.QRect(180, 230, 81, 23))
        self.btnLoginSignUp.setObjectName("btnLoginSignUp")
        self.btnOk = QtWidgets.QPushButton(self.centralwidget)
        self.btnOk.setGeometry(QtCore.QRect(180, 180, 75, 23))
        self.btnOk.setObjectName("btnOk")
        self.editSeqA = QtWidgets.QLineEdit(self.centralwidget)
        self.editSeqA.setGeometry(QtCore.QRect(30, 180, 113, 20))
        self.editSeqA.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.editSeqA.setObjectName("editSeqA")
        self.btnOk_2 = QtWidgets.QPushButton(self.centralwidget)
        self.btnOk_2.setGeometry(QtCore.QRect(180, 60, 75, 23))
        self.btnOk_2.setObjectName("btnOk_2")
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
        self.labelSeqQ.setText(_translate("MainWindow", "Sequrity Question"))
        self.editPassword.setPlaceholderText(_translate("MainWindow", "Password"))
        self.btnLoginSignUp.setText(_translate("MainWindow", "Login / SignUp"))
        self.btnOk.setText(_translate("MainWindow", "Get Password"))
        self.editSeqA.setPlaceholderText(_translate("MainWindow", "Sequrity Answer"))
        self.btnOk_2.setText(_translate("MainWindow", "Get Seq Ques"))

    def init(self,c):
        self.mainWindow.setWindowTitle("Forget Password")

        self.c=c
        self.btnOk_2.clicked.connect(self.funGetSeqQ)
        self.btnOk.clicked.connect(self.funGetPassword)

        self.btnOk.close()
        self.labelSeqQ.close()
        self.editPassword.close()
        self.editSeqA.close()
        self.mainWindow.closeEvent=self.onClose

    def funGetSeqQ(self):
        userName=self.editUserName.text()

        user=lec.checkUserName(userName)

        if user==True:

            self.c.functionList['getSequrityQuestion']=self.handle

            self.c.getSequrityQuestion(userName)

        else:
            showResult(self.statusbar,user)



    def funGetPassword(self):
        userName=self.editUserName.text()
        seqAnswer=self.editSeqA.text()

        user=lec.checkUserName(userName)
        seA=lec.checkSequrityAnswer(seqAnswer)

        if user==True:

            if seA==True:
                self.c.functionList['_forgetPassword']=self.handle
                self.c.forgetPassword(userName,seqAnswer)
                showResult(self.statusbar,"Loading ..",False)

            else:
                showResult(self.statusbar,seA)

        else:
            showResult(self.statusbar,user)



    def onClose(self,event):
        self.c.s.close()
        event.accept()



    def handle(self,msg):
        code=msg['code']
        if code=='0007':
            showResult(self.statusbar,"Passwords is copied to clipboard",False)

            passw=msg['userPass']
            pc.copy(passw)



        elif code=='0008':
            #Seq A not correct
            showResult(self.statusbar,"Sequrity Answer is incorrect")
        elif code=='4567':
            #Seq A not correct
            showResult(self.statusbar,"UserName don't exist")
        elif code=='45t6':
            #Seq A not correct
            showResult(self.statusbar,"Now Enter the sequrity Answer",False)

            #self.editUserName.setDisabled(True)
            self.labelSeqQ.show()
            self.editSeqA.show()
            self.btnOk.show()

            seqQ=msg['seqQ']
            self.labelSeqQ.setText(seqQ)


        else:
            #Unknown msg request
            showResult(self.statusbar,"Error :"+code)


class XLicense():
    def setupUi(self, MainWindow):
        self.mainWindow=MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(404, 313)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setGeometry(QtCore.QRect(20, 50, 351, 211))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        self.plainTextEdit.setFont(font)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(120, 10, 161, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(20, 270, 211, 17))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        self.checkBox.setFont(font)
        self.checkBox.setObjectName("checkBox")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(300, 270, 75, 23))
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        self.pushButton.clicked.connect(self.funContinue)
        self.pushButton.setDisabled(True)
        self.plainTextEdit.setReadOnly(True)
        self.checkBox.clicked.connect(self.funCheckLicenseAgreement)

        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.plainTextEdit.setPlainText(_translate("MainWindow", "\n"
        "Hello Everyone,\n"
        "\n"
        "Xprt-Client is a simple server-client application for the remote controlling client to client.\n"
        "\n"
        "For the software to successfully run or fully iterative to the user. It requires the following things.\n"
        "\n"
        "Requirements To Run Software\n"
        "\n"
        "1. Camera     \n"
        "2. Sound\n"
        "3. Mic\n"
        "4. Display Frame\n"
        "5. Keyboard \n"
        "6. Mouse Control\n"
        "\n"
        "These 6 are required to run successfully the software.\n"
        "\n"
        "Why these are required.\n"
        "\n"
        "1. Camera     -> For Video Conferencing your camera frame is required. \n"
        "2. Sound     -> For listening to the data sent by another user to you.\n"
        "3. Mic     -> For Audio Conferencing your mic frame is required.\n"
        "4. Display Frame -> For sharing your display frame it is required.\n"
        "5. Keyboard     -> It is required to control the user keyboard remotely.\n"
        "6. Mouse     -> It is required to control the user mouse remotely.\n"
        "\n"
        "These all are required to send data to the server and then after server will send these data to the client.\n"
        "\n"
        "So, you as a client will also receive these types of data.\n"
        "You have the authority to accept/reject these data from the other client.\n"
        "\n"
        "** If you will receive the keyboard and mouse data then your system will be controlled by that user using your keyboard and mouse.\n"
        "\n"
        "The data are end to end encrypted.\n"
        "\n"
        "If you wish/want to suggest any thing related to Xprt-Client then please send feedback.\n"
        "\n"
        "\n"
        "\n"
        "Thank You\n"
        "Bipin Singh\n"
        "\n"
        "Email:- xprtclient@gmail.com\n"
        "\n"
        "\n"
        ""))
        self.label.setText(_translate("MainWindow", "License & Agreement"))
        self.checkBox.setText(_translate("MainWindow", "I accept the license & Agreement"))
        self.pushButton.setText(_translate("MainWindow", "Continue"))

    def init(self,c):
        self.c=c
        self.mainWindow.setWindowTitle("License & Agreement")

    def funCheckLicenseAgreement(self):
        if self.checkBox.isChecked():
            self.pushButton.setEnabled(True)
        else:
            self.pushButton.setDisabled(True)

    def funContinue(self):
        mainWindow=QMainWindow()
        lc.varStore['XMainWindow']=mainWindow
        self.ui=lc.XMainWindow()
        self.ui.setupUi(mainWindow)
        self.ui.init(self.c)
        self.mainWindow.destroy()
        mainWindow.show()

class Ui_MainWindow():
    def setupUi(self, MainWindow):
        self.timerFunList=[]
        self.mainWindow=MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(404, 313)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.editLUserName = QtWidgets.QLineEdit(self.centralwidget)
        self.editLUserName.setGeometry(QtCore.QRect(40, 70, 113, 20))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.editLUserName.setFont(font)
        self.editLUserName.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.editLUserName.setObjectName("editLUserName")
        self.editLPassword = QtWidgets.QLineEdit(self.centralwidget)
        self.editLPassword.setGeometry(QtCore.QRect(40, 110, 113, 20))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setBold(False)
        font.setWeight(50)
        self.editLPassword.setFont(font)
        self.editLPassword.setObjectName("editLPassword")
        self.btnForgetPassword = QtWidgets.QPushButton(self.centralwidget)
        self.btnForgetPassword.setGeometry(QtCore.QRect(40, 170, 101, 23))
        self.btnForgetPassword.setObjectName("btnForgetPassword")
        self.btnLogin = QtWidgets.QPushButton(self.centralwidget)
        self.btnLogin.setGeometry(QtCore.QRect(80, 230, 75, 23))
        self.btnLogin.setObjectName("btnLogin")

        self.btnContinue=QPushButton(self.centralwidget)
        self.btnContinue.setGeometry(80,270,75,23)
        self.btnContinue.setText("Continue")

        self.btnContinue.close()

        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(183, 30, 20, 261))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(41, 20, 91, 31))
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
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(240, 20, 111, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(22)
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setMouseTracking(True)
        self.label_2.setMidLineWidth(1)
        self.label_2.setObjectName("label_2")
        self.editFullName = QtWidgets.QLineEdit(self.centralwidget)
        self.editFullName.setGeometry(QtCore.QRect(240, 70, 113, 20))
        self.editFullName.setObjectName("editFullName")
        self.editSUserName = QtWidgets.QLineEdit(self.centralwidget)
        self.editSUserName.setGeometry(QtCore.QRect(240, 110, 113, 20))
        self.editSUserName.setObjectName("editSUserName")
        self.editSPassword = QtWidgets.QLineEdit(self.centralwidget)
        self.editSPassword.setGeometry(QtCore.QRect(240, 150, 113, 20))
        self.editSPassword.setObjectName("editSPassword")
        self.editSeqQ = QtWidgets.QLineEdit(self.centralwidget)
        self.editSeqQ.setGeometry(QtCore.QRect(240, 190, 113, 20))
        self.editSeqQ.setObjectName("editSeqQ")
        self.editSeqA = QtWidgets.QLineEdit(self.centralwidget)
        self.editSeqA.setGeometry(QtCore.QRect(240, 230, 113, 20))
        self.editSeqA.setObjectName("editSeqA")
        self.btnSignUp = QtWidgets.QPushButton(self.centralwidget)
        self.btnSignUp.setGeometry(QtCore.QRect(280, 270, 75, 23))
        self.btnSignUp.setObjectName("btnSignUp")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        self.qTimer=QTimer()
        self.qTimer.setInterval(500)
        self.qTimer.timeout.connect(lambda :qTimerRefressFun(self.timerFunList))
        self.qTimer.start()
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.editLUserName.setPlaceholderText(_translate("MainWindow", "User Name"))
        self.editLPassword.setPlaceholderText(_translate("MainWindow", "Password"))
        self.btnForgetPassword.setText(_translate("MainWindow", "Forget Password"))
        self.btnLogin.setText(_translate("MainWindow", "Login!"))
        self.label.setText(_translate("MainWindow", "Login"))
        self.label_2.setText(_translate("MainWindow", "Sign Up"))
        self.editFullName.setPlaceholderText(_translate("MainWindow", "Full Name"))
        self.editSUserName.setPlaceholderText(_translate("MainWindow", "User Name"))
        self.editSPassword.setPlaceholderText(_translate("MainWindow", "Password"))
        self.editSeqQ.setPlaceholderText(_translate("MainWindow", "Sequrity Question"))
        self.editSeqA.setPlaceholderText(_translate("MainWindow", "Sequrity Answer"))
        self.btnSignUp.setText(_translate("MainWindow", "Sign Up!"))

        self.btnLogin.clicked.connect(self.funLogin)
        self.btnForgetPassword.clicked.connect(self.funForgetPassword)
        self.btnSignUp.clicked.connect(self.funSignUp)


    def funLogin(self):

        userName=self.editLUserName.text()
        password=self.editLPassword.text()


        user=lec.checkUserName(userName)
        passw=lec.checkUserPassword(password)

        if user==True:
            if passw==True:
                self.serverFunLogin(userName,password)
                self.btnLogin.setDisabled(True)
                self.btnSignUp.setDisabled(True)
                showResult(self.statusbar,"Loading ..",False)
            else:
                showResult(self.statusbar,passw)
        else:
            showResult(self.statusbar,user)


    def init(self,c):
        self.c=c
        self.mainWindow.setWindowTitle("Login / SignUp")
        self.mainWindow.closeEvent=self.onClose
        self.rExit=False


    def onClose(self,event):
        if not  self.rExit:
            print("SOCKET CLOSING")
            self.c.s.close()
        event.accept()


    def funForward(self):
        self.callMainWindow()

    def OnSuccessfull(self):


        mainWindow=QMainWindow()
        lc.varStore['XLicense']=mainWindow
        self.ui=lc.XLicense()
        self.ui.setupUi(mainWindow)
        self.ui.init(self.c)
        self.mainWindow.destroy()
        mainWindow.show()


    def handleLogin(self,msg):

        if msg=='0000':
            #Login Successful
            showResult(self.statusbar,"Login Successfull",False)
            self.OnSuccessfull()

        elif msg=='0001':
            #Incorrect password
            showResult(self.statusbar,"Incorrect Password")
        elif msg=='0002':
            showResult(self.statusbar,"User Name does't exist")
        else:
            showResult(self.statusbar,f"Error : {msg}")


    def handleSignUp(self,msg):
        if msg=='0003':
            showResult(self.statusbar,"User Name already exist.")
        elif msg=='0004':

            showResult(self.statusbar,"SignUp successfull",False)
            self.OnSuccessfull()
        else:
            showResult(self.statusbar,f"Error : {msg}")


    def handle(self,msg):
        def fun():
            self.btnLogin.setEnabled(True)
            self.btnSignUp.setEnabled(True)
            if msg['wType']=='_login':

                self.handleLogin(msg['code'])
            elif msg['wType']=='_signUp':

                self.handleSignUp(msg['code'])
            else:
                print("Unknown wType ",wType)
        self.timerFunList.append(fun)

    def serverFunLogin(self,userName,password):

        self.c.functionList['_login']=self.handle
        self.c.userName=userName

        self.editLPassword.setText("")
        self.c.login(userName,password)


    def serverFunSignUp(self,name,userName,password,seqQ,seqA):
        self.c.functionList['_signUp']=self.handle
        self.c.signUp(name,userName,password,seqQ,seqA)
        self.c.userName=userName


        self.editSPassword.setText("")
        self.editSeqA.setText("")

    def funBack(self,mainWindow):
        mainWindow.destroy()
        self.mainWindow.show()


    def funForgetPassword(self):
        mainWindow=QMainWindow()
        lc.varStore['ForgetPassword']=mainWindow
        self.rExit=True
        self.fp=lc.ForgetPassword()
        self.fp.setupUi(mainWindow)
        self.fp.init(self.c)

        self.fp.btnLoginSignUp.clicked.connect(lambda :self.funBack(mainWindow))

        mainWindow.show()
        self.mainWindow.close()


    def funSignUp(self):
        name=self.editFullName.text()
        userName=self.editSUserName.text()
        password=self.editSPassword.text()
        seqQ=self.editSeqQ.text()
        seqA=self.editSeqA.text()

        nm=lec.checkName(name)
        user=lec.checkUserName(userName)
        passw=lec.checkUserPassword(password)
        seQ=lec.checkSequrityQuestion(seqQ)
        seA=lec.checkSequrityAnswer(seqA)


        if nm==True:
            if user==True:
                if passw==True:
                    if seQ==True:
                        if seA==True:
                            showResult(self.statusbar,"Loading ..",False)
                            self.serverFunSignUp(name,userName,password,seqQ,seqA)
                            self.btnSignUp.setDisabled(True)
                            self.btnLogin.setDisabled(True)
                        else:
                            showResult(self.statusbar,seA)
                    else:
                        showResult(self.statusbar,seQ)
                else:
                    showResult(self.statusbar,passw)
            else:
                showResult(self.statusbar,user)
        else:
            showResult(self.statusbar,nm)

class Controls:

    def __init__(self):

        self.openWindows={}
        self.controlCond={}
        self.funList={}
        self.funFirstOnList={}
        #self.funFirstOffList={}
        self.funThread={}
        self.cond={}

        self.funOnStartInstance=None
        self.funOnEndInstance=None

    def funOpenWindow(self,userName):
        self.openWindows[userName]=True
        self.controlCond[userName]={}
        self.funThread[userName]={}

    def funCloseWindow(self,userName):
        self.openWindows[userName]=False
        del self.controlCond[userName]
        del self.funThread[userName]

    def funOnSending(self,userName,types):
        def fun():
            self.controlCond[userName][types]=True
            self.cond[types]=True

            self.executeOnStart(types)
            fts=self.funFirstOnList[types]

            class MThread(QThread):

                def run(self):
                    fts()
            self.t1=MThread()
            self.t1.start()

        class MThread(QThread):

            def run(self):
                fun()
        self.t2=MThread()
        self.t2.start()

    def funOffSending(self,userName,types):
        def fun():
            self.controlCond[userName][types]=False
            self.executeOnStop(types)


        class MThread(QThread):

            def run(self):
                fun()
        self.t4=MThread()
        self.t4.start()

    def executeOnStart(self,types):
        count=0
        cond=False
        for i in self.controlCond:
            if types in self.controlCond[i]:
                cond=True
                ct=self.controlCond[i][types]
                if ct:
                    count=count+1

        if cond:

            funs=self.funList[types]
            if count>1:
                pass
            else:
                funt=self.funOnStartInstance

                funt(types)
                def fun():

                    while self.cond[types]:
                        funs()
                class MThread(QThread):

                    def run(self):
                        fun()
                self.t5=MThread()
                self.t5.start()
                self.funThread[types]=self.t5



    def executeOnStop(self,types):
        count=0
        for i in self.controlCond:
            ct=self.controlCond[i][types]
            if not ct:
                count=count+1

        fun=self.funList[types]
        length=len(self.controlCond)
        if count!=length:
            pass
        else:
            self.cond[types]=False
            funt=self.funOnEndInstance

            funt(types)

class Function:


    def __init__(self,c):
        self.c=c


    def sendSound(self,userName,stream,fr=1024):
        frame=con.get_mic_frame(stream,fr)
        frame=ds.encb(frame)
        data=frame.decode()

        self.c._Sound(userName,data)

    def sendIntSound(self,userName,stream,fr=1024):
        frame=con.get_mic_frame(stream,fr)

        frame=ds.encb(frame)
        data=frame.decode()

        self.c._IntSound(userName,data)

    def sendCamera(self,userName,cap):
        frame=con.get_cam_frame(cap)
        if frame is not None:
            data=ds.prepSend(frame)

            self.c._Camera(userName,data[0],data[1],data[2])


    def sendScreen(self,userName,size=(600,300)):
        frame=con.get_screen_shot(size)
        data=ds.prepSend(frame)
        self.c._Screen(userName,data[0],data[1],data[2])

    def sendMouse(self,userName,mo):
        time.sleep(1)

        if len(mo.buttons)>0:
            data=mo.buttons
            mo.clear()

            data=ds.prepSend(data)

            self.c._Mouse(userName,data[0],data[1],data[2])

    def sendKeyboard(self,userName,kb):

        time.sleep(1)

        if len(kb.keys)>0:
            data=kb.keys

            kb.clear()
            data=ds.prepSend(data)

            self.c._Keyboard(userName,data[0],data[1],data[2])

class XMainWindow():
    openWindows={}
    onlineFriends={}
    labelOnlineFr={}
    giverManager={'sound':None,'IntSound':None,'camera':None,'mouse':None,'keyboard':None}

    xprtFunction=None
    xprtControl=None

    objContainer={}

    def setupUi(self, MainWindow):
        self.mainWindow=MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(476, 376)
        self.centralwidget = QtWidgets.QWidget(MainWindow)

        self.scrollContainer,self.scrollHolder=pqc.scrollBar(self.centralwidget,30,200,300,150)

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
        self.labelFullName.setGeometry(QtCore.QRect(280, 30, 161, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.labelFullName.setFont(font)
        self.labelFullName.setObjectName("labelFullName")
        self.labelUserName = QtWidgets.QLabel(self.centralwidget)
        self.labelUserName.setGeometry(QtCore.QRect(280, 60, 161, 20))
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
        self.btnFindFriends.setGeometry(QtCore.QRect(360, 210, 85, 23))
        self.btnFindFriends.setObjectName("btnFindFriends")
        self.btnGroupMeet = QtWidgets.QPushButton(self.centralwidget)
        self.btnGroupMeet.setGeometry(QtCore.QRect(360, 290, 85, 23))
        self.btnGroupMeet.setObjectName("btnGroupMeet")
        self.btnGroupChat = QtWidgets.QPushButton(self.centralwidget)
        self.btnGroupChat.setGeometry(QtCore.QRect(360, 250, 85, 23))
        self.btnGroupChat.setObjectName("btnGroupChat")


        self.btnAbout=QPushButton(self.centralwidget)
        self.btnAbout.setGeometry(404,25,61,23)
        self.btnAbout.setText("About")

        self.btnFeedBack=QPushButton(self.centralwidget)
        self.btnFeedBack.setGeometry(404,60,61,23)
        self.btnFeedBack.setText("Feedback")

        self.btnRefressFriend=QPushButton(self.centralwidget)
        self.btnRefressFriend.setText("Refress Friends")
        self.btnRefressFriend.setGeometry(360,330,85,23)
        self.btnRefressFriend.clicked.connect(self.funRefressFriendList)
        self.line_4 = QtWidgets.QFrame(self.centralwidget)
        self.line_4.setGeometry(QtCore.QRect(330, 200, 20, 151))
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.qTimer=QTimer()
        self.qTimer.setInterval(500)
        self.qTimer.timeout.connect(self.funRefressFriendList)
        self.qTimer.start()

        lc.qTimer=QTimer()
        lc.qTimer.setInterval(50)
        lc.qTimer.timeout.connect(self.funGlobalRefressList)
        lc.qTimer.start()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        self.timer=QTimer(self.mainWindow)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.funRefressFriendList)
        self.timer.start()
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

        self.btnEditProfile.clicked.connect(self.funBtnEditProfile)
        self.btnNotification.clicked.connect(self.funBtnNotification)
        self.btnBlockUnblock.clicked.connect(self.funBtnBlockUnblock)
        #self.btnLogOut.clicked.connect
        self.btnSequrity.clicked.connect(self.funBtnSequrity)
        self.btnFriendRequest.clicked.connect(self.funBtnFriendRequest)
        self.btnFindFriends.clicked.connect(self.funBtnFindFriend)
        self.btnGroupMeet.clicked.connect(self.funBtnGroupMeet)
        self.btnGroupChat.clicked.connect(self.funBtnGroupChat)

    def init(self,c):

        self.c=c
        self.btnLogOut.clicked.connect(self.funLogOut)
        self.ig=xcs.InfoGetter(self.c.send)

        self.memberChatWindow={}
        self.friendData=None
        self.friendListCount=0
        self.FWidList={}
        self.initiate()

        self.viewDict={}

        self.flistData={}

        self.logOut=False

        self.timerFunList=[]

        self.btnRefressFriend.setText("Exit Error")
        self.btnRefressFriend.clicked.connect(self.funExit)
        self.btnAbout.clicked.connect(self.funBtnAbout)
        self.btnFeedBack.clicked.connect(self.funBtnFeedback)

        self.mainWindow.closeEvent=self.onClose

        self.c.functionList['loginALoc']=self.handleLoginALoc
        self.c.functionList['request']=self.handleCWRequest
        self.c.functionList['response']=self.handleCWResponse

        self.c.functionList['InfoGetter']=self.handleInformation

        self.refress()
        self.refressInformation()

    def refressInformation(self):
        self.ig.iGGetInformation()
        self.ig.iGGetInfoC()

    def handleInformation(self,msg):
        def fun():
            code=msg['code']

            if code=='U53e':
                notif=msg['notification']
                freq=msg['friendRequest']
                greq=msg['groupRequest']

                if notif!='True':
                    colorButton(self.btnNotification)


                if freq!='True':
                    colorButton(self.btnFriendRequest)


                #if greq!='True':
                 #   colorButton(self.btnGroupChat)

            elif code=='45f6':

                data=ds.remodifyData(msg['data'],msg['dataType'],msg['dataShape'])

                for i in data:
                    userName,chat=i
                    self.viewDict[userName]=chat
                    if chat=='False':
                        if userName in self.FWidList:
                            frame=self.FWidList[userName]
                            children=frame.children()
                            colorButton(children[3])


            else:
                print("UNKNOWN INFORMATION ERROR :"+code)

        self.timerFunList.append(fun)


    def handleCWRequest(self,msg):


        code=msg['code']

        if code=='LHY0':
            def fun():
                userName=msg['userName']
                vType=msg['vType']
                windowName=userName.lower()+vType+' ChatWindow'
                cond=self.checkOpenWindow(windowName)

                if cond:
                    pass

                else:


                        lc.XMainWindow.openWindows[windowName]=True
                        mainWindow=QMainWindow()

                        def funAccept(windowName,mainWindow):
                            lc.XMainWindow.openWindows[windowName]=False
                            self.c.rResponse(userName,vType,'1')
                            mainWindow.destroy()

                            windowName=userName+'chatWindow'
                            cond=self.checkOpenWindow(windowName)
                            if cond:
                                pass

                            else:
                                XMainWindow.openWindows[windowName]=True
                                mainWindow=QMainWindow()
                                lc.varStore[windowName]=mainWindow
                                XMainWindow.xprtControl.funOpenWindow(userName)

                                self.memberChatWindow[userName]=lc.XChatWindowMember()
                                self.memberChatWindow[userName].setupUi(mainWindow)
                                data=self.flistData[userName]
                                self.memberChatWindow[userName].init(self.c,userName,data)

                                mainWindow.show()



                            def commonFunction():

                                if vType=='camera':
                                    self.memberChatWindow[userName].onSendCamera()
                                elif vType=='sound':
                                    self.memberChatWindow[userName].onSendSound()
                                elif vType=='keyboard':
                                    self.memberChatWindow[userName].onSendKeyboard()
                                elif vType=='screen':
                                    self.memberChatWindow[userName].onSendScreen()
                                elif vType=='mouse':
                                    self.memberChatWindow[userName].onSendMouse()
                                else:
                                    showResult(self.memberChatWindow[userName].statusbar,"VType :"+vType)

                            commonFunction()


                        def funReject(windowName,mainWindow):
                            lc.XMainWindow.openWindows[windowName]=False

                            self.c.rResponse(userName,vType,'0')
                            mainWindow.destroy()
                        ctx=windowName
                        def funOnClose(event):
                            lc.XMainWindow.openWindows[ctx]=False
                            self.c.rResponse(userName,vType,'0')
                            event.accept()



                        gmjr=lc.XGroupMeetJoinRequest()
                        gmjr.setupUi(mainWindow)
                        gmjr.labelText.setText(userName+' want to access your '+vType)
                        gmjr.btnAccept.clicked.connect(lambda :funAccept(windowName,mainWindow))
                        mainWindow.closeEvent=funOnClose
                        gmjr.btnReject.clicked.connect(lambda: funReject(windowName,mainWindow))
                        mainWindow.show()

            lc.timerFunList.append(fun)

        elif code=='LFG3':
            userName=msg['userName']
            vType=msg['vType']
            showResult(self.memberChatWindow[userName].statusbar,"User is already Sending "+vType,False)
        elif code=='LFG7':
            userName=msg['userName']
            showResult(self.memberChatWindow[userName].statusbar,"User is not Online")
        else:
            showResult(self.statusbar,"Error :"+code)
            print("ERROR L "+code)


    def handleCWResponse(self,msg):
        code=msg['code']

        if code=='LHN0':
            userName=msg['userName']
            vType=msg['vType']
            vValue=msg['vValue']
            statement=''
            if vValue=='1':
                statement=userName+' accepted your {0} request'.format(vType)
                print(vType,'is accepted')
                def commonFunction():
                    if vType=='camera':
                        self.memberChatWindow[userName].onRecvCamera()
                    elif vType=='sound':
                        self.memberChatWindow[userName].onRecvSound()
                    elif vType=='keyboard':
                        self.memberChatWindow[userName].onRecvKeyboard()
                    elif vType=='screen':
                        self.memberChatWindow[userName].onRecvScreen()
                    elif vType=='mouse':
                        self.memberChatWindow[userName].onRecvMouse()
                    else:
                        showResult(self.memberChatWindow[userName].statusbar,"VType :"+vType)

                commonFunction()


                showResult(self.memberChatWindow[userName].statusbar,statement,False)
            else:
                statement=userName+' rejected your {0} request'.format(vType)
                showResult(self.memberChatWindow[userName].statusbar,statement)

        else:
            showResult(self.statusbar,"Error :"+code)
            print("ERROR L "+code)

    def handleLoginALoc(self,msg):
        def fun():

            lc.stCont=xlc.Controller()

            for i in lc.varStore:
                win=lc.varStore[i]

                if i=='XMainWindow':

                    win.setDisabled(True)
                else:

                    win.destroy()
            self.executePopupLoginALoc()
        self.timerFunList.append(fun)

    def executeSecondLoginALocPart(self):
        lc.varStore={}


        lc.con=rc.Controls()
        lc.stream=con.on_mic()
        lc.stream2=con.on_mic()
        lc.keyb=km.Keyboard()
        lc.mous=km.Mouse()

        lc.gmCond=False
        lc.gcCond=False
        lc.timerFunList=[]


        lc.loadRecvDownloalFileList={}
        lc.loadSendFileList={}


        lc.funRecvFileStatus={}
        lc.funSendFileStatus={}

        lc.funListRecvEnd={}

        MainWindow = QMainWindow()
        lc.ui = Ui_MainWindow()
        lc.ui.setupUi(MainWindow)
        lc.varStore['mainWindowXyz']=MainWindow
        lc.ui.statusbar.showMessage("LogOut Successfully")
        ui.statusbar.setStyleSheet('background-color: rgb(0, 255, 0);')
        cond=True
        def serverError(SERVER_IP,SERVER_PORT):
            global cond
            cond=False
            lc.ui.statusbar.showMessage("Server Connection Error")
            lc.ui.statusbar.setStyleSheet('background-color: rgb(255, 0, 0);')


        c=xcs.Client()
        c.connect(SERVER_IP,SERVER_PORT,serverError)

        if cond:
            lc.ui.statusbar.showMessage("Connected To The Server")
            lc.ui.statusbar.setStyleSheet('background-color: rgb(0, 255, 0);')
            lc.ui.init(c)
            lc.fc=xtfo.FileControl(c)




        MainWindow.show()

    def executePopupLoginALoc(self):
        windowName='LoginFromALocation'
        cond=self.checkOpenWindow(windowName)
        if cond:
            pass
        else:
            lc.XMainWindow.openWindows[windowName]=True
            mainWindow=QMainWindow()

            def funAccept():
                mainWindow.destroy()
                lc.varStore['XMainWindow'].destroy()
                self.executeSecondLoginALocPart()

            def funReject():
                sys.exit()

            def funOnClose(event):
                event.accept()
                sys.exit()

            gmjr=lc.XGroupMeetJoinRequest()
            gmjr.setupUi(mainWindow)
            gmjr.labelText.setText("Your account is logined from another location. So you are logOuted.")
            gmjr.btnAccept.setText("Login Page")
            mainWindow.setWindowTitle("Login From Another Location")
            gmjr.btnReject.setText("Exit")
            gmjr.btnAccept.clicked.connect(funAccept)
            mainWindow.closeEvent=funOnClose
            gmjr.btnReject.clicked.connect(funReject)
            mainWindow.show()


    def initiate(self):

        XMainWindow.xprtFunction=lc.Function(self.c)
        XMainWindow.xprtControl=lc.Controls()

        XMainWindow.xprtControl.funOnStartInstance=self.activateFunction
        XMainWindow.xprtControl.funOnEndInstance=self.deactivateFunction

        XMainWindow.xprtControl.funList['sound']=self.xxsSound
        XMainWindow.xprtControl.funList['IntSound']=self.xxsIntSound
        XMainWindow.xprtControl.funList['camera']=self.xxsCamera
        XMainWindow.xprtControl.funList['screen']=self.xxsScreen
        XMainWindow.xprtControl.funList['mouse']=self.xxsMouse
        XMainWindow.xprtControl.funList['keyboard']=self.xxsKeyboard

    def onClose(self,event):
        self.c.send.stopAllFilesSending()
        gm=XMainWindow.giverManager
        sound=gm['sound']
        intSound=gm['IntSound']

        con.off_mic(sound)
        con.off_mic(intSound)

        cap=gm['camera']
        con.off_camera(cap)

        mouse=gm['mouse']
        if mouse is not None:
            mouse.mStop()

        keyboard=gm['keyboard']
        if keyboard is not None:
            keyboard.mStop()

        if not self.logOut:
            self.c.s.close()
            sys.exit(0)

    def funLogOut(self):

        self.c.send.stopAllFilesSending()

        self.c.logOut()
        lc.stCont=xlc.Controller()

        for i in lc.varStore:
            win=lc.varStore[i]
            win.destroy()
        lc.varStore={}


        lc.con=rc.Controls()
        lc.stream=con.on_mic()
        lc.stream2=con.on_mic()
        lc.keyb=km.Keyboard()
        lc.mous=km.Mouse()

        lc.gmCond=False
        lc.gcCond=False
        lc.timerFunList=[]


        lc.loadRecvDownloalFileList={}
        lc.loadSendFileList={}


        lc.funRecvFileStatus={}
        lc.funSendFileStatus={}

        lc.funListRecvEnd={}

        MainWindow = QMainWindow()
        lc.ui = Ui_MainWindow()
        lc.ui.setupUi(MainWindow)
        lc.varStore['mainWindowXyz']=MainWindow
        lc.ui.statusbar.showMessage("LogOut Successfully")
        ui.statusbar.setStyleSheet('background-color: rgb(0, 255, 0);')
        ui.init(self.c)


        MainWindow.show()
        #self.mainWindow.destroy()

    def activateFunction(self,types):

        if types=='sound':
            stream=con.on_mic()
            XMainWindow.giverManager['sound']=stream
        elif types=='IntSound':
            stream=con.on_mic()
            XMainWindow.giverManager['IntSound']=stream

        elif types=='camera':
            cap=con.on_camera(0)
            XMainWindow.giverManager['camera']=cap

        elif types=='mouse':
            mous.mStart()
            XMainWindow.giverManager['mouse']=mous

        elif types=='keyboard':
            keyb.mStart()
            XMainWindow.giverManager['keyboard']=keyb

        else:
            print(types)
            print("Unknow type you are expecting")

    def deactivateFunction(self,types):
        if types=='sound':
            stream=XMainWindow.giverManager['sound']
            if stream is not None:
                stream.close()
            XMainWindow.giverManager['sound']=None

        elif types=='camera':
            cap=XMainWindow.giverManager['camera']
            if cap is not None:
                cap.release()
            XMainWindow.giverManager['camera']=None

        elif types=='mouse':
            mouse=XMainWindow.giverManager['mouse']
            if mouse is not None:
                mouse.mStop()
            XMainWindow.giverManager['mouse']=None

        elif types=='keyboard':

            keyboard=XMainWindow.giverManager['keyboard']
            if keyboard is not None:
                keyboard.mStop()
            XMainWindow.giverManager['keyboard']=None

        else:
            print("Unknown type expectiing for Deactivtion")

    def xxsCamera(self):
        cap=XMainWindow.giverManager['camera']

        if cap is None:
            pass
        else:
            XMainWindow.xprtFunction.sendCamera('@none',cap)

    def xxsScreen(self):

        XMainWindow.xprtFunction.sendScreen('@none')

    def xxsSound(self):
        stream=XMainWindow.giverManager['sound']

        if stream is None:
            pass
        else:
            XMainWindow.xprtFunction.sendSound('@none',stream)

    def xxsMouse(self):
        mouse=XMainWindow.giverManager['mouse']

        if mouse is None:
            pass
        else:
            XMainWindow.xprtFunction.sendMouse('@none',mouse)

    def xxsKeyboard(self):
        keyboard=XMainWindow.giverManager['keyboard']
        if keyboard is None:
            pass
        else:

            XMainWindow.xprtFunction.sendKeyboard('@none',keyboard)

    def xxsIntSound(self):
        stream=XMainWindow.giverManager['IntSound']

        if stream is None:
            pass
        else:
            XMainWindow.xprtFunction.sendIntSound('@none',stream)

    def checkOpenWindow(self,windowName):
        if windowName in XMainWindow.openWindows:
            return XMainWindow.openWindows[windowName]
        else:
            return False

    def funBtnEditProfile(self):
        windowName='editProfile'
        cond=self.checkOpenWindow(windowName)
        if cond:
            pass

        else:
            XMainWindow.openWindows[windowName]=True
            mainWindow=QMainWindow()
            lc.varStore['XEditProfile']=mainWindow
            self.ui=lc.XEditProfile()
            self.ui.setupUi(mainWindow)
            self.ui.init(self.c)
            mainWindow.show()

    def funBtnNotification(self):
        windowName='notification'
        cond=self.checkOpenWindow(windowName)
        if cond:
            pass

        else:
            XMainWindow.openWindows[windowName]=True
            mainWindow=QMainWindow()
            lc.varStore[windowName]=mainWindow
            self.ui=lc.XNotification()
            self.ui.setupUi(mainWindow)
            colorButton(self.btnNotification,color=None)
            self.ui.init(self.c)
            mainWindow.show()

    def funBtnSequrity(self):
        windowName='sequrity'
        cond=self.checkOpenWindow(windowName)
        if cond:
            pass

        else:
            XMainWindow.openWindows[windowName]=True
            mainWindow=QMainWindow()
            lc.varStore[windowName]=mainWindow
            self.ui=lc.XSequrity()
            self.ui.setupUi(mainWindow)
            self.ui.init(self.c)
            mainWindow.show()

    def funBtnBlockUnblock(self):
        windowName='blockUnblock'
        cond=self.checkOpenWindow(windowName)
        if cond:
            pass

        else:
            XMainWindow.openWindows[windowName]=True
            mainWindow=QMainWindow()
            lc.varStore[windowName]=mainWindow
            self.ui=lc.XBlockUnblock()
            self.ui.setupUi(mainWindow)
            self.ui.init(self.c)
            mainWindow.show()

    def funBtnFindFriend(self):
        windowName='findFriend'
        cond=self.checkOpenWindow(windowName)
        if cond:
            pass

        else:
            XMainWindow.openWindows[windowName]=True
            mainWindow=QMainWindow()
            lc.varStore[windowName]=mainWindow
            self.ui=lc.XFindFriends()
            self.ui.setupUi(mainWindow)
            self.ui.init(self.c)
            mainWindow.show()

    def funBtnFriendRequest(self):
        windowName='friendRequest'
        cond=self.checkOpenWindow(windowName)
        if cond:
            pass

        else:
            XMainWindow.openWindows[windowName]=True
            mainWindow=QMainWindow()
            lc.varStore[windowName]=mainWindow
            self.ui=lc.XFriendRequest()
            self.ui.setupUi(mainWindow)
            self.ui.init(self.c)
            colorButton(self.btnFriendRequest,color=None)
            mainWindow.show()

    def funBtnGroupChat(self):
        windowName='groupChat'
        cond=self.checkOpenWindow(windowName)

        if cond:
            pass

        else:
            XMainWindow.openWindows[windowName]=True
            mainWindow=QMainWindow()
            lc.varStore[windowName]=mainWindow
            self.ui=lc.XGroupChat()
            self.ui.setupUi(mainWindow)
            self.ui.init(self.c)
            mainWindow.show()

    def funBtnGroupMeet(self):
        windowName='groupMeet'
        cond=self.checkOpenWindow(windowName)
        if cond:
            pass

        else:
            XMainWindow.openWindows[windowName]=True
            mainWindow=QMainWindow()
            lc.varStore[windowName]=mainWindow
            self.ui=lc.XGroupMeet()
            self.ui.setupUi(mainWindow)
            self.ui.init(self.c)
            mainWindow.show()
            #xc.Meeting(root,self.c,True)


    def funBtnAbout(self):
        windowName='about'
        cond=self.checkOpenWindow(windowName)

        if cond:
            pass

        else:
            XMainWindow.openWindows[windowName]=True
            mainWindow=QMainWindow()
            lc.varStore[windowName]=mainWindow
            self.ui=lc.XAbout()
            self.ui.setupUi(mainWindow)
            self.ui.init(self.c)
            mainWindow.show()

    def funBtnFeedback(self):
        windowName='feedback'
        cond=self.checkOpenWindow(windowName)
        if cond:
            pass

        else:
            XMainWindow.openWindows[windowName]=True
            mainWindow=QMainWindow()
            lc.varStore[windowName]=mainWindow
            self.ui=lc.XFeedBack()
            self.ui.setupUi(mainWindow)
            self.ui.init(self.c)
            mainWindow.show()
            #xc.Meeting(root,self.c,True)

    def refress(self):
        self.c.functionList['onlineStatus']=self.handle
        self.c.loadUserProfile(self.c.userName,'_mainWindow')
        self.c.functionList['_mainWindow']=self.handle
        self.c.functionList['_friendListLoad']=self.handle
        self.c.functionList['request']=self.handle
        self.c.functionList['response']=self.handle


        time.sleep(0.1)
        self.c.friendListLoad(self.c.userName,'_mainWindow')

    def handleLoadUserProfile(self,msg):
        userName=msg['userName']
        name=msg['name']
        img=ds.remodifyData(msg['profileData'],msg['profileType'],msg['profileShape'])
        shape=img.shape

        img=cv2.resize(img,(120,140))
        img=pqc.cv2toPqImage(img)
        self.labelFullName.setText(name)
        self.labelUserName.setText(userName)

        self.labelProfilePic.setPixmap(img)


    def destroyFriendListElement(self):
        for i in self.scrollContainer.children()[1:]:
            i.deleteLater()

    def funExit(self):
        sys.exit(0)

    def funRefressFriendList(self):
        funList=self.timerFunList

        if len(funList)>0:
            funList[0]()
            self.timerFunList.pop(0)

    def funGlobalRefressList(self):
        funList=lc.timerFunList

        if len(funList)>0:
            funList[0]()
            lc.timerFunList.pop(0)
        #self.timer.stop()

    def refressList(self):
        for i in self.scrollHolder.children():
            i.deleteLater()

    def handleFriendListLoad(self,msg):
        code=msg['code']
        if code=='f102':
            #No friends found


            showResult(self.statusbar,"You Have No Friends Found",False)
        elif code=='f028':
            def fun():
                data=ds.remodifyData(msg['friendData'],msg['friendType'],msg['friendShape'])


                self.destroyFriendListElement()

                if data is not None:

                    for i in data:
                        self.flistData[i[0]]=i
                        self.importData(i)

            self.timerFunList.append(fun)


        else:
            label=tk.Label(self.frameFriendCont,text='Error')
            label.pack()

    def handle(self,msg):
        def fun():

            if msg['wType']=='_loadUserProfile':
                self.handleLoadUserProfile(msg)

            elif msg['wType']=='_friendListLoad':
                self.handleFriendListLoad(msg)

            elif msg['wType']=='onlineStatus':
                self.handleOnlineFriend(msg)

            elif msg['wType']=='request':
                self.handleCWRequest(msg)

            elif msg['wType']=='response':
                self.handleCWResponse(msg)
            else:
                print("UNknow type you are expecting")
        self.timerFunList.append(fun)

    def handleOnlineFriend(self,msg):

        userName=msg['userName']
        cond=msg['status']

        XMainWindow.onlineFriends[userName]=cond
        d=self.FWidList[userName]
        d=d.children()
        if cond=='True':
            d[3].setStyleSheet('background-color: green;')


        else:
            d[3].setStyleSheet('background-color: red;')


        if userName.lower() in self.memberChatWindow:
            if cond=='True':
                self.memberChatWindow[userName].labelStatus.setStyleSheet('background-color: green;')
            else:
                self.memberChatWindow[userName].labelStatus.setStyleSheet('background-color: red;')

    def importData(self,data):

        i=data
        userName=i[0]
        dcount=self.friendListCount



        name=i[1]
        imgData=ds.remodifyData(i[2],i[3],i[4])
        cond=i[5]

        XMainWindow.onlineFriends[userName]=cond

        frame=QFrame(self.scrollContainer)
        frame.setFixedSize(280,101)

        labelProfile=QLabel(frame)
        labelProfile.setGeometry(10,10,60,80)
        labelProfile.setFixedSize(60,80)
        imgData=cv2.resize(imgData,(60,80))
        image=pqc.cv2toPqImage(imgData)
        labelProfile.setPixmap(image)



        labelFullName=QLabel(frame)
        labelFullName.setGeometry(80,10,81,15)
        font = QtGui.QFont()
        font.setPointSize(11)
        labelFullName.setFont(font)
        labelFullName.setText(name)
        labelFullName.adjustSize()


        labelUserName=QLabel(frame)
        labelUserName.setGeometry(80,40,81,16)
        font.setPointSize(8)
        labelUserName.setFont(font)
        labelUserName.setText(userName)
        labelUserName.adjustSize()

        labelStatus=QLabel(frame)
        labelStatus.setGeometry(235,10,20,20)

        btnChatWindow=None

        if cond!='False':
            #XMainWindow.labelOnlineFr[userName.lower()]=tk.Label(frame,width=2,height=1,bg='green')
            #XMainWindow.labelOnlineFr[userName.lower()].place(x=240,y=10)
            labelStatus.setStyleSheet("background-color: rgb(0, 255, 0);")
        else:
            #XMainWindow.labelOnlineFr[userName.lower()]=tk.Label(frame,width=2,height=1,bg='red')
            #XMainWindow.labelOnlineFr[userName.lower()].place(x=240,y=10)
            labelStatus.setStyleSheet("background-color: rgb(255, 0, 0);")

        def userProfile():
            windowName=userName+'userProfile'
            cond=self.checkOpenWindow(windowName)
            if cond:
                pass

            else:
                XMainWindow.openWindows[windowName]=True
                mainWindow=QMainWindow()
                lc.varStore[windowName]=mainWindow
                self.ui=lc.XViewProfileMember()
                self.ui.setupUi(mainWindow)
                self.ui.init(self.c,userName)
                mainWindow.show()

        def chatWindow():
            windowName=userName+'chatWindow'
            cond=self.checkOpenWindow(windowName)
            if cond:
                pass

            else:
                XMainWindow.openWindows[windowName]=True
                mainWindow=QMainWindow()
                lc.varStore[windowName]=mainWindow
                XMainWindow.xprtControl.funOpenWindow(userName)
                self.memberChatWindow[userName]=lc.XChatWindowMember()
                self.memberChatWindow[userName].setupUi(mainWindow)
                self.memberChatWindow[userName].init(self.c,userName,data)
                colorButton(btnChatWindow,color=None)
                mainWindow.show()







        btnChatWindow=QPushButton(frame)
        btnChatWindow.setText("Chat Window")
        btnChatWindow.clicked.connect(chatWindow)
        btnChatWindow.setGeometry(80,68,75,23)

        if userName in self.viewDict:
            chat=self.viewDict[userName]

            if chat=='False':
                colorButton(btnChatWindow)

        btnUserProfile=QPushButton(frame)
        btnUserProfile.setText("Profile")
        btnUserProfile.clicked.connect(userProfile)
        btnUserProfile.setGeometry(185,70,75,23)

        self.scrollHolder.addWidget(frame,dcount,0)


        self.friendListCount=dcount+1
        self.FWidList[userName]=frame

class XEditProfile():

    def setupUi(self, MainWindow):
        self.mainWindow=MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(390, 391)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.labelProfilePic = QtWidgets.QLabel(self.centralwidget)
        self.labelProfilePic.setGeometry(QtCore.QRect(10, 30, 120, 140))
        self.labelProfilePic.setStyleSheet("background-color: rgb(255, 0, 0);")
        self.labelProfilePic.setText("")
        self.labelProfilePic.setObjectName("labelProfilePic")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(160, 40, 81, 16))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(160, 70, 81, 16))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(160, 100, 81, 16))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(160, 130, 81, 16))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.labelUserName = QtWidgets.QLabel(self.centralwidget)
        self.labelUserName.setGeometry(QtCore.QRect(260, 40, 81, 16))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        self.labelUserName.setFont(font)
        self.labelUserName.setObjectName("labelUserName")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(160, 160, 81, 16))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(160, 190, 81, 16))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(160, 220, 81, 16))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(160, 250, 81, 16))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.editDiscription = QtWidgets.QPlainTextEdit(self.centralwidget)

        self.editDiscription.setGeometry(QtCore.QRect(160, 280, 211, 91))
        self.editDiscription.setObjectName("editDiscription")
        self.editFullName = QtWidgets.QLineEdit(self.centralwidget)
        self.editFullName.setGeometry(QtCore.QRect(260, 70, 113, 20))
        self.editFullName.setObjectName("editFullName")
        self.editIdentity = QtWidgets.QLineEdit(self.centralwidget)
        self.editIdentity.setGeometry(QtCore.QRect(260, 100, 113, 20))
        self.editIdentity.setObjectName("editIdentity")
        self.radioMale = QtWidgets.QRadioButton(self.centralwidget)
        self.radioMale.setGeometry(QtCore.QRect(260, 130, 31, 17))
        self.radioMale.setObjectName("radioMale")
        self.radioFemale = QtWidgets.QRadioButton(self.centralwidget)
        self.radioFemale.setGeometry(QtCore.QRect(300, 130, 31, 17))
        self.radioFemale.setObjectName("radioFemale")
        self.radioNone = QtWidgets.QRadioButton(self.centralwidget)
        self.radioNone.setGeometry(QtCore.QRect(340, 130, 31, 17))
        self.radioNone.setObjectName("radioNone")
        self.editMobileNo = QtWidgets.QLineEdit(self.centralwidget)
        self.editMobileNo.setGeometry(QtCore.QRect(260, 160, 113, 20))
        self.editMobileNo.setObjectName("editMobileNo")
        self.editEmail = QtWidgets.QLineEdit(self.centralwidget)
        self.editEmail.setGeometry(QtCore.QRect(260, 190, 113, 20))
        self.editEmail.setObjectName("editEmail")
        self.editDOB = QtWidgets.QLineEdit(self.centralwidget)
        self.editDOB.setGeometry(QtCore.QRect(260, 220, 113, 20))
        self.editDOB.setText("")
        self.editDOB.setObjectName("editDOB")
        self.btnSetImage = QtWidgets.QPushButton(self.centralwidget)
        self.btnSetImage.setGeometry(QtCore.QRect(10, 200, 111, 23))
        self.btnSetImage.setObjectName("btnSetImage")
        self.btnPreviewImage = QtWidgets.QPushButton(self.centralwidget)
        self.btnPreviewImage.setGeometry(QtCore.QRect(10, 240, 111, 23))
        self.btnPreviewImage.setObjectName("btnPreviewImage")
        self.btnSaveData = QtWidgets.QPushButton(self.centralwidget)
        self.btnSaveData.setGeometry(QtCore.QRect(10, 280, 111, 23))
        self.btnSaveData.setObjectName("btnSaveData")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(130, 10, 20, 351))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        self.qTimer=QTimer()
        self.qTimer.setInterval(500)
        self.qTimer.timeout.connect(lambda :qTimerRefressFun(self.timerFunList))
        self.qTimer.start()

        _translate = QtCore.QCoreApplication.translate
        self.btnPreviewImage.clicked.connect(self.funPreviewImage)
        self.btnSaveData.clicked.connect(self.uploadData)
        self.btnSetImage.clicked.connect(self.funSetImage)

        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_2.setText(_translate("MainWindow", "User Name "))
        self.label_3.setText(_translate("MainWindow", "Full Name  "))
        self.label_4.setText(_translate("MainWindow", "Identity"))
        self.label_5.setText(_translate("MainWindow", "Gender"))
        self.labelUserName.setText(_translate("MainWindow", "My User Name"))
        self.label_7.setText(_translate("MainWindow", "Mobile No"))
        self.label_8.setText(_translate("MainWindow", "Email"))
        self.label_9.setText(_translate("MainWindow", "Date Of Birth"))
        self.label_10.setText(_translate("MainWindow", "Discription "))
        self.editDiscription.setPlaceholderText(_translate("MainWindow", "This is the Discription"))
        self.editFullName.setPlaceholderText(_translate("MainWindow", "Eg. Your Name"))
        self.editIdentity.setPlaceholderText(_translate("MainWindow", "Eg. Identity"))
        self.radioMale.setText(_translate("MainWindow", "M"))
        self.radioFemale.setText(_translate("MainWindow", "F"))
        self.radioNone.setText(_translate("MainWindow", "N"))
        self.editMobileNo.setPlaceholderText(_translate("MainWindow", "Eg. 123456789"))
        self.editEmail.setPlaceholderText(_translate("MainWindow", "Eg. XXX@gmail.com"))
        self.editDOB.setPlaceholderText(_translate("MainWindow", "Eg. 01/01/0000"))
        self.btnSetImage.setText(_translate("MainWindow", "Set Image"))
        self.btnPreviewImage.setText(_translate("MainWindow", "Preview Image"))
        self.btnSaveData.setText(_translate("MainWindow", "Save Data"))

        self.btnPreviewImage.setDisabled(True)

    def init(self,c):
        self.c=c
        self.imageLoc=""

        self.mainWindow.setWindowTitle("Edit Profile")
        self.mainWindow.closeEvent=self.onClose
        self.timerFunList=[]
        self.refress()


    def refress(self):
        self.c.loadUserProfile(self.c.userName,'_editProfile')
        self.c.functionList['_editProfile']=self.handle

    def onClose(self,event):
        XMainWindow.openWindows['editProfile']=False
        self.c.loadUserProfile(self.c.userName,'_mainWindow')
        event.accept()

    def funSetImage(self):

        file=QFileDialog.getOpenFileName(self.mainWindow)[0]
        if file =="":
            self.btnPreviewImage.setDisabled(True)
        else:
            self.btnPreviewImage.setEnabled(True)
        self.imageLoc=file

    def funPreviewImage(self):

        imgs=cv2.imread(self.imageLoc)
        if imgs is not None:
            imgs=cv2.resize(imgs,(120,140))
            pix=pqc.cv2toPqImage(imgs)

            self.labelProfilePic.setPixmap(pix)
        else:
            showResult(self.statusbar,"Image Location Error/File Not supported")



    def uploadData(self):

        #print("I am uploading data")
        #print(self.imageLoc == '')
        #time.sleep(0.1)
        name=self.editFullName.text()
        if name!=self.tempData['name']:

            nm=lec.checkName(name)

            if nm==True:

                self.c.editProfile('name',name)
            else:
                showResult(self.statusbar,nm)

        identityU=self.editIdentity.text()
        if identityU!=self.tempData['identityU']:
            ids=lec.checkIdentity(identityU)
            if ids==True:
                self.c.editProfile('identityU',identityU)
            else:
                showResult(self.statusbar,ids)

        if(self.radioMale.isChecked()):
            gender=1
        elif self.radioFemale.isChecked():
            gender=2
        else:
            gender=0

        gender=str(gender)
        if gender!=self.tempData['gender']:
            self.c.editProfile('gender',gender)


        contactNo=self.editMobileNo.text()
        if contactNo!=self.tempData['contactNo']:
            cN=lec.checkPNumber(contactNo)
            if cN==True:

                self.c.editProfile('contactNo',contactNo)
            else:
                showResult(self.statusbar,cN)

        email=self.editEmail.text()
        if email!=self.tempData['email']:
            em=lec.checkEmail(email)
            if em==True:
                self.c.editProfile('email',email)
            else:
                showResult(self.statusbar,em)

        dob=self.editDOB.text()
        if dob!=self.tempData['dateOfBirth']:
            db=lec.checkDob(dob)
            if db==True:
                self.c.editProfile('dateOfBirth',dob)
            else:
                showResult(self.statusbar,db)


        dis=self.editDiscription.toPlainText()
        if dis!=self.tempData['discription']:
            di=lec.checkDiscription(dis)
            if di==True:
                self.c.editProfile('discription',dis)
            else:
                showResult(self.statusbar,di)


        if self.imageLoc!='' and self.imageLoc!='_None':
            self.c.editProfile('locProfilePic','imgData',self.imageLoc)

            self.funPreviewImage()




        self.c.functionList['_editProfile']=self.handle
        self.btnSaveData.setDisabled(True)

    def handle(self,msg):
        def fun():
            if 'userName' in msg:
                self.handleRefress(msg)
            else:
                self.handleResponse(msg)

        self.timerFunList.append(fun)

    def handleResponse(self,msg):

        if msg['code']=='0009':
            showResult(self.statusbar,"Updation Completed",False)

    def handleRefress(self,msg):
        self.tempData=msg

        userName=msg['userName']
        name=msg['name']

        img=ds.remodifyData(msg['profileData'],msg['profileType'],msg['profileShape'])
        shape=img.shape

        img=cv2.resize(img,(120,140))
        img=pqc.cv2toPqImage(img)

        self.labelUserName.setText(userName)

        self.editFullName.setText(name)
        self.editMobileNo.setText(msg['contactNo'])

        self.editIdentity.setText(msg['identityU'])
        self.editDOB.setText(msg['dateOfBirth'])

        #self.editDiscription.setText(msg['discription'])
        self.editDiscription.setPlainText(msg['discription'])
        self.editEmail.setText(msg['email'])
        dis=msg['discription']
        #self.editDiscription.setText(dis)
        g=msg['gender']
        if g=='1':
            self.radioMale.setChecked(True)
        elif g=='2':
            self.radioFemale.setChecked(True)
        else:
            self.radioNone.setChecked(True)

        self.labelProfilePic.setPixmap(img)

class XNotification():

    def setupUi(self, MainWindow):
        self.mainWindow=MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(277, 334)
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

        self.label.setText("Notification")

        self.btnLoadNotification=QPushButton(self.centralwidget)
        self.btnLoadNotification.setText("Load Notification")
        self.btnLoadNotification.move(170,20)
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
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")

        self.scrollContainer,self.scrollHolder=pqc.scrollBar(self.centralwidget,20,60,240,250)


        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        self.qTimer=QTimer()
        self.qTimer.setInterval(500)
        self.qTimer.timeout.connect(lambda :qTimerRefressFun(self.timerFunList))
        self.qTimer.start()

        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btnLoadNotification.clicked.connect(self.loadNotif)

    def init(self,c):
        self.c=c
        self.r1=0
        self.r2=100
        self.notifcationData=None

        self.timerFunList=[]

        self.refress()
        self.count=0
        self.btnLoadNotification.close()
        self.mainWindow.setWindowTitle("Notifications")
        self.mainWindow.closeEvent=self.onClose



    def onClose(self,event):
        XMainWindow.openWindows['notification']=False
        event.accept()

    def refressList(self):
        for i in self.scrollContainer.children():
            i.deleteLater()

    def destroyElement(self):
        for i in self.scrollContainer.children()[1:]:
            i.deleteLater()

    def loadNotif(self):
        #self.destroyElement()
        def fun():
            self.btnLoadNotification.close()
            d=self.notifcationData
            self.importData(d)
        lc.timerFunList.append(fun)

    def refress(self):
        self.c.loadNotification(self.r1,self.r2)
        self.c.functionList['_loadNotification']=self.handle

    def importData(self,data):

        data=data[::-1]

        for i in data:

            frame=QFrame(self.scrollContainer)

            label=QLabel(frame)
            label.setGeometry(10,5,221,16)

            label.setText(i[1])
            label.setWordWrap(True)
            label.setFixedWidth(221)
            font = QtGui.QFont()
            font.setFamily("Times New Roman")
            font.setPointSize(10)
            label.setFont(font)
            label.adjustSize()

            frame.adjustSize()

            self.scrollHolder.addWidget(frame,self.count,1)


            self.count=self.count+1

    def handle(self,msg):

        def fun():
            code=msg['code']

            if code=='kk01':
                showResult(self.statusbar,"No Records found",True)
                self.dataLengthIsZero=True


            elif code=='001k':

                showResult(self.statusbar,"Data founded")
                data=ds.remodifyData(msg['notifData'],msg['notifType'],msg['notifShape'])


                self.notifcationData=data
                self.loadNotif()
            else:
                showResult(self.statusbar,"Error :"+code)

        self.timerFunList.append(fun)

class XBlockUnblock():

    def setupUi(self, MainWindow):
        self.mainWindow=MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(428, 367)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 20, 81, 31))
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
        self.editUserName.setObjectName("editUserName")
        self.btnSearch = QtWidgets.QPushButton(self.centralwidget)
        self.btnSearch.setGeometry(QtCore.QRect(20, 110, 75, 23))
        self.btnSearch.setObjectName("btnSearch")

        self.btnLoadList=QPushButton(self.centralwidget)
        self.btnLoadList.setText("Load List")
        self.btnLoadList.setGeometry(120,110,75,23)
        self.btnLoadList.clicked.connect(self.funLoadList)
        self.btnLoadList.close()

        self.btnRefressList=QPushButton(self.centralwidget)
        self.btnRefressList.setText("Refress List")
        self.btnRefressList.setGeometry(340,70,75,23)
        self.btnRefressList.clicked.connect(self.funRefressList)

        self.scrollContainer1,self.scrollHolder1=pqc.scrollBar(self.centralwidget,20,150,180,190)
        self.scrollContainer2,self.scrollHolder2=pqc.scrollBar(self.centralwidget,240,110,180,230)


        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(240, 20, 111, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(22)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setMouseTracking(True)
        self.label_2.setMidLineWidth(1)
        self.label_2.setObjectName("label_2")
        self.btnLoadList = QtWidgets.QPushButton(self.centralwidget)
        self.btnLoadList.setGeometry(QtCore.QRect(240, 70, 75, 23))
        self.btnLoadList.setObjectName("btnLoadList")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(200, 20, 20, 291))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):

        self.qTimer=QTimer()
        self.qTimer.setInterval(500)
        self.qTimer.timeout.connect(lambda :qTimerRefressFun(self.timerFunList))
        self.qTimer.start()

        self.btnSearch.clicked.connect(self.funBtnBlockSearch)
        self.btnLoadList.clicked.connect(self.funBtnUnblockLoad)
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Block"))
        self.editUserName.setPlaceholderText(_translate("MainWindow", "UserName"))
        self.btnSearch.setText(_translate("MainWindow", "Search"))
        self.label_2.setText(_translate("MainWindow", "Unblock"))
        self.btnLoadList.setText(_translate("MainWindow", "Load List"))

    def init(self,c):
        self.c=c
        self.searchData=None
        self.unblockData=None
        self.count1=0
        self.count2=0
        self.FWidList1={}
        self.FWidList2={}

        self.timerFunList=[]


        self.mainWindow.setWindowTitle("Blcok Unblock")
        self.mainWindow.closeEvent=self.onClose

        self.btnRefressList.close()


    def onClose(self,event):
        XMainWindow.openWindows['blockUnblock']=False
        event.accept()

    def funLoadList(self):
        self.destroyElement(self.scrollContainer1)
        for i in self.searchData:
            self.importDataB(i)

    def funRefressList(self):
        self.destroyElement(self.scrollContainer2)
        for i in self.unblockData:
            self.importDataU(i)

    def destroyElement(self,scrollContainer):
        for i in scrollContainer.children()[1:]:
            i.deleteLater()

    def funBtnBlockSearch(self):
        self.c.functionList['_blockSearch']=self.handle
        userName=self.editUserName.text()

        usr=lec.checkUserName(userName)
        if usr==True:
            self.c.blockSearch(userName)
            self.btnSearch.setDisabled(True)
        else:
            showResult(self.statusbar,usr)

    def funBtnUnblockLoad(self):
        self.c.functionList['_unblockLoad']=self.handle
        self.btnLoadList.setDisabled(True)
        self.c.unblockLoad()

    def handle(self,msg):

        def fun():

            if msg['wType']=='_unblockLoad':
                self.btnLoadList.setEnabled(True)
                self.handleUnblock(msg)

            elif msg['wType']=='_blockSearch':
                self.btnSearch.setEnabled(True)
                self.handleBlock(msg)
            elif msg['wType']=='_block':
                self.handleBlockOnly(msg)
            elif msg['wType']=='_unblock':
                self.handleUnblockOnly(msg)
            else:
                showResult(self.statusbar,"Error :",msg['wType'])

        self.timerFunList.append(fun)

    def importDataB(self,data):

        i=data
        userName=i[0]
        name=i[1]

        imgData=ds.remodifyData(i[2],i[3],i[4])
        imgData=cv2.resize(imgData,(60,80))
        dcount=self.count1

        def funBlock():
            list=self.FWidList1[userName]
            list.deleteLater()

            self.c.functionList['_block']=self.handle
            self.c.block(userName)

        frame =QFrame(self.scrollContainer1)


        labelProfile=QLabel(frame)
        labelProfile.setGeometry(10,5,60,80)
        labelProfile.setFixedSize(60,80)
        imgData=cv2.resize(imgData,(60,80))
        image=pqc.cv2toPqImage(imgData)
        labelProfile.setPixmap(image)



        labelFullName=QLabel(frame)
        labelFullName.setGeometry(80,5,91,16)
        labelFullName.setFixedSize(130,12)
        font = QtGui.QFont()
        font.setPointSize(8)
        labelFullName.setFont(font)
        labelFullName.setText(name)
        labelFullName.adjustSize()

        labelUserName=QLabel(frame)
        labelUserName.setGeometry(80,32,81,16)
        labelUserName.setFixedSize(130,12)
        font.setPointSize(8)
        labelUserName.setFont(font)
        labelUserName.setText(userName)
        labelUserName.adjustSize()


        btnChatWindow=QPushButton(frame)
        btnChatWindow.setGeometry(80,60,75,23)
        btnChatWindow.setText("Block")
        btnChatWindow.clicked.connect(funBlock)



        self.scrollHolder1.addWidget(frame,dcount,0)



        self.count1=dcount+1

        self.FWidList1[userName]=frame

    def importDataU(self,data):

        i=data
        userName=i[0]
        name=i[1]

        imgData=ds.remodifyData(i[2],i[3],i[4])
        imgData=cv2.resize(imgData,(60,80))
        dcount=self.count2

        def funUnblock():
            list=self.FWidList2[userName]
            list.deleteLater()

            self.c.functionList['_unblock']=self.handle
            self.c.unblock(userName)

        frame=QFrame(self.scrollContainer2)
        frame.setFixedSize(200,85)
        labelProfile=QLabel(frame)
        labelProfile.setGeometry(10,5,60,80)
        imgData=cv2.resize(imgData,(60,80))
        image=pqc.cv2toPqImage(imgData)
        labelProfile.setPixmap(image)



        labelFullName=QLabel(frame)
        labelFullName.setGeometry(80,5,91,15)
        font = QtGui.QFont()
        font.setPointSize(11)
        labelFullName.setFont(font)
        labelFullName.setText(name)
        labelFullName.adjustSize()

        labelUserName=QLabel(frame)
        labelUserName.setGeometry(80,32,81,16)
        labelUserName.setFixedSize(130,13)
        font.setPointSize(8)
        labelUserName.setFont(font)
        labelUserName.setText(userName)
        labelUserName.adjustSize()

        btnChatWindow=QPushButton(frame)
        btnChatWindow.setText("Unblock")
        btnChatWindow.clicked.connect(funUnblock)
        btnChatWindow.setGeometry(80,60,75,23)



        self.scrollHolder2.addWidget(frame,dcount,0)
        frame.adjustSize()



        self.count2=dcount+1
        self.FWidList2[userName]=frame

    def handleBlock(self,msg):

        code=msg['code']

        if code=='0019':
            showResult(self.statusbar,"No Block Search Result Found",False)
        #   No Records found
        elif code=='0013':
            showResult(self.statusbar,"No Block Search Result Found",False)

        elif code=='0020':
            def fun():
                data=ds.remodifyData(msg['usersData'],msg['usersType'],msg['usersShape'])

                showResult(self.statusbar,str(len(data))+" Block Search Result Found",False)

                self.searchData=data
                self.funLoadList()

            lc.timerFunList.append(fun)

        else:
            showResult(self.statusbar,"Error :"+code)

    def handleUnblock(self,msg):


        code=msg['code']

        if code=='0022':
            showResult(self.statusbar,"No Unblock Data Founded",False)
            # No Records found
        elif code=='0023':
            def fun():
                data=ds.remodifyData(msg['usersData'],msg['usersType'],msg['usersShape'])
                showResult(self.statusbar,str(len(data))+" Unblock Data Founded",False)

                self.unblockData=data
                self.funRefressList()

            lc.timerFunList.append(fun)
        else:
            showResult(self.statusbar,"Error :"+code)

    def handleBlockOnly(self,msg):
        code=msg['code']

        if code=='0021':
            showResult(self.statusbar,'Blocking successfull',False)
            self.c.friendListLoad(self.c.userName,'_mainWindow')
        else:
            showResult(self.statusbar,'Blocking Unsuccessfull')

    def handleUnblockOnly(self,msg):
        code=msg['code']

        if code=='0024':
            showResult(self.statusbar,'Unblocking successfull',False)
        else:
            showResult(self.statusbar,'Unblocking Unsuccessfull')

class XSequrity():

    def setupUi(self, MainWindow):
        self.mainWindow=MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(408, 243)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.btnUpdateSequrity = QtWidgets.QPushButton(self.centralwidget)
        self.btnUpdateSequrity.setGeometry(QtCore.QRect(250, 190, 91, 23))
        self.btnUpdateSequrity.setObjectName("btnUpdateSequrity")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(192, 20, 20, 201))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.editSeqA = QtWidgets.QLineEdit(self.centralwidget)
        self.editSeqA.setGeometry(QtCore.QRect(249, 140, 113, 20))
        self.editSeqA.setObjectName("editSeqA")
        self.btnUpdatePassword = QtWidgets.QPushButton(self.centralwidget)
        self.btnUpdatePassword.setGeometry(QtCore.QRect(50, 140, 101, 23))
        self.btnUpdatePassword.setObjectName("btnUpdatePassword")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 201, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setMouseTracking(True)
        self.label.setMidLineWidth(1)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(219, 10, 181, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setMouseTracking(True)
        self.label_2.setMidLineWidth(1)
        self.label_2.setObjectName("label_2")
        self.editSeqQ = QtWidgets.QLineEdit(self.centralwidget)
        self.editSeqQ.setGeometry(QtCore.QRect(249, 100, 113, 20))
        self.editSeqQ.setObjectName("editSeqQ")
        self.editCurrentPassword = QtWidgets.QLineEdit(self.centralwidget)
        self.editCurrentPassword.setGeometry(QtCore.QRect(249, 60, 113, 20))
        self.editCurrentPassword.setObjectName("editCurrentPassword")
        self.editOldPassword = QtWidgets.QLineEdit(self.centralwidget)
        self.editOldPassword.setGeometry(QtCore.QRect(49, 60, 113, 20))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.editOldPassword.setFont(font)
        self.editOldPassword.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.editOldPassword.setObjectName("editOldPassword")
        self.editNewPassword = QtWidgets.QLineEdit(self.centralwidget)
        self.editNewPassword.setGeometry(QtCore.QRect(49, 100, 113, 16))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setBold(False)
        font.setWeight(50)
        self.editNewPassword.setFont(font)
        self.editNewPassword.setObjectName("editNewPassword")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        self.qTimer=QTimer()
        self.qTimer.setInterval(500)
        self.qTimer.timeout.connect(lambda :qTimerRefressFun(self.timerFunList))
        self.qTimer.start()
        _translate = QtCore.QCoreApplication.translate
        self.btnUpdatePassword.clicked.connect(self.btnFunUpdatePass)
        self.btnUpdateSequrity.clicked.connect(self.btnFunUpdateSeq)
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btnUpdateSequrity.setText(_translate("MainWindow", "Update Sequrity"))
        self.editSeqA.setPlaceholderText(_translate("MainWindow", "Sequrity Answer"))
        self.btnUpdatePassword.setText(_translate("MainWindow", "Update Password"))
        self.label.setText(_translate("MainWindow", "Change Password"))
        self.label_2.setText(_translate("MainWindow", "Change Sequrity Q/A"))
        self.editSeqQ.setPlaceholderText(_translate("MainWindow", "Sequrity Question"))
        self.editCurrentPassword.setPlaceholderText(_translate("MainWindow", "Current Password"))
        self.editOldPassword.setPlaceholderText(_translate("MainWindow", "Old Password"))
        self.editNewPassword.setPlaceholderText(_translate("MainWindow", "New Password"))

    def init(self,c):
        self.c=c
        self.mainWindow.setWindowTitle("Sequrity")
        self.timerFunList=[]

        self.mainWindow.closeEvent=self.onClose

    def onClose(self,event):
        XMainWindow.openWindows['sequrity']=False
        event.accept()

    def handle(self,msg):

        def fun():
            code=msg['code']
            self.btnUpdateSequrity.setEnabled(True)
            self.btnUpdatePassword.setEnabled(True)
            if code=='0005':
                showResult(self.statusbar,"Password Updated",False)
            elif code=='0006':
                showResult(self.statusbar,"Old Password is incorrect")
            elif code=='0011':
                showResult(self.statusbar,"Sequrity Question and Answer updated",False)
            elif code=='0010':
                showResult(self.statusbar,"Password is incorrect")
            else:
                showResult(self.statusbar,"Error :"+code)

        self.timerFunList.append(fun)

    def btnFunUpdatePass(self):
        self.c.functionList['_changePassword']=self.handle

        oldPass=self.editOldPassword.text()
        newPass=self.editNewPassword.text()

        op=lec.checkUserPassword(oldPass)
        np=lec.checkUserPassword(newPass)

        if op==True:
            if np==True:
                self.c.changePassword(self.c.userName,oldPass,newPass)
                self.btnUpdateSequrity.setDisabled(True)
                self.btnUpdatePassword.setDisabled(True)
            else:
                showResult(self.statusbar,np)
        else:
            showResult(self.statusbar,op)



    def btnFunUpdateSeq(self):
        self.c.functionList['_changeSeqQA']=self.handle

        currenPass=self.editCurrentPassword.text()
        seqQ=self.editSeqQ.text()
        seqA=self.editSeqA.text()

        cp=lec.checkUserPassword(currenPass)
        sQ=lec.checkSequrityQuestion(seqQ)
        sA=lec.checkSequrityAnswer(seqA)

        if cp==True:
            if sQ==True:
                if sA==True:
                    self.c.changeSeqQA(seqQ,seqA,currenPass)
                    self.btnUpdateSequrity.setDisabled(True)
                    self.btnUpdatePassword.setDisabled(True)
                else:
                    showResult(self.statusbar,sA)
            else:
                showResult(self.statusbar,sQ)
        else:
            showResult(self.statusbar,cp)

class XFriendRequest():
    def setupUi(self, MainWindow):
        self.mainWindow=MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(285, 324)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 20, 191, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setSizeIncrement(QtCore.QSize(0, 0))

        self.btnLoad=QPushButton(self.centralwidget)
        self.btnLoad.setText("Load")
        self.btnLoad.setGeometry(220,30,51,23)
        self.btnLoad.clicked.connect(self.funLoad)

        self.scrollContainer,self.scrollHolder=pqc.scrollBar(self.centralwidget,20,60,250,230)

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
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        self.qTimer=QTimer()
        self.qTimer.setInterval(500)
        self.qTimer.timeout.connect(lambda :qTimerRefressFun(self.timerFunList))
        self.qTimer.start()
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Friend Request"))

    def funLoad(self):
        self.destroyElement()
        for i in self.requestList:
            self.importData(i)

    def destroyElement(self):
        for i in self.scrollContainer.children()[1:]:
            i.deleteLater()

    def init(self,c):
        self.c=c

        self.timerFunList=[]

        self.requestList=None
        self.refress()
        self.count=0
        self.FWidList={}
        self.btnLoad.close()
        self.mainWindow.setWindowTitle("Friend Request")
        self.mainWindow.closeEvent=self.onClose

    def onClose(self,event):
        XMainWindow.openWindows['friendRequest']=False
        event.accept()

    def refress(self):
        self.c.loadFriendRequest()
        self.c.functionList['_loadFriendRequest']=self.handle

    def importData(self,data):

        i=data
        userName=i[0]
        name=i[1]

        imgData=ds.remodifyData(i[2],i[3],i[4])
        imgData=cv2.resize(imgData,(60,80))
        dcount=self.count

        def funBlock():
            list=self.FWidList[userName]
            list.deleteLater()
            self.c.functionList['_friendRequestAccept']=self.handle
            self.c.friendRequestAccept(userName)

        frame=QFrame(self.scrollContainer)
        frame.setFixedSize(200,85)

        labelProfile=QLabel(frame)
        labelProfile.setGeometry(10,5,60,80)
        imgData=cv2.resize(imgData,(60,80))
        image=pqc.cv2toPqImage(imgData)
        labelProfile.setPixmap(image)



        labelFullName=QLabel(frame)
        labelFullName.setGeometry(80,5,91,16)
        font = QtGui.QFont()
        font.setPointSize(8)
        labelFullName.setFont(font)
        labelFullName.setText(name)

        labelUserName=QLabel(frame)
        labelUserName.setGeometry(80,32,81,16)
        font.setPointSize(8)
        labelUserName.setFont(font)
        labelUserName.setText(userName)


        btnChatWindow=QPushButton(frame)
        btnChatWindow.setGeometry(80,60,75,23)
        btnChatWindow.setText("Accept")
        btnChatWindow.clicked.connect(funBlock)



        self.scrollHolder.addWidget(frame,dcount,0)




        self.count=dcount+1

        self.FWidList[userName]=frame

    def handleFriendRequestLoad(self,msg):
        code=msg['code']

        if code=='ss01':
            showResult(self.statusbar,"No Records found")
        elif code=='kks1':
            def fun():

                data=ds.remodifyData(msg['usersData'],msg['usersType'],msg['usersShape'])
                showResult(self.statusbar,str(len(data))+" Records found",False)
                self.requestList=data
                self.funLoad()

            lc.timerFunList.append(fun)
        else:
            showResult(self.statusbar,"Error :"+code)

    def handleFriendRequestAccept(self,msg):
        code=msg['code']

        if code=='0027':
            showResult(self.statusbar,"Friend Request Accept Successfull",False)
            self.c.friendListLoad(self.c.userName,'_mainWindow')

        else:
            showResult(self.statusbar,"Error :"+code)

    def handle(self,msg):

        def fun():
            wType=msg['wType']

            if wType=='_loadFriendRequest':
                self.handleFriendRequestLoad(msg)
            elif wType=='_friendRequestAccept':
                self.handleFriendRequestAccept(msg)
            else:
                showResult(self.statusbar,"Error :"+wType)

        self.timerFunList.append(fun)

class XFindFriends():
    def setupUi(self, MainWindow):
        self.mainWindow=MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(278, 372)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 20, 161, 31))
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

        self.btnLoad=QPushButton(self.centralwidget)
        self.btnLoad.setText("Load")
        self.btnLoad.setGeometry(190,40,60,23)
        self.btnLoad.clicked.connect(self.funLoadData)


        self.scrollContainer,self.scrollHolder=pqc.scrollBar(self.centralwidget,30,120,220,230)

        self.label.setFont(font)
        self.label.setMouseTracking(True)
        self.label.setMidLineWidth(1)
        self.label.setObjectName("label")
        self.editUserName = QtWidgets.QLineEdit(self.centralwidget)
        self.editUserName.setGeometry(QtCore.QRect(30, 60, 113, 20))
        self.editUserName.setObjectName("editUserName")
        self.btnSearch = QtWidgets.QPushButton(self.centralwidget)
        self.btnSearch.setGeometry(QtCore.QRect(180, 80, 75, 23))
        self.btnSearch.setObjectName("btnSearch")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")


        self.checkStrictSearch=QCheckBox(self.centralwidget)
        self.checkStrictSearch.setText("Strict Search")
        self.checkStrictSearch.setGeometry(30,85,91,17)
        self.checkStrictSearch.clicked.connect(self.funCheckStritSearch)



        self.btnSearch.clicked.connect(self.funBtnSearch)
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        self.qTimer=QTimer()
        self.qTimer.setInterval(500)
        self.qTimer.timeout.connect(lambda :qTimerRefressFun(self.timerFunList))
        self.qTimer.start()
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Find Friends"))
        self.editUserName.setPlaceholderText(_translate("MainWindow", "User Name"))
        self.btnSearch.setText(_translate("MainWindow", "Search"))

    def init(self,c):
        self.c=c
        self.dataList=None
        self.count=0
        self.stritCond='0'
        self.timerFunList=[]

        self.isSearched=False

        self.FWidList={}
        self.btnLoad.close()
        self.mainWindow.setWindowTitle("Find Friends")
        self.mainWindow.closeEvent=self.onClose


        self.refress()

    def funCheckStritSearch(self):
        if self.checkStrictSearch.isChecked():
            self.stritCond='1'
        else:
            self.stritCond='0'

    def refress(self):
        self.c.refressSearch()
        self.c.functionList['refressSearch']=self.handle

    def onClose(self,event):
        XMainWindow.openWindows['findFriend']=False
        event.accept()

    def destroyElement(self):
        for i in self.scrollContainer.children()[1:]:
            i.deleteLater()

    def funLoadData(self):
        self.destroyElement()
        for i in self.dataList:
            self.importData(i)



    def handleSearchResponse(self,msg):
        code=msg['code']

        if code=='0012' or code=='0013':
            showResult(self.statusbar,"No Records Found")
        elif code=='0014':
            def fun():
                data=ds.remodifyData(msg['usersData'],msg['usersType'],msg['usersShape'])
                showResult(self.statusbar,str(len(data))+" Records Found",False)

                self.dataList=data
                self.funLoadData()

            lc.timerFunList.append(fun)
        else:
            showResult(self.statusbar,"Error :"+code)

    def handleSendFriendRequest(self,msg):
        code=msg['code']

        if code=='0014':
            showResult(self.statusbar,"Friend Request Already Sent")
        elif code=='0015':
            showResult(self.statusbar,"Already Friends")
        elif code=='0016':
            showResult(self.statusbar,"Request Sending Successfull",False)
        else:
            showResult(self.statusbar,"Error :"+code)

    def handle(self,msg):

        def fun():
            wType=msg['wType']

            if wType=='_searchFriend':
                self.handleSearchResponse(msg)
            elif wType=='_sendFriendRequest':
                self.handleSendFriendRequest(msg)
            elif wType=='refressSearch':
                self.handleRefress(msg)
            else:
                showResult(self.statusbar,"Error :"+wType)

        self.timerFunList.append(fun)

    def handleRefress(self,msg):
        if not self.isSearched:
            code=msg['code']
            if code=='0014':
                def fun():
                    data=ds.remodifyData(msg['usersData'],msg['usersType'],msg['usersShape'])
                    #showResult(self.statusbar,str(len(data))+" Records Found",False)

                    self.dataList=data
                    self.funLoadData()

                lc.timerFunList.append(fun)
            else:
                showResult(self.statusbar,"Error :"+code)

    def funBtnSearch(self):
        userName=self.editUserName.text()
        self.c.functionList['_searchFriend']=self.handle

        usr=lec.checkUserName(userName)
        if usr==True:
            self.c.searchFriend(userName,self.stritCond)
            self.isSearched=True
            self.destroyElement()
        else:
            showResult(self.statusbar,usr)



    def importData(self,data):

        i=data
        userName=i[0]
        name=i[1]

        imgData=ds.remodifyData(i[2],i[3],i[4])
        imgData=cv2.resize(imgData,(60,80))
        dcount=self.count

        def funBlock():
            list=self.FWidList[userName]
            list.deleteLater()

            self.c.functionList['_sendFriendRequest']=self.handle
            self.c.sendFriendRequest(userName)

        frame=QFrame(self.scrollContainer)
        frame.setFixedSize(200,80)


        labelProfile=QLabel(frame)
        labelProfile.setGeometry(10,5,60,80)
        imgData=cv2.resize(imgData,(60,80))
        image=pqc.cv2toPqImage(imgData)
        labelProfile.setPixmap(image)



        labelFullName=QLabel(frame)
        labelFullName.setGeometry(80,5,91,16)
        font = QtGui.QFont()
        font.setPointSize(8)
        labelFullName.setFont(font)
        labelFullName.setText(name)

        labelUserName=QLabel(frame)
        labelUserName.setGeometry(80,32,81,16)
        font.setPointSize(8)
        labelUserName.setFont(font)
        labelUserName.setText(userName)


        btnChatWindow=QPushButton(frame)
        btnChatWindow.setGeometry(80,55,75,23)
        btnChatWindow.setText("Add Friend")
        btnChatWindow.clicked.connect(funBlock)



        self.scrollHolder.addWidget(frame,dcount,0)

        self.count=dcount+1
        #frame.adjustSize()
        self.FWidList[userName]=frame

class XGroupChat():

    def setupUi(self, MainWindow):
        self.mainWindow=MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(431, 324)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(40, 20, 121, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.btnCreateGroup = QtWidgets.QPushButton(self.centralwidget)
        self.btnCreateGroup.setGeometry(QtCore.QRect(260, 60, 81, 23))
        self.btnCreateGroup.setObjectName("btnCreateGroup")
        self.btnSearchGroup = QtWidgets.QPushButton(self.centralwidget)
        self.btnSearchGroup.setGeometry(QtCore.QRect(260, 100, 81, 23))
        self.btnSearchGroup.setObjectName("btnSearchGroup")
        self.btnGroupRequest = QtWidgets.QPushButton(self.centralwidget)
        self.btnGroupRequest.setGeometry(QtCore.QRect(260, 140, 81, 23))
        self.btnGroupRequest.setObjectName("btnGroupRequest")

        self.btnLoadList=QPushButton(self.centralwidget)
        self.btnLoadList.setText("Load List")
        self.btnLoadList.setGeometry(140,20,75,23)
        self.btnLoadList.clicked.connect(self.funLoadList)

        self.scrollContainer,self.scrollHolder=pqc.scrollBar(self.centralwidget,10,60,220,240)

        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(240, 60, 16, 231))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        self.qTimer=QTimer()
        self.qTimer.setInterval(500)
        self.qTimer.timeout.connect(lambda :qTimerRefressFun(self.timerFunList))
        self.qTimer.start()
        self.btnCreateGroup.clicked.connect(self.funCreateGroup)
        self.btnSearchGroup.clicked.connect(self.funSearchGroup)
        self.btnGroupRequest.clicked.connect(self.funGroupRequest)

        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_12.setText(_translate("MainWindow", "Group List"))
        self.btnCreateGroup.setText(_translate("MainWindow", "Create Group"))
        self.btnSearchGroup.setText(_translate("MainWindow", "Search Group"))
        self.btnGroupRequest.setText(_translate("MainWindow", "Group Request"))
        '''
        self.qTimer=QTimer()
        self.qTimer.setInterval(1000)
        self.qTimer.timeout.connect(self.funLoadList)
        self.qTimer.start()
        '''

    def init(self,c):
        self.c=c
        self.send=c.send
        self.gc=xcs.GroupChat(self.send)
        self.ig=xcs.InfoGetter(self.send)


        self.isAlreadySearched=False

        self.count=0
        self.FWidList={}
        self.dataList=None
        self.winControlPanel=None
        self.winChatWindow=None

        self.timerFunList=[]

        self.btnLoadList.close()

        self.viewDict={}

        self.initiate()

        lc.gcCond=False
        self.mainWindow.setWindowTitle("Group Chat")
        self.mainWindow.closeEvent=self.onClose

    def handleInfoGroupRequest(self,msg):
        code=msg['code']

        if code=='U53e':
            gr=msg['groupRequest']

            if gr!='True':
                colorButton(self.btnGroupRequest)
        else:
            print("UNknow Group Information Error :"+code)


    def handleInfoGC(self,msg):
        code=msg['code']

        if code=='45t6':

            data=ds.remodifyData(msg['data'],msg['dataType'],msg['dataShape'])
            for i in data:
                groupName,cp,c=i
                self.viewDict[groupName]=[cp,c]
        else:
            print("THIS IS ERROR CODE :"+code)

    def onClose(self,event):
        XMainWindow.openWindows['groupChat']=False
        event.accept()


    def funLoadList(self):
        for  i in self.scrollContainer.children()[1:]:
            i.deleteLater()

        def funInit(gName):
            frame=QFrame(self.scrollContainer)
            frame.setFixedSize(200,61)

            label=QLabel(frame)
            label.setGeometry(10,5,201,16)
            font = QtGui.QFont()
            font.setPointSize(12)
            label.setText(gName)
            dcount=self.count

            def funControlPanel():
                self.mainWindow.close()
                mainWindow=QMainWindow()
                lc.varStore['GroupChatControlPanel']=mainWindow
                lc.gcCond=True

                XMainWindow.openWindows['groupChat']=True
                self.winControlPanel=lc.XGroupChatControlPanel()
                colorButton(btnControlPanel,color=None)
                self.winControlPanel.setupUi(mainWindow)
                self.winControlPanel.btnBack.clicked.connect(lambda :self.funBack(mainWindow))
                self.winControlPanel.init(self.c,gName)
                self.winControlPanel.btnSearch.clicked.connect(self.winControlPanel.funSearchList)
                self.gc.groupControlPanel(gName)
                mainWindow.show()

            def funChatWindow():
                self.mainWindow.close()
                mainWindow=QMainWindow()

                lc.gcCond=True
                XMainWindow.openWindows['groupChat']=True
                lc.varStore['GroupChatControlPanel']=mainWindow
                self.winChatWindow=lc.XGroupChatChatWindow()
                self.winChatWindow.setupUi(mainWindow)

                colorButton(btnChatWindow,color=None)
                self.winChatWindow.btnBack.clicked.connect(lambda :self.funBack(mainWindow))
                self.winChatWindow.init(self.c,gName)
                self.gc.groupChatWindow(gName)

                mainWindow.show()


            btnControlPanel=QPushButton(frame)
            btnControlPanel.setText("Control Panel")
            btnControlPanel.clicked.connect(funControlPanel)
            btnControlPanel.setGeometry(10,30,75,23)


            btnChatWindow=QPushButton(frame)
            btnChatWindow.setText("Chat Window")
            btnChatWindow.clicked.connect(funChatWindow)
            btnChatWindow.setGeometry(110,30,75,23)

            if gName in self.viewDict:
                cp,chat=self.viewDict[gName]
                if cp=='False':
                    colorButton(btnControlPanel)
                if chat=='False':
                    colorButton(btnChatWindow)

            self.scrollHolder.addWidget(frame,dcount,0)

            self.count=dcount+1

            self.FWidList[gName]=frame

        if self.dataList is not None:
            data=self.dataList
            for i in data:
                funInit(i[1])
            #self.qTimer.stop()

    def initiate(self):
        window='GroupChat'
        self.c.functionList[window]=self.handle
        self.c.functionList['LocaliGGetInformation']=self.handleInfoGroupRequest

        self.c.functionList['LocaliGGetInfoG']=self.handleInfoGC


        self.ig.iGGetInfoG()
        self.ig.iGGetInformation('Local')

        self.gc.refressGC()



    def funCreateGroup(self):
        self.mainWindow.close()

        mainWindow=QMainWindow()
        lc.varStore['GroupChatCreateGroup']=mainWindow
        lc.gcCond=True
        XMainWindow.openWindows['groupChat']=True
        self.gccg=lc.XGroupChatCreateGroup()
        self.gccg.setupUi(mainWindow)
        self.gccg.btnBack.clicked.connect(lambda : self.funBack(mainWindow))
        self.gccg.btnCreate.clicked.connect(self.funBtnCreateGroup)
        mainWindow.show()

    def funBtnCreateGroup(self):
        groupName=self.gccg.editGroupName.text()
        gName=lec.checkGroupName(groupName)
        if gName==True:
            self.gc.createGroup(groupName)
            self.btnCreateGroup.setDisabled(True)
        else:
            showResult(self.gccg.statusbar,gName)


    def funBack(self,mainWindow):
        self.mainWindow.show()
        lc.gcCond=True
        XMainWindow.openWindows['groupChat']=True
        mainWindow.destroy()
        self.initiate()

    def funSearchGroup(self):
        self.mainWindow.close()
        mainWindow=QMainWindow()
        lc.varStore['GroupChatSearchGroup']=mainWindow
        lc.gcCond=True
        XMainWindow.openWindows['groupChat']=True
        self.gcsg=lc.XGroupChatSearchGroup()
        self.gcsg.setupUi(mainWindow)
        self.gcsg.init(self.c)
        self.gcsg.btnSearch.clicked.connect(self.funBtnSearchGroup)

        mainWindow.show()

    def funBtnSearchGroup(self):
        groupName=self.gcsg.editUserName.text()

        gName=lec.checkGroupName(groupName)
        if gName==True:
            self.gcsg.destroyElement()
            self.gcsg.searchGroup(groupName,self.gcsg.stritCond)
            self.btnSearchGroup.setDisabled(True)
        else:
            showResult(self.gcsg.statusbar,gName)


    def funGroupRequest(self):
        self.mainWindow.close()
        mainWindow=QMainWindow()
        lc.varStore['GroupChatRequestList']=mainWindow
        lc.gcCond=True
        XMainWindow.openWindows['groupChat']=True
        self.gcrr=lc.XGroupChatRequestRecieve()
        self.gcrr.setupUi(mainWindow)
        self.gcrr.init(self.c)
        colorButton(self.btnGroupRequest,color=None)
        self.gc.loadGroupRequest(tp='m')

        self.gcrr.btnBack.clicked.connect(lambda :self.funBack(mainWindow))

        mainWindow.show()

    def handle(self,msg):

        def fun():

            wType=msg['wType']
            info=msg

            if wType=='createGroup':
                self.gccg.btnCreate.setEnabled(True)
                self.handleCreateGroup(info)
            elif wType=='searchGroup':
                self.gcsg.btnSearch.setEnabled(True)
                self.handleSearchGroup(info)
            elif wType=='refressGCSearch':
                self.handleRefressGCSearch(info)
            elif wType=='groupRequest':
                self.handleGroupRequest(info)
            elif wType=='refressGC':
                self.handleRefress(info)
            elif wType=='groupChatWindow':
                self.handleGroupChatWindow(info)
            elif wType=='groupControlPanel':
                self.handleGroupControlPanel(info)
            elif wType=='acceptGroupRequestAdmin':
                self.handleAcceptGroupRequestAdmin(info)
            elif wType=='sendGroupRequest':
                self.handleSendGroupRequest(info)
            elif wType=='groupSearchMemberForSRequest':
                self.handleGroupSearchMemberForSRequest(msg)
            elif wType=='loadGroupRequest':
                tp=info['tp']

                if tp=='g':
                    self.loadGroupRequestAdmin(info)
                else:
                    self.loadGroupRequestMember(info)
            elif wType=='cancelGroupSendRequest':
                self.handlecancelGroupSendRequest(msg)
            elif wType=='groupSendRequest':
                self.handleGroupSendRequest(msg)
            elif wType=='acceptGroupRequestMember':
                self.handleAcceptGroupRequestMember(msg)
            elif wType=='sendGroupChat':
                self.handleSendGroupChat(msg)
            else:
                print(wType)
                showResult(self.statusbar,'Error :'+wType)

        self.timerFunList.append(fun)

    def handleSendGroupChat(self,info):

        if self.winChatWindow is not None:
            code=info['code']

            if code=='kkr1':
                data=info['chat']
                data=ds.dec(data)
                dType,info=ad.deAssValue(data,True)


                if dType=='Chat':
                    gName=info['groupName']
                    gName2=self.winChatWindow.gName

                    if gName2.lower()==gName.lower():
                        self.winChatWindow.handleChatWindow(info)
                    else:
                        showResult(self.winChatWindow.statusbar,"You are in another Group",False)
                else:
                    showResult(self.winChatWindow.statusbar,"File Recieving",True)

            elif code=='kkr2':

                gName=info['reciever']
                gName2=self.winChatWindow.gName
                if gName2.lower()==gName.lower():
                    self.winChatWindow.handleFileRuntime(info)
                else:
                    showResult(self.winChatWindow.statusbar,"You are in another Group",False)



            else:
                print("Error :#$ "+code)
                showResult(self.winChatWindow.statusbar,"Error :"+code)
        else:
            showResult(self.statusbar,"Recieving Message in Group Chat")

    def handleAcceptGroupRequestMember(self,info):
        code=info['code']

        if code=='ffe4':
            showResult(self.gcrr.statusbar,'Group Request Acception successfull',False)
        elif code=='tkm4':
            showResult(self.gcrr.statusbar,'Group Request Rejection successfull',False)
        else:
            showResult(self.gcrr.statusbar,"Error :"+code)

    def handleAcceptGroupRequestAdmin(self,info):
        code=info['code']

        if code=='ffe4':
            showResult(self.winControlPanel.statusbar,'User Group Request Acception successfull',False)
        elif code=='tkm4':
            showResult(self.winControlPanel.statusbar,'User Group Request Rejection successfull',False)
        else:
            showResult(self.winControlPanel.statusbar,"Error :"+code)


    def handleGroupSendRequest(self,msg):
        code=msg['code']
        if code=='1ee1':
            showResult(self.winControlPanel.statusbar,"You are not the Member of the Group")
        elif code=='1222':
            showResult(self.winControlPanel.statusbar,"Request Sending Successfull",False)
        elif code=='1uu1':
            showResult(self.winControlPanel.statusbar,"You are not the Admin of the Group")
        elif code=='e923':
            showResult(self.winControlPanel.statusbar,"Request Already Sent")
        else:
            print("ERROR A@: "+code)

    def handlecancelGroupSendRequest(self,msg):
        code=msg['code']

        if code=='tk87':
            showResult(self.winControlPanel.statusbar,"Cancel Request Successfull",False)
        else:
            print("ERROR A!:"+code)

    def loadGroupRequestMember(self,msg):
        def fun():
            data=ds.remodifyData(msg['data'],msg['type'],msg['shape'])

            self.gcrr.dataList=data
            self.gcrr.funLoadList()
            showResult(self.gcrr.statusbar,"{0} Records Found".format(len(data)),False)
        lc.timerFunList.append(fun)

    def loadGroupRequestAdmin(self,msg):
        pass

    def handleGroupSearchMemberForSRequest(self,msg):
        code=msg['code']

        if code=='0012' or code=='0013':
            showResult(self.winControlPanel.statusbar,"No Records Found")
        elif code=='0014':
            def fun():
                data=ds.remodifyData(msg['usersData'],msg['usersType'],msg['usersShape'])
                showResult(self.winControlPanel.statusbar,str(len(data))+" Records Found",False)

                self.winControlPanel.dataList=data
                self.winControlPanel.funLoadList()

            lc.timerFunList.append(fun)
        #Rcordf
        else:
            showResult(self.statusbar,"Error :"+code)

    def handleSendGroupRequest(self,info):
        code=info['code']
        if code=='1123':
            showResult(self.gcsg.statusbar,"Sending Request Successfull",False)
        elif code=='45g6':
            showResult(self.gcsg.statusbar,"Request Already Sent")
        elif code=='34f6':
            showResult(self.gcsg.statusbar,"Already Member of Group")
        else:
            showResult(self.gcsg.statusbar,"Error :"+code)

    def handleRefress(self,info):
        code=info['code']
        if code=='12k3':
            data=info['data']
            type=info['type']
            shape=info['shape']
            data=ds.remodifyData(data,type,shape)
            if len(data)==0:
                showResult(self.statusbar,"No Records Found")
            else:
                def fun():
                    showResult(self.statusbar,"{0} Records Found".format(len(data)),False)
                    self.dataList=data

                    self.funLoadList()

                lc.timerFunList.append(fun)




        else:
            showResult(self.statusbar,"Error :"+code)

    def handleCreateGroup(self,info):
        code=info['code']
        if code=='0000':
            showResult(self.gccg.statusbar,"Group Already Exist")
        elif code=='0011':
            showResult(self.gccg.statusbar,"Successfully Created Group",False)
        else:
            showResult(self.gccg.statusbar,"Error :"+code)

    def handleRefressGCSearch(self,info):

        if not self.isAlreadySearched:

            code=info['code']
            if code=='yh2k':
                #def fun():
                    data=info['data']
                    type=info['types']
                    shape=info['shape']

                    data=ds.remodifyData(data,type,shape)
                    length=len(data)

                    self.gcsg.dataList=data
                    self.gcsg.funLoadData()
                #lc.timerFunList.append(fun)

            else:
                showResult(self.gcsg.statusbar,"Error :"+code)

    def handleSearchGroup(self,info):
        self.isAlreadySearched=True
        code=info['code']
        if code=='y12k' or code=='kkr1':
            def fun():
                data=info['data']
                type=info['types']
                shape=info['shape']

                data=ds.remodifyData(data,type,shape)
                length=len(data)
                showResult(self.gcsg.statusbar,"{0} Records Found".format(length),False)
                self.gcsg.dataList=data
                self.gcsg.funLoadData()
            lc.timerFunList.append(fun)
        elif code=="2333" or code=='45kt':
            showResult(self.gcsg.statusbar,"No Records Found")

        else:
            showResult(self.gcsg.statusbar,"Error :"+code)

    def handleGroupRequest(self,info):
        code=info['code']

        if code=="11e1" or code=='eeeg':
            self.handleAdminGroupRequest(info)
        elif code=='1ss2' or  code=='4eem':
            self.handleMemberGroupRequest(info)
        else:
            showResult(self.statusbar,"Error :"+code)

    def handleMemberGroupRequest(self,info):
        code=info['code']
        if code=='1ss2':
            def fun():
                data=info['data']
                type=info['type']
                shape=info['shape']

                data=ds.remodifyData(data,type,shape)
                self.gcrr.dataList=data
                self.gcrr.funLoadList()


                showResult(self.gcrr.statusbar,"{0} Records Found"+len(data),False)
            lc.timerFunList.append(fun)
        else:
            showResult(self.gcrr.statusbar,"No Records Found")

    def handleAdminGroupRequest(self,info):
        code=info['code']

        if code=='11e1':

            data=ds.remodifyData(info['data'],info['type'],info['shape'])
            length=len(data)
            self.labelStatus.config(text=str(length)+" Records founded")

            self.destroyContElement(self.groupRequestListFrame)

            def funInitiate(name):
                frame=tk.Frame(self.groupRequestListFrame,width=230,height=50)

                label=tk.Label(frame,text=name)
                label.place(x=10,y=5)

                def funAccept():
                    self.gc.acceptGroupRequest(name,self.c.userName,'1','m')

                def funReject():

                    self.gc.acceptGroupRequest(name,self.c.userName,'0','m')


                btnAccept=tk.Button(frame,text='Accept',command=funAccept)
                btnAccept.place(x=10,y=45)

                btnReject=tk.Button(frame,text='Reject',command=funReject)
                btnReject.place(x=150,y=45)


                frame.pack()


        else:
            self.labelStatus.config(text="Something went wrong")

    def handleGroupChatWindow(self,info):
        self.winChatWindow.handle(info)

    def handleGroupControlPanel(self,info):
        code=info['code']

        if code=='kk14':
            def fun():
                dataM=ds.remodifyData(info['mm'],info['mmt'],info['mms'])
                dataS=ds.remodifyData(info['sm'],info['smt'],info['sms'])
                dataR=ds.remodifyData(info['rm'],info['rmt'],info['rms'])

                self.winControlPanel.dataListMembers=dataM
                self.winControlPanel.dataListSendMembers=dataS
                self.winControlPanel.dataListRecvMembers=dataR

                self.winControlPanel.funRefressAll()

            lc.timerFunList.append(fun)
        else:
            showResult(self.gcrr.statusbar,"Error :"+code)

class XGroupChatCreateGroup():

    def setupUi(self, MainWindow):
        self.mainWindow=MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(256, 128)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.editGroupName = QtWidgets.QLineEdit(self.centralwidget)
        self.editGroupName.setGeometry(QtCore.QRect(20, 30, 113, 20))
        self.editGroupName.setObjectName("editGroupName")
        self.btnCreate = QtWidgets.QPushButton(self.centralwidget)
        self.btnCreate.setGeometry(QtCore.QRect(20, 70, 75, 23))
        self.btnCreate.setObjectName("btnCreate")
        self.btnBack = QtWidgets.QPushButton(self.centralwidget)
        self.btnBack.setGeometry(QtCore.QRect(140, 70, 75, 23))
        self.btnBack.setObjectName("btnBack")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):

        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.editGroupName.setPlaceholderText(_translate("MainWindow", "Enter Group Name"))
        self.btnCreate.setText(_translate("MainWindow", "Create"))
        self.btnBack.setText(_translate("MainWindow", "Back"))


        self.mainWindow.setWindowTitle("Create Group")
        self.mainWindow.closeEvent=self.onClose
        lc.gcCond=False
        XMainWindow.openWindows["GroupChat"]=True


    def onClose(self,event):
        XMainWindow.openWindows['groupChat']=False
        event.accept()

class XGroupChatSearchGroup():
    def setupUi(self, MainWindow):
        self.mainWindow=MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(278, 372)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 20, 161, 31))
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

        self.btnLoad=QPushButton(self.centralwidget)
        self.btnLoad.setText("Load")
        self.btnLoad.setGeometry(190,40,60,23)
        self.btnLoad.clicked.connect(self.funLoadData)


        self.scrollContainer,self.scrollHolder=pqc.scrollBar(self.centralwidget,30,120,220,230)

        self.label.setFont(font)
        self.label.setMouseTracking(True)
        self.label.setMidLineWidth(1)
        self.label.setObjectName("label")
        self.editUserName = QtWidgets.QLineEdit(self.centralwidget)
        self.editUserName.setGeometry(QtCore.QRect(30, 60, 113, 20))
        self.editUserName.setObjectName("editUserName")

        self.checkStrictSearch=QCheckBox(self.centralwidget)
        self.checkStrictSearch.setGeometry(30,85,100,17)
        self.checkStrictSearch.setText("Strict Search")
        self.checkStrictSearch.clicked.connect(self.funCheckStrictSearch)


        self.btnSearch = QtWidgets.QPushButton(self.centralwidget)
        self.btnSearch.setGeometry(QtCore.QRect(180, 80, 75, 23))
        self.btnSearch.setObjectName("btnSearch")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")


        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        XMainWindow.openWindows["GroupChat"]=True

        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Search Group"))
        self.editUserName.setPlaceholderText(_translate("MainWindow", "Group Name"))
        self.btnSearch.setText(_translate("MainWindow", "Search"))

    def funBack(self,mainWindow):
        self.mainWindow.show()
        lc.gcCond=True
        XMainWindow.openWindows['groupChat']=True
        mainWindow.destroy()

    def funCheckStrictSearch(self):
        if self.checkStrictSearch.isChecked():
            self.stritCond='1'
        else:
            self.stritCond='0'

    def init(self,c):
        self.c=c
        self.dataList=None
        self.count=0

        self.stritCond='0'

        self.send=c.send
        self.gc=xcs.GroupChat(self.send)
        lc.gcCond=False
        self.FWidList={}
        self.btnLoad.close()
        self.mainWindow.setWindowTitle("Search Group")
        self.mainWindow.closeEvent=self.onClose
        self.refress()

    def refress(self):
        self.gc.refressGCSearch()

    def onClose(self,event):
        XMainWindow.openWindows['groupChat']=False
        event.accept()


    def destroyElement(self):
        for i in self.scrollContainer.children()[1:]:
            i.deleteLater()

    def funLoadData(self):
        self.destroyElement()

        for i in self.dataList:
            self.importData(i)


    def importData(self,data):

        i=data
        gName=i[0]
        members=i[1]


        dcount=self.count

        def funSendRequest():
            list=self.FWidList[gName]
            list.deleteLater()

            self.gc.sendGroupRequest(gName)


        def funViewProfile():
            self.mainWindow.close()
            mainWindow=QMainWindow()
            lc.varStore['GroupChatViewProfile']=mainWindow
            lc.gcCond=True
            XMainWindow.openWindows['groupChat']=True
            self.gcsgvp=lc.XGroupChatViewProfile()
            self.gcsgvp.setupUi(mainWindow)
            self.gcsgvp.init(self.c,gName)
            self.gcsgvp.btnBack.clicked.connect(lambda :self.funBack(mainWindow))
            mainWindow.show()



        frame=QFrame(self.scrollContainer)
        frame.setFixedSize(200,61)

        labelGName=QLabel(frame)
        labelGName.setGeometry(10,5,201,16)
        font = QtGui.QFont()
        font.setPointSize(8)
        labelGName.setFont(font)
        labelGName.setText(gName)


        btnSendRequest=QPushButton(frame)
        btnSendRequest.setGeometry(10,30,75,23)
        btnSendRequest.setText("Send Request")
        btnSendRequest.clicked.connect(funSendRequest)


        btnViewProfile=QPushButton(frame)
        btnViewProfile.setGeometry(110,30,75,23)
        btnViewProfile.setText("View Profile")
        btnViewProfile.clicked.connect(funViewProfile)





        self.scrollHolder.addWidget(frame,dcount,0)

        self.count=dcount+1

        self.FWidList[gName]=frame

class XGroupChatRequestRecieve():
    def setupUi(self, MainWindow):
        self.mainWindow=MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(292, 362)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.btnBack = QtWidgets.QPushButton(self.centralwidget)
        self.btnBack.setGeometry(QtCore.QRect(30, 30, 75, 23))
        self.btnBack.setObjectName("btnBack")

        self.btnLoadList=QPushButton(self.centralwidget)
        self.btnLoadList.setText("Load List")
        self.btnLoadList.setGeometry(190,30,75,23)
        self.btnLoadList.clicked.connect(self.funLoadList)

        self.scrollContainer,self.scrollHolder=pqc.scrollBar(self.centralwidget,30,70,230,270)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        XMainWindow.openWindows["GroupChat"]=True
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btnBack.setText(_translate("MainWindow", "Back"))


    def init(self,c):
        self.c=c
        self.count=0
        self.send=c.send
        self.gc=xcs.GroupChat(self.send)
        self.FWidList={}
        self.dataList=None
        self.btnLoadList.close()
        self.mainWindow.setWindowTitle("Group Request")
        self.mainWindow.closeEvent=self.onClose
        lc.gcCond=False

    def onClose(self,event):
        XMainWindow.openWindows['groupChat']=False
        event.accept()

    def funLoadList(self):
        for i in self.scrollContainer.children()[1:]:
            i.deleteLater()

        if self.dataList is not None:
            for i in self.dataList:
                self.importData(i)

    def importData(self,gName):
        gName=gName[1]

        frame=QFrame(self.scrollContainer)
        frame.setFixedSize(210,61)

        label=QLabel(frame)
        label.setGeometry(10,5,181,16)
        label.setText(gName)

        dcount=self.count

        def destroy():
            list= self.FWidList[gName]
            list.deleteLater()

        def funAccept():

            self.gc.acceptGroupRequest(gName,self.c.userName,acceptT='1',tp='m')
            destroy()

        def funReject():
            self.gc.acceptGroupRequest(gName,self.c.userName,acceptT='0',tp='m')
            destroy()


        btnAccept=QPushButton(frame)
        btnAccept.setText("Accept")
        btnAccept.clicked.connect(funAccept)
        btnAccept.setGeometry(10,30,75,23)

        btnReject=QPushButton(frame)
        btnReject.setText("Reject")
        btnReject.clicked.connect(funReject)
        btnReject.setGeometry(120,30,75,23)


        self.scrollHolder.addWidget(frame,dcount,0)


        self.count=dcount+1

        self.FWidList[gName]=frame

class XGroupChatControlPanel():
    def setupUi(self, MainWindow):
        self.mainWindow=MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(800, 352)
        MainWindow.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.labelGroupName = QtWidgets.QLabel(self.centralwidget)
        self.labelGroupName.setGeometry(QtCore.QRect(20, 20, 161, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.labelGroupName.setFont(font)
        self.labelGroupName.setObjectName("labelGroupName")
        self.label_13 = QtWidgets.QLabel(self.centralwidget)
        self.label_13.setGeometry(QtCore.QRect(190, 20, 161, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        self.labelAdminName = QtWidgets.QLabel(self.centralwidget)
        self.labelAdminName.setGeometry(QtCore.QRect(310, 20, 151, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.labelAdminName.setFont(font)
        self.labelAdminName.setObjectName("labelAdminName")
        self.labelMembers = QtWidgets.QLabel(self.centralwidget)
        self.labelMembers.setGeometry(QtCore.QRect(490, 20, 121, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.labelMembers.setFont(font)
        self.labelMembers.setObjectName("labelMembers")
        self.label_16 = QtWidgets.QLabel(self.centralwidget)
        self.label_16.setGeometry(QtCore.QRect(20, 70, 161, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_16.setFont(font)
        self.label_16.setObjectName("label_16")

        self.btnRefressAll=QPushButton(self.centralwidget)
        self.btnRefressAll.setText("Refress All")
        self.btnRefressAll.setGeometry(170,70,75,23)
        self.btnRefressAll.clicked.connect(self.funRefressAll)



        self.label_17 = QtWidgets.QLabel(self.centralwidget)
        self.label_17.setGeometry(QtCore.QRect(290, 70, 191, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_17.setFont(font)
        self.label_17.setFocusPolicy(QtCore.Qt.TabFocus)
        self.label_17.setObjectName("label_17")
        self.label_18 = QtWidgets.QLabel(self.centralwidget)
        self.label_18.setGeometry(QtCore.QRect(580, 70, 201, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_18.setFont(font)
        self.label_18.setObjectName("label_18")
        self.btnLeaveGroup = QtWidgets.QPushButton(self.centralwidget)
        self.btnLeaveGroup.setGeometry(QtCore.QRect(640, 20, 75, 23))
        self.btnLeaveGroup.setStyleSheet("background-color: rgb(255, 0, 0);")
        self.btnLeaveGroup.setObjectName("btnLeaveGroup")
        self.btnBack = QtWidgets.QPushButton(self.centralwidget)
        self.btnBack.setGeometry(QtCore.QRect(720, 20, 75, 23))
        self.btnBack.setObjectName("btnBack")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(260, 70, 16, 251))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(530, 70, 16, 251))
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setGeometry(QtCore.QRect(10, 50, 781, 16))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.editUserName = QtWidgets.QLineEdit(self.centralwidget)
        self.editUserName.setGeometry(QtCore.QRect(290, 100, 113, 20))
        self.editUserName.setObjectName("editUserName")
        self.btnSearch = QtWidgets.QPushButton(self.centralwidget)
        self.btnSearch.setGeometry(QtCore.QRect(410, 100, 41, 23))
        self.btnSearch.setObjectName("btnSearch")
        self.btnLoadList = QtWidgets.QPushButton(self.centralwidget)
        self.btnLoadList.setGeometry(QtCore.QRect(460, 100, 71, 23))
        self.btnLoadList.setObjectName("btnLoadList")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.scrollContainerM,self.scrollHolderM=pqc.scrollBar(self.centralwidget,20,100,230,230)
        self.scrollContainerR,self.scrollHolderR=pqc.scrollBar(self.centralwidget,560,100,230,230)

        self.scrollContainer,self.scrollHolder=pqc.scrollBar(self.centralwidget,290,130,240,200)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        XMainWindow.openWindows["GroupChat"]=True
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.labelGroupName.setText(_translate("MainWindow", "Group Name"))
        self.label_13.setText(_translate("MainWindow", "Admin Name :-"))
        self.labelAdminName.setText(_translate("MainWindow", "Group Name"))
        self.labelMembers.setText(_translate("MainWindow", "Members :-"))
        self.label_16.setText(_translate("MainWindow", "Group Member List"))
        self.label_17.setText(_translate("MainWindow", "Send Request To Members"))
        self.label_18.setText(_translate("MainWindow", "Group Member Reciev List"))
        self.btnLeaveGroup.setText(_translate("MainWindow", "Leave Group"))
        self.btnBack.setText(_translate("MainWindow", "Back"))
        self.editUserName.setPlaceholderText(_translate("MainWindow", "UserName"))
        self.btnSearch.setText(_translate("MainWindow", "Search"))
        self.btnLoadList.setText(_translate("MainWindow", "LoadList"))

        self.btnLoadList.clicked.connect(self.funLoadList)

    def getAdmin(self,mainMember):
        typMainMember=mainMember[:,1].tolist()
        index=typMainMember.index('a')
        admin=mainMember[index][0]

        if admin.lower()==self.c.userName.lower():
            self.condAdmin=True
            self.btnSearch.setDisabled(False)
            self.editUserName.setDisabled(False)
            self.btnLoadList.setDisabled(False)
        else:
            self.btnSearch.setDisabled(True)
            self.editUserName.setDisabled(True)
            self.btnLoadList.setDisabled(True)
            self.condAdmin=False

    def init(self,c,gName):
        self.c=c

        self.send=c.send
        self.gc=xcs.GroupChat(self.send)
        self.count=0
        self.countM=0
        self.countR=0

        self.FWidListM={}
        self.FWidList={}
        self.FWidListR={}
        self.btnRefressAll.close()
        self.btnLoadList.close()

        self.gName=gName
        self.condAdmin=False

        self.dataList=None

        self.dataListMembers=None
        self.dataListSendMembers=None
        self.dataListRecvMembers=None

        self.mainWindow.setWindowTitle(self.gName+" Control Panel")
        self.mainWindow.closeEvent=self.onClose
        lc.gcCond=False

        self.btnLeaveGroup.clicked.connect(self.funLeaveGroup)

    def funLeaveGroup(self):
        XMainWindow.openWindows['groupChat']=False
        self.gc.leaveGroup(self.gName)
        self.mainWindow.destroy()

    def onClose(self,event):
        XMainWindow.openWindows['groupChat']=False
        event.accept()

    def destroyElement(self,cont):

        for i in cont.children()[1:]:
            i.deleteLater()

    def importDataMember(self,data):
        userName=data[0]
        typ=data[1]
        dcount=self.countM
        def funKick():
            self.gc.kickMemberGroupChat(self.gName,userName)

            i= self.FWidListM[userName]
            i.deleteLater()

        frame=QFrame(self.scrollContainerM)
        frame.setFixedSize(210,61)

        labelU=QLabel(frame)
        labelU.setGeometry(10,5,181,16)
        labelU.setText(userName)

        labelT=QLabel(frame)
        labelT.setGeometry(10,35,81,16)
        labelT.setText(typ)





        if self.condAdmin and self.c.userName.lower()!=userName.lower():

            btnKick=QPushButton(frame)
            btnKick.setGeometry(120,30,75,23)
            btnKick.setText("Kick")
            btnKick.clicked.connect(funKick)

        self.scrollHolderM.addWidget(frame,dcount,0)
        self.FWidListM[userName]=frame

        self.countM=dcount+1

    def importDataSMember(self,userName):
        dcount=self.count

        def cancelRequest():

            i = self.FWidList[userName]
            i.deleteLater()

            self.gc.cancelGroupSendRequest(self.gName,userName)
            showResult(self.statusbar,"Cancel Request Successfull",False)

        frame=QFrame(self.scrollContainer)
        frame.setFixedSize(210,61)

        labelU=QLabel(frame)
        labelU.setText(userName)
        labelU.setGeometry(10,5,201,16)

        btnCancel=QPushButton(frame)
        btnCancel.setText("Cancel Request")
        btnCancel.clicked.connect(cancelRequest)
        btnCancel.setGeometry(10,30,85,23)

        if not self.condAdmin:
            btnCancel.setDisabled(True)


        self.scrollHolder.addWidget(frame,dcount,0)
        self.FWidList[userName]=frame

        self.count=dcount+1

    def importDataRMember(self,userName):
        dcount=self.countR

        def destroyE():

            for i in self.FWidListR[userName]:
                i.deleteLater()

        def rejectRequest():
            destroyE()
            self.gc.acceptGroupRequest(self.gName,userName,'0')

        def acceptRequest():
            destroyE()
            self.gc.acceptGroupRequest(self.gName,userName,'1')

        frame=QFrame(self.scrollContainerR)
        frame.setFixedSize(220,61)


        labelU=QLabel(frame)
        labelU.setText(userName)
        labelU.setGeometry(10,5,201,16)

        btnAccept=QPushButton(frame)
        btnAccept.setText("Accept")
        btnAccept.clicked.connect(acceptRequest)
        btnAccept.setGeometry(10,30,75,23)

        btnReject=QPushButton(frame)
        btnReject.setText("Reject")
        btnReject.clicked.connect(rejectRequest)
        btnReject.setGeometry(130,30,75,23)

        if not self.condAdmin:
            btnAccept.setDisabled(True)
            btnReject.setDisabled(True)


        self.scrollHolderR.addWidget(frame,dcount,0)
        self.countR=dcount+1

        self.FWidListR[userName]=frame

    def funRefressAll(self):

        self.destroyElement(self.scrollContainer)
        self.destroyElement(self.scrollContainerM)
        self.destroyElement(self.scrollContainerR)

        if self.dataListMembers is not None:

            self.getAdmin(self.dataListMembers)
            for i in self.dataListMembers:
                self.importDataMember(i)

        if self.dataListSendMembers is not None:

            for i in self.dataListSendMembers:
                self.importDataSMember(i)

        if self.dataListRecvMembers is not None:

            for i in self.dataListRecvMembers:
                self.importDataRMember(i)

    def funSearchList(self):
        userName=self.editUserName.text()
        usr=lec.checkUserName(userName)
        if usr==True:
            self.gc.groupSearchMemberForSRequest(userName)
            showResult(self.statusbar,"Searching ...",False)
        else:
            showResult(self.statusbar,usr)


    def funLoadList(self):
        self.destroyElement(self.scrollContainer)

        if self.dataList is not None:
            for i in self.dataList:
                self.importData(i)

    def importData(self,data):

        i=data
        userName=i[0]
        name=i[1]

        imgData=ds.remodifyData(i[2],i[3],i[4])
        imgData=cv2.resize(imgData,(60,80))
        dcount=self.count

        def funBlock():
            list=self.FWidList[userName]
            list.deleteLater()
            self.gc.groupSendRequest(userName,self.gName)


        frame=QFrame(self.scrollContainer)
        frame.setFixedSize(210,91)


        labelProfile=QLabel(frame)
        labelProfile.setGeometry(10,5,60,80)
        imgData=cv2.resize(imgData,(60,80))
        image=pqc.cv2toPqImage(imgData)
        labelProfile.setPixmap(image)



        labelFullName=QLabel(frame)
        labelFullName.setGeometry(80,5,91,16)
        font = QtGui.QFont()
        font.setPointSize(8)
        labelFullName.setFont(font)
        labelFullName.setText(name)

        labelUserName=QLabel(frame)
        labelUserName.setGeometry(80,32,81,16)
        labelUserName.setFixedSize(130,12)
        font.setPointSize(8)
        labelUserName.setFont(font)
        labelUserName.setText(userName)


        btnChatWindow=QPushButton(frame)
        btnChatWindow.setGeometry(80,60,75,23)
        btnChatWindow.setText("Send Request")
        btnChatWindow.clicked.connect(funBlock)



        self.scrollHolder.addWidget(frame,dcount,0)



        self.count=dcount+1

        self.FWidList[userName]=frame

class XGroupChatChatWindow():
    def setupUi(self, MainWindow):
        self.mainWindow=MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(320, 392)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(20, 30, 141, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.btnBack = QtWidgets.QPushButton(self.centralwidget)
        self.btnBack.setGeometry(QtCore.QRect(180, 30, 75, 23))
        self.btnBack.setObjectName("btnBack")
        self.editMessage = QtWidgets.QLineEdit(self.centralwidget)
        self.editMessage.setGeometry(QtCore.QRect(20, 310, 113, 20))
        self.editMessage.setObjectName("editMessage")
        self.btnSendMessage = QtWidgets.QPushButton(self.centralwidget)
        self.btnSendMessage.setGeometry(QtCore.QRect(180, 310, 81, 23))
        self.btnSendMessage.setObjectName("btnSendMessage")
        self.btnSetFile = QtWidgets.QPushButton(self.centralwidget)
        self.btnSetFile.setGeometry(QtCore.QRect(20, 340, 75, 23))
        self.btnSetFile.setObjectName("btnSetFile")
        self.btnSendFile = QtWidgets.QPushButton(self.centralwidget)
        self.btnSendFile.setGeometry(QtCore.QRect(180, 340, 75, 23))
        self.btnSendFile.setObjectName("btnSendFile")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(150, 310, 3, 61))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        #self.btnRefress=QPushButton(self.centralwidget)
        #self.btnRefress.setText("Refress")
        #self.btnRefress.setGeometry(120,30,75,23)
        #self.btnRefress.clicked.connect(self.handleRuntimeChatControl)

        self.scrollContainer,self.scrollGG,self.scrollHolder=pqc.scrollBarWithSA(self.centralwidget,20,60,290,240)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.qTimer=QTimer()
        self.qTimer.setInterval(500)
        self.qTimer.timeout.connect(self.handleRuntimeChatControl)
        self.qTimer.start()

    def retranslateUi(self, MainWindow):
        self.qTimer2=QTimer()
        self.qTimer2.setInterval(500)
        self.qTimer2.timeout.connect(lambda :self.qTimerRefressFun(self.timerFunList))
        self.qTimer2.start()

        XMainWindow.openWindows["GroupChat"]=True
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_12.setText(_translate("MainWindow", "Group Name"))
        self.btnBack.setText(_translate("MainWindow", "Back"))
        self.editMessage.setPlaceholderText(_translate("MainWindow", "Enter Message"))
        self.btnSendMessage.setText(_translate("MainWindow", "Send Message"))
        self.btnSetFile.setText(_translate("MainWindow", "Set Fiile"))
        self.btnSendFile.setText(_translate("MainWindow", "Send File"))
        self.btnSendMessage.clicked.connect(self.funSendChat)

    def init(self,c,gName):
        self.c=c
        self.gName=gName
        self.send=c.send
        self.gc=xcs.GroupChat(self.send)
        self.count=0
        self.timerFunList=[]
        self.selectedFile=''

        self.FWidList={}

        self.sWin='gc@'+gName
        fc.getSetWindow(self.sWin)

        self.btnSetFile.clicked.connect(self.funSetFile)
        self.btnSendFile.clicked.connect(self.funSendFile)
        self.c.functionList[gName+'-CancelDownloadFileChat']=self.handleCancelDownloadFile
        self.fileFlowing=[]


        data=fc.removeDublFromArray(fc.getAllFilesOfSend(self.sWin))
        #print("%^%^%^",data)
        if data is not None:
            self.fileFlowing=data
            for i in data:
                self.formatSendChatFile(i)

        data2=fc.removeDublFromArray(fc.getAllFilesOfRecv(self.sWin))

        if data2 is not None:
            self.fileFlowing=self.fileFlowing+data2




        self.dataList=None


        self.mainWindow.setWindowTitle(self.gName+" Chat Window")
        self.mainWindow.closeEvent=self.onClose
        lc.gcCond=False

    def onClose(self,event):
        XMainWindow.openWindows['groupChat']=False
        event.accept()
        self.fileFlowing=[]


    def funSendChat(self):
        chat=self.editMessage.text()
        if  chat!='':
            self.editMessage.setText("")
            self.insertChat(self.c.userName,chat)
            self.gc.sendGroupChat(self.gName,chat)

    def qTimerRefressFun(self,timerFunList):
        funList=timerFunList
        if len(funList)>0:
            funList[0]()
            timerFunList.pop(0)

        self.callFileRefress()

    def callFileRefress(self):

        for i in self.fileFlowing:
            st=fc.getFileSttr(i)

            if st is not None:
                if st=='s':
                    self.refSendFile(i)
                else:
                    self.refRecvFile(i)

    def refSendFile(self,fileName):

        flow=fc.getSendFileFlow(fileName)
        tsize=fc.getSendFileTempSize(fileName)
        size=fc.getSendFileSize(fileName)
        #print(f'{fileName} ->{tsize}/{size}')
        #print(fileName in self.FWidList)
        if fileName in self.FWidList:
            self.refGuiSendFile(fileName,flow,tsize,size)

    def refGuiSendFile(self,fileName,flow,tsize,size):
        if flow !=None:

            frame=self.FWidList[fileName]
            children=frame.children()

            mtS=opFile.getByteToMb(int(tsize))
            mSS=opFile.getByteToMb(int(size))

            mtS=round(mtS,2)
            mSS=round(mSS,2)

            per=0
            if mSS==0:
                per=0
            else:
                per=opFile.calculateFilePercentage(mtS,mSS)

            children[3].setValue(per)
            if mSS !=mtS:
                txt=f'{mtS}/{mSS} mb'
            else:
                children[3].setDisabled(True)
                txt=f'Size ->{mtS} mb'
            #print(txt)
            children[5].setText(txt)

    def refRecvFile(self,fileName):
        flow=fc.getRecvFileStatus(fileName)
        tsize=fc.getRecvFileTempSize(fileName)
        size=fc.getRecvFileSize(fileName)
        #print(f'{fileName} ->{tsize}/{size}')
        #print(fileName in self.FWidList)
        if fileName in self.FWidList:
            self.refGuiRecvFile(fileName,flow,tsize,size)

    def refGuiRecvFile(self,fileName,flow,tsize,size):
        if flow !=None:

            frame=self.FWidList[fileName]
            children=frame.children()

            mtS=opFile.getByteToMb(int(tsize))
            mSS=opFile.getByteToMb(int(size))

            mtS=round(mtS,2)
            mSS=round(mSS,2)

            per=0
            if mSS==0:
                per=0
            else:
                per=opFile.calculateFilePercentage(mtS,mSS)

            children[3].setValue(per)
            if mSS !=mtS:
                txt=f'{mtS}/{mSS} mb'
            else:
                children[3].setDisabled(True)
                txt=f'Size ->{mtS} mb'
            #print(txt)
            children[6].setText(txt)


    def funSetFile(self):
        file,inf=QFileDialog.getOpenFileName()
        self.selectedFile=file

        if file != '':
            showResult(self.statusbar,"File ->'"+file+"'<- is Selected",False)

    def funSendFile(self):
        def fun():
            if self.selectedFile != '':
                file=self.selectedFile

                f=opFile.attachFileWithtime(opFile.getActualFileName(self.selectedFile))


                self.selectedFile=''

                namesToTo=self.c.userName+'-'+self.gName

                def onStart():

                    fc.onSendStart(self.sWin,f)

                def onEnd(fName):
                    size=self.c.send.fileSize[fName]
                    fc.onSendEnd(self.sWin,fName)

                    def fun(size):
                        if fName in self.FWidList:
                            frame=self.FWidList[fName]
                            children=frame.children()
                            children[3].setDisabled(True)
                            children[2].setValue(100)
                            size=opFile.getByteToMb(size)
                            size=round(size,2)
                            children[4].setText(f'Size ->{size} mb')

                    self.timerFunList.append(lambda: fun(size))

                self.c.send.send_file3(file,fileTempName=f,onStart=onStart,
                                       toWhom=namesToTo,toType='groupChat')
                #fc.setSendFile(self.sWin,f)
                self.fileFlowing.append(f)
                self.formatSendChatFile(f)


        self.timerFunList.append(fun)

    def formatSendChatFile(self,f):
        dCount=self.count

        frame=QFrame(self.scrollContainer)
        frame.setFixedSize(250,131)

        styleBackground="""
        background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:0.983, y2:0, stop:0 rgba(0, 124, 0, 255), stop:1 rgba(255, 255, 255, 255));
        """

        styleUserName='''
        background-color: rgb(81, 255, 0);
        border: 1px solid #1C6EA4;

        '''

        styleFileName='''
        border: 1px solid #1C6EA4;
        border-color: rgb(255, 0, 0);
        background-color: rgb(0, 124,0);
        color:rgb(255,255,255);
        '''

        styleSize='''
        background-color: rgb(170, 255, 127);
        '''

        labelBackground=QLabel(frame)
        labelBackground.setGeometry(40,0,211,131)
        labelBackground.setStyleSheet(styleBackground)

        sendUser=QLabel(frame)
        sendUser.setGeometry(50,5,191,16)
        sendUser.setText("You")
        sendUser.setStyleSheet(styleUserName)

        fileName=QLabel(frame)
        fileName.setGeometry(50,30,191,31)
        fileName.setWordWrap(True)
        fts=opFile.getActualFileName(f)
        fileName.setStyleSheet(styleFileName)

        fileName.setText(fts)
        #fileName.setAlignment(QtCore.Qt.AlignRight)

        progressBar=QProgressBar(frame)
        progressBar.setRange(0,100)
        progressBar.setGeometry(50,70,191,23)

        def onEnd(fName):
                    size=self.c.send.fileSize[fName]
                    fc.onSendEnd(self.sWin,fName)

                    def fun(size):
                        if fName in self.FWidList:
                            frame=self.FWidList[fName]
                            children=frame.children()
                            children[4].setDisabled(True)
                            children[3].setValue(100)
                            size=opFile.getByteToMb(size)
                            size=round(size,2)
                            children[5].setText(f'Size ->{size} mb')

                    self.timerFunList.append(lambda: fun(size))

        self.c.send.funSendListEnd[f]=onEnd

        def funControl():
            frame.close()
            self.c.send.fileFlow[f]=False

        btnControl=QPushButton(frame)
        btnControl.setText("Cancel")
        btnControl.setGeometry(50,100,75,23)
        btnControl.clicked.connect(funControl)

        labelSize=QLabel(frame)
        labelSize.setGeometry(130,100,111,20)
        labelSize.setAlignment(QtCore.Qt.AlignRight)

        size=fc.getSendFileSize(f)

        if size is None:
            labelSize.setText("_None")
        else:
            si=int(size)
            st=opFile.getByteToMb(si)
            st=round(st,2)
            labelSize.setText(f"Size -> {st} mb")

        sendUser.adjustSize()

        labelSize.setStyleSheet(styleSize)

        self.scrollHolder.addWidget(frame,dCount,0)

        self.count=dCount+1
        self.FWidList[f]=frame

        #self.scrollGG.verticalScrollBar().setValue(1000*self.count);

    def handleDownloadFile(self,msg):
        def fun():

            code=msg['code']
            fileName=msg['fileName']

            if code=='c12c':
                text=f'{fileName}-> is downloading started'
                showResult(self.statusbar,text,False)
            elif code=='FEE4':
                text=f'{fileName}-> is deleted/not exist on server'
                showResult(self.statusbar,text)
            else:
                text='Error Code '+code
                showResult(self.statusbar,text)


        self.timerFunList.append(fun)

    def handleCancelDownloadFile(self,msg):
        def fun():

            code=msg['code']
            fileName=msg['fileName']

            if code=='tt56':
                text=f'{fileName}-> is canceled successfully'
                showResult(self.statusbar,text,False)
            elif code=='45GH':
                text=f'{fileName}-> is already downloaded/canceled from server'
                showResult(self.statusbar,text)
            else:
                text='Error Code '+code
                showResult(self.statusbar,text)


        self.timerFunList.append(fun)

    def formatRecvChatFile(self,sender,f,size):
        dCount=self.count

        condYou=False

        if sender.lower()==self.c.userName.lower():
            condYou=True

        frame=QFrame(self.scrollContainer)
        frame.setFixedSize(250,131)

        styleBackgroundUser="""
        background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:0.983, y2:0, stop:0 rgba(127, 127, 127, 255), stop:1 rgba(255, 255, 255, 255));
        """

        styleBackgroundUserYou="""
        background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:0.983, y2:0, stop:0 rgba(0, 124, 0, 255), stop:1 rgba(255, 255, 255, 255));
        
        """

        styleUserNameU='''
        background-color: rgb(81, 255, 0);
        border: 1px solid #1C6EA4;

        '''

        styleFileNameU='''
        background-color: rgb(0, 124,0);
        color:rgb(255,255,255);
        '''

        styleSizeU='''
        background-color: rgb(170, 255, 127);
        '''

        styleUserNameA='''
        background-color: rgb(170, 170, 127);
        border: 1px solid #1C6EA4;
        '''

        styleFileNameA='''
        background-color: rgb(107, 107, 107);
        color: rgb(255, 255, 255);
        '''

        styleSizeA='''
        background-color: rgba(227, 227, 227, 247);
        '''

        labelBackground=QLabel(frame)




        sendUser=QLabel(frame)
        labelSize=None



        fileName=QLabel(frame)

        fileName.setWordWrap(True)
        fts=opFile.getActualFileName(f)

        fileName.setText(fts)
        #fileName.setAlignment(QtCore.Qt.AlignRight)

        progressBar=QProgressBar(frame)
        progressBar.setRange(0,100)

        btnDownload=QPushButton(frame)
        btnCancel=QPushButton(frame)

        labelSize=QLabel(frame)
        btnOpen=QPushButton(frame)


        def onEnd(cond,size):
                fc.onRecvEnd(self.sWin,f)

                def fun():
                    children=self.FWidList[f].children()
                    if cond:
                        children[3].setValue(100)

                        children[-3].close()
                        children[-1].show()
                        children[4].close()
                        children[5].close()
                    else:
                        progressBar.reset()
                    si=int(size)
                    st=opFile.getByteToMb(si)
                    st=round(st,2)

                    labelSize.setText(f"Size -> {st} mb")

                self.timerFunList.append(fun)

        def funDownloadFile():
            self.c.functionList['g-'+self.gName+'-DownloadFileChat']=self.handleDownloadFile
            self.c.downloadFile(f,self.gName,'0')
            btnDownload.close()
            btnCancel.show()

            if f not in self.fileFlowing:
                self.fileFlowing.append(f)


            def onStart():
                fc.onRecvStart(self.sWin,f)

            def onEnd(cond,size):
                fc.onRecvEnd(self.sWin,f)

                def fun():
                    children=self.FWidList[f].children()
                    if cond:
                        children[3].setValue(100)

                        children[-3].close()
                        children[-1].show()
                        children[4].close()
                        children[5].close()
                    else:
                        progressBar.reset()
                    si=int(size)
                    st=opFile.getByteToMb(si)
                    st=round(st,2)

                    children[-2].setText(f"Size -> {st} mb")

                self.timerFunList.append(fun)

            lc.funListRecvEnd[f]=[onStart,onEnd]


        if f in lc.funListRecvEnd:
            lc.funListRecvEnd[f][1]=onEnd


        def funCancelFile():
            self.c.cancelDownloadFile(f,self.gName,'0')
            progressBar.reset()
            self.c.functionList['g-'+self.gName+'-CancelDownloadFileChat']=self.handleCancelDownloadFile
            btnDownload.show()
            btnCancel.close()


        floc=dataStorageLocation+f
        def funOpenFile():
            cond=opFile.checkFileExist(floc)
            if cond:
                def fun():
                    con.execute_command(floc,False)
                threading.Thread(target=fun).start()
                
                showResult(self.statusbar,"File is opening",False)
            else:
                showResult(self.statusbar,"File not Exist")





        btnDownload.setText("Download")
        btnCancel.setText("Cancel")



        btnOpen.setText("Open")

        btnDownload.clicked.connect(funDownloadFile)
        btnCancel.clicked.connect(funCancelFile)
        btnOpen.clicked.connect(funOpenFile)



        labelSize.setAlignment(QtCore.Qt.AlignRight)

        if condYou:
            labelBackground.setGeometry(40,0,211,131)
            labelBackground.setStyleSheet(styleBackgroundUserYou)
            sendUser.setGeometry(50,5,191,16)
            sendUser.setText("@You")
            fileName.setGeometry(50,30,191,31)
            progressBar.setGeometry(50,70,191,23)
            btnDownload.setGeometry(50,100,75,23)
            btnCancel.setGeometry(50,100,75,23)
            labelSize.setGeometry(130,100,111,20)
            btnOpen.setGeometry(50,100,75,23)

            sendUser.setStyleSheet(styleUserNameU)
            fileName.setStyleSheet(styleFileNameU)
            labelSize.setStyleSheet(styleSizeU)
        else:
            labelBackground.setGeometry(0,0,211,131)
            labelBackground.setStyleSheet(styleBackgroundUser)
            sendUser.setGeometry(10,5,191,16)
            sendUser.setText("#"+sender)
            fileName.setGeometry(10,30,191,31)
            progressBar.setGeometry(10,70,191,23)
            btnDownload.setGeometry(10,100,75,23)
            btnCancel.setGeometry(10,100,75,23)
            labelSize.setGeometry(90,100,111,20)
            btnOpen.setGeometry(10,100,75,23)

            sendUser.setStyleSheet(styleUserNameA)
            fileName.setStyleSheet(styleFileNameA)
            labelSize.setStyleSheet(styleSizeA)

        cond=opFile.checkFileExist(floc)
        if cond and not fc.isFileRecv(self.sWin,f):
            btnDownload.close()
            btnCancel.close()
        else:
            btnOpen.close()
            if fc.isFileRecv(self.sWin,f):
                btnDownload.close()
            else:
                btnCancel.close()

        si=int(size)
        st=opFile.getByteToMb(si)
        st=round(st,2)
        labelSize.setText(f"Size -> {st} mb")



        sendUser.adjustSize()

        self.scrollHolder.addWidget(frame,dCount,0)

        self.count=dCount+1
        self.FWidList[f]=frame

        #self.scrollGG.verticalScrollBar().setValue(1000*self.count);

    def handleFileRuntime(self,msg):
        file=msg['file']
        size=msg['size']
        sender=msg['sender']
        self.formatRecvChatFile(sender,file,size)

    def handleRuntimeChatControl(self):

        if self.dataList is not None:
            data=self.dataList
            self.dataList=None

            for i in data:
                dt,info=i
                dt=dt.lower()
                if dt=='chat':

                    userName=info['userName']
                    chat=ds.dec(info['chat'])
                    self.insertChat(userName,chat)
                elif dt=='file':
                    sender=info['sender']
                    file=info['file']
                    size=info['size']
                    self.formatRecvChatFile(sender,file,size)
                else:
                    print(dt,"Unknown Type")

    def insertChat(self,userName,chat):
        dCount=self.count

        frame=QFrame(self.scrollContainer)
        frame.setFixedSize(250,51)

        styleBackgroundUser="""
        background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:0.983, y2:0, stop:0 rgba(127, 127, 127, 255), stop:1 rgba(255, 255, 255, 255));
        """

        styleBackgroundUserYou="""
        background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:0.983, y2:0, stop:0 rgba(0, 124, 0, 255), stop:1 rgba(255, 255, 255, 255));
        
        """

        styleUserNameU='''
        background-color: rgb(81, 255, 0);
        border: 1px solid #1C6EA4;

        '''

        styleFileNameU='''
        background-color: rgb(0, 124,0);
        color:rgb(255,255,255);
        '''

        styleUserNameA='''
        background-color: rgb(170, 170, 127);
        border: 1px solid #1C6EA4;
        '''

        styleFileNameA='''
        background-color: rgb(107, 107, 107);
        color: rgb(255, 255, 255);
        '''



        labelBackground=QLabel(frame)


        labelN=QLabel(frame)
        labelN.setText(userName)

        label=QLabel(frame)
        text=chat
        label.setWordWrap(True)
        label.setText(text)
        #label.setFixedWidth(180)
        cond=userName.lower()==self.c.userName.lower()

        if cond:

            labelN.setGeometry(50,5,191,16)
            label.setGeometry(50,30,191,16)
            label.setAlignment(QtCore.Qt.AlignRight)
            labelN.setAlignment(QtCore.Qt.AlignRight)

            labelN.setStyleSheet(styleUserNameU)
            label.setStyleSheet(styleFileNameU)


        else:
            labelN.setGeometry(10,5,191,16)

            label.setGeometry(10,30,191,16)
            labelN.setStyleSheet(styleUserNameA)
            label.setStyleSheet(styleFileNameA)
            #label.setAlignment(QtCore.Qt.AlignLeft)

        labelN.adjustSize()

        label.adjustSize()
        label.setFixedWidth(191)

        frame.setFixedHeight(label.height()+40)
        frame.adjustSize()

        if cond:
            labelBackground.setStyleSheet(styleBackgroundUserYou)
            labelBackground.setGeometry(40,0,211,frame.height())
        else:
            labelBackground.setStyleSheet(styleBackgroundUser)
            labelBackground.setGeometry(0,0,211,frame.height())

        self.scrollHolder.addWidget(frame,dCount,0)
        self.count=dCount+1
        self.scrollGG.verticalScrollBar().setValue(1000*self.count);

    def handleChatWindow(self,info):
        userName=info['userName']
        chat=ds.dec(info['chat'])
        self.insertChat(userName,chat)


    def handle(self,msg):

        def fun():
            info=msg
            code=info['code']
            if code=='k31s':
                groupName=info['groupName']

                chatData=ds.remodifyData(info['dataC'],info['dataCT'],info['dataCS'])
                ar=[]

                for i in chatData:
                    data=ds.dec(i)
                    dT,info=ad.deAssValue(data,True)
                    ar.append([dT,info])
                self.dataList=ar

            else:
                print("ERROR E#: "+code)
                showResult(self.statusbar,"Error :"+code)

        self.timerFunList.append(fun)

class XGroupChatViewProfile():

    def setupUi(self, MainWindow):
        self.mainWindow=MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(285, 187)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.labelGroupName = QtWidgets.QLabel(self.centralwidget)
        self.labelGroupName.setGeometry(QtCore.QRect(30, 30, 151, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.labelGroupName.setFont(font)
        self.labelGroupName.setObjectName("labelGroupName")
        self.btnBack = QtWidgets.QPushButton(self.centralwidget)
        self.btnBack.setGeometry(QtCore.QRect(190, 40, 75, 23))
        self.btnBack.setObjectName("btnBack")
        self.labelAdmin = QtWidgets.QLabel(self.centralwidget)
        self.labelAdmin.setGeometry(QtCore.QRect(30, 80, 151, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.labelAdmin.setFont(font)
        self.labelAdmin.setObjectName("labelAdmin")
        self.labelMembers = QtWidgets.QLabel(self.centralwidget)
        self.labelMembers.setGeometry(QtCore.QRect(30, 120, 151, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.labelMembers.setFont(font)
        self.labelMembers.setObjectName("labelMembers")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        XMainWindow.openWindows["GroupChat"]=True
        self.qTimer=QTimer()
        self.qTimer.setInterval(500)
        self.qTimer.timeout.connect(lambda :qTimerRefressFun(self.timerFunList))
        self.qTimer.start()
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.labelGroupName.setText(_translate("MainWindow", "GroupName"))
        self.btnBack.setText(_translate("MainWindow", "Back"))
        self.labelAdmin.setText(_translate("MainWindow", "Admin"))
        self.labelMembers.setText(_translate("MainWindow", "Members"))

    def init(self,c,gName):
        self.c=c
        self.gName=gName
        self.timerFunList=[]

        self.labelGroupName.setText(gName)
        self.send=c.send
        self.gc=xcs.GroupChat(self.send)


        lc.gcCond=False
        self.mainWindow.setWindowTitle(self.gName+" View Profile")
        self.mainWindow.closeEvent=self.onClose
        self.refress()


    def onClose(self,event):
        XMainWindow.openWindows['groupChat']=False
        event.accept()

    def refress(self):
        self.gc.loadGroupInfo(self.gName,'viewGroupProfile')
        self.c.functionList['viewGroupProfile']=self.handle

    def handle(self,msg):

        def fun():

            code=msg['code']
            info=msg
            if code=='y12k':
                gName=info['groupName']
                adminName=info['admin']

                mainData=ds.remodifyData(info['mdata'],info['mtypes'],info['mshape'])

                length=len(mainData)

                self.labelGroupName.setText(gName)
                self.labelMembers.setText("Members  :- "+str(length))
                self.labelAdmin.setText("Admin  :- "+adminName)

            else:
                showResult(self.statusbar,"Error :"+code)
                print("ERROR A%:"+code)

        self.timerFunList.append(fun)

class XGroupMeet():
    def setupUi(self, MainWindow):
        self.mainWindow=MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(229, 131)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.btnCreateMeeting = QtWidgets.QPushButton(self.centralwidget)
        self.btnCreateMeeting.setGeometry(QtCore.QRect(70, 30, 91, 23))
        self.btnCreateMeeting.setObjectName("btnCreateMeeting")
        self.btnJoinMeeting = QtWidgets.QPushButton(self.centralwidget)
        self.btnJoinMeeting.setGeometry(QtCore.QRect(70, 70, 91, 23))
        self.btnJoinMeeting.setObjectName("btnJoinMeeting")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.btnCreateMeeting.clicked.connect(self.funCreateMeeting)
        self.btnJoinMeeting.clicked.connect(self.funJoinMeeting)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btnCreateMeeting.setText(_translate("MainWindow", "Create Meeting"))
        self.btnJoinMeeting.setText(_translate("MainWindow", "Join Meeting"))

    def funBack(self,mainWindow):
        self.mainWindow.show()
        mainWindow.destroy()


    def funCreateMeeting(self):
        self.mainWindow.close()
        mainWindow=QMainWindow()
        lc.varStore['GroupMeetCreateMeeting']=mainWindow

        lc.gmCond=True
        XMainWindow.openWindows['groupMeet']=True

        self.gm=lc.XGroupMeetCJ()
        self.gm.setupUi(mainWindow)
        self.gm.init(self.c,True)
        self.gm.btnBack.clicked.connect(lambda : self.funBack(mainWindow))

        mainWindow.show()

    def funJoinMeeting(self):
        self.mainWindow.close()
        mainWindow=QMainWindow()
        lc.varStore['GroupMeetJoinMeeting']=mainWindow
        lc.gmCond=True
        XMainWindow.openWindows['groupMeet']=True
        self.gm=lc.XGroupMeetCJ()

        self.gm.setupUi(mainWindow)
        self.gm.editMeetingName.setPlaceholderText("Meeting Id")
        self.gm.btnCreate.setText("Join Meeting")
        self.gm.init(self.c)
        self.gm.btnBack.clicked.connect(lambda : self.funBack(mainWindow))
        mainWindow.show()


    def init(self,c):
        self.c=c

        lc.gmCond=False
        self.mainWindow.setWindowTitle("Group Meet")
        self.mainWindow.closeEvent=self.onClose


    def onClose(self,event):
        if not lc.gcCond:
            XMainWindow.openWindows['groupMeet']=False
        event.accept()

class XGroupMeetCJ():
    def setupUi(self, MainWindow):
        self.mainWindow=MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(312, 118)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.editMeetingName = QtWidgets.QLineEdit(self.centralwidget)
        self.editMeetingName.setGeometry(QtCore.QRect(30, 20, 113, 20))
        self.editMeetingName.setObjectName("editMeetingName")
        self.editMeetingPassword = QtWidgets.QLineEdit(self.centralwidget)
        self.editMeetingPassword.setGeometry(QtCore.QRect(170, 20, 113, 20))
        self.editMeetingPassword.setObjectName("editMeetingPassword")
        self.btnCreate = QtWidgets.QPushButton(self.centralwidget)
        self.btnCreate.setGeometry(QtCore.QRect(30, 60, 75, 23))
        self.btnCreate.setObjectName("btnCreate")
        self.btnBack = QtWidgets.QPushButton(self.centralwidget)
        self.btnBack.setGeometry(QtCore.QRect(170, 60, 75, 23))
        self.btnBack.setObjectName("btnBack")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.qTimer=QTimer()
        self.qTimer.setInterval(1000);
        self.qTimer.timeout.connect(self.funCall)
        self.qTimer.start();
        self.qTimerCond=True

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        self.qTimer2=QTimer()
        self.qTimer2.setInterval(500)
        self.qTimer2.timeout.connect(lambda :qTimerRefressFun(self.timerFunList))
        self.qTimer2.start()
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.editMeetingName.setPlaceholderText(_translate("MainWindow", "Meeting Name"))
        self.editMeetingPassword.setPlaceholderText(_translate("MainWindow", "Meeting Password"))
        self.btnCreate.setText(_translate("MainWindow", "Create -->"))
        self.btnBack.setText(_translate("MainWindow", "<-- Back"))

    def init(self,c,adminCond=False):
        self.gmms=None
        self.c=c
        self.adminCond=adminCond
        self.c=c
        self.send=c.send
        self.gm=xcs.GroupMeet(self.send)

        self.timerFunList=[]

        self.info=None
        self.info2=None

        if adminCond:
            self.mainWindow.setWindowTitle("Create Meeting")
            self.btnCreate.clicked.connect(self.funCreateMeeting)
        else:
            self.mainWindow.setWindowTitle("Join Meeting")
            self.btnCreate.clicked.connect(self.funJoinMeeting)

        lc.gmCond=False

        self.mainWindow.closeEvent=self.onClose


    def onClose(self,event):
        if not lc.gcCond:
            XMainWindow.openWindows['groupMeet']=False
        event.accept()


    def funCall(self):
        if self.qTimerCond==False:
            self.openSecondScreen(self.adminCond)
            self.qTimer.stop()


    def openSecondScreen(self,cond=False):

        self.mainWindow.close()
        mainWindow=QMainWindow()
        lc.varStore['GroupMeet12']=mainWindow

        self.gmms=lc.XGroupMeetMainScreen()
        self.gmms.setupUi(mainWindow)
        self.gmms.init(self.c,cond)
        self.gmms.initData(self.info)
        self.c.functionList['GroupMeet']=self.gmms.handle
        mainWindow.show()
        lc.gmCond=True
        XMainWindow.openWindows['groupMeet']=True

        if self.info2 is not None:
            data=self.info2[0]
            for i in data:
                if i.lower()==self.c.userName.lower():
                    continue
                self.gmms.initSmallFrame(i)

    def funCreateMeeting(self):
        name=self.editMeetingName.text()
        passw=self.editMeetingPassword.text()

        nm=lec.checkName(name)
        if nm==True:
            self.c.functionList['gmCreateMeeting']=self.handle
            self.gm.createMeeting(name,passw)
            self.btnCreate.setDisabled(True)
        else:
            showResult(self.statusbar,nm)



    def funJoinMeeting(self):
        self.c.functionList['gmJoinMeeting']=self.handle

        name=self.editMeetingName.text()

        ids=lec.checkMeetingId(name)

        if ids==True:
            passw=self.editMeetingPassword.text()

            self.gm.joinMeeting(name,passw)
            self.btnCreate.setDisabled(True)
        else:
            showResult(self.statusbar,ids)



    def handle(self,msg):

        def fun():

            wType=msg['wType']

            if wType=='gmCreateMeeting':
                self.btnCreate.setEnabled(True)
                self.handleCreateMeeting(msg)

            elif wType=='gmJoinMeeting':
                self.handleJoinMeeting(msg)

            else:
                print("ERROR :%^ "+wType)

        self.timerFunList.append(fun)

    def handleCreateMeeting(self,info):

        code=info['code']
        if code=='1122':
            #self.destroyAllElement()
            self.info=info
            self.qTimerCond=False
        else:
            showResult(self.statusbar,"Error :-"+code)
            print("ERROR :55 "+code)

    def handleJoinMeeting(self,info):
        code=info['code']


        if code=='ini2':
            data=ds.remodifyData(info['data'],info['type'],info['shape'])
            self.info2=data
            self.qTimerCond=False
            self.info=info



        elif code=='kkr1':
            self.btnCreate.setEnabled(True)
            showResult(self.statusbar,"Group Meeting Id don't exist")
        elif code=='1221':
            self.btnCreate.setEnabled(True)
            showResult(self.statusbar,"Incorrect Password")
        elif code=='eel3':
            self.btnCreate.setEnabled(True)
            showResult(self.statusbar,"Meeeting is Locked")

        elif code=='fer3':


            self.qTimerCond=False
            self.info=info
            #mm=xc.Meeting(self.root,self.c,False)
            #mm.initData(info)

        elif code=='ft65':
            showResult(self.statusbar,"Room auth req is on\n Wait for a min \n for ADMIN RESPONSE",False)
        elif code=='kke3':
            self.btnCreate.setEnabled(True)
            id=info['id']
            showResult(self.statusbar,"Admin of {0} Reject \nyour request".format(id))

        else:
            print("ERROR :-"+code)
            showResult(self.statusbar,"Error :-"+code)

class XGroupMeetMainScreen():
    def setupUi(self, MainWindow):
        self.mainWindow=MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(861, 522)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 20, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(30, 50, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(30, 80, 131, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.labelNameMeeting = QtWidgets.QLabel(self.centralwidget)
        self.labelNameMeeting.setGeometry(QtCore.QRect(200, 20, 161, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.labelNameMeeting.setFont(font)
        self.labelNameMeeting.setObjectName("labelNameMeeting")
        self.labelIdMeeting = QtWidgets.QLabel(self.centralwidget)
        self.labelIdMeeting.setGeometry(QtCore.QRect(200, 50, 161, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.labelIdMeeting.setFont(font)
        self.labelIdMeeting.setObjectName("labelIdMeeting")

        self.labelAdmin=QtWidgets.QLabel(self.centralwidget)
        self.labelAdmin.setText("Admin :-")
        self.labelAdmin.setGeometry(710,60,130,30)

        self.labelPasswordMeeting = QtWidgets.QLabel(self.centralwidget)
        self.labelPasswordMeeting.setGeometry(QtCore.QRect(200, 80, 181, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.labelPasswordMeeting.setFont(font)
        self.labelPasswordMeeting.setObjectName("labelPasswordMeeting")
        self.editMessage = QtWidgets.QLineEdit(self.centralwidget)
        self.editMessage.setGeometry(QtCore.QRect(30, 470, 161, 20))
        self.editMessage.setObjectName("editMessage")
        self.btnSend = QtWidgets.QPushButton(self.centralwidget)
        self.btnSend.setGeometry(QtCore.QRect(200, 470, 75, 23))
        self.btnSend.setObjectName("btnSend")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(450, 20, 131, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.radioLockOn = QtWidgets.QRadioButton(self.centralwidget)
        self.radioLockOn.setGeometry(QtCore.QRect(450, 50, 82, 17))
        self.radioLockOn.setObjectName("radioLockOn")
        self.radioLockOff = QtWidgets.QRadioButton(self.centralwidget)
        self.radioLockOff.setGeometry(QtCore.QRect(570, 50, 82, 17))
        self.radioLockOff.setObjectName("radioLockOff")
        self.radioAuthReqOn = QtWidgets.QRadioButton(self.centralwidget)
        self.radioAuthReqOn.setGeometry(QtCore.QRect(450, 80, 82, 17))
        self.radioAuthReqOn.setObjectName("radioAuthReqOn")
        self.radioAuthReqOff = QtWidgets.QRadioButton(self.centralwidget)
        self.radioAuthReqOff.setGeometry(QtCore.QRect(570, 80, 82, 17))
        self.radioAuthReqOff.setObjectName("radioAuthReqOff")
        self.btnLeaveMeeting = QtWidgets.QPushButton(self.centralwidget)
        self.btnLeaveMeeting.setGeometry(QtCore.QRect(750, 20, 81, 23))
        self.btnLeaveMeeting.setStyleSheet("background-color: rgb(255, 0, 0);")
        self.btnLeaveMeeting.setObjectName("btnLeaveMeeting")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(320, 140, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.labelUserView = QtWidgets.QLabel(self.centralwidget)
        self.labelUserView.setGeometry(QtCore.QRect(320, 170, 321, 211))
        self.labelUserView.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.labelUserView.setText("")
        self.labelUserView.setObjectName("labelUserView")
        self.labelYourView = QtWidgets.QLabel(self.centralwidget)
        self.labelYourView.setGeometry(QtCore.QRect(680, 170, 161, 111))
        self.labelYourView.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.labelYourView.setText("")
        self.labelYourView.setObjectName("labelYourView")
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(680, 140, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.radioCameraOn = QtWidgets.QRadioButton(self.centralwidget)
        self.radioCameraOn.setGeometry(QtCore.QRect(680, 320, 82, 17))
        self.radioCameraOn.setObjectName("radioCameraOn")
        self.radioCameraOff = QtWidgets.QRadioButton(self.centralwidget)
        self.radioCameraOff.setGeometry(QtCore.QRect(770, 320, 82, 17))
        self.radioCameraOff.setObjectName("radioCameraOff")
        self.radioMicOn = QtWidgets.QRadioButton(self.centralwidget)
        self.radioMicOn.setGeometry(QtCore.QRect(680, 350, 82, 17))
        self.radioMicOn.setObjectName("radioMicOn")
        self.radioMicOff = QtWidgets.QRadioButton(self.centralwidget)
        self.radioMicOff.setGeometry(QtCore.QRect(770, 350, 82, 17))
        self.radioMicOff.setObjectName("radioMicOff")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(20, 110, 811, 21))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(410, 30, 3, 61))
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setGeometry(QtCore.QRect(700, 30, 3, 61))
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.line_4 = QtWidgets.QFrame(self.centralwidget)
        self.line_4.setGeometry(QtCore.QRect(300, 140, 20, 341))
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.line_5 = QtWidgets.QFrame(self.centralwidget)
        self.line_5.setGeometry(QtCore.QRect(650, 130, 20, 241))
        self.line_5.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.line_6 = QtWidgets.QFrame(self.centralwidget)
        self.line_6.setGeometry(QtCore.QRect(320, 390, 521, 16))
        self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.line_7 = QtWidgets.QFrame(self.centralwidget)
        self.line_7.setGeometry(QtCore.QRect(700, 300, 118, 3))
        self.line_7.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_7.setObjectName("line_7")
        self.labelLockStatus = QtWidgets.QLabel(self.centralwidget)
        self.labelLockStatus.setGeometry(QtCore.QRect(450, 50, 161, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelLockStatus.setFont(font)
        self.labelLockStatus.setObjectName("labelLockStatus")
        self.labelAuthReqStatus = QtWidgets.QLabel(self.centralwidget)
        self.labelAuthReqStatus.setGeometry(QtCore.QRect(450, 80, 161, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelAuthReqStatus.setFont(font)
        self.labelAuthReqStatus.setObjectName("labelAuthReqStatus")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


        self.groupBtnLock=QButtonGroup(self.centralwidget)
        self.groupBtnLock.addButton(self.radioLockOn)
        self.groupBtnLock.addButton(self.radioLockOff)
        self.groupBtnLock.buttonClicked.connect(self.onChangeLockOn)

        self.groupBtnAuthReq=QButtonGroup(self.centralwidget)
        self.groupBtnAuthReq.addButton(self.radioAuthReqOn)
        self.groupBtnAuthReq.addButton(self.radioAuthReqOff)
        self.groupBtnAuthReq.buttonClicked.connect(self.onChangeAuthReq)

        self.groupBtnCamera=QButtonGroup(self.centralwidget)
        self.groupBtnCamera.addButton(self.radioCameraOn)
        self.groupBtnCamera.addButton(self.radioCameraOff)
        self.groupBtnCamera.buttonClicked.connect(self.onChangeSendCamera)

        self.groupBtnMic=QButtonGroup(self.centralwidget)
        self.groupBtnMic.addButton(self.radioMicOn)
        self.groupBtnMic.addButton(self.radioMicOff)
        self.groupBtnMic.buttonClicked.connect(self.onChangeSendMic)

        self.qTimer=QTimer()
        self.qTimer.setInterval(100)
        self.qTimer.timeout.connect(self.handleOnFunInterval)
        self.qTimer.start()

    def retranslateUi(self, MainWindow):

        self.qTimer2=QTimer()
        self.qTimer2.setInterval(5)
        self.qTimer2.timeout.connect(lambda :qTimerRefressFun(self.timerFunList))
        self.qTimer2.start()

        self.scrollContainerChat,self.scrollGGChat,self.scrollHolderChat=pqc.scrollBarWithSA(self.centralwidget,20,140,270,320)
        self.scrollContainerMem,self.scrollGGMem,self.scrollHolderMem=pqc.scrollBarWithSA(self.centralwidget,320,410,520,80)

        self.btnLeaveMeeting.clicked.connect(self.funLeaveMeeting)
        self.btnSend.clicked.connect(self.funSendChat)

        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Meeting Name "))
        self.label_2.setText(_translate("MainWindow", "Meeting Id"))
        self.label_3.setText(_translate("MainWindow", "Meeting Password"))
        self.labelNameMeeting.setText(_translate("MainWindow", "Name of the Meeting"))
        self.labelIdMeeting.setText(_translate("MainWindow", "Id of the Meeting"))
        self.labelPasswordMeeting.setText(_translate("MainWindow", "Password of the Meeting"))
        self.editMessage.setPlaceholderText(_translate("MainWindow", "Message"))
        self.btnSend.setText(_translate("MainWindow", "Send"))
        self.label_7.setText(_translate("MainWindow", "Sequrity"))
        self.radioLockOn.setText(_translate("MainWindow", "Lock On"))
        self.radioLockOff.setText(_translate("MainWindow", "Lock Off"))
        self.radioAuthReqOn.setText(_translate("MainWindow", "Auth Req On"))
        self.radioAuthReqOff.setText(_translate("MainWindow", "Auth Req Off"))
        self.btnLeaveMeeting.setText(_translate("MainWindow", "Leave Meeting"))
        self.label_8.setText(_translate("MainWindow", "User View"))
        self.label_11.setText(_translate("MainWindow", "Your View"))
        self.radioCameraOn.setText(_translate("MainWindow", "Camera On"))
        self.radioCameraOff.setText(_translate("MainWindow", "Camera Off"))
        self.radioMicOn.setText(_translate("MainWindow", "Mic On"))
        self.radioMicOff.setText(_translate("MainWindow", "Mic Off"))
        self.labelLockStatus.setText(_translate("MainWindow", "Lock Room Status"))
        self.labelAuthReqStatus.setText(_translate("MainWindow", "Auth Request Status"))

    def funLeaveMeeting(self):

        if self.radioCameraOn.isChecked():
            self.radioCameraOff.setChecked(True)
            self.onChangeSendCamera()
            print("HELLO")

        if self.radioMicOn.isChecked():
            print("HI")
            self.radioMicOff.setChecked(True)
            self.onChangeSendMic()
        print("FDLKFDL")
        XMainWindow.openWindows['groupMeet']=False

        self.gm.gmLeaveMeeting()
        self.mainWindow.destroy()

    def init(self,c,adminCond=False):
        self.c=c
        self.adminCond=adminCond
        self.condAdmin=adminCond
        self.send=c.send
        self.gm=xcs.GroupMeet(self.send)
        self.memberFunList=[]

        self.countChat=0
        self.countMember=0
        self.timerFunList=[]

        self.FWidListChat={}
        self.FWidListMember={}

        self.sendC={}
        self.sendM={}

        self.defaultSettings()

        XMainWindow.xprtControl.funOpenWindow("@meet")

        if adminCond:
            self.labelLockStatus.close()
            self.labelAuthReqStatus.close()
        else:
            self.radioAuthReqOff.close()
            self.radioAuthReqOn.close()
            self.radioLockOff.close()
            self.radioLockOn.close()
        lc.gmCond=False
        self.mainWindow.setWindowTitle("Group Meet Main Screen")
        self.mainWindow.closeEvent=self.onClose

    def defaultSettings(self):
        self.radioLockOff.setChecked(True)
        self.radioAuthReqOff.setChecked(True)
        self.radioCameraOff.setChecked(True)
        self.radioMicOff.setChecked(True)


    def onClose(self,event):
        if not lc.gcCond:
            XMainWindow.openWindows['groupMeet']=False


        self.gm.gmLeaveMeeting();
        if self.radioCameraOn.isChecked():
            self.radioCameraOff.setChecked(True)
            self.onChangeSendCamera()
            print("HELLO")

        if self.radioMicOn.isChecked():
            print("HI")
            self.radioMicOff.setChecked(True)
            self.onChangeSendMic()
        event.accept()

    def initData(self,info):

        name=info['name']
        password=info['password']
        mid=info['id']
        self.setMeetingFunction()
        self.labelNameMeeting.setText(name)
        self.labelIdMeeting.setText(mid)
        self.labelPasswordMeeting.setText(password)

        if not self.adminCond :
            adminName=info['admin']
            self.labelAdmin.setText('#Admin :'+adminName)

        if self.adminCond:
            showResult(self.statusbar,"Group Meeting Created Successfully",False)
            self.labelAdmin.setText("You are the #ADMIN")
        else:
            showResult(self.statusbar,"Group Meeting Joined Successfully",False)

    def setMeetingFunction(self):
        self.frameListUser={}
        self.imgDict={}
        self.imgCounter={}
        self.impCond={}
        self.nameMainView=None

    def handle(self,msg):

        def fun():

            wType=msg['wType']
            info=msg
            if wType=='gmLockMeeting':
                self.handleLockMeeting(msg)
            elif wType=='gmAuthRequest':
                self.handleAuthRequest(msg)
            elif wType=='gmJoinClientRequest':
                self.handleJoinClientRequest(msg)
            elif wType=='gmJoiningResponse':
                self.handleJoiningResponse(msg)
            elif wType=='gmLeaveMeeting':
                self.handleLeaveMeeting(msg)
            elif wType=='gmSendChat':
                self.handleSendChat(msg)
            elif wType=='gmKickOut':
                self.handleKickOut(msg)
            elif wType=='gmInfoUpdate':
                self.handleInfoUpdate(msg)
            elif wType=='gmSendDetailOfMember':
                self.handleSendDetailOfMember(msg)
            elif wType=='gmAudData':
                self.handleAudData(msg)
            elif wType=='gmImgData':
                self.handleImgData(msg)
            elif wType=='gmOnClose':
                self.handleLeaveMeeting(msg)
            else:
                print(" THIS ERROR I DONT KNOW WY ",wType,msg['code'])
                showResult(self.statusbar,"Error :"+wType)

        self.timerFunList.append(fun)

    def handleInfoUpdate(self,info):
        code=info['code']
        if code=='kr14':
            self.handleLockMeeting(info)
        elif code=='kr13':
            self.handleAuthRequest(info)
        else:
            print("THIS IS BLUDFL INFO ",code)
            showResult(self.statusbar,"Error :"+code)

    def handleLockMeeting(self,info):
        code=info['code']

        if code=='kr14':
            value=info['value']
            if value=='1':

                self.labelLockStatus.setText("Meeting Room is locked")
            else:
                self.labelLockStatus.setText("Meeting Room is open")
        else:
            print("THIS IS LOCK MMETING ERROR ",code)
            showResult(self.statusbar,"Error :"+code)

    def handleAuthRequest(self,info):
        code=info['code']

        if code=='kr13':
            value=info['value']
            if value=='1':
                self.labelAuthReqStatus.setText("Authentification Request is On")
            else:
                self.labelAuthReqStatus.setText("Authentification Request is Off")
        else:
            print("this is mistake in auth req ",code)
            showResult(self.statusbar,'Error :'+code)

    def handleOnFunInterval(self):
        funList=self.memberFunList

        if len(funList)>0:
            funList[0]()
            self.memberFunList.pop(0)

    def handleJoinClientRequest(self,info):
        code=info['code']

        if code=='1er4':
            userName=info['userName']

            windowName=userName.lower()+'- > Join Request'
            cond=self.checkOpenWindow(windowName)
            if cond:
                pass

            else:

                def fun():
                    lc.XMainWindow.openWindows[windowName]=True
                    mainWindow=QMainWindow()

                    def funAccept():
                        lc.XMainWindow.openWindows[windowName]=False
                        self.gm.sendJoinClientRequestResponse(userName)
                        mainWindow.destroy()


                    def funReject():
                        lc.XMainWindow.openWindows[windowName]=False

                        self.gm.sendJoinClientRequestResponse(userName,'0')
                        mainWindow.destroy()

                    def funOnClose(event):
                        lc.XMainWindow.openWindows[windowName]=False
                        self.gm.sendJoinClientRequestResponse(userName,'0')
                        event.accept()



                    gmjr=lc.XGroupMeetJoinRequest()
                    gmjr.setupUi(mainWindow)
                    gmjr.labelText.setText(userName+' want to join the Meeting')
                    gmjr.btnAccept.clicked.connect(funAccept)
                    mainWindow.closeEvent=funOnClose
                    gmjr.btnReject.clicked.connect(funReject)
                    mainWindow.show()
                self.memberFunList.append(fun)
        else:
            print("THIS IS UNKNOWN KIND OF CODE ",code)
            showResult(self.statusbar,"Error :"+code)

    def handleJoiningResponse(self,info):
        data=ds.remodifyData(info['data'],info['type'],info['shape'])
        data=data[0]
        for i in data:
            if i.lower()==self.c.userName.lower():
                continue
            self.initSmallFrame(i)

    def handleLeaveMeeting(self,info):
        code=info['code']

        if code=='aa00':
            #Admin Left Meeting
            def fun():
                userName=info['userName'].lower()

                if self.radioCameraOn.isChecked():

                    self.radioCameraOff.setChecked(True)
                    self.onChangeSendCamera()

                if self.radioMicOn.isChecked():
                    self.radioMicOff.setChecked(True)
                    self.onChangeSendMic()
                txt='@A-{0} Left the meeting'.format(userName)
                showResult(self.statusbar,txt)


                #XMainWindow.openWindows['groupMeet']=False
                #time.sleep(3)

                self.mainWindow.setDisabled(True)

            self.memberFunList.append(fun)


        elif code=='mm00':
            def fun():
                userName=info['userName'].lower()

                showResult(self.statusbar,"@M-{0} left the Meeting".format(userName))

                list=self.FWidListMember[userName]

                list.deleteLater()
                #Member Left Meeting
                #I Love you Anjali Friday,December 18 2020


                #I just want to say this magical times many times but i dont know
                #How much time.

            self.memberFunList.append(fun)

        else:
            print("This is bludender type of mistake in a group ",code)

    def funSendChat(self):
        chat=self.editMessage.text()

        if chat=='':
            pass
        else:
            self.editMessage.setText('')
            data=self.insertChatGui(chat,self.c.userName)
            self.gm.sendChat(data)

    def insertChatGui(self,chat,userName):

        dcount=self.countChat

        frame=QFrame(self.scrollContainerChat)
        frame.setFixedSize(250,51)

        styleBackgroundUser="""
        background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:0.983, y2:0, stop:0 rgba(127, 127, 127, 255), stop:1 rgba(255, 255, 255, 255));
        """

        styleBackgroundUserYou="""
        background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:0.983, y2:0, stop:0 rgba(0, 124, 0, 255), stop:1 rgba(255, 255, 255, 255));
        
        """

        styleUserNameU='''
        background-color: rgb(81, 255, 0);
        border: 1px solid #1C6EA4;

        '''

        styleFileNameU='''
        background-color: rgb(0, 124,0);
        color:rgb(255,255,255);
        '''

        styleUserNameA='''
        background-color: rgb(170, 170, 127);
        border: 1px solid #1C6EA4;
        '''

        styleFileNameA='''
        background-color: rgb(107, 107, 107);
        color: rgb(255, 255, 255);
        '''



        labelBackground=QLabel(frame)


        labelN=QLabel(frame)
        labelN.setText(userName)

        label=QLabel(frame)
        text=chat
        label.setWordWrap(True)
        label.setText(text)
        #label.setFixedWidth(180)
        cond=userName.lower()==self.c.userName.lower()

        if cond:

            labelN.setGeometry(50,5,191,16)
            label.setGeometry(50,30,191,16)
            label.setAlignment(QtCore.Qt.AlignRight)
            labelN.setAlignment(QtCore.Qt.AlignRight)

            labelN.setStyleSheet(styleUserNameU)
            label.setStyleSheet(styleFileNameU)


        else:
            labelN.setGeometry(10,5,191,16)

            label.setGeometry(10,30,191,16)
            labelN.setStyleSheet(styleUserNameA)
            label.setStyleSheet(styleFileNameA)
            #label.setAlignment(QtCore.Qt.AlignLeft)

        labelN.adjustSize()

        label.adjustSize()
        label.setFixedWidth(191)

        frame.setFixedHeight(label.height()+40)
        frame.adjustSize()

        if cond:
            labelBackground.setStyleSheet(styleBackgroundUserYou)
            labelBackground.setGeometry(40,0,211,frame.height())
        else:
            labelBackground.setStyleSheet(styleBackgroundUser)
            labelBackground.setGeometry(0,0,211,frame.height())

        self.scrollHolderChat.addWidget(frame,dcount,0)
        self.countChat=dcount+1

        chat=ds.enc(text)
        data=ad.assValue(['userName','chat'],[self.c.userName,chat],'MeetingChat')
        return data

    def handleSendChat(self,info):
        code=info['code']

        if code=='9211':
            chat=info['chat']
            #userName=info['userName']

            dchat=ds.dec(chat)
            dType,inf=ad.deAssValue(dchat,True)
            chat=inf['chat']
            dchat=ds.dec(chat)
            userName=inf['userName']

            def fun():
                self.insertChatGui(dchat,userName)

            self.memberFunList.append(fun)


        else:
            print("This is chatting error ",code)

    def handleKickOut(self,info):
        code=info['code']

        if code=='98kk':
            showResult(self.statusbar,"You are kicked from the meeting")
            time.sleep(2)
            def fun():
                if self.radioCameraOn.isChecked():

                    self.radioCameraOff.setChecked(True)
                    self.onChangeSendCamera()

                if self.radioMicOn.isChecked():
                    self.radioMicOff.setChecked(True)
                    self.onChangeSendMic()


                self.mainWindow.setDisabled(True)

            self.memberFunList.append(fun)


        elif code=='99kk':
            #User has been kickouted
            if not self.condAdmin:
                userName=info['userName'].lower()
                showResult(self.statusbar,"{0} has been kicked from the meeting".format(userName))

                def fun():
                    list=self.FWidListMember[userName]
                    list.deleteLater()

                self.memberFunList.append(fun)

        else:
            print("THIS IS BLUNEDER MISTAKE ",code)

    def handleSendDetailOfMember(self,info):
        code=info['code']

        if code=='adm1':
            self.initSmallFrame(info['userName'].lower())

    def handleAudData(self,info):
        userName=info['userName'].lower()
        if userName in self.sendM:
            cond=self.sendM[userName].isChecked()

            if cond:
                data=info['data']
                ddata=ds.decb(bytes(data,'utf-8'))
                con.play_audio(stream,ddata)

    def handleImgData(self,info):
        userName=info['userName'].lower()
        if userName in self.sendC:
            cond=self.sendC[userName].isChecked()
            if cond:

                data=ds.remodifyData(info['data'],info['type'],info['shape'])
                if self.nameMainView==userName:

                    fdata=data.copy()
                    self.mainViewHandler(fdata)
                rimg=cv2.resize(data,(41,31))
                img=pqc.cv2toPqImage(rimg)

                frame=self.FWidListMember[userName]
                children=frame.children()
                children[0].setPixmap(img)

    def mainViewHandler(self,image):

        img=cv2.resize(image,(321,211))
        pimg=pqc.cv2toPqImage(img)
        self.labelUserView.setPixmap(pimg)

    def checkOpenWindow(self,windowName):
        if windowName in lc.XMainWindow.openWindows:
            return lc.XMainWindow.openWindows[windowName]
        else:
            return False

    def onChangeLockOn(self):
        if(self.radioLockOn.isChecked()):
            value=1
        else:
            value=0

        self.gm.lockMeeting(str(value));

    def onChangeAuthReq(self):
        if(self.radioAuthReqOn.isChecked()):
            value=1
        else:
            value=0
        self.gm.authRequest(str(value));

    def showCameraView(self):

        def fun():

            while self.radioCameraOn.isChecked():
                frame=con.camFrame
                if frame is not None:
                    frame=cv2.resize(frame,(160,111))
                    frame=pqc.cv2toPqImage(frame)
                    self.labelYourView.setPixmap(frame)
                time.sleep(0.03)



        class MThread(QThread):

            def run(self):
                fun()
        self.threadShowCamera=MThread()
        self.threadShowCamera.start()

    def onChangeSendCamera(self):
        if(self.radioCameraOn.isChecked()):
            value=1
        else:
            value=0
        value=str(value)
        def fun():
            pass
        if value=='1':
            XMainWindow.xprtControl.funFirstOnList['camera']=fun
            XMainWindow.xprtControl.funOnSending('@meet','camera')
            self.gm.gmUpdateYourSendCont('img','1')
            self.showCameraView()
        else:
            XMainWindow.xprtControl.funOffSending('@meet','camera')
            self.gm.gmUpdateYourSendCont('img','0')

    def onChangeSendMic(self):
        if(self.radioMicOn.isChecked()):
            value=1
        else:
            value=0
        def fun():
            pass
        value=str(value)
        if value=='1':
            XMainWindow.xprtControl.funFirstOnList['sound']=fun
            XMainWindow.xprtControl.funOnSending('@meet','sound')
            self.gm.gmUpdateYourSendCont('aud','1')
        else:
            XMainWindow.xprtControl.funOffSending('@meet','sound')
            self.gm.gmUpdateYourSendCont('aud','0')

    def initSmallFrame(self,i):
        def fun():
            def funOk():
                self.nameMainView=i
                self.label_8.setText(i)

            def funKick(i):
                self.gm.kickOut(i)
                us = self.FWidListMember[i]
                us.deleteLater()

            def funContImg(checkBox):

                if checkBox.isChecked():
                    value='1'
                else:
                    value='0'

                self.gm.gmUpdateUCamCont(i,value)

            def funContMic(checkBox):

                if checkBox.isChecked():
                    value='1'
                else:
                    value='0'
                self.gm.gmUpdateUMicCont(i,value)


            dcount=self.countMember

            frame=QFrame(self.scrollContainerMem)
            frame.setFixedSize(151,71)

            labelUView=QLabel(frame)
            labelUView.setGeometry(10,5,40,30)

            labelName=QLabel(frame)
            labelName.setText(i)
            labelName.setGeometry(60,5,61,16)

            checkBoxCam=QCheckBox(frame)
            checkBoxCam.setText("C")
            checkBoxCam.setGeometry(60,21,31,17)
            checkBoxCam.clicked.connect(lambda :funContImg(checkBoxCam))

            checkBoxMic=QCheckBox(frame)
            checkBoxMic.setText("M")
            checkBoxMic.setGeometry(100,21,31,17)
            checkBoxMic.clicked.connect(lambda :funContMic(checkBoxMic))


            btnKick=QPushButton(frame)
            btnKick.setGeometry(10,42,41,23)
            btnKick.setText("Kick")
            btnKick.clicked.connect(lambda :funKick(i))

            btnOk=QPushButton(frame)
            btnOk.setGeometry(80,40,41,23)
            btnOk.setText("_/")
            btnOk.clicked.connect(funOk)

            line=QFrame(frame)
            line.setGeometry(125,4,20,61)
            line.setFrameShape(QFrame.VLine)
            line.setFrameShadow(QFrame.Sunken)

            self.scrollHolderMem.addWidget(frame,0,dcount)


            self.sendC[i]=checkBoxCam
            self.sendM[i]=checkBoxMic


            self.FWidListMember[i]=frame
            if not self.condAdmin:
                btnKick.setDisabled(True)

            self.countMember=dcount+1
            #self.scrollGGMem.horizontalScrollBar().setValue(10000)

        self.memberFunList.append(fun)

class XGroupMeetJoinRequest():
    def setupUi(self, MainWindow):
        self.mainWindow=MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(358, 120)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.labelText = QtWidgets.QLabel(self.centralwidget)
        self.labelText.setGeometry(QtCore.QRect(30, 10, 291, 41))
        self.labelText.setSizeIncrement(QtCore.QSize(0, 2))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.labelText.setFont(font)
        self.labelText.setWordWrap(True)
        self.labelText.setObjectName("labelText")
        self.btnAccept = QtWidgets.QPushButton(self.centralwidget)
        self.btnAccept.setGeometry(QtCore.QRect(30, 70, 75, 23))
        self.btnAccept.setObjectName("btnAccept")
        self.btnReject = QtWidgets.QPushButton(self.centralwidget)
        self.btnReject.setGeometry(QtCore.QRect(250, 70, 75, 23))
        self.btnReject.setObjectName("btnReject")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.labelText.setText(_translate("MainWindow", "TextLabel"))
        self.btnAccept.setText(_translate("MainWindow", "Accept"))
        self.btnReject.setText(_translate("MainWindow", "Reject"))
        self.mainWindow.setWindowTitle("Group Meet Join Request")

class XChatWindowMember():

    def setupUi(self, MainWindow):
        self.mainWindow=MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(652, 454)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.labelProfilePic = QtWidgets.QLabel(self.centralwidget)
        self.labelProfilePic.setGeometry(QtCore.QRect(20, 20, 81, 91))
        self.labelProfilePic.setStyleSheet("background-color: rgb(0, 255, 255);")
        self.labelProfilePic.setText("")
        self.labelProfilePic.setObjectName("labelProfilePic")

        self.qTimer=QTimer()
        self.qTimer.setInterval(500)
        self.qTimer.timeout.connect(self.funQTimer)
        self.qTimer.start()


        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(130, 20, 91, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setMouseTracking(True)
        self.label_2.setMidLineWidth(1)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(130, 50, 91, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.label_3.setFont(font)
        self.label_3.setMouseTracking(True)
        self.label_3.setMidLineWidth(1)
        self.label_3.setObjectName("label_3")
        self.labelUserName = QtWidgets.QLabel(self.centralwidget)
        self.labelUserName.setGeometry(QtCore.QRect(230, 20, 111, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelUserName.sizePolicy().hasHeightForWidth())
        self.labelUserName.setSizePolicy(sizePolicy)
        self.labelUserName.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.labelUserName.setFont(font)
        self.labelUserName.setMouseTracking(True)
        self.labelUserName.setMidLineWidth(1)
        self.labelUserName.setObjectName("labelUserName")
        self.labelFullName = QtWidgets.QLabel(self.centralwidget)
        self.labelFullName.setGeometry(QtCore.QRect(230, 50, 91, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelFullName.sizePolicy().hasHeightForWidth())
        self.labelFullName.setSizePolicy(sizePolicy)
        self.labelFullName.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.labelFullName.setFont(font)
        self.labelFullName.setMouseTracking(True)
        self.labelFullName.setMidLineWidth(1)
        self.labelFullName.setObjectName("labelFullName")
        self.labelStatus = QtWidgets.QLabel(self.centralwidget)
        self.labelStatus.setGeometry(QtCore.QRect(230, 90, 20, 20))
        self.labelStatus.setStyleSheet("background-color: rgb(255, 0, 0);")
        self.labelStatus.setText("")
        self.labelStatus.setObjectName("labelStatus")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(130, 90, 91, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.label_7.setFont(font)
        self.label_7.setMouseTracking(True)
        self.label_7.setMidLineWidth(1)
        self.label_7.setObjectName("label_7")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(110, 10, 20, 101))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(130, 70, 201, 16))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(40, 160, 611, 271))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.tabWidget.setFont(font)
        self.tabWidget.setObjectName("tabWidget")
        self.tabTextFile = QtWidgets.QWidget()
        self.tabTextFile.setObjectName("tabTextFile")

        self.scrollContainer,self.scrollGG,self.scrollHolder=pqc.scrollBarWithSA(self.tabTextFile,10,10,291,221)


        self.editMessage = QtWidgets.QLineEdit(self.tabTextFile)
        self.editMessage.setGeometry(QtCore.QRect(330, 200, 161, 20))
        self.editMessage.setObjectName("editMessage")
        self.btnSendText = QtWidgets.QPushButton(self.tabTextFile)
        self.btnSendText.setGeometry(QtCore.QRect(520, 200, 75, 23))
        self.btnSendText.setObjectName("btnSendText")
        self.btnSetFile = QtWidgets.QPushButton(self.tabTextFile)
        self.btnSetFile.setGeometry(QtCore.QRect(330, 160, 75, 23))
        self.btnSetFile.setObjectName("btnSetFile")
        self.btnSendFile = QtWidgets.QPushButton(self.tabTextFile)
        self.btnSendFile.setGeometry(QtCore.QRect(520, 160, 75, 23))
        self.btnSendFile.setObjectName("btnSendFile")
        self.line_4 = QtWidgets.QFrame(self.tabTextFile)
        self.line_4.setGeometry(QtCore.QRect(300, 10, 16, 221))
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.tabWidget.addTab(self.tabTextFile, "")
        self.tabCamSound = QtWidgets.QWidget()
        self.tabCamSound.setObjectName("tabCamSound")
        self.label_8 = QtWidgets.QLabel(self.tabCamSound)
        self.label_8.setGeometry(QtCore.QRect(30, 10, 111, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.label_8.setFont(font)
        self.label_8.setMouseTracking(True)
        self.label_8.setMidLineWidth(1)
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.tabCamSound)
        self.label_9.setGeometry(QtCore.QRect(430, 20, 111, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        self.label_9.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.label_9.setFont(font)
        self.label_9.setMouseTracking(True)
        self.label_9.setMidLineWidth(1)
        self.label_9.setObjectName("label_9")
        self.labelSendCamera = QtWidgets.QLabel(self.tabCamSound)
        self.labelSendCamera.setGeometry(QtCore.QRect(20, 50, 170, 121))
        self.labelSendCamera.setStyleSheet("background-color: rgb(0, 255, 255);")
        self.labelSendCamera.setText("")
        self.labelSendCamera.setObjectName("labelSendCamera")
        self.labelRecvCamera = QtWidgets.QLabel(self.tabCamSound)
        self.labelRecvCamera.setGeometry(QtCore.QRect(420, 60, 170, 121))
        self.labelRecvCamera.setStyleSheet("background-color: rgb(0, 255, 255);")
        self.labelRecvCamera.setText("")
        self.labelRecvCamera.setObjectName("labelRecvCamera")
        self.radCamSendOn1 = QtWidgets.QRadioButton(self.tabCamSound)
        self.radCamSendOn1.setGeometry(QtCore.QRect(20, 190, 51, 17))
        self.radCamSendOn1.setObjectName("radCamSendOn1")
        self.radCamSendOff1 = QtWidgets.QRadioButton(self.tabCamSound)
        self.radCamSendOff1.setGeometry(QtCore.QRect(90, 190, 51, 17))
        self.radCamSendOff1.setObjectName("radCamSendOff1")
        self.radCamRecvOn1 = QtWidgets.QRadioButton(self.tabCamSound)
        self.radCamRecvOn1.setGeometry(QtCore.QRect(430, 200, 51, 17))
        self.radCamRecvOn1.setObjectName("radCamRecvOn1")
        self.radCamRecvOff1 = QtWidgets.QRadioButton(self.tabCamSound)
        self.radCamRecvOff1.setGeometry(QtCore.QRect(490, 200, 51, 17))
        self.radCamRecvOff1.setObjectName("radCamRecvOff1")
        self.line_3 = QtWidgets.QFrame(self.tabCamSound)
        self.line_3.setGeometry(QtCore.QRect(210, 10, 20, 211))
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.line_5 = QtWidgets.QFrame(self.tabCamSound)
        self.line_5.setGeometry(QtCore.QRect(370, 10, 20, 211))
        self.line_5.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.label_12 = QtWidgets.QLabel(self.tabCamSound)
        self.label_12.setGeometry(QtCore.QRect(240, 10, 111, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy)
        self.label_12.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.label_12.setFont(font)
        self.label_12.setMouseTracking(True)
        self.label_12.setMidLineWidth(1)
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(self.tabCamSound)
        self.label_13.setGeometry(QtCore.QRect(240, 40, 111, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy)
        self.label_13.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.label_13.setFont(font)
        self.label_13.setMouseTracking(True)
        self.label_13.setMidLineWidth(1)
        self.label_13.setObjectName("label_13")
        self.radSouSendOff1 = QtWidgets.QRadioButton(self.tabCamSound)
        self.radSouSendOff1.setGeometry(QtCore.QRect(300, 80, 51, 17))
        self.radSouSendOff1.setObjectName("radSouSendOff1")
        self.radSouSendOn1 = QtWidgets.QRadioButton(self.tabCamSound)
        self.radSouSendOn1.setGeometry(QtCore.QRect(240, 80, 51, 17))
        self.radSouSendOn1.setObjectName("radSouSendOn1")
        self.radSouRecvOff1 = QtWidgets.QRadioButton(self.tabCamSound)
        self.radSouRecvOff1.setGeometry(QtCore.QRect(300, 180, 51, 17))
        self.radSouRecvOff1.setObjectName("radSouRecvOff1")
        self.radSouRecvOn1 = QtWidgets.QRadioButton(self.tabCamSound)
        self.radSouRecvOn1.setGeometry(QtCore.QRect(240, 180, 51, 17))
        self.radSouRecvOn1.setObjectName("radSouRecvOn1")
        self.label_14 = QtWidgets.QLabel(self.tabCamSound)
        self.label_14.setGeometry(QtCore.QRect(240, 140, 111, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy)
        self.label_14.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.label_14.setFont(font)
        self.label_14.setMouseTracking(True)
        self.label_14.setMidLineWidth(1)
        self.label_14.setObjectName("label_14")
        self.line_6 = QtWidgets.QFrame(self.tabCamSound)
        self.line_6.setGeometry(QtCore.QRect(240, 110, 111, 20))
        self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")

        self.rGroupCamSend1=QButtonGroup(self.tabCamSound)
        self.rGroupCamSend1.addButton(self.radCamSendOn1)
        self.rGroupCamSend1.addButton(self.radCamSendOff1)


        self.rGroupCamRecv1=QButtonGroup(self.tabCamSound)
        self.rGroupCamRecv1.addButton(self.radCamRecvOn1)
        self.rGroupCamRecv1.addButton(self.radCamRecvOff1)



        self.rGroupSouSend1=QButtonGroup(self.tabCamSound)
        self.rGroupSouSend1.addButton(self.radSouSendOn1)
        self.rGroupSouSend1.addButton(self.radSouSendOff1)



        self.rGroupSouRecv1=QButtonGroup(self.tabCamSound)
        self.rGroupSouRecv1.addButton(self.radSouRecvOn1)
        self.rGroupSouRecv1.addButton(self.radSouRecvOff1)

        self.tabWidget.addTab(self.tabCamSound, "")
        self.tabScreen = QtWidgets.QWidget()
        self.tabScreen.setObjectName("tabScreen")
        self.labelRecvScreen1 = QtWidgets.QLabel(self.tabScreen)
        self.labelRecvScreen1.setGeometry(QtCore.QRect(10, 40, 361, 201))
        self.labelRecvScreen1.setStyleSheet("background-color: rgb(0, 255, 255);")
        self.labelRecvScreen1.setText("")
        self.labelRecvScreen1.setObjectName("labelRecvScreen1")
        self.labelSendScreen = QtWidgets.QLabel(self.tabScreen)
        self.labelSendScreen.setGeometry(QtCore.QRect(450, 150, 141, 91))
        self.labelSendScreen.setStyleSheet("background-color: rgb(0, 255, 255);")
        self.labelSendScreen.setText("")
        self.labelSendScreen.setObjectName("labelSendScreen")
        self.label_17 = QtWidgets.QLabel(self.tabScreen)
        self.label_17.setGeometry(QtCore.QRect(10, 10, 91, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_17.sizePolicy().hasHeightForWidth())
        self.label_17.setSizePolicy(sizePolicy)
        self.label_17.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.label_17.setFont(font)
        self.label_17.setMouseTracking(True)
        self.label_17.setMidLineWidth(1)
        self.label_17.setObjectName("label_17")
        self.radScreenRecvOn1 = QtWidgets.QRadioButton(self.tabScreen)
        self.radScreenRecvOn1.setGeometry(QtCore.QRect(120, 20, 51, 17))
        self.radScreenRecvOn1.setObjectName("radScreenRecvOn1")
        self.radScreenRecvOff1 = QtWidgets.QRadioButton(self.tabScreen)
        self.radScreenRecvOff1.setGeometry(QtCore.QRect(190, 20, 51, 17))
        self.radScreenRecvOff1.setObjectName("radScreenRecvOff1")

        self.rGroupScreenRecv1=QButtonGroup(self.tabScreen)
        self.rGroupScreenRecv1.addButton(self.radScreenRecvOn1)
        self.rGroupScreenRecv1.addButton(self.radScreenRecvOff1)

        self.line_7 = QtWidgets.QFrame(self.tabScreen)
        self.line_7.setGeometry(QtCore.QRect(390, 20, 20, 221))
        self.line_7.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_7.setObjectName("line_7")
        self.radScreenSendOn1 = QtWidgets.QRadioButton(self.tabScreen)
        self.radScreenSendOn1.setGeometry(QtCore.QRect(450, 120, 51, 17))
        self.radScreenSendOn1.setObjectName("radScreenSendOn1")
        self.radScreenSendOff1 = QtWidgets.QRadioButton(self.tabScreen)
        self.radScreenSendOff1.setGeometry(QtCore.QRect(510, 120, 51, 17))
        self.radScreenSendOff1.setObjectName("radScreenSendOff1")

        self.rGroupScreenSend1=QButtonGroup(self.tabScreen)
        self.rGroupScreenSend1.addButton(self.radScreenSendOn1)
        self.rGroupScreenSend1.addButton(self.radScreenSendOff1)

        self.label_18 = QtWidgets.QLabel(self.tabScreen)
        self.label_18.setGeometry(QtCore.QRect(450, 80, 91, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_18.sizePolicy().hasHeightForWidth())
        self.label_18.setSizePolicy(sizePolicy)
        self.label_18.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.label_18.setFont(font)
        self.label_18.setMouseTracking(True)
        self.label_18.setMidLineWidth(1)
        self.label_18.setObjectName("label_18")
        self.tabWidget.addTab(self.tabScreen, "")
        self.tabKeyMouse = QtWidgets.QWidget()
        self.tabKeyMouse.setObjectName("tabKeyMouse")
        self.label_19 = QtWidgets.QLabel(self.tabKeyMouse)
        self.label_19.setGeometry(QtCore.QRect(20, 10, 111, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_19.sizePolicy().hasHeightForWidth())
        self.label_19.setSizePolicy(sizePolicy)
        self.label_19.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.label_19.setFont(font)
        self.label_19.setMouseTracking(True)
        self.label_19.setMidLineWidth(1)
        self.label_19.setObjectName("label_19")
        self.radKeySendOff1 = QtWidgets.QRadioButton(self.tabKeyMouse)
        self.radKeySendOff1.setGeometry(QtCore.QRect(80, 40, 51, 17))
        self.radKeySendOff1.setObjectName("radKeySendOff1")
        self.radKeySendOn1 = QtWidgets.QRadioButton(self.tabKeyMouse)
        self.radKeySendOn1.setGeometry(QtCore.QRect(20, 40, 51, 17))
        self.radKeySendOn1.setObjectName("radKeySendOn1")

        self.rGroupKeySend1=QButtonGroup(self.tabKeyMouse)
        self.rGroupKeySend1.addButton(self.radKeySendOn1)
        self.rGroupKeySend1.addButton(self.radKeySendOff1)

        self.labelSendKeyboard1 = QtWidgets.QLabel(self.tabKeyMouse)
        self.labelSendKeyboard1.setGeometry(QtCore.QRect(20, 60, 111, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelSendKeyboard1.sizePolicy().hasHeightForWidth())
        self.labelSendKeyboard1.setSizePolicy(sizePolicy)
        self.labelSendKeyboard1.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.labelSendKeyboard1.setFont(font)
        self.labelSendKeyboard1.setMouseTracking(True)
        self.labelSendKeyboard1.setMidLineWidth(1)
        self.labelSendKeyboard1.setObjectName("labelSendKeyboard1")
        self.label_20 = QtWidgets.QLabel(self.tabKeyMouse)
        self.label_20.setGeometry(QtCore.QRect(20, 120, 111, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_20.sizePolicy().hasHeightForWidth())
        self.label_20.setSizePolicy(sizePolicy)
        self.label_20.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.label_20.setFont(font)
        self.label_20.setMouseTracking(True)
        self.label_20.setMidLineWidth(1)
        self.label_20.setObjectName("label_20")
        self.labelRecvKeyboard1 = QtWidgets.QLabel(self.tabKeyMouse)
        self.labelRecvKeyboard1.setGeometry(QtCore.QRect(20, 170, 111, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelRecvKeyboard1.sizePolicy().hasHeightForWidth())
        self.labelRecvKeyboard1.setSizePolicy(sizePolicy)
        self.labelRecvKeyboard1.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.labelRecvKeyboard1.setFont(font)
        self.labelRecvKeyboard1.setMouseTracking(True)
        self.labelRecvKeyboard1.setMidLineWidth(1)
        self.labelRecvKeyboard1.setObjectName("labelRecvKeyboard1")
        self.radKeyRecvOn1 = QtWidgets.QRadioButton(self.tabKeyMouse)
        self.radKeyRecvOn1.setGeometry(QtCore.QRect(20, 150, 51, 17))
        self.radKeyRecvOn1.setObjectName("radKeyRecvOn1")
        self.radKeyRecvOff1 = QtWidgets.QRadioButton(self.tabKeyMouse)
        self.radKeyRecvOff1.setGeometry(QtCore.QRect(80, 150, 51, 17))
        self.radKeyRecvOff1.setObjectName("radKeyRecvOff1")

        self.rGroupKeyRecv1=QButtonGroup(self.tabKeyMouse)
        self.rGroupKeyRecv1.addButton(self.radKeyRecvOn1)
        self.rGroupKeyRecv1.addButton(self.radKeyRecvOff1)

        self.labelSendMouse1 = QtWidgets.QLabel(self.tabKeyMouse)
        self.labelSendMouse1.setGeometry(QtCore.QRect(390, 60, 111, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelSendMouse1.sizePolicy().hasHeightForWidth())
        self.labelSendMouse1.setSizePolicy(sizePolicy)
        self.labelSendMouse1.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.labelSendMouse1.setFont(font)
        self.labelSendMouse1.setMouseTracking(True)
        self.labelSendMouse1.setMidLineWidth(1)
        self.labelSendMouse1.setObjectName("labelSendMouse1")
        self.radMouseSendOn1 = QtWidgets.QRadioButton(self.tabKeyMouse)
        self.radMouseSendOn1.setGeometry(QtCore.QRect(390, 40, 51, 17))
        self.radMouseSendOn1.setObjectName("radMouseSendOn1")

        self.radMouseSendOff1 = QtWidgets.QRadioButton(self.tabKeyMouse)
        self.radMouseSendOff1.setGeometry(QtCore.QRect(450, 40, 51, 17))
        self.radMouseSendOff1.setObjectName("radMouseSendOff1")

        self.rGroupMouseSend1=QButtonGroup(self.tabKeyMouse)
        self.rGroupMouseSend1.addButton(self.radMouseSendOn1)
        self.rGroupMouseSend1.addButton(self.radMouseSendOff1)


        self.label_24 = QtWidgets.QLabel(self.tabKeyMouse)
        self.label_24.setGeometry(QtCore.QRect(390, 10, 111, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_24.sizePolicy().hasHeightForWidth())
        self.label_24.setSizePolicy(sizePolicy)
        self.label_24.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.label_24.setFont(font)
        self.label_24.setMouseTracking(True)
        self.label_24.setMidLineWidth(1)
        self.label_24.setObjectName("label_24")
        self.labelRecvMouse1 = QtWidgets.QLabel(self.tabKeyMouse)
        self.labelRecvMouse1.setGeometry(QtCore.QRect(390, 170, 111, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelRecvMouse1.sizePolicy().hasHeightForWidth())
        self.labelRecvMouse1.setSizePolicy(sizePolicy)
        self.labelRecvMouse1.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.labelRecvMouse1.setFont(font)
        self.labelRecvMouse1.setMouseTracking(True)
        self.labelRecvMouse1.setMidLineWidth(1)
        self.labelRecvMouse1.setObjectName("labelRecvMouse1")
        self.radMouseRecvOn1 = QtWidgets.QRadioButton(self.tabKeyMouse)
        self.radMouseRecvOn1.setGeometry(QtCore.QRect(390, 150, 51, 17))
        self.radMouseRecvOn1.setObjectName("radMouseRecvOn1")

        self.radMouseRecvOff1 = QtWidgets.QRadioButton(self.tabKeyMouse)
        self.radMouseRecvOff1.setGeometry(QtCore.QRect(450, 150, 51, 17))
        self.radMouseRecvOff1.setObjectName("radMouseRecvOff1")

        self.rGroupMouseRecv1=QButtonGroup(self.tabKeyMouse)
        self.rGroupMouseRecv1.addButton(self.radMouseRecvOn1)
        self.rGroupMouseRecv1.addButton(self.radMouseRecvOff1)

        self.label_26 = QtWidgets.QLabel(self.tabKeyMouse)
        self.label_26.setGeometry(QtCore.QRect(390, 120, 111, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_26.sizePolicy().hasHeightForWidth())
        self.label_26.setSizePolicy(sizePolicy)
        self.label_26.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.label_26.setFont(font)
        self.label_26.setMouseTracking(True)
        self.label_26.setMidLineWidth(1)
        self.label_26.setObjectName("label_26")
        self.label_27 = QtWidgets.QLabel(self.tabKeyMouse)
        self.label_27.setGeometry(QtCore.QRect(190, 50, 61, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_27.sizePolicy().hasHeightForWidth())
        self.label_27.setSizePolicy(sizePolicy)
        self.label_27.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.label_27.setFont(font)
        self.label_27.setMouseTracking(True)
        self.label_27.setStyleSheet("background-color: rgb(255, 0, 0);")
        self.label_27.setMidLineWidth(1)
        self.label_27.setObjectName("label_27")
        self.label_28 = QtWidgets.QLabel(self.tabKeyMouse)
        self.label_28.setGeometry(QtCore.QRect(190, 90, 161, 121))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.label_28.setFont(font)
        self.label_28.setStyleSheet("background-color: rgb(0, 255, 127);")
        self.label_28.setLineWidth(-1)
        self.label_28.setMidLineWidth(-3)
        self.label_28.setWordWrap(True)
        self.label_28.setObjectName("label_28")
        self.tabWidget.addTab(self.tabKeyMouse, "")
        self.tabKeyMouScreen = QtWidgets.QWidget()
        self.tabKeyMouScreen.setObjectName("tabKeyMouScreen")
        self.radScreenRecvOff2 = QtWidgets.QRadioButton(self.tabKeyMouScreen)
        self.radScreenRecvOff2.setGeometry(QtCore.QRect(170, 10, 51, 17))
        self.radScreenRecvOff2.setObjectName("radScreenRecvOff2")
        self.labelRecvScreen2 = QtWidgets.QLabel(self.tabKeyMouScreen)
        self.labelRecvScreen2.setGeometry(QtCore.QRect(10, 30, 401, 211))
        self.labelRecvScreen2.setStyleSheet("background-color: rgb(0, 255, 255);")
        self.labelRecvScreen2.setText("")
        self.labelRecvScreen2.setObjectName("labelRecvScreen2")
        self.radScreenRecvOn2 = QtWidgets.QRadioButton(self.tabKeyMouScreen)
        self.radScreenRecvOn2.setGeometry(QtCore.QRect(110, 10, 51, 17))
        self.radScreenRecvOn2.setObjectName("radScreenRecvOn2")
        self.label_30 = QtWidgets.QLabel(self.tabKeyMouScreen)
        self.label_30.setGeometry(QtCore.QRect(10, 0, 91, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_30.sizePolicy().hasHeightForWidth())
        self.label_30.setSizePolicy(sizePolicy)
        self.label_30.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.label_30.setFont(font)
        self.label_30.setMouseTracking(True)
        self.label_30.setMidLineWidth(1)
        self.label_30.setObjectName("label_30")
        self.label_32 = QtWidgets.QLabel(self.tabKeyMouScreen)
        self.label_32.setGeometry(QtCore.QRect(470, 30, 111, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_32.sizePolicy().hasHeightForWidth())
        self.label_32.setSizePolicy(sizePolicy)
        self.label_32.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.label_32.setFont(font)
        self.label_32.setMouseTracking(True)
        self.label_32.setMidLineWidth(1)
        self.label_32.setObjectName("label_32")
        self.labelSendMouse2 = QtWidgets.QLabel(self.tabKeyMouScreen)
        self.labelSendMouse2.setGeometry(QtCore.QRect(470, 80, 111, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelSendMouse2.sizePolicy().hasHeightForWidth())
        self.labelSendMouse2.setSizePolicy(sizePolicy)
        self.labelSendMouse2.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.labelSendMouse2.setFont(font)
        self.labelSendMouse2.setMouseTracking(True)
        self.labelSendMouse2.setMidLineWidth(1)
        self.labelSendMouse2.setObjectName("labelSendMouse2")
        self.radMouseSendOff2 = QtWidgets.QRadioButton(self.tabKeyMouScreen)
        self.radMouseSendOff2.setGeometry(QtCore.QRect(530, 60, 51, 17))
        self.radMouseSendOff2.setObjectName("radMouseSendOff2")
        self.radMouseSendOn2 = QtWidgets.QRadioButton(self.tabKeyMouScreen)
        self.radMouseSendOn2.setGeometry(QtCore.QRect(470, 60, 51, 17))
        self.radMouseSendOn2.setObjectName("radMouseSendOn2")

        self.rGroupMouseSend2=QButtonGroup(self.tabKeyMouScreen)
        self.rGroupMouseSend2.addButton(self.radMouseSendOn2)
        self.rGroupMouseSend2.addButton(self.radMouseSendOff2)


        self.label_31 = QtWidgets.QLabel(self.tabKeyMouScreen)
        self.label_31.setGeometry(QtCore.QRect(470, 150, 111, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_31.sizePolicy().hasHeightForWidth())
        self.label_31.setSizePolicy(sizePolicy)
        self.label_31.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.label_31.setFont(font)
        self.label_31.setMouseTracking(True)
        self.label_31.setMidLineWidth(1)
        self.label_31.setObjectName("label_31")
        self.radKeySendOn2 = QtWidgets.QRadioButton(self.tabKeyMouScreen)
        self.radKeySendOn2.setGeometry(QtCore.QRect(470, 180, 51, 17))
        self.radKeySendOn2.setObjectName("radKeySendOn2")
        self.radKeySendOff2 = QtWidgets.QRadioButton(self.tabKeyMouScreen)
        self.radKeySendOff2.setGeometry(QtCore.QRect(530, 180, 51, 17))
        self.radKeySendOff2.setObjectName("radKeySendOff2")

        self.rGroupKeySend2=QButtonGroup(self.tabKeyMouScreen)
        self.rGroupKeySend2.addButton(self.radKeySendOn2)
        self.rGroupKeySend2.addButton(self.radKeySendOff2)

        self.labelSendKeyboard2 = QtWidgets.QLabel(self.tabKeyMouScreen)
        self.labelSendKeyboard2.setGeometry(QtCore.QRect(470, 200, 111, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelSendKeyboard2.sizePolicy().hasHeightForWidth())
        self.labelSendKeyboard2.setSizePolicy(sizePolicy)
        self.labelSendKeyboard2.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.labelSendKeyboard2.setFont(font)
        self.labelSendKeyboard2.setMouseTracking(True)
        self.labelSendKeyboard2.setMidLineWidth(1)
        self.labelSendKeyboard2.setObjectName("labelSendKeyboard2")
        self.line_8 = QtWidgets.QFrame(self.tabKeyMouScreen)
        self.line_8.setGeometry(QtCore.QRect(470, 120, 118, 3))
        self.line_8.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_8.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_8.setObjectName("line_8")
        self.line_9 = QtWidgets.QFrame(self.tabKeyMouScreen)
        self.line_9.setGeometry(QtCore.QRect(430, 40, 16, 191))
        self.line_9.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_9.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_9.setObjectName("line_9")
        self.tabWidget.addTab(self.tabKeyMouScreen, "")
        self.tabControlPanel = QtWidgets.QWidget()
        self.tabControlPanel.setObjectName("tabControlPanel")
        self.label_35 = QtWidgets.QLabel(self.tabControlPanel)
        self.label_35.setGeometry(QtCore.QRect(160, 10, 111, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_35.sizePolicy().hasHeightForWidth())
        self.label_35.setSizePolicy(sizePolicy)
        self.label_35.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.label_35.setFont(font)
        self.label_35.setMouseTracking(True)
        self.label_35.setMidLineWidth(1)
        self.label_35.setObjectName("label_35")
        self.label_36 = QtWidgets.QLabel(self.tabControlPanel)
        self.label_36.setGeometry(QtCore.QRect(430, 10, 111, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_36.sizePolicy().hasHeightForWidth())
        self.label_36.setSizePolicy(sizePolicy)
        self.label_36.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.label_36.setFont(font)
        self.label_36.setMouseTracking(True)
        self.label_36.setMidLineWidth(1)
        self.label_36.setObjectName("label_36")
        self.label_37 = QtWidgets.QLabel(self.tabControlPanel)
        self.label_37.setGeometry(QtCore.QRect(30, 40, 81, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_37.sizePolicy().hasHeightForWidth())
        self.label_37.setSizePolicy(sizePolicy)
        self.label_37.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.label_37.setFont(font)
        self.label_37.setMouseTracking(True)
        self.label_37.setMidLineWidth(1)
        self.label_37.setObjectName("label_37")
        self.label_38 = QtWidgets.QLabel(self.tabControlPanel)
        self.label_38.setGeometry(QtCore.QRect(30, 80, 81, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_38.sizePolicy().hasHeightForWidth())
        self.label_38.setSizePolicy(sizePolicy)
        self.label_38.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.label_38.setFont(font)
        self.label_38.setMouseTracking(True)
        self.label_38.setMidLineWidth(1)
        self.label_38.setObjectName("label_38")
        self.radCamSendOn2 = QtWidgets.QRadioButton(self.tabControlPanel)
        self.radCamSendOn2.setGeometry(QtCore.QRect(160, 50, 51, 17))
        self.radCamSendOn2.setObjectName("radCamSendOn2")
        self.radCamSendOff2 = QtWidgets.QRadioButton(self.tabControlPanel)
        self.radCamSendOff2.setGeometry(QtCore.QRect(220, 50, 51, 17))
        self.radCamSendOff2.setObjectName("radCamSendOff2")

        self.rGroupCamSend2=QButtonGroup(self.tabControlPanel)
        self.rGroupCamSend2.addButton(self.radCamSendOn2)
        self.rGroupCamSend2.addButton(self.radCamSendOff2)

        self.radCamRecvOn2 = QtWidgets.QRadioButton(self.tabControlPanel)
        self.radCamRecvOn2.setGeometry(QtCore.QRect(430, 50, 51, 17))
        self.radCamRecvOn2.setObjectName("radCamRecvOn2")
        self.radCamRecvOff2 = QtWidgets.QRadioButton(self.tabControlPanel)
        self.radCamRecvOff2.setGeometry(QtCore.QRect(490, 50, 51, 17))
        self.radCamRecvOff2.setObjectName("radCamRecvOff2")

        self.rGroupCamRecv2=QButtonGroup(self.tabControlPanel)
        self.rGroupCamRecv2.addButton(self.radCamRecvOn2)
        self.rGroupCamRecv2.addButton(self.radCamRecvOff2)

        self.radSouSendOn2 = QtWidgets.QRadioButton(self.tabControlPanel)
        self.radSouSendOn2.setGeometry(QtCore.QRect(160, 90, 51, 17))
        self.radSouSendOn2.setObjectName("radSouSendOn2")
        self.radSouSendOff2 = QtWidgets.QRadioButton(self.tabControlPanel)
        self.radSouSendOff2.setGeometry(QtCore.QRect(220, 90, 51, 17))
        self.radSouSendOff2.setObjectName("radSouSendOff2")

        self.rGroupSouSend2=QButtonGroup(self.tabControlPanel)
        self.rGroupSouSend2.addButton(self.radSouSendOn2)
        self.rGroupSouSend2.addButton(self.radSouSendOff2)

        self.radSouRecvOn2 = QtWidgets.QRadioButton(self.tabControlPanel)
        self.radSouRecvOn2.setGeometry(QtCore.QRect(430, 90, 51, 17))
        self.radSouRecvOn2.setObjectName("radSouRecvOn2")
        self.radSouRecvOff2 = QtWidgets.QRadioButton(self.tabControlPanel)
        self.radSouRecvOff2.setGeometry(QtCore.QRect(490, 90, 51, 17))
        self.radSouRecvOff2.setObjectName("radSouRecvOff2")

        self.rGroupSouRecv2=QButtonGroup(self.tabControlPanel)
        self.rGroupSouRecv2.addButton(self.radSouRecvOn2)
        self.rGroupSouRecv2.addButton(self.radSouRecvOff2)

        self.radKeySendOn3 = QtWidgets.QRadioButton(self.tabControlPanel)
        self.radKeySendOn3.setGeometry(QtCore.QRect(160, 130, 51, 17))
        self.radKeySendOn3.setObjectName("radKeySendOn3")
        self.radKeySendOff3 = QtWidgets.QRadioButton(self.tabControlPanel)
        self.radKeySendOff3.setGeometry(QtCore.QRect(220, 130, 51, 17))
        self.radKeySendOff3.setObjectName("radKeySendOff3")

        self.rGroupKeySend3=QButtonGroup(self.tabControlPanel)
        self.rGroupKeySend3.addButton(self.radKeySendOn3)
        self.rGroupKeySend3.addButton(self.radKeySendOff3)

        self.radKeyRecvOn2 = QtWidgets.QRadioButton(self.tabControlPanel)
        self.radKeyRecvOn2.setGeometry(QtCore.QRect(430, 130, 51, 17))
        self.radKeyRecvOn2.setObjectName("radKeyRecvOn2")
        self.radKeyRecvOff2 = QtWidgets.QRadioButton(self.tabControlPanel)
        self.radKeyRecvOff2.setGeometry(QtCore.QRect(490, 130, 51, 17))
        self.radKeyRecvOff2.setObjectName("radKeyRecvOff2")

        self.rGroupKeyRecv2=QButtonGroup(self.tabControlPanel)
        self.rGroupKeyRecv2.addButton(self.radKeyRecvOn2)
        self.rGroupKeyRecv2.addButton(self.radKeyRecvOff2)

        self.radMouseSendOn3 = QtWidgets.QRadioButton(self.tabControlPanel)
        self.radMouseSendOn3.setGeometry(QtCore.QRect(160, 170, 51, 17))
        self.radMouseSendOn3.setObjectName("radMouseSendOn3")
        self.radMouseSendOff3 = QtWidgets.QRadioButton(self.tabControlPanel)
        self.radMouseSendOff3.setGeometry(QtCore.QRect(220, 170, 51, 17))
        self.radMouseSendOff3.setObjectName("radMouseSendOff3")

        self.rGroupMouseSend3=QButtonGroup(self.tabControlPanel)
        self.rGroupMouseSend3.addButton(self.radMouseSendOn3)
        self.rGroupMouseSend3.addButton(self.radMouseSendOff3)

        self.radMouseRecvOn2 = QtWidgets.QRadioButton(self.tabControlPanel)
        self.radMouseRecvOn2.setGeometry(QtCore.QRect(430, 170, 51, 17))
        self.radMouseRecvOn2.setObjectName("radMouseRecvOn2")
        self.radMouseRecvOff2 = QtWidgets.QRadioButton(self.tabControlPanel)
        self.radMouseRecvOff2.setGeometry(QtCore.QRect(490, 170, 51, 17))
        self.radMouseRecvOff2.setObjectName("radMouseRecvOff2")

        self.rGroupMouseRecv2=QButtonGroup(self.tabControlPanel)
        self.rGroupMouseRecv2.addButton(self.radMouseRecvOn2)
        self.rGroupMouseRecv2.addButton(self.radMouseRecvOff2)

        self.radScreenSendOn2 = QtWidgets.QRadioButton(self.tabControlPanel)
        self.radScreenSendOn2.setGeometry(QtCore.QRect(160, 210, 51, 17))
        self.radScreenSendOn2.setObjectName("radScreenSendOn2")
        self.radScreenSendOff2 = QtWidgets.QRadioButton(self.tabControlPanel)
        self.radScreenSendOff2.setGeometry(QtCore.QRect(220, 210, 51, 17))
        self.radScreenSendOff2.setObjectName("radScreenSendOff2")

        self.rGroupScreenSend2=QButtonGroup(self.tabControlPanel)
        self.rGroupScreenSend2.addButton(self.radScreenSendOn2)
        self.rGroupScreenSend2.addButton(self.radScreenSendOff2)

        self.radScreenRecvOn3 = QtWidgets.QRadioButton(self.tabControlPanel)
        self.radScreenRecvOn3.setGeometry(QtCore.QRect(430, 210, 51, 17))
        self.radScreenRecvOn3.setObjectName("radScreenRecvOn3")
        self.radScreenRecvOff3 = QtWidgets.QRadioButton(self.tabControlPanel)
        self.radScreenRecvOff3.setGeometry(QtCore.QRect(490, 210, 51, 17))
        self.radScreenRecvOff3.setObjectName("radScreenRecvOff3")

        self.rGroupScreenRecv3=QButtonGroup(self.tabControlPanel)
        self.rGroupScreenRecv3.addButton(self.radScreenRecvOn3)
        self.rGroupScreenRecv3.addButton(self.radScreenRecvOff3)

        self.label_39 = QtWidgets.QLabel(self.tabControlPanel)
        self.label_39.setGeometry(QtCore.QRect(30, 160, 81, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_39.sizePolicy().hasHeightForWidth())
        self.label_39.setSizePolicy(sizePolicy)
        self.label_39.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.label_39.setFont(font)
        self.label_39.setMouseTracking(True)
        self.label_39.setMidLineWidth(1)
        self.label_39.setObjectName("label_39")
        self.label_40 = QtWidgets.QLabel(self.tabControlPanel)
        self.label_40.setGeometry(QtCore.QRect(30, 200, 81, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_40.sizePolicy().hasHeightForWidth())
        self.label_40.setSizePolicy(sizePolicy)
        self.label_40.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.label_40.setFont(font)
        self.label_40.setMouseTracking(True)
        self.label_40.setMidLineWidth(1)
        self.label_40.setObjectName("label_40")
        self.label_41 = QtWidgets.QLabel(self.tabControlPanel)
        self.label_41.setGeometry(QtCore.QRect(30, 120, 81, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_41.sizePolicy().hasHeightForWidth())
        self.label_41.setSizePolicy(sizePolicy)
        self.label_41.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.label_41.setFont(font)
        self.label_41.setMouseTracking(True)
        self.label_41.setMidLineWidth(1)
        self.label_41.setObjectName("label_41")
        self.line_10 = QtWidgets.QFrame(self.tabControlPanel)
        self.line_10.setGeometry(QtCore.QRect(340, 10, 20, 211))
        self.line_10.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_10.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_10.setObjectName("line_10")
        self.tabWidget.addTab(self.tabControlPanel, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def reSetup(self):
        self.line_10.close()

        self.btnRCamera=QPushButton(self.tabControlPanel)
        self.btnRCamera.setText("Request")
        self.btnRCamera.setGeometry(310,50,75,23)
        self.btnRCamera.clicked.connect(self.funRequestCam)
        self.btnRCamera.show()


        self.btnRSound=QPushButton(self.tabControlPanel)
        self.btnRSound.setText("Request")
        self.btnRSound.setGeometry(310,90,75,23)
        self.btnRSound.clicked.connect(self.funRequestSound)

        self.btnRKeyboard=QPushButton(self.tabControlPanel)
        self.btnRKeyboard.setText("Request")
        self.btnRKeyboard.setGeometry(310,130,75,23)
        self.btnRKeyboard.clicked.connect(self.funRequestKeyboard)

        self.btnRMouse=QPushButton(self.tabControlPanel)
        self.btnRMouse.setText("Request")
        self.btnRMouse.setGeometry(310,170,75,23)
        self.btnRMouse.clicked.connect(self.funRequestMouse)

        self.btnRScreen=QPushButton(self.tabControlPanel)
        self.btnRScreen.setText("Request")
        self.btnRScreen.setGeometry(310,210,75,23)
        self.btnRScreen.clicked.connect(self.funRequestScreen)

    def retranslateUi(self, MainWindow):
        self.qTimer2=QTimer()
        self.qTimer2.setInterval(5)
        self.qTimer2.timeout.connect(lambda :qTimerRefressFun(self.timerFunList))
        self.qTimer2.start()

        self.reSetup()
        self.finalSetup()
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_2.setText(_translate("MainWindow", "UserName"))
        self.label_3.setText(_translate("MainWindow", "Name"))
        self.labelUserName.setText(_translate("MainWindow", "My user Name"))
        self.labelFullName.setText(_translate("MainWindow", "Full Name"))
        self.label_7.setText(_translate("MainWindow", "Status"))
        self.editMessage.setPlaceholderText(_translate("MainWindow", "Enter Message"))
        self.btnSendText.setText(_translate("MainWindow", "Send Text"))
        self.btnSetFile.setText(_translate("MainWindow", "Set File"))
        self.btnSendFile.setText(_translate("MainWindow", "Send File"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabTextFile), _translate("MainWindow", "Text / File"))
        self.label_8.setText(_translate("MainWindow", "Send Camera"))
        self.label_9.setText(_translate("MainWindow", "Recv Camera"))
        self.radCamSendOn1.setText(_translate("MainWindow", "On"))
        self.radCamSendOff1.setText(_translate("MainWindow", "Off"))
        self.radCamRecvOn1.setText(_translate("MainWindow", "On"))
        self.radCamRecvOff1.setText(_translate("MainWindow", "Off"))
        self.label_12.setText(_translate("MainWindow", "Sound Settings"))
        self.label_13.setText(_translate("MainWindow", "Send Sound"))
        self.radSouSendOff1.setText(_translate("MainWindow", "Off"))
        self.radSouSendOn1.setText(_translate("MainWindow", "On"))
        self.radSouRecvOff1.setText(_translate("MainWindow", "Off"))
        self.radSouRecvOn1.setText(_translate("MainWindow", "On"))
        self.label_14.setText(_translate("MainWindow", "Recv Sound"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabCamSound), _translate("MainWindow", "Camera / Sound"))
        self.label_17.setText(_translate("MainWindow", "Recv Screen"))
        self.radScreenRecvOn1.setText(_translate("MainWindow", "On"))
        self.radScreenRecvOff1.setText(_translate("MainWindow", "Off"))
        self.radScreenSendOn1.setText(_translate("MainWindow", "On"))
        self.radScreenSendOff1.setText(_translate("MainWindow", "Off"))
        self.label_18.setText(_translate("MainWindow", "Send Screen"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabScreen), _translate("MainWindow", "Screen"))
        self.label_19.setText(_translate("MainWindow", "Send Keyboard"))
        self.radKeySendOff1.setText(_translate("MainWindow", "Off"))
        self.radKeySendOn1.setText(_translate("MainWindow", "On"))
        self.labelSendKeyboard1.setText(_translate("MainWindow", "Data Recieving"))
        self.label_20.setText(_translate("MainWindow", "Recv Keyboard"))
        self.labelRecvKeyboard1.setText(_translate("MainWindow", "Data Recieving"))
        self.radKeyRecvOn1.setText(_translate("MainWindow", "On"))
        self.radKeyRecvOff1.setText(_translate("MainWindow", "Off"))
        self.labelSendMouse1.setText(_translate("MainWindow", "Data Recieving"))
        self.radMouseSendOn1.setText(_translate("MainWindow", "On"))
        self.radMouseSendOff1.setText(_translate("MainWindow", "Off"))
        self.label_24.setText(_translate("MainWindow", "Send Mouse"))
        self.labelRecvMouse1.setText(_translate("MainWindow", "Data Recieving"))
        self.radMouseRecvOn1.setText(_translate("MainWindow", "On"))
        self.radMouseRecvOff1.setText(_translate("MainWindow", "Off"))
        self.label_26.setText(_translate("MainWindow", "Recv Mouse"))
        self.label_27.setText(_translate("MainWindow", "Note :-"))
        self.label_28.setText(_translate("MainWindow", "Press \"Ctrl+t\" to off sending mouse and keyboard data and Press \"Alt+t\" to off recieving mouse and keyboard data"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabKeyMouse), _translate("MainWindow", "Keyboard / Mouse"))
        self.radScreenRecvOff2.setText(_translate("MainWindow", "Off"))
        self.radScreenRecvOn2.setText(_translate("MainWindow", "On"))
        self.label_30.setText(_translate("MainWindow", "Recv Screen"))
        self.label_32.setText(_translate("MainWindow", "Send Mouse"))
        self.labelSendMouse2.setText(_translate("MainWindow", "Data Recieving"))
        self.radMouseSendOff2.setText(_translate("MainWindow", "Off"))
        self.radMouseSendOn2.setText(_translate("MainWindow", "On"))
        self.label_31.setText(_translate("MainWindow", "Send Keyboard"))
        self.radKeySendOn2.setText(_translate("MainWindow", "On"))
        self.radKeySendOff2.setText(_translate("MainWindow", "Off"))
        self.labelSendKeyboard2.setText(_translate("MainWindow", "Data Recieving"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabKeyMouScreen), _translate("MainWindow", "Keyboard / Mouse / Screen"))
        self.label_35.setText(_translate("MainWindow", "Sending Control"))
        self.label_36.setText(_translate("MainWindow", "Reciving Control"))
        self.label_37.setText(_translate("MainWindow", "Camera"))
        self.label_38.setText(_translate("MainWindow", "Sound"))
        self.radCamSendOn2.setText(_translate("MainWindow", "On"))
        self.radCamSendOff2.setText(_translate("MainWindow", "Off"))
        self.radCamRecvOn2.setText(_translate("MainWindow", "On"))
        self.radCamRecvOff2.setText(_translate("MainWindow", "Off"))
        self.radSouSendOn2.setText(_translate("MainWindow", "On"))
        self.radSouSendOff2.setText(_translate("MainWindow", "Off"))
        self.radSouRecvOn2.setText(_translate("MainWindow", "On"))
        self.radSouRecvOff2.setText(_translate("MainWindow", "Off"))
        self.radKeySendOn3.setText(_translate("MainWindow", "On"))
        self.radKeySendOff3.setText(_translate("MainWindow", "Off"))
        self.radKeyRecvOn2.setText(_translate("MainWindow", "On"))
        self.radKeyRecvOff2.setText(_translate("MainWindow", "Off"))
        self.radMouseSendOn3.setText(_translate("MainWindow", "On"))
        self.radMouseSendOff3.setText(_translate("MainWindow", "Off"))
        self.radMouseRecvOn2.setText(_translate("MainWindow", "On"))
        self.radMouseRecvOff2.setText(_translate("MainWindow", "Off"))
        self.radScreenSendOn2.setText(_translate("MainWindow", "On"))
        self.radScreenSendOff2.setText(_translate("MainWindow", "Off"))
        self.radScreenRecvOn3.setText(_translate("MainWindow", "On"))
        self.radScreenRecvOff3.setText(_translate("MainWindow", "Off"))
        self.label_39.setText(_translate("MainWindow", "Mouse"))
        self.label_40.setText(_translate("MainWindow", "Screen"))
        self.label_41.setText(_translate("MainWindow", "Keyboard"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabControlPanel), _translate("MainWindow", "Control Panel"))

    def initFunctionControl(self):

        self.radSouSendOff1.setChecked(True)
        self.radSouRecvOff1.setChecked(True)
        self.XFunSendSound(self.radSouSendOff1)
        self.XFunRecvSound(self.radSouRecvOff1)

        self.radKeySendOff1.setChecked(True)
        self.radKeyRecvOff1.setChecked(True)
        self.XFunSendKeyboard(self.radKeySendOff1)
        self.XFunRecvKeyboard(self.radKeyRecvOff1)

        self.radMouseSendOff1.setChecked(True)
        self.radMouseRecvOff1.setChecked(True)
        self.XFunSendMouse(self.radMouseSendOff1)
        self.XFunRecvMouse(self.radMouseRecvOff1)
        print("OK")
        self.radScreenSendOff1.setChecked(True)
        self.radScreenRecvOff1.setChecked(True)
        self.XFunSendScreen(self.radScreenSendOff1)
        self.XFunRecvScreen(self.radScreenRecvOff1)

        self.radCamSendOff1.setChecked(True)
        self.radCamRecvOff1.setChecked(True)
        self.XFunSendCamera(self.radCamSendOff1)
        self.XFunRecvCamera(self.radCamRecvOff1)

    def onSendCamera(self):
        self.radCamSendOn1.setChecked(True)
        self.XFunSendCamera(self.radCamSendOn1)

    def onSendSound(self):
        self.radSouSendOn1.setChecked(True)
        self.XFunSendSound(self.radSouSendOn1)

    def onSendScreen(self):
        self.radScreenSendOn1.setChecked(True)
        self.XFunSendScreen(self.radScreenSendOn1)

    def onSendKeyboard(self):
        self.radKeySendOn1.setChecked(True)
        self.XFunSendKeyboard(self.radKeySendOn1)

    def onSendMouse(self):
        self.radMouseSendOn1.setChecked(True)
        self.XFunSendMouse(self.radMouseSendOn1)

    def onRecvCamera(self):
        self.radCamRecvOn1.setChecked(True)
        self.XFunRecvCamera(self.radCamRecvOn1)

    def onRecvSound(self):
        self.radSouRecvOn1.setChecked(True)
        self.XFunRecvSound(self.radSouRecvOn1)

    def onRecvScreen(self):
        self.radScreenRecvOn1.setChecked(True)
        self.XFunRecvScreen(self.radScreenRecvOn1)

    def onRecvKeyboard(self):
        self.radKeyRecvOn1.setChecked(True)
        self.XFunRecvKeyboard(self.radKeyRecvOn1)

    def onRecvMouse(self):
        self.radMouseRecvOn1.setChecked(True)
        self.XFunRecvMouse(self.radMouseRecvOn1)

    def init(self,c,userName,data):
        self.userName=userName
        self.c=c
        self.count=0

        self.initiate()
        self.funSetControls()
        self.timerFunList=[]

        self.initFileStructure()

        self.data=data

        self.labelUserName.setText(userName)
        self.timerFunList=[]

        self.assImpData()

        self.atLastInitiate()

        self.refress()

        #self.initFunctionControl()

        self.mainWindow.setWindowTitle(self.userName+':- Chat Window')
        self.mainWindow.closeEvent=self.onClose
        #self.onSendCamera()

    def initFileStructure(self):
        self.selectedFile=''

        self.FWidList={}

        self.sWin='cw@'+self.userName
        fc.getSetWindow(self.sWin)

        self.btnSetFile.clicked.connect(self.funSetFile)
        self.btnSendFile.clicked.connect(self.funSendFile)
        self.c.functionList[self.userName+'-CancelDownloadFileChat']=self.handleCancelDownloadFile
        self.fileFlowing=[]


        data=fc.removeDublFromArray(fc.getAllFilesOfSend(self.sWin))
        #print("%^%^%^",data)
        if data is not None:
            self.fileFlowing=data
            for i in data:
                self.formatSendChatFile(i)

        data2=fc.removeDublFromArray(fc.getAllFilesOfRecv(self.sWin))

        if data2 is not None:
            self.fileFlowing=self.fileFlowing+data2

    def callFileRefress(self):

        for i in self.fileFlowing:
            st=fc.getFileSttr(i)

            if st is not None:
                if st=='s':
                    self.refSendFile(i)
                else:
                    self.refRecvFile(i)

    def refSendFile(self,fileName):

        flow=fc.getSendFileFlow(fileName)
        tsize=fc.getSendFileTempSize(fileName)
        size=fc.getSendFileSize(fileName)
        #print(f'{fileName} ->{tsize}/{size}')
        #print(fileName in self.FWidList)
        if fileName in self.FWidList:
            self.refGuiSendFile(fileName,flow,tsize,size)

    def refGuiSendFile(self,fileName,flow,tsize,size):
        if flow !=None:

            frame=self.FWidList[fileName]
            children=frame.children()

            mtS=opFile.getByteToMb(int(tsize))
            mSS=opFile.getByteToMb(int(size))

            mtS=round(mtS,2)
            mSS=round(mSS,2)

            per=0
            if mSS==0:
                per=0
            else:
                per=opFile.calculateFilePercentage(mtS,mSS)

            children[3].setValue(per)
            if mSS !=mtS:
                txt=f'{mtS}/{mSS} mb'
            else:
                children[3].setDisabled(True)
                txt=f'Size ->{mtS} mb'
            #print(txt)
            children[5].setText(txt)

    def refRecvFile(self,fileName):
        flow=fc.getRecvFileStatus(fileName)
        tsize=fc.getRecvFileTempSize(fileName)
        size=fc.getRecvFileSize(fileName)
        #print(f'{fileName} ->{tsize}/{size}')
        #print(fileName in self.FWidList)
        if fileName in self.FWidList:
            self.refGuiRecvFile(fileName,flow,tsize,size)

    def refGuiRecvFile(self,fileName,flow,tsize,size):
        if flow !=None:

            frame=self.FWidList[fileName]
            children=frame.children()

            mtS=opFile.getByteToMb(int(tsize))
            mSS=opFile.getByteToMb(int(size))

            mtS=round(mtS,2)
            mSS=round(mSS,2)

            per=0
            if mSS==0:
                per=0
            else:
                per=opFile.calculateFilePercentage(mtS,mSS)

            children[3].setValue(per)
            if mSS !=mtS:
                txt=f'{mtS}/{mSS} mb'
            else:
                children[3].setDisabled(True)
                txt=f'Size ->{mtS} mb'
            #print(txt)
            children[6].setText(txt)


    def funSetFile(self):
        file,inf=QFileDialog.getOpenFileName()
        self.selectedFile=file

        if file != '':
            showResult(self.statusbar,"File ->'"+file+"'<- is Selected",False)

    def funSendFile(self):
        def fun():
            if self.selectedFile != '':
                file=self.selectedFile

                f=opFile.attachFileWithtime(opFile.getActualFileName(self.selectedFile))


                self.selectedFile=''

                namesToTo=self.c.userName+'-'+self.userName

                def onStart():

                    fc.onSendStart(self.sWin,f)

                def onEnd(fName):
                    size=self.c.send.fileSize[fName]
                    fc.onSendEnd(self.sWin,fName)

                    def fun(size):
                        if fName in self.FWidList:
                            frame=self.FWidList[fName]
                            children=frame.children()
                            children[3].setDisabled(True)
                            children[2].setValue(100)
                            size=opFile.getByteToMb(size)
                            size=round(size,2)
                            children[4].setText(f'Size ->{size} mb')

                    self.timerFunList.append(lambda: fun(size))

                self.c.send.send_file3(file,fileTempName=f,onStart=onStart,
                                       toWhom=namesToTo,toType='chat')
                #fc.setSendFile(self.sWin,f)
                self.fileFlowing.append(f)
                self.formatSendChatFile(f)


        self.timerFunList.append(fun)

    def formatSendChatFile(self,f):
        dCount=self.count

        frame=QFrame(self.scrollContainer)
        frame.setFixedSize(250,131)

        styleBackground="""
        background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:0.983, y2:0, stop:0 rgba(0, 124, 0, 255), stop:1 rgba(255, 255, 255, 255));
        """

        styleUserName='''
        background-color: rgb(81, 255, 0);
        border: 1px solid #1C6EA4;

        '''

        styleFileName='''
        border: 1px solid #1C6EA4;
        border-color: rgb(255, 0, 0);
        background-color: rgb(0, 124,0);
        color:rgb(255,255,255);
        '''

        styleSize='''
        background-color: rgb(170, 255, 127);
        '''

        labelBackground=QLabel(frame)
        labelBackground.setGeometry(40,0,211,131)
        labelBackground.setStyleSheet(styleBackground)

        sendUser=QLabel(frame)
        sendUser.setGeometry(50,5,191,16)
        sendUser.setText("You")
        sendUser.setStyleSheet(styleUserName)

        fileName=QLabel(frame)
        fileName.setGeometry(50,30,191,31)
        fileName.setWordWrap(True)
        fts=opFile.getActualFileName(f)
        fileName.setStyleSheet(styleFileName)

        fileName.setText(fts)
        #fileName.setAlignment(QtCore.Qt.AlignRight)

        progressBar=QProgressBar(frame)
        progressBar.setRange(0,100)
        progressBar.setGeometry(50,70,191,23)

        def onEnd(fName):
                    size=self.c.send.fileSize[fName]
                    fc.onSendEnd(self.sWin,fName)

                    def fun(size):
                        if fName in self.FWidList:
                            frame=self.FWidList[fName]
                            children=frame.children()
                            children[4].setDisabled(True)
                            children[3].setValue(100)
                            size=opFile.getByteToMb(size)
                            size=round(size,2)
                            children[5].setText(f'Size ->{size} mb')

                    self.timerFunList.append(lambda: fun(size))

        self.c.send.funSendListEnd[f]=onEnd

        def funControl():
            frame.close()
            self.c.send.fileFlow[f]=False

        btnControl=QPushButton(frame)
        btnControl.setText("Cancel")
        btnControl.setGeometry(50,100,75,23)
        btnControl.clicked.connect(funControl)

        labelSize=QLabel(frame)
        labelSize.setGeometry(130,100,111,20)
        labelSize.setAlignment(QtCore.Qt.AlignRight)

        size=fc.getSendFileSize(f)

        if size is None:
            labelSize.setText("_None")
        else:
            si=int(size)
            st=opFile.getByteToMb(si)
            st=round(st,2)
            labelSize.setText(f"Size -> {st} mb")

        sendUser.adjustSize()

        labelSize.setStyleSheet(styleSize)

        self.scrollHolder.addWidget(frame,dCount,0)

        self.count=dCount+1
        self.FWidList[f]=frame

        #self.scrollGG.verticalScrollBar().setValue(1000*self.count);

    def handleDownloadFile(self,msg):
        def fun():

            code=msg['code']
            fileName=msg['fileName']

            if code=='c12c':
                text=f'{fileName}-> is downloading started'
                showResult(self.statusbar,text,False)
            elif code=='FEE4':
                text=f'{fileName}-> is deleted/not exist on server'
                showResult(self.statusbar,text)
            else:
                text='Error Code '+code
                showResult(self.statusbar,text)


        self.timerFunList.append(fun)

    def handleCancelDownloadFile(self,msg):
        def fun():

            code=msg['code']
            fileName=msg['fileName']

            if code=='tt56':
                text=f'{fileName}-> is canceled successfully'
                showResult(self.statusbar,text,False)
            elif code=='45GH':
                text=f'{fileName}-> is already downloaded/canceled from server'
                showResult(self.statusbar,text)
            else:
                text='Error Code '+code
                showResult(self.statusbar,text)


        self.timerFunList.append(fun)

    def formatRecvChatFile(self,sender,f,size):
        dCount=self.count

        condYou=False

        if sender.lower()==self.c.userName.lower():
            condYou=True

        frame=QFrame(self.scrollContainer)
        frame.setFixedSize(250,131)

        styleBackgroundUser="""
        background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:0.983, y2:0, stop:0 rgba(127, 127, 127, 255), stop:1 rgba(255, 255, 255, 255));
        """

        styleBackgroundUserYou="""
        background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:0.983, y2:0, stop:0 rgba(0, 124, 0, 255), stop:1 rgba(255, 255, 255, 255));
        
        """

        styleUserNameU='''
        background-color: rgb(81, 255, 0);
        border: 1px solid #1C6EA4;

        '''

        styleFileNameU='''
        background-color: rgb(0, 124,0);
        color:rgb(255,255,255);
        '''

        styleSizeU='''
        background-color: rgb(170, 255, 127);
        '''

        styleUserNameA='''
        background-color: rgb(170, 170, 127);
        border: 1px solid #1C6EA4;
        '''

        styleFileNameA='''
        background-color: rgb(107, 107, 107);
        color: rgb(255, 255, 255);
        '''

        styleSizeA='''
        background-color: rgba(227, 227, 227, 247);
        '''

        labelBackground=QLabel(frame)




        sendUser=QLabel(frame)
        labelSize=None



        fileName=QLabel(frame)

        fileName.setWordWrap(True)
        fts=opFile.getActualFileName(f)

        fileName.setText(fts)
        #fileName.setAlignment(QtCore.Qt.AlignRight)

        progressBar=QProgressBar(frame)
        progressBar.setRange(0,100)

        btnDownload=QPushButton(frame)
        btnCancel=QPushButton(frame)

        labelSize=QLabel(frame)
        btnOpen=QPushButton(frame)


        def onEnd(cond,size):
                fc.onRecvEnd(self.sWin,f)

                def fun():
                    children=self.FWidList[f].children()
                    if cond:
                        children[3].setValue(100)

                        children[-3].close()
                        children[-1].show()
                        children[4].close()
                        children[5].close()
                    else:
                        progressBar.reset()
                    si=int(size)
                    st=opFile.getByteToMb(si)
                    st=round(st,2)

                    labelSize.setText(f"Size -> {st} mb")

                self.timerFunList.append(fun)

        def funDownloadFile():
            self.c.functionList['c-'+self.userName+'-DownloadFileChat']=self.handleDownloadFile
            self.c.downloadFile(f,self.userName)
            btnDownload.close()
            btnCancel.show()

            if f not in self.fileFlowing:
                self.fileFlowing.append(f)


            def onStart():
                fc.onRecvStart(self.sWin,f)

            def onEnd(cond,size):
                fc.onRecvEnd(self.sWin,f)

                def fun():
                    children=self.FWidList[f].children()
                    if cond:
                        children[3].setValue(100)

                        children[-3].close()
                        children[-1].show()
                        children[4].close()
                        children[5].close()
                    else:
                        progressBar.reset()
                    si=int(size)
                    st=opFile.getByteToMb(si)
                    st=round(st,2)

                    children[-1].setText(f"Size -> {st} mb")

                self.timerFunList.append(fun)

            lc.funListRecvEnd[f]=[onStart,onEnd]


        if f in lc.funListRecvEnd:
            lc.funListRecvEnd[f][1]=onEnd


        def funCancelFile():
            self.c.cancelDownloadFile(f,self.userName)
            progressBar.reset()
            self.c.functionList['c-'+self.userName+'-CancelDownloadFileChat']=self.handleCancelDownloadFile
            btnDownload.show()
            btnCancel.close()


        floc=dataStorageLocation+f
        def funOpenFile():
            cond=opFile.checkFileExist(floc)
            if cond:
                def fun():
                    con.execute_command(floc,False)
                threading.Thread(target=fun).start()

                showResult(self.statusbar,"File is opening",False)
            else:
                showResult(self.statusbar,"File not Exist")





        btnDownload.setText("Download")
        btnCancel.setText("Cancel")



        btnOpen.setText("Open")

        btnDownload.clicked.connect(funDownloadFile)
        btnCancel.clicked.connect(funCancelFile)
        btnOpen.clicked.connect(funOpenFile)



        labelSize.setAlignment(QtCore.Qt.AlignRight)

        if condYou:
            labelBackground.setGeometry(40,0,211,131)
            labelBackground.setStyleSheet(styleBackgroundUserYou)
            sendUser.setGeometry(50,5,191,16)
            sendUser.setText("@You")
            fileName.setGeometry(50,30,191,31)
            progressBar.setGeometry(50,70,191,23)
            btnDownload.setGeometry(50,100,75,23)
            btnCancel.setGeometry(50,100,75,23)
            labelSize.setGeometry(130,100,111,20)
            btnOpen.setGeometry(50,100,75,23)

            sendUser.setStyleSheet(styleUserNameU)
            fileName.setStyleSheet(styleFileNameU)
            labelSize.setStyleSheet(styleSizeU)
        else:
            labelBackground.setGeometry(0,0,211,131)
            labelBackground.setStyleSheet(styleBackgroundUser)
            sendUser.setGeometry(10,5,191,16)
            sendUser.setText("#"+sender)
            fileName.setGeometry(10,30,191,31)
            progressBar.setGeometry(10,70,191,23)
            btnDownload.setGeometry(10,100,75,23)
            btnCancel.setGeometry(10,100,75,23)
            labelSize.setGeometry(90,100,111,20)
            btnOpen.setGeometry(10,100,75,23)

            sendUser.setStyleSheet(styleUserNameA)
            fileName.setStyleSheet(styleFileNameA)
            labelSize.setStyleSheet(styleSizeA)

        cond=opFile.checkFileExist(floc)
        if cond and not fc.isFileRecv(self.sWin,f):
            btnDownload.close()
            btnCancel.close()
        else:
            btnOpen.close()
            if fc.isFileRecv(self.sWin,f):
                btnDownload.close()
            else:
                btnCancel.close()

        si=int(size)
        st=opFile.getByteToMb(si)
        st=round(st,2)
        labelSize.setText(f"Size -> {st} mb")



        sendUser.adjustSize()

        self.scrollHolder.addWidget(frame,dCount,0)

        self.count=dCount+1
        self.FWidList[f]=frame

        #self.scrollGG.verticalScrollBar().setValue(1000*self.count);

    def handleFileRuntime(self,msg):
        file=msg['file']
        size=msg['size']
        sender=msg['sender']
        self.formatRecvChatFile(sender,file,size)


    def handleRuntimeChatControl(self):

        if self.dataList is not None:
            data=self.dataList
            self.dataList=None

            for i in data:
                dt,info=i
                dt=dt.lower()
                if dt=='chat':

                    userName=info['userName']
                    chat=ds.dec(info['chat'])
                    self.insertChat(userName,chat)
                elif dt=='file':
                    sender=info['sender']
                    file=info['file']
                    size=info['size']
                    self.formatRecvChatFile(sender,file,size)
                else:
                    print(dt,"Unknown Type")


    def formatChatText(self,userName,chat):
        dCount=self.count

        frame=QFrame(self.scrollContainer)
        frame.setFixedSize(250,51)

        styleBackgroundUser="""
        background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:0.983, y2:0, stop:0 rgba(127, 127, 127, 255), stop:1 rgba(255, 255, 255, 255));
        """

        styleBackgroundUserYou="""
        background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:0.983, y2:0, stop:0 rgba(0, 124, 0, 255), stop:1 rgba(255, 255, 255, 255));
        
        """

        styleUserNameU='''
        background-color: rgb(81, 255, 0);
        border: 1px solid #1C6EA4;

        '''

        styleFileNameU='''
        background-color: rgb(0, 124,0);
        color:rgb(255,255,255);
        '''

        styleUserNameA='''
        background-color: rgb(170, 170, 127);
        border: 1px solid #1C6EA4;
        '''

        styleFileNameA='''
        background-color: rgb(107, 107, 107);
        color: rgb(255, 255, 255);
        '''



        labelBackground=QLabel(frame)


        labelN=QLabel(frame)
        labelN.setText(userName)

        label=QLabel(frame)
        text=chat
        label.setWordWrap(True)
        label.setText(text)
        #label.setFixedWidth(180)
        cond=userName.lower()==self.c.userName.lower()

        if cond:

            labelN.setGeometry(50,5,191,16)
            label.setGeometry(50,30,191,16)
            label.setAlignment(QtCore.Qt.AlignRight)
            labelN.setAlignment(QtCore.Qt.AlignRight)

            labelN.setStyleSheet(styleUserNameU)
            label.setStyleSheet(styleFileNameU)


        else:
            labelN.setGeometry(10,5,191,16)

            label.setGeometry(10,30,191,16)
            labelN.setStyleSheet(styleUserNameA)
            label.setStyleSheet(styleFileNameA)
            #label.setAlignment(QtCore.Qt.AlignLeft)

        labelN.adjustSize()

        label.adjustSize()
        label.setFixedWidth(191)

        frame.setFixedHeight(label.height()+40)
        frame.adjustSize()

        if cond:
            labelBackground.setStyleSheet(styleBackgroundUserYou)
            labelBackground.setGeometry(40,0,211,frame.height())
        else:
            labelBackground.setStyleSheet(styleBackgroundUser)
            labelBackground.setGeometry(0,0,211,frame.height())

        self.scrollHolder.addWidget(frame,dCount,0)
        self.count=dCount+1
        self.scrollGG.verticalScrollBar().setValue(1000*self.count);

    def onClose(self,event):
        XMainWindow.openWindows[self.userName+'chatWindow']=False
        self.fileFlowing=[]
        self.c.loadChatWindow(self.userName,status='unload')
        event.accept()

    def funSetControls(self):
        self.btnSendText.clicked.connect(self.funSendChat)

    def funQTimer(self):
        funList=self.timerFunList

        if len(funList)>0:
            funList[0]()
            self.timerFunList.pop(0)
        self.callFileRefress()



    def finalSetup(self):
        self.radCamSendOn1.clicked.connect(lambda :self.XFunSendCamera(self.radCamSendOn1))
        self.radCamSendOff1.clicked.connect(lambda :self.XFunSendCamera(self.radCamSendOff1))
        self.radCamSendOn2.clicked.connect(lambda :self.XFunSendCamera(self.radCamSendOn2))
        self.radCamSendOff2.clicked.connect(lambda :self.XFunSendCamera(self.radCamSendOff2))

        self.radCamRecvOn1.clicked.connect(lambda :self.XFunRecvCamera(self.radCamRecvOn1))
        self.radCamRecvOff1.clicked.connect(lambda :self.XFunRecvCamera(self.radCamRecvOff1))
        self.radCamRecvOn2.clicked.connect(lambda :self.XFunRecvCamera(self.radCamRecvOn2))
        self.radCamRecvOff2.clicked.connect(lambda :self.XFunRecvCamera(self.radCamRecvOff2))

        self.radSouSendOn1.clicked.connect(lambda :self.XFunSendSound(self.radSouSendOn1))
        self.radSouSendOff1.clicked.connect(lambda :self.XFunSendSound(self.radSouSendOff1))
        self.radSouSendOn2.clicked.connect(lambda :self.XFunSendSound(self.radSouSendOn2))
        self.radSouSendOff2.clicked.connect(lambda :self.XFunSendSound(self.radSouSendOff2))

        self.radSouRecvOn1.clicked.connect(lambda :self.XFunRecvSound(self.radSouRecvOn1))
        self.radSouRecvOff1.clicked.connect(lambda :self.XFunRecvSound(self.radSouRecvOff1))
        self.radSouRecvOn2.clicked.connect(lambda :self.XFunRecvSound(self.radSouRecvOn2))
        self.radSouRecvOff2.clicked.connect(lambda :self.XFunRecvSound(self.radSouRecvOff2))

        self.radScreenRecvOn1.clicked.connect(lambda :self.XFunRecvScreen(self.radScreenRecvOn1))
        self.radScreenRecvOff1.clicked.connect(lambda :self.XFunRecvScreen(self.radScreenRecvOff1))
        self.radScreenRecvOn2.clicked.connect(lambda :self.XFunRecvScreen(self.radScreenRecvOn2))
        self.radScreenRecvOff2.clicked.connect(lambda :self.XFunRecvScreen(self.radScreenRecvOff2))
        self.radScreenRecvOn3.clicked.connect(lambda :self.XFunRecvScreen(self.radScreenRecvOn3))
        self.radScreenRecvOff3.clicked.connect(lambda :self.XFunRecvScreen(self.radScreenRecvOff3))


        self.radScreenSendOn1.clicked.connect(lambda :self.XFunSendScreen(self.radScreenSendOn1))
        self.radScreenSendOff1.clicked.connect(lambda :self.XFunSendScreen(self.radScreenSendOff1))
        self.radScreenSendOn2.clicked.connect(lambda :self.XFunSendScreen(self.radScreenSendOn2))
        self.radScreenSendOff2.clicked.connect(lambda :self.XFunSendScreen(self.radScreenSendOff2))

        self.radKeySendOn1.clicked.connect(lambda :self.XFunSendKeyboard(self.radKeySendOn1))
        self.radKeySendOff1.clicked.connect(lambda :self.XFunSendKeyboard(self.radKeySendOff1))
        self.radKeySendOn2.clicked.connect(lambda :self.XFunSendKeyboard(self.radKeySendOn2))
        self.radKeySendOff2.clicked.connect(lambda :self.XFunSendKeyboard(self.radKeySendOff2))
        self.radKeySendOn3.clicked.connect(lambda :self.XFunSendKeyboard(self.radKeySendOn3))
        self.radKeySendOff3.clicked.connect(lambda :self.XFunSendKeyboard(self.radKeySendOff3))


        self.radMouseSendOn1.clicked.connect(lambda :self.XFunSendMouse(self.radMouseSendOn1))
        self.radMouseSendOff1.clicked.connect(lambda :self.XFunSendMouse(self.radMouseSendOff1))
        self.radMouseSendOn2.clicked.connect(lambda :self.XFunSendMouse(self.radMouseSendOn2))
        self.radMouseSendOff2.clicked.connect(lambda :self.XFunSendMouse(self.radMouseSendOff2))
        self.radMouseSendOn3.clicked.connect(lambda :self.XFunSendMouse(self.radMouseSendOn3))
        self.radMouseSendOff3.clicked.connect(lambda :self.XFunSendMouse(self.radMouseSendOff3))


        self.radKeyRecvOn1.clicked.connect(lambda :self.XFunRecvKeyboard(self.radKeyRecvOn1))
        self.radKeyRecvOff1.clicked.connect(lambda :self.XFunRecvKeyboard(self.radKeyRecvOff1))
        self.radKeyRecvOn2.clicked.connect(lambda :self.XFunRecvKeyboard(self.radKeyRecvOn2))
        self.radKeyRecvOff2.clicked.connect(lambda :self.XFunRecvKeyboard(self.radKeyRecvOff2))

        self.radMouseRecvOn1.clicked.connect(lambda :self.XFunRecvMouse(self.radMouseRecvOn1))
        self.radMouseRecvOff1.clicked.connect(lambda :self.XFunRecvMouse(self.radMouseRecvOff1))
        self.radMouseRecvOn2.clicked.connect(lambda :self.XFunRecvMouse(self.radMouseRecvOn2))
        self.radMouseRecvOff2.clicked.connect(lambda :self.XFunRecvMouse(self.radMouseRecvOff2))

    def xyzFunction(self,widget,on,off):
        cond=widget.isChecked()
        txt=widget.text()
        if 'On' in txt:
            if cond:
                for i in on:
                    i.setChecked(True)
            else:
                for i in off:
                    i.setChecked(True)
        else:
             if cond:
                 for i in off:
                     i.setChecked(True)
             else:
                for i in on:
                    i.setChecked(True)

    def XFunSendCamera(self,widget):

        on=[self.radCamSendOn1,self.radCamSendOn2]
        off=[self.radCamSendOff1,self.radCamSendOff2]

        self.xyzFunction(widget,on,off)
        self.funSendCamera()

    def XFunRecvCamera(self,widget):
        on=[self.radCamRecvOn1,self.radCamRecvOn2]
        off=[self.radCamRecvOff1,self.radCamRecvOff2]

        self.xyzFunction(widget,on,off)
        self.funRecvCamera()

    def XFunSendSound(self,widget):
        on=[self.radSouSendOn1,self.radSouSendOn2]
        off=[self.radSouSendOff1,self.radSouSendOff2]

        self.xyzFunction(widget,on,off)
        self.funSendSound()

    def XFunRecvSound(self,widget):
        on=[self.radSouRecvOn1,self.radSouRecvOn2]
        off=[self.radSouRecvOff1,self.radSouRecvOff2]

        self.xyzFunction(widget,on,off)
        self.funRecvSound()

    def XFunSendKeyboard(self,widget):
        on=[self.radKeySendOn1,self.radKeySendOn2,self.radKeySendOn3]
        off=[self.radKeySendOff1,self.radKeySendOff2,self.radKeySendOff3]

        self.xyzFunction(widget,on,off)
        self.funSendKeyboard()

    def XFunRecvKeyboard(self,widget):
        on=[self.radKeyRecvOn1,self.radKeyRecvOn2]
        off=[self.radKeyRecvOff1,self.radKeyRecvOff2]

        self.xyzFunction(widget,on,off)
        self.funRecvKeyboard()

    def XFunSendMouse(self,widget):
        on=[self.radMouseSendOn1,self.radMouseSendOn2,self.radMouseSendOn3]
        off=[self.radMouseSendOff1,self.radMouseSendOff2,self.radMouseSendOff3]

        self.xyzFunction(widget,on,off)
        self.funSendMouse()

    def XFunRecvMouse(self,widget):
        on=[self.radMouseRecvOn1,self.radMouseRecvOn2]
        off=[self.radMouseRecvOff1,self.radMouseRecvOff2]

        self.xyzFunction(widget,on,off)
        self.funRecvMouse()

    def XFunSendScreen(self,widget):
        on=[self.radScreenSendOn1,self.radScreenSendOn2]
        off=[self.radScreenSendOff1,self.radScreenSendOff2]

        self.xyzFunction(widget,on,off)
        self.funSendScreen()

    def XFunRecvScreen(self,widget):
        on=[self.radScreenRecvOn1,self.radScreenRecvOn2,self.radScreenRecvOn3]
        off=[self.radScreenRecvOff1,self.radScreenRecvOff2,self.radScreenRecvOff3]

        self.xyzFunction(widget,on,off)
        self.funRecvScreen()

    def initiate(self):
        self.previousKeys={}
        keyb.addKeyComb(['Key.Ctrl','t'],self.offRecievingKM)
        keyb.addKeyComb(['Key.Alt','t'],self.offSendingKM)

    def atLastInitiate(self):
        keyb.funOnPress['Ch '+self.userName]=self.funOnKeyPress
        keyb.funOnRelease['Ch '+self.userName]=self.funOnKeyRelease

        mous.funOnScroll['Ch '+self.userName]=self.funOnMouseScroll
        mous.funOnMove['Ch '+self.userName]=self.funOnMouseMove
        mous.funOnClick['Ch '+self.userName]=self.funOnMouseClick

    def disableKeyboardSending(self):
        type='Ch '+self.userName

        if type in keyb.funOnPress:
            keyb.funOnPress[type]=None
            keyb.funOnRelease[type]=None

    def disableMouseSending(self):
        type='Ch '+self.userName

        if type in mous.funOnScroll:
            mous.funOnScroll[type]=None
            mous.funOnClick[type]=None
            mous.funOnMove[type]=None

    def funOnKeyPress(self,data):
        self.labelSendKeyboard1.setText(data)
        self.labelSendKeyboard2.setText(data)

    def funOnKeyRelease(self,data):
        self.labelSendKeyboard1.setText(data)
        self.labelSendKeyboard2.setText(data)

    def funOnMouseMove(self,data):
        self.labelSendMouse1.setText(data)
        self.labelSendMouse2.setText(data)

    def funOnMouseClick(self,data):
        self.labelSendMouse1.setText(data)
        self.labelSendMouse2.setText(data)

    def funOnMouseScroll(self,data):
        self.labelSendMouse1.setText(data)
        self.labelSendMouse2.setText(data)

    def sendCamera(self):
        self.c._Camera(self.fuserName,'@none','@none','@none')

    def sendScreen(self):
        self.c._Screen(self.fuserName,'@none','@none','@none')

    def sendSound(self):
        self.c._Sound(self.fuserName,'@none')

    def sendMouse(self):
        self.c._Mouse(self.fuserName,'@none','@none','@none')

    def sendKeyboard(self):
        self.c._Keyboard(self.fuserName,'@none','@none','@none')

    def setFormalities(self):
        self.condSendSound=False
        self.condSendIntSound=False
        self.condSendScreen=False
        self.condSendCamera=False
        self.condSendMouse=False
        self.condSendKeyboard=False

    def assImpData(self):

        i=self.data
        userName=i[0]
        self.fuserName=userName
        name=i[1]
        imgData=ds.remodifyData(i[2],i[3],i[4])
        cond=i[5]


        self.labelFullName.setText(name)

        imgData=cv2.resize(imgData,(81,91))
        image=pqc.cv2toPqImage(imgData)

        self.labelProfilePic.setPixmap(image)


        if cond=='True':
            self.labelStatus.setStyleSheet("background-color: rgb(0, 255, 0);")
        else:
            self.labelStatus.setStyleSheet("background-color: rgb(255, 0, 0);")

    def refress(self):
        self.c.loadChatWindow(self.userName,status='load')
        time.sleep(0.3)
        self.c.loadChat(self.userName)
        self.c.functionList[self.userName.lower()+'_loadChat']=self.handle
        self.c.functionList[self.userName.lower()+'_Text']=self.handle

        self.c.functionList[self.userName.lower()+'_File']=self.handle
        self.c.functionList[self.userName.lower()+'_Screen']=self.handle
        self.c.functionList[self.userName.lower()+'_Camera']=self.handle
        self.c.functionList[self.userName.lower()+'_Sound']=self.handle
        self.c.functionList[self.userName.lower()+'_IntSound']=self.handle
        self.c.functionList[self.userName.lower()+'_Keyboard']=self.handle
        self.c.functionList[self.userName.lower()+'_Mouse']=self.handle

    def funSendChat(self):

        data=self.editMessage.text()
        if data=='':
            pass
        else:
            self.editMessage.setText('')
            dt=data
            data=self.c.userName+'->'+data

            self.formatChatText(self.c.userName,dt)


            self.c._Text(self.userName,dt)

    def handle(self,msg):
        def fun():
            wType=msg['wType']

            if wType=='onlineStatus':
                self.handleOnlineStatus(msg)
            elif wType=='_loadChat':
                self.handleChat(msg)
            elif wType=='_Text':
                self.handleText(msg)
            elif wType=='_Sound':
                self.handleSound(msg)
            elif wType=='_IntSound':
                self.handleIntSound(msg)
            elif wType=='_Camera':
                self.handleCamera(msg)
            elif wType=='_Screen':
                self.handleScreen(msg)
            elif wType=='_Mouse':
                self.handleMouse(msg)
            elif wType=='_Keyboard':
                self.handleKeyboard(msg)
            elif wType=='_updateControls':
                print("I am controls updater")
            else:
                print("ERROR #$"+code)
                showResult(self.statusbar,"Error :"+code)
        self.timerFunList.append(fun)

    def handleText(self,msg):
        def fun():
            code=msg['code']
            if code=='L100':
                data=msg['chatText']
                data=ds.dec(data)
                #print(data)
                dType,val=ad.deAssValue(data,True)
                chat=ds.dec(val['chat'])

                self.formatChatText(self.userName,chat)
            elif code=='F100':
                val=msg
                print(val)
                file=val['file']
                size=val['size']
                sender=val['fuserName']

                self.formatRecvChatFile(sender,file,size)



            else:
                print("SOME KING OF ERROR IN FILE RECIEVING")

        self.timerFunList.append(fun)

    def handleFile(self,msg):
        print("FILE HANDLER")

    def handleSound(self,msg):
        code=msg['code']

        if code=='d201':
            cond=self.radSouRecvOn1.isChecked()

            if cond:
                #print("HELLO")
                data=msg['data']
                data=ds.decb(bytes(data,'utf-8'))
                stream.write(data)

    def handleCamera(self,msg):
        code=msg['code']

        if code=='d201':
            cond=self.radCamRecvOn1.isChecked()
            if cond:
                data=ds.remodifyData(msg['data'],msg['types'],msg['shape'])

                data=cv2.resize(data,(170,121))
                lb=pqc.cv2toPqImage(data)

                self.labelRecvCamera.setPixmap(lb)

    def handleScreen(self,msg):
        code=msg['code']


        if code=='d201':
            cond=self.radScreenRecvOn1.isChecked()
            if cond:
                data=ds.remodifyData(msg['data'],msg['types'],msg['shape'])

                d2=data.copy()
                d2=cv2.resize(d2,(401,211))
                data=cv2.resize(data,(361,201))

                d2=pqc.cv2toPqImage(d2)
                data=pqc.cv2toPqImage(data)

                self.labelRecvScreen2.setPixmap(d2)
                self.labelRecvScreen1.setPixmap(data)

    def handleMouse(self,msg):
        code=msg['code']

        if code=='d201':
            cond=self.radMouseRecvOn1.isChecked()

            if cond:
                data=ds.remodifyData(msg['data'],msg['types'],msg['shape'])

                for i in data:
                    self.labelRecvMouse1.setText(i)
                    mous.response(i)

    def handleKeyboard(self,msg):
        code=msg['code']

        if code=='d201':
            cond=self.radKeyRecvOn1.isChecked()
            if cond:
                data=ds.remodifyData(msg['data'],msg['types'],msg['shape'])
                for i in data:
                    self.labelRecvKeyboard1.setText(i)

                    keyb.response(i)

    def handleChat(self,msg):
        code=msg['code']

        if code=='se01':
            showResult(self.statusbar,"No Chat Records found")
        elif code=='00sk':
            def fun():
                showResult(self.statusbar,"Data Restored",False)

                data=ds.remodifyData(msg['loadChat'],msg['chatType'],msg['chatShape'])

                for i in data:
                    #print(i)
                    index=i[0]
                    i=ds.dec(i[1])
                    dType,val=ad.deAssValue(i,True)
                    if dType=='Chat':
                        chat=val['chat']
                        sender=val['sender']
                        chat=ds.dec(chat)
                        self.formatChatText(sender,chat)
                    elif dType=='File':
                        info=val
                        sender=info['sender']
                        file=info['file']
                        size=info['size']
                        self.formatRecvChatFile(sender,file,size)

                    else:
                        print("Unknown Data Type Recieving ",dType)



            self.timerFunList.append(fun)

        else:
            showResult(self.statusbar,"Error :"+code)

        self.setFormalities()

    def showSendCamera(self):

        def fun():

            while self.radCamSendOn1.isChecked():
                frame=con.camFrame
                if frame is not None:
                    frame=cv2.resize(frame,(170,121))
                    frame=pqc.cv2toPqImage(frame)
                    self.labelSendCamera.setPixmap(frame)
                time.sleep(0.03)



        class MThread(QThread):

            def run(self):
                fun()
        self.threadShowCamera=MThread()
        self.threadShowCamera.start()

    def showSendScreen(self):
        def fun():

            while self.radScreenSendOn1.isChecked():
                frame=con.screenFrame
                if frame is not None:
                    frame=cv2.resize(frame,(141,91))
                    frame=pqc.cv2toPqImage(frame)
                    self.labelSendScreen.setPixmap(frame)
                time.sleep(0.03)



        class MThread(QThread):

            def run(self):
                fun()
        self.threadShowScreen=MThread()
        self.threadShowScreen.start()

    def funSendCamera(self):
        userName=self.userName
        conType='sCamera'
        if self.radCamSendOn1.isChecked():
            conValue='1'
        else:
            conValue='0'
        if 'camera' in self.previousKeys:
            val=self.previousKeys['camera']
            if val==conValue:
                pass
            else:
                if conValue=='1':
                    XMainWindow.xprtControl.funFirstOnList['camera']=self.sendCamera
                    XMainWindow.xprtControl.funOnSending(self.fuserName,'camera')
                    self.showSendCamera()
                else:
                    XMainWindow.xprtControl.funOffSending(self.fuserName,'camera')
        else:
            if conValue=='1':
                XMainWindow.xprtControl.funFirstOnList['camera']=self.sendCamera
                XMainWindow.xprtControl.funOnSending(self.fuserName,'camera')
                self.showSendCamera()
            else:
                XMainWindow.xprtControl.funOffSending(self.fuserName,'camera')

        self.previousKeys['camera']=conValue
        self.c.updateControls(userName,conType,conValue)
        #self.c.functionList[self.userName.lower()+'_updateControls']=self.handle

    def funRecvCamera(self):
        userName=self.userName
        conType='rCamera'

        if self.radCamRecvOn1.isChecked():
            conValue='1'
        else:
            conValue='0'

        self.c.updateControls(userName,conType,conValue)

    def funSendSound(self):
        userName=self.userName
        conType='sSound'
        conValue=self.radSouSendOn1.isChecked()

        if conValue:
            XMainWindow.xprtControl.funFirstOnList['sound']=self.sendSound
            XMainWindow.xprtControl.funOnSending(self.fuserName,'sound')
            self.c.updateControls(userName,conType,'1')
        else:
            XMainWindow.xprtControl.funOffSending(self.fuserName,'sound')
            self.c.updateControls(userName,conType,'0')

    def funRecvSound(self):
        userName=self.userName
        conType='rSound'

        if self.radSouRecvOn1.isChecked():
            conValue='1'
        else:
            conValue='0'

        self.c.updateControls(userName,conType,conValue)

    def funSendKeyboard(self):
        userName=self.userName
        conType='sKeyboard'

        if self.radKeySendOn1.isChecked():
            conValue='1'
        else:
            conValue='0'

        if conValue=='1':
            XMainWindow.xprtControl.funFirstOnList['keyboard']=self.sendKeyboard
            XMainWindow.xprtControl.funOnSending(self.fuserName,'keyboard')
        else:
            XMainWindow.xprtControl.funOffSending(self.fuserName,'keyboard')
            self.disableKeyboardSending()

        self.c.updateControls(userName,conType,conValue)

    def funRecvKeyboard(self):
        userName=self.userName
        conType='rKeyboard'

        if self.radKeyRecvOn1.isChecked():
            conValue='1'
        else:
            conValue='0'

        self.c.updateControls(userName,conType,conValue)
    #I love you
    #i miss you
    #i want to meet you
    #But i dont know you also want same or not
    def funSendMouse(self):
        userName=self.userName
        conType='sMouse'

        if self.radMouseSendOn1.isChecked():
            conValue='1'
        else:
            conValue='0'

        if conValue=='1':
            XMainWindow.xprtControl.funFirstOnList['mouse']=self.sendMouse
            XMainWindow.xprtControl.funOnSending(self.fuserName,'mouse')
        else:
            XMainWindow.xprtControl.funOffSending(self.fuserName,'mouse')
            self.disableMouseSending()

        self.c.updateControls(userName,conType,conValue)

    def funRecvMouse(self):
        userName=self.userName
        conType='rMouse'

        if self.radMouseRecvOn1.isChecked():
            conValue='1'
        else:
            conValue='0'


        self.c.updateControls(userName,conType,conValue)

    def funSendScreen(self):
        userName=self.userName
        conType='sScreen'

        if self.radScreenSendOn1.isChecked():
            conValue='1'
        else:
            conValue='0'

        if 'screen' in self.previousKeys:
            val=self.previousKeys['screen']
            if val==conValue:
                pass
            else:
                if conValue=='1':
                    XMainWindow.xprtControl.funFirstOnList['screen']=self.sendScreen
                    XMainWindow.xprtControl.funOnSending(self.fuserName,'screen')
                    self.showSendScreen()
                else:
                    XMainWindow.xprtControl.funOffSending(self.fuserName,'screen')
        else:
            if conValue=='1':
                XMainWindow.xprtControl.funFirstOnList['screen']=self.sendScreen
                XMainWindow.xprtControl.funOnSending(self.fuserName,'screen')
                self.showSendScreen()
            else:
                XMainWindow.xprtControl.funOffSending(self.fuserName,'screen')

        self.previousKeys['screen']=conValue
        self.c.updateControls(userName,conType,conValue)

    def funRecvScreen(self):
        userName=self.userName
        conType='rScreen'

        if self.radScreenRecvOn1.isChecked():
            conValue='1'
        else:
            conValue='0'

        self.c.updateControls(userName,conType,conValue)

    def funRequestCam(self):
        vType='camera'
        self.c.rRequest(self.fuserName,vType)

    def funRequestSound(self):
        vType='sound'
        self.c.rRequest(self.fuserName,vType)

    def funRequestKeyboard(self):
        vType='keyboard'
        self.c.rRequest(self.fuserName,vType)

    def funRequestMouse(self):
        vType='mouse'
        self.c.rRequest(self.fuserName,vType)

    def funRequestScreen(self):
        vType='screen'
        self.c.rRequest(self.fuserName,vType)

    def offSendingKeyboard(self):
        self.radKeySendOff1.setChecked(True)
        self.XFunSendKeyboard(self.radKeySendOff1)

    def offSendingMouse(self):
        self.radMouseSendOff1.setChecked(True)
        self.XFunSendMouse(self.radMouseSendOff1)

    def offSendingKM(self):
        self.offSendingKeyboard()
        self.offSendingMouse()
        #[Key.Ctrl,t]

    def offRecievingKeyboard(self):
        self.radKeyRecvOff1.setChecked(True)
        self.XFunRecvKeyboard(self.radKeyRecvOff1)

    def offRecievingMouse(self):
        self.radMouseRecvOff1.setChecked(True)
        self.XFunRecvMouse(self.radMouseRecvOff1)

    def offRecievingKM(self):
        self.offRecievingKeyboard()
        self.offRecievingMouse()
        #[Key.Alt,t]

class XViewProfileMember():
    def setupUi(self, MainWindow):
        self.mainWindow=MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(402, 395)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(170, 250, 81, 16))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(140, 10, 20, 351))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(170, 100, 81, 16))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(170, 40, 81, 16))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(270, 40, 81, 16))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 30, 120, 140))
        self.label.setStyleSheet("background-color: rgb(255, 0, 0);")
        self.label.setText("")
        self.label.setObjectName("label")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(170, 190, 81, 16))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(170, 130, 81, 16))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(170, 160, 81, 16))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(170, 70, 81, 16))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(170, 220, 81, 16))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.textEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(170, 280, 211, 91))
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(270, 70, 101, 16))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(270, 100, 81, 16))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(self.centralwidget)
        self.label_13.setGeometry(QtCore.QRect(270, 130, 81, 16))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        self.label_14 = QtWidgets.QLabel(self.centralwidget)
        self.label_14.setGeometry(QtCore.QRect(270, 160, 111, 16))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        self.label_14.setFont(font)
        self.label_14.setObjectName("label_14")
        self.label_15 = QtWidgets.QLabel(self.centralwidget)
        self.label_15.setGeometry(QtCore.QRect(270, 190, 81, 16))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        self.label_15.setFont(font)
        self.label_15.setObjectName("label_15")
        self.label_16 = QtWidgets.QLabel(self.centralwidget)
        self.label_16.setGeometry(QtCore.QRect(270, 220, 111, 16))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        self.label_16.setFont(font)
        self.label_16.setObjectName("label_16")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        self.qTimer=QTimer()
        self.qTimer.setInterval(500)
        self.qTimer.timeout.connect(lambda :qTimerRefressFun(self.timerFunList))
        self.qTimer.start()
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_10.setText(_translate("MainWindow", "Discription "))
        self.label_4.setText(_translate("MainWindow", "Identity"))
        self.label_2.setText(_translate("MainWindow", "User Name "))
        self.label_6.setText(_translate("MainWindow", "My User Name"))
        self.label_8.setText(_translate("MainWindow", "Email"))
        self.label_5.setText(_translate("MainWindow", "Gender"))
        self.label_7.setText(_translate("MainWindow", "Mobile No"))
        self.label_3.setText(_translate("MainWindow", "Full Name  "))
        self.label_9.setText(_translate("MainWindow", "Date Of Birth"))
        self.textEdit.setPlaceholderText(_translate("MainWindow", "This is the Discription"))
        self.label_11.setText(_translate("MainWindow", "User Full Name"))
        self.label_12.setText(_translate("MainWindow", "User Identity"))
        self.label_13.setText(_translate("MainWindow", "User Gender"))
        self.label_14.setText(_translate("MainWindow", "Mobile Number"))
        self.label_15.setText(_translate("MainWindow", "User Email"))
        self.label_16.setText(_translate("MainWindow", "User Data of Birth"))

    def init(self,c,userName):
        self.c=c
        self.userName=userName
        self.loadData()
        self.label_6.setText(userName)
        self.timerFunList=[]
        self.data=None
        self.mainWindow.setWindowTitle(self.userName+':- User Profile')
        self.mainWindow.closeEvent=self.onClose



    def onClose(self,event):
        XMainWindow.openWindows[self.userName+'userProfile']=False
        event.accept()


    def initData(self):
        name=self.data['name']
        userName=self.data['userName']
        profilePic=ds.remodifyData(self.data['profileData']\
                                   ,self.data['profileType'],self.data['profileShape'])
        profilePic=cv2.resize(profilePic,(120,140))
        img=pqc.cv2toPqImage(profilePic)

        identityU=self.data['identityU']
        gender=self.data['gender']
        contactNo=self.data['contactNo']
        email=self.data['email']
        dob=self.data['dateOfBirth']
        discription=self.data['discription']

        self.label.setPixmap(img)

        if gender=='0':
            gender='Male'
        elif gender=='1':
            gender='Female'
        else:
            gender='Not Shown'

        self.label_11.setText(name)
        self.label_11.adjustSize()

        self.label_12.setText(identityU)
        self.label_12.adjustSize()

        self.label_13.setText(gender)
        self.label_13.adjustSize()

        self.label_14.setText(contactNo)
        self.label_14.adjustSize()

        self.label_15.setText(email)
        self.label_15.adjustSize()

        self.label_16.setText(dob)
        self.label_16.adjustSize()

        self.textEdit.setPlainText(discription)


    def loadData(self):
        window=self.userName+'userProfile'
        self.c.loadUserProfile(self.userName,window)
        self.c.functionList[window]=self.handle

    def handle(self,msg):
        def fun():

            code=msg['code']
            if code=='0028':

                self.data=msg
                self.initData()

            else:
                print("CODING ERROR "+code)
                showResult(self.statusbar,"Error :"+code)

        self.timerFunList.append(fun)

class XAbout():
    def setupUi(self, MainWindow):
        self.mainWindow=MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(279, 387)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.btnCheckUpdate = QtWidgets.QPushButton(self.centralwidget)
        self.btnCheckUpdate.setGeometry(QtCore.QRect(145, 90, 111, 23))
        self.btnCheckUpdate.setObjectName("btnCheckUpdate")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(5, 95, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:1, stop:0 rgba(251, 255, 0, 255), stop:0.971591 rgba(0, 255, 255, 255), stop:1 rgba(255, 255, 255, 255));")
        self.label.setObjectName("label")
        self.editCopyLink = QtWidgets.QLineEdit(self.centralwidget)
        self.editCopyLink.setGeometry(QtCore.QRect(5, 130, 161, 20))
        self.editCopyLink.setObjectName("editCopyLink")
        self.btnCopy = QtWidgets.QPushButton(self.centralwidget)
        self.btnCopy.setGeometry(QtCore.QRect(180, 130, 75, 23))
        self.btnCopy.setObjectName("btnCopy")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(60, 20, 151, 51))
        self.label_2.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(24)
        self.label_2.setFont(font)
        self.label_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.label_2.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:1, stop:0 rgba(126, 179, 255, 255), stop:0.971591 rgba(199, 255, 255, 255), stop:1 rgba(255, 255, 255, 255));")
        self.label_2.setObjectName("label_2")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(20, 160, 211, 41))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.label_4.setStyleSheet("background-color: rgb(85, 255, 0);")
        self.label_4.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(60, 270, 121, 21))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.label_5.setFont(font)
        self.label_5.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.label_5.setStyleSheet("background-color: rgb(170, 255, 127);")
        self.label_5.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_5.setWordWrap(True)
        self.label_5.setObjectName("label_5")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(60, 290, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("\n"
"")
        self.label_3.setTextFormat(QtCore.Qt.AutoText)
        self.label_3.setObjectName("label_3")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(20, 210, 211, 41))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.label_6.setFont(font)
        self.label_6.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.label_6.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:1, stop:0 rgba(251, 255, 255, 255), stop:0.971591 rgba(199, 255, 255, 255), stop:1 rgba(255, 255, 255, 255));")
        self.label_6.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_6.setWordWrap(True)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(10, 330, 271, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:1, stop:0 rgba(255, 208, 126, 255), stop:0.971591 rgba(199, 255, 255, 255), stop:1 rgba(255, 255, 255, 255));")
        self.label_7.setTextFormat(QtCore.Qt.AutoText)
        self.label_7.setObjectName("label_7")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        self.qTimer2=QTimer()
        self.qTimer2.setInterval(500)
        self.qTimer2.timeout.connect(lambda :qTimerRefressFun(self.timerFunList))
        self.qTimer2.start()
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btnCheckUpdate.setText(_translate("MainWindow", "Check for Updates"))
        self.label.setText(_translate("MainWindow", "Version : 1.001"))
        self.btnCopy.setText(_translate("MainWindow", "Copy"))
        self.label_2.setText(_translate("MainWindow", "Xprt-Client"))
        self.label_4.setText(_translate("MainWindow", "Xprt-Client is remote controlling software. \n"
""))
        self.label_5.setText(_translate("MainWindow", "Thanks For Joining"))
        self.label_3.setText(_translate("MainWindow", "Founder :- Bipin Singh"))
        self.label_6.setText(_translate("MainWindow", "The Evolution  can change anything from #0_2_hero."))
        self.label_7.setText(_translate("MainWindow", "Inspired by :- Iron Man 2 ( Tony Stark) - Movie"))

    def init(self,c):
        self.c=c
        self.mainWindow.setWindowTitle("About Xprt-Client")
        self.mainWindow.closeEvent=self.onClose
        self.c.functionList['About']=self.handle

        self.timerFunList=[]

        self.editCopyLink.close()
        self.btnCopy.close()
        self.btnCheckUpdate.clicked.connect(self.funCheckForUpdate)
        self.btnCopy.clicked.connect(self.funBtnCopy)
        self.link=''

    def funCheckForUpdate(self):
        self.c.yCheckVersion(VERSION)

    def handle(self,info):
        def fun():

            code=info['code']

            if code=='4fgr':
                showResult(self.statusbar,"Your version is already uptoDate",False)
            elif code=='hfgr':
                version=info['version']
                txt=f'Version : {version} is avalable'
                showResult(self.statusbar,txt,False)

                link=info['link']
                self.editCopyLink.setText(link)
                self.link=link
                self.btnCopy.show()
                self.editCopyLink.show()

            else:
                showResult(self.statusbar,"Error Code "+code)


        self.timerFunList.append(fun)

    def funBtnCopy(self):
        pyperclip.copy(self.link)

    def onClose(self,event):
        XMainWindow.openWindows['about']=False
        self.qTimer2.stop()
        event.accept()

class XFeedBack():
    def setupUi(self, MainWindow):
        self.mainWindow=MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(361, 170)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.btnSendFeedBack = QtWidgets.QPushButton(self.centralwidget)
        self.btnSendFeedBack.setGeometry(QtCore.QRect(140, 120, 81, 23))
        self.btnSendFeedBack.setObjectName("btnSendFeedBack")
        self.txtFeedBack = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.txtFeedBack.setGeometry(QtCore.QRect(20, 20, 331, 91))
        self.txtFeedBack.setObjectName("txtFeedBack")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        self.qTimer2=QTimer()
        self.qTimer2.setInterval(500)
        self.qTimer2.timeout.connect(lambda :qTimerRefressFun(self.timerFunList))
        self.qTimer2.start()
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btnSendFeedBack.setText(_translate("MainWindow", "Send Feedback"))

    def init(self,c):
        self.c=c

        self.timerFunList=[]

        self.mainWindow.setWindowTitle("Feedback")
        self.mainWindow.closeEvent=self.onClose
        self.c.functionList['feedback']=self.handle
        self.txtFeedBack.setPlainText("Write your feedback here ...")

        self.btnSendFeedBack.clicked.connect(self.funSendFeedBack)

    def funSendFeedBack(self):
        txt=self.txtFeedBack.toPlainText()

        if txt!='':
            self.txtFeedBack.setPlainText("")
            self.c.ySendFeedback(txt)


    def handle(self,info):

        def fun():

            code=info['code']

            if code=='56gt':
                showResult(self.statusbar,"Feedback Send Successfully",False)
            else:
                showResult(self.statusbar,"Error Code "+code)


        self.timerFunList.append(fun)

    def onClose(self,event):
        XMainWindow.openWindows['feedback']=False
        event.accept()
        self.qTimer2.stop()



if __name__ == "__main__":


    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    



    MainWindow.show()

    print(sys.exit(app.exec_()))



