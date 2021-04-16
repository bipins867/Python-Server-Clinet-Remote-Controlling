#Trial Version of server client
#this is server
import ControlUnit as cu
import threading
import DataShare as ds
import AssembleData as ad
import time
import dbquery as db
import Xprt_DataBase as xdb
from cryptography.fernet import Fernet
import numpy as np
import myStringLib as ms
        
key=b'eQ5jxFcJNYII5Z4vhBtvT-mNiqx64yQEUln1SOoYEDA='
fernet=Fernet(key)
dAssemble=ad.Dassemble()
Assemble=ad.Assemble()
mydb=db.genMdb()

class Server:

    
    
    def __init__(self):
        self.s=cu.create_server('localhost',4445,5000)
        print("Server is created")
        self.clients={}
        self.dclients={}

        self.nclients={}

        self.rnclients={}

        

        
        #threading.Thread(target=self.show).start()
        threading.Thread(target=self.clientConnector).start()
        threading.Thread(target=self.refressList).start()
        self.usr={}


    def closeConnection(self,addr):
        
        if(addr in self.clients):
            s=self.clients[addr]
            s.close()
            #del self.clients[addr]
            

            

    def show(self):
        
        while True:
            nclients=self.nclients
            if(len(nclients)>0):
                tf=[]
                for i in nclients:
                    tf.append([i,nclients[i]])
                print(tf)
        
    def clientConnector(self):
        while True:
            try:
                c,addr=self.s.accept()
                self.clients[addr]=c
                
                self.handleClient(c,addr)
            except:
                print("It an error in client connection")

    def handleClient(self,c,addr):
        
        def fun():
            send=ds.Send()
            recv=ds.Recv()
            
            self.dclients[addr]=[send,recv]

            #threading.Thread(target=recv.get,args=(c,'bipin')).start()

            for i in self.dclients:
                
                send,recv=self.dclients[i]
                s=self.clients[i]
                threading.Thread(target=self.loginManager,args=(send,recv,s,addr)).start()


        
            try:
                
                recv.get(c,'bipin')
            except:

                c.close()
                
                i=addr            
                del self.clients[i]
                
                del self.dclients[i]
    


        threading.Thread(target=fun).start()
        

    def xprtNotCreation(self,userName,mycursor):
        
        xnot=xdb.XprtNot(mycursor)
        xnot.createNotification(userName)
        xnot.createBlock(userName)
        xnot.createFriendRSent(userName)
        xnot.createFriendRRecv(userName)
        xnot.createFriend(userName)

    def prepSend(self,data):
        data=np.array(data)
        types=str(data.dtype)
        shape=str(data.shape)
        data=bytes(data)
        data=data.decode()

        return [data,types,shape]

    def loginManager(self,send,recv,s,addr):
        #print("This is login manager")
        #try:
            
            count=1
            login=False
            fuserName=None
            #globalMemberLoad=1
            while True:
                
                if count in recv.tmessage:
                    
                    msg=recv.tmessage[count]
                    del recv.tmessage[count]
                    count=count+1

                    dtype,toSend,data=dAssemble.dAssembler(msg.encode())
                    data=ad.deAssValue(data)

                    values=data[2]
                    vType=data[1]
                    wType=data[0]

                    if dtype=='Sequrity':
                        
                        cursor=mydb.cursor()

                        if data[0]=='login':
                            
                            userName=values[0]
                            userPass=values[1]
                            #print(userPass)
                            cb=db.cb1(cursor,'xprtinfo')
                            cond=cb.checkData('sequrity','username',userName)

                            if(cond):
                                passw=userPass
                                scond=cb.checkMulAndData('sequrity',['userName','password'],[userName,passw])
                                if(scond):
                                    login=True
                                    #print(self.nclients)
                                    if(userName in self.nclients):
                                        
                                        daddr=self.nclients[userName]
                                        data=ad.assValue(['code'],['0006'],'error')
                                        data=Assemble.aError(data,'user')
                                        data=data.decode()
                                        dsend,drecv=self.dclients[daddr]
                                        dsend.send_message(s,data,'bipin')

                                        self.closeConnection(daddr)
                                        
                                                            
                                    self.nclients[userName]=addr
                                    self.rnclients[addr]=userName
                                    #print(self.nclients)
                                    #Login Successful
                                    fuserName=userName
                                    data=ad.assValue(['code'],['0003'],'error')
                                    data=Assemble.aError(data,'user')
                                    data=data.decode()
                                    send.send_message(s,data,'bipin')
                                    self.usr[fuserName]=send,recv
                                else:
                                    login=False
                                    #Password Error
                                    data=ad.assValue(['code'],['0001'],'error')
                                    data=Assemble.aError(data,'user')
                                    data=data.decode()
                                    send.send_message(s,data,'bipin')
                            else:
                                
                                #UserName not found error
                                login=False
                                data=ad.assValue(['code'],['0002'],'error')
                                data=Assemble.aError(data,'user')
                                data=data.decode()
                                send.send_message(s,data,'bipin')
                        elif data[0]=='signUp':
                            userName=values[0]
                            
                            cb=db.cb1(cursor,'xprtinfo')
                            cond=cb.checkData('sequrity','username',userName)
                            name=values[2]
                            if cond:
                                login=False
                                #UserName already exists
                                data=ad.assValue(['code'],['0005'],'error')
                                data=Assemble.aError(data,'user')
                                        
                                data=data.decode()
                                send.send_message(s,data,'bipin')
                                
                            else:
                                
                                xinfo=xdb.XprtInfo(cursor)

                                self.nclients[userName]=addr
                                self.rnclients[addr]=userName
                                xinfo.insertSequrity(values)
                                xinfo.insertProfile(userName,name,'_None')
                                xinfo.insertControls([userName,'True','True','False','True','True'\
                                                      ,'True','True','True','True','True','True',\
                                                      'True','True','True'])
                                xinfo.insertInfoList([userName,'0','0','0'])

                                self.xprtNotCreation(userName,cursor)
                                mydb.commit()
                                login=True
                                data=ad.assValue(['code'],['0004'],'error')
                                data=Assemble.aError(data,'user')
                                fuserName=userName      
                                data=data.decode()
                                send.send_message(s,data,'bipin')
                                self.usr[fuserName]=send,recv
                        elif data[0]=='ForgetPassword':

                            userName=values[0]
                            seqA=values[1]
                            cb=db.cb1(cursor,'xprtinfo')

                            cond=cb.checkData('sequrity','userName',userName)
                            if(cond):
                                #UserName exists
                                scond=cb.checkMulAndData('sequrity',['userName','seqA'],[userName,seqA])

                                if(scond):
                                    #@#Sequrity answer is successful

                                    passw=cb.selectParticularData('sequrity','userName','password',userName)
                                    passw=ms.modifySqlResult(passw)
                                    data=ad.assValue(['password'],[passw[0]],'ForgetPasswordResponse')
                                    data=Assemble.aError(data,'user')
                                    data=data.decode()
                                    send.send_message(s,data,'bipin')
                                else:
                                    #Sequrity Answer is not correct
                                    data=ad.assValue(['code'],['0007'],'error')
                                    data=Assemble.aError(data,'user')
                                    data=data.decode()
                                    send.send_message(s,data,'bipin')
                            else:
                                #UserName already exists
                                data=ad.assValue(['code'],['0005'],'error')
                                data=Assemble.aError(data,'user')
                                        
                                data=data.decode()
                                send.send_message(s,data,'bipin')
                        else:
                            print(data[0])
                            print("THIS IS KDFSKLF")
                            data=ad.assValue(['code'],['eeee'],'error')
                            data=Assemble.aError(data,'user')
                                        
                            data=data.decode()
                            send.send_message(s,data,'bipin')
                        
                    elif dtype=='Admin':
                        pass
                    else:
                        if login:
                            
                            if dtype=='System' or dtype=='App' or dtype=='Error' or dtype=='Info':
                                #To the single user only
                                cb=db.cb1(mydb.cursor(),'xprtinfo')
                                if dtype=='Info':
                                    if wType=='EditProfile':
                                       
                                       val=ad.cvtArr2Dict(vType,values)
                                       fValue=val['name']


                                       cb.updateParticularData('sequrity','userName','name',fuserName,fValue)
                                       cb.updateParticularData('profile','userName','name',fuserName,fValue)
                                       data=self.cRequest('0008')
                                       send.send_message(s,data,'bipin')
                                       mydb.commit()
                                    elif wType=='ChangePassword':
                                        index=vType.index('OldPassword')
                                        fValue=values[index]
                                        cond=cb.checkMulAndData('sequrity',['userName','password'],[fuserName,fValue])

                                        if cond:
                                            index=vType.index('Password')
                                            fValue=values[index]
                                            cb.updateParticularData('sequrity','userName','password',fuserName,fValue)
                                            data=self.cRequest('0010')
                                            send.send_message(s,data,'bipin')
                                        else:
                                           data=self.cRequest('0009')
                                           send.send_message(s,data,'bipin')


                                    elif wType=='ChangeSeqQA':
                                        index=vType.index('Password')
                                        passw=values[index]

                                        index=vType.index('seqQ')
                                        seqQ=values[index]

                                        index=vType.index('seqA')
                                        seqA=values[index]
                                        cond=cb.checkMulAndData('sequrity',['userName','password'],[fuserName,passw])

                                        if cond:
                                            cb.updateParticularData('sequrity','userName','seqQ',fuserName,seqQ)
                                            cb.updateParticularData('sequrity','userName','seqA',fuserName,seqA)
                                            data=self.cRequest('0012')
                                            send.send_message(s,data,'bipin')
                                                                    
                                        else:
                                            data=self.cRequest('0011')
                                            send.send_message(s,data,'bipin')
                                    elif wType=='OverallControl':
                                        val=ad.cvtArr2Dict(vType,values)
                                        for i in val:
                                            try:
                                                cb.updateParticularData('overallcontrol','userName',i,fuserName,val[i])
                                            except:
                                                print("Error in sldkjfsdflj")

                                        data=self.cRequest('0013')
                                        send.send_message(s,data,'bipin') 
                                    

                                    elif wType=='SearchFriend':
                                        val=ad.cvtArr2Dict(vType,values)
                                        userName=val['userName']
                                        data=cb.selectByMulOrCond('sequrity',['userName','name'],[userName,userName],'userName,name')
                                        data=ms.modifySqlResult(data)
                                        data=np.array(data)
                                        types=str(data.dtype)
                                        shape=str(data.shape)
                                        data=bytes(data)
                                        
                                        data=data.decode()
                                        
                                        data=ds.enc(data)

                                        data=ad.assValue(['data','types','shape'],[data,types,shape],'searchFriendResponse')

                                        data=Assemble.aError(data,'user')
                                        
                                        data=data.decode()
                                        send.send_message(s,data,'bipin')

                                    elif wType=='SendFriendRequest':
                                        val=ad.cvtArr2Dict(vType,values)
                                        userName=val['userName']
                                        cond=cb.checkData('sequrity','userName',userName)

                                        if cond:

                                            #user Exists
                                            xnot=xdb.XprtNot(mydb.cursor())
                                            tName1='b_'+fuserName
                                            tName2='b_'+userName
                                            cond1=cb.checkData(tName1,'userName',userName)
                                            cond2=cb.checkData(tName2,'userName',fuserName)

                                            if cond1 and cond2:

                                                #Users are blocked 20
                                                data=self.cRequest('0020')
                                                send.send_message(s,data,'bipin')
                                            elif userName==fuserName:
                                                data=self.cRequest('0020')
                                                send.send_message(s,data,'bipin')
                                            else:

                                                xnot.insertFriendRSent(fuserName,userName)
                                                xnot.insertFriendRRecv(userName,fuserName)
                                                notification='{0} sent you a friend request.'.format(fuserName)
                                                xnot.insertNotification(userName,notification)
                                                data=self.cRequest('0021')
                                                send.send_message(s,data,'bipin')
                                        else:

                                            #User dont exists
                                            #22
                                            data=self.cRequest('0022')
                                            send.send_message(s,data,'bipin')

                                    elif wType=='Unfriend':
                                        val=ad.cvtArr2Dict(vType,values)
                                        userName=val['userName']
                                        cond=cb.checkData('sequrity','userName',userName)
                                        if cond:
                                            #user Exists
                                            xnot=xdb.XprtNot(mydb.cursor())
                                            tName1='f_'+fuserName
                                            tName2='f_'+userName
                                            cond1=cb.checkData(tName1,'userName',userName)
                                            cond2=cb.checkData(tName2,'userName',fuserName)

                                            if cond1 and cond2:
                                                xnot.deleteFriend(userName,fuserName)
                                                xnot.deleteFriend(fuserName,userName)
                                                data=self.cRequest('0024')
                                                send.send_message(s,data,'bipin')

                                            else:
                                                data=self.cRequest('0025')
                                                send.send_message(s,data,'bipin')
                                        else:
                                            #User dont exists
                                            #22
                                            data=self.cRequest('0022')
                                            send.send_message(s,data,'bipin')

                                    elif wType=='DeleteFriendRequest':
                                        val=ad.cvtArr2Dict(vType,values)
                                        userName=val['userName']
                                        cond=cb.checkData('sequrity','userName',userName)
                                        if cond:
                                            #user Exists
                                            xnot=xdb.XprtNot(mydb.cursor())
                                            tName1='b_'+fuserName
                                            tName2='b_'+userName
                                            cond1=cb.checkData(tName1,'userName',userName)
                                            cond2=cb.checkData(tName2,'userName',fuserName)

                                            if cond1 and cond2:
                                                #Users are blocked 20
                                                data=self.cRequest('0020')
                                                send.send_message(s,data,'bipin')
                                            else:
                                                xnot.deleteFriendRSent(fuserName,userName)
                                                xnot.deleteFriendRRecv(userName,fuserName)
                                                data=self.cRequest('0021')
                                                send.send_message(s,data,'bipin')
                                        else:
                                            #User dont exists
                                            #22
                                            data=self.cRequest('0022')
                                            send.send_message(s,data,'bipin')
                                    elif wType=='BlockSearch':
                                        val=ad.cvtArr2Dict(vType,values)

                                        userName=val['userName']
                                        cond=cb.checkData('sequrity','userName',userName)
                                        if(cond):
                                            if(userName==fuserName):
                                                data=self.cRequest('0015')
                                                send.send_message(s,data,'bipin')
                                            else:
                                                data=cb.selectByMulOrCond('sequrity',['userName','name'],[userName,userName],'userName,name')
                                                data=cb.modifySqlResult(data)
                                                data=np.array(data)
                                                types=str(data.dtype)
                                                shape=str(data.shape)
                                                data=bytes(data)

                                                data=data.decode()

                                                data=ds.enc(data)

                                                data=ad.assValue(['data','types','shape'],[data,types,shape],'blockSearchResponse')
                                                data=Assemble.aError(data,'user')

                                                data=data.decode()
                                                send.send_message(s,data,'bipin')
                                        else:
                                            #UserName not found
                                            data=self.cRequest('0014')
                                            send.send_message(s,data,'bipin')
                                    elif wType=='Block':
                                        val=ad.cvtArr2Dict(vType,values)
                                        userName=val['userName']
                                        cursor=mydb.cursor()
                                        xnot=xdb.XprtNot(cursor)

                                        xnot.insertBlock(fuserName,userName)
                                        mydb.commit()
                                        data=self.cRequest('0016')
                                        send.send_message(s,data,'bipin')

                                    elif wType=='UnblockLoad':
                                        cursor=mydb.cursor()
                                        xnot=xdb.XprtNot(cursor)
                                        data=xnot.selectBlock(fuserName)
                                        data=np.array(data)
                                        types=str(data.dtype)
                                        shape=str(data.shape)
                                        data=bytes(data)

                                        data=data.decode()

                                        data=ds.enc(data)

                                        data=ad.assValue(['data','types','shape'],[data,types,shape],'UnblockResponse')
                                        data=Assemble.aError(data,'user')

                                        data=data.decode()
                                        send.send_message(s,data,'bipin')

                                    elif wType=='Unblock':
                                        val=ad.cvtArr2Dict(vType,values)
                                        userName=val['userName']
                                        cursor=mydb.cursor()
                                        xnot=xdb.XprtNot(cursor)

                                        xnot.deleteBlock(fuserName,userName)
                                        mydb.commit()
                                        data=self.cRequest('0017')
                                        send.send_message(s,data,'bipin')


                                    elif wType=='FriendRequestLoad':
                                        cursor=mydb.cursor()
                                        xnot=xdb.XprtNot(cursor)
                                        data=xnot.selectFriendRequest(fuserName)
                                        data=ms.modifySqlResult(data)
                                        if data is None or data=='' or data==[]:

                                            data=self.cRequest('0098');
                                            send.send_message(s,data,'bipin')

                                        else:
                                            data=np.array(data)
                                            types=str(data.dtype)
                                            shape=str(data.shape)
                                            data=bytes(data)

                                            data=data.decode()

                                            data=ds.enc(data)

                                            data=ad.assValue(['data','types','shape'],[data,types,shape],'FriendRequestLoadResponse')
                                            data=Assemble.aError(data,'user')

                                            data=data.decode()
                                            send.send_message(s,data,'bipin')
                                    elif wType=='FriendRequestAccept':
                                        val=ad.cvtArr2Dict(vType,values)
                                        userName=val['userName']
                                        cursor=mydb.cursor()
                                        xnot=xdb.XprtNot(cursor)
                                        cond=cb.checkData('fr_'+fuserName,'userName',userName)
                                        if cond:

                                            xnot.insertFriend(fuserName,userName)
                                            xnot.createChat(fuserName,userName)
                                            xnot.deleteFriendRRecv(fuserName,userName)

                                            data=self.cRequest('0097');
                                            send.send_message(s,data,'bipin')

                                        else:
                                            data=self.cRequest('0099');
                                            send.send_message(s,data,'bipin')
                                    elif wType=='Notification':
                                        val=ad.cvtArr2Dict(vType,values)
                                        rangeIn=val['rangeIn']
                                        rangeOut=val['rangeOut']
                                        cursor=mydb.cursor()
                                        xnot=xdb.XprtNot(cursor)
                                        data=xnot.selectNotification(fuserName,rangeIn,rangeOut)
                                        data=np.array(data)
                                        types=str(data.dtype)
                                        shape=str(data.shape)
                                        data=bytes(data)

                                        data=data.decode()

                                        data=ds.enc(data)

                                        data=ad.assValue(['data','types','shape'],[data,types,shape],'NotificationResponse')
                                        data=Assemble.aError(data,'user')

                                        data=data.decode()
                                        send.send_message(s,data,'bipin')

                                    elif wType=='Chat':
                                        val=ad.cvtArr2Dict(vType,values)
                                        rangeIn=val['rangeIn']
                                        rangeOut=val['rangeOut']
                                        userName=val['userName']
                                        cursor=mydb.cursor()
                                        xnot=xdb.XprtNot(cursor)
                                        data=xnot.selectNotification(fuserName,userName,rangeIn,rangeOut)
                                        data=np.array(data)
                                        types=str(data.dtype)
                                        shape=str(data.shape)
                                        data=bytes(data)

                                        data=data.decode()

                                        data=ds.enc(data)

                                        data=ad.assValue(['data','types','shape'],[data,types,shape],'ChatResponse')
                                        data=Assemble.aError(data,'user')

                                        data=data.decode()
                                        send.send_message(s,data,'bipin')

                                    elif wType=='LoadUserProfile':
                                        val=ad.cvtArr2Dict(vType,values)
                                        userName=val['userName']
                                        data=cb.selectParticularData('profile','userName','*',userName)
                                        data=ms.modifySqlResult(data)
                                        if data ==None:
                                            #UserName dont exists
                                            data=self.cRequest('0018')
                                            send.send_message(s,data,'bipin')
                                        else:
                                            userName=data[0]
                                            name=data[1]
                                            img=data[2]
                                            data=ad.assValue(['userName','name','img'],[userName,name,img],'LoadUserProfileResponse')
                                            data=Assemble.aError(data,'user')

                                            data=data.decode()
                                            send.send_message(s,data,'bipin')
                                    elif wType=='LoadGlobalMember':
                                        data=cb.selectFieldData('user','userName')
                                        print("This Field will be activated in later movements")
                                    else:
                                        print("LJKFSDLFD")
                                        data=self.cRequest('eeee')
                                        send.send_message(s,data,'bipin')
                                elif dtype=='System':
                                    if wType=='LoadMainWindow':
                                        #Load Help Data
                                        #FriendRequest Numbers Latest
                                        #Notification Latest Number
                                        #Load all Friends profile
                                        helpData=cb.selectParticularData('_help','_type','_value','mainWindow')
                                        notifNum=cb.selectParticularData('InfoList','userName','notification',fuserName)
                                        friendRNum=cb.selectParticularData('InfoList','userName','friendrequest',fuserName)
                                        profile=[]
                                        tName='F_'+fuserName
                                        data=cb.selectFieldData(tName,'friend')
                                        data=ms.modifySqlResult(data)

                                        if data is not None:
                                            for i in data:
                                                dprofile=cb.selectAllDataByCondition('profile','userName',i)
                                                profile.append(dprofile)

                                        profile=self.prepSend(profile)

                                        #data=ds.enc(data)
                                        profileData=ds.enc(profile[0])
                                        data=ad.assValue(['helpData','notifNum','friendRNum','profileData','profileType','profileShape'],\
                                                         [helpData[0][0],notifNum,friendRNum,profileData,profile[1],profile[2]],'LoadMainWindowResponse')
                                        #data=ad.assValue(['data','types','shape'],[data,types,shape],'searchFriendResponse')
                                        data=Assemble.aError(data,'user')

                                        data=data.decode()
                                        send.send_message(s,data,'bipin')
                                    elif wType=='LoadEditProfile':
                                        helpData=cb.selectParticularData('_help','_type','_value','EditProfile')

                                        data=ad.assValue(['helpData'],[helpData[0][0]],'EditProfileResponse')
                                        data=Assemble.aError(data,'user')
                                        data=data.decode()
                                        send.send_message(s,data,'bipin')

                                    elif wType=='LoadOverallControl':
                                        helpData=cb.selectParticularData('_help','_type','_value','EditProfile')
                                        data=cb.selectAllDataByCondition('overallcontrol','userName',fuserName)
                                        data=self.prepSend(data)
                                        data=ad.assValue(['helpData','overallControlData','overallControlType','LoadOverallControlShape'],[helpData[0][0],data[0],data[1],data[2],'LoadOverallControlResponse'])

                                        data=Assemble.aError(data,'user')
                                        data=data.decode()
                                        send.send_message(s,data,'bipin')

                                    elif wType=='LoadSearchFriend':

                                        helpData=cb.selectParticularData('_help','_type','_value','SearchFriend')
                                        data=ad.assValue(['helpData'],[helpData[0][0]],'LoadSearchFriendResponse')
                                        data=Assemble.aError(data,'user')
                                        data=data.decode()
                                        send.send_message(s,data,'bipin')

                                    elif wType=='LoadBlock&Unblock':
                                        helpData=cb.selectParticularData('_help','_type','_value','SearchFriend')
                                        xnot=xdb.XprtNot(mydb.cursor())
                                        list=xnot.selectBlock(fuserName)
                                        data=self.prepSend(list)
                                        data=ad.assValue(['helpData','Block&UnblockData','Block&UnblockType','Block&UnblockShape'],[helpData[0][0],data[0],data[1],data[2]],'LoadBlock&UnblockResponse')

                                        data=Assemble.aError(data,'user')
                                        data=data.decode()
                                        send.send_message(s,data,'bipin')


                                    elif wType=='LoadFriendRequest':
                                        helpData=cb.selectParticularData('_help','_type','_value','FriendRequest')
                                        xnot=xdb.XprtNot(mydb.cursor())
                                        list=xnot.selectFriendRequest(fuserName)
                                        data=self.prepSend(list)
                                        data=ad.assValue(['helpData','FriendRequestData','FriendRequestType','FriendRequestShape'],[helpData[0][0],data[0],data[1],data[2]],'LoadFriendRequestResponse')
                                        data=Assemble.aError(data,'user')
                                        data=data.decode()
                                        send.send_message(s,data,'bipin')


                                    elif wType=='LoadNotification':
                                        helpData=cb.selectParticularData('_help','_type','_value','Notification')
                                        xnot=xdb.XprtNot(mydb.cursor())
                                        list=xnot.selectNotification(fuserName,0,10)
                                        data=self.prepSend(list)
                                        data=ad.assValue(['helpData','NotificationData','NotificationType','NotificationShape'],[helpData[0][0],data[0],data[1],data[2]],'LoadNotificationResponse')
                                        data=Assemble.aError(data,'user')
                                        data=data.decode()
                                        send.send_message(s,data,'bipin')

                                    elif wType=='LoadFindFriends':
                                        helpData=cb.selectParticularData('_help','_type','_value','FindFriend')
                                        data=ad.assValue(['helpData'],[helpData[0][0]],'FindFriendResponse')
                                        data=Assemble.aError(data,'user')
                                        data=data.decode()
                                        send.send_message(s,data,'bipin')

                                    elif wType=='LoadSystemSettings':
                                        helpData=cb.selectParticularData('_help','_type','_value','SystemSettings')
                                        data=ad.assValue(['helpData'],[helpData[0][0]],'SystemSettingsResponse')
                                        data=Assemble.aError(data,'user')
                                        data=data.decode()
                                        send.send_message(s,data,'bipin')

                                    else:
                                        #This option is not avalable
                                        print("This option is not avalable")


                                elif dtype=='App':
                                    pass
                                else:
                                    #This is error part
                                    pass
                            elif dtype=='Data':

                                i=userName
                                addr=self.nclients[i]
                                cs=self.clients[addr]
                                #ts=ds.Send()
                                val=ad.cvtArr2Dict(vType,values)

                                userName=val['userName']
                                xnot=xdb.XprtNot(mydb.cursor())
                                cb=db.cb1(mydb.cursor(),'xprtinfo')
                                data=cb.selectAllDataByCondition('overallcontrol','userName',userName)
                                data=data[0]
                                if userName in self.nclients:
                                    online=True
                                else:
                                    online=False

                                if wType=='_Text':
                                    print(data[9])
                                    if data[9]=='True':
                                            text=val['text']
                                            text=userName+'-'+text
                                            xnot=xdb.XprtNot(mydb.cursor())
                                            xnot.insertChat(fuserName,userName,text)

                                            data=self.cRequest('0019')
                                            send.send_message(s,data,'bipin')

                                    if wType=='_File':
                                            if data[8]=='True':
                                                pass
                                            else:
                                                data=self.cRequest('d001')
                                                send.send_message(s,data,'bipin')
                                    else:
                                            data=self.cRequest('d002')
                                            send.send_message(s,data,'bipin')

                                else:




                                    if online:
                                        addr=self.nclients[userName]
                                        dSender=self.dclients[addr][0]

                                        if wType=='_Screen':
                                            if data[10]=='True':
                                                screenData=val['screenData']
                                                screenType=val['screenType']
                                                screenShape=val['screenShape']
                                                data=ad.assValue(['userName','screenData','screenType','screenShape'],[fuserName,screenData,screenType,screenShape],'_ScreenResponse')
                                                data=Assemble.aData(data,fuserName)
                                                data=data.decode()
                                                dSender.send_message(cs,data,'bipin')
                                            else:
                                                data=self.cRequest('d003')
                                                send.send_message(s,data,'bipin')

                                        elif wType=='_Cmd':
                                            if data[10]=='True':
                                                screenData=val['cmdData']
                                                screenType=val['cmdType']
                                                screenShape=val['cmdShape']
                                                data=ad.assValue(['userName','cmdData','cmdType','cmdShape'],[fuserName,screenData,screenType,screenShape],'_CmdResponse')
                                                data=Assemble.aData(data,fuserName)

                                                data=data.decode()
                                                dSender.send_message(cs,data,'bipin')
                                            else:
                                                data=self.cRequest('dnn3')
                                                send.send_message(s,data,'bipin')

                                        elif wType=='_Camera':

                                            if data[11]=='True':
                                              
                                                cameraData=val['cameraData']
                                                cameraType=val['cameraType']
                                                cameraShape=val['cameraShape']
                                                data=ad.assValue(['userName','cameraData','cameraType','cameraShape'],[fuserName,cameraData,cameraType,cameraShape],'_CameraResponse')
                                                data=Assemble.aData(data,fuserName)

                                                data=data.decode()
                                                dSender.send_message(cs,data,'bipin')

                                            else:
                                                data=self.cRequest('d004')
                                                send.send_message(s,data,'bipin')

                                        elif wType=='_Voice':
                                            if data[12]=='True':
                                                #print("THIS IS MIC")
                                                type='Voice'
                                                voiceData=val[type.lower()+'Data']

                                                data=ad.assValue(['userName',type.lower()+'Data'],[fuserName,voiceData],'_'+type+'Response')
                                                data=Assemble.aData(data,fuserName)

                                                data=data.decode()
                                                dSender.send_message(cs,data,'bipin')

                                            else:
                                                data=self.cRequest('d005')
                                                send.send_message(s,data,'bipin')

                                        elif wType=='_Mouse':
                                            if data[13]=='True':
                                                type='Mouse'
                                                mouseData=val[type.lower()+'Data']
                                                mouseType=val[type.lower()+'Type']
                                                mouseShape=val[type.lower()+'Shape']
                                                data=ad.assValue(['userName',type.lower()+'Data',type.lower()+'Type',type.lower()+'Shape'],[fuserName,mouseData,mouseType,mouseShape],'_'+type+'Response')
                                                data=Assemble.aData(data,fuserName)

                                                data=data.decode()
                                                dSender.send_message(cs,data,'bipin')

                                            else:
                                                data=self.cRequest('d006')
                                                send.send_message(s,data,'bipin')

                                        elif wType=='_Keyboard':
                                            if data[14]=='True':
                                                type='Keyboard'
                                                keyboardData=val[type.lower()+'Data']
                                                keyboardType=val[type.lower()+'Type']
                                                keyboardShape=val[type.lower()+'Shape']
                                                data=ad.assValue(['userName',type.lower()+'Data',type.lower()+'Type',type.lower()+'Shape'],[fuserName,keyboardData,keyboardType,keyboardShape],'_'+type+'Response')
                                                data=Assemble.aData(data,fuserName)

                                                data=data.decode()
                                                dSender.send_message(cs,data,'bipin')

                                            else:
                                                data=self.cRequest('d007')
                                                send.send_message(s,data,'bipin')

                                        else:
                                            print(wType)
                                            print("This option is not avalable")
                                    else:
                                        data=self.cRequest('dddd')
                                        send.send_message(s,data,'bipin')

                            else:
                                #This option is not avalable
                                print("This optionis not avalable")
                                data=ad.assValue(['code'],['eeee'],'error')
                                data=Assemble.aError(data,'user')
                                        
                                data=data.decode()
                                send.send_message(s,data,'bipin')

                            mydb.commit()

                        else:
                            data=Assemble.aError('0000','user')
                            data=data.decode()
                            send.send_message(s,data,'bipin')

       # except:
        #        print("Error login manager")

    def cRequest(self,error):
        error=str(error)
        data=ad.assValue(['code'],[error],'error')
        data=Assemble.aError(data,'user')
                                        
        data=data.decode()
        return data
    
    def refressList(self):
        while True:
            try:

                self.refressClientList()
                self.refressLoginClient()
                self.refressDClients()
                #time.sleep(5)
            except:
                pass
    def refressClientList(self):
        tf=[]
        for i in self.clients:
            s=self.clients[i]

            send=self.dclients[i][0]
            
            try:
                send.send_message(s,'-----','bipin')
            except:
                tf.append(i)

        for i in tf:
            
                del self.clients[i]

    def refressDClients(self):
        tf=[]
        for i in self.dclients:
            if i in self.clients:
                pass
            else:
                tf.append(i)

        for  i in tf:
            del self.dclients[i]
    

    def refressLoginClient(self):
        tf=[]
        
        for i in self.rnclients:
            
            if(i in self.clients):
                pass
            else:
                tf.append(i)
            

        
        
        for i in tf:
            name=self.rnclients[i]
            del self.rnclients[i]
            del self.nclients[name]
        

                  
s=Server()
