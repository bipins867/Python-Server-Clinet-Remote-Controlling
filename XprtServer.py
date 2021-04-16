#XX-81
#XprtServer
import ControlUnit as cu 
import dbquery2 as db
import AssembleData as ad 
import TestingDataSharePh1 as ds
import myStringLib as ms 
import sys
import threading
import XprtDataBase as xdb
import Gui_Creation as gc
import cv2
import numpy as np
import time
import random
import FileIOManager as fim
import ArrayEditing as ae
import ast

opFile=fim.OperateFiles()


HOST='localhost'
HOST=''
#import XprtClient
location='C:\\XprtDataBase\\'

if HOST=='':
    DEFAULT_IMAGE_LOCATION='C:\\Python37\\userLogoM.png'
else:
    DEFAULT_IMAGE_LOCATION='C:\\Python\\userLogoM.png'
data=cv2.imread(DEFAULT_IMAGE_LOCATION)
cond,DEFAULT_IMAGE_DATA=cv2.imencode('*.jpg',data)
DEFAULT_IMAGE_DATA=ds.encb(DEFAULT_IMAGE_DATA).decode()
DEFAULT_IMAGE_TYPE=data.dtype
DEFAULT_IMAGE_SHAPE=data.shape



DEFAULT_CAMERA_RES=144
DEFAULT_SCREEN_RES=144

DEFAULT_SCREEN_FPS=15
DEFAULT_CAMERA_FPS=15

