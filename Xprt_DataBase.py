# DataBase Xprt

import dbquery2 as db
import myStringLib as ms


class XprtInfo:

    def __init__(self,mycursor):

        self.mycursor=mycursor

        #self.mycursor.execute('use xprtinfo')

        self.cb=db.cb1(self.mycursor,'_xprtinfo')

    def insertHelp(self,type,value):
        cond=self.cb.checkData('_help','_type',type)
        if not cond:
            self.cb.insertDataN('_help',[type,value])
    def insertUser(self,userName):
        values=self.cb.countValues('user')

        if values=='0' or values=='None' or values=='':
            values='1'

        values=str(int(values)+1)

        self.cb.insertDataN('user',[values,userName])

    def insertSequrity(self,values):
        self.cb.insertDataN('sequrity',values)

    def insertProfile(self,userName,name,profilePic):
        self.cb.insertDataN('profile',[userName,name,profilePic])
        


    def insertBlockList(self,value):
        self.cb.insertDataN('blocklist',value)

    def insertInfoList(self,value):
        self.cb.insertDataN('infolist',value)


    def selectHelp(self,type):
        data=self.cb.selectAllDataByCondition('_help','_type',type)
        return data

    def selectSequrity(self,userName):
        return self.cb.selectAllDataByCondition('sequrity','username',userName)

    def selectProfile(self,userName):
        return self.cb.selectAllDataByCondition('profile','username',userName)



    def selectBlockList(self):
        return self.cb.selectAllData('sequrity')

    def selectInfoList(self,userName):
        return self.cb.selectAllDataByCondition('infolist','username',userName)

    def deleteAllRecords(self):
        self.cb.deleteData('blocklist')
        self.cb.deleteData('infolist')

        self.cb.deleteData('profile')
        self.cb.deleteData('sequrity')
        #self.cb.deleteData('user')

        cb=db.cb1(self.mycursor,'xprtnot')
        cb.dropAllTables()


    def deleteUserRecords(self,userName):
        self.cb.deleteBySingleCond('blocklist','userName',userName)
        self.cb.deleteBySingleCond('infolist','userName',userName)

        self.cb.deleteBySingleCond('profile','userName',userName)
        self.cb.deleteBySingleCond('sequrity','userName',userName)
        self.cb.deleteBySingleCond('user','userName',userName)




    def deleteHelp(self,type):
        self.cb.deleteBySingleCond('_help','_type',type)

    def deleteUser(self,userName):
        self.cb.deleteBySingleCond('user','userName',userName)

    def deleteSequrity(self,userName):
        self.cb.deleteBySingleCond('sequrity','username',userName)
        
    def deleteProfile(self,userName):
        self.cb.deleteBySingleCond('profile','username',userName)



    def deleteBlockList(self,userName):
        self.cb.deleteBySingleCond('blocklist','userName',userName)
        
    def deleteInfoList(self,userName):
        self.cb.deleteBySingleCond('infolist','userName',userName)


    def updateSequrity(self,userName,field,value):
        self.cb.updateParticularData('sequrity','userName',field,userName,value)

    def updateProfile(self,userName,field,value):
        self.cb.updateParticularData('profile','userName',field,userName,value)




    def updateInfoList(self,userName,field,value):
        self.cb.updateParticularData('infolist','userName',field,userName,value)


class XprtNot:

    def __init__(self,mycursor):

        self.mycursor=mycursor

        #self.mycursor.execute('use xprtnot')

        self.cb=db.cb1(self.mycursor,'xprtnot')


    def createNotification(self,userName):
        self.cb.createTable('N_'+userName,['sno','notifications'],[40,500])

    def createChat(self,userName1,userName2):
        self.cb.createTable('C_'+userName1+'_'+userName2,['sno','chats'],[40,1000])
        
    def createBlock(self,userName):
        self.cb.createTable('B_'+userName,['sno','userName'],[40,40])
        
    def createFriendRSent(self,userName):
        self.cb.createTable('FS_'+userName,['sno','userName'],[40,40])
        
    def createFriendRRecv(self,userName):
        self.cb.createTable('FR_'+userName,['sno','userName'],[40,40])
        
    def createFriend(self,userName):
        self.cb.createTable('F_'+userName,\
                            ['sno','userName','_sScreen','_sCamera','_sVoice','_sMouse','_sKeyboard',\
                             '_rScreen','_rCamera','_rVoice','_rMouse','_rKeyboard']\
                            ,[40,500,40,40,40,40,40,40,40,40,40,40])
    
    

    def insertNotification(self,userName,notifications):
        values=self.cb.countValues('N_'+userName)

        if values=='0' or values=='None' or values=='':
            values='1'

        values=str(int(values)+1)

        self.cb.insertDataN('N_'+userName,[values,notifications])
        
        

    def insertChat(self,userName1,userName2,chats):
        tName='C_'+userName1+'_'+userName2
        
        values=self.cb.countValues(tName)

        if values=='0' or values=='None' or values=='':
            values='1'

        values=str(int(values)+1)

        self.cb.insertDataN(tName,[values,chats])
        
        
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

        #if int(count)>=int(rangeOut):
            #data=self.cb.selectRangeData(tName,'sno',rangeIn,rangeOut,'notifications')
            data=self.cb.selectFieldData(tName,'notifications')

            data=ms.modifySqlResult(data)

            return data

    def selectChat(self,userName1,userName2,rangeIn,rangeOut):

        tName='C_'+userName1+'_'+userName2
        count=self.cb.countValues(tName)

        if int(count)>=int(rangeOut):
            data=self.cb.selectRangeData(tName,'sno',rangeIn,rangeOut,'notifications')
            data=ms.modifySqlResult(data)

            return data

    def deleteNotification(self,userName):
        tName='N_'+userName
        self.cb.deleteData(tName)

    def deleteChat(self,userName):
        tName='C_'+userName
        self.cb.deleteData(tName)

    def deleteBlock(self,userName,userNameB):
        tName='B_'+userName
        self.cb.deleteBySingleCond(tName,'userName',userNameB)

    def deleteFriendRSent(self,userName,userNameB):
        tName='FS_'+userName
        self.cb.deleteBySingleCond(tName,'userName',userNameB)

    def deleteFriendRRecv(self,userName,userNameB):
        tName='FR_'+userName
        self.cb.deleteBySingleCond(tName,'userName',userNameB)

    def deleteFriend(self,userName,userNameB):
        tName='F_'+userName
        self.cb.deleteBySingleCond(tName,'userName',userNameB)

    
    def updateFriend(self,userName,userNameB,field,value):
        tName='F_'+userName
        self.cb.updateParticularData(tName,'userName',field,userNameB,value)
 
