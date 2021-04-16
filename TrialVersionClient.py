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

    def __init__(self,addr='localhost',port=4445):
        self.Login=False
        self.s=cu.client_connect(addr,port)
        self.count=1
        self.send=ds.Send()
        self.recv=ds.Recv()

        self.dcond={}
        self.data={}

        threading.Thread(target=self.recvData).start()
        threading.Thread(target=self.checking).start()
        threading.Thread(target=self.shower).start()
        threading.Thread(target=self.sh).start()
        print("client is connected")

    def handle(self,message):
                dtype,toSend,data=dAssemble.dAssembler(i.encode())
                if dtype=='Error':
                    print("Some error are occured")
                else:
                    print("Login is successful")

    def checking(self):
        while True:
            tmessage=self.recv.tmessage
            if(str(self.count) in tmessage):
                length=len(tmessage)
                message=tmessage[self.count]
                self.count=self.count+1
                self.handle(message)

    def login(self,userName,userPass):

        #userPass=ds.enc(userPass)
        data=ad.assValue(['userName','userPass'],[userName,userPass],'login')
        data=ass.aSequrity(data,'user')
        data=data.decode()
        self.send.send_message(self.s,data,'bipin')
        self.dcond['login']=False

    def dataHandle(self,msg):
        
        dtype,toSend,data=dAssemble.dAssembler(msg.encode())

        data=ad.deAssValue(data)

        for i in self.dcond:
            pass
        


    def signUp(self,userName,name,userPass,seqQ,seqA):
        #userPass=ds.enc(userPass)
        #seqA=ds.enc(seqA)
        data=ad.assValue(['userName','seqQ','name','seqA','userPass'],[userName,seqQ,name,seqA,userPass],'signUp')
        data=ass.aSequrity(data,'user')
        data=data.decode()
        self.send.send_message(self.s,data,'bipin')
        self.dcond['signUp']=False

    def forgetPassword(self,userName,seqA):
        data=ad.assValue(['userName','seqA'],[userName,seqA],'ForgetPassword')
        data=ass.aSequrity(data,'user')
        data=data.decode()
        self.send.send_message(self.s,data,'bipin')
        self.dcond['ForgetPassword']=False

    def editProfile(self,name):
        data=ad.assValue(['name'],['BipinSingh'],'EditProfile')
        data=ass.aInfo(data,'user')
        data=data.decode()
        self.send.send_message(self.s,data,'bipin')
        self.dcond['EditProfile']=False

    def changePassword(self,password,oldPassword):
        data=ad.assValue(['Password','OldPassword'],[password,oldPassword],'ChangePassword')
        data=ass.aInfo(data,'user')
        data=data.decode()
        self.send.send_message(self.s,data,'bipin')
        self.dcond['ChangePassword']=False

    def changeSeqQA(self,password,seqQ,seqA):
        data=ad.assValue(['Password','seqQ','seqA'],[password,seqQ,seqA],'ChangeSeqQA')
        data=ass.aInfo(data,'user')
        data=data.decode()
        self.send.send_message(self.s,data,'bipin')
        self.dcond['ChangeSeqQA']=False

    def overallControl(self,values14):
        data=ad.assValue(['sFile','sText','sScreen','sCamera','sVoice','sMouse','sKeyboard',\
                          'rFile','rText','rScreen','rCamera','rVoice','rMouse','rKeyboard']\
                         ,values14,'OverallControl')
        data=ass.aInfo(data,'user')
        data=data.decode()
        self.send.send_message(self.s,data,'bipin')
        self.dcond['OverallControl']=False

    def searchFriend(self,userName):
        data=ad.assValue(['userName'],[userName],'SearchFriend')
        data=ass.aInfo(data,'user')
        data=data.decode()
        self.send.send_message(self.s,data,'bipin')
        self.dcond['SearchFriend']=False

    def sendFriendRequest(self,userName):
        data=ad.assValue(['userName'],[userName],'SendFriendRequest')
        data=ass.aInfo(data,'user')
        data=data.decode()
        self.send.send_message(self.s,data,'bipin')
        self.dcond['SendFriendRequest']=False

    def deleteFriendRequest(self,userName):
        data=ad.assValue(['userName'],[userName],'DeleteFriendRequest')
        data=ass.aInfo(data,'user')
        data=data.decode()
        self.send.send_message(self.s,data,'bipin')
        self.dcond['DeleteFriendRequest']=False

    def blockSearch(self,userName):
        data=ad.assValue(['userName'],[userName],'BlockSearch')
        data=ass.aInfo(data,'user')
        data=data.decode()
        self.send.send_message(self.s,data,'bipin')
        self.dcond['BlockSearch']=False

    def block(self,userName):
        data=ad.assValue(['userName'],[userName],'Block')
        data=ass.aInfo(data,'user')
        data=data.decode()
        self.send.send_message(self.s,data,'bipin')
        self.dcond['Block']=False

    def unblockLoad(self):
        data=ad.assValue(['userName'],['user'],'UnblockLoad')
        data=ass.aInfo(data,'user')
        data=data.decode()
        self.send.send_message(self.s,data,'bipin')
        self.dcond['UnblockLoad']=False

    def unblock(self,userName):
        data=ad.assValue(['userName'],[userName],'Unblock')
        data=ass.aInfo(data,'user')
        data=data.decode()
        self.send.send_message(self.s,data,'bipin')
        self.dcond['Unblock']=False

    def FriendRequestLoad(self):
        data=ad.assValue(['userName'],['user'],'FriendRequestLoad')
        data=ass.aInfo(data,'user')
        data=data.decode()
        self.send.send_message(self.s,data,'bipin')
        self.dcond['FriendRequestLoad']=False

    def FriendRequestAccept(self,userName):
        data=ad.assValue(['userName'],[userName],'FriendRequestAccept')
        data=ass.aInfo(data,'user')
        data=data.decode()
        self.send.send_message(self.s,data,'bipin')
        self.dcond['FriendRequestAccept']=False

    def chat(self,userName,rangeIn,rangeOut):
        data=ad.assValue(['rangeIn','rangeOut','userName'],[rangeIn,rangeOut,userName],'Chat')
        data=ass.aInfo(data,'user')
        data=data.decode()
        self.send.send_message(self.s,data,'bipin')
        self.dcond['Chat']=False

    def Notification(self,rangeIn,rangeOut):
        data=ad.assValue(['rangeIn','rangeOut'],[rangeIn,rangeOut],'Notification')
        data=ass.aInfo(data,'user')
        data=data.decode()
        self.send.send_message(self.s,data,'bipin')
        self.dcond['Notification']=False

    def loadUserProfile(self,userName):
        data=ad.assValue(['userName'],[userName],'LoadUserProfile')
        data=ass.aInfo(data,'user')
        data=data.decode()
        self.send.send_message(self.s,data,'bipin')
        self.dcond['LoadUserProfile']=False

    def loadGlobalMember(self,userName):

        data=ad.assValue(['userName'],[userName],'LoadGlobalMember')
        data=ass.aInfo(data,'user')
        data=data.decode()
        self.send.send_message(self.s,data,'bipin')
        self.dcond['LoadGlobalMember']=False

    def loadMainWindow(self):
        data=ad.assValue(['userName'],['user'],'LoadMainWindow')
        data=ass.System(data,'user')
        data=data.decode()
        self.send.send_message(self.s,data,'bipin')
        self.dcond['LoadMainWindow']=False

    def loadEditProfile(self):

        data=ad.assValue(['userName'],['user'],'LoadEditProfile')
        data=ass.System(data,'user')
        data=data.decode()
        self.send.send_message(self.s,data,'bipin')
        self.dcond['LoadEditProifle']=False

    def loadOverallControl(self):

        data=ad.assValue(['userName'],['user'],'LoadOverallControl')
        data=ass.System(data,'user')
        data=data.decode()
        self.send.send_message(self.s,data,'bipin')
        self.dcond['LoadOverallControl']=False
