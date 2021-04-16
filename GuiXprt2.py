#GuiXprt2.py
import Gui_Creation as gc
import tkinter as tk
import GuiXprt2 as gx
import XprtLoginControl as xlc
import TrialVersionClient2 as tvc
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

mouse=km.Mouse()
keyboard=km.Keyboard()
lController=xlc.Controller()
helpDic={}
con=rc.Controls()



class Global:



    def __init__(self,root,c):
        
        self.c=c
        
        self.userName=None
        btnWidth=12
        entryWidth=25
        labelWidth=21
        self.root=root
        root.title('Global Interface')
        self.forward=False
        frame=tk.Frame(root,height=400,width=500)
        self.types=None
        #Title
        titleFrame=tk.Frame(frame,bg='#006266',height=50,width=500)

        labelTitle=tk.Label(titleFrame,text='Online Connection',font="Helvetica 20 bold ",bg='yellow',fg='red')
        labelTitle.place(x=30,y=5)

        

        

        leftFrame=tk.Frame(frame,bg='#00a8ff',height=350,width=250)

        self.varUserl=tk.StringVar(root)
        self.varPassl=tk.StringVar(root)

        self.varUserl.set('Bipin')
        self.varPassl.set('Bipin')

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
        gx.ForgetPassword(self.root,self.c)

    def signUp(self):

        tuserName=self.varUserr.get()
        tpassword=self.varPassr.get()
        tname=self.varNamer.get()
        tseqQ=self.varSeqQ.get()
        tseqA=self.varSeqA.get()

        self.forward=False

        self.c.signUp(tuserName,tname,tpassword,tseqQ,tseqA)
        self.userName=tuserName
        self.c.function1Type=self.handle
        

    def btnLogin(self):

        self.forward=False
        self.userName=self.varUserl.get()
        self.c.login(self.varUserl.get(),self.varPassl.get())
        self.c.function1Type=self.handle
        

    def btnForward(self):
        if self.forward:
            for child in self.root.winfo_children():
                child.destroy()
            self.root.geometry('1100x600+50+50')
            gx.MainWindow.windows={}
            gx.MainWindow(self.root,self.c,self.userName)

    def handle(self,msg):
        
        if msg['code']=='0006':
            self.leftLoginStatus.config(text='Login From Another Location')
            for child in self.root.winfo_children():
                child.destroy()
            
            self.root.geometry('500x400')
            self.c.userName=''
            gx.Global(self.root,self.c)
        
        elif msg['code']=='0003':
       		self.leftLoginStatus.config(text='Login Successful')
       		self.forward=True
       		self.btnForward()
       	elif msg['code']=='0001':
       		self.leftLoginStatus.config(text='Password Error')
       	elif msg['code']=='0002':
       		self.leftLoginStatus.config(text='UserName not found')
       	elif msg['code']=='0005':
       		self.labelUserStatus.config(text='UserName already exists')
       	elif msg['code']=='0004':
       		self.labelUserStatus.config(text='SignUp successfull')
       		self.forward=True
       		self.btnForward()
       	else:
       		self.leftLoginStatus.config(text='Error Code not in list')

class ForgetPassword:


    def __init__(self,root,c):
        
        self.c=c
        self.forward=False
        
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
        gx.Global(self.root,self.c)

    def submit(self):

        tuserName=self.varUserName.get()
        tseqAnswer=self.varSeqA.get()
        self.c.forgetPassword(tuserName,tseqAnswer)
        self.c.function1Type=self.handle
        
    def handle(self):
    	if msg['wType']=='ForgetPasswordResponse':
    		password=msg['password']
    		self.labelStatus.config(text='Password:-"'+password+'"')
    	elif msg['code']=='0007':
    		self.labelStatus.config(text='Incorrect SeqA')
    	elif msg['code']=='0005':
    		self.labelStatus.config(text='UserName not exists')
    	else:
    		self.labelStatus.config(text='Error')
    		
class RequestMessage:

    def __init__(self,r,c=None,userName='',user='',cdType='',title=''):
        




        self.r=r
        self.user=user
        self.c=c
        self.cdType=cdType
        self.r.geometry('300x100')
        self.r.title(title)
        self.r.protocol('WM_DELETE_WINDOW',self.reject)
        label=tk.Label(self.r,text=user+' is Requesting for '+cdType)
        label.place(x=10,y=10)

        btnAccept=tk.Button(self.r,text='Accept',command=self.accept)
        btnAccept.place(x=50,y=50)

        btnReject=tk.Button(self.r,text='Reject',command=self.reject)
        btnReject.place(x=200,y=50)
        
        self.userName=userName

    def accept(self):
        title='ChatWindow-'+self.user
        self.c.requestResponseFor(self.user,self.cdType,'1')
        self.c.updatePartFriendControl(self.user,'_r'+self.cdType,'1')
        self.r.destroy()
        print(gx.MainWindow.windows)
        print(title)
        if title in gx.MainWindow.windows:

                cond=gx.MainWindow.windows[title]

                if cond:
                    pass
                else:
                    gx.MainWindow.windows[title]=True
                    root=tk.Toplevel()
                    root.geometry('1100x600+50+50')
                    gx.ChatMainWindow(root,self.c,self.userName,user,gx.MainWindow.windows,title)
                    root.mainloop()
        else:
                gx.MainWindow.windows[title]=True
                root=tk.Toplevel()
                root.geometry('1100x600+50+50')
                gx.ChatMainWindow(root,self.c,self.userName,self.user,gx.MainWindow.windows,title)
                root.mainloop()


    def reject(self):
        self.c.requestResponseFor(self.user,self.cdType,'0')
        self.c.updatePartFriendControl(self.user,'_r'+self.cdType,'0')
        self.r.destroy()

class RequestResponse:

    def __init__(self,r,user='',cdType='',title=''):
        self.r=r

        self.cdType=cdType
        self.r.geometry('300x100')
        self.r.title(title)
        self.r.protocol('WM_DELETE_WINDOW',self.accept)
        label=tk.Label(self.r,text=title)
        label.place(x=10,y=10)

        btnAccept=tk.Button(self.r,text='Accept',command=self.accept)
        btnAccept.place(x=50,y=50)



    def accept(self):


        self.r.destroy()

