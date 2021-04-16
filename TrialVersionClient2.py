#Trial Version
#clieant
import ControlUnit as cu
import threading
import random
import AssembleData as ad
import DataShare as ds
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
    


    def __init__(self,addr='localhost',port=8787):
        self.Login=False
        self.s=cu.client_connect(addr,port)
        self.count=1
        self.send=ds.Send(self.s)
        self.recv=ds.Recv(self.s)
        
        
        self.functionList={}

        self.function1Type=None
        self.function2Type=None
        self.function3Type=None

        #self.argument1Type=None
        #self.argument2Type=None
        #self.argument3Type=None

        
        threading.Thread(target=self.recvData).start()

       

        print("client is connected")

    def dataHandle(self,msg):

        dtype,wType,values=ad.deAssValue(msg)
        info=ad.cvtArr2Dict(wType,values)
        print(dtype)

        if dtype=='Error':

            if self.function1Type is not None:
                self.function1Type(info)
        elif dtype=='Data':
            msg=info
            user=msg['user']
            try:

                msg['wt']
                print(msg['ofType'])
                if user in self.functionList:
                    handler=self.functionList[user][1]
                    handler(msg)
            except:
                print("BUT HI")
                if user in self.functionList:
                    handler=self.functionList[user][0]
                    handler(msg)
        elif dtype=='UserData':
            msg=info
            user=msg['user']
            if user in self.functionList:
                handler=self.functionList[user][0]
                handler(msg)
        else:
            print("This is another type of Response which can't be handled")
        



    def login(self,userName,userPass):

        #userPass=ds.enc(userPass)
        userName=userName.lower()
        data=ad.assValue(['userName','userPass','wType','user'],[userName,userPass,'login','user'],'Sequrity')
        self.send.send_message(data)
       
    def signUp(self,userName,name,userPass,seqQ,seqA):
        #userPass=ds.enc(userPass)
        #seqA=ds.enc(seqA)
        userName=userName.lower()
        data=ad.assValue(['userName','seqQ','name','seqA','userPass','wType','user'],[userName,seqQ,name,seqA,userPass,'signUp','user'],'Sequrity')
        self.send.send_message(data)
        

    def forgetPassword(self,userName,seqA):
        data=ad.assValue(['userName','seqA','wType','user'],[userName,seqA,'ForgetPassword','user'],'Sequrity')
        self.send.send_message(data)
        

    def editProfile(self,name='_None',img='_None'):
        data=ad.assValue(['name','wType','user','img'],[name,'EditProfile','user',img],'Info')
        self.send.send_message(data)
        

    def changePassword(self,password,oldPassword):
        data=ad.assValue(['Password','OldPassword','wType','user'],[password,oldPassword,'ChangePassword','user'],'Info')
        self.send.send_message(data)
        

    def changeSeqQA(self,password,seqQ,seqA):
        data=ad.assValue(['Password','seqQ','seqA','wType','user'],[password,seqQ,seqA,'ChangeSeqQA','user'],'Info')
        self.send.send_message(data)
        

    def overallControl(self,values14):
        data=ad.assValue(['sFile','sText','sScreen','sCamera','sVoice','sMouse','sKeyboard',\
                          'rFile','rText','rScreen','rCamera','rVoice','rMouse','rKeyboard','wType','user']\
                         ,values14+['OverallControl','user'],'Info')

        self.send.send_message(data)
        

    def searchFriend(self,userName):
        data=ad.assValue(['userName','wType','user'],[userName,'SearchFriend','user'],'Info')
        self.send.send_message(data)
       

    def sendFriendRequest(self,userName):
        data=ad.assValue(['userName','wType','user'],[userName,'SendFriendRequest','user'],'Info')
        self.send.send_message(data)
        

    def deleteFriendRequest(self,userName):
        data=ad.assValue(['userName','wType','user'],[userName,'DeleteFriendRequest','user'],'Info')
        self.send.send_message(data)
        

    def blockSearch(self,userName):
        data=ad.assValue(['userName','wType','user'],[userName,'BlockSearch','user'],'Info')
        self.send.send_message(data)
        
    def block(self,userName):
        data=ad.assValue(['userName','wType','user'],[userName,'Block','user'],'Info')
        self.send.send_message(data)
        

    def unblockLoad(self):
        data=ad.assValue(['userName','wType','user'],['user','UnblockLoad','user'],'Info')
        self.send.send_message(data)
        

    def unblock(self,userName):
        data=ad.assValue(['userName','wType','user'],[userName,'Unblock','user'],'Info')
        self.send.send_message(data)
        

    def FriendRequestLoad(self):
        data=ad.assValue(['userName','wType','user'],['user','FriendRequestLoad','user'],'Info')
        self.send.send_message(data)
        

    def FriendRequestAccept(self,userName):
        data=ad.assValue(['userName','wType','user'],[userName,'FriendRequestAccept','user'],'Info')
        self.send.send_message(data)
        


    def chat(self,userName,rangeIn,rangeOut):
        data=ad.assValue(['rangeIn','rangeOut','userName','wType','user'],[rangeIn,rangeOut,userName,'Chat','user'],'Info')
        self.send.send_message(data)
        

    def Notification(self,rangeIn,rangeOut):
        data=ad.assValue(['rangeIn','rangeOut','wType','user'],[rangeIn,rangeOut,'Notification','user'],'Info')
        self.send.send_message(data)
        


    def loadUserProfile(self,userName):
        data=ad.assValue(['userName','wType','user'],[userName,'LoadUserProfile','user'],'Info')
        self.send.send_message(data)
        


    def sendFile(self,file):

        self.send.send_file(self.s,file,'bipin')


    def loadGlobalMember(self,userName):

        data=ad.assValue(['userName','wType','user'],[userName,'LoadGlobalMember','user'],'Info')
        self.send.send_message(data)
        

    def loadMainWindow(self):
        data=ad.assValue(['userName','wType','user'],['user','LoadMainWindow','user'],'System')
        self.send.send_message(data)
        

    def loadEditProfile(self):

        data=ad.assValue(['userName','wType','user'],['user','LoadEditProfile','user'],'System')
        self.send.send_message(data)
        


    def loadOverallControl(self):

        data=ad.assValue(['userName','wType','user'],['user','LoadOverallControl','user'],'System')
        self.send.send_message(data)
       
