import Gui_Creation as gc
import tkinter as tk
import GuiXprt as gx
import XprtLoginControl as xlc
import TrialVersionClient1 as tvc
import threading
import DataShare as ds
from tkinter import filedialog
import numpy as np
from PIL import Image,ImageTk
import cv2

lController=xlc.Controller()
helpDic={}

'''
        def fun():
            pass

        threading.Thread(target=fun).start()
'''

class Global:


    def __init__(self,root,c,stf='GL'):
        #GL
        #GO
        self.c=c
        self.stf=stf
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

        btnForward=tk.Button(titleFrame,text='Forward',command=self.btnForward)
        btnForward.place(x=300,y=5)

        btnHelp=tk.Button(titleFrame,text='Help')
        btnHelp.place(x=450,y=5)

        #Left Pane

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

        def fun():
            self.root.geometry('500x400')
            gx.ForgetPassword(self.root,self.c)

        threading.Thread(target=fun).start()



    def signUp(self):
        def fun():
            tuserName=self.varUserr.get()
            tpassword=self.varPassr.get()
            tname=self.varNamer.get()
            tseqQ=self.varSeqQ.get()
            tseqA=self.varSeqA.get()

            self.forward=False

            self.c.signUp(tuserName,tname,tpassword,tseqQ,tseqA)
            self.userName=tuserName
            self.types='signUp'
            threading.Thread(target=self.handle).start()

        threading.Thread(target=fun).start()


    def btnLogin(self):
        def fun():
            self.forward=False
            self.userName=self.varUserl.get()
            self.c.login(self.varUserl.get(),self.varPassl.get())
            self.types='login'
            threading.Thread(target=self.handle).start()

        threading.Thread(target=fun).start()


    def btnForward(self):
        def fun():

            if self.forward:
                self.root.geometry('1100x600+50+50')
                gx.MainWindow(self.root,self.c,self.userName)

        threading.Thread(target=fun).start()

    def handle(self):
        types=self.types
        print("I AM HANDLER")
        while True:
                 if types=='login':
                     if self.c.dcond['login']==True:
                         msg=self.c.stmessage['login']
                         if msg['code']=='0006':
                             self.leftLoginStatus.config(text='Login From Another Location')
                         elif msg['code']=='0003':
                             self.leftLoginStatus.config(text='Login Successful')

                             self.forward=True
                         elif msg['code']=='0001':
                             self.leftLoginStatus.config(text='Password Error')
                         elif msg['code']=='0002':
                             self.leftLoginStatus.config(text='UserName not found')
                         else:
                             self.leftLoginStatus.config(text='Error')
                         break
                 elif types=='signUp':
                    if self.c.dcond['signUp']==True:
                        msg=self.c.stmessage['signUp']
                        if msg['code']=='0005':
                            self.labelUserStatus.config(text='UserName already exists')
                        elif msg['code']=='0004':
                            self.labelUserStatus.config(text='SignUp successfull')
                            self.forward=True
                        else:
                            pass
                        break

class ForgetPassword:


    def __init__(self,root,c,stf='GL'):
        #GL
        #GO
        self.c=c
        self.forward=False
        self.stf=stf
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

        btnHelp=tk.Button(titleFrame,text='Help')
        btnHelp.place(x=450,y=5)


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
        def fun():
            self.root.geometry('500x400')
            gx.Global(self.root,self.c)

        threading.Thread(target=fun).start()


    def submit(self):
        def fun():
            tuserName=self.varUserName.get()
            tseqAnswer=self.varSeqA.get()
            self.c.forgetPassword(tuserName,tseqAnswer)
            self.types='ForgetPassword'
            threading.Thread(target=self.handle).start()

        threading.Thread(target=fun).start()
    def handle(self):
        types=self.types
        print("I AM HANDLER")
        while True:
                 if types=='ForgetPassword':
                     if self.c.dcond['ForgetPassword']==True:
                         msg=self.c.stmessage['ForgetPassword']
                         if msg['wType']=='ForgetPasswordResponse':
                             password=msg['password']
                             self.labelStatus.config(text='Password:-"'+password+'"')
                         elif msg['code']=='0007':
                             self.labelStatus.config(text='Incorrect SeqA')
                         elif msg['code']=='0005':
                             self.labelStatus.config(text='UserName not exists')
                         else:
                             self.labelStatus.config(text='Error')
                         break