class MainWindow:
    windows={}
    winOpen={}

    def __init__(self,root,c,userName):
        self.userName=userName

        print("I AM MainWindow")
        btnWidth=12
        self.c=c
        self.root=root
        root.title('Main Window')
        frame=tk.Frame(root,height=600,width=1100)

        titleFrame=tk.Frame(height=50,width=1100)

        btnEditProfile=tk.Button(titleFrame,text='Edit Profile',width=btnWidth,command=self.editProfile)

        btnEditProfile.place(x=30,y=10)


        btnSequrity=tk.Button(titleFrame,text='Sequrity',width=btnWidth,command=self.sequrity)
        btnSequrity.place(x=130,y=10)

        self.mainStatus=tk.Label(titleFrame,text=self.userName,bg='yellow')
        self.mainStatus.place(x=300,y=10)

        btnRefress=tk.Button(titleFrame,text='Refress',width=btnWidth,command=self.refress)
        btnRefress.place(x=700,y=10)

        btnHelp=tk.Button(titleFrame,text='Help')
        btnHelp.place(x=1050,y=10)

        self.varTitleStatus=tk.StringVar(root)
        self.varTitleStatus.set('Welcome')


        self.labelTitleStatus=tk.Label(titleFrame,text=self.varTitleStatus.get(),bg='yellow')
        self.labelTitleStatus.place(x=900,y=10)

        leftFrame=tk.Frame(frame,bg='#daf9fb',height=500,width=700)


        llFrame=tk.Frame(leftFrame,bg='#F97F51',height=500,width=300)

        


        btnSearchFriend=tk.Button(llFrame,width=btnWidth,text='Search Friend',command=self.searchFriend)
        btnSearchFriend.place(x=150,y=10)


        btnBlockUnblock=tk.Button(llFrame,width=btnWidth,text='Block & Unblock',command=self.blockUnblock)
        btnBlockUnblock.place(x=30,y=50)


        btnFriendRequest=tk.Button(llFrame,width=btnWidth,text='Friend Request',command=self.friendRequest)
        btnFriendRequest.place(x=150,y=50)

        btnNotification=tk.Button(llFrame,width=btnWidth,text='Notification',command=self.notification)
        btnNotification.place(x=30,y=90)




        lrFrame=tk.Frame(leftFrame,bg='#d1d8e0',height=500,width=400)
        self.lrFrame=lrFrame
        labelTitle=tk.Label(lrFrame,text='Friends')
        labelTitle.place(x=30,y=30)

        entrySearchUser=tk.Entry(lrFrame)
        entrySearchUser.place(x=30,y=60)

        btnSearchEntry=tk.Button(lrFrame,text='Search')
        btnSearchEntry.place(x=230,y=60)

        self.lrDownFrame=tk.Frame(lrFrame,bg='grey',height=400,width=400)
  


        self.listFrame=tk.Frame(self.lrDownFrame,bg='#006266',height=400,width=380)
        self.listFrame.place(x=0,y=0)
        tFrame=tk.Frame(self.listFrame,bg='#006266',height=400,width=380)
        tFrame.place(x=0,y=0)

        self.listCont,self.can=gc.scrollableFrame(tFrame,400,380)



        self.lrDownFrame.place(y=100)

        llFrame.place(x=0,y=0)
        lrFrame.place(x=300,y=0)

        rightFrame=tk.Frame(frame,bg='#9980FA',height=500,width=400)

        bottomFrame=tk.Frame(frame,bg='#7ed6df',height=50,width=1100)

        btnSystemSettings=tk.Button(bottomFrame,text='System Settings',width=btnWidth,command=self.systemSettings)
        btnSystemSettings.place(x=30,y=10)

        btnLogOut=tk.Button(bottomFrame,text='LogOut',width=btnWidth,command=self.logOut)
        btnLogOut.place(x=140,y=10)

        leftFrame.place(x=0,y=50)
        rightFrame.place(x=700,y=50)
        bottomFrame.place(x=0,y=550)
        titleFrame.place(x=0,y=0)
        frame.place(x=0,y=0)
        self.imgdk={}
        self.refress()
        self.c.function2Type=self.dataHandler
        
    def controlFormalites(self):

            data=gx.MainWindow.winOpen

            if len(data)==0:
                pass
            else:
                cam=False
                mic=False
                for i in data:
                    d=data[i]
                    if d[1]==True:
                        cam=True
                    break

                for i in data:
                    d=data[i]
                    if d[2]==True:
                        mic=True
                    break

                if not cam:
                    self.offFormalitesCamera()

                if not mic:
                    self.offFormalitesMic()

    def dataHandler(self,msg):


                print("I AM DATA HANDLER TYPE ERROR MAY OCCUR")

                usr=msg['user']
                cdType=msg['cdType']
                if msg['ofType']=='Request':
                    title=usr+'_'+cdType
                    if title in gx.MainWindow.windows:
                        cond=gx.MainWindow.windows[title]
                        if cond:
                            pass
                        else:
                            gx.MainWindow.windows[title]=True
                            r=tk.Tk()
                            gx.RequestMessage(r,self.c,self.userName,usr,cdType,title)
                            r.mainloop()
                    else:
                        gx.MainWindow.windows[title]=True
                        r=tk.Tk()
                        gx.RequestMessage(r,self.c,self.userName,usr,cdType,title)
                        r.mainloop()
                elif msg['ofType']=='RequestResponse':
                    value=msg['value']

                    if value=='1':
                        title=usr+' Accepted '+cdType
                        r=tk.Tk()
                        gx.RequestResponse(r,usr,cdType,title)
                        r.mainloop()

                    else:
                        title=usr+' Rejected '+cdType
                        r=tk.Tk()
                        gx.RequestResponse(r,usr,cdType,title)
                        r.mainloop()

                else:
                    print("I dont know what you are searching")



                try:
                    if msg['wfType']=='UserData':
                        if msg['ofType']=='Request':
                            code=msg['code']
                            if code=='don4':
                                self.labelTitleStatus.config(text='User is not online')
                except:
                    pass


    def closeCamera(self):
        def fun():
            con.dStop()
        threading.Thread(target=fun).start()

    def closeMic(self):
        def fun():
            con.micStop()
        threading.Thread(target=fun).start()

    def onFormalitesCamera(self):
        def fun():
            con.on_camera()
            con.dStart()

        threading.Thread(target=fun).start()

    def offFormalitesCamera(self):
        def fun():
            con.dPause()


        threading.Thread(target=fun).start()

    def onFormalitesMic(self):
        def fun():


            con.on_mic()
            con.micStart()
            con.start()
        threading.Thread(target=fun).start()

    def offFormalitesMic(self):
        def fun():

            con.micPause()

        threading.Thread(target=fun).start()

    def refress(self):
        del self.lrDownFrame
        self.lrDownFrame=tk.Frame(self.lrFrame,bg='grey',height=400,width=400)
        self.lrDownFrame.place(y=100)
        self.listFrame=tk.Frame(self.lrDownFrame,bg='#006266',height=400,width=380)
        self.listFrame.place(x=0,y=0)
        tFrame=tk.Frame(self.listFrame,bg='#006266',height=400,width=380)
        tFrame.place(x=0,y=0)

        self.listCont,self.can=gc.scrollableFrame(tFrame,400,380)

        self.c.loadMainWindow()
        self.c.function1Type=self.handle

    def delReq(self,userName):


        self.c.deleteFriendRequest(userName)
        self.refress()

    def accReq(self,userName):
        self.c.FriendRequestAccept(userName)
        self.refress()

    def SearchLabelUser(self,sf,image,userName='',name='',color='yellow'):
        frame=tk.Frame(sf,height=130,width=400,bg=color)

        def chatWindow():
            def fun():


                #self.root.geometry('1100x600+50+50')
                title='ChatWindow-'+userName
                if title in gx.MainWindow.windows:

                    cond=gx.MainWindow.windows[title]
                    if cond:
                        pass
                    else:
                        gx.MainWindow.windows[title]=True
                        root=tk.Toplevel(self.root)
                        root.geometry('1100x600+50+50')
                        #self.onFormalitesCamera()
                        self.onFormalitesMic()
                        gx.MainWindow.winOpen[title]=[True,False,False]
                        gx.ChatMainWindow(root,self.c,self.userName,userName,gx.MainWindow.windows,title)

                else:
                    #self.onFormalitesCamera()
                    self.onFormalitesMic()
                    gx.MainWindow.winOpen[title]=[True,False,False]
                    gx.MainWindow.windows[title]=True
                    root=tk.Toplevel(self.root)
                    root.geometry('1100x600+50+50')
                    gx.ChatMainWindow(root,self.c,self.userName,userName,self.windows,title)
            threading.Thread(target=fun).start()

        label=tk.Label(frame,image=image,width=100,height=100)
        label.place(x=10,y=10)
        l2=tk.Label(frame,text=userName)
        l2.place(x=120,y=10)

        l3=tk.Label(frame,text=name)
        l3.place(x=120,y=40)



        btnChat=tk.Button(frame,text='ChatWindow',command=chatWindow)
        btnChat.place(x=120,y=80)
        frame.pack()


    def handle(self,msg):
    	if msg['wType']=='LoadMainWindowResponse':
    		self.labelTitleStatus.config(text='Updation Completed')
    		data=msg['profileData']
    		type=msg['profileType']
    		shape=msg['profileShape']
    		d=ds.remodifyData(data,type,shape)
    		if (len(d)!=0) and (d is not None) :
    			d=d[0]
    			for i in d:
    				usr=i[0]
    				nm=i[1]
    				im=i[2]
    				im=gc.cvtBin2Img2(im)
    				self.imgdk[usr]=im
    				self.SearchLabelUser(self.listCont,self.imgdk[usr],usr,nm)
    		else:
    			self.labelTitleStatus.config(text='No Records found')
    	else:
    		self.labelTitleStatus.config(text='Error')
                        


    def editProfile(self):
        for child in self.root.winfo_children():
            child.destroy()
        self.root.geometry('500x400')
        gx.EditProfile(self.root,self.c,self.userName,self.windows)

    def sequrity(self):
        for child in self.root.winfo_children():
            child.destroy()
        self.root.geometry('500x400')
        gx.Sequrity(self.root,self.c,self.userName,self.windows)

    

    def searchFriend(self):
        for child in self.root.winfo_children():
            child.destroy()
        
        self.root.geometry('500x400')
        gx.SearchFriend(self.root,self.c,self.userName,self.windows)

    def blockUnblock(self):
        for child in self.root.winfo_children():
            child.destroy()
        self.root.geometry('500x400')
        gx.BlockUnblock(self.root,self.c,self.userName,self.windows)

    def friendRequest(self):
        for child in self.root.winfo_children():
            child.destroy()
        self.root.geometry('500x400')
        gx.FriendRequest(self.root,self.c,self.userName,self.windows)

    def notification(self):
        for child in self.root.winfo_children():
            child.destroy()
        self.root.geometry('500x400')
        gx.Notification(self.root,self.c,self.userName,self.windows)


    def systemSettings(self):
        for child in self.root.winfo_children():
            child.destroy()
        self.root.geometry('1100x600+50+50')
        gx.SystemSettings(self.root,self.c,self.userName,self.windows)

    
    def logOut(self):
        for child in self.root.winfo_children():
            child.destroy()
        self.root.geometry('500x400')
        self.windows={}
        self.c.userName=''
        gx.Global(self.root,self.c)