#--
    def loadSearchFriend(self):
        data=ad.assValue(['userName'],['user'],'LoadSearchFriend')
        data=ass.System(data,'user')
        data=data.decode()
        self.send.send_message(self.s,data,'bipin')
        self.dcond['LoadSearchFriend']=False

    def loadBlockUnblock(self):
        data=ad.assValue(['userName'],['user'],'LoadBlock&Unblock')
        data=ass.System(data,'user')
        data=data.decode()
        self.send.send_message(self.s,data,'bipin')
        self.dcond['LoadBlock&Unblock']=False

    def loadFriendRequest(self):
        data=ad.assValue(['userName'],['user'],'LoadFriendRequest')
        data=ass.System(data,'user')
        data=data.decode()
        self.send.send_message(self.s,data,'bipin')
        self.dcond['LoadFriendRequest']=False

    def loadNotification(self):
        data=ad.assValue(['userName'],['user'],'LoadNotification')
        data=ass.System(data,'user')
        data=data.decode()
        self.send.send_message(self.s,data,'bipin')
        self.dcond['LoadNotification']=False

    def loadFindFriends(self):
        data=ad.assValue(['userName'],['user'],'LoadFindFriends')
        data=ass.System(data,'user')
        data=data.decode()
        self.send.send_message(self.s,data,'bipin')
        self.dcond['LoadFindFriends']=False

    def loadSystemSettings(self):
        data=ad.assValue(['userName'],['user'],'LoadSystemSettings')
        data=ass.System(data,'user')
        data=data.decode()
        self.send.send_message(self.s,data,'bipin')
        self.dcond['LoadSystemSettings']=False

    def _Text(self,text,userName):
        data=ad.assValue(['userName','text'],[userName,text],'_Text')
        data=ass.aData(data,userName)
        data=data.decode()
        self.send.send_message(self.s,data,'bipin')
        self.dcond['_Text']=False

    def _File(self,file,userName):
        pass

    def _Screen(self,data,userName):
        data=np.array(data)
        
        shape=data.shape
        types=data.dtype
        actData=bytes(data)
        actData=ds.enc(actData.decode())
        data=ad.assValue(['userName','screenData','screenType','screenShape'],[userName,actData,types,shape],'_Screen')
        data=ass.Data(data,userName)
        data=data.decode()
        self.send.send_message(self.s,data,'bipin')
        self.dcond['_Screen']=False

    def _Camera(self,data,userName):
        data=np.array(data)
        
        shape=data.shape
        types=data.dtype
        actData=bytes(data)
        actData=ds.enc(actData.decode())
        data=ad.assValue(['userName','cameraData','cameraType','cameraShape'],[userName,actData,types,shape],'_Camera')
        data=ass.Data(data,userName)
        data=data.decode()
        self.send.send_message(self.s,data,'bipin')
        self.dcond['_Camera']=False

    def _Voice(self,data,userName):
        
        data=np.array(data)
        
        shape=data.shape
        types=data.dtype
        actData=bytes(data)
        actData=ds.enc(actData.decode())
        data=ad.assValue(['userName','voiceData','voiceType','voiceShape'],[userName,actData,types,shape],'_Voice')
        data=ass.Data(data,userName)
        data=data.decode()
        self.send.send_message(self.s,data,'bipin')
        self.dcond['_Voice']=False

    def _Mouse(self,data,userName):
        data=np.array(data)
        
        shape=data.shape
        types=data.dtype
        actData=bytes(data)
        actData=ds.enc(actData.decode())
        data=ad.assValue(['userName','mouseData','mouseType','mouseShape'],[userName,actData,types,shape],'_Mouse')
        data=ass.Data(data,userName)
        data=data.decode()
        self.send.send_message(self.s,data,'bipin')
        self.dcond['_Mouse']=False

    def _Keyboard(self,data,userName):
        data=np.array(data)
        
        shape=data.shape
        types=data.dtype
        actData=bytes(data)
        actData=ds.enc(actData.decode())
        data=ad.assValue(['userName','keyboardData','keyboardType','keyboardShape'],[userName,actData,types,shape],'_Keyboard')
        data=ass.Data(data,userName)
        data=data.decode()
        self.send.send_message(self.s,data,'bipin')
        self.dcond['_Keyboard']=False

    def recvData(self):
        self.recv.get(self.s,'bipin')


    data=None
    def sh(self):
        while True:
            if str(self.data)==str(None):
                pass
            else:
                #stream.write(self.data)
                pass
            if cv2.waitKey(1) & 0xff==ord('q'):
                break
    def h(self,data):
        values=data[2]
        vType=data[1]
        wType=data[0]
        val=ad.cvtArr2Dict(vType,values)
        #print(wType)
        if wType=='_VoiceResponse':
            t1=time.time()
            ddata=val['voiceData']
        
            ddata=ds.decb(bytes(ddata,'utf-8'))
            self.data=ddata
            #print(time.time()-t1)



    def shower(self):
            count=1
            while True:
                
                recv=self.recv
                if count in recv.tmessage:
                    
                    msg=recv.tmessage[count]
                    del recv.tmessage[count]
                    count=count+1

                    self.dataHandle(msg)
                    #print("WHSY")

c=Client()
#print("Client work is completed")
#input()
#c.signUp('Thisisuser','name','password','SequrityQuestion','SequrityAnswer')
#c.signUp('Djjkkk','KingKhan','password','Hello_World','ProgrammingLanguage')
#c.forgetPassword('Thisisuser','SequrityAnser')
c.login('Bipin','Bipin')
c.loadEditProfile()
