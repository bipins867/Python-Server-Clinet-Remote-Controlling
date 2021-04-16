#GuiXprt2.py
import Gui_Creation as gc
import tkinter as tk
import XprtClient as xc
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

con=rc.Controls()
stream=con.on_mic()
stream2=con.on_mic()
keyb=km.Keyboard()
mous=km.Mouse()
ttk=tk.ttk


class Global:



    def __init__(self,root,c):


        self.c=c
        btnWidth=12
        entryWidth=25
        labelWidth=21
        self.root=root
        root.title('Global Interface')
        self.forward=False
        frame=tk.Frame(root,height=400,width=500)
        self.types=None
        #Title
        titleFrame=tk.Frame(frame,bg='#3A95B6',height=50,width=500)

        labelTitle=tk.Label(titleFrame,text='Online Connection',font="Helvetica 20 bold ",bg='yellow',fg='red')
        labelTitle.place(x=30,y=5)





        leftFrame=tk.Frame(frame,bg='#00a8ff',height=350,width=250)

        self.varUserl=tk.StringVar(root)
        self.varPassl=tk.StringVar(root)

        self.varUserl.set('userName')
        self.varPassl.set('Password')

        entUser=tk.Entry(leftFrame,width=entryWidth,textvariable=self.varUserl)
        entUser.place(x=60,y=30)

        entPass=tk.Entry(leftFrame,width=entryWidth,textvariable=self.varPassl)
        entPass.place(x=60,y=70)


        btnForget=tk.Button(leftFrame,text='Forget Password',width=btnWidth,command=self.forgetPassword)
        btnForget.place(x=60,y=110)

        varLoginStatus=tk.StringVar(root)
        varLoginStatus.set('Login Status')

        btnLogin=tk.Button(leftFrame,text='Login!',width=btnWidth,command=self.btnLogin)
        btnLogin.place(x=120,y=170)

        self.leftLoginStatus=tk.Label(leftFrame,width=labelWidth,text=varLoginStatus.get())
        self.leftLoginStatus.place(x=60,y=210)

        #Right Pane


        rightFrame=tk.Frame(frame,bg='#9AECDB',height=350,width=250)


        self.varNamer=tk.StringVar()
        self.varUserr=tk.StringVar()
        self.varPassr=tk.StringVar()
        self.varSeqQ=tk.StringVar()
        self.varSeqA=tk.StringVar()

        self.varNamer.set('Name')
        self.varUserr.set('UserName')
        self.varPassr.set('Password')
        self.varSeqQ.set('Sequrity Question')
        self.varSeqA.set('Sequrity Answer')

        varUserStatus=tk.StringVar()
        varUserStatus.set('Current Status')

        entNamer=tk.Entry(rightFrame,width=entryWidth,textvariable=self.varNamer)
        entNamer.place(x=60,y=30)

        entUserr=tk.Entry(rightFrame,width=entryWidth,textvariable=self.varUserr)
        entUserr.place(x=60,y=70)

        entPassr=tk.Entry(rightFrame,width=entryWidth,textvariable=self.varPassr)
        entPassr.place(x=60,y=110)

        entSeqQ=tk.Entry(rightFrame,width=entryWidth,textvariable=self.varSeqQ)
        entSeqQ.place(x=60,y=150)

        entSeqA=tk.Entry(rightFrame,width=entryWidth,textvariable=self.varSeqA)
        entSeqA.place(x=60,y=190)




        self.labelUserStatus=tk.Label(rightFrame,width=labelWidth,text=varUserStatus.get())
        self.labelUserStatus.place(x=60,y=230)


        btnSignUp=tk.Button(rightFrame,text='Sign Up!',width=btnWidth,command=self.signUp)
        btnSignUp.place(x=120,y=280)


        rightFrame.place(x=250,y=50)
        leftFrame.place(x=0,y=50)
        titleFrame.place(x=0,y=0)
        frame.place(x=0,y=0)



    def forgetPassword(self):
        for child in self.root.winfo_children():
            child.destroy()
        self.root.geometry('500x400')
        xc.ForgetPassword(self.root,self.c)

    def signUp(self):

        tuserName=self.varUserr.get()
        tpassword=self.varPassr.get()
        tname=self.varNamer.get()
        tseqQ=self.varSeqQ.get()
        tseqA=self.varSeqA.get()

        self.c.functionList['_signUp']=self.handle
        self.c.signUp(tname,tuserName,tpassword,tseqQ,tseqA)
        self.c.userName=tuserName



    def btnLogin(self):

        self.c.functionList['_login']=self.handle
        self.c.userName=self.varUserl.get()
        self.c.login(self.varUserl.get(),self.varPassl.get())

    def handleLogin(self,msg):
        if msg=='0000':
            #Login Successful
            xc.MainWindow(self.root,self.c)
            self.leftLoginStatus.config(text='Login Successful')
        elif msg=='0001':
            #Incorrect password
            self.leftLoginStatus.config(text='Incorrect Password')
        elif msg=='0002':
            #User not exist
            self.leftLoginStatus.config(text='UserName not exist')
        else:
            #Unknown msg request
            self.leftLoginStatus.config(text='Unknown message request')


    def handleSignUp(self,msg):
        if msg=='0003':
            #User already exist
            self.labelUserStatus.config(text='UserName already exist')
        elif msg=='0004':
            #Sign up successfull
            self.labelUserStatus.config(text='SignUp Successfull')
            xc.MainWindow(self.root,self.c)
        else:
            #Unknown msg request
            self.labelUserStatus.config(text='Unknown message request')


    def handle(self,msg):

        if msg['wType']=='_login':
            self.handleLogin(msg['code'])
        elif msg['wType']=='_signUp':
            self.handleSignUp(msg['code'])
        else:
            print("Unknown wType ",wType)

class ForgetPassword:


    def __init__(self,root,c):

        self.c=c


        btnWidth=12
        entryWidth=25
        labelWidth=21
        self.root=root
        root.title('Forget Passowrd')

        frame=tk.Frame(root,height=400,width=500)

        #Title
        titleFrame=tk.Frame(frame,bg='#006266',height=50,width=500)

        labelTitle=tk.Label(titleFrame,text='Forget Password',font="Helvetica 20 bold ",bg='yellow',fg='red')
        labelTitle.place(x=30,y=5)

        btnForward=tk.Button(titleFrame,text='Forward',command=self.btnForward)
        btnForward.place(x=300,y=5)




        downFrame=tk.Frame(frame,bg='#FD7272',height=350,width=500)

        self.varUserName=tk.StringVar(root)
        self.varUserName.set('Enter User Name')

        self.varSeqQ=tk.StringVar(root)
        self.varSeqQ.set('Sequrity Question')

        self.varSeqA=tk.StringVar(root)
        self.varSeqA.set('Sequrity Answer')


        self.varStatus=tk.StringVar(root)
        self.varStatus.set('Submit Status')

        entryUserName=tk.Entry(downFrame,width=entryWidth,textvariable=self.varUserName)
        entryUserName.place(x=200,y=10)

        self.labelSeqQ=tk.Label(downFrame,bg='yellow',text=self.varSeqQ.get(),wraplength=100)
        self.labelSeqQ.place(x=200,y=50)


        entrySeqA=tk.Entry(downFrame,width=entryWidth,textvariable=self.varSeqA)
        entrySeqA.place(x=200,y=150)


        self.labelStatus=tk.Label(downFrame,bg='yellow',text=self.varStatus.get(),wraplength=100)
        self.labelStatus.place(x=200,y=190)

        btnSubmit=tk.Button(downFrame,text='Submit',width=btnWidth,command=self.submit)
        btnSubmit.place(x=200,y=250)

        downFrame.place(x=0,y=50)
        titleFrame.place(x=0,y=0)
        frame.place(x=0,y=0)

    def btnForward(self):
        for child in self.root.winfo_children():
            child.destroy()

        self.root.geometry('500x400')
        xc.Global(self.root,self.c)

    def submit(self):

        tuserName=self.varUserName.get()
        tseqAnswer=self.varSeqA.get()
        self.c.functionList['_forgetPassword']=self.handle
        self.c.forgetPassword(tuserName,tseqAnswer)


    def handle(self,msg):
    	code=msg['code']
    	if code=='0007':
            print(msg)
            self.labelStatus.config(text='Password is copied to clipboard')
            passw=msg['userPass']
            pc.copy(passw)
    	elif code=='0008':
            #Seq A not correct
            self.labelStatus.config(text='SeqA not correct')
    	else:
            #Unknown msg request
            self.labelStatus.config(text='Unknown message request')

class MainWindow:
    openWindows={}
    onlineFriends={}
    labelOnlineFr={}
    giverManager={'sound':None,'IntSound':None,'camera':None,'mouse':None,'keyboard':None}

    xprtFunction=None
    xprtControl=None

    objContainer={}

    def __init__(self,root,c):



        self.root=root
        self.c=c
        self.initiate()
        btnWidth=12
        self.root.geometry('700x400')
        self.root.title('Main Window')
        self.root.protocol('WM_DELETE_WINDOW',self.onClose)
        mainFrame=tk.Frame(self.root,width=700,height=400,bg='red')

        topFrame=gf.GradientFrame(mainFrame,'#8FD1A9','#000000',width=700,height=400,steps=700)

        self.labelProfile=tk.Label(topFrame,width=17,height=10)
        self.labelProfile.place(x=30,y=20)


        self.labelName=tk.Label(topFrame,text='It is the Name of the person',font=self.getFont(15))
        self.labelName.place(x=180,y=20)

        self.labelUserName=tk.Label(topFrame,text='It is userName of the person',font=self.getFont(10))
        self.labelUserName.place(x=180,y=60)


        btnEditProfile=tk.Button(topFrame,text='Edit Profile',width=btnWidth,font=self.getFont(10),command=self.funBtnEditProfile)
        btnEditProfile.place(x=180,y=130)

        btnLogOut=tk.Button(topFrame,text='Log Out',width=btnWidth,font=self.getFont(10),border=2,bg='red')
        btnLogOut.place(x=300,y=130)

        bottomFrame=gf.GradientFrame(mainFrame,'#8FD1A9','#000000',width=700,height=400,steps=1000)

        ffframe=tk.Frame(bottomFrame,width=300,height=195)
        self.frameFriendCont=gf.GradientFrame(ffframe,'#8FD1A9','#000000',width=300,height=195,steps=300)
        self.frameFriendCont.pack()

        ffframe.place(x=20,y=10)


        btnNotification=tk.Button(bottomFrame,text='Notification',font=self.getFont(10),width=btnWidth,command=self.funBtnNotification)
        btnNotification.place(x=350,y=10)

        btnSequrity=tk.Button(bottomFrame,text='Sequrity',font=self.getFont(10),width=btnWidth,command=self.funBtnSequrity)
        btnSequrity.place(x=350,y=50)

        btnFindFriend=tk.Button(bottomFrame,text='Find Friend',font=self.getFont(10),width=btnWidth,command=self.funBtnFindFriend)
        btnFindFriend.place(x=350,y=90)

        btnFriendRequest=tk.Button(bottomFrame,text='Friend Request',font=self.getFont(10),width=btnWidth,command=self.funBtnFriendRequest)
        btnFriendRequest.place(x=350,y=130)

        btnCloudStorage=tk.Button(bottomFrame,text='Cloud Storage',font=self.getFont(10),width=btnWidth)
        #btnCloudStorage.place(x=350,y=170)

        btnBlockUnblock=tk.Button(bottomFrame,text='Block & Unblock',font=self.getFont(10),width=btnWidth,command=self.funBtnBlockUnblock)
        btnBlockUnblock.place(x=470,y=10)

        btnGroupChat=tk.Button(bottomFrame,text='Group Chat',font=self.getFont(10),width=btnWidth,command=self.funBtnGroupChat)
        btnGroupChat.place(x=470,y=50)

        btnGroupMetting=tk.Button(bottomFrame,text='Group Meet',font=self.getFont(10),width=btnWidth,command=self.funBtnGroupMeet)
        #btnGroupMetting.place(x=470,y=90)
        btnGroupMetting.place(x=350,y=170)

        btnHostOnline=tk.Button(bottomFrame,text='Host Online',font=self.getFont(10),width=btnWidth)
        #btnHostOnline.place(x=470,y=130)

        btnOnlineDownload=tk.Button(bottomFrame,text='Online-Download',font=self.getFont(10),width=btnWidth)
        #btnLogOut.place(x=590,y=10)
        #btnOnlineDownload.place(x=470,y=170)

        #btnPrivateStorage=tk.Button(bottomFrame,text='Private-Storage',font=self.getFont(10),width=btnWidth)
        #btnPrivateStorage.place(x=590,y=10)

        topFrame.place(x=0,y=0)
        bottomFrame.place(x=0,y=200)

        mainFrame.place(x=0,y=0)



        self.imgDict={}
        self.refress()

    def initiate(self):

        MainWindow.xprtFunction=xc.Function(self.c)
        MainWindow.xprtControl=xc.Controls()

        MainWindow.xprtControl.funOnStartInstance=self.activateFunction
        MainWindow.xprtControl.funOnEndInstance=self.deactivateFunction

        MainWindow.xprtControl.funList['sound']=self.xxsSound
        MainWindow.xprtControl.funList['IntSound']=self.xxsIntSound
        MainWindow.xprtControl.funList['camera']=self.xxsCamera
        MainWindow.xprtControl.funList['screen']=self.xxsScreen
        MainWindow.xprtControl.funList['mouse']=self.xxsMouse
        MainWindow.xprtControl.funList['keyboard']=self.xxsKeyboard

    def onClose(self):
        self.root.destroy()

        gm=MainWindow.giverManager
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

        self.c.send.s.close()
        sys.exit(1)

    def activateFunction(self,types):

        if types=='sound':
            stream=con.on_mic()
            MainWindow.giverManager['sound']=stream
        elif types=='IntSound':
            stream=con.on_mic()
            MainWindow.giverManager['IntSound']=stream

        elif types=='camera':
            cap=con.on_camera(0)
            MainWindow.giverManager['camera']=cap

        elif types=='mouse':
            mous.mStart()
            MainWindow.giverManager['mouse']=mous

        elif types=='keyboard':
            keyb.mStart()
            MainWindow.giverManager['keyboard']=keyb

        else:
            print(types)
            print("Unknow type you are expecting")

    def deactivateFunction(self,types):
        if types=='sound':
            stream=MainWindow.giverManager['sound']
            stream.close()
            MainWindow.giverManager['sound']=None

        elif types=='IntSound':
            stream=MainWindow.giverManager['IntSound']
            stream.close()
            MainWindow.giverManager['IntSound']=None

        elif types=='camera':
            cap=MainWindow.giverManager['camera']
            cap.release()
            MainWindow.giverManager['camera']=None

        elif types=='mouse':
            mouse=MainWindow.giverManager['mouse']
            mouse.mStop()
            MainWindow.giverManager['mouse']=None

        elif types=='keyboard':

            keyboard=MainWindow.giverManager['keyboard']
            keyboard.mStop()
            MainWindow.giverManager['keyboard']=None

        else:
            print("Unknown type expectiing for Deactivtion")

    def xxsCamera(self):
        cap=MainWindow.giverManager['camera']

        if cap is None:
            pass
        else:
            MainWindow.xprtFunction.sendCamera('@none',cap)

    def xxsScreen(self):

        MainWindow.xprtFunction.sendScreen('@none')

    def xxsSound(self):
        stream=MainWindow.giverManager['sound']

        if stream is None:
            pass
        else:
            MainWindow.xprtFunction.sendSound('@none',stream)

    def xxsMouse(self):
        mouse=MainWindow.giverManager['mouse']

        if mouse is None:
            pass
        else:
            MainWindow.xprtFunction.sendMouse('@none',mouse)

    def xxsKeyboard(self):
        keyboard=MainWindow.giverManager['keyboard']
        if keyboard is None:
            pass
        else:

            MainWindow.xprtFunction.sendKeyboard('@none',keyboard)

    def xxsIntSound(self):
        stream=MainWindow.giverManager['IntSound']

        if stream is None:
            pass
        else:
            MainWindow.xprtFunction.sendIntSound('@none',stream)

    def checkOpenWindow(self,windowName):
        if windowName in MainWindow.openWindows:
            return MainWindow.openWindows[windowName]
        else:
            return False

    def funBtnEditProfile(self):
        windowName='editProfile'
        cond=self.checkOpenWindow(windowName)
        if cond:
            pass

        else:
            MainWindow.openWindows[windowName]=True
            root=tk.Toplevel(self.root)
            xc.EditProfile(root,self.c)

    def funBtnNotification(self):
        windowName='notification'
        cond=self.checkOpenWindow(windowName)
        if cond:
            pass

        else:
            MainWindow.openWindows[windowName]=True
            root=tk.Toplevel(self.root)
            xc.Notification(root,self.c)

    def funBtnSequrity(self):
        windowName='sequrity'
        cond=self.checkOpenWindow(windowName)
        if cond:
            pass

        else:
            MainWindow.openWindows[windowName]=True
            root=tk.Toplevel(self.root)
            xc.Sequrity(root,self.c)

    def funBtnBlockUnblock(self):
        windowName='blockUnblock'
        cond=self.checkOpenWindow(windowName)
        if cond:
            pass

        else:
            MainWindow.openWindows[windowName]=True
            root=tk.Toplevel(self.root)
            xc.BlockUnblock(root,self.c)

    def funBtnFindFriend(self):
        windowName='findFriend'
        cond=self.checkOpenWindow(windowName)
        if cond:
            pass

        else:
            MainWindow.openWindows[windowName]=True
            root=tk.Toplevel(self.root)
            xc.FindFriend(root,self.c)

    def funBtnFriendRequest(self):
        windowName='friendRequest'
        cond=self.checkOpenWindow(windowName)
        if cond:
            pass

        else:
            MainWindow.openWindows[windowName]=True
            root=tk.Toplevel(self.root)
            xc.FriendRequest(root,self.c)

    def funBtnGroupChat(self):
        windowName='groupChat'
        cond=self.checkOpenWindow(windowName)

        if cond:
            pass

        else:
            MainWindow.openWindows[windowName]=True
            root=tk.Toplevel(self.root)
            xc.GroupChat(root,self.c)

    def funBtnGroupMeet(self):
        windowName='groupMeet'
        cond=self.checkOpenWindow(windowName)
        if cond:
            pass

        else:
            MainWindow.openWindows[windowName]=True
            root=tk.Toplevel(self.root)
            xc.GroupMeet(root,self.c)
            #xc.Meeting(root,self.c,True)

    def refress(self):
        self.c.functionList['onlineStatus']=self.handle
        self.c.loadUserProfile(self.c.userName,'_mainWindow')
        self.c.functionList['_mainWindow']=self.handle
        self.c.functionList['_friendListLoad']=self.handle
        self.c.functionList['_Request']=self.handle
        self.c.functionList['_Response']=self.handle

        time.sleep(0.1)
        self.c.friendListLoad(self.c.userName,'_mainWindow')

    def handleLoadUserProfile(self,msg):
        userName=msg['userName']
        name=msg['name']
        img=ds.remodifyData(msg['profileData'],msg['profileType'],msg['profileShape'])
        shape=img.shape

        img=cv2.resize(img,(140,160))
        img=gc.cvtIntoLabelImage(img)
        self.labelName.config(text=name)
        self.labelUserName.config(text=userName)

        self.imgDict['userMainPic']=img


        self.labelProfile.config(width=140,height=160)
        self.labelProfile.config(image=self.imgDict['userMainPic'])

    def refressList(self):
        for i in self.frameFriendCont.winfo_children():
            i.destroy()

    def handleFriendListLoad(self,msg):
        code=msg['code']

        if code=='f102':
            #No friends found


            label=tk.Label(self.frameFriendCont,text='You have no friends')
            label.pack()
        elif code=='f028':
            self.refressList()
            data=ds.remodifyData(msg['friendData'],msg['friendType'],msg['friendShape'])


            self.frameFriendCont1=gc.scrollableFrame(self.frameFriendCont,cwidth=300,cheight=195)[0]

            for i in data:
                self.importData(i)

        else:
            label=tk.Label(self.frameFriendCont,text='Error')
            label.pack()

    def handle(self,msg):

        if msg['wType']=='_loadUserProfile':
            self.handleLoadUserProfile(msg)

        elif msg['wType']=='_friendListLoad':
            self.handleFriendListLoad(msg)

        elif msg['wType']=='onlineStatus':
            self.handleOnlineFriend(msg)

        elif msg['wType']=='_Request':
            self.handle_Request(msg)

        elif msg['wType']=='_Response':
            self.handle_Response(msg)
        else:
            print("UNknow type you are expecting")

    def handleOnlineFriend(self,msg):
        print("I AM KINGDOM")
        userName=msg['userName']
        cond=msg['status']

        MainWindow.onlineFriends[userName]=cond
        if userName.lower() in MainWindow.labelOnlineFr:
            if cond=='True':

                MainWindow.labelOnlineFr[userName.lower()].config(bg='green')
            else:

                MainWindow.labelOnlineFr[userName.lower()].config(bg='red')

    def importData(self,data):

        i=data
        userName=i[0]

        name=i[1]
        imgData=ds.remodifyData(i[2],i[3],i[4])
        cond=i[5]

        MainWindow.onlineFriends[userName]=cond

        frame=tk.Frame(self.frameFriendCont1,width=300,height=100)
        imgData=cv2.resize(imgData,(70,90))
        self.imgDict[userName]=gc.cvtIntoLabelImage(imgData)
        label=tk.Label(frame,width=70,height=90)
        label.config(image=self.imgDict[userName])
        label.place(x=5,y=5)

        label=tk.Label(frame,text=userName)
        label.place(x=100,y=5)

        label=tk.Label(frame,text=name)
        label.place(x=100,y=35)
        if cond!='False':
            MainWindow.labelOnlineFr[userName.lower()]=tk.Label(frame,width=2,height=1,bg='green')
            MainWindow.labelOnlineFr[userName.lower()].place(x=240,y=10)
        else:
            MainWindow.labelOnlineFr[userName.lower()]=tk.Label(frame,width=2,height=1,bg='red')
            MainWindow.labelOnlineFr[userName.lower()].place(x=240,y=10)

        def userProfile():
            windowName=userName+'userProfile'
            cond=self.checkOpenWindow(windowName)
            if cond:
                pass

            else:
                MainWindow.openWindows[windowName]=True
                root=tk.Toplevel(self.root)

                xc.UserProfile(root,userName,self.c)

        def chatWindow():
            windowName=userName+'chatWindow'
            cond=self.checkOpenWindow(windowName)
            if cond:
                pass

            else:
                MainWindow.openWindows[windowName]=True
                root=tk.Toplevel(self.root)
                MainWindow.xprtControl.funOpenWindow(userName)

                xt=xc.ChatWindow(root,self.c,data)

                tit=userName.lower()+'-chatWindow'
                MainWindow.objContainer[tit]=xt
                self.c.functionList[userName.lower()+'1onlineStatus']=xt.handle



        btnViewProfile=tk.Button(frame,text='View Profile',command=userProfile)
        btnViewProfile.place(x=100,y=70)

        btnChatWindow=tk.Button(frame,text='Chat Window',command=chatWindow)
        btnChatWindow.place(x=180,y=70)

        frame.pack()


    def handle_Request(self,msg):

        userName=msg['userName']
        vType=msg['vType']
        code=msg['code']

        def Request():
            windowName=userName+'request'
            cond=self.checkOpenWindow(windowName)
            if cond:
                pass

            else:
                MainWindow.openWindows[windowName]=True
                root=tk.Toplevel(self.root)
                MainWindow.xprtControl.funOpenWindow(userName)

                xt=xc.Request(root,self.c,userName,vType)

        if code=='LHY0':

            Request()

    def handle_Response(self,msg):
        userName=msg['userName']
        vType=msg['vType']
        vValue=msg['vValue']

        print("KSKDFLFL")

        def Response():
            windowName=userName+'request'
            cond=self.checkOpenWindow(windowName)
            if cond:
                pass

            else:
                MainWindow.openWindows[windowName]=True
                root=tk.Toplevel(self.root)
                MainWindow.xprtControl.funOpenWindow(userName)

                xt=xc.Response(root,self.c,userName,vType,vValue)
        code=msg['code']

        if code=='LHN0':
            Response()

    def getFont(self,size):
        font="Helvetica {0} bold ".format(size)
        return font