class BlockUnblock:


    def __init__(self,root,c,userName,windows):
       
        self.windows=windows
        self.c=c
        
        self.userName=userName
        btnWidth=12
        entryWidth=25
        labelWidth=21
        self.root=root
        root.title('Block & Unblock')

        frame=tk.Frame(root,height=400,width=500)

        #Title
        titleFrame=tk.Frame(frame,bg='#006266',height=50,width=500)

        labelTitle=tk.Label(titleFrame,text='Block & Unblock',font="Helvetica 20 bold ",bg='yellow',fg='red')
        labelTitle.place(x=30,y=5)

        btnHelp=tk.Button(titleFrame,text='Help')
        btnHelp.place(x=450,y=5)

        btnRefress=tk.Button(titleFrame,text='Refress',width=btnWidth,command=self.refress)
        btnRefress.place(x=260,y=5)

        btnForward=tk.Button(titleFrame,text='Forward',width=btnWidth,command=self.forward)
        btnForward.place(x=360,y=5)


        downFrame=tk.Frame(frame,bg='grey',width=500,height=350)


        leftFrame=tk.Frame(downFrame,bg='#D6A2E8',width=250,height=350)

        labelLeftTitle=tk.Label(leftFrame,text='Block ',font="Helvetica 10 bold ",bg='yellow',fg='red')
        labelLeftTitle.place(x=30,y=5)

        self.labelStatus=tk.Label(leftFrame,text='Status')
        self.labelStatus.place(x=130,y=5)

        self.lvarUserName=tk.StringVar(root)
        self.lvarUserName.set('User Name')

        lentryUserName=tk.Entry(leftFrame,textvariable=self.lvarUserName,width=entryWidth)
        lentryUserName.place(x=30,y=50)

        lbtnSearch=tk.Button(leftFrame,text='search',width=btnWidth,command=self.searchl)
        lbtnSearch.place(x=30,y=90)

        #IN ONE
        self.leftFrame=leftFrame

        self.llistFrame=tk.Frame(leftFrame,bg='#006266',height=150,width=220)
        self.llistFrame.place(x=30,y=130)
        ltFrame=tk.Frame(self.llistFrame,bg='#006266',height=150,width=220)
        ltFrame.place(x=50,y=100)

        self.llistCont,self.can=gc.scrollableFrame(ltFrame,200,200)




        rightFrame=tk.Frame(downFrame,bg='#FEA47F',width=250,height=350)

        labelRightTitle=tk.Label(rightFrame,text='Unblock',font="Helvetica 10 bold ",bg='yellow',fg='red')
        labelRightTitle.place(x=30,y=5)



        rbtnSearch=tk.Button(rightFrame,text='Load',width=btnWidth,command=self.searchr)
        rbtnSearch.place(x=30,y=90)

        #IN ONE
        self.rightFrame=rightFrame
        self.rlistFrame=tk.Frame(self.rightFrame,bg='#006266',height=150,width=220)
        self.rlistFrame.place(x=30,y=130)
        rtFrame=tk.Frame(self.rlistFrame,bg='#006266',height=150,width=220)
        rtFrame.place(x=50,y=100)

        self.rlistCont,self.can=gc.scrollableFrame(rtFrame,200,180)




        leftFrame.place(x=0,y=0)
        rightFrame.place(x=250,y=0)
        downFrame.place(x=0,y=50)
        titleFrame.place(x=0,y=0)
        frame.place(x=0,y=0)
        self.imgdk={}

    def refress(self):
        del self.rlistFrame

        self.rlistFrame=tk.Frame(self.rightFrame,bg='#006266',height=150,width=220)
        self.rlistFrame.place(x=30,y=130)
        rtFrame=tk.Frame(self.rlistFrame,bg='#006266',height=150,width=220)
        rtFrame.place(x=50,y=100)

        self.rlistCont,self.can=gc.scrollableFrame(rtFrame,200,200)

        del self.llistFrame
        self.llistFrame=tk.Frame(self.leftFrame,bg='#006266',height=150,width=220)
        self.llistFrame.place(x=30,y=130)
        ltFrame=tk.Frame(self.llistFrame,bg='#006266',height=150,width=220)
        ltFrame.place(x=50,y=100)

        self.llistCont,self.can=gc.scrollableFrame(ltFrame,200,200)

        self.c.loadBlockUnblock()
        self.c.function1Type=self.handle

    def block(self,userName):
        self.c.block(userName)
        self.refress()

    def unblock(self,userName):
        self.c.unblock(userName)
        self.refress()

    def SearchLabelUserBlock(self,sf,image,userName='',color='yellow'):
  

        frame=tk.Frame(sf,height=130,width=300,bg=color)
        def block():
            print("KLDSF")
            self.block(userName)


        label=tk.Label(frame,image=self.imgdk[userName],width=100,height=100)
        label.place(x=10,y=10)
        l2=tk.Label(frame,text=userName)
        l2.place(x=120,y=10)
        self.imgdk[userName]=image

        btnDelRe=tk.Button(frame,text='Block',command=block)
        btnDelRe.place(x=120,y=40)


        frame.pack()

    def SearchLabelUserUnblock(self,sf,image,userName='',color='yellow'):
        frame=tk.Frame(sf,height=130,width=300,bg=color)
        def unblock():
            #print("HI")
            self.unblock(userName)

        self.imgdk[userName]=image
        label=tk.Label(frame,image=self.imgdk[userName],width=100,height=100)
        label.place(x=10,y=10)
        l2=tk.Label(frame,text=userName)
        l2.place(x=120,y=10)

        btnDelRe=tk.Button(frame,text='Unblock',command=unblock)
        btnDelRe.place(x=120,y=40)


        frame.pack()


    def handle(self,msg):
        if msg['wType']=='blockSearchResponse':
            data=msg['data']
            type=msg['type']
            shape=msg['shape']
            d=ds.remodifyData(data,type,shape)
            if d is not []:
                d=d[0]
                self.labelStatus.config(text='Data Restored')
                img=msg['img']
                img=gc.cvtBin2Img2(img)
                self.imgdk[d[0]]=img
                self.SearchLabelUserBlock(self.llistCont,self.imgdk[d[0]],d[0])
            else:
                self.labelStatus.config(text='No records found')
        elif msg['wType']=='UnblockResponse':
            data=msg['data']
            type=msg['type']
            shape=msg['shape']
            d=ds.remodifyData(data,type,shape)
            imgData=msg['imgData']
            imgType=msg['imgType']
            imgShape=msg['imgShape']
            dim=ds.remodifyData(imgData,imgType,imgShape)
            if d is []:
                self.labelStatus.config(text='No Recoreds found')
            else:
                self.labelStatus.config(text=str(d))
                for i in range(len(dim)):
                    im=gc.cvtBin2Img2(dim[i])
                    usr=d[i]
                    self.imgdk[usr]=im
                    self.SearchLabelUserUnblock(self.rlistCont,self.imgdk[usr],usr)

        elif msg['wType']=='LoadBlock&UnblockResponse':
            self.labelStatus.config(text='Data Restored')
        elif msg['code']=='0016':
            self.labelStatus.config(text='Blocked Successfull')
        elif msg['code']=='0017':
            self.labelStatus.config(text='Unblock Successfull')

        elif msg['code']=='0014':
            self.labelStatus.config(text='userName not exist')
        elif msg['code']=='0015':
            self.labelStatus.config(text='Same userName')


    def forward(self):
        for child in self.root.winfo_children():
            child.destroy()
        self.root.geometry('1100x600+50+50')
        gx.MainWindow.windows=self.windows
        gx.MainWindow(self.root,self.c,self.userName)
    def searchl(self):
        userName=self.lvarUserName.get()


        self.c.blockSearch(userName)
        self.types='BlockSearch'
        self.c.function1Type=self.handle
    def searchr(self):
        self.c.unblockLoad()
        self.types='UnblockLoad'
        self.c.function1Type=self.handle

class EditProfile:


    def __init__(self,root,c,userName,windows):
        
        self.windows=windows
        self.userName=userName
        self.c=c
        print("IMEDITOR")
        
        btnWidth=12
        entryWidth=25
        labelWidth=21
        self.image=None
        self.img=None
        self.root=root

        root.title('Edit Profile')

        frame=tk.Frame(root,height=400,width=500)

        #Title
        titleFrame=tk.Frame(frame,bg='#006266',height=50,width=500)

        labelTitle=tk.Label(titleFrame,text='Edit Profile',font="Helvetica 20 bold ",bg='yellow',fg='red')
        labelTitle.place(x=30,y=5)

        self.labelTitleStatus=tk.Label(titleFrame,text='Status')
        self.labelTitleStatus.place(x=200,y=5)

        btnRefress=tk.Button(titleFrame,text='Refress',width=btnWidth,command=self.refress)
        btnRefress.place(x=350,y=5)

        btnHelp=tk.Button(titleFrame,text='Help')
        btnHelp.place(x=450,y=5)


        downFrame=tk.Frame(frame,bg='grey',height=350,width=500)

        self.profileLabel=tk.Label(downFrame)
        self.profileLabel.place(x=30,y=20)




        setImage=tk.Button(downFrame,text='Set Image',command=self.fileDialog)
        setImage.place(x=30,y=230)



        self.varName=tk.StringVar(root)

        self.varStatusName=tk.StringVar(root)
        self.varStatusName.set('Change Name')


        labelStatusName=tk.Label(downFrame,text=self.varStatusName.get(),font="Helvetica 10 bold ",bg='yellow',fg='red')
        labelStatusName.place(x=250,y=20)

        entryName=tk.Entry(downFrame,textvariable=self.varName,width=18)
        entryName.place(x=250,y=60)

        varChNameStatus=tk.StringVar(root)
        varChNameStatus.set('Change Name Status')

        self.labelChNameStatus=tk.Label(downFrame,text=varChNameStatus.get(),font="Helvetica 10 bold ",bg='yellow',fg='red',wraplength=200)
        self.labelChNameStatus.place(x=250,y=100)


        btnUpdate=tk.Button(downFrame,text='Update',width=btnWidth,command=self.update)
        btnUpdate.place(x=250,y=180)

        btnForward=tk.Button(downFrame,text='Forward',width=btnWidth,command=self.forward)
        btnForward.place(x=400,y=180)

        downFrame.place(x=0,y=50)
        titleFrame.place(x=0,y=0)
        frame.place(x=0,y=0)
        self.conds=False
    def fileDialog(self):
        #fileName=filedialog.askopenfilename(initialdir='/',title='Hel',filetype=(('jpeg','*.jpg'),('All Files','*.*')))
        fileName=filedialog.askopenfilename(initialdir='/',title='select a file')
        #fileName=filedialog.askdirectory()
        self.image=fileName

    def refress(self):

        self.c.loadEditProfile()
        self.c.function1Type=self.handle
        
    def handle(self,msg):
       if msg['wType']=='EditProfileResponse':
            self.labelTitleStatus.config(text='Updation Completed')
            img=msg['img']
            imgtk=gc.cvtBin2Img2(img)
            self.img=imgtk
            self.profileLabel.config(image=self.img)
       elif msg['code']=='ee08':
            self.labelChNameStatus.config(text='Profile Updated')
       elif msg['code']=='dd08':
            self.labelChNameStatus.config(text='Name Updated')
       else:
            self.labelChNameStatus.config(text='Error')

    def forward(self):
        for child in self.root.winfo_children():
            child.destroy()
        self.root.geometry('1100x600+50+50')
        gx.MainWindow.windows=self.windows
        gx.MainWindow(self.root,self.c,self.userName)

    def update(self):
        name=self.varName.get()
        if name=='':
            name='_None'

        if self.image==None:
            img='_None'
        else:
            img=cv2.imread(self.image)
            img=cv2.resize(img,(200,200))
            img=bytes(img)
            img=ds.encb(img)
            img=img.decode()
        self.c.editProfile(name,img)
        self.types='EditProfile'
        self.c.function1Type=self.handle

