import time
import socket
import myStringLib as ms
import ast
import cv2
import ControlUnit as cu
import os
from cryptography.fernet import Fernet
import sys
import numpy as np
import threading
import AssembleData as ad
import TestingDataSharePh1 as ds
import dbquery2 as db
import FileIOManager as fim
import base64 as b6

opFile=fim.OperateFiles()

key=b'eQ5jxFcJNYII5Z4vhBtvT-mNiqx64yQEUln1SOoYEDA='
fernet=Fernet(key)

RECV_CHUNK=1024*8
SEND_CHUNK=1024*512

def strToShape(shape):
    shape=str(shape)

    shape=ms.distributeString(shape,',')
    if(len(shape)==2):
                if shape[1]==')':
                    first=shape[0]
                    first=int(first[1:])
                    shape=(first,)

                else:
                    first=shape[0]
                    second=shape[1]
                    first=int(first[1:])
                    second=int(second[:-1])
                    shape=(first,second)


    else:
                first=0
                last=0
                middle=[]
                first=int(shape[0][1:])
                last=int(shape[-1][:-1])
                for i in range(1,len(shape)-1):
                    s=shape[i]
                    middle.append(int(s[1:]))

                tf=[]
                tf.append(first)
                for i in middle:
                    tf.append(i)

                tf.append(last)
                shape=tuple(tf)
    return shape

def compareShape(shape1,shape2):
    if shape1==shape2:
        return 0
    else:
        a=1
        for i in shape1:
           a=a*i

        b=1
        for i in shape2:
            b=b*i
        if a>b:
            return 1
        else:
            return -1

def compareStrShape(shape1,shape2):
    shape1=str(shape1)
    shape2=str(shape2)

    shape1=ds.strToShape(shape1)
    shape2=ds.strToShape(shape2)

    return ds.compareShape(shape1,shape2)

def enc(data):
    data=bytes(data,'utf-8')
    data=fernet.encrypt(data)
    data=data.decode()
    return data


def dec(data):
    data=bytes(data,'utf-8')
    data=fernet.decrypt(data)
    data=data.decode()
    return data

def encb(data):
    data=fernet.encrypt(data)
    return data

def decb(data):
    data=fernet.decrypt(data)
    return data

def enc(data):
    data=bytes(data,'utf-8')
    data=b6.b64encode(data)
    data=data.decode()
    return data

def dec(data):
    data=bytes(data,'utf-8')
    data=b6.b64decode(data)
    data=data.decode()
    return data

def encb(data):
    data=b6.b64encode(data)
    return data

def decb(data):
    data=b6.b64decode(data)
    return data

def prepareImageFormat(img):
    typ=img.dtype
    shape=img.shape
    c,img=cv2.imencode('*.jpg',img)
    img=ds.encb(img).decode()

    return [img,str(typ),str(shape)]

def reFormatImageData(data):

    data=ds.decb(data)
    data=np.frombuffer(data,'uint8')
    data.shape=(data.shape[0],1)
    data=cv2.imdecode(data,1)
    return data

def prepSend(data,tp=None,sp=None):
        #print(data)


        if data is None:
            data=[]
        tempData=data.copy()
        data=np.array(data)
        types=str(data.dtype)
        shape=str(data.shape)
        if '<U' in types:
            data=str(data.tolist())

            data=ds.enc(data)

        else:
            data=bytes(data)
            data=ds.encb(data)
            data=data.decode()

            if tp is not None:
                types=tp

            if sp is not None:
                shape=sp

        return [data,types,shape]

def remodifyData(data,types,shape,img=False):
    if '<U' in types:
        data=ds.dec(data)
        data=ast.literal_eval(data)
        data=np.array(data)
        return data
    else:
        if not img:
            data=decb(bytes(data,'utf-8'))

        if(data is '_None'):
            return None
        else:
            #data=bytes(data,'utf-8')

            shape=ds.strToShape(shape)

            data=np.frombuffer(data,types)
            data.shape=shape

            return data

def mergeFile2One(oldFile,newFile,chunk=1024*1024*5):
    f1=open(oldFile,'ab')
    f2=open(newFile,'rb')

    d=f2.read(chunk)

    while d!=b'':
        f1.write(d)
        d=f2.read(chunk)

    f1.close()
    f2.close()



class S:
    def __init__(self):
        pass

    def send(self,msg):
        print(msg)

#start='@!$%~(*&~$',end='%~#*!%$~#@'