class EditProfile:

    def __init__(self,root,c):
        self.root=root
        self.c=c
        btnWidth=12
        self.root.geometry('300x400')
        self.tempData={}
        self.root.protocol('WM_DELETE_WINDOW',self.onClose)

        mainFrame=tk.Frame(self.root,width=300,height=400,bg='red')

        topFrame=gf.GradientFrame(mainFrame,'#4AB54E','#6A71D8',width=300,height=400,steps=700)


        self.labelProfilePic=tk.Label(topFrame,width=15,height=9)
        self.labelProfilePic.place(x=30,y=30)

        btnSetImage=tk.Button(topFrame,text='Set Image',font=self.getFont(10),width=btnWidth,command=self.setImage)
        btnSetImage.place(x=30,y=200)

        btnUpdate=tk.Button(topFrame,text='Upload \n to Server',font=self.getFont(10),width=btnWidth,command=self.uploadData)
        btnUpdate.place(x=30,y=250)

        self.labelStatus=tk.Label(topFrame)
        self.labelStatus.place(x=30,y=295)

        self.varName=tk.StringVar()
        self.varName.set('Hello World')
        self.varIdentityU=tk.StringVar()
        self.varGender=tk.IntVar()
        self.varContact=tk.StringVar()
        self.varEmail=tk.StringVar()
        self.varDob=tk.StringVar()

        self.imageLoc='_None'

        self.imgDict={}

        self.labelUserName=tk.Label(topFrame,text='UserName',font=self.getFont(10))
        self.labelUserName.place(x=170,y=30)



        entryName=tk.Entry(topFrame,textvariable=self.varName,font=self.getFont(10),width=17)
        entryName.place(x=170,y=70)

        entryIdentityU=tk.Entry(topFrame,textvariable=self.varIdentityU,font=self.getFont(10),width=17)
        entryIdentityU.place(x=170,y=110)

        r1=tk.Radiobutton(topFrame,text="Male",variable=self.varGender,value=1,font=self.getFont(7))
        r2=tk.Radiobutton(topFrame,text="Female",variable=self.varGender,value=-1,font=self.getFont(7))
        r3=tk.Radiobutton(topFrame,text="Other",variable=self.varGender,value=0,font=self.getFont(7))

        r1.place(x=170,y=140)
        r2.place(x=230,y=140)
        r3.place(x=200,y=170)

        entryContact=tk.Entry(topFrame,textvariable=self.varContact,font=self.getFont(10),width=17)
        entryContact.place(x=170,y=210)

        entryEmail=tk.Entry(topFrame,textvariable=self.varEmail,font=self.getFont(10),width=17)
        entryEmail.place(x=170,y=250)

        entryDob=tk.Entry(topFrame,textvariable=self.varDob,font=self.getFont(10),width=17)
        entryDob.place(x=170,y=290)

        self.textDiscription=tk.Text(topFrame,width=33,height=4)
        self.textDiscription.place(x=30,y=330)


        topFrame.place(x=0,y=0)
        mainFrame.place(x=0,y=0)

        self.refress()

    def refress(self):
        self.c.loadUserProfile(self.c.userName,'_editProfile')
        self.c.functionList['_editProfile']=self.handle

    def onClose(self):
        MainWindow.openWindows['editProfile']=False
        self.root.destroy()

    def getFont(self,size):
        font="Helvetica {0}  ".format(size)
        return font

    def setImage(self):

        #fileName=filedialog.askopenfilename(initialdir='/',title='Hel',filetype=(('jpeg','*.jpg'),('All Files','*.*')))
        fileName=filedialog.askopenfilename(initialdir='/',title='select a file')
        #fileName=filedialog.askdirectory()
        self.imageLoc=fileName

    def uploadData(self):
        #print("I am uploading data")
        #print(self.imageLoc == '')
        #time.sleep(0.1)
        name=self.varName.get()
        if name!=self.tempData['name']:
            self.c.editProfile('name',name)
            time.sleep(0.2)

        identityU=self.varIdentityU.get()
        if identityU!=self.tempData['identityU']:

            self.c.editProfile('identityU',identityU)
            time.sleep(0.2)

        gender=str(self.varGender.get())
        if gender!=self.tempData['gender']:
            self.c.editProfile('gender',gender)
            time.sleep(0.2)

        contactNo=self.varContact.get()
        if contactNo!=self.tempData['contactNo']:
            self.c.editProfile('contactNo',contactNo)
            time.sleep(0.2)

        email=self.varEmail.get()
        if email!=self.tempData['email']:
            self.c.editProfile('email',email)
            time.sleep(0.2)

        dob=self.varDob.get()
        if dob!=self.tempData['dateOfBirth']:
            self.c.editProfile('dateOfBirth',dob)
            time.sleep(0.2)
        content = self.textDiscription.get('1.0',tk.END)

        if content!=self.tempData['discription']:
            self.c.editProfile('discription',content)
            time.sleep(0.2)





        if self.imageLoc!='' and self.imageLoc!='_None':
            self.c.editProfile('locProfilePic','imgData',self.imageLoc)
            time.sleep(0.2)

        self.c.functionList['_editProfile']=self.handle

    def handle(self,msg):
        if 'userName' in msg:
            self.handleRefress(msg)
        else:
            self.handleResponse(msg)

    def handleResponse(self,msg):
        if msg['code']=='0009':
            self.labelStatus.config(text='Updation Completed')

    def handleRefress(self,msg):
        self.tempData=msg
        userName=msg['userName']
        name=msg['name']

        img=ds.remodifyData(msg['profileData'],msg['profileType'],msg['profileShape'])
        shape=img.shape

        img=cv2.resize(img,(130,150))
        img=gc.cvtIntoLabelImage(img)
        self.varName.set(name)
        self.labelUserName.config(text=userName)

        self.varEmail.set(msg['email'])

        self.varContact.set(msg['contactNo'])

        self.varIdentityU.set(msg['identityU'])
        self.varDob.set(msg['dateOfBirth'])
        self.textDiscription.insert(tk.INSERT,msg['discription'])
        self.varGender.set(int(msg['gender']))
        self.imgDict['userMainPic']=img


        self.labelProfilePic.config(width=130,height=150)
        self.labelProfilePic.config(image=self.imgDict['userMainPic'])

class Notification:

    def __init__(self,root,c):
        self.root=root
        self.c=c
        self.root.geometry('270x350')
        self.root.protocol('WM_DELETE_WINDOW',self.onClose)
        self.root.title("Notification")

        self.dataForMoreThanOne=False
        self.dataLengthIsZero=True

        self.r1=1
        self.r2=10

        mainFrame=tk.Frame(self.root,width=270,height=350,bg='red')

        topFrame=gf.GradientFrame(mainFrame,'#984FAF','#AF9C4F',width=270,height=350,steps=700)

        self.labelStatus=tk.Label(topFrame,text='Status',font=self.getFont(9))
        self.labelStatus.place(x=10,y=10)


        self.frameNotification1=gf.GradientFrame(topFrame,'#66571B','#5BC9DA',width=250,height=280,steps=300)
        self.frameNotification1.place(x=10,y=50)

        self.frameNotification=gf.GradientFrame(self.frameNotification1,'#66571B','#5BC9DA',width=250,height=280,steps=300)
        self.frameNotification.place(x=0,y=0)




        topFrame.place(x=0,y=0)
        mainFrame.place(x=0,y=0)


        self.refress()


    def refressList(self):
        for i in self.frameNotification1.winfo_children():
            i.destroy()

        self.frameNotification=gf.GradientFrame(self.frameNotification1,'#66571B','#5BC9DA',width=250,height=280,steps=300)
        self.frameNotification.place(x=0,y=0)



    def refress(self):
        self.c.loadNotification(self.r1,self.r2)
        self.c.functionList['_loadNotification']=self.handle

    def onClose(self):
        MainWindow.openWindows['notification']=False
        self.root.destroy()

    def getFont(self,size):
        font="Helvetica {0} bold ".format(size)
        return font

    def importData(self,data,tfm):

        data=data[::-1]
        frameList=self.frameNotification
        if tfm=='True':

            self.st=gc.scrollableFrame(frameList,cwidth=230,cheight=280)[0]
        else:
            self.st.winfo_children()[-1].destroy()
        st=self.st
        for i in data:
            frame=gf.GradientFrame(st,'#58A928','#28A9A1',230,50,steps=600)

            label=tk.Label(frame,text=i,font=self.getFont(7))

            label.place(x=10,y=10)



            frame.pack()

        frame=gf.GradientFrame(st,'#58A928','#28A9A1',230,50,steps=600)

        if not self.dataLengthIsZero:
            def fun():
                self.dataForMoreThanOne=True
                self.r1=self.r2+1

                self.r2=self.r2+11

                self.c.loadNotification(self.r1,self.r2)
            btn=tk.Button(frame,text='Load More',font=self.getFont(9),command=fun)
            btn.place(x=10,y=10)
        else:
            label=tk.Label(frame,text='X----------END----------X',font=self.getFont(7))
            label.place(x=10,y=10)
        frame.pack()


    def handle(self,msg):
        code=msg['code']

        if code=='kk01':
            self.labelStatus.config(text='No Data is found')
            self.dataLengthIsZero=True


        elif code=='001k':

            self.labelStatus.config(text='Data is founnded')
            data=ds.remodifyData(msg['notifData'],msg['notifType'],msg['notifShape'])

            self.dataLengthIsZero=False
            if msg['tfm']=='True':
                self.refressList()


            self.importData(data,msg['tfm'])
        else:
            self.labelStatus.config(text='Error data loading')

class Sequrity:

    def __init__(self,root,c):
        self.c=c
        self.root=root
        self.root.geometry('500x400')
        btnWidth=12
        self.root.protocol('WM_DELETE_WINDOW',self.onClose)
        self.root.title("Notification")
        mainFrame=tk.Frame(self.root,width=500,height=400,bg='red')

        topFrame=gf.GradientFrame(mainFrame,'#A55DAE','#907F2B',width=500,height=400,steps=700)

        self.changePassLabel=tk.Label(topFrame,text='Change Password',font=self.getFont(10))
        self.changePassLabel.place(x=30,y=30)

        self.varOldPass=tk.StringVar()
        self.varOldPass.set('Old Password')
        self.varNewPass=tk.StringVar()
        self.varNewPass.set('New Password')

        entryOldPass=tk.Entry(topFrame,textvariable=self.varOldPass,font=self.getFont(8))
        entryOldPass.place(x=30,y=70)

        entryNewPass=tk.Entry(topFrame,textvariable=self.varNewPass,font=self.getFont(8))
        entryNewPass.place(x=30,y=100)


        btnUpdatePass=tk.Button(topFrame,text='Update Password',font=self.getFont(9),width=btnWidth+3,command=self.btnFunUpdatePass)
        btnUpdatePass.place(x=30,y=140)

        self.changeSeqLabel=tk.Label(topFrame,text='Change Seq Q & A',font=self.getFont(10))
        self.changeSeqLabel.place(x=280,y=30)

        self.varCurrentPass=tk.StringVar()
        self.varCurrentPass.set('Current Password')
        self.varSeqQ=tk.StringVar()
        self.varSeqQ.set('Seq Q')
        self.varSeqA=tk.StringVar()
        self.varSeqA.set('Seq A')

        entryCurrentPass=tk.Entry(topFrame,textvariable=self.varCurrentPass,font=self.getFont(8))
        entryCurrentPass.place(x=280,y=70)

        entrySeqQ=tk.Entry(topFrame,textvariable=self.varSeqQ,font=self.getFont(8))
        entrySeqQ.place(x=280,y=100)

        entrySeqA=tk.Entry(topFrame,textvariable=self.varSeqA,font=self.getFont(8))
        entrySeqA.place(x=280,y=130)

        btnUpdateSeq=tk.Button(topFrame,text='Update Seq',font=self.getFont(9),width=btnWidth+3,command=self.btnFunUpdateSeq)
        btnUpdateSeq.place(x=280,y=170)

        self.labelStatus=tk.Label(topFrame,text='Status',font=self.getFont(12))
        self.labelStatus.place(x=30,y=250)

        topFrame.place(x=0,y=0)
        mainFrame.place(x=0,y=0)

    def onClose(self):
        MainWindow.openWindows['sequrity']=False
        self.root.destroy()

    def handle(self,msg):
        code=msg['code']

        if code=='0005':
            self.labelStatus.config(text='Password Updated"')
        elif code=='0006':
            self.labelStatus.config(text='Old Password Incorrect')
        elif code=='0011':
            self.labelStatus.config(text='Seq Q A updated')
        elif code=='0010':
            self.labelStatus.config(text='Password is incorrect')
        else:
            self.labelStatus.config(text=code)

    def btnFunUpdatePass(self):
        self.c.functionList['_changePassword']=self.handle

        oldPass=self.varOldPass.get()
        newPass=self.varNewPass.get()
        self.c.changePassword(self.c.userName,oldPass,newPass)


    def btnFunUpdateSeq(self):
        self.c.functionList['_changeSeqQA']=self.handle

        currenPass=self.varCurrentPass.get()
        seqQ=self.varSeqQ.get()
        seqA=self.varSeqA.get()

        self.c.changeSeqQA(seqQ,seqA,currenPass)

    def getFont(self,size):
        font="Helvetica {0} bold ".format(size)
        return font