class FriendRequest:


    def __init__(self,root,c,userName,windows):
        
        self.windows=windows
        self.c=c
        
        btnWidth=12
        self.userName=userName
        entryWidth=25
        labelWidth=21
        self.root=root
        root.title('Friend Request')

        frame=tk.Frame(root,height=400,width=500)

        #Title
        titleFrame=tk.Frame(frame,bg='#006266',height=50,width=500)

        labelTitle=tk.Label(titleFrame,text='Friend Request',font="Helvetica 20 bold ",bg='yellow',fg='red')
        labelTitle.place(x=30,y=5)

        btnHelp=tk.Button(titleFrame,text='Help')
        btnHelp.place(x=450,y=5)

        btnRefress=tk.Button(titleFrame,text='Refress',width=btnWidth,command=self.refress)
        btnRefress.place(x=240,y=5)

        btnForward=tk.Button(titleFrame,text='Forward',width=btnWidth,command=self.forward)
        btnForward.place(x=340,y=5)


        downFrame=tk.Frame(frame,bg='grey',height=350,width=500)

        self.labelStatus=tk.Label(downFrame,text='Status')
        self.labelStatus.place(x=50,y=0)


        self.downFrame=downFrame
        self.listFrame=tk.Frame(downFrame,bg='#006266',height=220,width=220)
        self.listFrame.place(x=50,y=40)
        tFrame=tk.Frame(self.listFrame,bg='#006266',height=220,width=220)
        tFrame.place(x=50,y=100)

        self.listCont,self.can=gc.scrollableFrame(tFrame,300,220)







        downFrame.place(x=0,y=50)
        titleFrame.place(x=0,y=0)
        frame.place(x=0,y=0)
        self.imgdk={}
    def refress(self):
        del self.listFrame
        self.listFrame=tk.Frame(self.downFrame,bg='#006266',height=220,width=220)
        self.listFrame.place(x=50,y=40)
        tFrame=tk.Frame(self.listFrame,bg='#006266',height=220,width=220)
        tFrame.place(x=50,y=100)

        self.listCont,self.can=gc.scrollableFrame(tFrame,300,220)

        self.c.loadFriendRequest()
        self.c.function1Type=self.handle

    def delReq(self,userName):
        self.c.deleteFriendRequest(userName)
        self.refress()
    def accReq(self,userName):
        self.c.FriendRequestAccept(userName)
        self.refress()
    def SearchLabelUser(self,sf,image,userName='',color='yellow'):
        frame=tk.Frame(sf,height=130,width=300,bg=color)
        def delr():
            self.delReq(userName)
        def accr():
            self.accReq(userName)

        label=tk.Label(frame,image=image,width=100,height=100)
        label.place(x=10,y=10)
        l2=tk.Label(frame,text=userName)
        l2.place(x=120,y=10)

        btnDelRe=tk.Button(frame,text='Delete Request',command=delr)
        btnDelRe.place(x=120,y=40)

        btn=tk.Button(frame,text='Accept Request',command=accr)
        btn.place(x=120,y=80)
        frame.pack()


    def handle(self,msg):
        if msg['wType']=='LoadFriendRequestResponse':
            data=msg['FriendRequestData']
            type=msg['FriendRequestType']
            shape=msg['FriendRequestShape']
            d1=msg['im']
            dt=msg['imtype']
            dts=msg['imshape']
            d=ds.remodifyData(data,type,shape)
            dd=ds.remodifyData(d1,dt,dts)
            for i in range(len(d)):
                img=dd[i]
                usr=d[i]
                img=gc.cvtBin2Img2(img)
                self.imgdk[usr]=img
                self.SearchLabelUser(self.listCont,self.imgdk[usr],usr)


            self.labelStatus.config(text=str('Data is restored'))
        elif msg['code']=='0099':
            self.labelStatus.config(text='Command Successful')
        elif msg['code']=='0097':
            self.labelStatus.config(text='Command Failure')
        elif msg['code']=='0020':
            self.labelStatus.config(text='Users blocked themselves')
        elif msg['code']=='0021':
            self.labelStatus.config(text='Successful Deletion')
        elif msg['code']=='0022':
            self.labelStatus.config(text='UserName not exist')


    def forward(self):
        for child in self.root.winfo_children():
            child.destroy()
        self.root.geometry('1100x600+50+50')
        gx.MainWindow(self.root,self.c,self.userName)

class Notification:


    def __init__(self,root,c,userName,windows):
        
        self.windows=windows
        self.c=c
        self.userName=userName
        
        btnWidth=12
        entryWidth=25
        labelWidth=21
        self.root=root

        root.title('Notification')

        frame=tk.Frame(root,height=400,width=500)

        #Title
        titleFrame=tk.Frame(frame,bg='#006266',height=50,width=500)

        labelTitle=tk.Label(titleFrame,text='Notfication',font="Helvetica 20 bold ",bg='yellow',fg='red')
        labelTitle.place(x=30,y=5)

        btnHelp=tk.Button(titleFrame,text='Help')
        btnHelp.place(x=450,y=5)

        btnForward=tk.Button(titleFrame,text='Forward',command=self.forward)
        btnForward.place(x=200,y=5)

        btnRefress=tk.Button(titleFrame,text='Refress',command=self.refress)
        btnRefress.place(x=350,y=5)

        downFrame=tk.Frame(frame,bg='grey',width=500,height=350)

        self.labelStatus=tk.Label(downFrame,text='Status')
        self.labelStatus.place(x=50,y=10)

        self.downFrame=downFrame
        self.listFrame=tk.Frame(downFrame,bg='#006266',height=220,width=220)
        self.listFrame.place(x=50,y=40)
        tFrame=tk.Frame(self.listFrame,bg='#006266',height=220,width=220)
        tFrame.place(x=50,y=100)

        self.listCont,self.can=gc.scrollableFrame(tFrame,300,220)




        downFrame.place(x=0,y=50)
        titleFrame.place(x=0,y=0)
        frame.place(x=0,y=0)

    def refress(self):
        del self.listFrame
        self.listFrame=tk.Frame(self.downFrame,bg='#006266',height=220,width=220)
        self.listFrame.place(x=50,y=40)
        tFrame=tk.Frame(self.listFrame,bg='#006266',height=220,width=220)
        tFrame.place(x=50,y=100)

        self.listCont,self.can=gc.scrollableFrame(tFrame,300,220)

        self.c.Notification(0,100)
        self.c.function1Type=self.handle
        

    def handle(self,msg):
    	if msg['wType']=='NotificationResponse':
            data=msg['data']
            type=msg['type']
            shape=msg['shape']
            d=ds.remodifyData(data,type,shape)
            for i in range(len(d)):
                if i%2==0:
                    gc.NotificationLabel(self.listCont,d[i],'yellow')
                else:
                    gc.NotificationLabel(self.listCont,d[i],'green')
            self.labelStatus.config(text='Data is restored')


    def forward(self):
        for child in self.root.winfo_children():
            child.destroy()
        self.root.geometry('1100x600+50+50')
        gx.MainWindow.windows=self.windows
        gx.MainWindow(self.root,self.c,self.userName)


