#Trial Version
#clieant
import ControlUnit as cu
import threading
import random
import AssembleData as ad
import DataShare1234ButOriginal as ds
import XprtLoginControl as xlc
import cv2
import time
import numpy as np
import RControl as rc

con=rc.Controls()
stream=con.on_mic()
xc=xlc.Controller()
ass=ad.Assemble()
dAssemble=ad.Dassemble()

class Client:
    dataValues={}
    dataCount=0
    dataUserCount=0

    requestValues={}
    requestCount=0
    requestUserCount=0

    errorValues={}
    errorCount=0
    errorUserCount=0

    dataErrorValues={}
    dataErrorCount=0
    dataErrorUserCount=0


    def __init__(self,addr='localhost',port=9085):
        self.Login=False
        self.s=cu.client_connect(addr,port)
        self.count=1
        self.send=ds.Send()
        self.recv=ds.Recv()
        self.showers=True
        self.dcond={}
        self.data={}



        self.curMessage='NONE'
        self.stmessage={}
        threading.Thread(target=self.recvData).start()

        threading.Thread(target=self.shower).start()

        print("client is connected")

    def dataHandle(self,msg):

        dtype,wType,values=ad.deAssValue(msg)
        info=ad.cvtArr2Dict(wType,values)
        print(dtype)
        if dtype=='Data':
            Client.dataValues[Client.dataCount]=info
            Client.dataCount=Client.dataCount+1
        elif dtype=='Request' or dtype=='RequestResponse':

            Client.requestValues[Client.requestCount]=info
            Client.requestCount=Client.requestCount+1
        elif dtype=='Error':
            try:
                wfType=info['wfType']
            except:
                wfType='ksdlkfslkf'
            if wfType=='Data':

                Client.dataErrorValues[Client.dataErrorCount]=info
                Client.dataErrorCount=Client.dataErrorCount+1

                #self.stmessage[info['ofType']]=info
            else:
                #print("I AM ONLY ERROR")
                Client.errorValues[Client.errorCount]=info
                Client.errorCount=Client.errorCount+1
                self.stmessage[info['ofType']]=info


                for i in self.dcond:
                    if self.dcond[i]==True:
                        continue
                    if info['ofType']==i:
                        self.dcond[i]=True
        else:



            self.stmessage[info['ofType']]=info


            for i in self.dcond:
                if self.dcond[i]==True:
                    continue
                if info['ofType']==i:
                    self.dcond[i]=True



    def login(self,userName,userPass):

        #userPass=ds.enc(userPass)
        userName=userName.lower()
        data=ad.assValue(['userName','userPass','wType','user'],[userName,userPass,'login','user'],'Sequrity')
        self.send.send_message(self.s,data,'bipin')
        self.dcond['login']=False

    def signUp(self,userName,name,userPass,seqQ,seqA):
        #userPass=ds.enc(userPass)
        #seqA=ds.enc(seqA)
        userName=userName.lower()
        data=ad.assValue(['userName','seqQ','name','seqA','userPass','wType','user'],[userName,seqQ,name,seqA,userPass,'signUp','user'],'Sequrity')
        self.send.send_message(self.s,data,'bipin')
        self.dcond['signUp']=False

    def forgetPassword(self,userName,seqA):
        data=ad.assValue(['userName','seqA','wType','user'],[userName,seqA,'ForgetPassword','user'],'Sequrity')
        self.send.send_message(self.s,data,'bipin')
        self.dcond['ForgetPassword']=False

    def editProfile(self,name='_None',img='_None'):
        data=ad.assValue(['name','wType','user','img'],[name,'EditProfile','user',img],'Info')
        self.send.send_message(self.s,data,'bipin')
        self.dcond['EditProfile']=False

    def changePassword(self,password,oldPassword):
        data=ad.assValue(['Password','OldPassword','wType','user'],[password,oldPassword,'ChangePassword','user'],'Info')
        self.send.send_message(self.s,data,'bipin')
        self.dcond['ChangePassword']=False

    def changeSeqQA(self,password,seqQ,seqA):
        data=ad.assValue(['Password','seqQ','seqA','wType','user'],[password,seqQ,seqA,'ChangeSeqQA','user'],'Info')
        self.send.send_message(self.s,data,'bipin')
        self.dcond['ChangeSeqQA']=False

    def overallControl(self,values14):
        data=ad.assValue(['sFile','sText','sScreen','sCamera','sVoice','sMouse','sKeyboard',\
                          'rFile','rText','rScreen','rCamera','rVoice','rMouse','rKeyboard','wType','user']\
                         ,values14+['OverallControl','user'],'Info')

        self.send.send_message(self.s,data,'bipin')
        self.dcond['OverallControl']=False

    def searchFriend(self,userName):
        data=ad.assValue(['userName','wType','user'],[userName,'SearchFriend','user'],'Info')
        self.send.send_message(self.s,data,'bipin')
        self.dcond['SearchFriend']=False

    def sendFriendRequest(self,userName):
        data=ad.assValue(['userName','wType','user'],[userName,'SendFriendRequest','user'],'Info')
        self.send.send_message(self.s,data,'bipin')
        self.dcond['SendFriendRequest']=False

    def deleteFriendRequest(self,userName):
        data=ad.assValue(['userName','wType','user'],[userName,'DeleteFriendRequest','user'],'Info')
        self.send.send_message(self.s,data,'bipin')
        self.dcond['DeleteFriendRequest']=False


    def blockSearch(self,userName):
        data=ad.assValue(['userName','wType','user'],[userName,'BlockSearch','user'],'Info')
        self.send.send_message(self.s,data,'bipin')
        self.dcond['BlockSearch']=False

    def block(self,userName):
        data=ad.assValue(['userName','wType','user'],[userName,'Block','user'],'Info')
        self.send.send_message(self.s,data,'bipin')
        self.dcond['Block']=False

    def unblockLoad(self):
        data=ad.assValue(['userName','wType','user'],['user','UnblockLoad','user'],'Info')
        self.send.send_message(self.s,data,'bipin')
        self.dcond['UnblockLoad']=False

    def unblock(self,userName):
        data=ad.assValue(['userName','wType','user'],[userName,'Unblock','user'],'Info')
        self.send.send_message(self.s,data,'bipin')
        self.dcond['Unblock']=False

    def FriendRequestLoad(self):
        data=ad.assValue(['userName','wType','user'],['user','FriendRequestLoad','user'],'Info')
        self.send.send_message(self.s,data,'bipin')
        self.dcond['FriendRequestLoad']=False

    def FriendRequestAccept(self,userName):
        data=ad.assValue(['userName','wType','user'],[userName,'FriendRequestAccept','user'],'Info')
        self.send.send_message(self.s,data,'bipin')
        self.dcond['FriendRequestAccept']=False

    def chat(self,userName,rangeIn,rangeOut):
        data=ad.assValue(['rangeIn','rangeOut','userName','wType','user'],[rangeIn,rangeOut,userName,'Chat','user'],'Info')
        self.send.send_message(self.s,data,'bipin')
        self.dcond['Chat']=False

    def Notification(self,rangeIn,rangeOut):
        data=ad.assValue(['rangeIn','rangeOut','wType','user'],[rangeIn,rangeOut,'Notification','user'],'Info')
        self.send.send_message(self.s,data,'bipin')
        self.dcond['Notification']=False

    def loadUserProfile(self,userName):
        data=ad.assValue(['userName','wType','user'],[userName,'LoadUserProfile','user'],'Info')
        self.send.send_message(self.s,data,'bipin')
        self.dcond['LoadUserProfile']=False

    def sendFile(self,file):

        self.send.send_file(self.s,file,'bipin')


    def loadGlobalMember(self,userName):

        data=ad.assValue(['userName','wType','user'],[userName,'LoadGlobalMember','user'],'Info')
        self.send.send_message(self.s,data,'bipin')
        self.dcond['LoadGlobalMember']=False

    def loadMainWindow(self):
        data=ad.assValue(['userName','wType','user'],['user','LoadMainWindow','user'],'System')
        self.send.send_message(self.s,data,'bipin')
        self.dcond['LoadMainWindow']=False

    def loadEditProfile(self):

        data=ad.assValue(['userName','wType','user'],['user','LoadEditProfile','user'],'System')
        self.send.send_message(self.s,data,'bipin')
        self.dcond['LoadEditProfile']=False


    def loadOverallControl(self):

        data=ad.assValue(['userName','wType','user'],['user','LoadOverallControl','user'],'System')
        self.send.send_message(self.s,data,'bipin')
        self.dcond['LoadOverallControl']=False
