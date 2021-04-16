#XprtClientScript
import ControlUnit as cu 
import dbquery2 as db
import AssembleData as ad 
import TestingDataSharePh1 as ds
import myStringLib as ms 
import sys
import threading
import cv2

#import XprtClient

class Client:

	def __init__(self):
		print("Client is activated")
		self.s=None

	def connect(self,address='localhost',port=9898,serverError=None,loc=''):
		s=cu.client_connect(address,port)
		self.s=s
		if s is not  None:
			self.send=ds.Send(s)
			self.recv=ds.Recv(s,loc)
			self.recv.function=self.handleMessage
			self.recv.get()
			self.functionList={}
			self.userName=None
		else:
			if serverError is not None:
				serverError(address,port)

	def handleFunResult(self,info):
		wType=info['wType']

		fun=self.functionList[wType]
		if fun is not None:
			fun(info)

	def handleFunResult2(self,info):
		wType=str(1)+info['wType']
		userName=info['userName']


		wType=userName.lower()+wType

		if wType in self.functionList:

			fun=self.functionList[wType]
			if fun is not None:
				fun(info)


	def handleWhoRequestedResult(self,info):
		whoRequested=info['whoRequested']
		fun=self.functionList[whoRequested]
		if fun is not None:
			fun(info)

	def handleData(self,info):
		wType=info['wType']

		ty=['_Sound','_Screen','_Camera','_IntSound','_Keyboard','_Mouse']
		wT=['DownloadFile','CancelDownloadFile']
		if wType in ty:
			fuserName=info['userName']
			wName=fuserName.lower()+info['wType']


		elif wType in wT:
			fuserName=info['fuserName']

			if wType=='DownloadFile':
				wName=fuserName+'-DownloadFileChat'
			elif wType=='CancelDownloadFile':
				wName=fuserName+'-CancelDownloadFileChat'
			else:
				wName='i dont know '

			cf=info['cf']

			if cf=='0':
				wName='g-'+wName
			else:
				wName='c-'+wName



		else:
			fuserName=info['fuserName']
			wName=fuserName.lower()+info['wType']



		fun=self.functionList[wName]
		if fun is not None:
			fun(info)

	def handleMessage(self,msg):
		dtype,info=ad.deAssValue(msg,dicts=True)

		if dtype=='specialDType':
			print("I AM HANDLING REQUEST")
			self.handleFunResult(info)

		elif dtype=='_Response':
			if 'whoRequested' in msg:
				self.handleWhoRequestedResult(info)
			else:

				self.handleFunResult(info)
		elif dtype=='request':

			self.handleFunResult(info)
		elif dtype=='_data':
			self.handleData(info)

		elif dtype=='DataRequest':
			if info['dataType']=='upload':

			    self.handleUploadResume(info)
			else:
			    pass

		elif dtype=='GroupChat':

			a=[]
			a.append('viewGroupProfile')



			wType=info['wType']

			if wType in a:
				self.handleFunResult(info)
			else:
				self.handleByDtype(dtype,info)

		elif dtype=='GroupMeet':
			ar=['gmCreateMeeting','gmJoinMeeting']

			wType=info['wType']
			if wType in ar:
				self.handleFunResult(info)
			else:

				self.handleByDtype(dtype,info)

		elif dtype=='Sequrity':
			self.handleFunResult(info)

		elif dtype=='InfoGetter':
			wType=info['wType']

			if wType=='iGGetInformation':
				type=info['type']
				if type=='global':
					self.handleByDtype(dtype,info)
				else:
					fun=self.functionList['Local'+wType]
					fun(info)
			elif wType=='iGGetInfoC':
				self.handleByDtype(dtype,info)
			elif wType=='iGGetInfoG':
				fun=self.functionList['Local'+wType]
				fun(info)
			else:
				print("UNKONW INFORMATION ERROR ",wType)


		elif dtype=='About':
			self.handleByDtype(dtype,info)
		elif dtype=='feedback':
			self.handleByDtype(dtype,info)

		elif dtype=='ControlPanel':
			wType=info['wType']
			if wType=='updateDataRFController':
				self.handleFunResult(info)
			elif wType=='loadDataRFController':
				whoAsked=info['whoAsked']
				ats=whoAsked+wType
				if ats in self.functionList:
					fun=self.functionList[ats]
					fun(info)
			else:
				print("UNKnown Control Panel ",wType)
		else:
			print("IT IS A BLUNDER MISTAKE")
			print("DTYPE ",dtype)

	def handleByDtype(self,dtype,info):

		fun=self.functionList[dtype]
		fun(info)

	def handleUploadResume(self,info):
            userName=info['userName']
            fileName=info['fileName']
            fName=userName+'+'+fileName
            try:
                print(fName)
                print(self.functionList)
                fun=self.functionList[fName]
                if fun is not None:
                    fun(info)
            except:
                print("Error in finding the function")
	def initCheckVersion(self,version):
		dType='sequrity'
		wType='initCheckVersion'

		data=ad.assValue(['wType','version'],[wType,version],dType)
		self.send.send_message(data)

	def updateDataRFController(self,valuesArray):
		dType='ControlPanel'
		wType='updateDataRFController'

		data=ds.enc(str(valuesArray))
		data=ad.assValue(['wType','data'],[wType,data],dType)
		self.send.send_message(data)

	def loadDataRFController(self,whoAsked='MainWindow'):
		wType='loadDataRFController'
		dType='ControlPanel'

		data=ad.assValue(['wType','whoAsked'],[wType,whoAsked],dType)
		self.send.send_message(data)

	def login(self,userName,userPass):
		dType='sequrity'
		wType='login'

		data=ad.assValue(['wType','userName','userPass'],[wType,userName,userPass],dType)
		self.send.send_message(data)

	def logOut(self):
		wType='logOut'
		dType='sequrity'

		data=ad.assValue(['wType'],[wType],dType)
		self.send.send_message(data)

	def signUp(self,name,userName,userPass,seqQ,seqA):
		dType='sequrity'
		wType='signUp'
		data=ad.assValue(['wType','userName','userPass','name','seqQ','seqA'],[wType,userName,userPass,name,seqQ,seqA],dType)
		self.send.send_message(data)

	def getSequrityQuestion(self,userName):
		dType='sequrity'
		wType='getSequrityQuestion'


		data=ad.assValue(['wType','userName'],[wType,userName],dType)
		self.send.send_message(data)

	def forgetPassword(self,userName,seqA):
		dType='sequrity'
		wType='forgetPassword'


		data=ad.assValue(['wType','userName','seqA'],[wType,userName,seqA],dType)
		self.send.send_message(data)

	def changePassword(self,userName,oldPassword,newPassword):
		dType='sequrity'
		wType='changePassword'
		data=ad.assValue(['wType','userName','oldPassword','newPassword']\
						 ,[wType,userName,oldPassword,newPassword],dType)

		self.send.send_message(data)

	#------------------------------------------------------

	def updateHideProfile(self,value):
		dType='information'
		wType='updateHideProfile'

		data=ad.assValue(['wType','value'],[wType,str(value)],dType)
		self.send.send_message(data)


	def editProfile(self,ofType,ofTypeVal,locProfilePic=None):
		dType='information'
		wType='editProfile'

		if ofType=='locProfilePic':
			data=cv2.imread(locProfilePic)
			if data is not None:
				data=cv2.resize(data,(120,140))
				data=ds.prepareImageFormat(data)

				data=ad.assValue(['wType','ofType','ofTypeVal','profileData','profileType','profileShape']\
								 ,[wType,ofType,'Values',data[0],data[1],data[2]],dType)
				self.send.send_message(data)

		else:
			data=ad.assValue(['wType','ofType','ofTypeVal'],[wType,ofType,ofTypeVal],dType)
			self.send.send_message(data)

	def changeSeqQA(self,seqQ,seqA,userPass):
		dType='information'
		wType='changeSeqQA'

		data=ad.assValue(['wType','seqQ','seqA','userPass'],[wType,seqQ,seqA,userPass],dType)
		self.send.send_message(data)

	def refressSearch(self):
		dType='information'
		wType='refressSearch'

		data=ad.assValue(['wType'],[wType],dType)
		self.send.send_message(data)

	def searchFriend(self,userName,strictS='1'):

		dType='information'
		wType='searchFriend'

		data=ad.assValue(['wType','userName','hs'],[wType,userName,strictS],dType)
		self.send.send_message(data)

	def sendFriendRequest(self,userName):
		dType='information'
		wType='sendFriendRequest'

		data=ad.assValue(['wType','userName'],[wType,userName],dType)
		self.send.send_message(data)

	def unfriend(self,userName):
		dType='information'
		wType='unfriend'

		data=ad.assValue(['wType','userName'],[wType,userName],dType)
		self.send.send_message(data)


	def deleteFriendRequest(self,userName):
		dType='information'
		wType='deleteFriendRequest'

		data=ad.assValue(['wType','userName'],[wType,userName],dType)
		self.send.send_message(data)


	def blockSearch(self,userName):
		dType='information'
		wType='blockSearch'

		data=ad.assValue(['wType','userName'],[wType,userName],dType)
		self.send.send_message(data)


	def block(self,userName):
		dType='information'
		wType='block'

		data=ad.assValue(['wType','userName'],[wType,userName],dType)
		self.send.send_message(data)


	def unblockLoad(self):
		dType='information'
		wType='unblockLoad'

		data=ad.assValue(['wType'],[wType],dType)
		self.send.send_message(data)

	def unblock(self,userName):
		dType='information'
		wType='unblock'

		data=ad.assValue(['wType','userName'],[wType,userName],dType)
		self.send.send_message(data)

	def loadFriendRequest(self):
		dType='information'
		wType='loadFriendRequest'

		data=ad.assValue(['wType','status'],[wType,'load'],dType)
		self.send.send_message(data)

	def friendRequestAccept(self,userName):
		dType='information'
		wType='friendRequestAccept'

		data=ad.assValue(['wType','userName'],[wType,userName],dType)
		self.send.send_message(data)

	def loadNotification(self,r1=0,r2=10):
		dType='system'
		wType='loadNotification'
		status='load'
		data=ad.assValue(['wType','status','r1','r2'],[wType,status,str(r1),str(r2)],dType)
		self.send.send_message(data)

	def loadChat(self,userName,r1=0,r2=10):
		dType='data'
		wType='loadChat'
		status='load'
		data=ad.assValue(['wType','status','r1','r2','fuserName'],[wType,status,str(r1),str(r2),userName],dType)
		self.send.send_message(data)



	def loadUserProfile(self,userName,whoRequested):
		dType='information'
		wType='loadUserProfile'

		data=ad.assValue(['wType','userName','whoRequested'],[wType,userName,whoRequested],dType)
		self.send.send_message(data)

	def friendListLoad(self,userName,whoRequested='_friendListLoad'):
		dType='information'
		wType='friendListLoad'

		data=ad.assValue(['wType','userName','whoRequested'],[wType,userName,whoRequested],dType)
		self.send.send_message(data)

	def loadChatWindow(self,userName,status):
		dType='system'
		wType='loadChatWindow'

		data=ad.assValue(['wType','userName','status'],[wType,userName,status],dType)
		self.send.send_message(data)

	def updateControls(self,userName,conType,conValue):
		#conType
		#conValue
		#userName

		dType='data'
		wType='updateControls'

		data=ad.assValue(['wType','conType','conValue','userName']\
						 ,[wType,conType,conValue,userName],dType)

		self.send.send_message(data)

	def downloadFile(self,fName,fuserName,cf='1'):

		dType='DataRequest'
		wType='DownloadFile'
		data=ad.assValue(['wType','fName','userName','cf'],
						 [wType,fName,fuserName,cf],dType)

		self.send.send_message(data)

	def cancelDownloadFile(self,fName,fuserName,cf='1'):
		dType='DataRequest'
		wType='cancelDownloadFile'

		data=ad.assValue(['wType','fName','userName','cf'],
						 [wType,fName,fuserName,cf],dType)
		self.send.send_message(data)

	def _Text(self,userName,text):
		dType='data'
		wType='_Text'
		data=ad.assValue(['wType','chatText','userName'],[wType,text,userName],dType)
		self.send.send_message(data)

	def _File(self,userName,text,status='start'):
		dType='data'
		wType='_File'
		data=ad.assValue(['wType','chatFile','userName','status'],[wType,text,userName,status],dType)
		self.send.send_message(data)

	def _Screen(self,userName,data,types,shape):
		dType='data'
		wType='_Screen'

		data=ad.assValue(['wType','data','types','shape','userName'],[wType,data,types,shape,userName],dType)
		self.send.send_message(data)

	def _Sound(self,userName,data):
		dType='data'
		wType='_Sound'

		data=ad.assValue(['wType','data','userName'],[wType,data,userName],dType)
		self.send.send_message(data)

	def _IntSound(self,userName,data):
		dType='data'
		wType='_IntSound'

		data=ad.assValue(['wType','data','userName'],[wType,data,userName],dType)
		self.send.send_message(data)

	def _Camera(self,userName,data,types,shape):
		dType='data'
		wType='_Camera'

		data=ad.assValue(['wType','data','types','shape','userName'],[wType,data,types,shape,userName],dType)

		self.send.send_message(data)


	def _Mouse(self,userName,data,types,shape):
		dType='data'
		wType='_Mouse'

		data=ad.assValue(['wType','data','types','shape','userName'],[wType,data,types,shape,userName],dType)
		self.send.send_message(data)

	def _Keyboard(self,userName,data,types,shape):
		dType='data'
		wType='_Keyboard'

		data=ad.assValue(['wType','data','types','shape','userName'],[wType,data,types,shape,userName],dType)
		self.send.send_message(data)

	def rRequest(self,userName,vType):
		dType='request'
		wType='request'

		data=ad.assValue(['wType','userName','vType'],[wType,userName,vType],dType)
		self.send.send_message(data)

	def rResponse(self,userName,vType,vValue):
		dType='request'
		wType='response'

		data=ad.assValue(['wType','userName','vType','vValue'],[wType,userName,vType,vValue],dType)

		self.send.send_message(data)

	def ySendFeedback(self,feedback):
		dType='feedback'
		wType='feedback'
		encF=ds.enc(feedback)

		data=ad.assValue(['wType','feedback'],[wType,encF],dType)
		self.send.send_message(data)

	def yCheckVersion(self,version='1.001'):
		dType='About'
		wType='checkVersion'

		data=ad.assValue(['wType','version'],[wType,version],dType)
		self.send.send_message(data)