class MainWindow:

    def __init__(self,root,c,userName):
        self.userName=userName
        print("I AM USERNAMW")
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

        btnOverAllControl=tk.Button(llFrame,width=btnWidth,text='Overall Control',command=self.overallControl)
        btnOverAllControl.place(x=30,y=10)


        btnSearchFriend=tk.Button(llFrame,width=btnWidth,text='Search Friend',command=self.searchFriend)
        btnSearchFriend.place(x=150,y=10)


        btnBlockUnblock=tk.Button(llFrame,width=btnWidth,text='Block & Unblock',command=self.blockUnblock)
        btnBlockUnblock.place(x=30,y=50)


        btnFriendRequest=tk.Button(llFrame,width=btnWidth,text='Friend Request',command=self.friendRequest)
        btnFriendRequest.place(x=150,y=50)

        btnNotification=tk.Button(llFrame,width=btnWidth,text='Notification',command=self.notification)
        btnNotification.place(x=30,y=90)




        lrFrame=tk.Frame(leftFrame,bg='#d1d8e0',height=500,width=400)


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

    def refress(self):
        def fun():
            self.c.loadMainWindow()
            self.types='LoadMainWindow'
            threading.Thread(target=self.handle).start()

        threading.Thread(target=fun).start()


    def handle(self):
        types=self.types
        print("I AM HANDLER")
        while True:
                 if types=='LoadMainWindow':
                     if self.c.dcond['LoadMainWindow']==True:
                         msg=self.c.stmessage['LoadMainWindow']
                         if msg['wType']=='LoadMainWindowResponse':
                             self.labelTitleStatus.config(text='Updation Completed')

                         else:
                             self.labelTitleStatus.config(text='Error')
                         break


    def editProfile(self):
        def fun():
            self.root.geometry('500x400')
            gx.EditProfile(self.root,self.c,self.userName)

        threading.Thread(target=fun).start()



    def sequrity(self):
        def fun():
            self.root.geometry('500x400')
            gx.Sequrity(self.root,self.c,self.userName)

        threading.Thread(target=fun).start()



    def overallControl(self):
        def fun():
            self.root.geometry('500x400')
            gx.OverallControl(self.root,self.c,self.userName)

        threading.Thread(target=fun).start()



    def searchFriend(self):
        def fun():
            self.root.geometry('500x400')
            gx.SearchFriend(self.root,self.c,self.userName)

        threading.Thread(target=fun).start()



    def blockUnblock(self):
        def fun():
            self.root.geometry('500x400')
            gx.BlockUnblock(self.root,self.c,self.userName)

        threading.Thread(target=fun).start()



    def friendRequest(self):
        def fun():
            self.root.geometry('500x400')
            gx.FriendRequest(self.root,self.c,self.userName)

        threading.Thread(target=fun).start()



    def notification(self):
        def fun():
            self.root.geometry('500x400')
            gx.Notification(self.root,self.c,self.userName)

        threading.Thread(target=fun).start()




    def systemSettings(self):
        def fun():
            self.root.geometry('1100x600+50+50')
            gx.SystemSettings(self.root,self.c,self.userName)

        threading.Thread(target=fun).start()



    def _help(self):
        pass

    def logOut(self):
        def fun():
            self.root.geometry('500x400')
            gx.Global(self.root,self.c,self.userName)

        threading.Thread(target=fun).start()

class BlockUnblock:


    def __init__(self,root,c,userName,stf='GL'):
        #GL
        #GO
        self.c=c
        self.stf=stf
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
        llistFrame=tk.Frame(leftFrame,bg='#006266',height=150,width=220)
        llistFrame.place(x=30,y=130)
        ltFrame=tk.Frame(llistFrame,bg='#006266',height=150,width=220)
        ltFrame.place(x=50,y=100)

        llistCont=gc.scrollableFrame(ltFrame,200,180)