#--
    def loadSearchFriend(self):
        data=ad.assValue(['userName','wType','user'],['user','LoadSearchFriend','user'],'System')
        self.send.send_message(self.s,data,'bipin')
        self.dcond['LoadSearchFriend']=False

    def loadBlockUnblock(self):
        data=ad.assValue(['userName','wType','user'],['user','LoadBlock&Unblock','user'],'System')
        self.send.send_message(self.s,data,'bipin')
        self.dcond['LoadBlock&Unblock']=False

    def loadFriendRequest(self):
        data=ad.assValue(['userName','wType','user'],['user','LoadFriendRequest','user'],'System')
        self.send.send_message(self.s,data,'bipin')
        self.dcond['LoadFriendRequest']=False

    def loadNotification(self):
        data=ad.assValue(['userName','wType','user'],['user','LoadNotification','user'],'System')
        self.send.send_message(self.s,data,'bipin')
        self.dcond['LoadNotification']=False

    def loadFindFriends(self):
        data=ad.assValue(['userName','wType','user'],['user','LoadFindFriends','user'],'System')
        self.send.send_message(self.s,data,'bipin')
        self.dcond['LoadFindFriends']=False

    def loadSystemSettings(self):
        data=ad.assValue(['userName','wType','user'],['user','LoadSystemSettings','user'],'System')
        self.send.send_message(self.s,data,'bipin')
        self.dcond['LoadSystemSettings']=False

    def loadFriendControl(self,userName):
        data=ad.assValue(['user','wType'],[userName,'LoadFriendControl'],'System')
        self.send.send_message(self.s,data,'bipin')
        self.dcond['LoadFriendControl']=False

    def loadChatWindow(self,userName,status):
        data=ad.assValue(['user','wType','status'],[userName,'LoadChatWindow',status],'System')
        self.send.send_message(self.s,data,'bipin')
        self.dcond['LoadChatWindow']=False


    def updatePartFriendControl(self,userName,field,value):
        print("I M SINGLE reQUst")
        data=ad.assValue(['field','wType','user','fieldValue'],[field,'UpdateFriendControl',userName,value],'UserData')
        self.send.send_message(self.s,data,'bipin')
        self.dcond['UpdateFriendControl']=False

    def updateFriendControls(self,userName,values14):
        data=ad.assValue(['_sScreen','_sCamera','_sVoice','_sMouse','_sKeyboard',\
                          '_rScreen','_rCamera','_rVoice','_rMouse','_rKeyboard','wType','user']\
                         ,values14+['UpdateFriendControls',userName],'UserData')
        self.send.send_message(self.s,data,'bipin')
        self.dcond['UpdateFriendControls']=False

    def requestFor(self,userName,cType):

        data=ad.assValue(['cdType','user','wType'],[cType,userName,'Request'],'UserData')
        self.send.send_message(self.s,data,'bipin')
        self.dcond['Error']=False

    def requestResponseFor(self,userName,cType,value):

        data=ad.assValue(['cdType','user','wType','value'],[cType,userName,'RequestResponse',value],'UserData')
        self.send.send_message(self.s,data,'bipin')
        self.dcond['Error']=False

    def _Text(self,text,userName):
        data=ad.assValue(['userName','text','wType','user'],[userName,text,'_Text',userName],'Data')
        self.send.send_message(self.s,data,'bipin')
        self.dcond['_Text']=False

    def _File(self,file,userName):
        pass

    def _Screen(self,data,userName):
        data=ds.prepSend(data)
        data=ad.assValue(['userName','screenData','screenType','screenShape','wType','user'],[userName,data[0],data[1],data[2],'_Screen',userName],'Data')
        self.send.send_message(self.s,data,'bipin')
        self.dcond['_Screen']=False

    def _Camera(self,data,userName):
        data=ds.prepSend(data)

        data=ad.assValue(['userName','cameraData','cameraType','cameraShape','wType','user'],[userName,data[0],data[1],data[2],'_Camera',userName],'Data')
        self.send.send_message(self.s,data,'bipin')
        self.dcond['_Camera']=False

    def _Voice(self,data,userName):

        data=ds.encb(data).decode()
        data=ad.assValue(['userName','voiceData','wType','user'],[userName,data,'_Voice',userName],'Data')
        self.send.send_message(self.s,data,'bipin')
        self.dcond['_Voice']=False

    def _Mouse(self,data,userName):
        data=ds.prepSend(data)
        data=ad.assValue(['userName','mouseData','mouseType','mouseShape','wType','user'],[userName,data[0],data[1],data[2],'_Mouse',userName],'Data')
        self.send.send_message(self.s,data,'bipin')
        self.dcond['_Mouse']=False

    def _Keyboard(self,data,userName):
        data=ds.prepSend(data)
        data=ad.assValue(['userName','keyboardData','keyboardType','keyboardShape','wType','user'],[userName,data[0],data[1],data[2],'_Keyboard',userName],'Data')
        self.send.send_message(self.s,data,'bipin')
        self.dcond['_Keyboard']=False

    def recvData(self):
        self.recv.get(self.s,'bipin')




    def shower(self):
            #print("HI")
            count=1
            while True:
                if self.showers:
                    pass
                else:
                    continue
                recv=self.recv
                if count in recv.tmessage:
                    print("I AM OK")
                    t1=time.time()
                    msg=recv.tmessage[count]
                    del recv.tmessage[count]
                    count=count+1
                    self.curMessage=msg
                    self.dataHandle(msg)
                    print(time.time()-t1)



#c=Client()
#print("Client work is completed")
#input()
#c.signUp('Thisisuser','name','password','SequrityQuestion','SequrityAnswer')
#c.signUp('Djjkkk','KingKhan','password','Hello_World','ProgrammingLanguage')
#c.forgetPassword('Thisisuser','SequrityAnser')
#c.login('Bipin','Bipin')
#c.loadEditProfile()