class GroupChat:

	def __init__(self,send):
		self.dType='GroupChat'
		self.send=send

	def createGroup(self,groupName):
		wType='createGroup'

		data=ad.assValue(['wType','groupName'],[wType,groupName],self.dType)

		self.send.send_message(data)

	def refressGCSearch(self):
		dType='GroupChat'
		wType='refressGCSearch'

		data=ad.assValue(['wType'],[wType],dType)
		self.send.send_message(data)

	def groupSearchMemberForSRequest(self,userName):
		wType='groupSearchMemberForSRequest'
		data=ad.assValue(['wType','userName'],[wType,userName],self.dType)
		self.send.send_message(data)

	def searchGroup(self,groupName,hs='1'):
		wType='searchGroup'

		data=ad.assValue(['wType','groupName','hs'],[wType,groupName,hs],self.dType)

		self.send.send_message(data)

	def loadGroupInfo(self,groupName,xt=''):
		wType='loadGroupInfo'
		if xt=='':
			xt=wType
		data=ad.assValue(['wType','groupName','xt'],[wType,groupName,xt],self.dType)

		self.send.send_message(data)

	def groupSendRequest(self,userName,groupName):
		wType='groupSendRequest'
		data=ad.assValue(['wType','groupName','userName'],\
						 [wType,groupName,userName],self.dType)

		self.send.send_message(data)

	def sendGroupRequest(self,groupName):
		wType='sendGroupRequest'
		data=ad.assValue(['wType','groupName'],[wType,groupName],self.dType)

		self.send.send_message(data)

	def loadGroupRequest(self,groupName='None',tp='g'):
		wType='loadGroupRequest'
		data=ad.assValue(['wType','groupName','tp'],[wType,groupName,type],self.dType)

		self.send.send_message(data)

	def acceptGroupRequest(self,groupName='None',userName='None',acceptT='1',tp='g'):
		wType='acceptGroupRequest'
		data=ad.assValue(['wType','groupName','userName','tp','acceptT'],\
						 [wType,groupName,userName,tp,acceptT],self.dType)

		self.send.send_message(data)

	def cancelGroupSendRequest(self,groupName='None',userName='None'):
		wType='cancelGroupSendRequest'

		data=ad.assValue(['wType','groupName','userName'],
						 [wType,groupName,userName],self.dType)

		self.send.send_message(data)

	def loadGroupChatInfo(self,groupName):
		wType='loadGroupChatInfo'
		data=ad.assValue(['wType','groupName'],[wType,groupName],self.dType)

		self.send.send_message(data)

	def groupControlPanel(self,groupName):
		wType='groupControlPanel'
		data=ad.assValue(['wType','groupName'],[wType,groupName],self.dType)

		self.send.send_message(data)

	def groupChatWindow(self,groupName):
		wType='groupChatWindow'
		data=ad.assValue(['wType','groupName'],[wType,groupName],self.dType)

		self.send.send_message(data)

	def leaveGroup(self,groupName):
		wType='leaveGroup'
		data=ad.assValue(['wType','groupName'],[wType,groupName],self.dType)

		self.send.send_message(data)

	def sendGroupChat(self,groupName,chat):
		wType='sendGroupChat'
		chat=ds.enc(chat)
		data=ad.assValue(['wType','groupName','chat'],[wType,groupName,chat],self.dType)

		self.send.send_message(data)

	def kickMemberGroupChat(self,groupName,userName):
            wType='kickMemberGroupChat'
            data=ad.assValue(['wType','groupName','userName'],[wType,groupName,userName],self.dType)
            self.send.send_message(data)


	def refressGC(self):
		wType='refressGC'
		data=ad.assValue(['wType'],[wType],self.dType)
		self.send.send_message(data)

