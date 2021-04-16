

import dbquery2 as db
import myStringLib as ms
import os

location='C:\\XprtDataBase\\'

class XprtInfo:

    def __init__(self,mycursor):

        self.mycursor=mycursor
        self.cb=db.cb1(self.mycursor,'_xprtinfo')

    def change2Dict(self,tName,data):
    	cols=self.cb.getColName(tName)
    	cols=ms.modifySqlResult(cols)

    	data=ad.cvtArr2Dict(cols,data)
    	return data

    def createSequrity(self):
    	self.mycursor.execute('create table sequrity (userName varchar(50),seqQ text,name text,seqA text,userPass text)');

    def createProfile(self):
    	self.mycursor.execute('create table profile(userName varchar(40),name\
    	 varchar(40),locProfilePic text,identityU text,gender varchar(10),\
    	 contactNo varchar(20),email varchar(100),dateOfBirth varchar(20),\
    	 discription Text)');

    def createGroupChat(self):

        self.mycursor.execute('create table GroupChat (groupName varchar(50), members varchar(10))')


    def createGroupMemberList(self):
        self.mycursor.execute('create table GroupMemberList(userName varchar(50), groupList blob)')

    def createGroupMemberListSent(self):
        self.mycursor.execute('create table GroupMemberListSent(userName varchar(50), groupList blob)')

    def createGroupMemberListRecv(self):
        self.mycursor.execute('create table GroupMemberListRecv(userName varchar(50), groupList blob)')

    def createUserGroupList(self):
        self.mycursor.execute("create table usergrouplist(user varchar(50),rRecv blob,recvType varchar(50), recvShape varchar(50),rSent blob,rsentType varchar(50),rsentShape varchar(50),gName blob,gNameType varchar(50),gNameShape varchar(50))")


    def getSomeProfile(self,userName):
        data=self.cb.selectFieldByCond('profile',['userName','name','locProfilePic'],['userName'],[userName])
        data=ms.modifySqlResult(data)
        return data


    def createInformation(self):
    	self.mycursor.execute('create table Information (userName varchar(50),notifN varchar(10),\
    		notifUS varchar(10),FRN varchar(10),FRUS varchar(10))');

    def insertSequrity(self,values):
        self.cb.insertDataN('sequrity',values)

    def insertProfile(self,values):
        self.cb.insertDataN('profile',values)

    def insertDataRFController(self,values):
        self.cb.insertDataN('DataRFController',values)

    def insertInformation(self,values):
    	self.cb.insertDataN('Information',values)
        


    def insertGroupChat(self,values):
        self.cb.insertDataN('GroupChat',values)
    

    def selectSequrity(self,userName):
        return self.cb.selectAllDataByCondition('sequrity','username',userName)

    def selectProfile(self,userName):
        return self.cb.selectAllDataByCondition('profile','username',userName)

    def selectInformation(self,userName):
    	return self.cb.selectAllDataByCondition('Information','userName',userName)
    

    def deleteUserRecords(self,userName):
 

        self.deleteSequrity(userName)
        self.deleteProfile(userName)
        self.deleteInformation(userName)     



    def deleteSequrity(self,userName):
        self.cb.deleteBySingleCond('sequrity','username',userName)
        
    def deleteProfile(self,userName):
        self.cb.deleteBySingleCond('profile','username',userName)

    def deleteInformation(self,userName):
    	self.cb.deleteBySingleCond('Information','userName',userName)


    def updateSequrity(self,userName,field,value):
        self.cb.updateParticularData('sequrity','userName',field,userName,value)

    def updateProfile(self,userName,field,value):
        self.cb.updateParticularData('profile','userName',field,userName,value)

    def updateInformation(self,userName,field,value):
    	self.cb.updateParticularData('Information','userName',field,userName,value)

    def updateGroupChat(self,groupName,value):
        self.cb.updateParticularData('GroupChat','groupName','members',groupName,value)

    def updateDataRFController(self,userName,field,value):
        self.cb.updateParticularData('DataRFController','userName',field,userName,value)