class BlockUnblock:


    def __init__(self,root,c):
        self.root=root
        self.c=c
        self.imgDict={}
        self.root.title('Block & unblock')
        self.root.geometry('500x400')
        btnWidth=12

        self.root.protocol('WM_DELETE_WINDOW',self.onClose)

        mainFrame=tk.Frame(self.root,width=500,height=400,bg='red')

        topFrame=gf.GradientFrame(mainFrame,'#297B94','#795B55',width=500,height=400,steps=700)

        self.labelBlock=tk.Label(topFrame,text='Block',font=self.getFont(10))
        self.labelBlock.place(x=30,y=30)

        self.varBlockName=tk.StringVar()
        self.varBlockName.set("UserName/Name")

        entryBlockName=tk.Entry(topFrame,textvariable=self.varBlockName,font=self.getFont(8))
        entryBlockName.place(x=30,y=70)

        btnSearchBlock=tk.Button(topFrame,text='Search',font=self.getFont(9),width=btnWidth,command=self.funBtnBlockSearch)
        btnSearchBlock.place(x=30,y=100)

        self.frameBlockList1=gf.GradientFrame(topFrame,'#297B94','#795B55',width=200,height=200,steps=700)
        self.frameBlockList1.place(x=30,y=130)

        self.frameBlockList=gf.GradientFrame(self.frameBlockList1,'#297B94','#795B55',width=200,height=200,steps=700)
        self.frameBlockList.place(x=0,y=0)

        self.labelUnblock=tk.Label(topFrame,text='Unblock',font=self.getFont(10))
        self.labelUnblock.place(x=280,y=30)


        btnLoadUnblock=tk.Button(topFrame,text='Load',font=self.getFont(9),width=btnWidth,command=self.funBtnUnblockLoad)
        btnLoadUnblock.place(x=280,y=70)

        self.frameUnBlockList1=gf.GradientFrame(topFrame,'#297B94','#795B55',width=200,height=200,steps=700)
        self.frameUnBlockList1.place(x=280,y=130)
        self.frameUnBlockList=gf.GradientFrame(self.frameUnBlockList1,'#297B94','#795B55',width=200,height=200,steps=700)
        self.frameUnBlockList.place(x=0,y=0)

        self.labelStatus=tk.Label(topFrame,text='Status',font=self.getFont(12))
        self.labelStatus.place(x=30,y=350)

        topFrame.place(x=0,y=0)
        mainFrame.place(x=0,y=0)

    def getFont(self,size):
        font="Helvetica {0} bold ".format(size)
        return font
    def onClose(self):
        MainWindow.openWindows['blockUnblock']=False
        self.root.destroy()

    def funBtnBlockSearch(self):
        self.c.functionList['_blockSearch']=self.handle

        userName=self.varBlockName.get()
        self.refressList()
        self.c.blockSearch(userName)

    def funBtnUnblockLoad(self):
        self.c.functionList['_unblockLoad']=self.handle
        self.refressList()
        self.c.unblockLoad()

    def handle(self,msg):

        if msg['wType']=='_unblockLoad':
            self.handleUnblock(msg)
        elif msg['wType']=='_blockSearch':
            self.handleBlock(msg)
        elif msg['wType']=='_block':
            self.handleBlockOnly(msg)
        elif msg['wType']=='_unblock':
            self.handleUnblockOnly(msg)
        else:
            self.labelStatus.config(text='Error ')

    def handleBlockOnly(self,msg):
        code=msg['code']
        print("HANDLE BLOCK ONLY")
        if code=='0021':
            self.labelStatus.config(text='Blocking successfull')
        else:
            self.labelStatus.config(text='Blocking Unsuccessfull')

    def handleUnblockOnly(self,msg):
        code=msg['code']
        print("HANDLE UNBLOCK ONLY")
        if code=='0021':
            self.labelStatus.config(text='UnBlocking successfull')
        else:
            self.labelStatus.config(text='UnBlocking Unsuccessfull')

    def refressList(self):
        for i in self.frameBlockList1.winfo_children():
            i.destroy()
        for i in self.frameUnBlockList1.winfo_children():
            i.destroy()
        self.frameUnBlockList=gf.GradientFrame(self.frameUnBlockList1,'#297B94','#795B55',width=200,height=200,steps=700)
        self.frameUnBlockList.place(x=280,y=130)


        self.frameBlockList=gf.GradientFrame(self.frameBlockList1,'#297B94','#795B55',width=200,height=200,steps=700)
        self.frameBlockList.place(x=0,y=0)

    def importData(self,frameList,data,types='block'):
        st=gc.scrollableFrame(frameList)[0]
        i=data
        userName=i[0]
        name=i[1]
        imgData=ds.remodifyData(i[2],i[3],i[4])

        frame=gf.GradientFrame(st,'#58A928','#28A9A1',200,100,steps=600)
        imgData=cv2.resize(imgData,(70,90))
        self.imgDict[userName]=gc.cvtIntoLabelImage(imgData)
        label=tk.Label(frame,width=70,height=90)
        label.config(image=self.imgDict[userName])
        label.place(x=5,y=5)

        label=tk.Label(frame,text=userName)
        label.place(x=100,y=5)

        label=tk.Label(frame,text=name)
        label.place(x=100,y=35)
        def funBlock():

            self.c.functionList['_block']=self.handle
            self.c.block(userName)
            self.refressList()


        def funUnblock():

            self.refressList()
            self.c.functionList['_unblock']=self.handle
            self.c.unblock(userName)





        if types=='block':
            btn=tk.Button(frame,text='Block')
            btn.config(command=funBlock)
        else:
            btn=tk.Button(frame,text='UnBlock')
            btn.config(command=funUnblock)

        btn.place(x=100,y=70)

        frame.pack()

    def handleBlock(self,msg):

        code=msg['code']
        self.refressList()
        if code=='0019':
            self.labelStatus.config(text='Block-No Records found')
        #   No Records found
        elif code=='0013':
            self.labelStatus.config(text='Block-No Records found')

        elif code=='0020':
            self.labelStatus.config(text='Block-Records found')
            data=ds.remodifyData(msg['usersData'],msg['usersType'],msg['usersShape'])

            for i in data:
                self.importData(self.frameBlockList,i)

        else:
            self.labelStatus.config(text=code)

    def handleUnblock(self,msg):

        self.refressList()
        code=msg['code']

        if code=='0022':
            self.labelStatus.config(text='No Records found')
            # No Records found
        elif code=='0023':
            self.labelStatus.config(text='Records found')
            data=ds.remodifyData(msg['usersData'],msg['usersType'],msg['usersShape'])

            for i in data:
                self.importData(self.frameUnBlockList,i,'unblock')
        else:
            self.labelStatus.config(text=code)

class FindFriend:

    def __init__(self,root,c):
        self.c=c
        self.root=root
        self.imgDict={}
        self.root.geometry('300x400')
        btnWidth=12

        self.root.protocol('WM_DELETE_WINDOW',self.onClose)

        self.root.title("Find Friends")
        mainFrame=tk.Frame(self.root,width=300,height=400,bg='red')

        topFrame=gf.GradientFrame(mainFrame,'#11267A','#5EB074',width=300,height=400,steps=700)

        self.varUserName=tk.StringVar()
        self.varUserName.set("UserName/Name")

        entryUserName=tk.Entry(topFrame,textvariable=self.varUserName,font=self.getFont(8))
        entryUserName.place(x=30,y=30)


        btnSearch=tk.Button(topFrame,text='Search',width=btnWidth,font=self.getFont(7),command=self.funBtnSearch)

        btnSearch.place(x=200,y=30)

        self.labelStatus=tk.Label(topFrame,text='Status',font=self.getFont(9))
        self.labelStatus.place(x=30,y=70)

        self.frameList1=gf.GradientFrame(topFrame,'#B07F5E','#258D33',width=250,height=290,steps=300)
        self.frameList1.place(x=30,y=100)

        self.frameList=gf.GradientFrame(self.frameList1,'#B07F5E','#258D33',width=250,height=290,steps=300)
        self.frameList.place(x=0,y=0)

        topFrame.place(x=0,y=0)
        mainFrame.place(x=0,y=0)

    def getFont(self,size):
        font="Helvetica {0} bold ".format(size)
        return font

    def handleSearchResponse(self,msg):
        code=msg['code']

        if code=='0012' or code=='0013':
            self.labelStatus.config(text='No Data Found')
        elif code=='0014':
            self.labelStatus.config(text='Data Found')
            data=ds.remodifyData(msg['usersData'],msg['usersType'],msg['usersShape'])

            for i in data:
                self.importData(self.frameList,i)
        #Rcordf
        else:
            self.labelStatus.config(text='Error Only')

    def handleSendFriendRequest(self,msg):
        code=msg['code']

        if code=='0014':
            self.labelStatus.config(text='Friend Request Already Sent')
        elif code=='0015':
            self.labelStatus.config(text='Already Friend')
        elif code=='0016':
            self.labelStatus.config(text='Friend Request Sending Successfull')
        else:
            self.labelStatus.config(text=code)

    def handle(self,msg):
        wType=msg['wType']

        if wType=='_searchFriend':
            self.handleSearchResponse(msg)
        elif wType=='_sendFriendRequest':
            self.handleSendFriendRequest(msg)
        else:
            self.labelStatus.config('Unknown type of data')

    def refressList(self):
        for i in self.frameList1.winfo_children():
            i.destroy()

        self.frameList=gf.GradientFrame(self.frameList1,'#B07F5E','#258D33',width=250,height=290,steps=300)
        self.frameList.place(x=0,y=0)

    def funBtnSearch(self):
        userName=self.varUserName.get()
        self.c.functionList['_searchFriend']=self.handle
        self.refressList()
        self.c.searchFriend(userName)

    def importData(self,frameList,data):
        st=gc.scrollableFrame(frameList,cheight=290,cwidth=250)[0]
        i=data
        userName=i[0]
        name=i[1]

        imgData=ds.remodifyData(i[2],i[3],i[4])

        frame=gf.GradientFrame(st,'#58A928','#28A9A1',250,100,steps=600)
        imgData=cv2.resize(imgData,(70,90))
        self.imgDict[userName]=gc.cvtIntoLabelImage(imgData)
        label=tk.Label(frame,width=70,height=90)
        label.config(image=self.imgDict[userName])
        label.place(x=5,y=5)

        label=tk.Label(frame,text=userName)
        label.place(x=100,y=5)

        label=tk.Label(frame,text=name)
        label.place(x=100,y=35)
        def funBlock():

            self.c.functionList['_sendFriendRequest']=self.handle
            self.c.sendFriendRequest(userName)
            self.refressList()


        btn=tk.Button(frame,text='Add Friend')
        btn.config(command=funBlock)



        btn.place(x=100,y=70)

        frame.pack()

    def onClose(self):
        MainWindow.openWindows['findFriend']=False
        self.root.destroy()

class FriendRequest:

    def __init__(self,root,c):
        self.root=root
        self.c=c
        self.imgDict={}
        self.root.geometry('270x350')
        self.root.protocol('WM_DELETE_WINDOW',self.onClose)
        self.root.title("Friend Request")
        mainFrame=tk.Frame(self.root,width=270,height=350,bg='red')

        topFrame=gf.GradientFrame(mainFrame,'#984FAF','#AF9C4F',width=270,height=350,steps=700)

        self.labelStatus=tk.Label(topFrame,text='Status',font=self.getFont(9))
        self.labelStatus.place(x=10,y=10)


        self.frameNotification1=gf.GradientFrame(topFrame,'#66571B','#5BC9DA',width=250,height=280,steps=300)
        self.frameNotification1.place(x=10,y=50)

        self.frameNotification=gf.GradientFrame(self.frameNotification1,'#66571B','#5BC9DA',width=250,height=280,steps=300)
        self.frameNotification.place(x=0,y=0)




        topFrame.place(x=0,y=0)
        mainFrame.place(x=0,y=0)

        self.refress()

    def refressList(self):
        for i in self.frameNotification1.winfo_children():
            i.destroy()

        self.frameNotification=gf.GradientFrame(self.frameNotification1,'#66571B','#5BC9DA',width=250,height=280,steps=300)
        self.frameNotification.place(x=0,y=0)



    def refress(self):
        self.c.loadFriendRequest()
        self.c.functionList['_loadFriendRequest']=self.handle

    def onClose(self):
        MainWindow.openWindows['friendRequest']=False
        self.root.destroy()

    def getFont(self,size):
        font="Helvetica {0} bold ".format(size)
        return font

    def importData(self,data):
        frameList=self.frameNotification
        st=gc.scrollableFrame(frameList,cwidth=230,cheight=280)[0]

        for i in data:
            frame=gf.GradientFrame(st,'#58A928','#28A9A1',230,100,steps=600)
            userName=i[0]
            name=i[1]
            imgData=ds.remodifyData(i[2],i[3],i[4])
            imgData=cv2.resize(imgData,(70,90))
            self.imgDict[userName]=gc.cvtIntoLabelImage(imgData)
            label=tk.Label(frame,width=70,height=90)
            label.config(image=self.imgDict[userName])
            label.place(x=5,y=5)

            label=tk.Label(frame,text=userName)
            label.place(x=100,y=5)

            label=tk.Label(frame,text=name)
            label.place(x=100,y=35)
            def funBlock():

                self.c.functionList['_friendRequestAccept']=self.handle
                self.c.friendRequestAccept(userName)
                self.refressList()


            btn=tk.Button(frame,text='Add Friend')
            btn.config(command=funBlock)


            btn.place(x=100,y=70)


            frame.pack()



    def handleFriendRequestLoad(self,msg):
        code=msg['code']
        self.refressList()
        if code=='ss01':
            self.labelStatus.config(text='No Data is found')
        elif code=='kks1':
            self.labelStatus.config(text='Data is founnded')
            data=ds.remodifyData(msg['usersData'],msg['usersType'],msg['usersShape'])

            self.importData(data)
        else:
            self.labelStatus.config(text='Error data loading')

    def handleFriendRequestAccept(self,msg):
        code=msg['code']

        if code=='0027':
            self.labelStatus.config(text='Friend Request Accept Successfull')

        else:
            self.labelStatus.config(text=code)

    def handle(self,msg):
        wType=msg['wType']

        if wType=='_loadFriendRequest':
            self.handleFriendRequestLoad(msg)
        elif wType=='_friendRequestAccept':
            self.handleFriendRequestAccept(msg)
        else:
            self.labelStatus.config(text='This is unknown option')

class UserProfile:

    def __init__(self,root,userName,c):
        self.root=root
        self.userName=userName
        self.c=c
        self.data=None
        btnWidth=12
        self.root.geometry('300x400')
        self.imgDict={}
        self.root.title('User Profile :-'+userName)
        mainFrame=tk.Frame(self.root,width=300,height=400,bg='red')

        topFrame=gf.GradientFrame(mainFrame,'#4AB54E','#6A71D8',width=300,height=400,steps=700)


        self.labelProfilePic=tk.Label(topFrame,width=120,height=160)
        self.labelProfilePic.place(x=30,y=30)





        self.imageLoc='_None'


        self.labelUserName=tk.Label(topFrame,text='UserName',font=self.getFont(10))
        self.labelUserName.place(x=170,y=30)



        self.labelName=tk.Label(topFrame,text='Name',font=self.getFont(10))
        self.labelName.place(x=170,y=70)

        self.labelIdentityU=tk.Label(topFrame,text='Identity U dklsjflsdklfsdlkfklsdflksdfks',font=self.getFont(10),wraplength=180)
        self.labelIdentityU.place(x=170,y=110)

        self.labelGender=tk.Label(topFrame,text='Gender',font=self.getFont(10))
        self.labelGender.place(x=170,y=170)

        self.labelContact=tk.Label(topFrame,text='Contact',font=self.getFont(10))
        self.labelContact.place(x=30,y=210)

        self.labelEmail=tk.Label(topFrame,text='Email',font=self.getFont(10))
        self.labelEmail.place(x=30,y=250)

        self.labelDob=tk.Label(topFrame,text='dob',font=self.getFont(10))
        self.labelDob.place(x=30,y=290)

        self.labelDiscription=tk.Label(topFrame,text='Discription',font=self.getFont(8),wraplength=300)
        self.labelDiscription.place(x=30,y=330)


        topFrame.place(x=0,y=0)
        mainFrame.place(x=0,y=0)

        self.root.protocol('WM_DELETE_WINDOW',self.onClose)
        self.loadData()

    def initData(self):
        name=self.data['name']
        userName=self.data['userName']
        profilePic=ds.remodifyData(self.data['profileData']\
                                   ,self.data['profileType'],self.data['profileShape'])
        profilePic=cv2.resize(profilePic,(120,160))
        img=gc.cvtIntoLabelImage(profilePic)
        self.imgDict[userName]=img
        identityU=self.data['identityU']
        gender=self.data['gender']
        contactNo=self.data['contactNo']
        email=self.data['email']
        dob=self.data['dateOfBirth']
        discription=self.data['discription']

        self.labelName.config(text=name)
        self.labelUserName.config(text=userName)
        self.labelProfilePic.config(image=self.imgDict[userName])

        if gender=='0':
            gender='male'
        elif gender=='1':
            gender='female'
        else:
            gender='other'
        self.labelGender.config(text='Gender :-'+gender)
        self.labelIdentityU.config(text=identityU)
        self.labelContact.config(text=contactNo)
        self.labelEmail.config(text=email)
        self.labelDob.config(text=dob)
        self.labelDiscription.config(text=discription)

    def loadData(self):
        window=self.userName+'userProfile'
        self.c.loadUserProfile(self.userName,window)
        self.c.functionList[window]=self.handle

    def handle(self,msg):
        self.data=msg
        self.initData()

    def onClose(self):
        MainWindow.openWindows[self.userName+'userProfile']=False
        self.root.destroy()

    def getFont(self,size):
        font="Helvetica {0}  ".format(size)
        return font