class GroupMeet:
	def __init__(self,send):
		self.dType='GroupMeet'
		self.send=send

	def createMeeting(self,name,password):
		wType='gmCreateMeeting'

		data=ad.assValue(['wType','name','password'],[wType,name,password],self.dType)

		self.send.send_message(data)

	def joinMeeting(self,id,password):
		wType='gmJoinMeeting'

		data=ad.assValue(['wType','id','password'],[wType,id,password],self.dType)

		self.send.send_message(data)

	def sendChat(self,chat):
		wType='gmSendChat'
		chat=ds.enc(chat)
		data=ad.assValue(['wType','chat'],[wType,chat],self.dType)
		self.send.send_message(data)

	def kickOut(self,userName):
		wType='gmKickOut'

		data=ad.assValue(['wType','userName'],[wType,userName],self.dType)

		self.send.send_message(data)

	def lockMeeting(self,value='1'):
		wType='gmLockMeeting'
		data=ad.assValue(['wType','value'],[wType,value],self.dType)

		self.send.send_message(data)

	def authRequest(self,value='1'):
		wType='gmAuthRequest'
		data=ad.assValue(['wType','value'],[wType,value],self.dType)

		self.send.send_message(data)

	def sendJoinClientRequestResponse(self,userName,value='1'):
		wType='gmJoinClientRequestResponse'

		data=ad.assValue(['wType','userName','value'],
						 [wType,userName,value],self.dType)

		self.send.send_message(data)

	def gmOnClose(self):
		wType='gmOnClose'

		data=ad.assValue(['wType'],[wType],self.dType)
		self.send.send_message(data)

	def gmUpdateOCamCont(self,value):
		wType='gmUpdateOCamCont'

		data=ad.assValue(['wType','value'],[wType,value],self.dType)
		self.send.send_message(data)

	def gmUpdateOMicCont(self,value):
		wType='gmUpdateOMicCont'

		data=ad.assValue(['wType','value'],[wType,value],self.dType)
		self.send.send_message(data)

	def gmUpdateUCamCont(self,userName,value):
		wType='gmUpdateUCamCont'

		data=ad.assValue(['wType','value','userName'],[wType,value,userName],self.dType)
		self.send.send_message(data)

	def gmUpdateUMicCont(self,userName,value):
		wType='gmUpdateUMicCont'

		data=ad.assValue(['wType','value','userName'],[wType,value,userName],self.dType)
		self.send.send_message(data)

	def gmLeaveMeeting(self):
		wType='gmLeaveMeeting'

		data=ad.assValue(['wType'],[wType],self.dType)
		self.send.send_message(data)

	def gmUpdateYourSendCont(self,typ='img',value='0'):
		wType='gmUpdateYourSendCont'

		data=ad.assValue(['wType','type','value'],[wType,typ,value],self.dType)
		self.send.send_message(data)

class InfoGetter:

	def __init__(self,send):
		self.dType='InfoGetter'
		self.send=send

	def iGGetInformation(self,type='global'):
		wType='iGGetInformation'
		data=ad.assValue(['wType','type'],[wType,type],self.dType)
		self.send.send_message(data)

	def iGGetInfoC(self):
		wType='iGGetInfoC'
		data=ad.assValue(['wType'],[wType],self.dType)
		self.send.send_message(data)

	def iGGetInfoG(self):
		wType='iGGetInfoG'
		data=ad.assValue(['wType'],[wType],self.dType)
		self.send.send_message(data)







#c=Client()
#c.connect()
#c.login("USERNAME","USERPASS")
