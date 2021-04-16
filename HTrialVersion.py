#Trial Version
#clieant
import ControlUnit as cu
import threading
import random
import AssembleData as ad
import DataShare as ds
import XprtLoginControl as xlc
import cv2
import numpy as np
import time
import  RControl as rc

con=rc.Controls()
xc=xlc.Controller()
ass=ad.Assemble()
dAssemble=ad.Dassemble()

class Client:

    def __init__(self):
        self.Login=False
        self.s=cu.client_connect('localhost',4445)
        self.count=1
        self.send=ds.Send()
        self.recv=ds.Recv()

        #threading.Thread(target=self.recvData).start()
        #threading.Thread(target=self.checking).start()

        #self.recvData()
        #threading.Thread(target=self.shower).start()
        
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


    def signUp(self,userName,name,userPass,seqQ,seqA):
        #userPass=ds.enc(userPass)
        #seqA=ds.enc(seqA)
        data=ad.assValue(['userName','seqQ','name','seqA','userPass'],[userName,seqQ,name,seqA,userPass],'signUp')
        data=ass.aSequrity(data,'user')
        data=data.decode()
        self.send.send_message(self.s,data,'bipin')

    def forgetPassword(self,userName,seqA):
        data=ad.assValue(['userName','seqA'],[userName,seqA],'ForgetPassword')
        data=ass.aSequrity(data,'user')
        data=data.decode()
        self.send.send_message(self.s,data,'bipin')

    def editProfile(self,name):
        data=ad.assValue(['name'],['BipinSingh'],'EditProfile')
        data=ass.aInfo(data,'user')
        data=data.decode()
        self.send.send_message(self.s,data,'bipin')

    def changePassword(self,password,oldPassword):
        data=ad.assValue(['Password','OldPassword'],[password,oldPassword],'ChangePassword')
        data=ass.aInfo(data,'user')
        data=data.decode()
        self.send.send_message(self.s,data,'bipin')

    def changeSeqQA(self,password,seqQ,seqA):
        data=ad.assValue(['Password','seqQ','seqA'],[password,seqQ,seqA],'ChangeSeqQA')
        data=ass.aInfo(data,'user')
        data=data.decode()
        self.send.send_message(self.s,data,'bipin')

    def overallControl(self,values14):
        data=ad.assValue(['sFile','sText','sScreen','sCamera','sVoice','sMouse','sKeyboard',\
                          'rFile','rText','rScreen','rCamera','rVoice','rMouse','rKeyboard']\
                         ,values14,'OverallControl')
        data=ass.aInfo(data,'user')
        data=data.decode()
        self.send.send_message(self.s,data,'bipin')



    def searchFriend(self,userName):
        data=ad.assValue(['userName'],[userName],'SearchFriend')
        data=ass.aInfo(data,'user')
        data=data.decode()
        self.send.send_message(self.s,data,'bipin')

    def sendFriendRequest(self,userName):
        data=ad.assValue(['userName'],[userName],'SendFriendRequest')
        data=ass.aInfo(data,'user')
        data=data.decode()
        self.send.send_message(self.s,data,'bipin')

    def deleteFriendRequest(self,userName):
        data=ad.assValue(['userName'],[userName],'DeleteFriendRequest')
        data=ass.aInfo(data,'user')
        data=data.decode()
        self.send.send_message(self.s,data,'bipin')

    def blockSearch(self,userName):
        data=ad.assValue(['userName'],[userName],'BlockSearch')
        data=ass.aInfo(data,'user')
        data=data.decode()
        self.send.send_message(self.s,data,'bipin')

    def block(self,userName):
        data=ad.assValue(['userName'],[userName],'Block')
        data=ass.aInfo(data,'user')
        data=data.decode()
        self.send.send_message(self.s,data,'bipin')

    def unblockLoad(self):
        data=ad.assValue(['userName'],['user'],'UnblockLoad')
        data=ass.aInfo(data,'user')
        data=data.decode()
        self.send.send_message(self.s,data,'bipin')

    def unblock(self,userName):
        data=ad.assValue(['userName'],[userName],'Unblock')
        data=ass.aInfo(data,'user')
        data=data.decode()
        self.send.send_message(self.s,data,'bipin')

    def FriendRequestLoad(self):
        data=ad.assValue(['userName'],['user'],'FriendRequestLoad')
        data=ass.aInfo(data,'user')
        data=data.decode()
        self.send.send_message(self.s,data,'bipin')

    def FriendRequestAccept(self,userName):
        data=ad.assValue(['userName'],[userName],'FriendRequestAccept')
        data=ass.aInfo(data,'user')
        data=data.decode()
        self.send.send_message(self.s,data,'bipin')

    def chat(self,userName,rangeIn,rangeOut):
        data=ad.assValue(['rangeIn','rangeOut','userName'],[rangeIn,rangeOut,userName],'Chat')
        data=ass.aInfo(data,'user')
        data=data.decode()
        self.send.send_message(self.s,data,'bipin')

    def Notification(self,rangeIn,rangeOut):
        data=ad.assValue(['rangeIn','rangeOut'],[rangeIn,rangeOut],'Notification')
        data=ass.aInfo(data,'user')
        data=data.decode()
        self.send.send_message(self.s,data,'bipin')

    def loadUserProfile(self,userName):
        data=ad.assValue(['userName'],[userName],'LoadUserProfile')
        data=ass.aInfo(data,'user')
        data=data.decode()
        self.send.send_message(self.s,data,'bipin')

    def loadGlobalMember(self,userName):

        data=ad.assValue(['userName'],[userName],'LoadGlobalMember')
        data=ass.aInfo(data,'user')
        data=data.decode()
        self.send.send_message(self.s,data,'bipin')

    def loadMainWindow(self):
        data=ad.assValue(['userName'],['user'],'LoadMainWindow')
        data=ass.Sequrity(data,'user')
        data=data.decode()
        self.send.send_message(self.s,data,'bipin')

    def loadEditProfile(self):

        data=ad.assValue(['userName'],['user'],'LoadMainWindow')
        data=ass.Sequrity(data,'user')
        data=data.decode()
        self.send.send_message(self.s,data,'bipin')

    def loadOverallControl(self):

        data=ad.assValue(['userName'],['user'],'LoadOverallControl')
        data=ass.Sequrity(data,'user')
        data=data.decode()
        self.send.send_message(self.s,data,'bipin')