class ChatWindow:


    def __init__(self,root,c,data):
        self.root=root
        self.conditionChanged=False
        self.fuserName=None
        self.c=c
        self.initiate()
        self.root.title("Chat Window")
        self.onlineCond=False

        self.imgDict={}

        self.data=data
        self.userName=data[0]
        btnWidth=12

        self.root.geometry('700x500')
        self.root.protocol('WM_DELETE_WINDOW',self.onClose)

        mainFrame=tk.Frame(self.root,width=700,height=500,bg='red')

        Frame=gf.GradientFrame(mainFrame,'#D07835','#D035B6',width=700,height=500,steps=700)


        topFrame=gf.GradientFrame(Frame,'#D07835','#D035B6',width=700,height=100,steps=700)

        self.labelProfile=tk.Label(topFrame,height=5,width=10)
        self.labelProfile.place(x=10,y=10)

        self.labelName=tk.Label(topFrame,text='Name',font=self.getFont(15))
        self.labelName.place(x=130,y=10)

        self.labelUserName=tk.Label(topFrame,text='UserName',font=self.getFont(15))
        self.labelUserName.place(x=130,y=60)

        self.labelStatus=tk.Label(topFrame,text='Status',width=2,height=1)
        self.labelStatus.place(x=350,y=10)

        self.labelInfoStatus=tk.Label(topFrame,text='Info Status',font=self.getFont(10))
        self.labelInfoStatus.place(x=350,y=60)

        sideFrame=gf.GradientFrame(Frame,'#D07835','#D035B6',width=150,height=400,steps=700)

        self.btnTextFile=tk.Button(sideFrame,text='Text/File',font=self.getFont(10),width=btnWidth,command=self.funTextFile)
        self.btnTextFile.place(x=10,y=10)

        self.btnTextFile.config(bg='green')

        self.btnCamSound=tk.Button(sideFrame,text='Cam/Sound',font=self.getFont(10),width=btnWidth,command=self.funCamSound)
        self.btnCamSound.place(x=10,y=50)

        self.btnScreen=tk.Button(sideFrame,text='Screen',font=self.getFont(10),width=btnWidth,command=self.funScreen)
        self.btnScreen.place(x=10,y=90)

        self.btnKeyMou=tk.Button(sideFrame,text='Keyb./Mouse',font=self.getFont(10),width=btnWidth,command=self.funKeyMouse)
        self.btnKeyMou.place(x=10,y=130)

        self.btnKMD=tk.Button(sideFrame,text='Ke/Mo/Disp',font=self.getFont(10),width=btnWidth,command=self.funKeyMoScreen)
        self.btnKMD.place(x=10,y=170)

        self.btnControl=tk.Button(sideFrame,text='User Control',font=self.getFont(10),width=btnWidth,command=self.funUserControl)
        self.btnControl.place(x=10,y=250)


        self.varSScreen=tk.IntVar()
        self.varSCamera=tk.IntVar()
        self.varSSound=tk.IntVar()
        self.varSIntSound=tk.IntVar()
        self.varSKeyboard=tk.IntVar()
        self.varSMouse=tk.IntVar()

        self.varRScreen=tk.IntVar()
        self.varRCamera=tk.IntVar()
        self.varRSound=tk.IntVar()
        self.varRIntSound=tk.IntVar()
        self.varRKeyboard=tk.IntVar()
        self.varRMouse=tk.IntVar()




        rightFrame=gf.GradientFrame(Frame,'#D07835','#D035B6',width=550,height=400,steps=700)

        self.textFileFrame=tk.Frame(rightFrame,width=550,height=400)

        self.camSoundFrame=tk.Frame(rightFrame,width=550,height=400)

        self.ScreenFrame=tk.Frame(rightFrame,width=550,height=400)

        self.keyMouseFrame=tk.Frame(rightFrame,width=550,height=400)

        self.keyMoDispFrame=tk.Frame(rightFrame,width=550,height=400)

        self.userControlFrame=tk.Frame(rightFrame,width=550,height=400)

        #--------------------------------------------------------------
        self.textFileFrame1=gf.GradientFrame(self.textFileFrame,'#3559D0','#35B1D0',width=550,height=400,steps=700)



        self.frameChat1=gf.GradientFrame(self.textFileFrame1,'#66571B','#5BC9DA',width=250,height=300,steps=300)
        self.frameChat1.place(x=30,y=10)

        self.frameChat=gf.GradientFrame(self.frameChat1,'#66571B','#5BC9DA',width=250,height=300,steps=300)
        self.frameChat.place(x=0,y=0)

        self.frameChatSt,self.chatCont=gc.scrollableFrame(self.frameChat,cwidth=230,cheight=280)

        self.varEntryText=tk.StringVar()
        self.file2Send=None

        entryText=tk.Entry(self.textFileFrame1,textvariable=self.varEntryText,width=22,font=self.getFont(12))
        entryText.place(x=30,y=320)

        btnSendText=tk.Button(self.textFileFrame1,text='Send',font=self.getFont(9),command=self.funSendChat)
        btnSendText.place(x=245,y=320)

        btnSetFile=tk.Button(self.textFileFrame1,text='Set File',font=self.getFont(9),command=self.funSetFile)
        btnSetFile.place(x=30,y=360)

        btnSendFile=tk.Button(self.textFileFrame1,text='Send File',font=self.getFont(9),command=self.funSendFile)
        btnSendFile.place(x=130,y=360)

        #-----------------------------------------------------------------------
        self.camSoundFrame1=gf.GradientFrame(self.camSoundFrame,'#D07835','#35D06E',width=550,height=400,steps=700)

        labelCameraStatusSent=tk.Label(self.camSoundFrame1,text='Sent Camera',font=self.getFont(10),bg='yellow')
        labelCameraStatusSent.place(x=30,y=30)

        self.labelSentCamera=tk.Label(self.camSoundFrame1,width=20,height=10)
        self.labelSentCamera.place(x=30,y=60)

        sentCameraRad1=tk.Radiobutton(self.camSoundFrame1,text='On',variable=self.varSCamera,value=1,command=self.funSendCamera)
        sentCameraRad1.place(x=30,y=230)

        sentCameraRad2=tk.Radiobutton(self.camSoundFrame1,text='Off',variable=self.varSCamera,value=0,command=self.funSendCamera)
        sentCameraRad2.place(x=90,y=230)



        self.labelRecvCamera=tk.Label(self.camSoundFrame1,width=20,height=10)
        self.labelRecvCamera.place(x=300,y=60)

        labelCameraStatusRecv=tk.Label(self.camSoundFrame1,text='Recv Camera',font=self.getFont(10),bg='yellow')
        labelCameraStatusRecv.place(x=300,y=30)

        recvCameraRad1=tk.Radiobutton(self.camSoundFrame1,text='On',variable=self.varRCamera,value=1,command=self.funRecvCamera)
        recvCameraRad1.place(x=300,y=230)

        recvCameraRad2=tk.Radiobutton(self.camSoundFrame1,text='Off',variable=self.varRCamera,value=0,command=self.funRecvCamera)
        recvCameraRad2.place(x=360,y=230)


        labelSoundStatus=tk.Label(self.camSoundFrame1,text='Sound Settings',font=self.getFont(10),bg='red')
        labelSoundStatus.place(x=30,y=280)

        labelSentSound=tk.Label(self.camSoundFrame1,text='Send Sound',font=self.getFont(10),bg='yellow')
        labelSentSound.place(x=30,y=310)

        sentSoundRad1=tk.Radiobutton(self.camSoundFrame1,text='On',variable=self.varSSound,value=1,command=self.funSendSound)
        sentSoundRad1.place(x=30,y=340)

        sentSoundRad2=tk.Radiobutton(self.camSoundFrame1,text='Off',variable=self.varSSound,value=0,command=self.funSendSound)
        sentSoundRad2.place(x=90,y=340)

        labelRecvSound=tk.Label(self.camSoundFrame1,text='Recv Sound',font=self.getFont(10),bg='yellow')
        labelRecvSound.place(x=300,y=310)

        recvSoundRad1=tk.Radiobutton(self.camSoundFrame1,text='On',variable=self.varRSound,value=1,command=self.funRecvSound)
        recvSoundRad1.place(x=300,y=340)

        recvSoundRad2=tk.Radiobutton(self.camSoundFrame1,text='Off',variable=self.varRSound,value=0,command=self.funRecvSound)
        recvSoundRad2.place(x=390,y=340)


        #------------------------------------------------------------------------
        self.ScreenFrame1=gf.GradientFrame(self.ScreenFrame,'#35B1D0','#35D073',width=550,height=400,steps=700)


        self.labelRecvScreen=tk.Label(self.ScreenFrame1,width=50,height=17)
        self.labelRecvScreen.place(x=10,y=10)

        labelRecvScreenStatus=tk.Label(self.ScreenFrame1,text='Recv Screen Settings',font=self.getFont(10),bg='yellow')
        labelRecvScreenStatus.place(x=10,y=310)

        #jksdlfkjsdflsdjkflsdjflksdfjsldfksdfkjlsdfkdskk----------------------------------------------------
        recvScreenRad1=tk.Radiobutton(self.ScreenFrame1,text='On',variable=self.varRScreen,value=1,command=self.funRecvScreen)
        recvScreenRad1.place(x=10,y=340)

        recvScreenRad2=tk.Radiobutton(self.ScreenFrame1,text='Off',variable=self.varRScreen,value=0,command=self.funRecvScreen)
        recvScreenRad2.place(x=70,y=340)




        labelSentScreenStatus=tk.Label(self.ScreenFrame1,text='Sent Screen Settings',font=self.getFont(10),bg='yellow')
        labelSentScreenStatus.place(x=360,y=205)

        sentScreenRad1=tk.Radiobutton(self.ScreenFrame1,text='On',variable=self.varSScreen,value=1,command=self.funSendScreen)
        sentScreenRad1.place(x=360,y=245)

        sentScreenRad2=tk.Radiobutton(self.ScreenFrame1,text='Off',variable=self.varSScreen,value=0,command=self.funSendScreen)
        sentScreenRad2.place(x=430,y=245)

        self.labelSentScreen=tk.Label(self.ScreenFrame1,width=23,height=8)
        self.labelSentScreen.place(x=360,y=275)
        #-----------------------------------------------------------------------
        self.keyMouseFrame1=gf.GradientFrame(self.keyMouseFrame,'#D07835','#3569D0',width=550,height=400,steps=700)

        labelSentKeyboardStatus=tk.Label(self.keyMouseFrame1,text='Send Keyboard',font=self.getFont(10),bg='yellow')
        labelSentKeyboardStatus.place(x=30,y=30)

        sentKeyboardRad1=tk.Radiobutton(self.keyMouseFrame1,text='On',variable=self.varSKeyboard,value=1,command=self.funSendKeyboard)
        sentKeyboardRad1.place(x=30,y=70)

        sentKeyboardRad2=tk.Radiobutton(self.keyMouseFrame1,text='Off',variable=self.varSKeyboard,value=0,command=self.funSendKeyboard)
        sentKeyboardRad2.place(x=90,y=70)

        self.labelSentKeyboardInfo=tk.Label(self.keyMouseFrame1,text='Data',font=self.getFont(10),wraplength=100)
        self.labelSentKeyboardInfo.place(x=30,y=110)



        labelSentMouseStatus=tk.Label(self.keyMouseFrame1,text='Send Mouse',font=self.getFont(10),bg='yellow')
        labelSentMouseStatus.place(x=300,y=30)

        sentMouseRad1=tk.Radiobutton(self.keyMouseFrame1,text='On',variable=self.varSMouse,value=1,command=self.funSendMouse)
        sentMouseRad1.place(x=300,y=70)

        sentMouseRad2=tk.Radiobutton(self.keyMouseFrame1,text='Off',variable=self.varSMouse,value=0,command=self.funSendMouse)
        sentMouseRad2.place(x=360,y=70)

        self.labelSentMouseInfo=tk.Label(self.keyMouseFrame1,text='Data',font=self.getFont(10),wraplength=100)
        self.labelSentMouseInfo.place(x=300,y=110)


        #0x-----------------------------------

        labelRecvKeyboardStatus=tk.Label(self.keyMouseFrame1,text='Recv Keyboard',font=self.getFont(10),bg='yellow')
        labelRecvKeyboardStatus.place(x=30,y=190)

        recvKeyboardRad1=tk.Radiobutton(self.keyMouseFrame1,text='On',variable=self.varRKeyboard,value=1,command=self.funRecvKeyboard)
        recvKeyboardRad1.place(x=30,y=230)

        recvKeyboardRad2=tk.Radiobutton(self.keyMouseFrame1,text='Off',variable=self.varRKeyboard,value=0,command=self.funRecvKeyboard)
        recvKeyboardRad2.place(x=90,y=230)

        self.labelRecvKeyboardInfo=tk.Label(self.keyMouseFrame1,text='Data',font=self.getFont(10),wraplength=100)
        self.labelRecvKeyboardInfo.place(x=30,y=270)



        labelRecvMouseStatus=tk.Label(self.keyMouseFrame1,text='Recv Mouse',font=self.getFont(10),bg='yellow')
        labelRecvMouseStatus.place(x=300,y=190)

        recvMouseRad1=tk.Radiobutton(self.keyMouseFrame1,text='On',variable=self.varRMouse,value=1,command=self.funRecvMouse)
        recvMouseRad1.place(x=300,y=230)

        recvMouseRad2=tk.Radiobutton(self.keyMouseFrame1,text='Off',variable=self.varRMouse,value=0,command=self.funRecvMouse)
        recvMouseRad2.place(x=360,y=230)

        self.labelRecvMouseInfo=tk.Label(self.keyMouseFrame1,text='Data',font=self.getFont(10),wraplength=100)
        self.labelRecvMouseInfo.place(x=300,y=270)


        labelCondStatus=tk.Label(self.keyMouseFrame1,text='Press "Ctrl+t" to off sending mouse and keyboard data \n \
        and Press "Alt+t" to off recieving mouse and keyboard data ',font=self.getFont(10),bg='red')
        labelCondStatus.place(x=30,y=330)

        #-------------------------------------------------------------------------
        self.keyMoDispFrame1=gf.GradientFrame(self.keyMoDispFrame,'#8DD035','#35D073',width=550,height=400,steps=700)

        labelRecvScreenInfo1=tk.Label(self.keyMoDispFrame1,text='Recv Screen',font=self.getFont(10),bg='yellow')
        labelRecvScreenInfo1.place(x=10,y=10)

        recvScreenRad11=tk.Radiobutton(self.keyMoDispFrame1,text='On',variable=self.varRScreen,value=1,command=self.funRecvScreen)
        recvScreenRad11.place(x=150,y=10)

        recvScreenRad12=tk.Radiobutton(self.keyMoDispFrame1,text='Off',variable=self.varRScreen,value=0,command=self.funRecvScreen)
        recvScreenRad12.place(x=210,y=10)

        self.labelRecvScreenData=tk.Label(self.keyMoDispFrame1,width=70,height=18)
        self.labelRecvScreenData.place(x=10,y=40)

        #----
        labelSentKeyboardStatus=tk.Label(self.keyMoDispFrame1,text='Send Keyboard',font=self.getFont(10),bg='yellow')
        labelSentKeyboardStatus.place(x=30,y=320)

        sentKeyboardRad1=tk.Radiobutton(self.keyMoDispFrame1,text='On',variable=self.varSKeyboard,value=1,command=self.funSendKeyboard)
        sentKeyboardRad1.place(x=30,y=345)

        sentKeyboardRad2=tk.Radiobutton(self.keyMoDispFrame1,text='Off',variable=self.varSKeyboard,value=0,command=self.funSendKeyboard)
        sentKeyboardRad2.place(x=90,y=345)

        self.labelSentKeyboardInfo1=tk.Label(self.keyMoDispFrame1,text='Data',font=self.getFont(10),wraplength=100)
        self.labelSentKeyboardInfo1.place(x=30,y=375)



        labelSentMouseStatus=tk.Label(self.keyMoDispFrame1,text='Send Mouse',font=self.getFont(10),bg='yellow')
        labelSentMouseStatus.place(x=300,y=320)

        sentMouseRad1=tk.Radiobutton(self.keyMoDispFrame1,text='On',variable=self.varSMouse,value=1,command=self.funSendMouse)
        sentMouseRad1.place(x=300,y=345)

        sentMouseRad2=tk.Radiobutton(self.keyMoDispFrame1,text='Off',variable=self.varSMouse,value=0,command=self.funSendMouse)
        sentMouseRad2.place(x=360,y=345)

        self.labelSentMouseInfo1=tk.Label(self.keyMoDispFrame1,text='Data',font=self.getFont(10),wraplength=100)
        self.labelSentMouseInfo1.place(x=300,y=375)


        #-------------------------------------------------------------------------
        self.userControlFrame1=gf.GradientFrame(self.userControlFrame,'#35D073','#894224',width=550,height=400,steps=700)

        labelLeftSending=tk.Label(self.userControlFrame1,text='Sending Control',bg='yellow',font=self.getFont(10))
        labelLeftSending.place(x=200,y=10)

        labelRightReciving=tk.Label(self.userControlFrame1,text='Reciving Control',bg='yellow',font=self.getFont(10))
        labelRightReciving.place(x=400,y=10)
        #------------------
        labelCameraStat=tk.Label(self.userControlFrame1,text='Camera',bg='red',font=self.getFont(10))
        labelCameraStat.place(x=30,y=60)

        radSendCam1=tk.Radiobutton(self.userControlFrame1,text='On',variable=self.varSCamera,value=1,command=self.funSendCamera)
        radSendCam1.place(x=200,y=60)

        radSendCam2=tk.Radiobutton(self.userControlFrame1,text='Off',variable=self.varSCamera,value=0,command=self.funSendCamera)
        radSendCam2.place(x=260,y=60)

        btnRequestCam=tk.Button(self.userControlFrame1,text='Request',font=self.getFont(9),bg='blue',command=self.funRequestCam)
        btnRequestCam.place(x=315,y=60)

        radRecvCam1=tk.Radiobutton(self.userControlFrame1,text='On',variable=self.varRCamera,value=1,command=self.funRecvCamera)
        radRecvCam1.place(x=400,y=60)

        radRecvCam2=tk.Radiobutton(self.userControlFrame1,text='Off',variable=self.varRCamera,value=0,command=self.funRecvCamera)
        radRecvCam2.place(x=460,y=60)

        #----
        labelSoundStat=tk.Label(self.userControlFrame1,text='Sound',bg='red',font=self.getFont(10))
        labelSoundStat.place(x=30,y=110)

        radSendSound1=tk.Radiobutton(self.userControlFrame1,text='On',variable=self.varSSound,value=1,command=self.funSendSound)
        radSendSound1.place(x=200,y=110)

        radSendSound2=tk.Radiobutton(self.userControlFrame1,text='Off',variable=self.varSSound,value=0,command=self.funSendSound)
        radSendSound2.place(x=260,y=110)


        btnRequestSound=tk.Button(self.userControlFrame1,text='Request',font=self.getFont(9),bg='blue',command=self.funRequestSound)
        btnRequestSound.place(x=315,y=110)

        radRecvSound1=tk.Radiobutton(self.userControlFrame1,text='On',variable=self.varRSound,value=1,command=self.funRecvSound)
        radRecvSound1.place(x=400,y=110)

        radRecvSound2=tk.Radiobutton(self.userControlFrame1,text='Off',variable=self.varRSound,value=0,command=self.funRecvSound)
        radRecvSound2.place(x=460,y=110)

        #-----------------
        labelIntSound=tk.Label(self.userControlFrame1,text='Int Sound',bg='red',font=self.getFont(10))
        labelIntSound.place(x=30,y=160)

        radSendIntSound1=tk.Radiobutton(self.userControlFrame1,text='On',variable=self.varSIntSound,value=1,command=self.funSendIntSound)
        radSendIntSound1.place(x=200,y=160)

        radSendIntSound2=tk.Radiobutton(self.userControlFrame1,text='Off',variable=self.varSIntSound,value=0,command=self.funSendIntSound)
        radSendIntSound2.place(x=260,y=160)


        btnRequestIntSound=tk.Button(self.userControlFrame1,text='Request',font=self.getFont(9),bg='blue',command=self.funRequestIntSound)
        btnRequestIntSound.place(x=315,y=160)

        radRecvIntSound1=tk.Radiobutton(self.userControlFrame1,text='On',variable=self.varRIntSound,value=1,command=self.funRecvIntSound)
        radRecvIntSound1.place(x=400,y=160)

        radRecvIntSound2=tk.Radiobutton(self.userControlFrame1,text='Off',variable=self.varRIntSound,value=0,command=self.funRecvIntSound)
        radRecvIntSound2.place(x=460,y=160)

        #-----------------------------
        labelKeyboardStat=tk.Label(self.userControlFrame1,text='Keyboard',bg='red',font=self.getFont(10))
        labelKeyboardStat.place(x=30,y=210)

        radSendKeyboard1=tk.Radiobutton(self.userControlFrame1,text='On',variable=self.varSKeyboard,value=1,command=self.funSendKeyboard)
        radSendKeyboard1.place(x=200,y=210)


        radSendKeyboard2=tk.Radiobutton(self.userControlFrame1,text='Off',variable=self.varSKeyboard,value=0,command=self.funSendKeyboard)
        radSendKeyboard2.place(x=260,y=210)


        btnRequestKeyboard=tk.Button(self.userControlFrame1,text='Request',font=self.getFont(9),bg='blue',command=self.funRequestKeyboard)
        btnRequestKeyboard.place(x=315,y=210)

        radRecvKeyboard1=tk.Radiobutton(self.userControlFrame1,text='On',variable=self.varRKeyboard,value=1,command=self.funRecvKeyboard)
        radRecvKeyboard1.place(x=400,y=210)

        radRecvKeyboard2=tk.Radiobutton(self.userControlFrame1,text='Off',variable=self.varRKeyboard,value=0,command=self.funRecvKeyboard)
        radRecvKeyboard2.place(x=460,y=210)

        #-------------------
        labelMouseStat=tk.Label(self.userControlFrame1,text='Mouse',bg='red',font=self.getFont(10))
        labelMouseStat.place(x=30,y=260)

        radSendMouse1=tk.Radiobutton(self.userControlFrame1,text='On',variable=self.varSMouse,value=1,command=self.funSendMouse)
        radSendMouse1.place(x=200,y=260)

        radSendMouse2=tk.Radiobutton(self.userControlFrame1,text='Off',variable=self.varSMouse,value=0,command=self.funSendMouse)
        radSendMouse2.place(x=260,y=260)


        btnRequestMouse=tk.Button(self.userControlFrame1,text='Request',font=self.getFont(9),bg='blue',command=self.funRequestMouse)
        btnRequestMouse.place(x=315,y=260)

        radRecvMouse1=tk.Radiobutton(self.userControlFrame1,text='On',variable=self.varRMouse,value=1,command=self.funRecvMouse)
        radRecvMouse1.place(x=400,y=260)

        radRecvMouse2=tk.Radiobutton(self.userControlFrame1,text='Off',variable=self.varRMouse,value=0,command=self.funRecvMouse)
        radRecvMouse2.place(x=460,y=260)

        #--------------------------------------------------------------

        labelScreenStat=tk.Label(self.userControlFrame1,text='Screen',bg='red',font=self.getFont(10))
        labelScreenStat.place(x=30,y=310)

        radSendScreen1=tk.Radiobutton(self.userControlFrame1,text='On',variable=self.varSScreen,value=1,command=self.funSendScreen)
        radSendScreen1.place(x=200,y=310)

        radSendScreen2=tk.Radiobutton(self.userControlFrame1,text='Off',variable=self.varSScreen,value=0,command=self.funSendScreen)
        radSendScreen2.place(x=260,y=310)


        btnRequestScreen=tk.Button(self.userControlFrame1,text='Request',font=self.getFont(9),bg='blue',command=self.funRequestScreen)
        btnRequestScreen.place(x=315,y=310)

        radRecvScreen1=tk.Radiobutton(self.userControlFrame1,text='On',variable=self.varRScreen,value=1,command=self.funRecvScreen)
        radRecvScreen1.place(x=400,y=310)

        radRecvScreen2=tk.Radiobutton(self.userControlFrame1,text='Off',variable=self.varRScreen,value=0,command=self.funRecvScreen)
        radRecvScreen2.place(x=460,y=310)



        #lsentScreenRad1=

        #---------------x----------------------x--------------o-----------
        self.textFileFrame1.place(x=0,y=0)
        self.camSoundFrame1.place(x=0,y=0)
        self.ScreenFrame1.place(x=0,y=0)
        self.keyMouseFrame1.place(x=0,y=0)
        self.keyMoDispFrame1.place(x=0,y=0)
        self.userControlFrame1.place(x=0,y=0)

        self.textFileFrame.place(x=0,y=0)
        self.camSoundFrame.place(x=0,y=0)
        self.ScreenFrame.place(x=0,y=0)
        self.keyMouseFrame.place(x=0,y=0)
        self.keyMoDispFrame.place(x=0,y=0)
        self.userControlFrame.place(x=0,y=0)
        #x=150, y=100

        topFrame.place(x=0,y=0)
        sideFrame.place(x=0,y=100)
        rightFrame.place(x=150,y=100)
        Frame.place(x=0,y=0)
        mainFrame.place(x=0,y=0)





        self.funTextFile()
        self.assImpData()
        self.atLastInitiate()
        self.refress()

    def initiate(self):
        self.previousKeys={}
        self.imgCounter={'camera':0,'screen':0}

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
        self.labelSentKeyboardInfo.config(text=data)
        self.labelSentKeyboardInfo1.config(text=data)

    def funOnKeyRelease(self,data):
        self.labelSentKeyboardInfo.config(text=data)
        self.labelSentKeyboardInfo1.config(text=data)

    def funOnMouseMove(self,data):
        self.labelSentMouseInfo.config(text=data)
        self.labelSentMouseInfo1.config(text=data)

    def funOnMouseClick(self,data):
        self.labelSentMouseInfo.config(text=data)
        self.labelSentMouseInfo1.config(text=data)


    def funOnMouseScroll(self,data):
        self.labelSentMouseInfo.config(text=data)
        self.labelSentMouseInfo1.config(text=data)



    def sendCamera(self):
        self.c._Camera(self.fuserName,'@none','@none','@none')

    def sendScreen(self):
        self.c._Screen(self.fuserName,'@none','@none','@none')

    def sendSound(self):
        self.c._Sound(self.fuserName,'@none')

    def sendIntSound(self):
        self.c._IntSound(self.fuserName,'@none')

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

    def onClose(self):
        #print(MainWindow.openWindows)
        MainWindow.openWindows[self.userName+'chatWindow']=False
        #print(MainWindow.openWindows)
        self.c.loadChatWindow(self.userName,status='unload')
        self.root.destroy()

    def assImpData(self):
        i=self.data
        userName=i[0]
        self.fuserName=userName
        name=i[1]
        imgData=ds.remodifyData(i[2],i[3],i[4])
        cond=i[5]

        self.labelUserName.config(text=userName)
        self.labelName.config(text=name)
        imgData=cv2.resize(imgData,(70,90))
        self.imgDict[userName]=gc.cvtIntoLabelImage(imgData)
        #label=tk.Label(frame,width=70,height=90)
        self.labelProfile.config(width=70)
        self.labelProfile.config(height=90)
        self.labelProfile.config(image=self.imgDict[userName])

        self.labelStatus.config(text='')
        if cond=='True':
            self.labelStatus.config(bg='green')
        else:
            self.labelStatus.config(bg='red')

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

        data=self.varEntryText.get()
        if data=='':
            pass
        else:
            self.varEntryText.set('')

            data=self.c.userName+'->'+data

            self.formatChatText(data)


            self.c._Text(self.userName,data)

    def formatChatText(self,data,type='Chat'):
        frame=gf.GradientFrame(self.frameChatSt,'#58A928','#28A9A1',230,50,steps=600)
        label=tk.Label(frame,text=data,font=self.getFont(7))

        label.place(x=10,y=10)
        if type!='Chat':
            label.config(bg='red')

        frame.pack()
        self.chatCont.yview_moveto(1)


    def funSetFile(self):
        f=tk.filedialog.askopenfilename()

        if f==None or f=='':
            self.file2Send=None
        else:
            self.file2Send=f


    def sendFileFunction(self,args,tempSize,size,cond=False):
        cond2=args[-1]
        try:
            if cond2:
                if not  cond:
                    progress=args[0]
                    labelSizeStatus=args[1]
                    pr=int(tempSize/size*100)
                    progress['value']=pr
                    #print(progress['value'])
                    frame=args[2]
                    frame.update_idletasks()
                    d=round(tempSize/size*100,3)
                    labelSizeStatus.config(text=d)

                else:
                    labelSizeStatus=args[1]
                    labelSizeStatus.config(text='Completed')
                    frame=args[2]
                    fName=args[-1]
                    btnCancel=args[3]
                    self.c._File(self.userName,fName,'end')

                    btnCancel.destroy()
                    frame.config(height=80)
        except:
            print("This is blunder mistake in sending the data")

    def funSendFile(self):
        if self.file2Send==None:
            pass
        else:
            fName=self.file2Send
            self.file2Send=None
            data=self.userName+'->'+fName
            frame=gf.GradientFrame(self.frameChatSt,'#58A928','#28A9A1',230,120,steps=600)
            labelText=tk.Label(frame,text=data,font=self.getFont(7))

            labelText.place(x=10,y=10)

            progress = ttk.Progressbar(frame, orient = tk.HORIZONTAL,
              length = 100, mode = 'determinate')
            progress.place(x=10,y=50)
            #progress['value'] = 20
            labelSizeStatus=tk.Label(frame,text='0/0 mb')
            labelSizeStatus.place(x=130,y=50)


            btnCancel=tk.Button(frame,text='Cancel')
            btnCancel.place(x=180,y=90)
            args=[progress,labelSizeStatus,frame,btnCancel]
            tfName={}


            self.c.send.send_file(fName,function=self.sendFileFunction,args=args,tfs=tfName,chunk=1024)
            frame.pack()


            def funCancel():
                for i in tfName:
                    tf=tfName[i];
                fName=tf
                self.c.send.fileFlow[fName]=False
                frame.destroy()

            btnCancel.config(command=funCancel)

            self.chatCont.yview_moveto(1)

    def handle(self,msg):

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
            self.labelInfoStatus.config('Error Code')

    def handleText(self,msg):
        data=msg['chatText']
        data=ds.dec(data)
        #print(data)
        dType,val=ad.deAssValue(data,True)
        chat=ds.dec(val['chat'])

        self.formatChatText(chat)

    def handleFile(self,msg):
        data=msg['chatFile']
        data=ds.dec(data)
        #print(data)
        dType,val=ad.deAssValue(data,True)
        chat=ds.dec(val['name'])

        self.formatChatText(chat,'File')

    def handleSound(self,msg):
        code=msg['code']

        if code=='d201':
            cond=self.varRSound.get()

            if cond==1:
                #print("HELLO")
                data=msg['data']
                data=ds.decb(bytes(data,'utf-8'))
                stream.write(data)

    def handleIntSound(self,msg):
        code=msg['code']

        if code=='d201':
            cond=self.varRSound.get()

            if cond==1:
                #print("HELLO")
                data=msg['data']
                data=ds.decb(bytes(data,'utf-8'))
                stream2.write(data)

    def handleCamera(self,msg):
        code=msg['code']
        val=self.imgCounter['camera']
        if 'cameraR' in self.imgCounter:

            count=self.imgCounter['cameraR']
        else:
            self.imgCounter['cameraR']=0
            count=0

        if code=='d201':
            cond=self.varRCamera.get()
            if cond==1:
                data=ds.remodifyData(msg['data'],msg['types'],msg['shape'])
                self.labelRecvCamera.config(width=180)
                self.labelRecvCamera.config(height=150)

                data=cv2.cvtColor(data,cv2.COLOR_BGR2RGB)
                data=cv2.resize(data,(180,150))
                lb=gc.cvtIntoLabelImage(data)

                count=count+1

                self.imgDict['cameraR_'+self.userName+str(count)]=lb


                self.labelRecvCamera.config(image=self.imgDict['cameraR_'+self.userName+str(count)])

                if count%2==0:

                    self.imgCounter['cameraR']=0
                else:
                    self.imgCounter['cameraR']=count

    def handleScreen(self,msg):
        code=msg['code']
        val=self.imgCounter['screen']
        if 'screenR' in self.imgCounter:

            count=self.imgCounter['screenR']
        else:
            self.imgCounter['screenR']=0
            count=0

        if code=='d201':
            cond=self.varRScreen.get()
            if cond==1:
                data=ds.remodifyData(msg['data'],msg['types'],msg['shape'])
                if not self.conditionChanged:
                    self.labelRecvScreenData.config(width=540)
                    self.labelRecvScreenData.config(height=330)
                    self.conditionChanged=True

                self.labelRecvScreen.config(width=450)
                self.labelRecvScreen.config(height=275)



                data=cv2.cvtColor(data,cv2.COLOR_BGR2RGB)
                d2=data.copy()
                data1=cv2.resize(d2,(450,275))

                lb=gc.cvtIntoLabelImage(data)
                lb2=gc.cvtIntoLabelImage(data1)
                count=count+1

                self.imgDict['screenR_'+self.userName+'_'+str(count)]=lb2
                self.imgDict['screenR1_'+self.userName+'_'+str(count)]=lb


                self.labelRecvScreen.config(image=self.imgDict['screenR_'+self.userName+'_'+str(count)])
                self.labelRecvScreenData.config(image=self.imgDict['screenR1_'+self.userName+'_'+str(count)])

                if count%2==0:

                    self.imgCounter['screenR']=0
                else:
                    self.imgCounter['screenR']=count


    def handleMouse(self,msg):
        code=msg['code']

        if code=='d201':
            cond=self.varRMouse.get()

            if cond==1:
                data=ds.remodifyData(msg['data'],msg['types'],msg['shape'])
                print(data)
                for i in data:
                    mous.response(i)

    def handleKeyboard(self,msg):
        code=msg['code']

        if code=='d201':
            cond=self.varRKeyboard.get()
            if cond==1:
                data=ds.remodifyData(msg['data'],msg['types'],msg['shape'])
                print(data)
                for i in data:
                    keyb.response(i)

    def handleOnlineStatus(self,msg):
        status=msg['status']

        if status=='False':
            self.labelStatus.config(bg='red')
        else:
            self.labelStatus.config(bg='green')

    def handleChat(self,msg):
        code=msg['code']

        if code=='se01':
            self.labelInfoStatus.config(text='No Chat Found')
        elif code=='00sk':
            self.labelInfoStatus.config(text='Chat Found')

            data=ds.remodifyData(msg['loadChat'],msg['chatType'],msg['chatShape'])

            for i in data:
                #print(i)
                index=i[0]
                dType,val=ad.deAssValue(i[1],True)
                chat=val['chat']
                sender=val['sender']
                recever=val['recever']

                chat=ds.dec(chat)

                self.formatChatText(chat)

        else:
            self.labelInfoStatus.config(text=code+' error')
        self.setFormalities()

    def showSendCamera(self):
        self.labelSentCamera.config(width=180)
        self.labelSentCamera.config(height=150)
        def fun():
            count=0
            while self.varSCamera.get()==1:
                frame=con.camFrame
                count=count+1
                if frame is None:
                    pass
                else:
                    frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

                    frame=cv2.resize(frame,(180,150))
                    frame=gc.cvtIntoLabelImage(frame)

                    self.imgDict['cam_'+self.userName+str(count)]=frame
                    self.labelSentCamera.config(image=self.imgDict['cam_'+self.userName+str(count)])
                if count%2==0:
                    count=0

        threading.Thread(target=fun).start()

    def showSendScreen(self):
        self.labelSentScreen.config(width=180)
        self.labelSentScreen.config(height=110)
        def fun():
            count=0
            while self.varSScreen.get()==1:
                frame=con.screenFrame
                count=count+1
                if frame is None:
                    pass
                else:
                    #frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

                    frame=cv2.resize(frame,(180,110))
                    frame=gc.cvtIntoLabelImage(frame)

                    self.imgDict['scr_'+self.userName+str(count)]=frame
                    self.labelSentScreen.config(image=self.imgDict['scr_'+self.userName+str(count)])
                if count%2==0:
                    count=0

        threading.Thread(target=fun).start()

    def funSendCamera(self):
        userName=self.userName
        conType='sCamera'
        conValue=str(self.varSCamera.get())
        if 'camera' in self.previousKeys:
            val=self.previousKeys['camera']
            if val==conValue:
                pass
            else:
                if conValue=='1':
                    MainWindow.xprtControl.funFirstOnList['camera']=self.sendCamera
                    MainWindow.xprtControl.funOnSending(self.fuserName,'camera')
                    self.showSendCamera()
                else:
                    MainWindow.xprtControl.funOffSending(self.fuserName,'camera')
        else:
            if conValue=='1':
                MainWindow.xprtControl.funFirstOnList['camera']=self.sendCamera
                MainWindow.xprtControl.funOnSending(self.fuserName,'camera')
                self.showSendCamera()
            else:
                MainWindow.xprtControl.funOffSending(self.fuserName,'camera')

        self.previousKeys['camera']=conValue
        self.c.updateControls(userName,conType,conValue)
        #self.c.functionList[self.userName.lower()+'_updateControls']=self.handle


    def setOnlineCond(self,cond):
        self.onlineCond=cond

    def funRecvCamera(self):
        userName=self.userName
        conType='rCamera'
        conValue=str(self.varRCamera.get())

        self.c.updateControls(userName,conType,conValue)


    def funSendSound(self):
        userName=self.userName
        conType='sSound'
        conValue=str(self.varSSound.get())
        if conValue=='1':
            MainWindow.xprtControl.funFirstOnList['sound']=self.sendSound
            MainWindow.xprtControl.funOnSending(self.fuserName,'sound')
        else:
            MainWindow.xprtControl.funOffSending(self.fuserName,'sound')

        self.c.updateControls(userName,conType,conValue)


    def funRecvSound(self):
        userName=self.userName
        conType='rSound'
        conValue=str(self.varRSound.get())

        self.c.updateControls(userName,conType,conValue)



    def funSendIntSound(self):
        userName=self.userName
        conType='sIntSound'
        conValue=str(self.varSIntSound.get())
        if conValue=='1':
            MainWindow.xprtControl.funFirstOnList['IntSound']=self.sendIntSound
            MainWindow.xprtControl.funOnSending(self.fuserName,'IntSound')
        else:
            MainWindow.xprtControl.funOffSending(self.fuserName,'IntSound')

        self.c.updateControls(userName,conType,conValue)


    def funRecvIntSound(self):
        userName=self.userName
        conType='rIntSound'
        conValue=str(self.varRIntSound.get())

        self.c.updateControls(userName,conType,conValue)


    def funSendKeyboard(self):
        userName=self.userName
        conType='sKeyboard'
        conValue=str(self.varSKeyboard.get())
        if conValue=='1':
            MainWindow.xprtControl.funFirstOnList['keyboard']=self.sendKeyboard
            MainWindow.xprtControl.funOnSending(self.fuserName,'keyboard')
        else:
            MainWindow.xprtControl.funOffSending(self.fuserName,'keyboard')
            self.disableKeyboardSending()

        self.c.updateControls(userName,conType,conValue)


    def funRecvKeyboard(self):
        userName=self.userName
        conType='rKeyboard'
        conValue=str(self.varRKeyboard.get())

        self.c.updateControls(userName,conType,conValue)

    #I love you
    #i miss you
    #i want to meet you
    #But i dont know you also want same or not

    def funSendMouse(self):
        userName=self.userName
        conType='sMouse'
        conValue=str(self.varSMouse.get())
        if conValue=='1':
            MainWindow.xprtControl.funFirstOnList['mouse']=self.sendMouse
            MainWindow.xprtControl.funOnSending(self.fuserName,'mouse')
        else:
            MainWindow.xprtControl.funOffSending(self.fuserName,'mouse')
            self.disableMouseSending()

        self.c.updateControls(userName,conType,conValue)


    def funRecvMouse(self):
        userName=self.userName
        conType='rMouse'
        conValue=str(self.varRMouse.get())

        self.c.updateControls(userName,conType,conValue)


    def funSendScreen(self):
        userName=self.userName
        conType='sScreen'
        conValue=str(self.varSScreen.get())
        if 'screen' in self.previousKeys:
            val=self.previousKeys['screen']
            if val==conValue:
                pass
            else:
                if conValue=='1':
                    MainWindow.xprtControl.funFirstOnList['screen']=self.sendScreen
                    MainWindow.xprtControl.funOnSending(self.fuserName,'screen')
                    self.showSendScreen()
                else:
                    MainWindow.xprtControl.funOffSending(self.fuserName,'screen')
        else:
            if conValue=='1':
                MainWindow.xprtControl.funFirstOnList['screen']=self.sendScreen
                MainWindow.xprtControl.funOnSending(self.fuserName,'screen')
                self.showSendScreen()
            else:
                MainWindow.xprtControl.funOffSending(self.fuserName,'screen')

        self.previousKeys['screen']=conValue
        self.c.updateControls(userName,conType,conValue)


    def funRecvScreen(self):
        userName=self.userName
        conType='rScreen'
        conValue=str(self.varRScreen.get())

        self.c.updateControls(userName,conType,conValue)



    def funRequestCam(self):
        vType='camera'
        self.c.rRequest(self.fuserName,vType)

    def funRequestSound(self):
        vType='sound'
        self.c.rRequest(self.fuserName,vType)

    def funRequestIntSound(self):
        vType='intSound'
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

    def formatButton(self,index):
        button=[self.btnTextFile,self.btnCamSound\
            ,self.btnScreen,self.btnKeyMou,self.btnKMD,self.btnControl]


        for i in button:
            i.config(bg='white')

        bt=button[index]

        bt.config(bg='green')

    def funTextFile(self):
        self.formatButton(0)
        self.textFileFrame.tkraise()

    def funCamSound(self):
        self.formatButton(1)
        self.camSoundFrame.tkraise()

    def funScreen(self):
        self.formatButton(2)
        self.ScreenFrame.tkraise()

    def funKeyMouse(self):
        self.formatButton(3)
        self.keyMouseFrame.tkraise()

    def funKeyMoScreen(self):
        self.formatButton(4)
        self.keyMoDispFrame.tkraise()

    def funUserControl(self):
        self.formatButton(5)
        self.userControlFrame.tkraise()


    def offSendingKeyboard(self):
        self.varSKeyboard.set(0)

    def offSendingMouse(self):
        self.varSMouse.set(0)


    def offSendingKM(self):
        self.offSendingKeyboard()
        self.offSendingMouse()
        #[Key.Ctrl,t]

    def offRecievingKeyboard(self):
        self.varRKeyboard.set(0)

    def offRecievingMouse(self):
        self.varRMouse.set(0)

    def offRecievingKM(self):
        self.offRecievingKeyboard()
        self.offRecievingMouse()
        #[Key.Alt,t]




    def getFont(self,size):
        font="Helvetica {0}  ".format(size)
        return font

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

            threading.Thread(target=fts).start()

        threading.Thread(target=fun).start()

    def funOffSending(self,userName,types):
        def fun():
            self.controlCond[userName][types]=False
            self.executeOnStop(types)


        threading.Thread(target=fun).start()

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
                t1=threading.Thread(target=fun)
                t1.start()
                self.funThread[types]=t1



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