class SearchFriend:


    def __init__(self,root,c,userName,windows):
        self.windows=windows
        
        self.c=c
        
        self.userName=userName
        btnWidth=12
        entryWidth=25
        labelWidth=21
        self.root=root
        root.title('Search Friend')
        self.uuusss=None
        frame=tk.Frame(root,height=400,width=500)
        self.imgs=None
        #Title
        titleFrame=tk.Frame(frame,bg='#006266',height=50,width=500)

        labelTitle=tk.Label(titleFrame,text='Search Friends',font="Helvetica 20 bold ",bg='yellow',fg='red')
        labelTitle.place(x=30,y=5)

        btnForward=tk.Button(titleFrame,text='Forward',command=self.forward)
        btnForward.place(x=250,y=5)

        btnRefress=tk.Button(titleFrame,text='Refress',width=btnWidth,command=self.refress)
        btnRefress.place(x=350,y=5)

        btnHelp=tk.Button(titleFrame,text='Help')
        btnHelp.place(x=450,y=5)

        downFrame=tk.Frame(frame,bg='grey',height=350,width=500)

        self.varUserName=tk.StringVar(root)
        self.varUserName.set('User Name')

        entryUserName=tk.Entry(downFrame,textvariable=self.varUserName,width=entryWidth)
        entryUserName.place(x=30,y=10)

        btnSearch=tk.Button(downFrame,text='Search!',width=btnWidth,command=self.search)
        btnSearch.place(x=250,y=10)

        self.labelStatus=tk.Label(downFrame,text='Status')
        self.labelStatus.place(x=350,y=10)




        self.downFrame=downFrame
        self.listFrame=tk.Frame(downFrame,bg='#006266',height=220,width=220)
        self.listFrame.place(x=50,y=40)
        tFrame=tk.Frame(self.listFrame,bg='#006266',height=220,width=220)
        tFrame.place(x=50,y=100)

        self.listCont,self.can=gc.scrollableFrame(tFrame,300,220)



        downFrame.place(x=0,y=50)
        titleFrame.place(x=0,y=0)
        frame.place(x=0,y=0)

    def refress(self):


        self.c.loadSearchFriend()
        self.c.function1Type=self.handle
        
    def handle(self,msg):
        if msg['wType']=='LoadSearchFriendResponse':
            self.labelStatus.config(text='Refress completd')
        elif msg['wType']=='searchFriendResponse':
            self.labelStatus.config(text='Data Restored')
            data=msg['data']
            type=msg['type']
            shape=msg['shape']
            d=ds.remodifyData(data,type,shape)
            if len(d)==0:
                self.labelStatus.config(text='No Records found')
            else:
                d=d[0]
                img=msg['img']
                userName=d[0]
                self.uuusss=userName
                name=d[1]
                img=gc.cvtBin2Img2(img)
                self.imgs=img
                self.SearchLabelUser(self.listCont,self.imgs,userName,name)

        elif msg['code']=='0002':
            self.labelStatus.config(text='UserName not found')
        elif msg['code']=='020202':
            self.labelStatus.config(text='Both are friends :-Search in Friend list')
        elif msg['code']=='0020':
            self.labelStatus.config(text='Users Block Themselves')
        elif msg['code']=='0021':
            self.labelStatus.config(text='FriendRequest sending Successful')
        elif msg['code']=='0022':
            self.labelStatus.config(text='userNot found')
        elif msg['code']=='22k22':
            self.labelStatus.config(text='Friend Request already sent')
                         
      


    def SearchLabelUser(self,sf,image,userName='',name='',color='yellow'):
        frame=tk.Frame(sf,height=130,width=300,bg=color)

        label=tk.Label(frame,image=image,width=100,height=100)
        label.place(x=10,y=10)
        l2=tk.Label(frame,text=userName)
        l2.place(x=120,y=10)

        l2=tk.Label(frame,text=name)
        l2.place(x=120,y=40)
        btn=tk.Button(frame,text='SendFriendRequest',command=self.sendFriendRequest)
        btn.place(x=120,y=80)
        frame.pack()

    def sendFriendRequest(self):
        userName=self.uuusss
        self.c.sendFriendRequest(userName)
        self.labelStatus.config(text='FriendRequest Sent')
        self.c.function1Type=self.handle

    def forward(self):
        for child in self.root.winfo_children():
            child.destroy()
        self.root.geometry('1100x600+50+50')
        gx.MainWindow.windows=self.windows
        gx.MainWindow(self.root,self.c,self.userName)
    def search(self):
        del self.listFrame
        self.listFrame=tk.Frame(self.downFrame,bg='#006266',height=220,width=220)
        self.listFrame.place(x=50,y=40)
        tFrame=tk.Frame(self.listFrame,bg='#006266',height=220,width=220)
        tFrame.place(x=50,y=100)

        self.listCont,self.can=gc.scrollableFrame(tFrame,300,220)
        userName=self.varUserName.get()


        self.c.searchFriend(userName)
        self.c.function1Type=self.handle        

class Sequrity:


    def __init__(self,root,c,userName,windows):
        #GL
        #GO
        self.windows=windows
        self.c=c
        self.userName=userName
        
        btnWidth=14
        entryWidth=25
        labelWidth=21
        self.root=root
        root.title('Sequrity')

        frame=tk.Frame(root,height=400,width=500)

        #Title
        titleFrame=tk.Frame(frame,bg='#006266',height=50,width=500)

        labelTitle=tk.Label(titleFrame,text='Sequrity',font="Helvetica 20 bold ",bg='yellow',fg='red')
        labelTitle.place(x=30,y=5)


        downFrame=tk.Frame(frame,bg='grey',height=350,width=500)


        btnChangePassword=tk.Button(downFrame,text='Change Passowrds',width=btnWidth,command=self.changePassword)
        btnChangePassword.place(x=100,y=50)

        btnChangeSeqQA=tk.Button(downFrame,text='Change Seq-Q&A',width=btnWidth,command=self.changeSeqQA)
        btnChangeSeqQA.place(x=100,y=90)

        btnBack=tk.Button(downFrame,text='Back',width=btnWidth,command=self.back)
        btnBack.place(x=100,y=130)

        downFrame.place(x=0,y=50)
        titleFrame.place(x=0,y=0)
        frame.place(x=0,y=0)

    def changePassword(self):
        for child in self.root.winfo_children():
            child.destroy()
        self.root.geometry('500x400')
        gx.ChangePasswords(self.root,self.c,self.userName,self.windows)


    def changeSeqQA(self):
        for child in self.root.winfo_children():
            child.destroy()
        self.root.geometry('500x400')
        gx.ChangeSeqQA(self.root,self.c,self.userName,self.windows)

    def back(self):
        for child in self.root.winfo_children():
            child.destroy()
        self.root.geometry('1100x600+50+50')
        gx.MainWindow.windows=self.windows
        gx.MainWindow(self.root,self.c,self.userName)

class SystemSettings:


    def __init__(self,root,c,userName,windows):
        #GL
        #GO
        self.windows=windows
        self.c=c
        
        self.userName=userName
        btnWidth=12
        entryWidth=25
        labelWidth=21
        self.root=root
        root.title('System Settings')

        frame=tk.Frame(root,height=600,width=1100)

        #Title
        titleFrame=tk.Frame(frame,bg='#006266',height=50,width=1100)

        labelTitle=tk.Label(titleFrame,text='System Settings',font="Helvetica 20 bold ",bg='yellow',fg='red')
        labelTitle.place(x=30,y=5)

        btnHelp=tk.Button(titleFrame,text='Help')
        btnHelp.place(x=1050,y=5)

        btnForward=tk.Button(titleFrame,text='Forward', width=btnWidth,command=self.forward)
        btnForward.place(x=300,y=5)

        downFrame=tk.Frame(frame,bg='grey',height=550,width=1100)


        labelTempStatus=tk.Label(downFrame,text='This option Will Be comming Soon',font='Helvetica 20 bold' ,bg='red',fg='white')
        labelTempStatus.place(x=30,y=200)


        downFrame.place(x=0,y=50)
        titleFrame.place(x=0,y=0)
        frame.place(x=0,y=0)

    def forward(self):
        for child in self.root.winfo_children():
            child.destroy()
        self.root.geometry('1100x600+50+50')
        gx.MainWindow.windows=self.windows
        gx.MainWindow(self.root,self.c,self.userName)

class ChangePasswords:


    def __init__(self,root,c,userName,windows):
        #GL
        #GO
        self.windows=windows
        self.c=c
        self.userName=userName
        
        btnWidth=14
        entryWidth=25
        labelWidth=21
        self.root=root
        root.title('Change Passwords')

        frame=tk.Frame(root,height=400,width=500)

        #Title
        titleFrame=tk.Frame(frame,bg='#006266',height=50,width=500)

        labelTitle=tk.Label(titleFrame,text='Change Passwords',font="Helvetica 20 bold ",bg='yellow',fg='red')
        labelTitle.place(x=30,y=5)

        btnHelp=tk.Button(titleFrame,text='Help')
        btnHelp.place(x=450,y=5)


        btnForward=tk.Button(titleFrame,text='Forward',width=btnWidth,command=self.forward)
        btnForward.place(x=300,y=5)

        downFrame=tk.Frame(frame,bg='grey',height=350,width=500)

        self.varCurrentPassword=tk.StringVar(root)
        self.varNewPassword=tk.StringVar(root)

        self.varCurrentPassword.set('Current Passwords')
        self.varNewPassword.set('New Passwords')


        entryCurrentPassword=tk.Entry(downFrame,textvariable=self.varCurrentPassword,width=18)
        entryCurrentPassword.place(x=100,y=30)

        entryNewPassword=tk.Entry(downFrame,textvariable=self.varNewPassword,width=18)
        entryNewPassword.place(x=100,y=70)

        btnUpdate=tk.Button(downFrame,text='Update',width=btnWidth,command=self.update)
        btnUpdate.place(x=100,y=130)

        self.labelStatus=tk.Label(downFrame,text='Status')
        self.labelStatus.place(x=100,y=190)

        downFrame.place(x=0,y=50)
        titleFrame.place(x=0,y=0)
        frame.place(x=0,y=0)



    def forward(self):
        for child in self.root.winfo_children():
            child.destroy()
        self.root.geometry('500x400')
        gx.Sequrity(self.root,self.c,self.userName,self.windows)
    def handle(self,msg):
    	
        if msg['code']=='0010':
            self.labelStatus.config(text='Updation Completed')
        elif msg['code']=='0009':
            self.labelStatus.config(text='Password was incorrect')
        else:
            self.labelStatus.config(text='Error')



    def update(self):
        currP=self.varCurrentPassword.get()
        newP=self.varNewPassword.get()
        self.c.changePassword(newP,currP)
        self.c.function1Type=self.handle
        


