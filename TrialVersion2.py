#Trial Version of server client
#this is server
import ControlUnit as cu
import threading
import DataShare as ds
import AssembleData as ad
import time
import dbquery2 as db
import Xprt_DataBase as xdb
from cryptography.fernet import Fernet
import numpy as np
import myStringLib as ms
import cv2

key=b'eQ5jxFcJNYII5Z4vhBtvT-mNiqx64yQEUln1SOoYEDA='

fernet=Fernet(key)
dAssemble=ad.Dassemble()
Assemble=ad.Assemble()
mydb=db.genMdb()

img='userLogo.png'
img=cv2.imread(img)

img=cv2.resize(img,(200,200))
tcursor=mydb.cursor()
img=bytes(img)

img=ds.encb(img)
img=img.decode()
imgjkil=img

def deleteAllRecords():
    mydb=db.genMdb()
    cursor=mydb.cursor()
    cursor=tcursor
    x=xdb.XprtInfo(cursor)
    x.deleteAllRecords()
    print("All Records are deleted")
mydb=db.genMdb()
def createDataInfo(mydb):
    try:
        mydb.execute('ATTACH DATABASE "xprtinfo.db" as xprtinfo')
    except:
        print("Already in use")
    mydb.execute('create table blocklist (userName varchar(40))');
    mydb.execute('create table infolist (userName varchar(40),friends varchar(20), friendrequest varchar(20),notification varchar(20))');
    mydb.execute('create table profile(userName varchar(40),name varchar(40),profilePic longblob)');
    mydb.execute('create table sequrity (userName varchar(50),seqQ text,name text,seqA text,password text)');