class Server:


    def __init__(self):
        print("Server class is Activated")
        self.defaultImageLocation='_None'

        #--------------------------------
        self.userAddrSR={}
        self.userAddrNL={}
        self.userNAddr={}
        self.dbHandleAddr={}

        self.userWindows={}
        self.userControls={}

        #----------------------------

        self.userDataList={}


        self.MeetingId={}
        self.MeetingMembers={}
        self.MeetingContData={}
        self.MembersMeeting={}
        self.MeetingLock={}
        self.MeetingAuthReq={}
        self.MeetingSendCont={}

        self.clientVersion='1.001'
        self.leastVersion='1.001'
        self.versionLink='I dont know .com '

        self.dataContainer={}
        self.dataResizeController={}

    def startServer(self,address='192.168.43.177',port=9898,no_of_clients=1000):
        try:
            print(address,port)
            c=cu.create_server(address,port,no_of_clients)

            print("Server is created")
        except:
            print("Unable to Create Server")
            sys.exit(1)

        threading.Thread(target=self.clientConnector,args=(c,)).start()
        #threading.Thread(target=self.alwaysRunning).start()

    def handleConnectionError(self,addr):
        #print("IDKLFDFKLFK")
        send,recv=self.userAddrSR[addr]
        send.s.close()
        if addr in self.userAddrNL:
            userName,Login=self.userAddrNL[addr]
            self.onOfflineUser(userName.lower(),addr)
            if addr in self.userAddrNL:
                del self.userAddrNL[addr]
            if userName.lower() in self.userNAddr:
                del self.userNAddr[userName.lower()]
            if userName.lower() in self.userControls:
                del self.userControls[userName.lower()]
            if userName.lower() in self.userWindows:
                del self.userWindows[userName.lower()]
        print("Offline ADDRESS :- ",addr)
        if addr in self.userAddrSR:
            del self.userAddrSR[addr]

        if addr in self.dbHandleAddr:
            del self.dbHandleAddr[addr]

    def onSendErrorOffline(self):
        pass

    def alwaysRunning(self):
        while True:
            d=self.userAddrSR.copy()
            print(self.MeetingId)
            print(self.MeetingMembers)
            print(self.MembersMeeting)

            print("------------------------------------")
            time.sleep(3)

    def clientConnector(self,c):
        while True:
            s,addr=c.accept()
            #self.onSendErrorOffline
            send=ds.Send(s)
            recv=ds.Recv(s)

            recv.setHandleFileFunction(self.handleOnFileStartRecv
                                       ,self.handleOnFileEndRecv)

            self.userAddrSR[addr]=[send,recv]
            print("Connected S :-",addr)
            recv.function=self.handleClient
            recv.argument=addr
            recv.errorFunction=self.handleConnectionError
            recv.errorFunctionArg=addr
            mydb=db.genMdb()
            self.dbHandleAddr[addr]=mydb
            recv.get()

    def getSendByAddr(self,addr):
        if addr in self.userAddrSR:
            return self.userAddrSR[addr][0]

    def handleClient(self,addr,msg):


        dtype,info=ad.deAssValue(msg,dicts=True)

        wType=info['wType']

        if dtype=='sequrity':
            if wType=='login':
                self._login(info,addr)
            elif wType=='signUp':
	            self._signUp(info,addr)
            elif wType=='forgetPassword':
                self._forgetPassword(info,addr)
            elif wType=='changePassword':
                self._changePassword(info,addr)
            elif wType=='getSequrityQuestion':
                self.getSequrityQuestion(info,addr)
            elif wType=='logOut':
                self.logOut(info,addr)
            elif wType=='initCheckVersion':
                self.initCheckVersion(info,addr)
            else:
                print("This option is not avalable")
        else:
            if dtype=='information':
                if wType=='editProfile':
                    self._editProfile(info,addr)
                elif wType=='updateHideProfile':
                    self.updateHideProfile(info,addr)
                elif wType=='changeSeqQA':
                    self._changeSeqQA(info,addr)
                elif wType=='searchFriend':
                    self._searchFriend(info,addr)
                elif wType=='refressSearch':
                    self.refressSearch(info,addr)
                elif wType=='sendFriendRequest':
                    self._sendFriendRequest(info,addr)
                elif wType=='unfriend':
                    self._unfriend(info,addr)
                elif wType=='deleteFriendRequest':
                    self._deleteFriendRequest(info,addr)
                elif wType=='blockSearch':
                    self._blockSearch(info,addr)
                elif wType=='block':
                    self._block(info,addr)
                elif wType=='unblockLoad':
                    self._unblockLoad(info,addr)
                elif wType=='unblock':
                    self._unblock(info,addr)
                elif wType=='loadFriendRequest':

                    self._loadFriendRequest(info,addr)

                elif wType=='friendRequestAccept':
                    self._friendRequestAccept(info,addr)
                elif wType=='loadUserProfile':
                    self._loadUserProfile(info,addr)
                elif wType=='friendListLoad':
                    self._friendListLoad(info,addr)
                else:
                    print("This option not avalable in information")

            elif dtype=='request':
                if wType=='request':
                    self.request(info,addr)
                elif wType=='response':
                    self.response(info,addr)
                else:
                    print("UNKNOWN request your are expecting",wType)
            elif dtype=='system':
                if wType=='loadMainWindow':
                    self._loadMainWindow(info,addr)
                elif wType=='loadEditProfile':
                    self._loadEditProfile(info,addr)
                elif wType=='loadFriendControl':
                    self._loadFriendControl(info,addr)
                elif wType=='loadChatWindow':
                    self._loadChatWindow(info,addr)
                elif wType=='loadSearchFriend':
                    self._loadSearchFriend(info,addr)
                elif wType=='loadBlockUnblock':
                    self._loadBlockUnblock(info,addr)

                elif wType=='loadNotification':
                    self._loadNotification(info,addr)
                elif wType=='loadFindFriends':
                    self._loadFindFriends(info,addr)
                elif wType=='loadSystemSettings':
                    self._loadSystemSetting(info,addr)

            elif dtype=='data':

                if wType=='_Text':
                    self._Text(info,addr)
                elif wType=='_File':
                    self._File(info,addr)
                elif wType=='_Screen':
                    self._Screen(info,addr)
                elif wType=='_Camera':
                    self._Camera(info,addr)
                elif wType=='_Sound':
                    self._Sound(info,addr)
                elif wType=='_Keyboard':
                    self._Keyboard(info,addr)
                elif wType=='_Mouse':
                    self._Mouse(info,addr)
                elif wType=='_IntSound':
                    self._IntSound(info,addr)

                elif wType=='updateControls':
                    self.updateControls(info,addr)
                elif wType=='loadChat':
                    self._loadChat(info,addr)
                else:
                    print("This option is not avalable in data")

            elif dtype=='DataRequest':
                if wType=='DownloadFile':
                    self.DownloadFile(info,addr)
                elif wType=='cancelDownloadFile':
                    self.cancelDownloadFile(info,addr)
                else:
                    print("Unknow DataRequest Type")

            elif dtype=='GroupChat':

                if wType=='createGroup':
                    self.createGroup(info,addr)
                elif wType=='refressGCSearch':
                    self.refressGCSearch(info,addr)
                elif wType=='searchGroup':
                    self.searchGroup(info,addr)
                elif wType=='loadGroupInfo':
                    self.loadGroupInfo(info,addr)
                elif wType=='sendGroupRequest':
                    self.sendGroupRequest(info,addr)
                elif wType=='loadGroupRequest':
                    self.loadGroupRequest(info,addr)
                elif wType=='acceptGroupRequest':
                    self.acceptGroupRequest(info,addr)
                elif wType=='loadGroupChatInfo':
                    self.loadGroupChatInfo(info,addr)
                elif wType=='groupControlPanel':
                    self.groupControlPanel(info,addr)
                elif wType=='leaveGroup':
                    self.leaveGroup(info,addr)
                elif wType=='groupSendRequest':
                    self.groupSendRequest(info,addr)
                elif wType=='sendGroupChat':
                    self.sendGroupChat(info,addr)
                elif wType=='refressGC':
                    self.refressGC(info,addr)
                elif wType=='groupChatWindow':
                    self.groupChatWindow(info,addr)
                elif wType=='kickMemberGroupChat':
                    self.kickMemberGroupChat(info,addr)
                elif wType=='cancelGroupSendRequest':
                    self.cancelGroupSendRequest(info,addr)
                elif wType=='groupSearchMemberForSRequest':
                    self.groupSearchMemberForSRequest(info,addr)
                else:
                    print("This group meet option not avalable",wType)

            elif dtype=='GroupMeet':
                if wType=='gmCreateMeeting':
                    self.gmCreateMeeting(info,addr)
                elif wType=='gmJoinMeeting':
                    self.gmJoinMeeting(info,addr)
                elif wType=='gmLeaveMeeting':
                    self.gmLeaveMeeting(info,addr)
                elif wType=='gmSendChat':
                    self.gmSendChat(info,addr)
                elif wType=='gmKickOut':
                    self.gmKickOut(info,addr)
                elif wType=='gmLockMeeting':
                    self.gmLockMeeting(info,addr)
                elif wType=='gmAuthRequest':
                    self.gmAuthRequest(info,addr)
                elif wType=='gmJoinClientRequestResponse':
                    self.gmJoinClientRequestResponse(info,addr)
                elif wType=='gmOnClose':
                    self.gmOnClose(info,addr)
                elif wType=='gmUpdateOCamCont':
                    self.gmUpdateOCamCont(info,addr)
                elif wType=='gmUpdateOMicCont':
                    self.gmUpdateOMicCont(info,addr)
                elif wType=='gmUpdateUCamCont':
                    self.gmUpdateUCamCont(info,addr)
                elif wType=='gmUpdateUMicCont':
                    self.gmUpdateUMicCont(info,addr)
                elif wType=='gmUpdateYourSendCont':
                    self.gmUpdateYourSendCont(info,addr)
                else:
                    print("Group Meet wType error ",wType)

            elif dtype=='InfoGetter':
                if wType=='iGGetInformation':
                    self.iGGetInformation(info,addr)
                elif wType=='iGGetInfoC':
                    self.iGGetInfoC(info,addr)
                elif wType=='iGGetInfoG':
                    self.iGGetInfoG(info,addr)
                else:
                    print("Error Coded wType Information ",wType)

            elif dtype=='feedback':

                if wType=='feedback':
                    self.ySendFeedback(info,addr)
                else:
                    print("Unknown Feedback ",wType)

            elif dtype=='About':

                if wType=='checkVersion':
                    self.yCheckVersion(info,addr)
                else:
                    print("Unknown Checking Version ",wType)

            elif dtype=='ControlPanel':
                if wType=='updateDataRFController':
                    self.updateDataRFController(info,addr)
                elif wType=='loadDataRFController':
                    self.loadDataRFController(info,addr)
                else:
                    print("Unknown Control Panel ",wType)
            else:
                print("This option is not avalable")

    def handleFileOnUserOffline(self,userName):
        recv=self.getRecvOfUser(userName)
        if recv is not None:
            fileList=recv.fileNames.copy()
            tLoc=[]
            for i in fileList:
                tLoc.append(recv.fileNames[i])
                recv.clearFileLogF(i)

            for i in tLoc:
                opFile.deletFile(i)

    def loginFromAnotherLocation(self,userName,addr):
        self.gmOnGoingOffline(userName)
        self.handleFileOnUserOffline(userName)
        addr=self.userNAddr[userName.lower()]
        send,recv=self.userAddrSR[addr]
        data=self.cRequest('45gh','loginALoc','Sequrity')
        send.send_message(data)
        send.s.close()
        self.onOfflineUser(userName,addr)
        del self.userAddrNL[addr]
        del self.userNAddr[userName.lower()]

    def handleOnFileStartRecv(self,recv,fName):
        pass

    def handleOnFileEndRecv(self,recv,fName,cond):
        if cond:
            addr=recv.argument
            if addr in self.userAddrNL:
                userName,lCond=self.userAddrNL[addr]

                if lCond:
                    toWhom=recv.fileToWhom[fName]
                    toType=recv.fileToType[fName]
                    size=recv.fileSize[fName]

                    tName=recv.fileNames[fName]
                    if toType=='chat':
                        self.handleFileOnEndForChat(toWhom,fName,tName,size)
                    elif toType=='groupChat':
                        self.handleFileOnEndForGroupChat(toWhom,fName,tName,size)
                    else:
                        print("Error File Recieving ",toType)
            else:
                print("Address Not Found Error")

    def getNewCbForDataBase(self):
        mydb=db.genMdb()
        cursor=mydb.cursor()
        cb=db.cb1(cursor,'_xprtinfo')
        return cb,cursor,mydb

    def handleFileOnEndForChat(self,toWhom,fName,tName,size):

        sender,reciever=ms.distributeString(toWhom,'-')

        fileChat=ad.assValue(['file','location','sender','recever','size']
                         ,[fName,tName,sender,reciever,str(size)],'File')
        fileChat=ds.enc(fileChat)
        cb,cursor,mydb=self.getNewCbForDataBase()
        xnot=xdb.XprtNot(cursor)
        xnot.insertChat(sender,reciever,fileChat)
        xnot.insertChat(reciever,sender,fileChat)




        self.informForFileInChat(sender,reciever,fName,xnot,mydb,size)

    def informForFileInChat(self,userName,fuserName,fileChat,xnot,mydb,size):
        condOnline=self.checkUserOnline(fuserName.lower())
        condWin=self.checkOpenWindow(userName.lower(),fuserName.lower())

        dType='_data'
        wType='_Text'
        if condOnline and condWin:
            send=self.getSendOfUser(fuserName)

            data=ad.assValue(['wType','file','code','fuserName','size'],
                             ['_Text',fileChat,'F100',userName,str(size)],dType)
            send.send_message(data)
        else:
            xnot.updateInfoCC(fuserName,userName,'False')
        mydb.commit()


    def handleFileOnEndForGroupChat(self,toWhom,fName,tName,size):
        sender,reciever=ms.distributeString(toWhom,'-')

        fileChat=ad.assValue(['file','location','sender','recever','size']
                         ,[fName,tName,sender,reciever,str(size)],'File')
        fileChat=ds.enc(fileChat)
        cb,cursor,mydb=self.getNewCbForDataBase()
        cb.insertDataN('gc_'+reciever,['1',fileChat])


        #mydb.commit()
        self.informForFileInGroupChat(sender,reciever,fName,cb,cursor,mydb,size)

    def informForFileInGroupChat(self,sender,reciever,fName,cb,cursor,mydb,size):
        xnot=xdb.XprtNot(cursor)
        gName=reciever

        members=cb.selectFieldData('g_'+reciever,'userName')

        members=ms.modifySqlResult(members)
        for i in members:
            luser=i.lower()
            if luser!=sender.lower():
                send=self.getSendOfUser(luser)
                if send is not None:

                    data=ad.assValue(['wType','code','file','size','sender','reciever'],
                                     ['sendGroupChat','kkr2',fName,str(size),sender,reciever],'GroupChat')
                    send.send_message(data)
                else:
                    xnot.updateInfoGC(i,gName,'False')

        mydb.commit()

    def cRequest(self,code,wType,dType='_Response'):
        data=ad.assValue(['wType','code'],[wType,code],dType)
        return data

    def logOut(self,info,addr):
        userName=self.getName(addr)

        #recv=self.getRecvOfUser(userName)
        #recv.saveAllAndDeleteAll()
        send=self.getSendOfUser(userName)
        send.stopAllFilesSending()

        self.gmOnGoingOffline(userName)
        self.onOfflineUser(userName,addr)
        del self.userAddrNL[addr]
        del self.userNAddr[userName.lower()]

    def initCheckVersion(self,info,addr):
        wType=info['wType']
        dType='Sequrity'

        version=info['version']


        send=self.getSendByAddr(addr)
        if version==self.clientVersion:
            data=ad.assValue(['wType','code'],[wType,'yes4'],dType)
        else:
            if float(version)<float(self.leastVersion):
                data=ad.assValue(['wType','code','link'],[wType,'ntr4',self.versionLink],dType)
            else:
                data=ad.assValue(['wType','code'],[wType,'yes5'],dType)

        if send is not None:
            send.send_message(data)

    def _login(self,info,addr):

        userName=info['userName']
        userPass=info['userPass']

        cb,cursor,mydb=self.getNewCbForDataBase()

        send=self.userAddrSR[addr][0]

        userCond=cb.checkData('sequrity','userName',userName)




        if userCond:
            #UserName not exist
            passCond=cb.checkDataCond('sequrity',['userName','userPass'],[userName.lower(),userPass])

            if passCond:
                #Correct Password
                if userName.lower() in self.userNAddr:
                    self.loginFromAnotherLocation(userName.lower(),addr)

                self.userAddrNL[addr]=[userName.lower(),True]
                self.userNAddr[userName.lower()]=addr


                data=ad.assValue(['code','wType','data','type','shape'],
                ['0000','_login',DEFAULT_IMAGE_DATA,DEFAULT_IMAGE_TYPE,DEFAULT_IMAGE_SHAPE],'_Response')
                send.send_message(data)
                self.onOnlineUser(userName.lower(),addr)
                self.userWindows[userName.lower()]={}
                self.userControls[userName.lower()]={}
                self.userDataList[userName.lower()]={}

                self.dataContainer[userName.lower()]={}
            else:
                #Incorrect Password
                data=self.cRequest('0001','_login')
                send.send_message(data)
        else:
			#User not exist
            data=self.cRequest('0002','_login')
            send.send_message(data)

    def _signUp(self,info,addr):

        name=info['name']
        userName=info['userName']
        userPass=info['userPass']
        seqQ=info['seqQ']
        seqA=info['seqA']


        cb,cursor,mydb=self.getNewCbForDataBase()
        send=self.userAddrSR[addr][0]

        userCond=cb.checkData('sequrity','userName',userName.lower())

        if userCond:
            #User Exist

            data=self.cRequest('0003','_signUp')
            send.send_message(data)

        else:
            #user not exist creating one
            xinfo=xdb.XprtInfo(cursor)

            dataSeq=[userName.lower(),seqQ,name,seqA,userPass]
            dataInfo=[userName.lower(),'True','True','True']
            #self.defaultImageLocation
            dataProfile=[userName.lower(),name,self.defaultImageLocation,\
                         'Identity of User','0','Contact No.','Email','Date of birth','Discription','0']

            dataRFController=[userName.lower(),'144','144','15','15','144','144','8192','8192','8192']

            xinfo.insertSequrity(dataSeq)
            xinfo.insertInformation(dataInfo)
            xinfo.insertProfile(dataProfile)
            xinfo.insertDataRFController(dataRFController)


            xnot=xdb.XprtNot(cursor)

            xnot.createUserGroupInfoHolder(userName)
            xnot.createBlock(userName.lower())
            xnot.createFriend(userName.lower())
            xnot.createInfoC(userName.lower())
            xnot.createInfoG(userName.lower())
            xnot.createFriendRRecv(userName.lower())
            xnot.createFriendRSent(userName.lower())
            xnot.createInfoChat(userName.lower())
            xnot.createNotification(userName.lower())

            mydb.commit()


            data=ad.assValue(['code','wType','data','type','shape'],
                ['0004','_signUp',DEFAULT_IMAGE_DATA,DEFAULT_IMAGE_TYPE,DEFAULT_IMAGE_SHAPE],'_Response')

            send.send_message(data)
            self.userWindows[userName.lower()]={}
            self.userAddrNL[addr]=[userName.lower(),True]

            self.userNAddr[userName.lower()]=addr
            self.userControls[userName.lower()]={}
            self.userDataList[userName.lower()]={}
            self.dataContainer[userName.lower()]={}

            col=cb.getColName('dataRFController')
            col=ms.modifySqlResult(col)

            data=cb.selectAllDataByCondition('dataRFController','userName',userName)
            data=ms.modifySqlResult(data)[0]

            self.prepareDataRFController(col,data)


    def _changePassword(self,info,addr):
        userName=info['userName']
        oldPassword=info['oldPassword']
        newPassword=info['newPassword']

        cb,cursor,mydb=self.getNewCbForDataBase()
        send=self.userAddrSR[addr][0]



        xinfo=xdb.XprtInfo(cursor)

        cond=cb.checkMulAndData('sequrity',['userName','userPass'],[userName.lower(),oldPassword])

        if cond:
            xinfo.updateSequrity(userName.lower(),'userPass',newPassword)
            data=self.cRequest('0005','_'+info['wType'])
            send.send_message(data)
        else:
            data=self.cRequest('0006','_'+info['wType'])
            send.send_message(data)

        mydb.commit()

    def _forgetPassword(self,info,addr):
        userName=info['userName']
        seqA=info['seqA']

        cb,cursor,mydb=self.getNewCbForDataBase()
        send=self.userAddrSR[addr][0]

        cond=cb.checkMulAndData('sequrity',['userName','seqA'],[userName,seqA])

        if cond:
            userPass=cb.selectParticularData('sequrity','userName','userPass',userName)
            userPass=ms.modifySqlResult(userPass)[0]
            data=ad.assValue(['wType','code','userPass'],['_forgetPassword','0007',userPass],'_Response')
            send.send_message(data)
        else:
            #Seq A dont exist
            data=self.cRequest('0008','_forgetPassword')
            send.send_message(data)

    def getSequrityQuestion(self,info,addr):
        userName=info['userName']

        cb,cursor,mydb=self.getNewCbForDataBase()
        send=self.userAddrSR[addr][0]


        cond=cb.checkData('sequrity','userName',userName)

        if cond:
            userPass=cb.selectParticularData('sequrity','userName','seqQ',userName)
            userPass=ms.modifySqlResult(userPass)[0]
            data=ad.assValue(['wType','code','seqQ'],['getSequrityQuestion','45t6',userPass],'_Response')
            send.send_message(data)
        else:
            data=self.cRequest('4567','getSequrityQuestion')
            send.send_message(data)

    #------------------------------------------------------
    def updateHideProfile(self,info,addr):
        cb,cursor,mydb=self.getNewCbForDataBase()
        send=self.userAddrSR[addr][0]
        userName,login=self.userAddrNL[addr]
        xinfo=xdb.XprtInfo(cursor)
        ofType='hideProfile'
        ofTypeVal=info['value']
        if login:
            xinfo.updateProfile(userName,ofType,ofTypeVal)
            data=self.cRequest('0078','_editProfile')
            send.send_message(data)
            mydb.commit()
        else:
            #print("Login First")
            data=self.cRequest('1111','_editProfile')
            send.send_message(data)

    def _editProfile(self,info,addr):
        ofType=info['ofType']
        ofTypeVal=info['ofTypeVal']

        cb,cursor,mydb=self.getNewCbForDataBase()
        send=self.userAddrSR[addr][0]


        userName,login=self.userAddrNL[addr]

        xinfo=xdb.XprtInfo(cursor)
        if login:

            if ofType=='name':

                xinfo.updateSequrity(userName,ofType,ofTypeVal)
                xinfo.updateProfile(userName,ofType,ofTypeVal)
                mydb.commit()
            elif ofType=='locProfilePic':
                data=ds.reFormatImageData(info['profileData'])
                data=ds.remodifyData(data,info['profileType']\
                                    ,info['profileShape'],True)


                loc=location+'user@'+userName+'\\Profile\\profilePic.jpg'
                cv2.imwrite(loc,data)
                loc=ds.enc(loc)
                xinfo.updateProfile(userName,ofType,loc)
            elif ofType=='identityU':
                xinfo.updateProfile(userName,ofType,ofTypeVal)
            elif ofType=='gender':
                xinfo.updateProfile(userName,ofType,ofTypeVal)
            elif ofType=='contactNo':
                xinfo.updateProfile(userName,ofType,ofTypeVal)
            elif ofType=='email':
                xinfo.updateProfile(userName,ofType,ofTypeVal)
            elif ofType=='dateOfBirth':
                xinfo.updateProfile(userName,ofType,ofTypeVal)
            elif ofType=='discription':
                xinfo.updateProfile(userName,ofType,ofTypeVal)
            else:
                print(ofType+" option is not avalable in edit profile")
            mydb.commit()
            data=self.cRequest('0009','_editProfile')
            send.send_message(data)
        else:
            #print("Login First")
            data=self.cRequest('1111','_editProfile')
            send.send_message(data)

    def _changeSeqQA(self,info,addr):
        seqQ=info['seqQ']
        seqA=info['seqA']
        userPass=info['userPass']

        cb,cursor,mydb=self.getNewCbForDataBase()
        send=self.userAddrSR[addr][0]


        userName,login=self.userAddrNL[addr]

        xinfo=xdb.XprtInfo(cursor)

        if login:
            passCond=cb.checkMulAndData('sequrity',['userName','userPass'],[userName,userPass])
            if passCond:
                xinfo.updateSequrity(userName,'seqQ',seqQ)
                xinfo.updateSequrity(userName,'seqA',seqA)

                data=self.cRequest('0011','_changeSeqQA')
                send.send_message(data)
            else:
                data=self.cRequest('0010','_changeSeqQA')
                send.send_message(data)
        else:

            data=self.cRequest('1111','_changeSeqQA')
            send.send_message(data)

    def refressSearch(self,info,addr):
        dType='_Response'
        wType=info['wType']

        cb,cursor,mydb=self.getNewCbForDataBase()
        send=self.userAddrSR[addr][0]

        userName,login=self.userAddrNL[addr]


        xinfo=xdb.XprtInfo(cursor)
        if login:
            data=cb.selectRandomData('profile','userName',50)
            data=ms.modifySqlResult(data)

            if data is not None:
                rdata=[]

                for i in data:
                    t1='b_'+i
                    t2='b_'+userName
                    t3='f_'+userName

                    if i.lower() !=userName:
                        cond=cb.checkData(t1,'userName',userName)
                        cond2=cb.checkData(t2,'userName',i)
                        cond3=cb.checkData(t3,'userName',i)

                        if not cond and not cond2 and not cond3:
                            rdata.append(i)

                usrData=[]
                for user in rdata:
                    d=xinfo.getSomeProfile(user)[0]
                    d=list(d)
                    if d[2]=='_None':
                        imgD=['_None','_None','_None']
                    else:
                        d[2]=ds.dec(d[2])
                        d[2]=cv2.imread(d[2])
                        imgD=ds.prepareImageFormat(d[2])
                    d=d[:2]

                    usrData.append(d+imgD)

                if len(usrData)>0:
                    uD=ds.prepSend(usrData)

                    data=ad.assValue(['wType','code','usersData','usersType','usersShape'],
                                     [wType,'0014',uD[0],uD[1],uD[2]],dType)
                    send.send_message(data)

        else:
            data=self.cRequest('1111',wType)
            send.send_message(data)

    def _searchFriend(self,info,addr):

        wType='_searchFriend'
        searchUserName=info['userName']
        cb,cursor,mydb=self.getNewCbForDataBase()
        send=self.userAddrSR[addr][0]


        userName,login=self.userAddrNL[addr]

        data=cb.selectByMulOrCondNot('sequrity',['userName','name'],[searchUserName,searchUserName],['userName'],[userName],'userName')
        data=ms.modifySqlResult(data)
        xnot=xdb.XprtNot(cursor)
        xinfo=xdb.XprtInfo(cursor)
        if login:
            if info['hs']=='1':
                if data is None:
                    data=self.cRequest('0012',wType)
                    send.send_message(data)
                else:
                    correctUser=[]
                    for user in data:
                        cond1=xnot.checkBlock(userName,user)
                        cond2=xnot.checkBlock(user,userName)
                        if (not cond1) and(not cond2):
                            correctUser.append(user)


                    usrData=[]
                    for user in correctUser:

                        if user==userName:
                            continue
                        d=xinfo.getSomeProfile(user)[0]
                        d=list(d)
                        if d[2]=='_None':
                            imgD=['_None','_None','_None']
                        else:
                            d[2]=ds.dec(d[2])
                            d[2]=cv2.imread(d[2])
                            imgD=ds.prepareImageFormat(d[2])
                        d=d[:2]

                        usrData.append(d+imgD)

                    if len(usrData)==0:
                        data=self.cRequest('0013',wType)
                        send.send_message(data)
                    else:
                        uD=ds.prepSend(usrData)

                        data=ad.assValue(['wType','code','usersData','usersType','usersShape'],
                                         [wType,'0014',uD[0],uD[1],uD[2]],'_Response')
                        send.send_message(data)
            else:
                cm=f'%{searchUserName}%'
                data=cb.selectRandomWithLike('sequrity','userName',cm,'userName',30)
                data2=cb.selectRandomWithLike('sequrity','name',cm,'userName',30)

                data =ms.modifySqlResult(data)
                data2=ms.modifySqlResult(data2)

                rdata=[]
                if data is not None:
                    rdata=data

                if data2 is not None:
                    rdata=rdata+data2

                ddata=ae.remDubFromArray(rdata)

                newData=[]

                for i in ddata:
                    t1='b_'+i
                    t2='b_'+userName


                    if i.lower() !=userName:
                        cond=cb.checkData(t1,'userName',userName)
                        cond2=cb.checkData(t2,'userName',i)
                        #cond3=cb.checkData(t3,'userName',i)

                        if not cond and not cond2 :
                            newData.append(i)

                usrData=[]
                for user in newData:
                    d=xinfo.getSomeProfile(user)[0]
                    d=list(d)
                    if d[2]=='_None':
                        imgD=['_None','_None','_None']
                    else:
                        d[2]=ds.dec(d[2])
                        d[2]=cv2.imread(d[2])
                        imgD=ds.prepareImageFormat(d[2])

                    d=d[:2]

                    usrData.append(d+imgD)

                if len(usrData)>0:
                    uD=ds.prepSend(usrData)

                    data=ad.assValue(['wType','code','usersData','usersType','usersShape'],
                                     [wType,'0014',uD[0],uD[1],uD[2]],'_Response')

                else:
                    data=self.cRequest('0013',wType,'_Response')

                send.send_message(data)

        else:
            data=self.cRequest('1111',wType)
            send.send_message(data)

    def _sendFriendRequest(self,info,addr):

        wType='_sendFriendRequest'
        fuserName=info['userName']
        cb,cursor,mydb=self.getNewCbForDataBase()
        send=self.userAddrSR[addr][0]


        userName,login=self.userAddrNL[addr]
        xnot=xdb.XprtNot(cursor)
        if login:
            cond=cb.checkDataCond('fs_'+userName,['userName'],[fuserName])
            if cond:
                data=self.cRequest('0014',wType)
                send.send_message(data)
            else:
                cond=cb.checkDataCond('f_'+userName,['userName'],[fuserName])
                if cond:
                    data=self.cRequest('0015',wType)
                    send.send_message(data)
                else:
                    xnot.insertFriendRRecv(fuserName,userName)
                    xnot.insertFriendRSent(userName,fuserName)
                    xnot.insertNotification(fuserName,userName+' sent your friend request')
                    mydb.commit()
                    data=self.cRequest('0016',wType)
                    send.send_message(data)
        else:
            data=self.cRequest('1111',wType)
            send.send_message(data)

    def _unfriend(self,info,addr):
        wType='_unfriend'
        fuserName=info['userName']
        cb,cursor,mydb=self.getNewCbForDataBase()

        send=self.userAddrSR[addr][0]


        userName,login=self.userAddrNL[addr]
        xnot=xdb.XprtNot(cursor)

        if login:
            xnot.deleteFriend(userName,fuserName)
            xnot.deleteFriend(fuserName,userName)

            data=self.cRequest('0017',wType)
            send.send_message(data)

        else:
            data=self.cRequest('1111',wType)
            send.send_message(data)

    def _deleteFriendRequest(self,info,addr):

        wType='_deleteFriendRequest'
        fuserName=info['userName']
        cb,cursor,mydb=self.getNewCbForDataBase()
        send=self.userAddrSR[addr][0]
        cb=db.cb1(cursor,'_xprtinfo')

        userName,login=self.userAddrNL[addr]
        xnot=xdb.XprtNot(cursor)

        if login:
            xnot.deleteFriendRSent(fuserName,userName)
            xnot.deleteFriendRRecv(userName,fuserName)

            data=self.cRequest('0018',wType)
            send.send_message(data)

        else:
            data=self.cRequest('1111',wType)
            send.send_message(data)

    def _blockSearch(self,info,addr):

        wType='_blockSearch'
        searchUserName=info['userName']
        cb,cursor,mydb=self.getNewCbForDataBase()
        send=self.userAddrSR[addr][0]


        userName,login=self.userAddrNL[addr]

        data=cb.selectByMulOrCondNot('sequrity',['userName','name'],[searchUserName,searchUserName],['userName'],[userName],'userName')
        data=ms.modifySqlResult(data)
        xnot=xdb.XprtNot(cursor)
        xinfo=xdb.XprtInfo(cursor)
        if login:
            if data is None:
                data=self.cRequest('0019',wType)
                send.send_message(data)
            else:
                correctUser=[]
                for user in data:
                    cond1=xnot.checkBlock(userName,user)
                    cond2=xnot.checkBlock(user,userName)
                    if (not cond1) and(not cond2):
                        correctUser.append(user)


                usrData=[]
                for user in correctUser:
                    d=xinfo.getSomeProfile(user)[0]

                    d=list(d)
                    if d[2]=='_None':
                        imgD=['_None','_None','_None']
                    else:
                        d[2]=ds.dec(d[2])

                        d[2]=cv2.imread(d[2])
                        imgD=ds.prepareImageFormat(d[2])
                        print(imgD)

                    d=d[:2]
                    usrData.append(d+imgD)

                if len(usrData)==0:
                    data=self.cRequest('0013',wType)
                    send.send_message(data)
                else:

                    uD=ds.prepSend(usrData)

                    data=ad.assValue(['wType','code','usersData','usersType','usersShape'],[wType,'0020',uD[0],uD[1],uD[2]],'_Response')
                    send.send_message(data)
        else:
            data=self.cRequest('1111',wType)
            send.send_message(data)

    def _block(self,info,addr):
        wType='_block'
        fuserName=info['userName']
        cb,cursor,mydb=self.getNewCbForDataBase()
        send=self.userAddrSR[addr][0]


        userName,login=self.userAddrNL[addr]
        xnot=xdb.XprtNot(cursor)

        if login:
            xnot.deleteFriend(userName,fuserName)
            xnot.deleteFriend(fuserName,userName)

            xnot.deleteFriendRRecv(userName,fuserName)
            xnot.deleteFriendRRecv(fuserName,userName)

            xnot.deleteFriendRSent(userName,fuserName)
            xnot.deleteFriendRSent(userName,fuserName)

            xnot.deleteInfoC(userName,fuserName)
            xnot.deleteInfoC(fuserName,userName)

            xnot.insertBlock(userName,fuserName)

            xnot.deleteInfoC(userName,fuserName)

            data=self.cRequest('0021',wType)
            send.send_message(data)
            mydb.commit()

        else:
            data=self.cRequest('1111',wType)
            send.send_message(data)

    def _unblockLoad(self,info,addr):
        wType='_unblockLoad'

        cb,cursor,mydb=self.getNewCbForDataBase()
        send=self.userAddrSR[addr][0]


        userName,login=self.userAddrNL[addr]
        xinfo=xdb.XprtInfo(cursor)

        if login:

            data=cb.selectFieldData('b_'+userName,'userName')
            data=ms.modifySqlResult(data)
            usrData=[]
            if data is not None:

                for user in data:
                    d=xinfo.getSomeProfile(user)[0]

                    d=list(d)
                    if d[2]=='_None':
                        imgD=['_None','_None','_None']
                    else:
                        d[2]=ds.dec(d[2])

                        d[2]=cv2.imread(d[2])
                        imgD=ds.prepareImageFormat(d[2])
                    d=d[:2]
                    usrData.append(d+imgD)

            if len(usrData)==0:
                data=self.cRequest('0022',wType)
                send.send_message(data)
            else:
                uD=ds.prepSend(usrData)
                data=ad.assValue(['wType','code','usersData','usersType','usersShape'],[wType,'0023',uD[0],uD[1],uD[2]],'_Response')
                send.send_message(data)
        else:
            data=self.cRequest('1111',wType)
            send.send_message(data)

    def _unblock(self,info,addr):

        wType='_unblock'
        fuserName=info['userName']
        cb,cursor,mydb=self.getNewCbForDataBase()
        send=self.userAddrSR[addr][0]


        userName,login=self.userAddrNL[addr]
        xnot=xdb.XprtNot(cursor)

        if login:
            xnot.deleteBlock(userName,fuserName)

            data=self.cRequest('0024',wType)
            send.send_message(data)
            mydb.commit()

        else:
            data=self.cRequest('1111',wType)
            send.send_message(data)

    def _friendRequestAccept(self,info,addr):

        wType='_friendRequestAccept'
        fuserName=info['userName']
        cb,cursor,mydb=self.getNewCbForDataBase()
        send=self.userAddrSR[addr][0]


        userName,login=self.userAddrNL[addr]
        xnot=xdb.XprtNot(cursor)

        if login:
            xnot.deleteFriendRSent(userName,fuserName)
            xnot.deleteFriendRSent(fuserName,userName)
            xnot.deleteFriendRRecv(userName,fuserName)
            xnot.deleteFriendRRecv(fuserName,userName)

            xnot.insertFriend(fuserName,userName)
            xnot.insertFriend(userName,fuserName)

            xnot.createChat(fuserName,userName)
            xnot.createChat(userName,fuserName)

            xnot.insertNotification(fuserName,f'{userName} accepted your friend request.')

            xnot.insertInfoC(userName,fuserName)
            xnot.insertInfoC(fuserName,userName)

            data=self.cRequest('0027',wType)
            send.send_message(data)

        else:
            data=self.cRequest('1111',wType)
            send.send_message(data)
        mydb.commit()

    def _loadUserProfile(self,info,addr):

        dType='_Response'
        wType='_loadUserProfile'
        fuserName=info['userName']

        whoRequested=info['whoRequested']


        cb,cursor,mydb=self.getNewCbForDataBase()
        send=self.userAddrSR[addr][0]


        userName,login=self.userAddrNL[addr]
        xinfo=xdb.XprtInfo(cursor)

        if login:

            data=xinfo.selectProfile(fuserName)
            data=ms.modifySqlResult(data)[0]

            data=list(data)

            imgLoc=data[2]
            if imgLoc=='_None':
                imgD=['_None','_None','_None']
            else:
                imgLoc=ds.dec(imgLoc)
                d=cv2.imread(imgLoc)
                imgD=ds.prepareImageFormat(d)

            cond=cb.checkMulAndData('profile',['userName','hideProfile'],[fuserName,'1'])


            if userName.lower()==fuserName.lower() :
                tf=data[:2]+imgD+data[3:]
                data=ad.assValue(['wType','code','userName','name','profileData',\
                              'profileType','profileShape','identityU','gender','contactNo',\
                              'email','dateOfBirth','discription','hideProfile','whoRequested'],
                                 [wType,'0028']+tf+[whoRequested],dType)
            else:
                if cond:
                    tf=data[:2]+imgD
                    data=ad.assValue(['wType','code','userName','name','profileData',\
                                  'profileType','profileShape','whoRequested'],
                                     [wType,'0029']+tf+[whoRequested],dType)
                else:
                    tf=data[:2]+imgD+data[3:]
                    data=ad.assValue(['wType','code','userName','name','profileData',\
                              'profileType','profileShape','identityU','gender','contactNo',\
                              'email','dateOfBirth','discription','hideProfile','whoRequested'],
                                 [wType,'0028']+tf+[whoRequested],dType)
            send.send_message(data)


        else:
            data=self.cRequest('1111',wType)
            send.send_message(data)

    def _friendListLoad(self,info,addr):


        dType='_Response'
        wType='_friendListLoad'
        whoRequested=info['whoRequested']
        cb,cursor,mydb=self.getNewCbForDataBase()
        send=self.userAddrSR[addr][0]


        userName,login=self.userAddrNL[addr]
        xinfo=xdb.XprtInfo(cursor)

        if login:


                friends=cb.selectFieldData('f_'+userName,'userName')
                friends=ms.modifySqlResult(friends)
                if friends is not None:
                    usrData=[]
                    for i in friends:
                        d=xinfo.getSomeProfile(i)[0]
                        d=list(d)
                        cond=self.checkUserOnline(i)
                        #print(i,cond)
                        if d[2]=='_None':
                            imgD=['_None','_None','_None']
                        else:
                            d[2]=ds.dec(d[2])

                            d[2]=cv2.imread(d[2])
                            imgD=ds.prepareImageFormat(d[2])
                        d=d[:2]

                        usrData.append(d+imgD+[str(cond)])
                        #usrData.append(str(cond))

                    ads=ds.prepSend(usrData)

                    data=ad.assValue(['wType','code','whoRequested','friendData','friendType','friendShape']\
                                     ,[wType,'f028',whoRequested,ads[0],ads[1],ads[2]],dType)

                    send.send_message(data)
                    print(len(data), ' is amount of data')
                else:
                    #No friend exist

                    data=self.cRequest('f102',wType)
                    #print(data)
                    send.send_message(data)

        else:
            data=self.cRequest('1111',wType)
            send.send_message(data)
    #---------------------------------------------------

    def _loadMainWindow(self,info,addr):
        status=info['status']

        dType='_Response'
        wType='_loadMainWindow'
        cb,cursor,mydb=self.getNewCbForDataBase()
        send=self.userAddrSR[addr][0]


        userName,login=self.userAddrNL[addr]
        xinfo=xdb.XprtInfo(cursor)

        if login:

            if status=='load':

                #data=self.cRequest('L101',wType)
                #send.send_message(data)
                pass
            else:
                data=self.cRequest('L102',wType)
                send.send_message(data)
        else:
            data=self.cRequest('1111',wType)
            send.send_message(data)


    def _loadEditProfile(self,info,addr):
        status=info['status']

        dType='_Response'
        wType='_loadEditProfile'
        cb,cursor,mydb=self.getNewCbForDataBase()
        send=self.userAddrSR[addr][0]


        userName,login=self.userAddrNL[addr]
        xinfo=xdb.XprtInfo(cursor)

        if login:

            if status=='load':
                data=self.cRequest('L101',wType)
                send.send_message(data)
            else:
                data=self.cRequest('L102',wType)
                send.send_message(data)
        else:
            data=self.cRequest('1111',wType)
            send.send_message(data)

    def _loadFriendControl(self,info,addr):
        status=info['status']

        dType='_Response'
        wType='_loadFriendControl'
        cb,cursor,mydb=self.getNewCbForDataBase()
        send=self.userAddrSR[addr][0]


        userName,login=self.userAddrNL[addr]
        xinfo=xdb.XprtInfo(cursor)

        if login:

            if status=='load':
                data=self.cRequest('L101',wType)
                send.send_message(data)
            else:
                data=self.cRequest('L102',wType)
                send.send_message(data)
        else:
            data=self.cRequest('1111',wType)
            send.send_message(data)

    def _loadChatWindow(self,info,addr):
        status=info['status']
        cuserName=info['userName']


        dType='_Response'
        wType='_loadChatWindow'
        cb,cursor,mydb=self.getNewCbForDataBase()



        userName,login=self.userAddrNL[addr]
        xnot=xdb.XprtNot(cursor)
        send=self.getSendOfUser(userName)
        if login:
            if status=='load':
                dicts={'sScreen':0,'sCamera':0,'sSound':0,'sIntSound':0,'sKeyboard':0,'sMouse':0,\
                       'rScreen':0,'rCamera':0,'rSound':0,'rIntSound':0,'rKeyboard':0,'rMouse':0}

                self.userControls[userName.lower()][cuserName.lower()]=dicts
                self.userWindows[userName.lower()][cuserName.lower()]=True
                xnot.updateInfoCC(userName,cuserName,'True')
                #dics=['sScreen','sCamera','sSound','sInternalSound','sKeyboard','sMouse']
                for i in dicts:
                    self.userDataList[userName.lower()][i]={}


                for i in dicts:
                    self.userDataList[userName.lower()][i][cuserName.lower()]=0

            else:
                self.userWindows[userName.lower()][cuserName.lower()]=False
                del self.userControls[userName.lower()][cuserName.lower()]


        else:
            data=self.cRequest('1111',wType)
            send.send_message(data)

    def _loadSearchFriend(self,info,addr):
        status=info['status']

        dType='_Response'
        wType='_loadSearchFriend'
        cb,cursor,mydb=self.getNewCbForDataBase()
        send=self.userAddrSR[addr][0]


        userName,login=self.userAddrNL[addr]
        xinfo=xdb.XprtInfo(cursor)

        if login:

            if status=='load':
                data=self.cRequest('L101',wType)
                send.send_message(data)
            else:
                data=self.cRequest('L102',wType)
                send.send_message(data)
        else:
            data=self.cRequest('1111',wType)
            send.send_message(data)

    def _loadBlockUnblock(self,info,addr):
        status=info['status']

        dType='_Response'
        wType='_loadBlockUnblock'
        cb,cursor,mydb=self.getNewCbForDataBase()
        send=self.userAddrSR[addr][0]


        userName,login=self.userAddrNL[addr]
        xinfo=xdb.XprtInfo(cursor)

        if login:

            if status=='load':
                data=self.cRequest('L101',wType)
                send.send_message(data)
            else:
                data=self.cRequest('L102',wType)
                send.send_message(data)
        else:
            data=self.cRequest('1111',wType)
            send.send_message(data)

    def _loadFriendRequest(self,info,addr):
        status=info['status']

        dType='_Response'
        wType='_loadFriendRequest'
        cb,cursor,mydb=self.getNewCbForDataBase()
        send=self.userAddrSR[addr][0]


        userName,login=self.userAddrNL[addr]
        xinfo=xdb.XprtInfo(cursor)


        if login:


            notif=cb.selectFieldData('fr_'+userName.lower(),'userName')
            #print(notif)
            notif=ms.modifySqlResult(notif)
            #print(notif)
            cb.updateParticularData('Information','userName','friendRequest'
                                     ,userName,'True')
            if notif is None or len(notif)==0:
                data=self.cRequest('ss01',wType)
            else:
                usrData=[]
                for i in notif:
                    d=xinfo.getSomeProfile(i)[0]
                    d=list(d)
                    
                    if d[2]=='_None':
                        imgD=['_None','_None','_None']
                    else:
                        d[2]=ds.dec(d[2])

                        d[2]=cv2.imread(d[2])
                        imgD=ds.prepareImageFormat(d[2])

                    d=d[:2]

                    usrData.append(d+imgD)
                
                uD=ds.prepSend(usrData)
                data=ad.assValue(['wType','code','usersData','usersType','usersShape'],[wType,'kks1',uD[0],uD[1],uD[2]],'_Response')

            xinfo.updateInformation(userName,'friendRequest','True')

            mydb.commit()


            send.send_message(data)
        else:
            data=self.cRequest('1111',wType)
            send.send_message(data)

    def _loadNotification(self,info,addr):
        status=info['status']

        r1=int(info['r1'])
        r2=int(info['r2'])


        dType='_Response'
        wType='_loadNotification'
        cb,cursor,mydb=self.getNewCbForDataBase()
        send=self.userAddrSR[addr][0]


        userName,login=self.userAddrNL[addr]
        xinfo=xdb.XprtInfo(cursor)

        if login:
            tVal=cb.countValues('N_'+userName)
            #diff=abs(r1-r2)+1

            s1=tVal-r1+1
            s2=tVal-r2+1
            notif=cb.selectRangeData('N_'+userName,'sno',s2,s1,'*')
            #print(notif)
            notif=ms.modifySqlResult(notif)
            cb.updateParticularData('Information','userName','notification'
                                     ,userName,'True')
            mydb.commit()
            #print(notif)
            if notif is None or len(notif)==0:
                data=self.cRequest('kk01',wType)
            else:
                data=ds.prepSend(notif)

                if r1==0 or r1==1:

                    data=ad.assValue(['wType','code','notifData','notifType','notifShape','tfm']\
                                     ,[wType,'001k',data[0],data[1],data[2],'True'],dType)
                else:
                    data=ad.assValue(['wType','code','notifData','notifType','notifShape','tfm']\
                                     ,[wType,'001k',data[0],data[1],data[2],'False'],dType)
            send.send_message(data)
        else:
            data=self.cRequest('1111',wType)
            send.send_message(data)

    def _loadFindFriends(self,info,addr):
        status=info['status']

        dType='_Response'
        wType='_loadFindFriends'
        cb,cursor,mydb=self.getNewCbForDataBase()
        send=self.userAddrSR[addr][0]


        userName,login=self.userAddrNL[addr]
        xinfo=xdb.XprtInfo(cursor)

        if login:

            if status=='load':
                data=self.cRequest('L101',wType)
                send.send_message(data)
            else:
                data=self.cRequest('L102',wType)
                send.send_message(data)
        else:
            data=self.cRequest('1111',wType)
            send.send_message(data)

    def _loadSystemSetting(self,info,addr):
        status=info['status']

        dType='_Response'
        wType='_loadSystemSetting'
        cb,cursor,mydb=self.getNewCbForDataBase()
        send=self.userAddrSR[addr][0]


        userName,login=self.userAddrNL[addr]
        xinfo=xdb.XprtInfo(cursor)

        if login:

            if status=='load':
                data=self.cRequest('L101',wType)
                send.send_message(data)
            else:
                data=self.cRequest('L102',wType)
                send.send_message(data)
        else:
            data=self.cRequest('1111',wType)
            send.send_message(data)

    #--------------------------------------------

    def checkOpenWindow(self,userName,fuserName):
        onlineCond=self.checkUserOnline(fuserName.lower())

        if onlineCond:
            if fuserName.lower() in self.userWindows:
                wList=self.userWindows[fuserName.lower()]
                winName=userName.lower()
                if winName in wList:
                    return True
                else:

                    return False
            else:
                return False
        else:
            return False

    def checkUserControl(self,userName,fuserName,types):
        if userName.lower() in self.userControls:
            x= self.userControls[userName.lower()]
            #print(x)
            if fuserName.lower() in x:
                y=x[fuserName.lower()]
                #print(y)

                return y[types]
            else:
                return False
        else:
            return False

    def checkUserOnline(self,userName):
        if userName.lower() in self.userNAddr:
            return True
        else:
            return False

    def getAddress(self,userName):
        cond=self.checkUserOnline(userName.lower())

        if cond:
            return self.userNAddr[userName.lower()]
        else:
            return None

    def checkAddrOnline(self,addr):
        if addr in self.userAddrNL:
            return True
        else:
            return False


    def getName(self,addr):
        cond=self.checkAddrOnline(addr)
        if cond:
            return self.userAddrNL[addr][0]
        else:
            return None