#--
    def loadSearchFriend(self):
        data=ad.assValue(['userName'],['user'],'LoadSearchFriend')
        data=ass.Sequrity(data,'user')
        data=data.decode()
        self.send.send_message(self.s,data,'bipin')

    def loadBlockUnblock(self):
        data=ad.assValue(['userName'],['user'],'LoadBlock&Unblock')
        data=ass.Sequrity(data,'user')
        data=data.decode()
        self.send.send_message(self.s,data,'bipin')

    def loadFriendRequest(self):
        data=ad.assValue(['userName'],['user'],'LoadFriendRequest')
        data=ass.Sequrity(data,'user')
        data=data.decode()
        self.send.send_message(self.s,data,'bipin')

    def loadNotification(self):
        data=ad.assValue(['userName'],['user'],'LoadNotification')
        data=ass.Sequrity(data,'user')
        data=data.decode()
        self.send.send_message(self.s,data,'bipin')

    def loadFindFriends(self):
        data=ad.assValue(['userName'],['user'],'LoadFindFriends')
        data=ass.Sequrity(data,'user')
        data=data.decode()
        self.send.send_message(self.s,data,'bipin')

    def loadSystemSettings(self):
        data=ad.assValue(['userName'],['user'],'LoadSystemSettings')
        data=ass.Sequrity(data,'user')
        data=data.decode()
        self.send.send_message(self.s,data,'bipin')

    def _Text(self,text,userName):
        data=ad.assValue(['userName','text'],[userName,text],'_Text')
        data=ass.aData(data,userName)
        data=data.decode()
        self.send.send_message(self.s,data,'bipin')

    def _File(self,file,userName):
        pass

    def _Screen(self,data,userName):
        data=self.dataCvt(data,userName,'Screen')
        self.send.send_message(self.s,data,'bipin')

    def dataCvt(self,data,userName,type):
        data=np.array(data)

        shape=str(data.shape)
        types=str(data.dtype)
        actData=bytes(data)


        actData=ds.encb(actData)


        actData=actData.decode()

        
        
        data=ad.assValue(['userName',type.lower()+'Data',type.lower()+'Type',type.lower()+'Shape'],[userName,actData,types,shape],'_'+type)


        data=ass.aData(data,userName)


        data=data.decode()


        return data


    def _Camera(self,data,userName):

        data=self.dataCvt(data,userName,'Camera')
        self.send.send_message(self.s,data,'bipin')
    
    def startSending(self):
        userName='Bipin'
        stream=con.on_mic()
        while True:
            d=stream.read(1024)
            
            self._Voice(d,userName)
            #print('overall Time -',time.time()-t1)
    def _Voice(self,data,userName):

        
        actData=ds.encb(data).decode()
        data=ad.assValue(['userName','voiceData'],[userName,actData],'_Voice')
        data=ass.aData(data,userName)
        data=data.decode()
        self.send.send_message(self.s,data,'bipin')

    def _Mouse(self,data,userName):
        data=np.array(data)

        shape=data.shape
        types=data.dtype
        actData=bytes(data)
        actData=ds.enc(actData.decode())
        data=ad.assValue(['userName','mouseData','mouseType','mouseShape'],[userName,actData,types,shape],'_Screen')
        data=ass.Data(data,userName)
        data=data.decode()
        self.send.send_message(self.s,data,'bipin')

    def _Keyboard(self,data,userName):
        data=np.array(data)

        shape=data.shape
        types=data.dtype
        actData=bytes(data)
        actData=ds.enc(actData.decode())
        data=ad.assValue(['userName','keyboardData','keyboardType','keyboardShape'],[userName,actData,types,shape],'_Screen')
        data=ass.Data(data,userName)
        data=data.decode()
        self.send.send_message(self.s,data,'bipin')

    def recvData(self):
        self.recv.get(self.s,'bipin')

    def h(self,data):
        values=data[2]
        vType=data[1]
        wType=data[0]
        val=ad.cvtArr2Dict(vType,values)
        if wType=='_Camera':
            ddata=val['cameraData']
            dtype=val['cameraType']
            dshape=val['cameraShape']
            ar=ds.remodifyData(ddata,dtype,dshape)
            self.data=ar

    def shower(self):
            count=1
            while True:
                
                recv=self.recv
                if count in recv.tmessage:

                    msg=recv.tmessage[count]
                    del recv.tmessage[count]
                    count=count+1

                    dtype,toSend,data=dAssemble.dAssembler(msg.encode())

                    data=ad.deAssValue(data)
                    
                    print(len(str(data)))

c=Client()
print("Client work is completed")
#input()
#c.sign#SignUp(TrialVersion")Up('Thisisuser','name','password','SequrityQuestion','SequrityAnswer')
#c.signUp('Djjkkk','KingKhan','password','Hello_World','ProgrammingLanguage')
#c.forgetPassword('Thisisuser','SequrityAnser')
c.login('Suraj','Suraj')