#IN )NE



        rightFrame=tk.Frame(downFrame,bg='#FEA47F',width=250,height=350)

        labelRightTitle=tk.Label(rightFrame,text='Unblock',font="Helvetica 10 bold ",bg='yellow',fg='red')
        labelRightTitle.place(x=30,y=5)



        rbtnSearch=tk.Button(rightFrame,text='Load',width=btnWidth,command=self.searchr)
        rbtnSearch.place(x=30,y=90)

        #IN ONE
        rlistFrame=tk.Frame(rightFrame,bg='#006266',height=150,width=220)
        rlistFrame.place(x=30,y=130)
        rtFrame=tk.Frame(rlistFrame,bg='#006266',height=150,width=220)
        rtFrame.place(x=50,y=100)

        rlistCont=gc.scrollableFrame(rtFrame,200,180)

#IN )NE


        leftFrame.place(x=0,y=0)
        rightFrame.place(x=250,y=0)
        downFrame.place(x=0,y=50)
        titleFrame.place(x=0,y=0)
        frame.place(x=0,y=0)

    def refress(self):
        def fun():
            self.c.loadBlockUnblock()
            self.types='LoadBlock&Unblock'
            threading.Thread(target=self.handle).start()

        threading.Thread(target=fun).start()




    def handle(self):
        types=self.types
        print("I AM HANDLER")
        while True:
                 if types=='BlockSearch':
                     if self.c.dcond['BlockSearch']==True:
                         msg=self.c.stmessage['BlockSearch']
                         if msg['code']=='0015':
                             self.labelStatus.config(text='Same userName')
                         elif msg['code']=='0014':
                             self.labelStatus.config(text='userName not exist')
                         elif msg['wType']=='blockSearchResponse':
                            data=msg['data']
                            type=msg['type']
                            shape=msg['shape']

                            d=ds.remodifyData(data,type,shape)
                            self.labelStatus.config(text=str(d))
                         else:
                             self.labelStatus.config(text='Error')
                         break

                 elif types=='UnblockLoad':

                     if self.c.dcond['UnblockLoad']==True:
                         msg=self.c.stmessage['UnblockLoad']

                         if msg['wType']=='UnblockResponse':

                            data=msg['data']
                            type=msg['type']
                            shape=msg['shape']

                            d=ds.remodifyData(data,type,shape)
                            self.labelStatus.config(text=str(d))

                         else:
                             self.labelStatus.config(text='Error')
                         break
                 elif types=='':
                     if self.c.dcond['LoadBlock&Unblock']==True:
                         msg=self.c.stmessage['LoadBlock&Unblock']

                         if msg['wType']=='LoadBlock&UnblockResponse':
                            self.labelStatus.config(text='Data Restored')

                         else:
                             self.labelStatus.config(text='Error')
                         break

    def forward(self):
        def fun():
            self.root.geometry('1100x600+50+50')
            gx.MainWindow(self.root,self.c,self.userName)

        threading.Thread(target=fun).start()


    def searchl(self):
        def fun():
                userName=self.lvarUserName.get()


                self.c.blockSearch(userName)
                self.types='BlockSearch'
                threading.Thread(target=self.handle).start()


        threading.Thread(target=fun).start()

    def searchr(self):
        def fun():
            self.c.unblockLoad()
            self.types='UnblockLoad'
            threading.Thread(target=self.handle).start()

        threading.Thread(target=fun).start()



class EditProfile:


    def __init__(self,root,c,userName,stf='GL'):
        #GL
        #GO
        self.userName=userName
        self.c=c
        print("IMEDITOR")
        self.stf=stf
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
        def fun():
            self.c.loadEditProfile()
            self.types='LoadEditProfile'
            threading.Thread(target=self.handle).start()

        threading.Thread(target=fun).start()




    def handle(self):
        types=self.types
        print("I AM HANDLER")
        while True:
                 if types=='LoadEditProfile':
                     if self.c.dcond['LoadEditProfile']==True:
                         msg=self.c.stmessage['LoadEditProfile']
                         if msg['wType']=='EditProfileResponse':
                             self.labelTitleStatus.config(text='Updation Completed')
                             img=msg['img']
                             img=bytes(img[2:-1],'utf-8')

                             img=ds.decb(img)
                             img=np.frombuffer(img,dtype='uint8')
                             img.shape=(200,200,3)
                             #cv2.imwrite('C:\\Users\\Bipin\\Desktop\\kk.jpeg',img)
                             img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
                             #print(img.shape)
                             #cv2.imshow('hi',img)
                             img=Image.fromarray(img)
                             imgtk=ImageTk.PhotoImage(img)

                             self.img=imgtk

                             self.profileLabel.config(image=self.img)

                             #label.config(image=imgtk)

                         else:
                             self.labelTitleStatus.config(text='Error')
                         break

                 elif types=='EditProfile':

                     if self.c.dcond['EditProfile']==True:
                         msg=self.c.stmessage['EditProfile']

                         if msg['code']=='ee08':
                            self.labelChNameStatus.config(text='Profile Updated')
                         elif msg['code']=='dd08':
                             self.labelChNameStatus.config(text='Name Updated')
                         else:
                             self.labelChNameStatus.config(text='Error')




    def forward(self):
        def fun():
            self.root.geometry('1100x600+50+50')
            gx.MainWindow(self.root,self.c,self.userName)

        threading.Thread(target=fun).start()



    def update(self):
        def fun():
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
            threading.Thread(target=self.handle).start()

        threading.Thread(target=fun).start()