#deleteAllRecords()
#createDataInfo(mydb)
class Server:


    openWindows={}
    onlineUser={}
    def __init__(self):
        self.s=cu.create_server('localhost',8787,5000)
        print("Server is created")
        self.clients={}
        self.dclients={}
        self.myncursor=tcursor

        self.nclients={}

        self.rnclients={}

        self.stNameLogin={}
        self.fuserData={}

        #threading.Thread(target=self.show).start()
        threading.Thread(target=self.clientConnector).start()
        threading.Thread(target=self.refressList).start()

        self.userControlPanel={}
        

    def closeConnection(self,addr):

        if(addr in self.clients):
            s=self.clients[addr]
            s.close()
            del self.clients[addr]

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
                print(addr)

                self.handleClient(c,addr)
            except:
                print("It an error in client connection")

    def handleClient(self,c,addr):

        def fun():
            send=ds.Send(c)
            recv=ds.Recv(c)

            self.dclients[addr]=[send,recv]

            #threading.Thread(target=recv.get,args=(c,'bipin')).start()

            for i in self.dclients:

                send,recv=self.dclients[i]

                threading.Thread(target=self.loginManager,args=(addr,)).start()



            try:

                recv.get()
            except:
                print("I am heree in action")
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
        #print(data)
        if data is None:
            data=[]
        data=np.array(data)
        types=str(data.dtype)
        shape=str(data.shape)
        data=bytes(data)
        data=ds.encb(data)
        data=data.decode()

        return [data,types,shape]

    def loginManager(self,addr):
        print("I AM LOGIN MANAGER")

        login=False
        send,recv=self.dclients[addr]
        fuserName=None

        def function(addr,msg):

                    mydb=db.genMdb()
                    cursor=mydb.cursor()
                    dtype,wType,values=ad.deAssValue(msg)
                    tcursor=cursor
                    info=ad.cvtArr2Dict(wType,values)
                    if addr in self.stNameLogin:
                        fuserName,login=self.stNameLogin[addr]
                    else:
                        fuserName,login=None,False

                    wType=info['wType']
                    t1=time.time()
                    #print(wType,login)
                    if dtype=='Sequrity':


                        tcursor=cursor
                        if wType=='login':

                            userName=info['userName']
                            userPass=info['userPass']
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
                                        #User already exists
                                        addr=self.fuserData[userName]

                                        data=ad.assValue(['code','wType','user','ofType'],['0006','error','user','login'],'Error')

                                        dsend,drecv=self.dclients[addr]
                                        dsend.send_message(data)

                                        #self.closeConnection(addr)
                                        self.nclients[userName.lower()]=addr
                                        self.rnclients[addr]=userName

                                        #print(self.nclients)
                                        #Login Successful
                                        fuserName=userName
                                        Server.onlineUser[fuserName]=True
                                        self.fuserData[userName]=addr
                                        data=ad.assValue(['code','wType','user','ofType'],['0003','error','user','login'],'Error')
                                        send.send_message(data)

                                    else:
                                        self.nclients[userName.lower()]=addr
                                        self.rnclients[addr]=userName

                                        #print(self.nclients)
                                        #Login Successful
                                        fuserName=userName
                                        Server.onlineUser[fuserName]=True
                                        self.fuserData[userName]=addr
                                        data=ad.assValue(['code','wType','user','ofType'],['0003','error','user','login'],'Error')
                                        send.send_message(data)
                                    self.stNameLogin[addr]=[fuserName,login]
                                    


                                else:
                                    login=False
                                    #Password Error
                                    data=ad.assValue(['code','wType','user','ofType'],['0001','error','user','login'],'Error')
                                    send.send_message(data)
                                    self.stNameLogin[addr]=[userName,login]
                            else:

                                #UserName not found error
                                login=False
                                data=ad.assValue(['code','wType','user','ofType'],['0002','error','user','login'],'Error')
                                send.send_message(data)
                                self.stNameLogin[addr]=[userName,login]
                        elif wType=='signUp':
                            userName=info['userName']

                            cb=db.cb1(cursor,'xprtinfo')
                            cond=cb.checkData('sequrity','username',userName)
                            name=info['name']
                            if cond:
                                login=False
                                #UserName already exists
                                data=ad.assValue(['code','wType','user','ofType'],['0005','error','user','signUp'],'Error')
                                send.send_message(data)
                                self.stNameLogin[addr]=[userName,login]
                            else:

                                xinfo=xdb.XprtInfo(cursor)

                                self.nclients[userName]=addr
                                self.rnclients[addr]=userName
                                values=[info['userName'],info['seqQ'],info['name'],info['seqA'],info['userPass']]
                                xinfo.insertSequrity(values)
                                img=imgjkil
                                print(len(img))
                                xinfo.insertProfile(userName,name,img)

                                xinfo.insertInfoList([userName,'0','0','0'])

                                self.xprtNotCreation(userName,cursor)
                                mydb.commit()
                                login=True
                                self.fuserData[userName]=addr
                                data=ad.assValue(['code','wType','user','ofType'],['0004','error','user','signUp'],'Error')
                                fuserName=userName
                                Server.onlineUser[fuserName]=True
                                send.send_message(data)
                                self.stNameLogin[addr]=[userName,login]
                        elif wType=='ForgetPassword':

                            userName=info['userName']
                            seqA=info['seqA']
                            cb=db.cb1(cursor,'xprtinfo')

                            cond=cb.checkData('sequrity','userName',userName)
                            if(cond):
                                #UserName exists
                                scond=cb.checkMulAndData('sequrity',['userName','seqA'],[userName,seqA])

                                if(scond):
                                    #@#Sequrity answer is successful

                                    passw=cb.selectParticularData('sequrity','userName','password',userName)
                                    passw=ms.modifySqlResult(passw)
                                    data=ad.assValue(['password','wType','user','ofType'],[passw[0],'ForgetPasswordResponse','user',wType],'Error')
                                    send.send_message(data)
                                else:
                                    #Sequrity Answer is not correct
                                    data=ad.assValue(['code','wType','user','ofType'],['0007','error','user',wType],'Error')

                                    send.send_message(data)
                            else:
                                #UserName already exists
                                data=ad.assValue(['code','wType','user','ofType'],['0005','error','user',wType],'Error')
                                send.send_message(data)
                        else:

                            print("THIS IS KDFSKLF")
                            data=ad.assValue(['code','wType','user'],['eeee','error','user'],'Error')
                            send.send_message(data)

                    elif dtype=='Admin':
                        pass
                    else:
                        if login:

                            if dtype=='System' or dtype=='App' or dtype=='Error' or dtype=='Info':
                                #To the single user only
                                cb=db.cb1(tcursor,'xprtinfo')
                                bcb=db.cb1(tcursor,'xprtnot')
                                if dtype=='Info':
                                    if wType=='EditProfile':

                                       cb=db.cb1(tcursor,'xprtinfo')
                                       fValue=info['name']
                                       img=info['img']

                                       if img=='_None':
                                           pass
                                       else:
                                           print(len(img))
                                           cb.updateParticularData('profile','userName','profilePic',fuserName,img)
                                           data=self.cRequest('ee08','EditProfile')

                                       if fValue=='_None':
                                           pass
                                       else:
                                           cb.updateParticularData('sequrity','userName','name',fuserName,fValue)
                                           cb.updateParticularData('profile','userName','name',fuserName,fValue)
                                           data=self.cRequest('dd08','EditProfile')




                                       send.send_message(data)
                                       mydb.commit()
                                    elif wType=='ChangePassword':
                                        cb=db.cb1(tcursor,'xprtinfo')
                                        fValue=info['OldPassword']
                                        cond=cb.checkMulAndData('sequrity',['userName','password'],[fuserName,fValue])

                                        if cond:

                                            fValue=info['Password']
                                            cb.updateParticularData('sequrity','userName','password',fuserName,fValue)
                                            data=self.cRequest('0010','ChangePassword')
                                            send.send_message(data)
                                            mydb.commit()
                                        else:
                                           data=self.cRequest('0009','ChangePassword')
                                           send.send_message(data)
                                    elif wType=='ChangeSeqQA':
                                        cb=db.cb1(tcursor,'xprtinfo')
                                        passw=info['Password']

                                        seqQ=info['seqQ']

                                        seqA=info['seqA']

                                        cond=cb.checkMulAndData('sequrity',['userName','password'],[fuserName,passw])

                                        if cond:
                                            cb.updateParticularData('sequrity','userName','seqQ',fuserName,seqQ)
                                            cb.updateParticularData('sequrity','userName','seqA',fuserName,seqA)
                                            data=self.cRequest('0012','ChangeSeqQA')
                                            send.send_message(data)
                                            mydb.commit()

                                        else:
                                            data=self.cRequest('0011','ChangeSeqQA')
                                            send.send_message(data)
                                    elif wType=='OverallControl':
                                        cb=db.cb1(tcursor,'xprtinfo')
                                        val=[info['sFile'],info['sText'],info['sScreen'],info['sCamera']\
                                            , info['sVoice'],info['sMouse'],info['sKeyboard'],info['rFile']\
                                            ,info['rText'],info['rScreen'],info['rCamera'],info['rVoice'],\
                                             info['rMouse'],info['rKeyboard']]
                                        col=cb.getColName('overallControl')
                                        for i in range(1,len(col)):
                                            cb.updateParticularData('overallcontrol','userName',col[i],fuserName,val[i-1])


                                        data=self.cRequest('0013','OverallControl')
                                        send.send_message(data)
                                    elif wType=='SearchFriend':

                                        cb=db.cb1(tcursor,'xprtinfo')
                                        userName=info['userName']
                                        cond=cb.checkData('sequrity','userName',userName)
                                        bcb=db.cb1(tcursor,'xprtnot')
                                        con2=bcb.checkData('f_'+fuserName,'userName',userName)
                                        if cond and (not con2):
                                            bcb=db.cb1(tcursor,'xprtnot')

                                            d1=bcb.selectFieldData('b_'+userName,'userName')
                                            d2=bcb.selectFieldData('b_'+fuserName,'userName')

                                            d1=ms.modifySqlResult(d1)
                                            d2=ms.modifySqlResult(d2)
                                            cb=db.cb1(tcursor,'xprtinfo')
                                            img=cb.selectParticularData('profile','userName','profilePic',userName)
                                            img=ms.modifySqlResult(img)
                                            img=img[0]
                                            if d1==None and d2==None:
                                                data=cb.selectByMulOrCondNot('sequrity',['userName','name'],[userName,userName],['userName'],[fuserName],'userName,name')


                                            elif d1==None:
                                                l=len(d2)
                                                fs=[]
                                                for i in range(l):
                                                    fs.append('userName')
                                                data=cb.selectByMulOrCondNot('sequrity',['userName','name'],[userName,userName],['userName']+fs,[fuserName]+d2,'userName,name')

                                            elif d2==None:
                                                l=len(d1)
                                                fs=[]
                                                for i in range(l):
                                                    fs.append('userName')
                                                data=cb.selectByMulOrCondNot('sequrity',['userName','name'],[userName,userName],['userName']+fs,[fuserName]+d1,'userName,name')

                                            else:
                                                l=len(d1)
                                                fs=[]
                                                for i in range(l):
                                                    fs.append('userName')
                                                l=len(d2)

                                                for i in range(l):
                                                    fs.append('userName')
                                                data=cb.selectByMulOrCondNot('sequrity',['userName','name'],[userName,userName],['userName']+fs,[fuserName]+d1+d2,'userName,name')



                                            data=ms.modifySqlResult(data)
                                            if data==None:
                                                data=[]
                                            data=np.array(data)

                                            types=str(data.dtype)
                                            shape=str(data.shape)
                                            data=bytes(data)
                                            data=ds.encb(data)
                                            data=data.decode()

                                            #data=ds.enc(data)

                                            data=ad.assValue(['data','type','shape','wType','user','ofType','img'],[data,types,shape,'searchFriendResponse','user','SearchFriend',img],'Error')

                                            send.send_message(data)
                                            print("KSDLKF")
                                        else:
                                            if not con2:
                                                data=self.cRequest('0002','SearchFriend')
                                            else:
                                                data=self.cRequest('020202','SearchFriend')
                                            send.send_message(data)

                                    elif wType=='SendFriendRequest':
                                        cb=db.cb1(tcursor,'xprtinfo')
                                        userName=info['userName']
                                        cond=cb.checkData('sequrity','userName',userName)
                                        bcb=db.cb1(tcursor,'xprtnot')
                                        cond2=bcb.checkData('fs_'+fuserName,'userName',userName)
                                        if cond and(not cond2):

                                            #user Exists
                                            xnot=xdb.XprtNot(tcursor)
                                            tName1='b_'+fuserName
                                            tName2='b_'+userName
                                            cond1=cb.checkData(tName1,'userName',userName)
                                            cond2=cb.checkData(tName2,'userName',fuserName)

                                            if cond1 and cond2:

                                                #Users are blocked 20
                                                data=self.cRequest('0020','SendFriendRequest')
                                                send.send_message(data)
                                            elif userName==fuserName:
                                                data=self.cRequest('0020','SendFriendRequest')
                                                send.send_message(data)
                                            else:

                                                xnot.insertFriendRSent(fuserName,userName)
                                                xnot.insertFriendRRecv(userName,fuserName)
                                                notification='{0} sent you a friend request.'.format(fuserName)
                                                xnot.insertNotification(userName,notification)
                                                data=self.cRequest('0021','SendFriendRequest')
                                                send.send_message(data)
                                                mydb.commit()
                                        else:

                                            #User dont exists
                                            #22
                                            if cond:
                                                data=self.cRequest('0022','SendFriendRequest')
                                            else:
                                                data=self.cRequest('22k22','SendFriendRequest')
                                            send.send_message(data)
                                    elif wType=='Unfriend':
                                        cb=db.cb1(tcursor,'xprtinfo')
                                        userName=info['userName']
                                        cond=cb.checkData('sequrity','userName',userName)
                                        if cond:
                                            #user Exists
                                            xnot=xdb.XprtNot(tcursor)
                                            tName1='f_'+fuserName
                                            tName2='f_'+userName
                                            cond1=cb.checkData(tName1,'userName',userName)
                                            cond2=cb.checkData(tName2,'userName',fuserName)

                                            if cond1 and cond2:
                                                xnot.deleteFriend(userName,fuserName)
                                                xnot.deleteFriend(fuserName,userName)
                                                data=self.cRequest('0024','Unfriend')
                                                send.send_message(data)
                                                mydb.commit()

                                            else:
                                                data=self.cRequest('0025','Unfriend')
                                                send.send_message(data)
                                        else:
                                            #User dont exists
                                            #22
                                            data=self.cRequest('0022','Unfriend')
                                            send.send_message(data)
                                    elif wType=='DeleteFriendRequest':
                                        cb=db.cb1(tcursor,'xprtinfo')
                                        userName=info['userName']
                                        cond=cb.checkData('sequrity','userName',userName)
                                        if cond:
                                            #user Exists
                                            xnot=xdb.XprtNot(tcursor)
                                            tName1='b_'+fuserName
                                            tName2='b_'+userName
                                            cond1=cb.checkData(tName1,'userName',userName)
                                            cond2=cb.checkData(tName2,'userName',fuserName)

                                            if cond1 and cond2:
                                                #Users are blocked 20
                                                data=self.cRequest('0020','DeleteFriendRequest')
                                                send.send_message(data)
                                            else:
                                                print("I AM TRYING TO DELETE SOMETHING")
                                                print(fuserName,userName)
                                                xnot.deleteFriendRSent(userName,fuserName)
                                                xnot.deleteFriendRRecv(fuserName,userName)
                                                data=self.cRequest('0021','DeleteFriendRequest')
                                                send.send_message(data)
                                                mydb.commit()
                                        else:
                                            #User dont exists
                                            #22
                                            data=self.cRequest('0022','DeleteFriendRequest')
                                            send.send_message(data)
                                    elif wType=='BlockSearch':

                                        cb=db.cb1(tcursor,'xprtinfo')
                                        userName=info['userName']
                                        cond=cb.checkData('sequrity','userName',userName)
                                        if(cond):
                                            if(userName==fuserName):
                                                data=self.cRequest('0015','BlockSearch')
                                                send.send_message(data)
                                            else:
                                                bcb=db.cb1(tcursor,'xprtnot')

                                                d1=bcb.selectFieldData('b_'+userName,'userName')
                                                d2=bcb.selectFieldData('b_'+fuserName,'userName')

                                                d1=ms.modifySqlResult(d1)
                                                d2=ms.modifySqlResult(d2)
                                                cb=db.cb1(tcursor,'xprtinfo')
                                                img=cb.selectParticularData('profile','userName','profilePic',userName)
                                                img=ms.modifySqlResult(img)
                                                img=img[0]
                                                if d1==None and d2==None:
                                                    data=cb.selectByMulOrCondNot('sequrity',['userName','name'],[userName,userName],['userName'],[fuserName],'userName,name')


                                                elif d1==None:
                                                    l=len(d2)
                                                    fs=[]
                                                    for i in range(l):
                                                        fs.append('userName')
                                                    data=cb.selectByMulOrCondNot('sequrity',['userName','name'],[userName,userName],['userName']+fs,[fuserName]+d2,'userName,name')

                                                elif d2==None:
                                                    l=len(d1)
                                                    fs=[]
                                                    for i in range(l):
                                                        fs.append('userName')
                                                    data=cb.selectByMulOrCondNot('sequrity',['userName','name'],[userName,userName],['userName']+fs,[fuserName]+d1,'userName,name')

                                                else:
                                                    l=len(d1)
                                                    fs=[]
                                                    for i in range(l):
                                                        fs.append('userName')
                                                    l=len(d2)

                                                    for i in range(l):
                                                        fs.append('userName')
                                                    data=cb.selectByMulOrCondNot('sequrity',['userName','name'],[userName,userName],['userName']+fs,[fuserName]+d1+d2,'userName,name')




                                                #data=cb.selectByMulOrCond('sequrity',['userName','name'],[userName,userName],'userName,name')
                                                data=ms.modifySqlResult(data)
                                                if data==None:
                                                    data=[]

                                                data=np.array(data)
                                                types=str(data.dtype)
                                                shape=str(data.shape)
                                                data=bytes(data)


                                                data=ds.encb(data)
                                                data=data.decode()


                                                data=ad.assValue(['code','data','type','shape','wType','user','ofType','img'],['1415skfdlsdf',data,types,shape,'blockSearchResponse','user','BlockSearch',img],'Error')

                                                send.send_message(data)
                                        else:
                                            #UserName not found
                                            data=self.cRequest('0014','BlockSearch')
                                            send.send_message(data)
                                    elif wType=='Block':
                                        cb=db.cb1(tcursor,'xprtinfo')
                                        bcb=db.cb1(tcursor,'xprtnot')
                                        userName=info['userName']
                                        cursor=tcursor
                                        xnot=xdb.XprtNot(cursor)
                                        bcb.deleteBySingleCond('f_'+userName,'userName',fuserName)
                                        bcb.deleteBySingleCond('f_'+fuserName,'userName',userName)

                                        bcb.deleteBySingleCond('fr_'+userName,'userName',fuserName)
                                        bcb.deleteBySingleCond('fr_'+fuserName,'userName',userName)

                                        bcb.deleteBySingleCond('fs_'+userName,'userName',fuserName)
                                        bcb.deleteBySingleCond('fs_'+fuserName,'userName',userName)


                                        xnot.insertBlock(fuserName,userName)
                                        mydb.commit()
                                        data=self.cRequest('0016','Block')
                                        send.send_message(data)
                                    elif wType=='UnblockLoad':
                                        cb=db.cb1(tcursor,'xprtinfo')
                                        cursor=tcursor
                                        xnot=xdb.XprtNot(cursor)
                                        data=xnot.selectBlock(fuserName)

                                        if data==None:
                                            data=[]
                                        imgs=[]
                                        cb=db.cb1(tcursor,'xprtinfo')
                                        for i in data:
                                            im=cb.selectParticularData('profile','userName','profilePic',i)
                                            imgs.append(im[0][0])

                                        imgs=self.prepSend(imgs)
                                        data=np.array(data)
                                        types=str(data.dtype)
                                        shape=str(data.shape)
                                        data=bytes(data)



                                        data=ds.encb(data)
                                        data=data.decode()


                                        data=ad.assValue(['data','type','shape','wType','user','ofType','imgData','imgType','imgShape'],\
                                                         [data,types,shape,'UnblockResponse','user','UnblockLoad',imgs[0],imgs[1],imgs[2]],'Error')

                                        send.send_message(data)
                                    elif wType=='Unblock':
                                        cb=db.cb1(tcursor,'xprtinfo')
                                        userName=info['userName']
                                        cursor=tcursor
                                        xnot=xdb.XprtNot(cursor)

                                        xnot.deleteBlock(fuserName,userName)
                                        xnot.deleteBlock(userName,fuserName)
                                        mydb.commit()
                                        data=self.cRequest('0017','Unblock')
                                        send.send_message(data)
                                    elif wType=='FriendRequestLoad':
                                        cb=db.cb1(tcursor,'xprtinfo')
                                        cursor=tcursor
                                        xnot=xdb.XprtNot(cursor)
                                        data=xnot.selectFriendRequest(fuserName)
                                        data=ms.modifySqlResult(data)
                                        if data is None or data=='' or data==[]:

                                            data=self.cRequest('0098','FriendRequestLoad');
                                            send.send_message(data)

                                        else:
                                            data=np.array(data)
                                            types=str(data.dtype)
                                            shape=str(data.shape)
                                            data=bytes(data)

                                            data=data.decode()

                                            data=ds.enc(data)

                                            data=ad.assValue(['data','types','shape','wType','user','ofType'],[data,types,shape,'FriendRequestLoadResponse','user','FriendRequestLoad'],'Error')

                                            send.send_message(data)
                                    elif wType=='FriendRequestAccept':
                                        cb=db.cb1(tcursor,'xprtinfo')
                                        userName=info['userName']
                                        cursor=tcursor
                                        xnot=xdb.XprtNot(cursor)
                                        cond=cb.checkData('fr_'+fuserName,'userName',userName)
                                        if cond:
                                            print("LSDKFLSKFKF")
                                            xnot.insertFriend(fuserName,userName)
                                            xnot.insertFriend(userName,fuserName)
                                            xnot.insertNotification(userName,fuserName+ ' accepts your friend request')
                                            xnot.createChat(fuserName,userName)
                                            xnot.createChat(userName,fuserName)
                                            xnot.deleteFriendRRecv(fuserName,userName)
                                            xnot.deleteFriendRSent(userName,fuserName)

                                            xnot.deleteFriendRRecv(userName,fuserName)
                                            xnot.deleteFriendRSent(fuserName,userName)

                                            data=self.cRequest('0097','FriendRequestAccept');
                                            send.send_message(data)
                                            mydb.commit()
                                            print("DSKFLSDKFJJF")
                                        else:
                                            data=self.cRequest('0099','FriendRequestAccept');
                                            send.send_message(data)
                                    elif wType=='Notification':

                                        cb=db.cb1(tcursor,'xprtinfo')
                                        val=info
                                        rangeIn=val['rangeIn']
                                        rangeOut=val['rangeOut']
                                        cursor=tcursor
                                        xnot=xdb.XprtNot(cursor)
                                        data=xnot.selectNotification(fuserName,rangeIn,rangeOut)
                                        if data==None:
                                            data=[]
                                        data=np.array(data)
                                        types=str(data.dtype)
                                        shape=str(data.shape)
                                        data=bytes(data)

                                        data=ds.encb(data)

                                        data=data.decode()

                                        data=ad.assValue(['data','type','shape','wType','user','ofType'],[data,types,shape,'NotificationResponse','user','Notification'],'Error')

                                        send.send_message(data)
                                    elif wType=='Chat':
                                        cb=db.cb1(tcursor,'xprtinfo')
                                        val=ad.cvtArr2Dict(vType,values)
                                        rangeIn=val['rangeIn']
                                        rangeOut=val['rangeOut']
                                        userName=val['userName']
                                        cursor=tcursor
                                        xnot=xdb.XprtNot(cursor)
                                        data=xnot.selectNotification(fuserName,userName,rangeIn,rangeOut)
                                        data=np.array(data)
                                        types=str(data.dtype)
                                        shape=str(data.shape)
                                        data=bytes(data)

                                        data=data.decode()

                                        data=ds.enc(data)

                                        data=ad.assValue(['data','types','shape','wType','user','ofType'],[data,types,shape,'ChatResponse','user','Chat'],'Error')

                                        send.send_message(data)
                                    elif wType=='LoadUserProfile':
                                        cb=db.cb1(tcursor,'xprtinfo')
                                        userName=info['userName']
                                        data=cb.selectParticularData('profile','userName','*',userName)
                                        data=ms.modifySqlResult(data)
                                        if data ==None:
                                            #UserName dont exists
                                            data=self.cRequest('0018','LoadUserProfile')
                                            send.send_message(data)
                                        else:
                                            userName=data[0]
                                            name=data[1]
                                            img=data[2]
                                            data=ad.assValue(['userName','name','img','wType','user','ofType'],[userName,name,img,'LoadUserProfileResponse','user','LoadUserProfile'],'Error')

                                            send.send_message(data)
                                    elif wType=='LoadGlobalMember':
                                        cb=db.cb1(tcursor,'xprtinfo')
                                        data=cb.selectFieldData('user','userName')
                                        print("This Field will be activated in later movements")
                                    else:
                                        print("LJKFSDLFD")
                                        data=self.cRequest('eeee','ElsePart')
                                        send.send_message(data)
                                elif dtype=='System':
                                    if   wType=='LoadMainWindow':

                                        #FriendRequest Numbers Latest
                                        #Notification Latest Number
                                        #Load all Friends profile
                                        cb=db.cb1(tcursor,'xprtinfo')

                                        notifNum=cb.selectParticularData('InfoList','userName','notification',fuserName)
                                        friendRNum=cb.selectParticularData('InfoList','userName','friendrequest',fuserName)
                                        profile=[]
                                        tName='F_'+fuserName
                                        bcb=db.cb1(tcursor,'xprtnot')
                                        data=bcb.selectFieldData(tName,'userName')
                                        data=ms.modifySqlResult(data)
                                        cb=db.cb1(tcursor,'xprtinfo')
                                        if data is not None:
                                            for i in data:

                                                dprofile=cb.selectAllDataByCondition('profile','userName',i)
                                                profile.append(dprofile)




                                        profile=self.prepSend(profile)

                                        #data=ds.enc(data)
                                        #profileData=ds.enc(profile[0])

                                        data=ad.assValue(['notifNum','friendRNum','profileData','profileType','profileShape','wType','user','ofType'],\
                                                         [notifNum,friendRNum,profile[0],profile[1],profile[2],'LoadMainWindowResponse','user','LoadMainWindow'],'Error')
                                        #data=ad.assValue(['data','types','shape'],[data,types,shape],'searchFriendResponse')

                                        send.send_message(data)
                                    elif wType=='LoadEditProfile':
                                        cb=db.cb1(tcursor,'xprtinfo')


                                        img=cb.selectParticularData('profile','userName','profilePic',fuserName)

                                        img=img[0][0]

                                        data=ad.assValue(['wType','user','ofType','img'],['EditProfileResponse','user','LoadEditProfile',img],'Error')

                                        send.send_message(data)
                                    elif wType=='LoadOverallControl':
                                        cb=db.cb1(tcursor,'xprtinfo')

                                        data=cb.selectAllDataByCondition('overallcontrol','userName',fuserName)
                                        data=self.prepSend(data)

                                        data=ad.assValue(['overallControlData','overallControlType','overallControlShape','wType','user','ofType']\
                                                         ,[data[0],data[1],data[2],'LoadOverallControlResponse','user','LoadOverallControl'],'Error')


                                        send.send_message(data)
                                    elif wType=='LoadFriendControl':
                                        cb=db.cb1(tcursor,'xprtinfo')

                                        usr=info['user']
                                        cb=db.cb1(tcursor,'xprtnot')
                                        data=cb.selectAllDataByCondition('f_'+fuserName,'userName',usr)
                                        data=self.prepSend(data)

                                        data=ad.assValue(['overallControlData','overallControlType','overallControlShape','wType','user','ofType']\
                                                         ,[data[0],data[1],data[2],'LoadFriendControlResponse','user','LoadFriendControl'],'Error')
                                        send.send_message(data)
                                    elif wType=='LoadChatWindow':
                                        user=info['user']
                                        cond=info['status']
                                        online=False
                                        if user in Server.onlineUser:
                                            online=Server.onlineUser[user]

                                        if cond=='False':
                                            Server.openWindows[user+'_'+fuserName]=False
                                            del self.userControlPanel[fuserName+'-'+user]
                                        else:
                                            Server.openWindows[user+'_'+fuserName]=True
                                            cb=db.cb1(tcursor,'xprtnot')
                                            chatData=cb.selectAllData('c_'+fuserName+'_'+user)

                                            data=cb.selectAllDataByCondition('f_'+user,'userName',fuserName)
                                            data2=cb.selectAllDataByCondition('f_'+fuserName,'userName',user)
                                            self.userControlPanel[fuserName+'-'+user]=data[0]
                                            print(fuserName,data)
                                            data=self.prepSend(data)
                                            data2=self.prepSend(data2)
                                            chatData=self.prepSend(chatData)
                                            data=ad.assValue(['data','type','shape','data2','type2','shape2'\
                                                                 ,'wType','user','ofType','online','chatData','chatType','chatShape','user']\
                                                             ,[data[0],data[1],data[2],data2[0],data2[1],data2[2],\
                                                               'LoadChatWindowResponse',user,'LoadChatWindow',online,chatData[0],chatData[1],chatData[2],user],'Data')

                                            send.send_message(data)
                                    elif wType=='LoadSearchFriend':
                                        cb=db.cb1(tcursor,'xprtinfo')


                                        data=ad.assValue(['wType','user','ofType'],['LoadSearchFriendResponse','user','LoadSearchFriend'],'Error')

                                        send.send_message(data)
                                    elif wType=='LoadBlock&Unblock':
                                        cb=db.cb1(tcursor,'xprtinfo')

                                        xnot=xdb.XprtNot(tcursor)
                                        list=xnot.selectBlock(fuserName)
                                        data=self.prepSend(list)
                                        data=ad.assValue(['Block&UnblockData','Block&UnblockType','Block&UnblockShape','wType','user','ofType']\
                                                         ,[data[0],data[1],data[2],'LoadBlock&UnblockResponse','user','LoadBlock&Unblock'],'Error')


                                        send.send_message(data)
                                    elif wType=='LoadFriendRequest':
                                        cb=db.cb1(tcursor,'xprtinfo')

                                        xnot=xdb.XprtNot(tcursor)
                                        list=xnot.selectFriendRequest(fuserName)

                                        list=ms.modifySqlResult(list)
                                        if list is None:
                                            data=self.cRequest('kkkk','LoadFriendRequestResponser')
                                            send.send_message(data)
                                        else:
                                            data=self.prepSend(list)
                                            imgs=[]
                                            for i in list:
                                                cb=db.cb1(tcursor,'xprtinfo')
                                                d=cb.selectParticularData('profile','userName','profilePic',i)
                                                d=ms.modifySqlResult(d)

                                                d=d[0]
                                                imgs.append(d)
                                            imgs=np.array(imgs)

                                            imgd=self.prepSend(imgs)

                                            data=ad.assValue(['FriendRequestData','FriendRequestType','FriendRequestShape','wType','user','ofType','im','imtype','imshape'],\
                                                             [data[0],data[1],data[2],'LoadFriendRequestResponse','user','LoadFriendRequest',imgd[0],imgd[1],imgd[2]],'Error')

                                            send.send_message(data)
                                    elif wType=='LoadNotification':
                                        cb=db.cb1(tcursor,'xprtinfo')

                                        xnot=xdb.XprtNot(tcursor)
                                        list=xnot.selectNotification(fuserName,0,10)
                                        data=self.prepSend(list)
                                        data=ad.assValue(['NotificationData','NotificationType','NotificationShape','wType','user','ofType']\
                                                         ,[data[0],data[1],data[2],'LoadNotificationResponse','user','LoadNotification'],'Error')

                                        send.send_message(data)
                                    elif wType=='LoadFindFriends':
                                        cb=db.cb1(tcursor,'xprtinfo')

                                        data=ad.assValue(['wType','user','ofType'],['FindFriendResponse','user','LoadFindFriends'],'Error')

                                        send.send_message(data)
                                    elif wType=='LoadSystemSettings':
                                        cb=db.cb1(tcursor,'xprtinfo')

                                        data=ad.assValue(['wType','user','ofType'],['SystemSettingsResponse','user','LoadSystemSettings'],'Error')

                                        send.send_message(data)
                                    else:
                                        #This option is not avalable
                                        print("This option is not avalable")
                                elif dtype=='App':
                                    pass
                                else:
                                    print("HTAG this is error part which will never came in this type of area")
                            elif dtype=='Data':
                                userName=info['userName'].lower()
                                try:
                                    openCondition=Server.openWindows[fuserName+'_'+userName]
                                except:
                                    openCondition=False
                                
                                dcond=None

                                cond=self.userControlPanel[fuserName+'-'+userName]
                                #cond=cb.selectAllCheckData('f_'+userName,'userName',fuserName)[0]
                                cols=['sno', 'userName', '_sScreen', '_sCamera', '_sVoice', '_sMouse', '_sKeyboard', '_rScreen', '_rCamera', '_rVoice', '_rMouse', '_rKeyboard']


                                finfo=ad.cvtArr2Dict(cols,cond)

                                #print(finfo)
                                wType=info['wType']
                                cs=None

                                online=False

                                if userName in self.nclients:
                                    online=True

                                    addr=self.nclients[userName]


                                    dcond=self.dclients[addr]
                                
                                if wType=='_Text':
                                    text=fuserName+'->'+info['text']
                                    xnot=xdb.XprtNot(tcursor)
                                    xnot.insertChat(fuserName,userName,text)
                                    xnot.insertChat(userName,fuserName,text)

                                    if online and openCondition:
                                        data=ad.assValue(['text','wType','ofType','user','wt'],[info['text'],'Text','_Text',fuserName,'wt'],'Data')
                                        dcond[0].send_message(data)

                                    mydb.commit()
                                elif wType=='_Screen':
                                    #print(fuserName+'->'+userName)
                                    data=info['screenData']
                                    type=info['screenType']
                                    shape=info['screenShape']
                                    if  online and (int(finfo['_rScreen'])==1) and openCondition:
                                        
                                        data=ad.assValue(['screenData','screenType','screenShape','wType','ofType','user','wt'],[data,type,shape,'Screen','_Screen',fuserName,'wt'],'Data')
                                        dcond[0].send_message(data)



                                    else:

                                        if online :
                                            #print("ONLINE")
                                            data=self.cRequest('UsrO00','_Screen','Data')
                                        else:
                                            if openCondition==False:
                                                #print("OPEN CONDINTION")
                                                data=self.cRequest('UsrC00','_Screen','Data')
                                            else:
                                                #print("KKR CONDITION")

                                                data=self.cRequest('UsrD00','_Screen','Data')
                                        send.send_message(data)

                                elif wType=='_Camera':
                                    data=info['cameraData']
                                    type=info['cameraType']
                                    shape=info['cameraShape']
                                    if  online and int(finfo['_rCamera']) and openCondition:
                                        data=ad.assValue(['cameraData','cameraType','cameraShape','wType','ofType','user','wt']\
                                                         ,[data,type,shape,'Camera','_Camera',fuserName,'wt'],'Data')
                                        dcond[0].send_message(data)
                                    else:

                                        if online:
                                            data=self.cRequest('UsrO01','_Camera','Data')
                                        else:
                                            if openCondition==False:
                                                data=self.cRequest('UsrC01','_Camera','Data')
                                            else:
                                                data=self.cRequest('UsrD01','_Camera','Data')
                                        send.send_message(data)
                                elif wType=='_Voice':
                                    data=info['voiceData']

                                    if  online and int(finfo['_rVoice']) and openCondition:
                                        data=ad.assValue(['voiceData','wType','ofType','user','wt']\
                                                         ,[data,'Voice','_Voice',fuserName,'wt'],'Data')
                                        dcond[0].send_message(data)
                                    else:

                                        if online:
                                            data=self.cRequest('UsrO02','_Voice','Data')
                                        else:
                                            if openCondition==False:
                                                data=self.cRequest('UsrC02','_Voice','Data')
                                            else:
                                                data=self.cRequest('UsrD02','_Voice','Data')
                                        send.send_message(data)
                                elif wType=='_Keyboard':
                                    data=info['keyboardData']
                                    type=info['keyboardType']
                                    shape=info['keyboardShape']
                                    if  online and int(finfo['_rKeyboard']) and openCondition:
                                        data=ad.assValue(['keyboardData','keyboardType','keyboardShape','wType','ofType','user','wt']\
                                                         ,[data,type,shape,'Keyboard','_Keyboard',fuserName,'wt'],'Data')
                                        dcond[0].send_message(data)
                                    else:

                                        if online:
                                            data=self.cRequest('UsrO03','_Keyboard','Data')
                                        else:
                                            if openCondition==False:
                                                data=self.cRequest('UsrC03','_Keyboard','Data')
                                            else:
                                                data=self.cRequest('UsrD03','_Keyboard','Data')
                                        send.send_message(data)
                                elif wType=='_Mouse':
                                    data=info['mouseData']
                                    type=info['mouseType']
                                    shape=info['mouseShape']
                                    if  online and int(finfo['_rMouse']) and openCondition:
                                        data=ad.assValue(['mouseData','mouseType','mouseShape','wType','ofType','user','wt']\
                                                         ,[data,type,shape,'Mouse','_Mouse',fuserName,'wt'],'Data')
                                        dcond[0].send_message(data)
                                    else:

                                        if online:
                                            data=self.cRequest('UsrO04','_Mouse','Data')
                                        else:
                                            if openCondition==False:
                                                data=self.cRequest('UsrC04','_Mouse','Data')
                                            else:
                                                data=self.cRequest('UsrD04','_Mouse','Data')
                                        send.send_message(data)
                                elif wType=='_File':
                                    pass

                            elif dtype=='UserData':
                                if wType=='UpdateFriendControls':
                                        cb=db.cb1(tcursor,'xprtnot')
                                        val=[info['_sScreen'],info['_sCamera']\
                                            , info['_sVoice'],info['_sMouse'],info['_sKeyboard'],info['_rScreen'],info['_rCamera'],info['_rVoice'],\
                                             info['_rMouse'],info['_rKeyboard']]
                                        usr=info['user']
                                        col=cb.getColName('f_'+usr)
                                        print(val)
                                        self.userControlPanel[usr+'_'+fuserName]=['1',usr]+val
                                        print(usr,['1',usr]+val)
                                        for i in range(2,len(col)):
                                            cb.updateParticularData('f_'+fuserName,'userName',col[i],usr,val[i-2])

                                        print('f_'+fuserName)
                                        print("UPDATION COMPLETED")
                                        data=self.cRequest2('d26d','UpdateFriendControls','UserData',usr)
                                        send.send_message(data)

                                elif wType=='UpdateFriendControl':
                                    cb=db.cb1(tcursor,'xprtnot')
                                    field=info['field']
                                    value=info['fieldValue']
                                    user=info['user']

                                    
                                    cb.updateParticularData('f_'+fuserName,'userName',field,user,value)
                                    data=self.cRequest2('d27d','UpdateFriendControl1','UserData',user)
                                    send.send_message(data)
                                elif wType=='Request':
                                    cdType=info['cdType']
                                    usr=info['user'].lower()
                                    try:

                                        addr=self.nclients[usr]
                                        print("I AM TH UAWE ",usr)
                                        
                                        dcond=self.dclients[addr]
                                        data=ad.assValue(['user','cdType','ofType','wType'],[fuserName,cdType,'Request','Request'],'Request')
                                        dcond[0].send_message(data)
                                    except:
                                        data=self.cRequest2('don4','Request','UserData')
                                        send.send_message(data)

                                elif wType=='RequestResponse':
                                    cdType=info['cdType']
                                    usr=info['user'].lower()
                                    try:
                                        addr=self.nclients[usr.lower()]
                                        
                                        dcond=self.dclients[addr]
                                        value=info['value']
                                        data=ad.assValue(['user','cdType','ofType','value','wType'],[usr,cdType,'RequestResponse',value,'RequestResponse'],'RequestResponse')
                                        dcond[0].send_message(data)
                                    except:
                                        data=self.cRequest2('don4','RequestResponse','UserData')
                                        send.send_message(data)

                                else:

                                    print(wType)
                                    print("I dont know what ur searching For")
                            else:
                                #This option is not avalable
                                print("This optionis not avalable")
                                data=self.cRequest('eeee','deElsePart')
                                send.send_message(data)

                            #mydb.commit()

                        else:
                            data=self.cRequest('0000','OOElsePart')
                            send.send_message(data)
                    t2=time.time()
                    #print(t2-t1)
                    #print(wType,'End')

        recv.function=function
        recv.argument=addr
       

                    
                #Server.onlineUser[fuserName]=False

    def cRequest(self,error,ofType=None,wType='wType'):
        error=str(error)
        if ofType !=None:
            data=ad.assValue(['code','wType','user','ofType','wfType'],[error,'error','user',ofType,wType],'Error')
        else:
            data=ad.assValue(['code','wType','user'],[error,'error','user'],'Error')

        return data

    def cRequest2(self,error,ofType=None,wType='wType',user=''):
        error=str(error)
        if ofType !=None:
            if user=='':
                data=ad.assValue(['code','wType','user','ofType','wfType'],[error,'error','user',ofType,wType],'UserData')
            else:
                data=ad.assValue(['code','wType','user','ofType','wfType','user'],[error,'error','user',ofType,wType,user],'UserData')

        else:
            data=ad.assValue(['code','wType','user'],[error,'error','user'],'UserData')

        return data

    def refressList(self):
        while True:
            try:

                self.refressClientList()
                self.refressLoginClient()
                
                #time.sleep(5)
            except:
                pass

    def refressClientList(self):
        tf=[]
        for i in self.clients:
            s=self.clients[i]

            

            try:
                s.send(b'')
            except:
                tf.append(i)

        for i in tf:
                
                del self.clients[i]
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