class Request:

    def __init__(self,root,c,userName,vType):
        self.root=root
        self.userName=userName
        self.vType=vType

        self.root.title('Requesting')
        self.root.geometry('250x100')

        self.root.protocol('WM_DELETE_WINDOW',self.onClose)

        self.c=c
        btnWidth=12


        mainFrame=tk.Frame(self.root,width=250,height=100,bg='red')

        topFrame=gf.GradientFrame(mainFrame,'#11267A','#5EB074',width=250,height=100,steps=700)


        self.labelTitle=tk.Label(topFrame,text='This is the title of the label')
        self.labelTitle.place(x=20,y=10)

        btnAccept=tk.Button(topFrame,text='Accept',width=btnWidth,command=self.funBtnAccept)
        btnAccept.place(x=20,y=70)

        btnReject=tk.Button(topFrame,text='Reject',width=btnWidth,command=self.funBtnReject)
        btnReject.place(x=150,y=70)

        topFrame.place(x=0,y=0)
        mainFrame.place(x=0,y=0)


    def funBtnAccept(self):
        self.c.rResponse(self.userName,self.vType,'1')

        self.onClose()

    def funBtnReject(self):
        self.c.rResponse(self.userName,self.vType,'0')

        self.onClose()

    def onClose(self):
        #print(MainWindow.openWindows)
        MainWindow.openWindows[self.userName+'request']=False

        self.root.destroy()

    def getFont(self,size):
        font="Helvetica {0} bold ".format(size)
        return font