class ChangeSeqQA:


    def __init__(self,root,c,userName,windows):
        #GL
        self.windows=windows
        #GO
        self.c=c
        
        btnWidth=14
        entryWidth=25
        labelWidth=21
        self.userName=userName
        self.root=root
        root.title('Change Seq Q & A')

        frame=tk.Frame(root,height=400,width=500)

        #Title
        titleFrame=tk.Frame(frame,bg='#006266',height=50,width=500)

        labelTitle=tk.Label(titleFrame,text='Change Seq Q & A',font="Helvetica 20 bold ",bg='yellow',fg='red')
        labelTitle.place(x=30,y=5)

        btnHelp=tk.Button(titleFrame,text='Help')
        btnHelp.place(x=450,y=5)

        btnForward=tk.Button(titleFrame,text='Forward',width=btnWidth,command=self.forward)
        btnForward.place(x=300,y=5)


        downFrame=tk.Frame(frame,bg='grey',height=350,width=500)

        self.varCurrentPassword=tk.StringVar(root)
        self.varSeqQ=tk.StringVar(root)
        self.varSeqA=tk.StringVar(root)

        self.varCurrentPassword.set('Current Passwords')
        self.varSeqQ.set('Sequrity Question')
        self.varSeqA.set('Sequrity Answer')


        entryCurrentPassword=tk.Entry(downFrame,textvariable=self.varCurrentPassword,width=entryWidth)
        entryCurrentPassword.place(x=100,y=30)

        entrySeqQ=tk.Entry(downFrame,textvariable=self.varSeqQ,width=entryWidth)
        entrySeqQ.place(x=100,y=70)

        entrySeqA=tk.Entry(downFrame,textvariable=self.varSeqA,width=entryWidth)
        entrySeqA.place(x=100,y=110)





        btnUpdate=tk.Button(downFrame,text='Update',width=btnWidth,command=self.update)
        btnUpdate.place(x=100,y=170)

        self.labelStatus=tk.Label(downFrame,text='Status')
        self.labelStatus.place(x=100,y=230)

        downFrame.place(x=0,y=50)
        titleFrame.place(x=0,y=0)
        frame.place(x=0,y=0)

    def forward(self):
        for child in self.root.winfo_children():
            child.destroy()
        self.root.geometry('500x400')
        gx.Sequrity(self.root,self.c,self.userName,self.windows)

    def handle(self,msg):
        if msg['code']=='0012':
            self.labelStatus.config(text='Updation Completed')
        elif msg['code']=='0011':
            self.labelStatus.config(text='Password was incorrect')
        else:
            self.labelStatus.config(text='Errorsldfks')



    def update(self):
        curP=self.varCurrentPassword.get()
        seqQ=self.varSeqQ.get()
        seqA=self.varSeqA.get()
        self.c.changeSeqQA(curP,seqQ,seqA)
        self.c.function1Type=self.handle