class FriendRequest:


    def __init__(self,root,c,userName,stf='GL'):
        #GL
        #GO
        self.c=c
        self.stf=stf
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

#IN ONE
        listFrame=tk.Frame(downFrame,bg='#006266',height=220,width=220)
        listFrame.place(x=50,y=50)
        tFrame=tk.Frame(listFrame,bg='#006266',height=220,width=220)
        tFrame.place(x=50,y=100)

        listCont=gc.scrollableFrame(tFrame,300,400)

#IN )NE






        downFrame.place(x=0,y=50)
        titleFrame.place(x=0,y=0)
        frame.place(x=0,y=0)
    def refress(self):
        def fun():
            self.c.loadFriendRequest()
            self.types='LoadFriendRequest'
            threading.Thread(target=self.handle).start()

        threading.Thread(target=fun).start()

    def handle(self):
        types=self.types
        print("I AM HANDLER")
        while True:
                 if types=='LoadFriendRequest':

                     if self.c.dcond['LoadFriendRequest']==True:
                         msg=self.c.stmessage['LoadFriendRequest']
                         if msg['wType']=='LoadFriendRequestResponse':
                            data=msg['FriendRequestData']
                            type=msg['FriendRequestType']
                            shape=msg['FriendRequestShape']

                            d=ds.remodifyData(data,type,shape)
                            self.labelStatus.config(text=str(d))
                         else:
                             self.labelStatus.config(text='Error')
                         break

    def forward(self):
        def fun():
            self.root.geometry('1100x600+50+50')
            gx.MainWindow(self.root,self.c,self.userName)

        threading.Thread(target=fun).start()



class Notification:


    def __init__(self,root,c,userName,stf='GL'):
        #GL
        #GO
        self.c=c
        self.userName=userName
        self.stf=stf
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
#IN ONE
        listFrame=tk.Frame(downFrame,bg='#006266',height=220,width=220)
        listFrame.place(x=50,y=40)
        tFrame=tk.Frame(listFrame,bg='#006266',height=220,width=220)
        tFrame.place(x=50,y=100)

        listCont=gc.scrollableFrame(tFrame,300,400)

#IN )NE



        downFrame.place(x=0,y=50)
        titleFrame.place(x=0,y=0)
        frame.place(x=0,y=0)

    def refress(self):
        def fun():
            self.c.Notification(0,100)
            self.types='Notification'
            threading.Thread(target=self.handle).start()

        threading.Thread(target=fun).start()

    def handle(self):
        types=self.types
        print("I AM HANDLER")
        while True:
                 if types=='Notification':

                     if self.c.dcond['Notification']==True:
                         msg=self.c.stmessage['Notification']
                         if msg['wType']=='NotificationResponse':
                            data=msg['data']
                            type=msg['type']
                            shape=msg['shape']

                            d=ds.remodifyData(data,type,shape)
                            self.labelStatus.config(text=str(d))
                         else:
                             self.labelStatus.config(text='Error')
                         break

    def forward(self):
        def fun():
                self.root.geometry('1100x600+50+50')
                gx.MainWindow(self.root,self.c,self.userName)


        threading.Thread(target=fun).start()