#------------------------------------------------------------------------------
#   I Love You
#------------------------------------------------------------------------------

    def _Text(self,info,addr):
        dType='_data'
        wType='_Text'

        chatText=info['chatText']

        fuserName=info['userName']
        cb,cursor,mydb=self.getNewCbForDataBase()
        send=self.userAddrSR[addr][0]


        userName,login=self.userAddrNL[addr]
        xnot=xdb.XprtNot(cursor)

        if login:
            chatText=ds.enc(chatText)
            chat=ad.assValue(['chat','sender','recever'],[chatText,userName.lower(),fuserName.lower()],'Chat')
            chat=ds.enc(chat)
            xnot.insertChat(userName.lower(),fuserName.lower(),chat)
            xnot.insertChat(fuserName.lower(),userName.lower(),chat)

            condOnline=self.checkUserOnline(fuserName.lower())
            condWin=self.checkOpenWindow(userName.lower(),fuserName.lower())


            if condOnline and condWin:
                addr1=self.userNAddr[fuserName.lower()]
                send=self.userAddrSR[addr1][0]

                data=ad.assValue(['wType','chatText','code','fuserName'],[wType,chat,'L100',userName],dType)
                send.send_message(data)
            elif condOnline:
                pass
            else:
                xnot.updateInfoCC(fuserName,userName,'False')
            mydb.commit()

        else:
            data=self.cRequest('L103',wType,dType)
            send.send_message(data)


    def _loadChat(self,info,addr):


        r1=int(info['r1'])
        r2=int(info['r2'])


        dType='_data'
        wType='_loadChat'
        cb,cursor,mydb=self.getNewCbForDataBase()
        send=self.userAddrSR[addr][0]


        userName,login=self.userAddrNL[addr]
        xnot=xdb.XprtNot(cursor)

        fuserName=info['fuserName']

        if login:
            tName='C_'+userName+'_'+fuserName
            tVal=cb.countValues(tName)
            #diff=abs(r1-r2)+1

            s1=tVal-r1+1
            s2=tVal-r2+1
            notif=cb.selectRangeData(tName,'sno',s2,s1,'*')
            #print(notif)
            notif=ms.modifySqlResult(notif)
            #print(notif)
            xnot.updateInfoCC(userName,fuserName,'True')
            mydb.commit()
            if notif is None or len(notif)==0:
                #data=self.cRequest('se01',wType,dType)
                data=ad.assValue(['code','wType','fuserName'],['se01',wType,fuserName],dType)

            else:
                data=ds.prepSend(notif)

                if r1==0 or r1==1:

                    data=ad.assValue(['wType','code','loadChat','chatType','chatShape','tfm','fuserName']\
                                     ,[wType,'00sk',data[0],data[1],data[2],'True',fuserName.lower()],dType)
                else:
                    data=ad.assValue(['wType','code','loadChat','chatType','chatShape','tfm','fuserName']\
                                     ,[wType,'00sk',data[0],data[1],data[2],'False',fuserName.lower()],dType)

            send.send_message(data)
        else:
            data=ad.assValue(['code','wType','fuserName'],['1111',wType,fuserName.lower()],dType)
            send.send_message(data)


    def _File(self,info,addr):
        dType='_data'
        wType='_File'

        chatText=info['chatFile']

        fuserName=info['userName']
        cb,cursor,mydb=self.getNewCbForDataBase()
        send=self.userAddrSR[addr][0]


        userName,login=self.userAddrNL[addr]
        xnot=xdb.XprtNot(cursor)

        if login:
            chatText=ds.enc(chatText)
            chat=ad.assValue(['name','sender','recever'],[chatText,userName.lower(),fuserName.lower()],'File')

            xnot.insertChat(userName.lower(),fuserName.lower(),chat)
            xnot.insertChat(fuserName.lower(),userName.lower(),chat)

            condOnline=self.checkUserOnline(fuserName.lower())
            condWin=self.checkOpenWindow(userName.lower(),fuserName.lower())

            mydb.commit()
            if condOnline and condWin:
                addr1=self.userNAddr[fuserName.lower()]
                send=self.userAddrSR[addr1][0]
                chat=ds.enc(chat)
                data=ad.assValue(['wType','chatFile','code','fuserName'],[wType,chat,'L140',userName],dType)
                send.send_message(data)

        else:
            data=self.cRequest('L193',wType,dType)
            send.send_message(data)


    def cancelDownloadFile(self,info,addr):
        dType='_data'
        wType='CancelDownloadFile'

        fileName=info['fName']

        fuserName=info['userName']
        cb,cursor,mydb=self.getNewCbForDataBase()

        userName,login=self.userAddrNL[addr]
        xnot=xdb.XprtNot(cursor)
        recv=self.getRecvOfUser(userName)
        send=self.getSendOfUser(userName)


        if login:
            if fileName in send.fileFlow:
                send.fileFlow[fileName]=False

                data=ad.assValue(['wType','code','fuserName','fileName','cf'],
                                 [wType,'tt56',fuserName,fileName,info['cf']],dType)
                send.send_message(data)
            else:
                data=ad.assValue(['wType','code','fuserName','fileName','cf'],
                                 [wType,'45GH',fuserName,fileName,info['cf']],dType)
                send.send_message(data)



        else:
            data=self.cRequest('F103',wType,dType)
            send.send_message(data)

    def DownloadFile(self,info,addr):
        dType='_data'
        wType='DownloadFile'

        fileName=info['fName']

        fuserName=info['userName']
        cb,cursor,mydb=self.getNewCbForDataBase()

        userName,login=self.userAddrNL[addr]
        xnot=xdb.XprtNot(cursor)
        recv=self.getRecvOfUser(userName)
        send=self.getSendOfUser(userName)
        loc=recv.location+fileName

        if login:
            try:
                print(loc)

                open(loc)


                def fun():
                    data=ad.assValue(['wType','code','status','fileName','fuserName','cf'],
                                     [wType,'c12c','True',fileName,fuserName,info['cf']],dType)
                    send.send_message(data)
                namesToTo=fuserName+'-'+userName

                send.send_file3(loc,fileTempName=fileName,onStart=fun,toWhom=namesToTo,toType='Chat')

            except:

                data=ad.assValue(['wType','code','fuserName','fileName','cf'],
                                 [wType,'FEE4',fuserName,fileName,info['cf']],dType)
                send.send_message(data)
        else:
            data=self.cRequest('F103',wType,dType)
            send.send_message(data)

    def updateControls(self,info,addr):

        dType='_data'
        wType='_updateControls'


        send=self.userAddrSR[addr][0]



        userName,login=self.userAddrNL[addr]


        if login:
            types=info['conType']
            value=int(info['conValue'])
            fuserName=info['userName']
            if fuserName=='@none':
                pass
            else:
                #print(fuserName,types,value)

                if fuserName.lower() in self.userControls[userName.lower()]:
                    self.userControls[userName.lower()][fuserName.lower()][types]=value

                if value==0:

                    self.formatList(userName.lower(),fuserName.lower(),types,False)
                else:
                    self.formatList(userName.lower(),fuserName.lower(),types,True)


                #data=self.cRequest('1rt1',wType,dType)
                #send.send_message(data)

            #else:
                #data=self.cRequest('1111',wType,dType)
                #send.send_message(data)

    def checkControls(self,userName,fuserName,types):
        if userName.lower() in self.userControls:
            d=self.userControls[userName.lower()]
            if fuserName.lower() in d:
                s=d[fuserName.lower()]

                if types in s:
                    return s[types]
                else:
                    print("Types Error")
                    return 0
            else:
                print("F user Name error")
                return 0
        else:
            print("User Name error")
            return 0

    def _Screen(self,info,addr):
        dType='_data'
        wType='_Screen'
        fType='sScreen'
        rType='rScreen'
        data=info['data']

        fuserName=info['userName']


        send=self.userAddrSR[addr][0]


        userName,login=self.userAddrNL[addr]
        if fuserName=='@none':
            userList=self.userDataList[userName.lower()][fType]
        else:

            self.formatList(userName.lower(),fuserName.lower(),fType,True)
            userList=self.userDataList[userName.lower()][fType]

        if data!='@none':
            types=info['types']
            shape=info['shape']
            self.dataContainer[userName.lower()][wType]=[data,types,shape]
        #print("I AM SOUND RECIEVER")

        if login:

            for i in userList:
                cond=userList[i]
                if cond:
                    onlineCond=self.checkUserOnline(i)
                    openWindow=self.checkOpenWindow(userName.lower(),i)

                    if onlineCond and openWindow:
                        cond2=self.checkUserControl(i.lower(),userName.lower(),rType)

                        if cond2:
                            #print("HE IS RECIEVING")
                            addr1=self.userNAddr[i.lower()]
                            hsend=self.userAddrSR[addr1][0]
                            if data!='@none':
                                data=self.dataContainer[userName.lower()][wType]
                                data=self.reFormatResolution(data,i,'rScreenRes')
                                types=data[1]
                                shape=data[2]
                                data=data[0]
                                data=ad.assValue(['wType','code','data','types','shape','userName'],[wType,'d201',data,types,shape,userName.lower()],dType)

                                hsend.send_message(data)



        else:
            data=self.cRequest('L103',wType,dType)
            send.send_message(data)

    def _Camera(self,info,addr):
        dType='_data'
        wType='_Camera'
        fType='sCamera'
        rType='rCamera'
        data=info['data']

        fuserName=info['userName']


        send=self.userAddrSR[addr][0]


        userName,login=self.userAddrNL[addr]
        if fuserName=='@none' or fuserName=='@meet':
            try:
                if fuserName=='@none':
                    userList=self.userDataList[userName.lower()][fType]
                else:
                    userList=[]
            except:
                userList=[]
        else:

            self.formatList(userName.lower(),fuserName.lower(),fType,True)
            userList=self.userDataList[userName.lower()][fType]
        #print("I AM SOUND RECIEVER")
        if data!='@none':
            types=info['types']
            shape=info['shape']
            self.dataContainer[userName.lower()][wType]=[data,types,shape]

        if login:

            threading.Thread(target=self.gmDataControlling,args=(userName,info,'img')).start()

            for i in userList:
                cond=userList[i]
                if cond:
                    onlineCond=self.checkUserOnline(i)
                    openWindow=self.checkOpenWindow(userName.lower(),i)

                    if onlineCond and openWindow:
                        cond2=self.checkUserControl(i.lower(),userName.lower(),rType)

                        if cond2:
                            #print("HE IS RECIEVING")
                            addr1=self.userNAddr[i.lower()]
                            hsend=self.userAddrSR[addr1][0]
                            if data!='@none':
                                data=self.dataContainer[userName.lower()][wType]

                                data=self.reFormatResolution(data,i,'rCameraRes')
                                types=data[1]
                                shape=data[2]
                                data=data[0]



                                data=ad.assValue(['wType','code','data','types','shape','userName'],
                                                 [wType,'d201',data,types,shape,userName.lower()],dType)

                                hsend.send_message(data)



        else:
            data=self.cRequest('L103',wType,dType)
            send.send_message(data)


    def reFormatResolution(self,data,userName,types='rCameraRes'):
        typ=data[1]
        rData=ds.reFormatImageData(data[0])
        data=ds.remodifyData(rData,data[1],data[2],True)

        shape1=data.shape
        if userName.lower() in self.dataResizeController:
            width=self.dataResizeController[userName.lower()][types]

            width=int(width)
        else:
            width=DEFAULT_CAMERA_RES

        if types=='rCameraRes':
            height=int(1.3*int(width))
        else:
            height=int(1.7*int(width))

        shape2=(width,height,3)

        cond=ds.compareStrShape(shape1,shape2)

        if cond==1:
            data=cv2.resize(data,(shape2[0],shape2[1]))

            data=ds.prepareImageFormat(data)
        else:
            data=ds.prepareImageFormat(data)

        return data

    def _Sound(self,info,addr):
        dType='_data'
        wType='_Sound'
        fType='sSound'
        rType='rSound'
        data=info['data']

        fuserName=info['userName']


        send=self.userAddrSR[addr][0]


        userName,login=self.userAddrNL[addr]
        if fuserName=='@none' or fuserName=='@meet':
            try:
                if fuserName=='@none':
                    userList=self.userDataList[userName.lower()][fType]
                else:
                    userList=[]
            except:
                userList=[]
        else:

            self.formatList(userName.lower(),fuserName.lower(),fType,True)
            userList=self.userDataList[userName.lower()][fType]
        #print("I AM SOUND RECIEVER")
        if data!='@none':

            self.dataContainer[userName.lower()][wType]=data
        if login:

            threading.Thread(target=self.gmDataControlling,args=(userName,info,'aud')).start()

            for i in userList:
                cond=userList[i]
                if cond:
                    onlineCond=self.checkUserOnline(i)
                    openWindow=self.checkOpenWindow(userName.lower(),i)

                    if onlineCond and openWindow:
                        cond2=self.checkUserControl(i.lower(),userName.lower(),rType)

                        if cond2:
                            #print("HE IS RECIEVING")
                            addr1=self.userNAddr[i.lower()]
                            hsend=self.userAddrSR[addr1][0]
                            if data!='@none':
                                data=self.dataContainer[userName.lower()][wType]
                                data=ad.assValue(['wType','code','data','userName'],[wType,'d201',data,userName.lower()],dType)

                                hsend.send_message(data)


        else:
            data=self.cRequest('L103',wType,dType)
            send.send_message(data)

    def _IntSound(self,info,addr):
        dType='_data'
        wType='_IntSound'
        fType='sIntSound'
        rType='rIntSound'
        data=info['data']

        fuserName=info['userName']


        send=self.userAddrSR[addr][0]


        userName,login=self.userAddrNL[addr]
        if fuserName=='@none':
            userList=self.userDataList[userName.lower()][fType]
        else:

            self.formatList(userName.lower(),fuserName.lower(),fType,True)
            userList=self.userDataList[userName.lower()][fType]
        #print("I AM SOUND RECIEVER")

        if login:

            for i in userList:
                cond=userList[i]
                if cond:
                    onlineCond=self.checkUserOnline(i)
                    openWindow=self.checkOpenWindow(userName.lower(),i)

                    if onlineCond and openWindow:
                        cond2=self.checkUserControl(i.lower(),userName.lower(),rType)

                        if cond2:
                            #print("HE IS RECIEVING")
                            addr1=self.userNAddr[i.lower()]
                            hsend=self.userAddrSR[addr1][0]
                            if data=='@none':
                                pass
                            else:
                                data=ad.assValue(['wType','code','data','userName'],[wType,'d201',data,userName.lower()],dType)

                                hsend.send_message(data)



        else:
            data=self.cRequest('L103',wType,dType)
            send.send_message(data)

    def _Keyboard(self,info,addr):
        dType='_data'
        wType='_Keyboard'
        fType='sKeyboard'
        rType='rKeyboard'
        data=info['data']

        fuserName=info['userName']


        send=self.userAddrSR[addr][0]

        userName,login=self.userAddrNL[addr]
        if fuserName=='@none':
            userList=self.userDataList[userName.lower()][fType]
        else:

            self.formatList(userName.lower(),fuserName.lower(),fType,True)
            userList=self.userDataList[userName.lower()][fType]
        #print("I AM SOUND RECIEVER")

        if login:

            for i in userList:
                cond=userList[i]
                if cond:
                    onlineCond=self.checkUserOnline(i)
                    openWindow=self.checkOpenWindow(userName.lower(),i)

                    if onlineCond and openWindow:
                        cond2=self.checkUserControl(i.lower(),userName.lower(),rType)

                        if cond2:
                            #print("HE IS RECIEVING")
                            addr1=self.userNAddr[i.lower()]
                            hsend=self.userAddrSR[addr1][0]
                            if data=='@none':
                                pass
                            else:
                                types=info['types']
                                shape=info['shape']
                                data=ad.assValue(['wType','code','data','types','shape','userName'],[wType,'d201',data,types,shape,userName.lower()],dType)

                                hsend.send_message(data)



        else:
            data=self.cRequest('L103',wType,dType)
            send.send_message(data)

    def _Mouse(self,info,addr):
        dType='_data'
        wType='_Mouse'
        fType='sMouse'
        rType='rMouse'
        data=info['data']

        fuserName=info['userName']


        send=self.userAddrSR[addr][0]


        userName,login=self.userAddrNL[addr]
        if fuserName=='@none':
            userList=self.userDataList[userName.lower()][fType]
        else:

            self.formatList(userName.lower(),fuserName.lower(),fType,True)
            userList=self.userDataList[userName.lower()][fType]
        #print("I AM SOUND RECIEVER")

        if login:

            for i in userList:
                cond=userList[i]
                if cond:
                    onlineCond=self.checkUserOnline(i)
                    openWindow=self.checkOpenWindow(userName.lower(),i)

                    if onlineCond and openWindow:
                        cond2=self.checkUserControl(i.lower(),userName.lower(),rType)

                        if cond2:
                            #print("HE IS RECIEVING")
                            addr1=self.userNAddr[i.lower()]
                            hsend=self.userAddrSR[addr1][0]
                            if data=='@none':
                                pass
                            else:
                                types=info['types']
                                shape=info['shape']
                                data=ad.assValue(['wType','code','data','types','shape','userName'],[wType,'d201',data,types,shape,userName.lower()],dType)

                                hsend.send_message(data)



        else:
            data=self.cRequest('L103',wType,dType)
            send.send_message(data)

    def request(self,info,addr):
        dType='request'
        wType='request'

        vType=info['vType']

        fuserName=info['userName']

        send=self.userAddrSR[addr][0]
        userName,login=self.userAddrNL[addr]

        if login:

            condOnline=self.checkUserOnline(fuserName.lower())
            vst={'camera':'rCamera',
                 'sound':'rSound',
                 'screen':'rScreen'
                ,'keyboard':'rKeyboard',
                 'mouse':'rMouse'}
            cond2=self.checkUserControl(fuserName.lower(),userName.lower(),vst[vType])

            if condOnline:

                if not cond2:
                    addr1=self.userNAddr[fuserName.lower()]
                    send=self.userAddrSR[addr1][0]

                    data=ad.assValue(['wType','code','userName','vType'],
                                     [wType,'LHY0',userName,vType],dType)
                    send.send_message(data)
                else:
                    data=ad.assValue(['wType','code','userName','vType'],
                                     [wType,'LFG3',fuserName,vType],dType)
                    send.send_message(data)
            else:
                data=ad.assValue(['wType','code','userName','vType'],
                                     [wType,'LFG7',fuserName,vType],dType)
                send.send_message(data)
        else:
            data=self.cRequest('L103',wType,dType)
            send.send_message(data)

    def response(self,info,addr):
        dType='request'
        wType='response'

        vType=info['vType']
        vValue=info['vValue']

        fuserName=info['userName']

        send=self.userAddrSR[addr][0]
        userName,login=self.userAddrNL[addr]

        if login:

            condOnline=self.checkUserOnline(fuserName.lower())

            if condOnline:
                addr1=self.userNAddr[fuserName.lower()]
                send=self.userAddrSR[addr1][0]
                data=ad.assValue(['wType','code','userName','vType','vValue'],
                                 [wType,'LHN0',userName,vType,vValue],dType)
                send.send_message(data)

        else:
            data=self.cRequest('L103',wType,dType)
            send.send_message(data)

    def formatList(self,userName,fuserName,types,status):

        self.userDataList[userName.lower()][types][fuserName.lower()]=status

    def prepareDataRFController(self,types,values):

        dicts=ad.cvtArr2Dict(types[1:],values[1:])
        self.dataResizeController[values[0]]=dicts
        userName=values[0]
        send=self.getSendOfUser(userName)
        if send is not None:

            send.SEND_FILE_BUFFER=int(dicts['recvFileBuff'])


    def destroyDataRFController(self,userName):
        if userName in self.dataResizeController:
            del self.dataResizeController[userName]

    def onOnlineUser(self,userName,addr=''):
        print(userName,' online ',addr)
        cb,cursor,mydb=self.getNewCbForDataBase()
        users=cb.selectFieldData('f_'+userName,'userName')
        users=ms.modifySqlResult(users)

        col=cb.getColName('dataRFController')
        col=ms.modifySqlResult(col)

        data=cb.selectAllDataByCondition('dataRFController','userName',userName)
        data=ms.modifySqlResult(data)[0]

        self.prepareDataRFController(col,data)

        if users is None:
            pass
        else:
            for i in users:
                cond=self.checkUserOnline(i)

                if cond:
                    addr1=self.userNAddr[i.lower()]
                    send=self.userAddrSR[addr1][0]

                    data=ad.assValue(['wType','status','code','userName'],\
                                     ['onlineStatus','True','L100',userName],\
                                     'specialDType')
                    #print(send)
                    send.send_message(data)


    def onOfflineUser(self,userName,addr):
        print(userName ,' offline ',addr)
        self.handleFileOnUserOffline(userName)
        self.gmOnGoingOffline(userName)
        mydb=db.genMdb()
        cursor=mydb.cursor()

        self.destroyDataRFController(userName)
        cb=db.cb1(cursor,'_xprtinfo')

        users=cb.selectFieldData('f_'+userName,'userName')
        users=ms.modifySqlResult(users)

        if users is None:
            pass
        else:

            for i in users:
                cond=self.checkUserOnline(i)

                if cond:
                    addr1=self.userNAddr[i.lower()]
                    send=self.userAddrSR[addr1][0]

                    data=ad.assValue(['wType','status','code','userName'],\
                                     ['onlineStatus','False','L100',userName.lower()],\
                                     'specialDType')
                    #print(send)
                    send.send_message(data)

    #-----------------Group-Chat-------------
    def createGroup(self,info,addr):

        dType='GroupChat'
        wType=info['wType']

        cb,cursor,mydb=self.getNewCbForDataBase()
        send=self.userAddrSR[addr][0]


        userName,login=self.userAddrNL[addr]
        xinfo=xdb.XprtInfo(cursor)
        xnot=xdb.XprtNot(cursor)

        if login:
            groupName=info['groupName']
            cond=cb.checkData('GroupChat','groupName',groupName)

            if cond:
                data=self.cRequest('0000',wType,dType)
                send.send_message(data)
            else:
                xinfo.insertGroupChat([groupName,'1'])
                xnot.createChatGroupChat(groupName)
                xnot.createGroupRRecv(groupName)
                xnot.createGroupRSent(groupName)
                xnot.createGroupMembers(groupName)

                xnot.insertInfoG(userName,groupName)

                cb.insertDataN('g_'+groupName,['0',userName,'a'])


                cb.insertDataN('ug_'+userName,['1',groupName])

                data=self.cRequest('0011',wType,dType)
                send.send_message(data)
        else:
            data=self.cRequest('1111',wType)
            send.send_message(data)

        mydb.commit()

    def ifNotFoundUserGroupIdentity(self,cursor,userName):
        xnot=xdb.XprtNot(cursor)
        xnot.createUserGroupInfoHolder(userName)

    def refressGCSearch(self,info,addr):
        dType='GroupChat'
        wType=info['wType']

        cb,cursor,mydb=self.getNewCbForDataBase()
        send=self.userAddrSR[addr][0]

        userName,login=self.userAddrNL[addr]


        if login:
            data=cb.selectRandomData('groupchat','*',30)

            data=ms.modifySqlResult(data)

            dfData=[]

            for i in data:
                mem=i[1]
                i=i[0]
                t1='g_'+i

                cond=cb.checkData(t1,'userName',userName)

                if not cond:
                    dfData.append([i,mem])

            if len(dfData) >0:
                    prepData=ds.prepSend(dfData)

                    data=ad.assValue(['wType','data','types','shape','code']
                                 ,[wType]+prepData+['yh2k'],dType)
                    send.send_message(data)

        else:
            data=self.cRequest('1111',wType)
            send.send_message(data)

    def searchGroup(self,info,addr):
        dType='GroupChat'
        wType=info['wType']

        cb,cursor,mydb=self.getNewCbForDataBase()
        send=self.userAddrSR[addr][0]


        userName,login=self.userAddrNL[addr]
        xinfo=xdb.XprtInfo(cursor)

        if login:
            groupName=info['groupName']

            if info['hs']=='1':

                cond=cb.checkData('GroupChat','groupName',groupName)

                if cond:
                    #Group Exist

                    data=cb.selectAllDataByCondition('GroupChat','groupName',groupName)
                    data=ms.modifySqlResult(data)

                    try:
                        udata=cb.selectFieldData('ug_'+userName,'groupName')
                        udata=ms.modifySqlResult(udata)
                    except:
                        self.ifNotFoundUserGroupIdentity(cursor,userName)
                        udata=[]

                    prepData=ds.prepSend([])

                    if udata is None:
                        prepData=ds.prepSend(data)
                        data=ad.assValue(['wType','data','types','shape','code']
                                     ,[wType]+prepData+['y12k'],dType)
                        send.send_message(data)
                    else:

                        d=[]
                        for i in data:


                            if not  ms.inEqual(i[0],udata):
                                d.append(i)

                        prepData=ds.prepSend(d)



                        data=ad.assValue(['wType','data','types','shape','code']
                                         ,[wType]+prepData+['y12k'],dType)
                        send.send_message(data)
                else:
                    #Group Don't exist
                    data=self.cRequest('2333',wType,dType)
                    send.send_message(data)

            else:
                cm=f'%{groupName}%'
                data=cb.selectRandomWithLike('groupchat','groupName',cm,'*',30)
                data=ms.modifySqlResult(data)


                dfData=[]

                for i in data:
                    mem=i[1]
                    i=i[0]
                    t1='g_'+i

                    cond=cb.checkData(t1,'userName',userName)

                    if not cond:
                        dfData.append(i)

                if len(dfData) >0:
                        prepData=ds.prepSend(data)
                        data=ad.assValue(['wType','data','types','shape','code']
                                     ,[wType]+prepData+['y12k'],dType)
                        send.send_message(data)
                else:
                        data=self.cRequest('45kt',wType,dType)
                        send.send_message(data)




        else:
            data=self.cRequest('1111',wType)
            send.send_message(data)

    def loadGroupInfo(self,info,addr):

        dType='GroupChat'
        wType=info['wType']

        cb,cursor,mydb=self.getNewCbForDataBase()
        send=self.userAddrSR[addr][0]


        userName,login=self.userAddrNL[addr]
        xinfo=xdb.XprtInfo(cursor)

        if login:

            groupName=info['groupName']

            cond=cb.checkData('GroupChat','groupName',groupName)

            if cond:
                data=cb.selectAllDataByCondition('GroupChat','groupName',groupName)

                data=ms.modifySqlResult(data)

                prepData=ds.prepSend(data)

                mdata=cb.selectAllData('g_'+groupName)
                mdata=ms.modifySqlResult(mdata)
                mprepData=ds.prepSend(mdata)
                wType=info['xt']

                ft=cb.selectAllDataByCondition('g_'+groupName,'type','a')
                ft=ms.modifySqlResult(ft)[0]
                adm=ft[1]

                data=ad.assValue(['wType','admin','code','groupName','data','types','shape','mdata','mtypes','mshape']
                                 ,[wType,adm,'y12k',groupName]+prepData+mprepData,dType)

                send.send_message(data)
            else:
                data=self.cRequest('2333',wType,dType)
                send.send_message(data)

        else:
            data=self.cRequest('1111',wType)
            send.send_message(data)

    def refressGC(self,info,addr):

        dType='GroupChat'
        wType=info['wType']

        cb,cursor,mydb=self.getNewCbForDataBase()
        send=self.userAddrSR[addr][0]


        userName,login=self.userAddrNL[addr]
        xinfo=xdb.XprtInfo(cursor)

        if login:

            cond=cb.checkTable('ug_'+userName)
            if not cond:
                self.ifNotFoundUserGroupIdentity(cursor,userName)

            data=cb.selectAllData('ug_'+userName)

            data=ms.modifySqlResult(data)

            data=ds.prepSend(data)
            data=ad.assValue(['wType','code','data','type','shape'],
                             [wType,'12k3']+data,dType)
            send.send_message(data)

        else:
            data=self.cRequest('1111',wType)
            send.send_message(data)

    def getAllMemberOfGC(self,cb,groupName):
        tName='g_'+groupName
        userName=cb.selectFieldData(tName,'userName')
        userName=ms.modifySqlResult(userName)
        return userName

    def sendGroupRequest(self,info,addr):
        dType='GroupChat'
        wType=info['wType']

        cb,cursor,mydb=self.getNewCbForDataBase()
        send=self.userAddrSR[addr][0]


        userName,login=self.userAddrNL[addr]
        xinfo=xdb.XprtInfo(cursor)

        if login:
            groupName=info['groupName']
            tName='g_'+groupName

            cond=cb.checkData(tName,'userName',userName)
            if not cond:

                tname2='gr_'+groupName
                cond=cb.checkData(tname2,'userName',userName)

                if not cond:
                    cb.insertDataN(tname2,['1',userName])

                    cb.insertDataN('ugs_'+userName,['1',groupName])
                    data=self.cRequest('1123',wType,dType)
                else:
                    data=self.cRequest('45g6',wType,dType)
            else:
                data=self.cRequest('34f6',wType,dType)



            send.send_message(data)
            mydb.commit()

        else:
            data=self.cRequest('1111',wType)
            send.send_message(data)

    def groupSendRequest(self,info,addr):
        dType='GroupChat'
        wType=info['wType']

        cb,cursor,mydb=self.getNewCbForDataBase()
        send=self.userAddrSR[addr][0]


        userName,login=self.userAddrNL[addr]
        xnot=xdb.XprtNot(cursor)

        if login:

            groupName=info['groupName']
            users=self.getAllMemberOfGC(cb,groupName)

            us=info['userName']
            user=cb.selectAllDataByCondition('g_'+groupName,'userName',userName)

            user=ms.modifySqlResult(user)

            if user is  None:

                data=self.cRequest('1ee1',wType,dType)
                send.send_message(data)

            else:
                user=user[0]
                uName=user[1]
                type=user[2]
                if type=='a':

                    tName='gs_'+groupName

                    cond=cb.checkData(tName,'userName',us)

                    if cond:
                        data=self.cRequest('e923',wType,dType)
                        send.send_message(data)
                    else:

                        cb.insertDataN(tName,['1',us])

                        cb.insertDataN('ugr_'+us,['1',groupName])

                        data=self.cRequest('1222',wType,dType)

                        cb.updateParticularData('information','userName','groupRequest',us,'False')

                        for i in users:
                            xnot.updateInfoGCP(i,groupName,'False')

                        send.send_message(data)
                        mydb.commit()
                else:

                    data=self.cRequest('1uu1',wType,dType)
                    send.send_message(data)
        else:
            data=self.cRequest('1111',wType)
            send.send_message(data)

        mydb.commit()

    def groupSearchMemberForSRequest(self,info,addr):

        wType=info['wType']
        dType='GroupChat'
        searchUserName=info['userName']
        cb,cursor,mydb=self.getNewCbForDataBase()
        send=self.userAddrSR[addr][0]


        userName,login=self.userAddrNL[addr]

        data=cb.selectByMulOrCondNot('sequrity',['userName','name'],
                                     [searchUserName,searchUserName],
                                     ['userName'],[userName],'userName')
        data=ms.modifySqlResult(data)
        xnot=xdb.XprtNot(cursor)
        xinfo=xdb.XprtInfo(cursor)
        if login:
            if data is None:
                data=self.cRequest('0012',wType,dType)
                send.send_message(data)
            else:
                correctUser=[]
                for user in data:
                    cond1=xnot.checkBlock(userName,user)
                    cond2=xnot.checkBlock(user,userName)
                    if (not cond1) and(not cond2):
                        correctUser.append(user)


                usrData=[]
                for user in correctUser:

                    if user==userName:
                        continue
                    d=xinfo.getSomeProfile(user)[0]
                    d=list(d)
                    if d[2]=='_None':
                        imgD=['_None','_None','_None']
                    else:
                        d[2]=ds.dec(d[2])
                        d[2]=cv2.imread(d[2])
                        imgD=ds.prepareImageFormat(d[2])

                    d=d[:2]

                    usrData.append(d+imgD)

                if len(usrData)==0:
                    data=self.cRequest('0013',wType,dType)
                    send.send_message(data)
                else:
                    uD=ds.prepSend(usrData)

                    data=ad.assValue(['wType','code','usersData','usersType','usersShape'],
                                     [wType,'0014',uD[0],uD[1],uD[2]],dType)
                    send.send_message(data)
        else:
            data=self.cRequest('1111',wType)
            send.send_message(data)

    def loadGroupRequest(self,info,addr):

        dType='GroupChat'
        wType=info['wType']

        cb,cursor,mydb=self.getNewCbForDataBase()
        send=self.userAddrSR[addr][0]


        userName,login=self.userAddrNL[addr]
        xnot=xdb.XprtNot(cursor)

        if login:
            tp=info['tp']

            if tp=='g':
                groupName=info['groupName']
                users=self.getAllMemberOfGC(cb,groupName)

                tName='g_'+groupName
                cond=cb.checkMulAndData(tName,['userName','type'],[userName,'a'])
                if cond:
                    tName='gr_'+groupName
                    data=cb.selectFieldData(tName,'userName')
                    data=ms.modifySqlResult(data)
                    tdata=[]
                    if data is not None:
                        for userName in data:
                            p=xinfo.getSomeProfile(userName)
                            tdata.append(p)
                    data=ds.prepSend(tdata)
                    for i in users:
                        xnot.updateInfoGCP(i,groupName,'False)')

                    data=ad.assValue(['wType','code','tp','data','type','shape'],
                                     [wType,'11e1','g',data[0],data[1],data[2]],dType)
                    send.send_message(data)
                else:
                    data=self.cRequest('eeeg',wType,dType)
                    send.send_message(data)

            else:
                #Member
                cb.updateParticularData('Information','userName','GroupRequest'
                                     ,userName,'True')

                data=cb.selectAllData('ugr_'+userName)
                data=ms.modifySqlResult(data)
                data=ds.prepSend(data)
                data=ad.assValue(['wType','code','tp','data','type','shape'],
                                     [wType,'1ss2','m',data[0],data[1],data[2]],dType)
                send.send_message(data)


        else:
            data=self.cRequest('1111',wType)
            send.send_message(data)
        mydb.commit()

    def deleteFromArray(self,array,data,num=True):
        if num:
            a=array.tolist()
        else:
            a=array
        index=a.index(data)
        a.pop(index)
        if num:
            a=np.array(a)

        return a

    def rejectGroupRequest(self,info,addr):

        dType='GroupChat'
        wType='acceptGroupRequestAdmin'

        cb,cursor,mydb=self.getNewCbForDataBase()
        send=self.userAddrSR[addr][0]


        userName,login=self.userAddrNL[addr]
        xinfo=xdb.XprtInfo(cursor)

        if login:
            groupName=info['groupName']
            user=info['userName']
            cb.deleteBySingleCond('ugr_'+userName,'groupName',groupName)
            time.sleep(0.1)
            cb.deleteBySingleCond('ugs_'+userName,'groupName',groupName)
            time.sleep(0.1)
            cb.deleteBySingleCond('gr_'+groupName,'userName',user)
            time.sleep(0.1)
            cb.deleteBySingleCond('gs_'+groupName,'userName',user)
            time.sleep(0.1)

            mydb.commit()
            data=ad.assValue(['wType','code'],[wType,'tkm4'],dType)
            send.send_message(data)

        else:
            data=self.cRequest('1111',wType)
            send.send_message(data)

    def acceptGroupRequest(self,info,addr):
        at=info['acceptT']
        tp=info['tp']
        if tp=='g':
            if at=='1':
                dType='GroupChat'
                wType='acceptGroupRequestAdmin'

                mydb=self.dbHandleAddr[addr]
                cursor=mydb.cursor()
                send=self.userAddrSR[addr][0]
                cb=db.cb1(cursor,'_xprtinfo')

                groupName=info['groupName']

                users=self.getAllMemberOfGC(cb,groupName)
                userName,login=self.userAddrNL[addr]
                xnot=xdb.XprtNot(cursor)

                if login:
                    user=info['userName']

                    cb.deleteBySingleCond('ugr_'+userName,'groupName',groupName)
                    cb.deleteBySingleCond('ugs_'+userName,'groupName',groupName)
                    cb.deleteBySingleCond('gr_'+groupName,'userName',user)
                    cb.deleteBySingleCond('gs_'+groupName,'userName',user)

                    cb.insertDataN('g_'+groupName,['1',user,'m'])
                    cb.insertDataN('ug_'+user,['1',groupName])

                    msg=f'{user} joined group chat'
                    msg=ds.enc(msg)
                    data=ad.assValue(['chat','groupName','userName',],[msg,groupName,'@Official'],'Chat')
                    data=ds.enc(data)
                    cb.insertDataN('gc_'+groupName,['1',data])

                    xnot.insertInfoG(user,groupName)
                    for i in users:
                        xnot.updateInfoGCP(i,groupName,'False')
                        xnot.updateInfoGC(i,groupName,'False')

                    data=ad.assValue(['wType','code'],[wType,'ffe4'],dType)
                    send.send_message(data)
                    mydb.commit()
                else:
                    data=self.cRequest('1111',wType)
                    send.send_message(data)
            else:
                self.rejectGroupRequest(info,addr)
        else:
            if at=='1':
                self.acceptGroupRequestMember(info,addr)
            else:
                self.rejectGroupRequestMember(info,addr)

    def acceptGroupRequestMember(self,info,addr):
        wType='acceptGroupRequestMember'
        dType='GroupChat'

        cb,cursor,mydb=self.getNewCbForDataBase()
        send=self.userAddrSR[addr][0]
        cb=db.cb1(cursor,'_xprtinfo')

        groupName=info['groupName']

        users=self.getAllMemberOfGC(cb,groupName)
        userName,login=self.userAddrNL[addr]
        xnot=xdb.XprtNot(cursor)

        user=info['userName']


        msg=f'{user} joined group chat'
        msg=ds.enc(msg)
        data=ad.assValue(['chat','groupName','userName',],[msg,groupName,'@Official'],'Chat')
        data=ds.enc(data)
        cb.insertDataN('gc_'+groupName,['1',data])

        xnot.insertInfoG(userName,groupName)
        for i in users:
            xnot.updateInfoGCP(i,groupName,'False')
            xnot.updateInfoGC(i,groupName,'False')

        cb.deleteBySingleCond('ugr_'+userName,'groupName',groupName)
        cb.deleteBySingleCond('ugs_'+userName,'groupName',groupName)
        cb.deleteBySingleCond('gr_'+groupName,'userName',user)
        cb.deleteBySingleCond('gs_'+groupName,'userName',user)

        cb.insertDataN('g_'+groupName,['1',user,'m'])
        cb.insertDataN('ug_'+user,['1',groupName])

        data=ad.assValue(['wType','code'],[wType,'ffe4'],dType)
        send.send_message(data)
        mydb.commit()

    def rejectGroupRequestMember(self,info,addr):
        wType='acceptGroupRequestMember'
        dType='GroupChat'
        cb,cursor,mydb=self.getNewCbForDataBase()
        send=self.userAddrSR[addr][0]


        userName,login=self.userAddrNL[addr]
        xinfo=xdb.XprtInfo(cursor)
        groupName=info['groupName']
        user=info['userName']
        cb.deleteBySingleCond('ugr_'+userName,'groupName',groupName)
        time.sleep(0.1)
        cb.deleteBySingleCond('ugs_'+userName,'groupName',groupName)
        time.sleep(0.1)
        cb.deleteBySingleCond('gr_'+groupName,'userName',user)
        time.sleep(0.1)
        cb.deleteBySingleCond('gs_'+groupName,'userName',user)
        time.sleep(0.1)
        mydb.commit()
        data=ad.assValue(['wType','code'],[wType,'tkm4'],dType)
        send.send_message(data)

    def loadGroupChatInfo(self,info,addr):

        dType='GroupChat'
        wType=info['wType']

        cb,cursor,mydb=self.getNewCbForDataBase()
        send=self.userAddrSR[addr][0]


        userName,login=self.userAddrNL[addr]
        xinfo=xdb.XprtInfo(cursor)

        if login:
            groupName=info['groupName']
            tName='gc_'+groupName

            chats=cb.selectFieldData(tName,'chats')

            chats=ms.modifySqlResult(chats)

            data=ds.prepSend(chats)

            data=ad.assValue(['wType','code','cdata','ctype','cshape'],
                             [wType,'12k3',data[0],data[1],data[2]],dType)

            send.send_message(data)



        else:
            data=self.cRequest('1111',wType)
            send.send_message(data)

    def groupControlPanel(self,info,addr):

        dType='GroupChat'
        wType=info['wType']

        cb,cursor,mydb=self.getNewCbForDataBase()
        send=self.userAddrSR[addr][0]


        userName,login=self.userAddrNL[addr]
        xnot=xdb.XprtNot(cursor)

        if login:
            gName=info['groupName']

            mainMember=cb.selectFieldData('g_'+gName,'userName,type')
            sendMember=cb.selectFieldData('gs_'+gName,'userName')
            recvMember=cb.selectFieldData('gr_'+gName,'userName')

            mainMember=ms.modifySqlResult(mainMember)
            sendMember=ms.modifySqlResult(sendMember)
            recvMember=ms.modifySqlResult(recvMember)

            xnot.updateInfoGCP(userName,gName,'True')



            pMainMember=ds.prepSend(mainMember)
            pSendMember=ds.prepSend(sendMember)
            pRecvMember=ds.prepSend(recvMember)



            data=ad.assValue(['wType','code','groupName','mm','mmt','mms','sm','smt','sms','rm','rmt','rms'],
                             [wType,'kk14',gName]+pMainMember+pSendMember+pRecvMember,dType)


            send.send_message(data)
        else:
            data=self.cRequest('1111',wType)
            send.send_message(data)
        mydb.commit()

    def groupChatWindow(self,info,addr):

        dType='GroupChat'
        wType=info['wType']

        cb,cursor,mydb=self.getNewCbForDataBase()
        send=self.userAddrSR[addr][0]


        userName,login=self.userAddrNL[addr]
        xnot=xdb.XprtNot(cursor)

        if login:

            groupName=info['groupName']
            xnot.updateInfoGC(userName,groupName,'True')
            #Now from here the searching for the chat is started
            #I am very sad today 7:12:2020 5:43 PM
            #I miss someone very much i dont know why
            # His name is Anjali-XXXX911493-XXXghat
            #Now the time changes i became what i was
            #December 12,2020 2:01 PM
            #Let's see what will happen to the next

            #12:34 8/1/2021 I lost Here

            data=cb.selectFieldData('gc_'+groupName,'chats')
            data=ms.modifySqlResult(data)

            data=ds.prepSend(data)
            data=ad.assValue(['wType','code','dataC','dataCT','dataCS','groupName'],
                             [wType,'k31s',data[0],data[1],data[2],groupName],dType)
            send.send_message(data)


        else:
            data=self.cRequest('1111',wType)
            send.send_message(data)

        mydb.commit()

    def leaveGroup(self,info,addr):

        dType='GroupChat'
        wType=info['wType']

        cb,cursor,mydb=self.getNewCbForDataBase()
        send=self.userAddrSR[addr][0]


        userName,login=self.userAddrNL[addr]
        xnot=xdb.XprtNot(cursor)

        if login:
            groupName=info['groupName']
            tName='g_'+groupName
            cond=cb.checkMulAndData(tName,['userName','type'],[userName,'a'])

            if cond:
                cb.deleteBySingleCond('groupchat','groupName',groupName)

                cb.deleteBySingleCond('ug_'+userName,'groupName',groupName)
                data=cb.selectFieldData('g_'+groupName,'userName')
                data=ms.modifySqlResult(data)



                time.sleep(0.3)
                cb.dropTable(tName)
                time.sleep(0.3)
                cb.dropTable('gc_'+groupName)
                time.sleep(0.3)
                cb.dropTable('gs_'+groupName)
                time.sleep(0.3)
                cb.dropTable('gr_'+groupName)
                time.sleep(0.3)


                for i in data:
                    cb.deleteBySingleCond('ug_'+i,'groupName',groupName)



            else:
                d=cb.selectParticularData('groupChat','groupName','members',groupName)
                d=int(d[0][0])
                d=d-1
                cb.updateParticularData('groupChat','groupName','members',groupName,str(d))


                cb.deleteBySingleCond(tName,'userName',userName)
                cb.deleteBySingleCond('ug_'+userName,'groupName',groupName)
                msg=f'{userName} leaved group chat'
                msg=ds.enc(msg)
                data=ad.assValue(['chat','groupName','userName',],[msg,groupName,'@Official'],'Chat')
                data=ds.enc(data)
                cb.insertDataN('gc_'+groupName,['1',data])

            xnot.deleteInfoG(userName,groupName)


        else:
            data=self.cRequest('1111',wType)
            send.send_message(data)

        mydb.commit()

    def kickMemberGroupChat(self,info,addr):

        dType='GroupChat'
        wType=info['wType']

        cb,cursor,mydb=self.getNewCbForDataBase()
        send=self.userAddrSR[addr][0]


        userName,login=self.userAddrNL[addr]
        xnot=xdb.XprtNot(cursor)

        if login:
            userName=info['userName']
            groupName=info['groupName']

            tName='g_'+groupName
            cb.deleteBySingleCond(tName,'userName',userName)
            cb.deleteBySingleCond('ug_'+userName,'groupName',groupName)

            msg=f'{userName} kicked group chat'
            msg=ds.enc(msg)
            data=ad.assValue(['chat','groupName','userName',],[msg,groupName,'@Official'],'Chat')
            data=ds.enc(data)
            cb.insertDataN('gc_'+groupName,['1',data])
            xnot.deleteInfoG(userName,groupName)
            mydb.commit()

        else:
            data=self.cRequest('1111',wType)
            send.send_message(data)

    def cancelGroupSendRequest(self,info,addr):

        dType='GroupChat'
        wType=info['wType']

        cb,cursor,mydb=self.getNewCbForDataBase()
        send=self.userAddrSR[addr][0]


        userName,login=self.userAddrNL[addr]
        xinfo=xdb.XprtInfo(cursor)

        if login:
                    groupName=info['groupName']
                    user=info['userName']

                    cb.deleteBySingleCond('gr_'+groupName,'userName',user)
                    cb.deleteBySingleCond('gs_'+groupName,'userName',user)
                    cb.deleteBySingleCond('ugr_'+userName,'groupName',groupName)
                    cb.deleteBySingleCond('ugs_'+userName,'groupName',groupName)


                    data=self.cRequest('tk87',wType,dType)
                    mydb.commit()
                    send.send_message(data)
        else:
            data=self.cRequest('1111',wType)
            send.send_message(data)

    def sendGroupChat(self,info,addr):

        dType='GroupChat'
        wType=info['wType']

        cb,cursor,mydb=self.getNewCbForDataBase()
        send=self.userAddrSR[addr][0]


        userName,login=self.userAddrNL[addr]
        xnot=xdb.XprtNot(cursor)

        if login:
            gName=info['groupName']
            chat=info['chat']


            data=ad.assValue(['chat','groupName','userName'],[chat,gName,userName],'Chat')

            data=ds.enc(data)


            cb.insertDataN('gc_'+gName,['1',data])

            members=cb.selectFieldData('g_'+gName,'userName')
            members=ms.modifySqlResult(members)

            for i in members:
                luser=i.lower()
                if luser==userName.lower():
                    pass
                else:
                    send=self.getSendOfUser(luser)

                    if send is not None:


                        data=ad.assValue(['wType','code','chat']
                                         ,[wType,'kkr1',data],dType)
                        send.send_message(data)
                    else:
                        xnot.updateInfoGC(i,gName,'False')


        else:
            data=self.cRequest('1111',wType)
            send.send_message(data)

        mydb.commit()

    def getSendOfUser(self,user):
        user=user.lower()

        cond=self.checkUserOnline(user)
        if cond:
            addr1=self.userNAddr[user]
            send=self.userAddrSR[addr1][0]
            return send

    def getRecvOfUser(self,user):
        user=user.lower()

        cond=self.checkUserOnline(user)
        if cond:
            addr1=self.userNAddr[user]
            recv=self.userAddrSR[addr1][1]
            return recv

    #-------------------------Group-Meeting------------

    def gmGenMeetingId(self):
        d=None
        while True:
            d=str(random.randint(100000,999999))
            if d in self.MeetingId:
                pass
            else:
                break
        return d

    def gmCreateMeeting(self,info,addr):

        dType='GroupMeet'
        wType=info['wType']

        send=self.userAddrSR[addr][0]


        userName,login=self.userAddrNL[addr]


        if login:

            name=info['name']
            password=info['password']
            id=self.gmGenMeetingId()
            self.MeetingId[id]=[name,password]

            self.MeetingMembers[id]={userName:'a'}
            self.MeetingContData[id]={userName:{}}
            self.MembersMeeting[userName]=id
            self.MeetingLock[id]='0'
            self.MeetingAuthReq[id]='0'
            self.MeetingSendCont[id]={userName:{'img':0,'aud':0}}
            #self.MeetingContData[id]={userName:{userName2:{img:1,aud:0}}}


            data=ad.assValue(['wType','id','name','password','code'],
                             [wType,id,name,password,'1122'],dType)
            send.send_message(data)


        else:
            data=self.cRequest('1111',wType)
            send.send_message(data)

    def gmGetAdminOfMeeting(self,id):
        ads=None

        if id in self.MeetingMembers:

            for i in self.MeetingMembers[id]:

                v=self.MeetingMembers[id][i]

                if v=='a':
                    ads=i
                    break

        return ads

    def gmJoinMeeting(self,info,addr):

        dType='GroupMeet'
        wType=info['wType']


        send=self.userAddrSR[addr][0]


        userName,login=self.userAddrNL[addr]


        if login:
            id=info['id']
            password=info['password']

            cond=id in self.MeetingId

            if cond:

                name,passw=self.MeetingId[id]

                if passw==password:
                    #Password Confirmed

                    lockCond=self.MeetingLock[id]

                    if lockCond=='0':
                        #Meeting Room is Open

                        authReqCond=self.MeetingAuthReq[id]

                        if authReqCond=='0':


                            members=self.MeetingMembers[id]

                            mem=self.gmMergeMembers(id,userName)
                            self.gmSendDetailOfMember(mem,userName)
                            adminName=self.gmGetAdminOfMeeting(id)

                            data=ad.assValue(['wType','code','id','name','password','admin'],
                                             [wType,'fer3',id,name,'*********',adminName],dType)
                            send.send_message(data)
                            time.sleep(2)
                            self.gmInitTrueJoinCondition(id,userName)

                        else:
                            self.gmInitFalseJoinCondition(id,userName)
                            data=self.cRequest('ft65',wType,dType)
                            send.send_message(data)
                    else:
                        #Meeting Room is closed
                        data=self.cRequest('eel3',wType,dType)
                        send.send_message(data)
                    '''
                    admin=self.gmGetAdminOfMeeting(id)
                    addr1=self.userNAddr[admin.lower()]
                    hsend=self.userAddrSR[addr1][0]
                    data=ad.assValue(['wType','userName'],[wType,userName],dType)
                    hsend.send_message(data)
                    '''

                else:
                    data=self.cRequest('1221',wType,dType)
                    send.send_message(data)

            else:
                data=self.cRequest('kkr1',wType,dType)
                send.send_message(data)

        else:
            data=self.cRequest('1111',wType)
            send.send_message(data)

    def gmOnClose(self,info,addr):

        self.gmLeaveMeeting(info,addr)

    def gmMergeMembers(self,id,newUser):
        self.MembersMeeting[newUser]=id

        mem=[]
        members=self.MeetingMembers[id]

        self.MeetingContData[id][newUser]={}

        for user in members:
            self.MeetingContData[id][user][newUser]={'img':1,'aud':0}
            self.MeetingContData[id][newUser][user]={'img':1,'aud':0}
            mem.append(user)

        self.MeetingMembers[id][newUser]='m'
        return mem

    def gmSendDetailOfMember(self,member,userName):
        dType='GroupMeet'
        for i in member:
            send=self.getSendOfUser(i.lower())
            data=ad.assValue(['wType','userName','code'],
                             ["gmSendDetailOfMember",userName,'adm1'],dType)
            send.send_message(data)

    def gmInitTrueJoinCondition(self,id,userName,code='ini1'):
        member=self.MeetingMembers[id]

        member=ad.cvtDict2Array(member)
        mdata=ds.prepSend(member)
        if code=='ini1':

            wType='gmJoiningResponse'
        else:
            wType='gmJoinMeeting'

        dType='GroupMeet'

        send=self.getSendOfUser(userName)

        self.MeetingSendCont[id][userName]={'img':0,'aud':0}
        name,password=self.MeetingId[id]
        adminName=self.gmGetAdminOfMeeting(id)
        data=ad.assValue(['wType','admin','code','data','type','shape','name','password','id'],
                         [wType,adminName,code,mdata[0],mdata[1],mdata[2],name,'*********',id],dType)




        if send is not None:
            send.send_message(data)

    def gmInitFalseJoinCondition(self,id,userName):
        admin=self.gmGetAdminOfMeeting(id)

        sAdmin=self.getSendOfUser(admin)
        sUserName=self.getSendOfUser(userName)

        wType='gmJoinClientRequest'
        dType="GroupMeet"

        data1=ad.assValue(['wType','code','userName'],[wType,'1er4',userName],dType)

        if sAdmin is not None:
            sAdmin.send_message(data1)

    def gmJoinClientRequestResponse(self,info,addr):

        dType='GroupMeet'
        wType=info['wType']

        send=self.userAddrSR[addr][0]


        userName,login=self.userAddrNL[addr]

        if login:
            id=self.MembersMeeting[userName]
            user=info['userName']
            value=info['value']
            adminName=self.gmGetAdminOfMeeting(id)
            if adminName.lower()==userName.lower():

                if value=='1':
                    members=self.MeetingMembers[id]
                    mem=self.gmMergeMembers(id,user)

                    self.gmSendDetailOfMember(mem,user)

                    self.gmInitTrueJoinCondition(id,user,'ini2')
                else:
                    send=self.getSendOfUser(user)
                    if send is not None:
                        data=ad.assValue(['wType','code','id'],["gmJoinMeeting",'kke3',id],dType)
                        send.send_message(data)


        else:
            data=self.cRequest('1111',wType)
            send.send_message(data)

    def gmAdminLeftMeeting(self,id):
        members=self.MeetingMembers[id]
        sender=[]
        for user in members:
            types=members[user]
            if types=='a':
                pass
            else:
                send=self.getSendOfUser(user)
                sender.append(send)
        return sender

    def gmMemberLeftMeeting(self,userName,id):
        members=self.MeetingMembers[id]
        sender=[]
        for user in members:
            if user.lower()==userName.lower():
                continue

            send=self.getSendOfUser(user)
            sender.append(send)
        return sender

    def gmLeaveMeeting(self,info,addr):

        dType='GroupMeet'
        wType=info['wType']



        send=self.userAddrSR[addr][0]


        userName,login=self.userAddrNL[addr]


        if login:
            id=self.MembersMeeting[userName]
            cond=id in self.MeetingId
            if cond:
                admin=self.gmGetAdminOfMeeting(id)
                if admin != None:
                    if admin.lower()==userName.lower():
                        data=ad.assValue(['wType','code','GpStatus','userName'],
                                         [wType,'aa00','mend',userName],dType)
                        sender=self.gmAdminLeftMeeting(id)
                        for i in sender:
                            if i is not None:
                                i.send_message(data)

                        del self.MeetingId[id]
                        del self.MeetingMembers[id]
                        del self.MeetingContData[id]
                        del self.MembersMeeting[userName]
                        del self.MeetingLock[id]
                        del self.MeetingAuthReq[id]
                        del self.MeetingSendCont[id]

                    else:
                        data=ad.assValue(['wType','code','GpStatus','userName']
                                         ,[wType,'mm00','mend',userName],dType)
                        sender=self.gmMemberLeftMeeting(userName,id)
                        for i in sender:
                            if i is not None:
                                i.send_message(data)
                        if id in self.MeetingMembers:
                            del self.MeetingMembers[id][userName]
                        if id in self.MeetingContData:
                            del self.MeetingContData[id][userName]
                        if userName in self.MembersMeeting:
                            del self.MembersMeeting[userName]


        else:
            data=self.cRequest('1111',wType)
            send.send_message(data)

    def gmSendChat(self,info,addr):

        dType='GroupMeet'
        wType=info['wType']


        send=self.userAddrSR[addr][0]


        userName,login=self.userAddrNL[addr]


        if login:

            if userName in self.MembersMeeting:
                id=self.MembersMeeting[userName]
                chat=info['chat']
                sender=self.gmMemberLeftMeeting(userName,id)

                data=ad.assValue(['wType','chat','userName','code'],
                                 [wType,chat,userName,'9211'],dType)
                for i in sender:
                    i.send_message(data)


            else:
                data=self.cRequest('2311',wType,dType)
                send.send_message(data)
        else:
            data=self.cRequest('1111',wType)
            send.send_message(data)

    def gmKickOut(self,info,addr):

        dType='GroupMeet'
        wType=info['wType']


        send=self.userAddrSR[addr][0]


        userName,login=self.userAddrNL[addr]


        if login:
            id=self.MembersMeeting[userName]
            user=info['userName']
            data=ad.assValue(['wType','code','userName'],[wType,'99kk',user],dType)
            sender=self.gmMemberLeftMeeting(user,id)
            for i in sender:
                i.send_message(data)

            data=ad.assValue(['wType','code','id'],[wType,'98kk',id],dType)
            send=self.getSendOfUser(user)
            if send is not None:
                send.send_message(data)

            del self.MeetingMembers[id][userName]
            del self.MeetingContData[id][userName]
            del self.MembersMeeting[userName]
        else:
            data=self.cRequest('1111',wType)
            send.send_message(data)

    def gmLockMeeting(self,info,addr):

        dType='GroupMeet'
        wType=info['wType']

        send=self.userAddrSR[addr][0]

        userName,login=self.userAddrNL[addr]


        if login:
            id=self.MembersMeeting[userName]
            admin=self.gmGetAdminOfMeeting(id)

            if admin.lower()==userName.lower():
                self.MeetingLock[id]=info['value']

                self.gmUpdateMembersOfMeeting(id,'kr14',info['value'])
        else:
            data=self.cRequest('1111',wType)
            send.send_message(data)

    def gmAuthRequest(self,info,addr):

        dType='GroupMeet'
        wType=info['wType']

        send=self.userAddrSR[addr][0]

        userName,login=self.userAddrNL[addr]


        if login:
            id=self.MembersMeeting[userName]
            admin=self.gmGetAdminOfMeeting(id)

            if admin.lower()==userName.lower():
                self.MeetingAuthReq[id]=info['value']
                self.gmUpdateMembersOfMeeting(id,'kr13',info['value'])
        else:
            data=self.cRequest('1111',wType)
            send.send_message(data)

    def gmUpdateMembersOfMeeting(self,id,code,value='0',wType='gmInfoUpdate'):
        members=self.MeetingMembers[id]
        dType='GroupMeet'

        for i in members:
            if members[i]!='a':
                send=self.getSendOfUser(i)

                if send is not None:
                    data=ad.assValue(['wType','code','value'],[wType,code,value],dType)
                    send.send_message(data)

    def gmUpdateOCamCont(self,info,addr):

        dType='GroupMeet'
        wType=info['wType']

        send=self.userAddrSR[addr][0]

        userName,login=self.userAddrNL[addr]


        if login:
            pass
        else:
            data=self.cRequest('1111',wType)
            send.send_message(data)

    def gmUpdateOMicCont(self,info,addr):

        dType='GroupMeet'
        wType=info['wType']

        send=self.userAddrSR[addr][0]

        userName,login=self.userAddrNL[addr]


        if login:
            pass
        else:
            data=self.cRequest('1111',wType)
            send.send_message(data)

    def gmUpdateUCamCont(self,info,addr):

        dType='GroupMeet'
        wType=info['wType']

        send=self.userAddrSR[addr][0]

        userName,login=self.userAddrNL[addr]


        if login:
            user=info['userName']
            typ='img'
            value=info['value']
            id=self.MembersMeeting[userName]

            self.MeetingContData[id][userName][user][typ]=value

        else:
            data=self.cRequest('1111',wType)
            send.send_message(data)

    def gmUpdateUMicCont(self,info,addr):

        dType='GroupMeet'
        wType=info['wType']

        send=self.userAddrSR[addr][0]

        userName,login=self.userAddrNL[addr]


        if login:
            user=info['userName']
            typ='aud'
            value=info['value']
            id=self.MembersMeeting[userName]

            self.MeetingContData[id][userName][user][typ]=value

        else:
            data=self.cRequest('1111',wType)
            send.send_message(data)

    def gmUpdateYourSendCont(self,info,addr):

        dType='GroupMeet'
        wType=info['wType']

        send=self.userAddrSR[addr][0]

        userName,login=self.userAddrNL[addr]


        if login:
            if userName in self.MembersMeeting:
                id=self.MembersMeeting[userName]
                typ=info['type']
                value=info['value']
                if id in self.MeetingSendCont:
                    self.MeetingSendCont[id][userName][typ]=value
                else:
                    print(id ,' Not Avalable')

        else:
            data=self.cRequest('1111',wType)
            send.send_message(data)

    def gmDataControlling(self,userName,info,typ='aud'):
        wS='_Sound'
        wC='_Camera'
        if typ=='aud':
            data=info['data']
            if data !='@none':
                members=self.gmSetRecievingList(userName)

                for i in members:
                    send=self.getSendOfUser(i)
                    if send is not None:
                        data==self.dataContainer[userName.lower()][wS]
                        data=ad.assValue(['wType','code','data','userName']
                                         ,['gmAudData','aud1',data,userName],'GroupMeet')
                        send.send_message(data)

        elif typ=='img':
            data=info['data']
            if data !='@none':

                members=self.gmSetRecievingList(userName,'img')
                for i in members:
                    send=self.getSendOfUser(i)
                    if send is not None:
                        data=self.dataContainer[userName.lower()][wC]
                        data=self.reFormatResolution(data,i,'rCameraRes')
                        data=ad.assValue(['wType','code','data','type','shape','userName'],
                                         ['gmImgData','img1',data[0],data[1],data[2],userName],'GroupMeet')
                        send.send_message(data)
        else:
            print("UNKNOWN TYP TYPE",typ)

    def gmGetMembersOfMeeting(self,id):
        if id in self.MeetingMembers:
            members=self.MeetingMembers[id]
            mem=[]

            for i in members:
                mem.append(i)

            return mem
        else:
            return []

    def gmSetRecievingList(self,userName,typ='aud'):
        if userName in self.MembersMeeting:
            id=self.MembersMeeting[userName]
            mem=self.gmGetMembersOfMeeting(id)
            m=[]
            for i in mem:
                if i.lower()==userName.lower():
                    continue
                cont=self.gmGetRecievingControl(i,userName)
                cond=cont[typ]
                if cond=='1':
                    m.append(i)

            return m
        else:
            return []

    def gmGetSendingControl(self,userName):
        id=self.MembersMeeting[userName]
        data=self.MeetingSendCont[id][userName]

        return data

    def gmGetRecievingControl(self,userName1,userName2):
        id=self.MembersMeeting[userName1]
        data=self.MeetingContData[id][userName1][userName2]

        return data

    def gmOnGoingOffline(self,userName):
        wType='gmLeaveMeeting'
        dType='GroupMeet'

        if userName in self.MembersMeeting:
            id=self.MembersMeeting[userName]
            admin=self.gmGetAdminOfMeeting(id)
            if admin is not None:
                if admin.lower()==userName.lower():
                    data=ad.assValue(['wType','code','GpStatus','userName'],
                                         [wType,'aa00','mend',userName],dType)
                    sender=self.gmAdminLeftMeeting(id)
                    for i in sender:
                        if i is not None:
                            i.send_message(data)
                    del self.MeetingId[id]
                    del self.MeetingMembers[id]
                    del self.MeetingContData[id]
                    del self.MembersMeeting[userName]
                    del self.MeetingLock[id]
                    del self.MeetingAuthReq[id]
                    del self.MeetingSendCont[id]
                else:
                    data=ad.assValue(['wType','code','GpStatus','userName']
                                         ,[wType,'mm00','mend',userName],dType)
                    sender=self.gmMemberLeftMeeting(userName,id)
                    for i in sender:
                        if i is not None:
                            i.send_message(data)

                    del self.MeetingMembers[id][userName]
                    del self.MeetingContData[id][userName]
                    del self.MembersMeeting[userName]

    #---------------------Information_Getter-------------------

    def iGGetInformation(self,info,addr):
        dType='InfoGetter'
        wType='iGGetInformation'


        send=self.userAddrSR[addr][0]


        userName,login=self.userAddrNL[addr]
        cb,cursor,mydb=self.getNewCbForDataBase()


        if login:
            type=info['type']
            tableName='information'
            data=cb.selectAllDataByCondition(tableName,'userName',userName)
            data=ms.modifySqlResult(data)[0]


            data=ad.assValue(['wType','code','type','notification','friendRequest','groupRequest'],
                             [wType,'U53e',type,data[1],data[2],data[3]],dType)
            send.send_message(data)

        else:
            data=self.cRequest('1111',wType)
            send.send_message(data)

    def iGGetInfoC(self,info,addr):
        dType='InfoGetter'
        wType='iGGetInfoC'


        send=self.userAddrSR[addr][0]


        userName,login=self.userAddrNL[addr]
        cb,cursor,mydb=self.getNewCbForDataBase()


        if login:
            tableName='infoc_'+userName

            data=cb.selectAllData(tableName)
            data=ms.modifySqlResult(data)

            ddata=ds.prepSend(data)

            data=ad.assValue(['wType','code','data','dataType','dataShape'],
                             [wType,'45f6']+ddata,dType)


            send.send_message(data)
        else:
            data=self.cRequest('1111',wType)
            send.send_message(data)

    def iGGetInfoG(self,info,addr):
        dType='InfoGetter'
        wType='iGGetInfoG'


        send=self.userAddrSR[addr][0]


        userName,login=self.userAddrNL[addr]
        cb,cursor,mydb=self.getNewCbForDataBase()


        if login:
            tableName='infog_'+userName

            data=cb.selectAllData(tableName)
            data=ms.modifySqlResult(data)

            ddata=ds.prepSend(data)

            data=ad.assValue(['wType','code','data','dataType','dataShape'],
                             [wType,'45t6']+ddata,dType)


            send.send_message(data)
        else:
            data=self.cRequest('1111',wType)
            send.send_message(data)

    #---------------------------About and Check Version---------------

    def ySendFeedback(self,info,addr):


        dType='feedback'
        wType=info['wType']

        send=self.userAddrSR[addr][0]

        userName,login=self.userAddrNL[addr]


        if login:
            feedback=info['feedback']

            cb,cursor,mydb=self.getNewCbForDataBase()

            cb.insertDataN('feedback',[userName,feedback])
            mydb.commit()

            data=self.cRequest('56gt',wType,dType)
            send.send_message(data)

        else:
            data=self.cRequest('1111',wType)
            send.send_message(data)

    def yCheckVersion(self,info,addr):


        dType='About'
        wType=info['wType']

        send=self.userAddrSR[addr][0]

        userName,login=self.userAddrNL[addr]


        if login:
            version=info['version']

            if version==self.clientVersion:
                data=ad.assValue(['wType','code'],[wType,'4fgr'],dType)
            else:

                data=ad.assValue(['wType','code','version','link'],
                                 [wType,'hfgr',self.clientVersion,self.versionLink],dType)
            send.send_message(data)

        else:
            data=self.cRequest('1111',wType)
            send.send_message(data)

    def updateDataRFController(self,info,addr):
        dType='ControlPanel'
        wType=info['wType']

        send=self.userAddrSR[addr][0]

        userName,login=self.userAddrNL[addr]


        if login:


            cb,cursor,mydb=self.getNewCbForDataBase()
            xinfo=xdb.XprtInfo(cursor)
            col=cb.getColName('dataRFController')
            data=info['data']
            data=ds.dec(data)
            data=ast.literal_eval(data)
            tdata=data


            for i in range(len(col)-1):
                xinfo.updateDataRFController(userName,str(col[i+1]),str(data[i]))


            data=self.cRequest('56gt',wType,dType)
            send.send_message(data)
            mydb.commit()

            col=['userName']+col[1:]
            tdata=[userName]+tdata

            self.prepareDataRFController(col,tdata)


        else:
            data=self.cRequest('1111',wType)
            send.send_message(data)

    def loadDataRFController(self,info,addr):
        dType='ControlPanel'
        wType=info['wType']

        send=self.userAddrSR[addr][0]

        userName,login=self.userAddrNL[addr]


        if login:


            cb,cursor,mydb=self.getNewCbForDataBase()

            data=cb.selectAllDataByCondition('dataRFController','userName',userName)
            data=ms.modifySqlResult(data)[0][1:]
            data=ds.enc(str(data))

            whoAsked=info['whoAsked']

            data=ad.assValue(['wType','whoAsked','code','data'],
                             [wType,whoAsked,'43k5',data],dType)
            send.send_message(data)





        else:
            data=self.cRequest('1111',wType)
            send.send_message(data)


s=Server()
s.startServer(HOST)