class ChatMainWindow:

    #def __init__(self,root):

    def __init__(self,root,c,userName,user,windows,title):
        btnWidth=12
        self.title=title
        self.windows=windows
        self.info={}
        self.info2={}
        self.root=root
        self.c=c
        self.userName=userName
        self.user=user
        self.sendCondition=False
        #title='kkr'
        self.filetoSend=None
        root.title(title)
        frame=tk.Frame(root,height=600,width=1100)



        chatGridFrame=tk.Frame(frame,bg='#45aaf2',height=400,width=300)
        labelChatTitle=tk.Label(chatGridFrame,text='Chat Label')
        labelChatTitle.place(x=10,y=10)

        self.labelChatOnline=tk.Label(chatGridFrame,bg='Green',width=2)
        self.labelChatOnline.place(x=100,y=10)

        btnSendFile=tk.Button(chatGridFrame,text='Send-Files',command=self.sendFile)
        btnSendFile.place(x=200,y=10)
        
        btnSetFile=tk.Button(chatGridFrame,text='Set File',command=self.setFile)
        btnSetFile.place(x=150,y=10)



        self.chatWindow=tk.Frame(chatGridFrame,bg='grey',height=300,width=280)
        #self.chatWindow.place(x=10,y=40)



        self.listFrame=tk.Frame(chatGridFrame,bg='#006266',height=300,width=280)
        self.listFrame.place(x=10,y=40)
        tFrame=tk.Frame(self.listFrame,bg='#006266',height=300,width=250)
        tFrame.place(x=50,y=100)

        self.listCont,self.can=gc.scrollableFrame(tFrame,300,220)


        self.varChatMessage=tk.StringVar()


        entryChat=tk.Entry(chatGridFrame,width=30,textvariable=self.varChatMessage)
        entryChat.place(x=10,y=360)

        btnChat=tk.Button(chatGridFrame,text='Send',width=10,command=self.sendChat)
        btnChat.place(x=210,y=360)

        #----------------------------------
        ScreenFrame=tk.Frame(frame,bg='#778ca3',height=300,width=500)


        labelScreenTitle=tk.Label(ScreenFrame,text='Screen Label')
        labelScreenTitle.place(x=10,y=10)

        self.labelScreenOnline=tk.Label(ScreenFrame,bg='Green',width=2)
        self.labelScreenOnline.place(x=100,y=10)

        btnRequestScreen=tk.Button(ScreenFrame,text='Request-Screen',command=self.requestScreen)
        btnRequestScreen.place(x=200,y=10)

        self.labelScreenShow=tk.Label(ScreenFrame,width=600,height=300)
        self.labelScreenShow.place(x=10,y=40)



        #---------------------------


        mouseFrame=tk.Frame(frame,bg='#D6A2E8',height=200,width=300)

        labelMouseFrame=tk.Label(mouseFrame,text='Mouse Label')
        labelMouseFrame.place(x=10,y=10)

        self.labelMouseOnline=tk.Label(mouseFrame,bg='Green',width=2)
        self.labelMouseOnline.place(x=100,y=10)

        btnRequestMouse=tk.Button(mouseFrame,text='Request-Mouse',command=self.requestMouse)
        btnRequestMouse.place(x=200,y=10)

        btnStartMouseSending=tk.Button(mouseFrame,text='Start-Sending',command=self.mouseSender)
        btnStartMouseSending.place(x=10,y=40)

        labelForExitMouse=tk.Label(mouseFrame,text='Press "Esc" from sending \n mouse control')
        labelForExitMouse.place(x=10,y=70)


        #--------------------
        keyboardFrame=tk.Frame(frame,bg='#f7b731',height=250,width=500)

        labelKeyboardFrame=tk.Label(keyboardFrame,text='Keyboard Label')
        labelKeyboardFrame.place(x=10,y=10)

        self.labelKeyboardOnline=tk.Label(keyboardFrame,bg='Green',width=2)
        self.labelKeyboardOnline.place(x=100,y=10)

        btnRequestKeyboard=tk.Button(keyboardFrame,text='Request-Keyboard',command=self.requestKeyboard)
        btnRequestKeyboard.place(x=10,y=40)

        btnStartKeyboardSending=tk.Button(keyboardFrame,text='Start-Sending',command=self.keyboardSender)
        btnStartKeyboardSending.place(x=10,y=70)

        btnStopKeyboardSending=tk.Button(keyboardFrame,text='Stop-Sending',command=self.keyboardBreak)
        btnStopKeyboardSending.place(x=10,y=100)

        #-----------------------------

        userSettingFrame=tk.Frame(frame,bg='grey',width=300,height=100)
        labelUserSettingFrame=tk.Label(userSettingFrame,text='UserSetting label')
        labelUserSettingFrame.place(x=10,y=10)

        self.labelOnline=tk.Label(userSettingFrame,bg='Green',width=2)
        self.labelOnline.place(x=130,y=10)

        #-----------------------------
        CameraFrame=tk.Frame(frame,bg='#9AECDB',width=300,height=300)
        labelCameraFrame=tk.Label(CameraFrame,text='Camera Frame')
        labelCameraFrame.place(x=10,y=10)

        self.labelCameraShow=tk.Label(CameraFrame,width=250,height=250)
        self.labelCameraShow.place(x=10,y=40)

        self.labelCameraFrame=tk.Label(CameraFrame,bg='Green',width=2)
        self.labelCameraFrame.place(x=100,y=10)

        btnRequestCamera=tk.Button(CameraFrame,text='Request-Camera',command=self.requestCamera)
        btnRequestCamera.place(x=200,y=10)



        #-----------------------------
        bottomFrame=tk.Frame(frame,bg='#2C3A47',width=800,height=50)
        labelBottomFrame=tk.Label(bottomFrame,text='Label Bottom Frame')
        labelBottomFrame.place(x=10,y=10)

        btnMainWindow=tk.Button(bottomFrame,text='MainWindow')
        btnMainWindow.place(x=200,y=10)

        btnRefress=tk.Button(bottomFrame,text='Refress',command=self.refress)
        btnRefress.place(x=300,y=10)



        self.labelStatus=tk.Label(bottomFrame,text='I am Status')
        self.labelStatus.place(x=380,y=10)


        #--------------------------------------------

        VoiceFrame=tk.Frame(frame,height=150,width=300,bg='red')
        labelVoiceFrame=tk.Label(VoiceFrame,text='Voice Label')
        labelVoiceFrame.place(x=10,y=10)

        self.labelVoiceOnline=tk.Label(VoiceFrame,bg='Green',width=2)
        self.labelVoiceOnline.place(x=100,y=10)

        btnRequestVoice=tk.Button(VoiceFrame,text='Request-Voice',command=self.requestVoice)
        btnRequestVoice.place(x=200,y=10)


        #-------------------------------------------
        userControl=tk.Frame(frame,height=250,width=300,bg='grey')

        self.varSScreen=tk.IntVar(self.root)
        self.varSCamera=tk.IntVar(self.root)
        self.varSMouse=tk.IntVar(self.root)
        self.varSKeyboard=tk.IntVar(self.root)
        self.varSVoice=tk.IntVar(self.root)

        self.varRScreen=tk.IntVar(self.root)
        self.varRCamera=tk.IntVar(self.root)
        self.varRMouse=tk.IntVar(self.root)
        self.varRKeyboard=tk.IntVar(self.root)
        self.varRVoice=tk.IntVar(self.root)

        sAScreen=tk.Radiobutton(userControl,text='SScreen 1',variable=self.varSScreen,value=1)
        sACamera=tk.Radiobutton(userControl,text='SCamera 1',variable=self.varSCamera,value=1)
        sAMouse=tk.Radiobutton(userControl,text='SMouse 1',variable=self.varSMouse,value=1)
        sAKeyboard=tk.Radiobutton(userControl,text='SKeyboard 1',variable=self.varSKeyboard,value=1)
        sAVoice=tk.Radiobutton(userControl,text='SVoice 1',variable=self.varSVoice,value=1)

        sAScreen.place(x=2)
        sACamera.place(x=2,y=30)
        sAMouse.place(x=2,y=60)

        sAKeyboard.place(x=2,y=90)
        sAVoice.place(x=2,y=120)

        sBScreen=tk.Radiobutton(userControl,text='0',variable=self.varSScreen,value=0)
        sBCamera=tk.Radiobutton(userControl,text='0',variable=self.varSCamera,value=0)
        sBMouse=tk.Radiobutton(userControl,text='0',variable=self.varSMouse,value=0)
        sBKeyboard=tk.Radiobutton(userControl,text='0',variable=self.varSKeyboard,value=0)
        sBVoice=tk.Radiobutton(userControl,text='0',variable=self.varSVoice,value=0)

        sBScreen.place(x=100)
        sBCamera.place(x=100,y=30)
        sBMouse.place(x=100,y=60)

        sBKeyboard.place(x=100,y=90)
        sBVoice.place(x=100,y=120)



        #jsdfkjsfjkjksd


        rAScreen=tk.Radiobutton(userControl,text='RScreen 1',variable=self.varRScreen,value=1)
        rACamera=tk.Radiobutton(userControl,text='RCamera 1',variable=self.varRCamera,value=1)
        rAMouse=tk.Radiobutton(userControl,text='RMouse 1',variable=self.varRMouse,value=1)
        rAKeyboard=tk.Radiobutton(userControl,text='RKeyboard 1',variable=self.varRKeyboard,value=1)
        rAVoice=tk.Radiobutton(userControl,text='RVoice 1',variable=self.varRVoice,value=1)

        rAScreen.place(x=150)
        rACamera.place(x=150,y=30)
        rAMouse.place(x=150,y=60)

        rAKeyboard.place(x=150,y=90)
        rAVoice.place(x=150,y=120)

        rBScreen=tk.Radiobutton(userControl,text='0',variable=self.varRScreen,value=0)
        rBCamera=tk.Radiobutton(userControl,text='0',variable=self.varRCamera,value=0)
        rBMouse=tk.Radiobutton(userControl,text='0',variable=self.varRMouse,value=0)
        rBKeyboard=tk.Radiobutton(userControl,text='0',variable=self.varRKeyboard,value=0)
        rBVoice=tk.Radiobutton(userControl,text='0',variable=self.varRVoice,value=0)

        rBScreen.place(x=250)
        rBCamera.place(x=250,y=30)
        rBMouse.place(x=250,y=60)

        rBKeyboard.place(x=250,y=90)
        rBVoice.place(x=250,y=120)

        btnUpdate=tk.Button(userControl,text='Update',command=self.update)
        btnUpdate.place(x=10,y=200)

        #--------------------------------------------
        bottomFrame.place(x=300,y=550)
        CameraFrame.place(x=800,y=100)

        userSettingFrame.place(x=800,y=0)
        keyboardFrame.place(x=300,y=300)
        userControl.place(x=500,y=300)
        mouseFrame.place(x=0,y=400)
        ScreenFrame.place(x=300,y=0)
        chatGridFrame.place(x=0,y=0)
        VoiceFrame.place(x=800,y=400)
        frame.place(x=0,y=0)

        self.img={}

        self.root.protocol('WM_DELETE_WINDOW',self.onClose)
        threading.Thread(target=self.refress).start()

        self.dimg={}
        self.imgCount=0

        self.cimg={}
        self.cimgCount=0
        self.sender()
        self.keyboardListener=False
        self.c.functionList[user]=[self.handle,self.dataHandler]
    def update(self):

        val=[self.varSScreen,self.varSCamera,self.varSVoice,self.varSMouse,self.varSKeyboard ,\
             self.varRScreen,self.varRCamera,self.varRVoice,self.varRMouse,self.varRKeyboard]

        values=[]
        for i in val:
            values.append(str(i.get()))
        print(values)
        self.c.updateFriendControls(self.user,values)
        



    def radActCamera(self):
        d=gx.MainWindow.winOpen[self.title]
        val=d[2]
        data=self.varSCamera.get()
        if data==0:
            gx.MainWindow.winOpen[self.title]=[True,False,val]
        else:
            gx.MainWindow.winOpen[self.title]=[True,True,val]
        gx.MainWindow.controlFormalites()
    def radActMic(self):

        d=gx.MainWindow.winOpen[self.title]
        val=d[1]
        data=self.varSVoice.get()

        if data==0:
            gx.MainWindow.winOpen[self.title]=[True,val,False]
        else:
            gx.MainWindow.winOpen[self.title]=[True,val,True]
        gx.MainWindow.controlFormalites()

    def requestScreen(self):
        self.c.requestFor(self.user,'Screen')
        self.c.updatePartFriendControl(self.user,'_sScreen','1')

    def requestMouse(self):
        self.c.requestFor(self.user,'Mouse')
        self.c.updatePartFriendControl(self.user,'_sMouse','1')

    def requestKeyboard(self):
        self.c.requestFor(self.user,'Keyboard')
        self.c.updatePartFriendControl(self.user,'_sKeyboard','1')

    def requestCamera(self):
        self.c.requestFor(self.user,'Camera')
        self.c.updatePartFriendControl(self.user,'_sCamera','1')

    def requestVoice(self):
        self.c.requestFor(self.user,'Voice')
        self.c.updatePartFriendControl(self.user,'_sVoice','1')

    def onClose(self):
        gx.MainWindow.windows[self.title]=False
        del gx.MainWindow.winOpen[self.title]#=[False,False,False]
        self.c.loadChatWindow(self.user,'False')
        self.root.destroy()

    def keyboardSender(self):
        threading.Thread(target=keyboard.mStart).start()
        #keyboard.mStart()
        self.keyboardListener=True

    def keyboardBreak(self):


        keyboard.mStop()

    def mouseSender(self):
        def fun():
            if self.keyboardListener==False:
                keyboard.mStart()

            keyboard.keyPress='Key.esc'
            keyboard.actionPress=self.mouseBreak

            mouse.mStart()
            self.mouseFreez=True
            #self.onFreez((500,500))
            #self.root.config(cursor='none')
        threading.Thread(target=fun).start()
    def onFreez(self,pos):

        def fun():
            while True:
                mouse.setPosition(pos)
                if not self.mouseFreez:
                    break
        threading.Thread(target=fun).start()


    def mouseBreak(self):
        self.mouseFreez=False
        mouse.mStop()

    def refress(self):


        self.c.loadChatWindow(self.user,'True')
        self.types='LoadChatWindow'



    def dataHandler(self,msg):

                

                ofType=msg['ofType']

                #print(ofType)

                if ofType=='_Screen':

                    data=msg['screenData']
                    type=msg['screenType']
                    shape=msg['screenShape']
                    d=ds.remodifyData(data,type,shape)
                    d=cv2.cvtColor(d,cv2.COLOR_BGR2RGB)
                    img=gc.cvtIntoLabelImage(d)


                    self.labelScreenShow.config(image=img)
                    
                    self.imgCount=self.imgCount+1

                elif ofType=='_Camera':
                    data=msg['cameraData']
                    type=msg['cameraType']
                    shape=msg['cameraShape']
                    d=ds.remodifyData(data,type,shape)
                    d=cv2.cvtColor(d,cv2.COLOR_BGR2RGB)
                    img=gc.cvtIntoLabelImage(d)

                    if self.cimgCount%2==0:
                        self.cimgCount=1
                    else:
                        self.cimgCount=0
                    self.cimg[self.cimgCount]=img
                    self.labelCameraShow.config(image=self.cimg[self.cimgCount])
                    
                    self.cimgCount=self.cimgCount+1

                elif ofType=='_Voice':
                    data=msg['voiceData']
                    data=ds.decb(bytes(data,'utf-8'))
                    if data is  None:
                        print("I AM Voice NONE")
                    else:
                        stream=con.micStream
                        con.play_Voice(stream,data)

                elif ofType=='_Keyboard':
                    data=msg['keyboardData']
                    type=msg['keyboardType']
                    shape=msg['keyboardShape']
                    d=ds.remodifyData(data,type,shape)


                    if len(d)==0 or d is None:
                        pass
                    else:
                        for i in d:

                            keyboard.response(i)
                elif ofType=='_Mouse':
                    data=msg['mouseData']
                    type=msg['mouseType']
                    shape=msg['mouseShape']
                    d=ds.remodifyData(data,type,shape)

                    if len(d)==0 or d is None:
                        pass
                    else:
                        for i in d:
                            mouse.response(i)
                elif ofType=='_Text':
                    text=msg['text']
                    user=msg['user']
                    frame=tk.Frame(self.listCont,height=40,width=280,bg='red')
                    label=tk.Label(frame,text=text)
                    label.place(x=10,y=10)
                    frame.pack()
                    #self.c._Text(msg,self.user)

    def handle(self,msg):
        

        if msg['ofType']=='LoadChatWindow':
                             data=msg['data']
                             type=msg['type']
                             shape=msg['shape']
                             col=[ '_sScreen', '_sCamera', '_sVoice', '_sMouse', '_sKeyboard', '_rScreen', '_rCamera', '_rVoice', '_rMouse', '_rKeyboard']

                             d=ds.remodifyData(data,type,shape)
                             if len(d)==0:
                                 pass
                             else:
                                 d=d[0][2:]

                                 info=ad.cvtArr2Dict(col,d)






                                 data2=msg['data2']
                                 type2=msg['type2']
                                 shape2=msg['shape2']

                                 d2=ds.remodifyData(data2,type2,shape2)
                                 d2=d2[0][2:]
                                 info2=ad.cvtArr2Dict(col,d2)

                                 self.varSScreen.set(int(info2['_sScreen']))
                                 self.varSCamera.set(int(info2['_sCamera']))
                                 self.varSVoice.set(int(info2['_sVoice']))
                                 self.varSKeyboard.set(int(info2['_sKeyboard']))
                                 self.varSMouse.set(int(info2['_sMouse']))

                                 self.varRScreen.set(int(info2['_rScreen']))
                                 self.varRCamera.set(int(info2['_rCamera']))
                                 self.varRVoice.set(int(info2['_rVoice']))
                                 self.varRKeyboard.set(int(info2['_rKeyboard']))
                                 self.varRMouse.set(int(info2['_rMouse']))

                                 user=msg['user']
                                 self.info[user]=info
                                 self.info2[user]=info2
                                 self.labelStatus.config(text='Loading Completed')


                                 chatData=msg['chatData']
                                 chatType=msg['chatType']
                                 chatShape=msg['chatShape']

                                 chatData=ds.remodifyData(chatData,chatType,chatShape)


                                 self.handleChatInfo(chatData)

                                 #self.sender()
                                 self.sendCondition=True

        elif msg['code']=='d26d':
            self.labelStatus.config(text='TUpdation Completed')
        elif msg['code']=='d27d':
            self.labelStatus.config(text='ReUpdation Completed')
        else:
            self.labelStatus.config(text='Error')





    def sender(self):
        def fun():

            while True :
                if self.sendCondition:
                    info=self.info2[self.user]
                    #print(int(info['_sScreen']))

                    if int(info['_sScreen']):
                        data=con.screenFrame
                        if data is None:
                            print("Screen is none")
                        else:
                            self.c._Screen(data,self.user)
                    if int(info['_sCamera']):
                        data=con.camFrame
                        if data is None:
                            print("Camera is None")
                        else:
                            self.c._Camera(data,self.user)

                    if int(info['_sVoice']):
                        data=con.micFrame
                        if data is None:
                            print("MUJKO TO KOI AUE DIKAT HAI")
                        else:
                            self.c._Voice(data,self.user)
                    if int(info['_sMouse']):
                        data=mouse.buttons
                        if data==[]:
                            pass
                        else:
                            mouse.clear()
                            self.c._Mouse(data,self.user)
                    if int(info['_sKeyboard']):

                        data=keyboard.keys
                        #print(data)
                        if data==[]:
                            pass
                        else:

                            keyboard.clear()
                            self.c._Keyboard(data,self.user)





        threading.Thread(target=fun).start()

    def sendChat(self):
        msg=self.varChatMessage.get()
        if msg=='':
            pass
        else:
            frame=tk.Frame(self.listCont,height=50,width=250,bg='red')
            fmsg=self.userName+'->'+msg
            label=tk.Label(frame,text=fmsg)
            label.place(x=10,y=10)
            frame.pack()
            self.can.yview_moveto(1)
            self.c._Text(msg,self.user)
            self.varChatMessage.set('')

    def genFileLabelSend(self,file):
        frame=tk.Frame(self.listCont,height=100,width=250,bg='red')
        label1=tk.Label(frame,text=file)
        label1.place(x=10,y=10)

        label2=tk.Label(frame,text='Sending...')
        label2.place(x=10,y=40)
        stat=os.stat(file)
        size=stat.st_size
        mb=ds.Recv.get_mb(1,size)
        mb=round(mb,3)
        stat='0/{0} mb'.format(mb)
        labelStatus=tk.Label(frame,text=stat)
        labelStatus.place(x=10,y=70)
        frame.pack()
        return frame

    def genFileLabelRecv(self,listCont,file):
        frame=tk.Frame(listCont,height=100,width=250,bg='red')
        label1=tk.Label(frame,text=file)
        label1.place(x=10,y=10)

        label2=tk.Label(frame,text='Recving...')
        label2.place(x=10,y=40)
        stat=os.stat(file)
        size=stat.st_size
        mb=ds.Recv.get_mb(size)
        mb=round(mb,3)
        stat='0/{0} mb'.format(mb)
        labelStatus=tk.Label(frame,text=stat)
        labelStatus.place(x=10,y=70)
        frame.pack()
        return frame

    def updateStatusLabelSend(self,frame,size,tsize,sentStatus=False):
        label2=frame.winfo_children()[1]
        labelStauts=frame.winfo_children()[2]
        if sentStatus==True:
            label2.config(text='Sent Completed')
            mb0=ds.Recv.get_mb(1,size)
            mb1=ds.Recv.get_mb(1,tsize)
            mb0=round(mb0,3)
            mb1=round(mb1,3)
            stat='{0} mb'.format(mb1)
            labelStauts.config(text=stat)
        else:
            mb0=ds.Recv.get_mb(1,size)
            mb1=ds.Recv.get_mb(1,tsize)
            mb0=round(mb0,3)
            mb1=round(mb1,3)
            stat='{0}/{1} mb'.format(mb0,mb1)
            labelStauts.config(text=stat)

    def updateStatusLabelRecv(self,frame,size,tsize,sentStatus=False):
        label2=frame.winfo_children()[1]
        labelStauts=frame.winfo_children()[2]
        if sentStatus==True:
            label2.config(text='Recv Completed')
            mb0=ds.Recv.get_mb(1,size)
            mb1=ds.Recv.get_mb(1,tsize)
            mb0=round(mb0,3)
            mb1=round(mb1,3)
            stat='{0} mb'.format(mb1)
            labelStatus.config(text=stat)
        else:
            mb0=ds.Recv.get_mb(1,size)
            mb1=ds.Recv.get_mb(1,tsize)
            mb0=round(mb0,3)
            mb1=round(mb1,3)
            stat='{0}/{1} mb'.format(mb0,mb1)
            labelStatus.config(text=stat)


    def setFile(self):
        
        file=filedialog.askopenfilename()
        self.fileToSend=file
    def sendFile(self):
        

        file=self.fileToSend
        if file=='':
            pass
        else:
            frame=self.genFileLabelSend(file)
            self.c.send.send_file(file,function=self.updateStatusLabelSend,args=frame)

    def handleChatInfo(self,chatData):
        for i in self.listFrame.winfo_children():
            i.destroy()

        tFrame=tk.Frame(self.listFrame,bg='#006266',height=300,width=250)
        tFrame.place(x=50,y=100)

        self.listCont,self.can=gc.scrollableFrame(tFrame,300,220)
        a=chatData
        #self.lists.place(x=10,y=10)

        if len(a)==0:
            frame=tk.Frame(self.listCont,height=50,width=250,bg='red')
            label=tk.Label(frame,text='You and your friend never chatted \n '+\
                'Create your first chat')
            label.place(x=10,y=10)
            frame.pack()
        else:
            for i in a:
                chat=i[1]
                frame=tk.Frame(self.listCont,height=50,width=250,bg='yellow')
                label=tk.Label(frame,text=chat)
                label.place(x=10,y=10)
                frame.pack()
                self.can.yview_moveto(1)







main=__name__
print(main)
if '__main__'==main:
    c=tvc.Client()
    print("HI")
    root=tk.Tk()
    root.geometry('500x400')
    Global(root,c)
    root.mainloop()