class OverallControl:


    def __init__(self,root,c,userName,stf='GL'):
        #GL
        #GO
        self.c=c
        self.userName=userName
        self.stf=stf
        btnWidth=5
        entryWidth=25
        labelWidth=21
        self.root=root
        root.title('Overall Control')

        frame=tk.Frame(root,height=400,width=500)

        #Title
        titleFrame=tk.Frame(frame,bg='#006266',height=50,width=500)

        labelTitle=tk.Label(titleFrame,text='Overall Control',font="Helvetica 20 bold ",bg='yellow',fg='red')
        labelTitle.place(x=30,y=5)

        btnRefress=tk.Button(titleFrame,text='Refress',width=btnWidth,command=self.refress)
        btnRefress.place(x=360,y=5)


        btnHelp=tk.Button(titleFrame,text='Help')
        btnHelp.place(x=450,y=5)

        btnUpdate=tk.Button(titleFrame,text='Update',command=self.update)
        btnUpdate.place(x=280,y=5)


        downFrame=tk.Frame(frame,bg='grey',height=350,width=500)


        leftFrame=tk.Frame(downFrame,bg='#58B19F',height=350,width=350)

        labelLeftTitle=tk.Label(leftFrame,text='Sending Control',font="Helvetica 10 bold ",bg='yellow',fg='red')
        labelLeftTitle.place(x=30,y=5)

        btnForward=tk.Button(leftFrame,text='Forward',width=btnWidth,command=self.forward)
        btnForward.place(x=150,y=5)

        labelFile=tk.Label(leftFrame,text='File',width=labelWidth)
        labelText=tk.Label(leftFrame,text='Text',width=labelWidth)
        labelScreenCap=tk.Label(leftFrame,text='Screen Capture',width=labelWidth)
        labelCameraCap=tk.Label(leftFrame,text='Camera Capture',width=labelWidth)
        labelVoice=tk.Label(leftFrame,text='Voice',width=labelWidth)
        labelMouse=tk.Label(leftFrame,text='Mouse',width=labelWidth)
        labelKeyboard=tk.Label(leftFrame,text='Keyboard',width=labelWidth)

        self.varFilel=tk.IntVar()
        self.varTextl=tk.IntVar()
        self.varScreenCapl=tk.IntVar()
        self.varCameraCapl=tk.IntVar()
        self.varVoicel=tk.IntVar()
        self.varMousel=tk.IntVar()
        self.varKeyboardl=tk.IntVar()

        self.varFiler=tk.IntVar()
        self.varTextr=tk.IntVar()
        self.varScreenCapr=tk.IntVar()
        self.varCameraCapr=tk.IntVar()
        self.varVoicer=tk.IntVar()
        self.varMouser=tk.IntVar()
        self.varKeyboardr=tk.IntVar()



        labelFile.place(x=30,y=40)
        labelText.place(x=30,y=80)
        labelScreenCap.place(x=30,y=120)
        labelCameraCap.place(x=30,y=160)
        labelVoice.place(x=30,y=200)
        labelMouse.place(x=30,y=240)
        labelKeyboard.place(x=30,y=280)




        laradFile=tk.Radiobutton(leftFrame,text='on',variable=self.varFilel,value=1)
        laradText=tk.Radiobutton(leftFrame,text='on',variable=self.varTextl,value=1)
        laradScreenCap=tk.Radiobutton(leftFrame,text='on',variable=self.varScreenCapl,value=1)
        laradCameraCap=tk.Radiobutton(leftFrame,text='on',variable=self.varCameraCapl,value=1)
        laradVoice=tk.Radiobutton(leftFrame,text='on',variable=self.varVoicel,value=1)
        laradMouse=tk.Radiobutton(leftFrame,text='on',variable=self.varMousel,value=1)
        laradKeyboard=tk.Radiobutton(leftFrame,text='on',variable=self.varKeyboardl,value=1)

        lbradFile=tk.Radiobutton(leftFrame,text='off',variable=self.varFilel,value=0)
        lbradText=tk.Radiobutton(leftFrame,text='off',variable=self.varTextl,value=0)
        lbradScreenCap=tk.Radiobutton(leftFrame,text='off',variable=self.varScreenCapl,value=0)
        lbradCameraCap=tk.Radiobutton(leftFrame,text='off',variable=self.varCameraCapl,value=0)
        lbradVoice=tk.Radiobutton(leftFrame,text='off',variable=self.varVoicel,value=0)
        lbradMouse=tk.Radiobutton(leftFrame,text='off',variable=self.varMousel,value=0)
        lbradKeyboard=tk.Radiobutton(leftFrame,text='off',variable=self.varKeyboardl,value=0)


        laradFile.place(x=200,y=40)
        laradText.place(x=200,y=80)
        laradScreenCap.place(x=200,y=120)
        laradCameraCap.place(x=200,y=160)
        laradVoice.place(x=200,y=200)
        laradMouse.place(x=200,y=240)
        laradKeyboard.place(x=200,y=280)

        lbradFile.place(x=280,y=40)
        lbradText.place(x=280,y=80)
        lbradScreenCap.place(x=280,y=120)
        lbradCameraCap.place(x=280,y=160)
        lbradVoice.place(x=280,y=200)
        lbradMouse.place(x=280,y=240)
        lbradKeyboard.place(x=280,y=280)



        rightFrame=tk.Frame(downFrame,bg='#9AECDB',height=350,width=150)

        raradFile=tk.Radiobutton(rightFrame,text='on',variable=self.varFiler,value=1)
        raradText=tk.Radiobutton(rightFrame,text='on',variable=self.varTextr,value=1)
        raradScreenCap=tk.Radiobutton(rightFrame,text='on',variable=self.varScreenCapr,value=1)
        raradCameraCap=tk.Radiobutton(rightFrame,text='on',variable=self.varCameraCapr,value=1)
        raradVoice=tk.Radiobutton(rightFrame,text='on',variable=self.varVoicer,value=1)
        raradMouse=tk.Radiobutton(rightFrame,text='on',variable=self.varMouser,value=1)
        raradKeyboard=tk.Radiobutton(rightFrame,text='on',variable=self.varKeyboardr,value=1)

        rbradFile=tk.Radiobutton(rightFrame,text='off',variable=self.varFiler,value=0)
        rbradText=tk.Radiobutton(rightFrame,text='off',variable=self.varTextr,value=0)
        rbradScreenCap=tk.Radiobutton(rightFrame,text='off',variable=self.varScreenCapr,value=0)
        rbradCameraCap=tk.Radiobutton(rightFrame,text='off',variable=self.varCameraCapr,value=0)
        rbradVoice=tk.Radiobutton(rightFrame,text='off',variable=self.varVoicer,value=0)
        rbradMouse=tk.Radiobutton(rightFrame,text='off',variable=self.varMouser,value=0)
        rbradKeyboard=tk.Radiobutton(rightFrame,text='off',variable=self.varKeyboardr,value=0)


        raradFile.place(x=20,y=40)
        raradText.place(x=20,y=80)
        raradScreenCap.place(x=20,y=120)
        raradCameraCap.place(x=20,y=160)
        raradVoice.place(x=20,y=200)
        raradMouse.place(x=20,y=240)
        raradKeyboard.place(x=20,y=280)

        rbradFile.place(x=90,y=40)
        rbradText.place(x=90,y=80)
        rbradScreenCap.place(x=90,y=120)
        rbradCameraCap.place(x=90,y=160)
        rbradVoice.place(x=90,y=200)
        rbradMouse.place(x=90,y=240)
        rbradKeyboard.place(x=90,y=280)







        labelRightTitle=tk.Label(rightFrame,text='Reciving Control',font="Helvetica 10 bold ",bg='yellow',fg='red')
        labelRightTitle.place(x=30,y=5)



        self.labelStatus=tk.Label(leftFrame,text='Status')
        self.labelStatus.place(x=30,y=320)

        rightFrame.place(x=350,y=0)
        leftFrame.place(x=0,y=0)
        downFrame.place(x=0,y=50)
        titleFrame.place(x=0,y=0)
        frame.place(x=0,y=0)

    def refress(self):
        def fun():
            self.c.loadOverallControl()
            self.types='LoadOverallControl'
            threading.Thread(target=self.handle).start()


        threading.Thread(target=fun).start()



    def handle(self):
        types=self.types
        print("I AM HANDLER")
        while True:
                 if types=='LoadOverallControl':
                     if self.c.dcond['LoadOverallControl']==True:
                         msg=self.c.stmessage['LoadOverallControl']
                         if msg['wType']=='LoadOverallControlResponse':
                             self.labelStatus.config(text='Refress Completed')

                             data=msg['overallControlData']
                             type=msg['overallControlType']
                             shape=msg['overallControlShape']

                             d=ds.remodifyData(data,type,shape)
                             d=d[0][1:]
                             val=[]
                             for i in d:
                                 val.append(int(i))

                             self.varFilel.set(val[0])
                             self.varTextl.set(val[1])
                             self.varScreenCapl.set(val[2])
                             self.varCameraCapl.set(val[3])
                             self.varVoicel.set(val[4])
                             self.varMousel.set(val[5])
                             self.varKeyboardl.set(val[6])

                             self.varFiler.set(val[7])
                             self.varTextr.set(val[8])
                             self.varScreenCapr.set(val[9])
                             self.varCameraCapr.set(val[10])
                             self.varVoicer.set(val[11])
                             self.varMouser.set(val[12])
                             self.varKeyboardr.set(val[13])

                         else:
                             self.labelStatus.config(text='Error')
                         break

                 elif types=='OverallControl':

                     if self.c.dcond['OverallControl']==True:
                         msg=self.c.stmessage['OverallControl']

                         if msg['code']=='0013':
                            self.labelStatus.config(text='Updation Completed')
                         else:
                             self.labelStatus.config(text='Error')
                         break

    def forward(self):
        def fun():
            self.root.geometry('1100x600+50+50')
            gx.MainWindow(self.root,self.c,self.userName)
        threading.Thread(target=fun).start()


    def update(self):
        def fun():

            values=[self.varFilel.get(),self.varTextl.get(),self.varScreenCapl.get()\
                ,self.varCameraCapl.get(),self.varVoicel.get(),\
                    self.varMousel.get(),self.varKeyboardl.get(),\
                    self.varFiler.get(),self.varTextr.get(),\
                    self.varScreenCapr.get(),self.varCameraCapr.get()\
                ,self.varVoicer.get(),self.varMouser.get(),self.varKeyboardr.get()]

            val=[]
            for i in values:
                val.append(str(i))

            self.c.overallControl(val)
            self.types='OverallControl'
            threading.Thread(target=self.handle).start()

        threading.Thread(target=fun).start()

