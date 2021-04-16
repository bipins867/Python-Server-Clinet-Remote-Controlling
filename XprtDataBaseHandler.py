import dbquery2 as db
#This is XprtDataBaseHandler
#XprtDataHandler
mydb=db.genMdb()

class DataHandler:

    def __init__(self):
        self.cursor=mydb.cursor()

    

    def dropAndCreate(self):

        self.cursor.execute('drop database _xprtinfo')
        self.cursor.execute('create database _xprtinfo')

    def createAll(self):
        cursor=self.cursor
        cb=db.cb1(cursor,'_xprtinfo')

        t1='create table groupchat ( groupname varchar(50),members varchar(10))'
        t2='create table sequrity (userName varchar(50),seqQ text,name text,seqA text,userPass text)'
        t3='create table usergrouplist (user varchar(50),rRecv blob,recvType varchar(50),recvShape varchar(50),\
            rSent blob,rsentType varchar(50), rsentShape varchar(50),gName blob,gNameType varchar(50),\
            gNameShape varchar(50))'
        t4='create table Information (userName varchar(50),notification varchar(10),\
    		friendRequest varchar(10),GroupRequest varchar(10))'
        
        t5='create table profile(userName varchar(40),name\
    	 varchar(40),locProfilePic text,identityU text,gender varchar(10),\
    	 contactNo varchar(20),email varchar(100),dateOfBirth varchar(20),\
    	 discription Text,hideProfile varchar(10))'
        t6='create table feedback(userName varchar(30),feedback text)'

        t7='create table DataRFController(userName varchar(30),sCameraRes varchar(30),sScreenRes varchar(30),\
            sCameraFps varchar(30),sScreenFps varchar(30),rCameraRes varchar(30), rScreenRes varchar(30),\
            sendFileBuff varchar(30),recvDataBuff varchar(30),recvFileBuff varchar(30))'
        
        cursor.execute(t1)
        cursor.execute(t2)
        #cursor.execute(t3)
        cursor.execute(t4)
        cursor.execute(t5)
        cursor.execute(t6)
        cursor.execute(t7)

d=DataHandler()