class Send:
    start='<!@#$%^&>'
    end='<$)#&$&%>'

    def __init__(self,s,onSendError=None):
        self.s=s

        self.SEND_FILE_BUFFER=ds.SEND_CHUNK

        self.fileNames={}
        self.fileSize={}
        self.fileTempSize={}
        self.fileStatus={}
        self.fileFlow={}

        self.hfileNames={}
        self.hfileSize={}
        self.hfileTempSize={}
        self.hfileStatus={}
        self.hfileFlow={}

        self.onSendError=onSendError

        self.funSendListEnd={}

        self.fileCurrentName={}

    def sendMsg(self,message):
        message=enc(message)
        data=Send.start+message+Send.end+'\n'
        data=bytes(data,'utf-8')
        try:
            #t1=time.time()
            self.s.send(data)
            #t2=time.time()
            #print("Send ",len(data),t2-t1)
        except:
            if self.onSendError is not None:
                self.onSendError()

    def send_message(self,message):
        data=ad.assValue(['message'],[message],'MM',start='@!$%~(*&~$',end='%~#*!%$~#@')
        self.sendMsg(data)

    def get_file_name(self,file):
        sizes=os.stat(file).st_size
        dfile=file[::-1]
        index=None
        try:
            index=dfile.index('\\')
        except:
            try:
                index=dfile.index('/')
            except:
                index=None


        if index==None:

            file=ms.replaceBy_String(file,' ','_')
            return [file,sizes]
        else:
            cu=len(file)-(1+index)
            fName=file[cu+1:]
            fName=ms.replaceBy_String(fName,' ')
            return [fName,sizes]

    def getMainFileName(self,fName):
        cond=None
        for i in self.fileNames:
            if i==fName:
                cond=i
                break
        return cond

    def send_file(self,file,chunk=SEND_CHUNK,function=None,args=None,tfs={}):
        def fun(file,chunk=1024*1024*5,function=None,args=None,tfs={}):
            fName,size=self.get_file_name(file)
            fn=fName
            #First Stage
            t=str(time.time())
            t=ms.replaceBy_String(t,'.','_')
            fName=t+'-'+fName

            tfs[file]=fName

            self.fileNames[fName]=fn
            self.fileSize[fName]=size
            self.fileStatus[fName]=0
            self.fileTempSize[fName]=0
            self.fileFlow[fName]=True


            data=ad.assValue(['fName','fsize'],[fName,str(size)],'FF',start='@!$%~(*&~$',end='%~#*!%$~#@')
            self.sendMsg(data)

            #Second Stage
            file=open(file,'rb')
            cond=True
            while True and cond:
                cond=self.fileFlow[fName]

                d=file.read(chunk)
                length=len(d)
                if d==b'':
                    break
                self.fileTempSize[fName]=self.fileTempSize[fName]+length
                if function is not None:
                    function(args+[cond],self.fileTempSize[fName],size)
                self.fileStatus[fName]=1

                data=encb(d)
                data=data.decode('utf-8')
                data=ad.assValue(['Data','fName'],[data,fName],'FM',start='@!$%~(*&~$',end='%~#*!%$~#@')
                self.sendMsg(data)


            #Third Stage

            time.sleep(2)

            if cond:
                data=ad.assValue(['Data','fName','eType'],['End',fName,True],'FE',start='@!$%~(*&~$',end='%~#*!%$~#@')
            else:
                data=ad.assValue(['Data','fName','eType'],['End',fName,False],'FE',start='@!$%~(*&~$',end='%~#*!%$~#@')



            self.fileStatus[fName]=2
            if function is not None:
                function(args+[cond,fName],self.fileTempSize[fName],self.fileSize[fName],True)

            self.sendMsg(data)

            self.clearFileLog(fName,'F')
        threading.Thread(target=fun,args=(file,chunk,function,args,tfs)).start()

    def send_file2(self,file,chunk=SEND_CHUNK):
        def fun(file,chunk=1024*1024*5):
            fName,size=self.get_file_name(file)

            #First Stage
            t=str(time.time())
            t=ms.replaceBy_String(t,'.','_')
            fName=t+'-'+fName

            data=ad.assValue(['fName','fsize'],[fName,str(size)],'FF',start='@!$%~(*&~$',end='%~#*!%$~#@')
            self.sendMsg(data)

            #Second Stage
            file=open(file,'rb')

            while True:

                d=file.read(chunk)

                if d==b'':
                    break

                data=encb(d)
                data=data.decode('utf-8')
                data=ad.assValue(['Data','fName'],[data,fName],'FM',start='@!$%~(*&~$',end='%~#*!%$~#@')
                self.sendMsg(data)


            #Third Stage

            time.sleep(2)

            data=ad.assValue(['Data','fName','eType'],['End',fName,True],'FE',start='@!$%~(*&~$',end='%~#*!%$~#@')
            self.sendMsg(data)


        threading.Thread(target=fun,args=(file,chunk)).start()

    def stopAllFilesSending(self):
        data=self.fileFlow.copy()
        for i in data:
            self.fileFlow[i]=False

    def send_file3(self,file,chunk=SEND_CHUNK,nt=False,fileTempName=None,onStart=None,onEnd=None,toWhom='_None',toType='_None'):
        def fun(file,chunk=1024*1024*5,nt=False,fileTempName=None,onStart=None,onEnd=None,toWhom='_None',toType='_None'):
            fName,size=self.get_file_name(file)

            #First Stage
            if nt:
                t=str(time.time())
                t=ms.replaceBy_String(t,'.','_')
                fName=t+'-'+fName
            else:
                fName=fileTempName

            self.fileSize[fName]=size
            self.fileTempSize[fName]=0
            self.fileFlow[fName]=True

            onStart()
            data=ad.assValue(['fName','fsize','toWhom','toType'],[fName,str(size),toWhom,toType],'FF',start='@!$%~(*&~$',end='%~#*!%$~#@')
            self.sendMsg(data)


            #Second Stage
            file=open(file,'rb')

            while True and self.fileFlow[fName]:

                d=file.read(int(self.SEND_FILE_BUFFER))

                length=len(d)
                if d==b'':
                    break
                self.fileTempSize[fName]=self.fileTempSize[fName]+length
                data=encb(d)
                data=data.decode('utf-8')
                data=ad.assValue(['Data','fName'],[data,fName],'FM',start='@!$%~(*&~$',end='%~#*!%$~#@')

                self.sendMsg(data)


            #Third Stage

            #time.sleep(2)

            if onEnd is not None:
                onEnd(fName)

            if fName in self.funSendListEnd:
                fun=self.funSendListEnd[fName]
                fun(fName)

            if self.fileFlow[fName]:
                data=ad.assValue(['Data','fName','eType'],['End',fName,True],'FE',start='@!$%~(*&~$',end='%~#*!%$~#@')
            else:
                data=ad.assValue(['Data','fName','eType'],['End',fName,False],'FE',start='@!$%~(*&~$',end='%~#*!%$~#@')

            self.sendMsg(data)
            self.clearFileLog3(fName)



        arg=(file,chunk,nt,fileTempName,onStart,onEnd,toWhom,toType)
        threading.Thread(target=fun,args=arg).start()

    def clearFileLog3(self,fName):
        del self.fileSize[fName]
        del self.fileTempSize[fName]
        del self.fileFlow[fName]

    def sendHalf_file(self,file,loc,tfName,startAt,chunk=1024*1024*5,function=None,args=None,tfs={}):
        def fun(file,startAt,chunk=1024*1024*5,function=None,args=None,tfs={}):
            fName,size=self.get_file_name(file)
            fn=fName
            #First Stage

            fName=tfName

            data=ad.assValue(['fName','fsize','floc'],[fName,str(size),loc],'HF',start='@!$%~(*&~$',end='%~#*!%$~#@')
            self.sendMsg(data)

            #Second Stage
            file=open(file,'rb')
            flush=file.read(startAt)
            length=len(flush)

            self.hfileNames[fName]=fn
            self.hfileSize[fName]=size
            self.hfileStatus[fName]=0
            self.hfileTempSize[fName]=length

            tfs[file]=fName



            del flush
            cond=True
            while True and cond:
                cond=self.hfileFlow[fName]
                d=file.read(chunk)
                if d==b'':
                    break
                self.hfileTempSize[fName]=self.hfileTempSize[fName]+length
                if function is not None:
                    function(args,self.hfileTempSize[fName],size)
                self.hfileStatus[fName]=1
                data=encb(d)
                data=data.decode('utf-8')
                data=ad.assValue(['Data','fName'],[data,fName],'HM',start='@!$%~(*&~$',end='%~#*!%$~#@')
                self.sendMsg(data)


            #Third Stage

            time.sleep(2)
            if cond:
                data=ad.assValue(['Data','fName','eType'],['End',fName,True],'FE',start='@!$%~(*&~$',end='%~#*!%$~#@')
            else:
                data=ad.assValue(['Data','fName','eType'],['End',fName,False],'FE',start='@!$%~(*&~$',end='%~#*!%$~#@')






            self.sendMsg(data)
            self.hfileStatus[fName]=2
            if function is not None:
                function(args+[cond],self.hfileTempSize[fName],self.hfileSize[fName],True)
            self.sendMsg(data)
            self.clearFileLog(fName,'H')
        threading.Thread(target=fun,args=(file,startAt,chunk,function,args,tfs)).start()

    def clearFileLog(self,fName,typ='F'):
        if typ=='F':
            del self.fileNames[fName]
            del self.fileSize[fName]
            del self.fileStatus[fName]
            del self.fileTempSize[fName]
            del self.fileFlow[fName]
        elif typ=='H':
            del self.hfileNames[fName]
            del self.hfileSize[fName]
            del self.hfileStatus[fName]
            del self.hfileTempSize[fName]
            del self.hfileFlow[fName]
        else:
            print("Unknown TYpe you are expecting")