class SearchFriend:


    def __init__(self,root,c,userName,stf='GL'):
        #GL
        #GO
        self.c=c
        self.stf=stf
        self.userName=userName
        btnWidth=12
        entryWidth=25
        labelWidth=21
        self.root=root
        root.title('Search Friend')

        frame=tk.Frame(root,height=400,width=500)

        #Title
        titleFrame=tk.Frame(frame,bg='#006266',height=50,width=500)

        labelTitle=tk.Label(titleFrame,text='Search Friend',font="Helvetica 20 bold ",bg='yellow',fg='red')
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


#      ONE

        listFrame=tk.Frame(downFrame,bg='#006266',height=260,width=400)
        listFrame.place(x=30,y=60)
        tFrame=tk.Frame(listFrame,bg='#006266',height=260,width=400)
        tFrame.place(x=50,y=100)

        listCont=gc.scrollableFrame(tFrame,260,400)

#IN )NE



        downFrame.place(x=0,y=50)
        titleFrame.place(x=0,y=0)
        frame.place(x=0,y=0)

    def refress(self):
        def fun():
            self.c.loadSearchFriend()
            self.types='LoadSearchFriend'
            threading.Thread(target=self.handle).start()

        threading.Thread(target=fun).start()

    def handle(self):
        types=self.types
        print("I AM HANDLER")
        while True:
                 if types=='LoadSearchFriend':
                     if self.c.dcond['LoadSearchFriend']==True:
                         msg=self.c.stmessage['LoadSearchFriend']
                         if msg['wType']=='LoadSearchFriendResponse':
                             self.labelStatus.config(text='Refress Completed')

                         else:
                             self.labelStatus.config(text='Error')
                         break

                 elif types=='SearchFriend':

                     if self.c.dcond['SearchFriend']==True:
                         msg=self.c.stmessage['SearchFriend']

                         if msg['wType']=='searchFriendResponse':
                            self.labelStatus.config(text='Data Restored')
                            data=msg['data']
                            type=msg['type']
                            shape=msg['shape']

                            d=ds.remodifyData(data,type,shape)

                            if len(d)==0:
                                self.labelStatus.config(text='No Records found')
                            else:
                                self.labelStatus.config(text=str(d))
                         else:
                             self.labelStatus.config(text='Error')
                         break
    def forward(self):
        def fun():
            self.root.geometry('1100x600+50+50')
            gx.MainWindow(self.root,self.c,self.userName)

        threading.Thread(target=fun).start()


    def search(self):
        def fun():

            userName=self.varUserName.get()


            self.c.searchFriend(userName)
            self.types='SearchFriend'
            threading.Thread(target=self.handle).start()


        threading.Thread(target=fun).start()