#--
    def loadSearchFriend(self):
        data=ad.assValue(['userName','wType','user'],['user','LoadSearchFriend','user'],'System')
        self.send.send_message(data)
        

    def loadBlockUnblock(self):
        data=ad.assValue(['userName','wType','user'],['user','LoadBlock&Unblock','user'],'System')
        self.send.send_message(data)
        

    def loadFriendRequest(self):
        data=ad.assValue(['userName','wType','user'],['user','LoadFriendRequest','user'],'System')
        self.send.send_message(data)
        

    def loadNotification(self):
        data=ad.assValue(['userName','wType','user'],['user','LoadNotification','user'],'System')
        self.send.send_message(data)
        

    def loadFindFriends(self):
        data=ad.assValue(['userName','wType','user'],['user','LoadFindFriends','user'],'System')
        self.send.send_message(data)
        

    def loadSystemSettings(self):
        data=ad.assValue(['userName','wType','user'],['user','LoadSystemSettings','user'],'System')
        self.send.send_message(data)
        

    def loadFriendControl(self,userName):
        data=ad.assValue(['user','wType'],[userName,'LoadFriendControl'],'System')
        self.send.send_message(data)
        

    def loadChatWindow(self,userName,status):
        data=ad.assValue(['user','wType','status'],[userName,'LoadChatWindow',status],'System')
        self.send.send_message(data)
       

    def updatePartFriendControl(self,userName,field,value):
        print("I M SINGLE reQUst")
        data=ad.assValue(['field','wType','user','fieldValue'],[field,'UpdateFriendControl',userName,value],'UserData')
        self.send.send_message(data)
        

    def updateFriendControls(self,userName,values14):
        data=ad.assValue(['_sScreen','_sCamera','_sVoice','_sMouse','_sKeyboard',\
                          '_rScreen','_rCamera','_rVoice','_rMouse','_rKeyboard','wType','user']\
                         ,values14+['UpdateFriendControls',userName],'UserData')
        self.send.send_message(data)
       

    def requestFor(self,userName,cType):

        data=ad.assValue(['cdType','user','wType'],[cType,userName,'Request'],'UserData')
        self.send.send_message(data)
        

    def requestResponseFor(self,userName,cType,value):

        data=ad.assValue(['cdType','user','wType','value'],[cType,userName,'RequestResponse',value],'UserData')
        self.send.send_message(data)
        

    def _Text(self,text,userName):
        data=ad.assValue(['userName','text','wType','user'],[userName,text,'_Text',userName],'Data')
        self.send.send_message(data)
        

    def _File(self,file,userName):
        pass

    def _Screen(self,data,userName):
        data=ds.prepSend(data)
        data=ad.assValue(['userName','screenData','screenType','screenShape','wType','user'],[userName,data[0],data[1],data[2],'_Screen',userName],'Data')
        self.send.send_message(data)
        

    def _Camera(self,data,userName):
        data=ds.prepSend(data)

        data=ad.assValue(['userName','cameraData','cameraType','cameraShape','wType','user'],[userName,data[0],data[1],data[2],'_Camera',userName],'Data')
        self.send.send_message(data)
        

    def _Voice(self,data,userName):

        data=ds.encb(data).decode()
        data=ad.assValue(['userName','voiceData','wType','user'],[userName,data,'_Voice',userName],'Data')
        self.send.send_message(data)
        

    def _Mouse(self,data,userName):
        data=ds.prepSend(data)
        data=ad.assValue(['userName','mouseData','mouseType','mouseShape','wType','user'],[userName,data[0],data[1],data[2],'_Mouse',userName],'Data')
        self.send.send_message(data)
        

    def _Keyboard(self,data,userName):
        data=ds.prepSend(data)
        data=ad.assValue(['userName','keyboardData','keyboardType','keyboardShape','wType','user'],[userName,data[0],data[1],data[2],'_Keyboard',userName],'Data')
        self.send.send_message(data)
        

    def recvData(self):
        self.recv.function=self.dataHandle
        self.recv.get()
        








#c=Client()
#print("Client work is completed")
#input()
#c.signUp('Thisisuser','name','password','SequrityQuestion','SequrityAnswer')
#c.signUp('Djjkkk','KingKhan','password','Hello_World','ProgrammingLanguage')
#c.forgetPassword('Thisisuser','SequrityAnser')
#c.login('Bipin','Bipin')
#c.loadEditProfile()