class XprtNot:

    def __init__(self,mycursor):

        self.mycursor=mycursor
        self.cb=db.cb1(self.mycursor,'_xprtinfo')

    def change2Dict(self,tName,data):
    	cols=self.cb.getColName(tName)
    	cols=ms.modifySqlResult(cols)

    	data=ad.cvtArr2Dict(cols,data)
    	return data

    def createNotification(self,userName):
        self.cb.createTable('N_'+userName,['sno','notifications'],[40,500])

    def createInfoC(self,userName):
        self.cb.createTable('infoC_'+userName,['userName','chat'],[40,40])
        

    def createInfoG(self,userName):
        self.cb.createTable('infoG_'+userName,['groupName','ControlPanel','chat'],[40,40,40])
        
    def createChat(self,userName1,userName2):
        self.cb.createTable('C_'+userName1+'_'+userName2,['sno','chats'],[40,1000])



    def createInfoChat(self,userName1):
    	self.cb.createTable('IC_'+userName1,['userName','ChatN','ChatUS'],[40,10,10])
        
    def createBlock(self,userName):
        self.cb.createTable('B_'+userName,['sno','userName'],[40,40])
        
    def createFriendRSent(self,userName):
        self.cb.createTable('FS_'+userName,['sno','userName'],[40,40])

    def createGroupRSent(self,groupName):
        self.cb.createTable('gs_'+groupName,['sno','userName'],[40,40])
        
    def createFriendRRecv(self,userName):
        self.cb.createTable('FR_'+userName,['sno','userName'],[40,40])

    def createGroupRRecv(self,groupName):
        self.cb.createTable('gr_'+groupName,['sno','userName'],[40,40])

    def createFriend(self,userName):
        self.cb.createTable('F_'+userName,\
                            ['sno','userName','_sScreen','_sCamera','_sVoice','_sMouse','_sKeyboard',\
                             '_rScreen','_rCamera','_rVoice','_rMouse','_rKeyboard']\
                            ,[40,500,40,40,40,40,40,40,40,40,40,40])

    def createGroupMembers(self,groupName):
        self.cb.createTable('g_'+groupName,['sno','userName','type'],[40,40,10])


    def createUserGroupInfoHolder(self,userName):
        self.cb.createTable('ug_'+userName,['sno','groupName'],[40,40])
        self.cb.createTable('ugr_'+userName,['sno','groupName'],[40,40])
        self.cb.createTable('ugs_'+userName,['sno','groupName'],[40,40])


    def createChatGroupChat(self,groupName):
        self.cb.createTable('gc_'+groupName,['sno','chats'],[40,1000])


    def checkBlock(self,userName1,userName2):
        tName='B_'+userName1
        cond=self.cb.checkData(tName,'userName',userName2)

        return cond
    

    def insertNotification(self,userName,notifications):
        values=self.cb.countValues('N_'+userName)

        if values=='0' or values=='None' or values=='':
            values='1'

        values=str(int(values)+1)


        self.cb.insertDataN('N_'+userName,[values,notifications])
        self.cb.updateParticularData('Information','userName','notification'
                                     ,userName,'False')

        

    def insertInfoC(self,userName,fuserName):
        tableName=f'infoc_{userName}'

        self.cb.insertDataN(tableName,[fuserName,"False"])

    def insertInfoG(self,userName,groupName):
        tableName=f'infog_{userName}'

        self.cb.insertDataN(tableName,[groupName,"False","False"])


    def insertChat(self,userName1,userName2,chats):
        tName='C_'+userName1+'_'+userName2
        
        values=self.cb.countValues(tName)

        if values=='0' or values=='None' or values=='':
            values='1'

        values=str(int(values)+1)

        self.cb.insertDataN(tName,[values,chats])

    def insertChatGroupChat(self,groupName,chats):
        tName='gC_'+groupName

        values=self.cb.countValues(tName)

        if values=='0' or values=='None' or values=='':
            values='1'

        values=str(int(values)+1)

        self.cb.insertDataN(tName,[values,chats])

    def insertInfoChat(self,userName1,userName2):
    	tName='IC_'+userName1
    	self.cb.insertDataN(tName,[userName2,'0','0'])
        
    def insertBlock(self,userName,blocklist):
        tName='B_'+userName
        
        values=self.cb.countValues(tName)

        if values=='0' or values=='None' or values=='':
            values='1'

        values=str(int(values)+1)

        self.cb.insertDataN(tName,[values,blocklist])
        

    def insertFriendRSent(self,userName,friend):
        tName='FS_'+userName
        
        values=self.cb.countValues(tName)

        if values=='0' or values=='None' or values=='':
            values='1'

        values=str(int(values)+1)

        self.cb.insertDataN(tName,[values,friend])


    def insertFriendRRecv(self,userName,friend):
        tName='FR_'+userName
        
        values=self.cb.countValues(tName)

        if values=='0' or values=='None' or values=='':
            values='1'

        values=str(int(values)+1)

        self.cb.insertDataN(tName,[values,friend])
        self.cb.updateParticularData('Information','userName','friendRequest'
                                     ,userName,'False')


    def insertFriend(self,userName,friend):
        tName='F_'+userName
        
        values=self.cb.countValues(tName)
        tf=['0','0','0','0','0','0','0','0','0','0']
        if values=='0' or values=='None' or values=='':
            values='1'

        values=str(int(values)+1)

        self.cb.insertDataN(tName,[values,friend]+tf)


    def selectFriendRequest(self,userName):
        tName='FR_'+userName
        data=self.cb.selectFieldData(tName,'userName')
        data=ms.modifySqlResult(data)

        return data

    def selectBlock(self,userName):
        tName='B_'+userName
        data=self.cb.selectFieldData(tName,'userName')
        data=ms.modifySqlResult(data)

        return data

    def selectNotification(self,userName,rangeIn,rangeOut):

        tName='N_'+userName
        count=self.cb.countValues(tName)

        


    def selectChat(self,userName1,userName2,rangeIn,rangeOut):

        tName='C_'+userName1+'_'+userName2
        count=self.cb.countValues(tName)

    def selectChatGroupChat(self,groupName):
        pass

    def selectInfoChat(self,userName1,userName2):
    	tName='IC_'+userName1

    	data=self.cb.selectAllDataByCondition(tName,'userName',userName2)
    	return data

    def deleteNotification(self,userName):
        tName='N_'+userName
        self.cb.deleteData(tName)

    def deleteChat(self,userName1,userName2):
        tName='C_'+userName1+'_'+userName2
        self.cb.deleteData(tName)

    def deleteInfoChat(self,userName1):
    	tName='IC_'+userName1
    	self.cb.deleteData(tName)

    def deleteBlock(self,userName,userNameB):
        tName='B_'+userName
        self.cb.deleteBySingleCond(tName,'userName',userNameB)

    def deleteFriendRSent(self,userName,userNameB):
        tName='FS_'+userName
        self.cb.deleteBySingleCond(tName,'userName',userNameB)



    def deleteInfoC(self,userName,fuserName):
        tableName=f'infoc_{userName}'

        self.cb.deleteBySingleCond(tableName,'userName',fuserName)

    def deleteInfoG(self,userName,groupName):
        tableName=f'infog_{userName}'

        self.cb.deleteBySingleCond(tableName,'groupName',groupName)


    def deleteFriendRRecv(self,userName,userNameB):
        tName='FR_'+userName
        self.cb.deleteBySingleCond(tName,'userName',userNameB)

    def deleteFriend(self,userName,userNameB):
        tName='F_'+userName
        self.cb.deleteBySingleCond(tName,'userName',userNameB)




    def deleteInfoC(self,userName,fuserName):
        tableName=f'infoc_{userName}'

        self.cb.deleteBySingleCond(tableName,'userName',fuserName)

    def deleteInfoG(self,userName,groupName):
        tableName=f'infog_{userName}'

        self.cb.deleteBySingleCond(tableName,'groupName',groupName)



    
    def updateFriend(self,userName,userNameB,field,value):
        tName='F_'+userName
        self.cb.updateParticularData(tName,'userName',field,userNameB,value)

    def updateInfoChat(self,userName1,userName2,totalC,totalUS):
    	tName='IC_'+userName1
    	self.cb.updateParticularData(tName,'userName','ChatN',userName2,totalIC)
    	self.cb.updateParticularData(tName,'userName','ChatUS',userName2,totalUS)
 


    def updateInfoCC(self,userName,fuserName,value='True'):
        tableName=f'infoc_{userName}'

        self.cb.updateParticularData(tableName,'userName','chat',fuserName,value)

    def updateInfoGCP(self,userName,groupName,value='True'):
        tableName=f'infog_{userName}'

        self.cb.updateParticularData(tableName,'groupName','ControlPanel',groupName,value)

    def updateInfoGC(self,userName,groupName,value='True'):
        tableName=f'infog_{userName}'

        self.cb.updateParticularData(tableName,'groupName','Chat',groupName,value)