class Sequrity:


    def __init__(self,root,c,userName,stf='GL'):
        #GL
        #GO
        self.c=c
        self.userName=userName
        self.stf=stf
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
        def fun():
            self.root.geometry('500x400')
            gx.ChangePasswords(self.root,self.c,self.userName)

        threading.Thread(target=fun).start()

    def changeSeqQA(self):
        def fun():
            self.root.geometry('500x400')
            gx.ChangeSeqQA(self.root,self.c,self.userName)


        threading.Thread(target=fun).start()


    def back(self):
        def fun():
            self.root.geometry('1100x600+50+50')
            gx.MainWindow(self.root,self.c,self.userName)

        threading.Thread(target=fun).start()



class SystemSettings:


    def __init__(self,root,c,userName,stf='GL'):
        #GL
        #GO
        self.c=c
        self.stf=stf
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
        def fun():
            self.root.geometry('1100x600+50+50')
            gx.MainWindow(self.root,self.c,self.userName)

        threading.Thread(target=fun).start()



class ChangePasswords:


    def __init__(self,root,c,userName,stf='GL'):
        #GL
        #GO
        self.c=c
        self.userName=userName
        self.stf=stf
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
        def fun():
            self.root.geometry('500x400')
            gx.Sequrity(self.root,self.c,self.userName)

        threading.Thread(target=fun).start()


    def handle(self):
        types=self.types
        print("I AM HANDLER")
        while True:
                 if types=='ChangePassword':
                     if self.c.dcond['ChangePassword']==True:
                         msg=self.c.stmessage['ChangePassword']
                         if msg['code']=='0010':
                             self.labelStatus.config(text='Updation Completed')
                         elif msg['code']=='0009':
                             self.labelStatus.config(text='Password was incorrect')
                         else:
                             self.labelStatus.config(text='Error')
                         break




    def update(self):
        def fun():
            currP=self.varCurrentPassword.get()
            newP=self.varNewPassword.get()
            self.c.changePassword(newP,currP)
            self.types='ChangePassword'
            threading.Thread(target=self.handle).start()

        threading.Thread(target=fun).start()