class Response:

    def __init__(self,root,c,userName,vType,vValue):
        self.root=root
        self.root.title('Response')
        self.root.geometry('250x100')
        self.root.protocol('WM_DELETE_WINDOW',self.onClose)

        self.userName=userName
        self.vType=vType
        self.vValue=vValue

        self.c=c

        btnWidth=12


        mainFrame=tk.Frame(self.root,width=250,height=100,bg='red')

        topFrame=gf.GradientFrame(mainFrame,'#11267A','#5EB074',width=250,height=100,steps=700)

        if self.vValue=='1':

            data=self.userName+' accepted your '+self.vType+' request.'
        else:
            data=self.userName+' rejected your '+self.vType+' request.'

        self.labelTitle=tk.Label(topFrame,text=data)
        self.labelTitle.place(x=20,y=10)

        btnAccept=tk.Button(topFrame,text='Ok',width=btnWidth,command=self.funBtnOk)
        btnAccept.place(x=100,y=70)

        topFrame.place(x=0,y=0)
        mainFrame.place(x=0,y=0)

    def funBtnOk(self):
        self.onClose()

    def onClose(self):
        #print(MainWindow.openWindows)
        MainWindow.openWindows[self.userName+'response']=False

        self.root.destroy()

    def getFont(self,size):
        font="Helvetica {0} bold ".format(size)
        return font

class GroupChat:

    def __init__(self,root,c):
        self.root=root
        self.root.title('Group Chat')
        self.c=c
        self.send=c.send
        self.gc=xcs.GroupChat(self.send)
        btnWidth=12
        self.root.geometry('500x400')

        self.root.protocol('WM_DELETE_WINDOW',self.onClose)

        mainFrame=tk.Frame(self.root,width=700,height=400,bg='red')

        topFrame=gf.GradientFrame(mainFrame,'#8FD1A9','#000000',width=500,height=400,steps=700)

        labelGroupList=tk.Label(topFrame,text='Group List',font=self.getFont(10))
        labelGroupList.place(x=30,y=10)

        self.labelStatus=tk.Label(topFrame,text='Status')
        self.labelStatus.place(x=200,y=10)

        listFrame=gf.GradientFrame(topFrame,'#8FD1A9','#58A928',width=300,height=300,steps=700)

        self.sflistFrame=gc.scrollableFrame(listFrame,300,300)[0]
        listFrame.place(x=30,y=50)


        btnCreateGroup=tk.Button(topFrame,text='Create Group',width=btnWidth,command=self.funCreateGroup)
        btnCreateGroup.place(x=380,y=50)

        btnSearchGroup=tk.Button(topFrame,text='Search Group',width=btnWidth,command=self.funSearchGroup)
        btnSearchGroup.place(x=380,y=90)

        btnGroupRequest=tk.Button(topFrame,text='Group Request',width=btnWidth,command=self.funGroupRequest)
        btnGroupRequest.place(x=380,y=130)


        topFrame.place(x=0,y=0)

        mainFrame.place(x=0,y=0)
        self.initiate()

    def initiate(self):
        window='GroupChat'
        self.c.functionList[window]=self.handle
        self.gc.refressGC()

    def onClose(self):
        MainWindow.openWindows['groupChat']=False
        self.root.destroy()

    def destroyAllElement(self):

        for i in self.root.winfo_children():
            i.destroy()

    def destroyContElement(self,cont):
        for i in cont.winfo_children():
            i.destroy()

    def funCreateGroup(self):
        self.destroyAllElement()
        self.root.title('Create Group')
        self.root.geometry('250x100')


        mainFrame=tk.Frame(self.root,width=700,height=400,bg='red')

        topFrame=gf.GradientFrame(mainFrame,'#8FD1A9','#000000',width=500,height=400,steps=700)

        self.varEntryGroupName=tk.StringVar()



        entryGroupName=tk.Entry(topFrame,text='Enter group Name',textvariable=self.varEntryGroupName)

        entryGroupName.place(x=10,y=30)

        btnCreateGroup=tk.Button(topFrame,text='Create',command=self.btnCreateGroup)

        btnCreateGroup.place(x=150,y=30)

        btnBack=tk.Button(topFrame,text='Back',command=self.funBack)
        btnBack.place(x=200,y=30)

        self.labelStatus=tk.Label(topFrame,text='Status')
        self.labelStatus.place(x=10,y=70)

        topFrame.place(x=0,y=0)

        mainFrame.place(x=0,y=0)

    def btnCreateGroup(self):
        groupName=self.varEntryGroupName.get()
        self.gc.createGroup(groupName)


    def funBack(self):
        self.destroyAllElement()
        self.__init__(self.root,self.c)

    def funSearchGroup(self):
        self.destroyAllElement()
        self.root.title('Search Group')
        self.root.geometry('250x300')


        mainFrame=tk.Frame(self.root,width=700,height=300,bg='red')

        topFrame=gf.GradientFrame(mainFrame,'#8FD1A9','#000000',width=500,height=300,steps=700)

        self.varSearchGroup=tk.StringVar()


        entryGroupName=tk.Entry(topFrame,text='Enter group Name',textvariable=self.varSearchGroup)
        entryGroupName.place(x=10,y=30)
        def funSearchGroup():
            self.gc.searchGroup(self.varSearchGroup.get())

        btnSearchGroup=tk.Button(topFrame,text='Search',command=funSearchGroup)
        btnSearchGroup.place(x=150,y=30)

        btnBack=tk.Button(topFrame,text='Back',command=self.funBack)
        btnBack.place(x=200,y=30)

        self.labelStatus=tk.Label(topFrame,text='Status')
        self.labelStatus.place(x=10,y=70)

        listSearchGroupFrame=gf.GradientFrame(mainFrame,'#8FD1A9','#000000',width=230,height=180,steps=700)

        self.searchListFrame=gc.scrollableFrame(listSearchGroupFrame,180,230)[0]

        listSearchGroupFrame.place(x=10,y=110)

        topFrame.place(x=0,y=0)

        mainFrame.place(x=0,y=0)

    def btnSearchGroup(self):
        groupName=self.varSearchGroup.get()
        self.destroyAllElement()
        self.gc.searchGroup(groupName)

    def funGroupRequest(self):
        self.gc.loadGroupRequest(tp='m')
        self.root.title('Group Request')

        btnWidth=12
        self.root.geometry('250x300')


        mainFrame=tk.Frame(self.root,width=250,height=400,bg='red')

        topFrame=gf.GradientFrame(mainFrame,'#8FD1A9','#000000',width=250,height=400,steps=700)


        self.labelStatus=tk.Label(topFrame,text='Status',font=self.getFont(10))
        self.labelStatus.place(x=10,y=10)

        btnBack=tk.Button(topFrame,text='Back',command=self.funBack)
        btnBack.place(x=200,y=10)

        frameList=gf.GradientFrame(mainFrame,'#8FD1A9','#000000',width=230,height=240,steps=700)
        self.groupRequestListFrame=gc.scrollableFrame(frameList,240,230)[0]
        frameList.place(x=10,y=50)

        topFrame.place(x=0,y=0)

        mainFrame.place(x=0,y=0)

    def handle(self,msg):
        wType=msg['wType']
        info=msg
        if wType=='createGroup':
            self.handleCreateGroup(info)
        elif wType=='searchGroup':
            self.handleSearchGroup(info)
        elif wType=='groupRequest':
            self.handleGroupRequest(info)
        elif wType=='refressGC':
            self.handleRefress(info)
        elif wType=='groupChatWindow':
            self.handleGroupChatWindow(info)
        elif wType=='groupControlPanel':
            self.handleGroupControlPanel(info)
        elif wType=='acceptGroupRequest':
            self.handleAcceptGroupRequest(info)
        elif wType=='sendGroupRequest':
            self.handleSendGroupRequest(info)
        else:
            print("Unknow wType you are expecting ->"+wType)

    def handleSendGroupRequest(self,info):
        code=info['code']
        if code=='1123':
            self.labelStatus.config(text="Sending Request Successfull")
        else:
            self.labelStatus.config(text=code)

    def handleRefress(self,info):
        code=info['code']
        if code=='12k3':
            data=info['data']
            type=info['type']
            shape=info['shape']
            data=ds.remodifyData(data,type,shape)
            if len(data)==0:
                self.labelStatus.config(text='No Records found')
            else:




                self.labelStatus.config(text='{0} records found'.format(len(data)))
                for i in self.sflistFrame.winfo_children():
                    i.destroy()



                def funInit(gName):
                    frame=tk.Frame(self.sflistFrame,width=295,height=50)
                    frame.pack()
                    label=tk.Label(frame,text=gName)
                    label.place(x=10,y=2)
                    def funControlPanel():

                       xc.GroupChatControlPanel(self.root,gName,self.c)


                    def funChatWindow():

                        xc.GroupChat2Window(self.root,gName,self.c)

                    btnControlPanel=tk.Button(frame,text='Control Panel',command=funControlPanel)
                    btnControlPanel.place(x=10,y=22)

                    btnChatWindow=tk.Button(frame,text='Chat Window',command=funChatWindow)
                    btnChatWindow.place(x=130,y=22)

                for i in data:
                    funInit(i[1])

        else:
            self.labelStatus.config(text='Unknown type you are expecting'+code)

    def handleCreateGroup(self,info):
        code=info['code']
        if code=='0000':
            self.labelStatus.config(text="GroupName already exists");
        elif code=='0011':
            self.labelStatus.config(text='Successfully created group')
        else:
            self.labelStatus.config(text="Unknown type expecting "+code);

    def handleSearchGroup(self,info):
        code=info['code']
        if code=='y12k' or code=='kkr1':

            data=info['data']
            type=info['types']
            shape=info['shape']

            data=ds.remodifyData(data,type,shape)
            length=len(data)
            self.labelStatus.config(text=str(length)+ " Records Founded")
            self.destroyContElement(self.searchListFrame)

            if length!=0:
                for i in data:

                    frame=tk.Frame(self.searchListFrame,width=225,height=50)
                    gName=i[0]
                    members=i[1]
                    label=tk.Label(frame,text=gName)

                    label.place(x=10,y=2)

                    labelM=tk.Label(frame,text=members)

                    labelM.place(x=130,y=2)

                    def funViewProfle():
                        xc.GroupViewProfile(self.root,gName,self.c)

                    def funSendRequest():
                        self.gc.sendGroupRequest(gName)
                        self.destroyContElement(self.searchListFrame)


                    btnProfile=tk.Button(frame,text='View Profile',command=funViewProfle)
                    btnProfile.place(x=10,y=22)

                    btnSendRequest=tk.Button(frame,text='Send Request',command=funSendRequest)
                    btnSendRequest.place(x=130,y=22)

                    frame.pack()

        elif code=="2333":
            self.labelStatus.config(text='No Records found')

        else:
            self.labelStatus.config(text="Unknown type expecting "+code);

    def handleGroupRequest(self,info):
        code=info['code']

        if code=="11e1" or code=='eeeg':
            self.handleAdminGroupRequest(info)
        elif code=='1ss2' or  code=='4eem':
            self.handleMemberGroupRequest(info)
        else:
            print("UNKNOWN TYPE YOU Are Expecting ->"+code)

    def handleMemberGroupRequest(self,info):
        code=info['code']
        if code=='1ss2':
            self.labelStatus.config(text="Records found")
            data=info['data']
            type=info['type']
            shape=info['shape']

            data=ds.remodifyData(data,type,shape)

            def funInit(gName):
                frame=tk.Frame(self.sflistFrame,width=240,height=100)
                frame.pack()
                label=tk.Label(frame,text=gName)
                label.place(x=30,y=10)
                def funAccept():
                    self.gc.acceptGroupRequest(gName,acceptT='1',tp='m')
                    frame.destroy()

                def funReject():
                    self.gc.acceptGroupRequest(gName,acceptT='0',tp='m')
                    frame.destroy()

                btnControlPanel=tk.Button(frame,text='Accept',command=funAccept)
                btnControlPanel.place(x=30,y=60)

                btnChatWindow=tk.Button(frame,text='Reject',command=funReject)
                btnChatWindow.place(x=150,y=60)
            for i in data:
                funInit(i)

        else:
            self.labelStatus.config(text="No Records found")

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
        print("THIS IS RIDICUFLDLL")

    def handleGroupControlPanel(self,info):
        print("THISLKIDFSLFKJLFJK")

    def handleAcceptGroupRequest(self,info):
        code=info['code']

        if code=='tmm4':
            self.labelStatus.config(text='Group Request Acception successfull')
        elif code=='tkm4':
            self.labelStatus.config(text='Group Request Rejection successfull')
        else:
            print("UNKNOWNKFDLFJ FDFJL "+code)
            pass
            #self.labelStatus.config(text='Unknown type you are expecting '+code)


    def getFont(self,size):
        font="Helvetica {0} bold ".format(size)
        return font