class Recv:
    start='<!@#$%^&>'
    end='<$)#&$&%>'

    def __init__(self,s,location='C:\\XprtDataBase\\',chunk=RECV_CHUNK,function=None,argument=None):
        self.s=s
        self.chunk=chunk

        self.RECV_DATA_BUFF=ds.RECV_CHUNK

        self.location=location
        try:
            os.makedirs(location)
        except:
            print("Directory Already Exist")
        self.fileNames={}
        self.fileSize={}
        self.fileTempSize={}
        self.fileStatus={}
        self.filef={}
        self.fileToWhom={}
        self.fileToType={}


        self.hfileNames={}
        self.hfileSize={}
        self.hfileTempSize={}
        self.hfileStatus={}
        self.hfilef={}

        self.function=function
        self.argument=argument
        self.errorFunction=None
        self.errorFunctionArg=None

        self.handleFileOnStart=None
        self.handleFileOnEnd=None


    def get_mb(self,size):

        size=size/1024
        size=size/1024

        return size

    def saveAllFiles(self):
        d=self.fileStatus
        for  i in d:
            st=d[i]
            if st==1:
                file=self.filef[i]
                file.close()
        d=self.hfileStatus
        for  i in d:
            st=d[i]
            if st==1:
                file=self.hfilef[i]
                file.close()

    def clearRecordF(self):
        d=self.fileStatus
        for  i in d:
            st=d[i]
            if st==2:
                del self.fileStatus[i]
                del self.fileSize[i]
                del self.fileTempSize[i]
                del self.fileNames[i]
                del self.filef[i]

    def clearRecordH(self):
        d=self.hfileStatus
        for  i in d:
            st=d[i]
            if st==2:
                del self.hfileStatus[i]
                del self.hfileSize[i]
                del self.hfileTempSize[i]
                del self.hfileNames[i]
                del self.hfilef[i]

    def clearAllRecords(self):
        self.clearRecordH()
        self.clearRecordF()

    def setHandleFileFunction(self,onStart,onEnd):
        self.handleFileOnStart=onStart
        self.handleFileOnEnd=onEnd


    def handleMessage(self,message):
        #print('kkrst'+str(self.function)+'st')

        m=message['message']
        dt,df=ad.deAssValue(m,True)

        if self.function is not None:
            d=message['message']
            if self.argument is not None:
                threading.Thread(target=self.function,args=(self.argument,d)).start()
            else:
            #self.function(message['message'])
                threading.Thread(target=self.function,args=(d,)).start()

    def handleFile(self,data,dtype):



        if dtype=='FF':
            fName=data['fName']
            fsize=data['fsize']

            toWhom=data['toWhom']
            toType=data['toType']

            self.fileToWhom[fName]=toWhom
            self.fileToType[fName]=toType

            if self.handleFileOnStart is not None:

                self.handleFileOnStart(self,fName)

            tName=self.location+fName

            file=open(tName,'wb')

            self.fileNames[fName]=tName
            self.filef[fName]=file
            self.fileSize[fName]=fsize
            self.fileTempSize[fName]=0
            self.fileStatus[fName]=0

        else:
            fName=data['fName']
            fName in self.fileNames
            if fName in self.fileNames:
                if dtype=='FM':
                    d=data['Data']
                    d=bytes(d,'utf-8')
                    d=decb(d)


                    file=self.filef[fName]

                    file.write(d)

                    self.fileTempSize[fName]=self.fileTempSize[fName]+len(d)
                    self.fileStatus[fName]=1
                elif dtype=='FE':
                    d=data['Data']

                    file=self.filef[fName]

                    eType=data['eType']
                    file.close()
                    cond=True

                    if eType=='False':
                        cond=False
                        loc=self.fileNames[fName]
                        statment='del "'+loc+'"'
                        os.popen(statment)




                    if self.handleFileOnEnd is not None:

                        self.handleFileOnEnd(self,fName,cond)



                    self.fileStatus[fName]=2
                    time.sleep(2)
                    self.clearFileLogF(fName)

                else:
                    print("This is An Error Which will never arise")

            else:
                print(fName," Not Found Or Deleted")

    def saveAllAndDeleteAll(self):
        locations=[]
        for i in self.fileNames:
            loc=self.fileNames[i]
            locations.append(loc)

            if i in self.filef:
                file=self.filef[i]
                file.close()

        for i in locations:
            statment='del "'+i+'"'
            os.popen(statment)


    def clearFileLogF(self,fName):
        if fName in self.fileNames:
            del self.fileToType[fName]
            del self.fileToWhom[fName]
            del self.fileTempSize[fName]
            del self.fileSize[fName]
            del self.filef[fName]
            del self.fileNames[fName]
            del self.fileStatus[fName]

    def deleteFileFromItsLoc(self,fName):
        tLoc=self.fileNames[fName]
        opFile.deletFile(tLoc)

    def handleHFile(self,data,dtype):
        if dtype=='HF':
            fName=data['fName']
            fsize=data['fsize']
            floc=data['floc']
            tName=floc
            #tName=self.location+fName
            file=open(tName,'ab')

            size=os.stat(tName).st_size

            self.hfileNames[fName]=tName
            self.hfilef[fName]=file
            self.hfileSize[fName]=fsize
            self.hfileTempSize[fName]=size
            self.hfileStatus[fName]=0

        elif dtype=='HM':
            d=data['Data']
            d=bytes(d,'utf-8')
            d=decb(d)
            fName=data['fName']

            file=self.hfilef[fName]

            file.write(d)

            self.hfileTempSize[fName]=self.hfileTempSize[fName]+len(d)
            self.hfileStatus[fName]=1
        elif dtype=='HE':
            d=data['Data']
            fName=data['fName']
            file=self.hfilef[fName]

            eType=data['eType']

            if eType=='False':
                mydb=db.genMdb()
                cursor=mydb.cursor()
                cb=db.cb1(mycursor,'filesaver')
                cond=cb.checkData('fSave','fName',fName)
                loc=self.hfileNames[fName]
                if not cond:
                    cb.insertDataN('fsave',[fName,loc])

            file.close()

            self.hfileStatus[fName]=2

        else:
            print("This is An Error Which will never arise")

    def seprateData(self,fdata):
        dtype=fdata[0]
        types=fdata[1]
        values=fdata[2]


        info=ad.cvtArr2Dict(types,values)

        if dtype=='MM':
            self.handleMessage(info)
        elif dtype[0]=='F':
            self.handleFile(info,dtype)
        elif dtype[0]=='H':
            self.handleHFile(info,dtype)
        else:
            print("This should not be arises due to MM ,FF,HH")

    def onLBGet(self,data):
        
        if True:

            fdata=ms.find_mid_text(data,Recv.start,Recv.end)
            
            fdata=dec(fdata)
            fdata=ad.deAssValue(fdata,start='@!$%~(*&~$',end='%~#*!%$~#@')
            self.seprateData(fdata)

    def get(self):
        def fun():

            data=''
            d=''
            while True:
                
                try:

                    d=self.s.recv(int(self.RECV_DATA_BUFF)).decode()


                except:
                    self.saveAllFiles()

                    if self.errorFunction is not None:

                        if self.errorFunctionArg is not None:

                            self.errorFunction(self.errorFunctionArg)
                        else:

                            self.errorFunction()

                    break

                
                cond=True
                while cond:
                        
                        if '\n' in d:
                                
                                index=ms.check_word(d,'\n')
                                df=data+d[:index]
                                
                                da=d[index+1:]
                                d=da
                                self.onLBGet(df)
                                data=''
                                
                        else:
                                
                                cond=False
                                data=data+d
                       
                        

                if cond:
                        data=data+d

                      

                
        threading.Thread(target=fun).start()



class SR:
        def __init__(self,s):
            self.send=Send(s)
            self.recv=Recv(s)


if __name__=='__main__':
    s=S()
    send=Send(s)
    send.send_message("HELLO WORLD")