class ChangeSeqQA:


    def __init__(self,root,c,userName,stf='GL'):
        #GL
        #GO
        self.c=c
        self.stf=stf
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
        def fun():
            self.root.geometry('500x400')
            gx.Sequrity(self.root,self.c,self.userName)

        threading.Thread(target=fun).start()

    def handle(self):
        types=self.types
        print("I AM HANDLER")
        while True:
                 if types=='ChangeSeqQA':
                     if self.c.dcond['ChangeSeqQA']==True:
                         msg=self.c.stmessage['ChangeSeqQA']
                         if msg['code']=='0012':
                             self.labelStatus.config(text='Updation Completed')
                         elif msg['code']=='0011':
                             self.labelStatus.config(text='Password was incorrect')
                         else:
                             self.labelStatus.config(text='Error')
                         break

    def update(self):
        def fun():
            curP=self.varCurrentPassword.get()
            seqQ=self.varSeqQ.get()
            seqA=self.varSeqA.get()
            self.c.changeSeqQA(curP,seqQ,seqA)
            self.types='ChangeSeqQA'
            threading.Thread(target=self.handle).start()

        threading.Thread(target=fun).start()






main=__name__
print(main)
if '__main__'==main:
    c=tvc.Client()
    print("HI")
    root=tk.Tk()
    root.geometry('500x400')
    Global(root,c)
    root.mainloop()