class GroupChatControlPanel:

    def __init__(self,root,gName,c):
        self.root=root
        self.gName=gName
        self.c=c
        self.send=c.send
        self.gc=xcs.GroupChat(self.send)


        self.root.title(gName+" - Control Panel")

        self.root.geometry('900x350')

        mainFrame=tk.Frame(self.root,width=900,height=400,bg='red')

        topFrame=gf.GradientFrame(mainFrame,'#8FD1A9','#000000',width=900,height=400,steps=700)

        self.labelTitleGName=tk.Label(topFrame,text="Title of The group")
        self.labelTitleAName=tk.Label(topFrame,text="Admin of the Group")
        self.labelTitleNoM=tk.Label(topFrame,text="Members :- 0")
        self.labelStatus=tk.Label(topFrame,text="Status")



        self.labelTitleGName.place(x=30,y=10)
        self.labelTitleAName.place(x=250,y=10)
        self.labelTitleNoM.place(x=480,y=10)
        self.labelStatus.place(x=600,y=10)

        def funLeaveGroup():
            self.gc.leaveGroup(self.gName)
            time.sleep(1)
            self.funBack()

        btnLeavel=tk.Button(topFrame,text="Leavel Group",command=funLeaveGroup)
        btnLeavel.place(x=800,y=60)

        btnBack=tk.Button(topFrame,text='Back',command=self.funBack)
        btnBack.place(x=800,y=10)

        labelMem=tk.Label(topFrame,text="Group Members")
        labelMem.place(x=30,y=60)

        listFrame1=gf.GradientFrame(topFrame,'#8FD1A9','#58A928',width=250,height=300,steps=700)

        self.sflistFrame1=gc.scrollableFrame(listFrame1,250,230)[0]
        listFrame1.place(x=30,y=90)


        labelMemSentRe=tk.Label(topFrame,text='Group Sent Request')
        labelMemSentRe.place(x=330,y=60)

        listFrame2=gf.GradientFrame(topFrame,'#8FD1A9','#58A928',width=200,height=300,steps=700)

        self.sflistFrame2=gc.scrollableFrame(listFrame2,250,230)[0]
        listFrame2.place(x=330,y=90)


        labelMemRecvRe=tk.Label(topFrame,text="Group Recv Request")
        labelMemRecvRe.place(x=630,y=60)

        listFrame3=gf.GradientFrame(topFrame,'#8FD1A9','#58A928',width=200,height=300,steps=700)

        self.sflistFrame3=gc.scrollableFrame(listFrame3,250,230)[0]
        listFrame3.place(x=630,y=90)






        topFrame.place(x=0,y=0)

        mainFrame.place(x=0,y=0)


        self.initiate()

    def simpleFrameLabel(self,cont,text,width=100,height=50):
        frame=tk.Frame(cont,width=width,height=height)

        label=tk.Label(frame,text=text)
        label.place(x=10,y=10)
        frame.pack()

    def funBack(self):
        self.destroyAllElement()
        xc.GroupChat(self.root,self.c)

    def refress(self):


        self.gc.groupControlPanel(self.gName)
        self.c.functionList['groupControlPanel']=self.handle

    def ref(self):

        xc.GroupChatControlPanel(self.root,self.gName,self.c)

    def initiate(self):
        self.refress()

    def handle(self,msg):
        code=msg['code']
        info=msg

        if code=='kk14':
            self.labelStatus.config(text="Result Founded Successfully")

            mainMember=ds.remodifyData(info['mm'],info['mmt'],info['mms'])
            sendMember=ds.remodifyData(info['sm'],info['smt'],info['sms'])
            recvMember=ds.remodifyData(info['rm'],info['rmt'],info['rms'])

            gName=info['groupName']

            self.labelTitleGName.config(text=gName)
            length=len(mainMember)
            self.labelTitleNoM.config(text='Members :- '+str(length))

            typMainMember=mainMember[:,1].tolist()
            index=typMainMember.index('a')
            admin=mainMember[index][0]
            self.labelTitleAName.config(text='Admin :- '+admin)

            adminCond=False


            if(self.c.userName.lower()==admin.lower()):
                adminCond=True

            def funMainMember(ids):
                name=ids[0]
                typ=ids[1]
                frame=tk.Frame(self.sflistFrame1,width=250,height=60)
                label=tk.Label(frame,text=name)
                label.place(x=10,y=2)

                ltype=tk.Label(frame,text='Type : '+typ)
                ltype.place(x=10,y=27)

                def funKick():
                    self.gc.kickMemberGroupChat(self.gName,name)
                    self.c.functionList['acceptGroupRequest']=self.handle

                    self.ref()

                if adminCond:

                    if self.c.userName.lower()==name.lower():
                        pass
                    else:
                        btnKick=tk.Button(frame,text="Kick",command=funKick)
                        btnKick.place(x=120,y=27)

                frame.pack()

            def funSentMember(ids):
                name=ids
                frame=tk.Frame(self.sflistFrame2,width=250,height=60)
                label=tk.Label(frame,text=name)
                label.place(x=10,y=2)


                def funCancel():
                    self.gc.cancelGroupSendRequest(self.gName,name)
                    self.c.functionList['acceptGroupRequest']=self.handle

                    self.ref()

                if adminCond:
                    if self.c.userName==admin:
                        label=tk.Label(frame,text="You are not capable to perform action")
                        label.place(x=10,y=27)
                    else:


                        btnKick=tk.Button(frame,text="Cancel",command=funCancel)
                        btnKick.place(x=120,y=27)

                frame.pack()

            def funRecvMember(ids):
                name=ids
                frame=tk.Frame(self.sflistFrame3,width=250,height=60)
                label=tk.Label(frame,text=name)
                label.place(x=10,y=2)

                def funAccept():
                    self.gc.acceptGroupRequest(self.gName,name)
                    self.c.functionList['acceptGroupRequest']=self.handle

                    self.ref()

                def funReject():
                    self.gc.acceptGroupRequest(self.gName,name,'0')
                    self.c.functionList['acceptGroupRequest']=self.handle

                    self.ref()
                if adminCond:
                    if self.c.userName==admin:
                        label=tk.Label(frame,text="You are not capable to perform action")
                        label.place(x=10,y=27)
                    else:
                        btnAccept=tk.Button(frame,text='Accept',command=funAccept)
                        btnAccept.place(x=10,y=27)
                        btnKick=tk.Button(frame,text=" Reject",command=funReject)
                        btnKick.place(x=120,y=27)

                frame.pack()



            for i in mainMember:
                    funMainMember(i)

            for i in sendMember:
                funSentMember(i)

            for i in recvMember:
                funRecvMember(i)

        elif code=='tkm4':

            self.labelStatus.config(text="Rejection Successfull")
        elif code=='ffe4':


            self.labelStatus.config(text='Acception Successfull')

        else:


            self.labelStatus.config(text="Something went wrong E:"+code)

    def destroyAllElement(self):

        for i in self.root.winfo_children():
            i.destroy()

class GroupChat2Window:

    def __init__(self,root,gName,c):
        self.root=root
        self.gName=gName
        self.c=c
        self.send=c.send
        self.gc=xcs.GroupChat(self.send)

        self.empty=False

        self.root.title(gName+" - ChatWindow")

        self.root.geometry('300x400')

        mainFrame=tk.Frame(self.root,width=300,height=400,bg='red')

        topFrame=gf.GradientFrame(mainFrame,'#8FD1A9','#000000',width=300,height=400,steps=700)

        self.labelTitleGName=tk.Label(topFrame,text="Title of The group")


        self.labelTitleGName.place(x=30,y=10)

        btnBack=tk.Button(topFrame,text="Back",command=self.funBack)
        btnBack.place(x=210,y=10)




        listFrame=gf.GradientFrame(topFrame,'#8FD1A9','#58A928',width=200,height=300,steps=700)

        self.sflistFrame=gc.scrollableFrame(listFrame,250,230)[0]
        listFrame.place(x=30,y=60)


        self.varTextMsg=tk.StringVar()

        entMsg=tk.Entry(topFrame,textvariable=self.varTextMsg)
        entMsg.place(x=30,y=320)

        def funSendMsg():
            msg=self.varTextMsg.get()
            self.gc.sendGroupChat(self.gName,msg)

            if self.empty:
                for i in self.sflistFrame.winfo_children():
                    i.destroy()

                self.empty=False

            text='Me :- '+msg
            self.varTextMsg.set("")
            self.simpleFrameLabel(self.sflistFrame,text,width=250)


        btnSendMsg=tk.Button(topFrame,text="Send Msg",command=funSendMsg)
        btnSetFile=tk.Button(topFrame,text='Set File')
        btnSendFile=tk.Button(topFrame,text="Send File")

        btnSendMsg.place(x=210,y=320)
        btnSetFile.place(x=30,y=360)
        btnSendFile.place(x=210,y=360)



        topFrame.place(x=0,y=0)

        mainFrame.place(x=0,y=0)


        self.initiate()

    def funBack(self):
        self.destroyAllElement()
        xc.GroupChat(self.root,self.c)

    def simpleFrameLabel(self,cont,text,width=100,height=50):
        frame=tk.Frame(cont,width=width,height=height)

        label=tk.Label(frame,text=text)
        label.place(x=10,y=10)
        frame.pack()


    def initiate(self):
        self.refress()

    def destroyAllElement(self):

        for i in self.root.winfo_children():
            i.destroy()

    def refress(self):
        self.gc.groupChatWindow(self.gName)
        self.c.functionList['groupChatWindow']=self.handle

    def handle(self,msg):
        info=msg
        code=info['code']

        if code=='k31s':
            groupName=info['groupName']

            chatData=ds.remodifyData(info['dataC'],info['dataCT'],info['dataCS'])

            self.labelTitleGName.config(text=groupName)

            if(len(chatData)==0):
                self.empty=True
                self.simpleFrameLabel(self.sflistFrame,'@No Chats were founded',width=250)
            else:
                self.empty=False
                for i in chatData:
                    #print(i)
                    wType,data=ad.deAssValue(i,True)

                    #print(data)
                    #print("_-----")
                    chat=data['chat']
                    chat=ds.dec(chat)
                    userName=data['userName']
                    data=userName+' :- '+chat
                    self.simpleFrameLabel(self.sflistFrame,data,width=250)

        else:
            self.labelTitleGName.config(text="Something went wrong ..")

class GroupViewProfile:

    def __init__(self,root,gName,c):
        self.root=root
        self.gName=gName
        self.c=c
        self.send=c.send
        self.gc=xcs.GroupChat(self.send)

        self.root.title(gName+" - View Profile")

        self.root.geometry('300x100')

        mainFrame=tk.Frame(self.root,width=300,height=100,bg='red')

        topFrame=gf.GradientFrame(mainFrame,'#8FD1A9','#000000',width=300,height=400,steps=700)

        self.labelTitleGName=tk.Label(topFrame,text="Title of The group")


        self.labelTitleGName.place(x=30,y=10)

        btnBack=tk.Button(topFrame,text="Back",command=self.funBack)
        btnBack.place(x=210,y=10)

        self.labelMembers=tk.Label(topFrame,text="Members no")
        self.labelMembers.place(x=30,y=50)




        topFrame.place(x=0,y=0)

        mainFrame.place(x=0,y=0)


        self.initiate()

    def funBack(self):
        self.destroyAllElement()
        xc.GroupChat(self.root,self.c)

    def initiate(self):
        self.refress()
        pass
    def destroyAllElement(self):

        for i in self.root.winfo_children():
            i.destroy()

    def refress(self):
        self.gc.loadGroupInfo(self.gName,'viewGroupProfile')

        self.c.functionList['viewGroupProfile']=self.handle

    def handle(self,msg):

        code=msg['code']
        info=msg
        if code=='y12k':
            gName=info['groupName']

            mainData=ds.remodifyData(info['mdata'],info['mtypes'],info['mshape'])

            length=len(mainData)

            self.labelTitleGName.config(text=gName)
            self.labelMembers.config(text="Members :- "+str(length))

        else:
            self.labelTitleGName.config(text="Something went wrong ..")

class GroupMeet:

    def __init__(self,root,c):
        self.root=root
        self.root.title('Group Meet')
        self.c=c
        self.send=c.send
        self.gm=xcs.GroupMeet(self.send)

        btnWidth=12
        self.root.geometry('250x100')

        self.root.protocol('WM_DELETE_WINDOW',self.onClose)
        mainFrame=tk.Frame(self.root,width=700,height=400,bg='red')

        topFrame=gf.GradientFrame(mainFrame,'#8FD1A9','#000000',width=500,height=400,steps=700)

        def tin():
           xc.Meeting(self.root,self.c,True)

        btnCreateMeet=tk.Button(topFrame,text='Create Meeting',width=btnWidth,command=self.funCreateMeeting)
        btnCreateMeet.place(x=80,y=10)

        btnJoinMeet=tk.Button(topFrame,text='Join Meeting',width=btnWidth,command=self.funJoinMeeting)
        btnJoinMeet.place(x=80,y=50)

        topFrame.place(x=0,y=0)

        mainFrame.place(x=0,y=0)

    def getFont(self,size):
        font="Helvetica {0} bold ".format(size)
        return font

    def onClose(self):
        MainWindow.openWindows['groupMeet']=False
        self.gm.gmOnClose();
        self.root.destroy()

    def destroyAllElement(self):

        for i in self.root.winfo_children():
            i.destroy()

    def funBack(self):
        self.destroyAllElement()
        self.__init__(self.root,self.c)

    def funCreateMeeting(self):
        self.destroyAllElement()

        self.root.title('Create Meeting')

        btnWidth=12
        self.root.geometry('300x100')


        mainFrame=tk.Frame(self.root,width=700,height=400,bg='red')

        topFrame=gf.GradientFrame(mainFrame,'#8FD1A9','#000000',width=500,height=400,steps=700)

        varMeet=tk.StringVar()
        varPass=tk.StringVar()

        varMeet.set("MEETING NAME")
        varPass.set("MEETING PASSWORD")

        entryMeetingId=tk.Entry(topFrame,textvariable=varMeet)
        entryMeetingId.place(x=10,y=10)

        entryMeetingPassword=tk.Entry(topFrame,textvariable=varPass)
        entryMeetingPassword.place(x=150,y=10)

        def funCreate():

            self.c.functionList['gmCreateMeeting']=self.handle
            self.gm.createMeeting(varMeet.get(),varPass.get())



        btnCreate=tk.Button(topFrame,text='Create',command=funCreate)
        btnCreate.place(x=10,y=50)

        btnBack=tk.Button(topFrame,text='Back',command=self.funBack)
        btnBack.place(x=80,y=50)

        label=tk.Label(topFrame,text='Status')
        label.place(x=150,y=50)


        topFrame.place(x=0,y=0)

        mainFrame.place(x=0,y=0)

    def funJoinMeeting(self):
        self.destroyAllElement()
        self.root.title('Join Meeting')

        btnWidth=12
        self.root.geometry('300x100')


        mainFrame=tk.Frame(self.root,width=700,height=400,bg='red')

        topFrame=gf.GradientFrame(mainFrame,'#8FD1A9','#000000',width=500,height=400,steps=700)


        varMeet=tk.StringVar()
        varPass=tk.StringVar()

        varMeet.set("MEETING ID")
        varPass.set("MEETING PASSWORD")

        entryMeetingId=tk.Entry(topFrame,textvariable=varMeet)
        entryMeetingId.place(x=10,y=10)

        entryMeetingPassword=tk.Entry(topFrame,textvariable=varPass)
        entryMeetingPassword.place(x=150,y=10)

        def funJoin():
            self.c.functionList['gmJoinMeeting']=self.handle

            self.gm.joinMeeting(varMeet.get(),varPass.get())

        btnCreate=tk.Button(topFrame,text='Join',command=funJoin)
        btnCreate.place(x=10,y=50)

        btnBack=tk.Button(topFrame,text='Back',command=self.funBack)
        btnBack.place(x=80,y=50)

        self.labelStatus=tk.Label(topFrame,text='Status')
        self.labelStatus.place(x=150,y=50)


        topFrame.place(x=0,y=0)

        mainFrame.place(x=0,y=0)


    def handle(self,msg):

        wType=msg['wType']

        if wType=='gmCreateMeeting':
            self.handleCreateMeeting(msg)

        elif wType=='gmJoinMeeting':
            self.handleJoinMeeting(msg)

        else:
            print("This is blunder mistake ",wType,msg['code'])

    def handleCreateMeeting(self,info):

        code=info['code']
        if code=='1122':
            #self.destroyAllElement()

            mm=xc.Meeting(self.root,self.c,True)
            mm.initData(info)
        else:
            print("THIS LDJLFD IS FID ",code)

    def handleJoinMeeting(self,info):
        code=info['code']


        if code=='ini2':
            mm=xc.Meeting(self.root,self.c,False)
            mm.initData(info)

            data=ds.remodifyData(info['data'],info['type'],info['shape'])
            data=data[0]
            for i in data:
                if i.lower()==self.c.userName.lower():
                    continue
                mm.initSmallFrame(i)
        elif code=='kkr1':
            self.labelStatus.config(text="Group Meeting Id\ndon't exist")
        elif code=='1221':
            self.labelStatus.config(text="Incorrect Password")
        elif code=='eel3':
            self.labelStatus.config(text='Meeting is locked')

        elif code=='fer3':

            self.labelStatus.config(text="Joining the room")
            mm=xc.Meeting(self.root,self.c,False)
            mm.initData(info)

        elif code=='ft65':
            self.labelStatus.config(text="Room auth req is on\n Wait for a min \n for ADMIN RESPONSE")

        elif code=='kke3':
            id=info['id']
            self.labelStatus.config(text="Admin of {0} Reject \nyour request".format(id))

        else:
            print(" This is blunder mistake ",code)

class Meeting:

    def __init__(self,root,c,condAdmin=False):

        MainWindow.xprtControl.funOpenWindow("@meet")

        self.root=root
        self.c=c
        self.c.functionList['GroupMeet']=self.handle

        self.send=c.send
        self.gm=xcs.GroupMeet(self.send)

        self.condAdmin=condAdmin

        self.root.title('Meeting')
        self.sendC={}
        self.sendM={}
        btnWidth=12
        self.root.geometry('910x500')


        mainFrame=tk.Frame(self.root,width=1000,height=500,bg='red')

        topFrame=gf.GradientFrame(mainFrame,'#8FD1A9','#000000',width=1000,height=500,steps=700)

        topFrame.place(x=0,y=0)

        mainFrame.place(x=0,y=0)

        self.labelMeetingName=tk.Label(topFrame,text="Meeting Name")
        self.labelMeetingName.place(x=30,y=10)

        self.labelStatus=tk.Label(topFrame,text="Label Status")
        self.labelStatus.place(x=250,y=10)

        self.labelMeetingId=tk.Label(topFrame,text="Meeting Id :-")
        self.labelMeetingId.place(x=30,y=70)

        self.labelMeetingPass=tk.Label(topFrame,text="Meeting Password :-")
        self.labelMeetingPass.place(x=250,y=70)

        def funLeaveMeeting():
            self.gm.gmLeaveMeeting()

        btnLeaveMeeting=tk.Button(topFrame,text="Leave Meeting",command=funLeaveMeeting)
        btnLeaveMeeting.place(x=500,y=10)

        self.varLockMeeting=tk.IntVar()
        self.varAuthReq=tk.IntVar()
        frame=tk.Frame(topFrame,width=300,height=100)

        lb=tk.Label(frame,text="Sequrity")
        lb.place(x=30,y=5)

        if self.condAdmin:
            self.varLockMeeting.set(0)
            self.varAuthReq.set(0)

            lockOn=tk.Radiobutton(frame,text='Lock On',variable=self.varLockMeeting,value=1,command=self.onChangeLockOn)
            lockOn.place(x=30,y=40)

            lockOn=tk.Radiobutton(frame,text='Lock Off',variable=self.varLockMeeting,value=0,command=self.onChangeLockOn)
            lockOn.place(x=180,y=40)

            authReq=tk.Radiobutton(frame,text="Auth. Request On",variable=self.varAuthReq,value=1,command=self.onChangeAuthReq)
            authReq.place(x=30,y=75)

            authReq=tk.Radiobutton(frame,text="Auth. Request Off",variable=self.varAuthReq,value=0,command=self.onChangeAuthReq)
            authReq.place(x=180,y=75)
        else:
            self.labelLock=tk.Label(frame,text="Status of Lock")
            self.labelLock.place(x=30,y=40)


            self.labelAuthReq=tk.Label(frame,text="Status of Auth Request")
            self.labelAuthReq.place(x=30,y=75)
        frame.place(x=600,y=10)


        listFrame=gf.GradientFrame(topFrame,'#8FD1A9','#58A928',width=2300,height=3000,steps=700)

        self.chatListFrame,self.chatCont=gc.scrollableFrame(listFrame,300,230)
        listFrame.place(x=30,y=130)

        self.varChat=tk.StringVar()

        entryChat=tk.Entry(topFrame,textvariable=self.varChat)
        entryChat.place(x=30,y=450)

        def funSendChat():

            chat=self.varChat.get()
            if chat=='':
                pass
            else:
                data=self.insertChatGui(chat)
                self.gm.sendChat(data)

        btnSend=tk.Button(topFrame,text="Send Chat",command=funSendChat)
        btnSend.place(x=215,y=450)


        frame=tk.Frame(topFrame,width=350,height=230)

        self.labelMainView=tk.Label(frame,width=350,height=230)
        self.labelMainView.place(x=10,y=10)

        frame.place(x=300,y=130)

        frame=tk.Frame(topFrame,width=215,height=230)

        self.labelYourView=tk.Label(frame,text="Your View")
        self.labelYourView.place(x=10,y=5)

        self.labelHisView=tk.Label(frame)
        self.labelHisView.place(x=10,y=40)

        self.varSCamera=tk.IntVar()
        self.varSCamera.set(0)


        sentCameraRad2=tk.Radiobutton(frame,text='Camera On',variable=self.varSCamera,value=1,command=self.onChangeSendCamera)
        sentCameraRad2.place(x=10,y=180)

        sentCameraRad2=tk.Radiobutton(frame,text='Camera Off',variable=self.varSCamera,value=0,command=self.onChangeSendCamera)
        sentCameraRad2.place(x=110,y=180)

        self.varSMic=tk.IntVar()

        sentMicRad2=tk.Radiobutton(frame,text='Mic On',variable=self.varSMic,value=1,command=self.onChangeSendMic)
        sentMicRad2.place(x=10,y=200)
        self.varSMic.set(0)
        sentMicRad2=tk.Radiobutton(frame,text='Mic Off',variable=self.varSMic,value=0,command=self.onChangeSendMic)
        sentMicRad2.place(x=110,y=200)


        frame.place(x=680,y=130)

        listFrame=gf.GradientFrame(topFrame,'#8FD1A9','#58A928',width=6000,height=1000,steps=700)

        self.scroolMemberInList=gc.scrollableFrameHorizontal(listFrame,100,600)[0]
        listFrame.place(x=300,y=370)

        self.setMeetingFunction()

    def insertChatGui(self,chat,mt='ME'):
        frame=tk.Frame(self.chatListFrame,width=230,height=50)
        label=tk.Label(frame,text="@{0} ->".format(mt)+chat)
        label.place(x=3,y=3)
        frame.pack()

        chat=ds.enc(chat)
        self.varChat.set("")
        self.chatCont.yview_moveto(1)

        data=ad.assValue(['userName','chat'],[self.c.userName,chat],'MeetingChat')
        return data


    def initData(self,info):
        name=info['name']
        password=info['password']
        mid=info['id']

        self.labelMeetingName.config(text=name)
        self.labelMeetingId.config(text='Meeting Id :- '+mid)
        self.labelMeetingPass.config(text='Meeting Password :- '+password)

        self.labelStatus.config(text='Group Meeting Successfully Created')

    def setMeetingFunction(self):
        self.frameListUser={}
        self.imgDict={}
        self.imgCounter={}
        self.impCond={}
        self.nameMainView=None

    def handle(self,msg):
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

    def handleInfoUpdate(self,info):
        code=info['code']
        if code=='kr14':
            self.handleLockMeeting(info)
        elif code=='kr13':
            self.handleAuthRequest(info)
        else:
            print("THIS IS BLUDFL INFO ",code)

    def handleLockMeeting(self,info):
        code=info['code']

        if code=='kr14':
            value=info['value']
            if value=='1':

                self.labelLock.config(text="Meeting Room is locked")
            else:
                self.labelLock.config(text="Meeting Room is open")
        else:
            print("THIS IS LOCK MMETING ERROR ",code)

    def handleAuthRequest(self,info):
        code=info['code']

        if code=='kr13':
            value=info['value']
            if value=='1':
                self.labelAuthReq.config(text='Auth Request is on')
            else:
                self.labelAuthReq.config(text="Auth Request is off")
        else:
            print("this is mistake in auth req ",code)

    def handleJoinClientRequest(self,info):
        code=info['code']

        if code=='1er4':
            userName=info['userName']

            print(userName,self.c.userName)


            windowName=userName.lower()+'- > Join Request'
            cond=self.checkOpenWindow(windowName)
            if cond:
                pass

            else:
                MainWindow.openWindows[windowName]=True
                root=tk.Toplevel(self.root)

                def funOnClose():
                    MainWindow.openWindows[windowName]=False
                    funReject()

                    root.destroy()
                def funAccept():
                    MainWindow.openWindows[windowName]=False
                    self.gm.sendJoinClientRequestResponse(userName)
                    root.destroy()

                def funReject():
                    MainWindow.openWindows[windowName]=False

                    self.gm.sendJoinClientRequestResponse(userName,'0')
                    root.destroy()

                root.protocol('WM_DELETE_WINDOW',funOnClose)
                xc.GroupMeetJoinRequest(root,userName,funAccept,funReject)
        else:
            print("THIS IS UNKNOWN KIND OF CODE ",code)

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
            userName=info['userName'].lower()
            self.labelStatus.config(text='@A-{0} Left the meeting'.format(userName))
            time.sleep(3)
            self.labelStatus.config(text='Everything will be destroyed soon')
            time.sleep(3)

            self.root.destroy()
        elif code=='mm00':
            userName=info['userName'].lower()

            self.labelStatus.config(text="@M-{0} left the Meeting".format(userName))
            frame=self.frameListUser[userName]
            #Member Left Meeting
            #I Love you Anjali Friday,December 18 2020

            frame.destroy()
            #I just want to say this magical times many times but i dont know
            #How much time.
            pass

        else:
            print("This is bludender type of mistake in a group ",code)

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

            self.insertChatGui(dchat,userName)


        else:
            print("This is chatting error ",code)

    def handleKickOut(self,info):
        code=info['code']

        if code=='98kk':
            self.labelStatus.config(text="You are kicked from the meeting")
            time.sleep(2)
            self.root.destroy()
        elif code=='99kk':
            #User has been kickouted
            if not self.condAdmin:
                userName=info['userName'].lower()
                self.labelStatus.config(text="{0} has been kicked from the meeting".format(userName))
                frame=self.frameListUser[userName]
                frame.destroy()

        else:
            print("THIS IS BLUNEDER MISTAKE ",code)

    def handleSendDetailOfMember(self,info):
        code=info['code']

        if code=='adm1':
            self.initSmallFrame(info['userName'])

    def handleAudData(self,info):
        userName=info['userName']
        value=str(self.sendM[userName].get())

        if value=='1':
            data=info['data']
            ddata=ds.decb(bytes(data,'utf-8'))
            con.play_audio(stream,ddata)


    def handleImgData(self,info):
        userName=info['userName']
        value=str(self.sendC[userName].get())

        if value=='1':
            frame=self.frameListUser[userName.lower()]

            winfoChild=frame.winfo_children()


            if userName not in self.imgCounter:
                self.imgCounter[userName]=0
                winfoChild[0].config(width=30)
                winfoChild[0].config(height=20)





            self.imgCounter[userName]=self.imgCounter[userName]+1


            data=ds.remodifyData(info['data'],info['type'],info['shape'])
            if self.nameMainView==userName:
                fdata=data.copy()
                self.mainViewHandler(fdata,userName)
            rimg=cv2.resize(data,(20,30))
            img=gc.cvtIntoLabelImage(rimg)

            self.imgDict[userName+"@"+str(self.imgCounter[userName])]=img



            winfoChild[0].config(image=self.imgDict[userName+"@"+str(self.imgCounter[userName])])

            if self.imgCounter[userName]%2==0:
                self.imgCounter[userName]=0



    def mainViewHandler(self,image,userName):
        tName='@'+userName
        if tName not in self.imgCounter:
                self.imgCounter[tName]=0

        self.imgCounter[tName]=self.imgCounter[tName]+1

        img=cv2.resize(image,(300,230))
        limg=gc.cvtIntoLabelImage(img)
        f=tName+"@"+str(self.imgCounter[tName])
        self.imgDict[f]=limg

        self.labelMainView.config(image=self.imgDict[f])

        if self.imgCounter[tName]%2==0:
            self.imgCounter[tName]=0


    def checkOpenWindow(self,windowName):
        if windowName in MainWindow.openWindows:
            return MainWindow.openWindows[windowName]
        else:
            return False

    def onChangeLockOn(self):
        value=self.varLockMeeting.get()

        self.gm.lockMeeting(str(value));

    def onChangeAuthReq(self):
        value=self.varAuthReq.get()
        self.gm.authRequest(str(value));

    def showCameraView(self):
        self.labelYourView.config(width=180)
        self.labelYourView.config(height=150)

        def fun():
            count=0
            while self.varSCamera.get()==1:
                frame=con.camFrame
                count=count+1

                if frame is not None:
                    frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

                    frame=cv2.resize(frame,(180,150))
                    frame=gc.cvtIntoLabelImage(frame)

                    self.imgDict['cam_'+str(count)]=frame
                    self.labelYourView.config(image=self.imgDict['cam_'+str(count)])

                if count%2==0:
                    count=0

        threading.Thread(target=fun).start()


    def onChangeSendCamera(self):
        value=str(self.varSCamera.get())
        def fun():
            pass
        if value=='1':
            MainWindow.xprtControl.funFirstOnList['camera']=fun
            MainWindow.xprtControl.funOnSending('@meet','camera')
            self.gm.gmUpdateYourSendCont('img','1')
            self.showCameraView()
        else:
            MainWindow.xprtControl.funOffSending('@meet','camera')
            self.gm.gmUpdateYourSendCont('img','0')

    def onChangeSendMic(self):
        value=str(self.varSMic.get())
        def fun():
            pass
        if value=='1':
            MainWindow.xprtControl.funFirstOnList['sound']=fun
            MainWindow.xprtControl.funOnSending('@meet','sound')
            self.gm.gmUpdateYourSendCont('aud','1')
        else:
            MainWindow.xprtControl.funOffSending('@meet','sound')
            self.gm.gmUpdateYourSendCont('aud','0')

    def getFont(self,size):
        font="Helvetica {0} bold ".format(size)
        return font

    def destroyAllElement(self):

        for i in self.root.winfo_children():
            i.destroy()

    def funBack(self):
        self.destroyAllElement()
        self.__init__(self.root)

    def initSmallFrame(self,i):

        frame=tk.Frame(self.scroolMemberInList,width=150,height=100)
        self.frameListUser[i.lower()]=frame
        label=tk.Label(frame,width=5,height=3,bg='red')
        label.place(x=2,y=2)

        def funOk():
            self.nameMainView=i


        def funKick():
            self.gm.kickOut(i)
            frame.destroy()

        varSCamera=tk.IntVar()
        varSMic=tk.IntVar()
        self.sendC[i]=varSCamera
        self.sendM[i]=varSMic

        def funContImg():

            value=str(self.sendC[i].get())

            self.gm.gmUpdateUCamCont(i,value)

        def funContMic():

            value=str(self.sendM[i].get())
            self.gm.gmUpdateUMicCont(i,value)


        btnOk=tk.Button(frame,text='ØK',bg='green',command=funOk)
        btnOk.place(x=50,y=2)
        if self.condAdmin:
            btnOk=tk.Button(frame,text='Kick',bg='green',command=funKick)
            btnOk.place(x=100,y=2)

        labelName=tk.Label(frame,text=i)
        labelName.place(x=50,y=30)



        sentCameraRad2=tk.Radiobutton(frame,text='CO',variable=self.sendC[i],value=1,command=funContImg)
        sentCameraRad2.place(x=2,y=60)

        sentCameraRad2=tk.Radiobutton(frame,text='CF',variable=self.sendC[i],value=0,command=funContImg)
        sentCameraRad2.place(x=70,y=60)


        sentMicRad2=tk.Radiobutton(frame,text='MO',variable=self.sendM[i],value=1,command=funContMic)
        sentMicRad2.place(x=2,y=80)

        sentMicRad2=tk.Radiobutton(frame,text='MO',variable=self.sendM[i],value=0,command=funContMic)
        sentMicRad2.place(x=70,y=80)

        frame.pack(side='left')

class GroupMeetJoinRequest:

    def __init__(self,root,userName,funAccept,funReject):

        self.root=root

        self.root.title("Join Request")

        self.root.geometry('300x100')

        self.labelStatus=tk.Label(self.root,text=userName+' want to join the Meeting')

        self.labelStatus.place(x=50,y=10)

        btnAccept=tk.Button(self.root,text='Accept',command=funAccept)
        btnAccept.place(x=30,y=50)

        btnReject=tk.Button(self.root,text='Reject',command=funReject)
        btnReject.place(x=200,y=50)




if __name__=='__main__':
    root=tk.Tk()
    root.geometry('500x400')

    host=tk.StringVar()
    port=tk.IntVar()

    host.set('localhost')
    port.set(9898)
    labelHost=tk.Entry(root,textvariable=host)
    labelHost.place(x=10,y=10)

    labelPort=tk.Entry(root,textvariable=port)
    labelPort.place(x=10,y=50)

    labelStatus=tk.Label(root,text='Status')

    def fun():
        global xgc,xgm
        try:
            lh=host.get()
            pr=port.get()
            print(lh,pr)
            c=xcs.Client()
            c.connect(lh,int(pr))
            labelStatus.config(text='Connected')
            for i in root.winfo_children():
                i.destroy()

            g=Global(root,c)

        except:
            labelStatus.config(text='Error')


    btnConnect=tk.Button(root,text='Connect',command=fun)
    btnConnect.place(x=10,y=90)

    labelStatus.place(x=10,y=150)





    root.mainloop()
