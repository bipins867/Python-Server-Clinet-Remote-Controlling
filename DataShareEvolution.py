import time
import socket
import myStringLib as ms
import ControlUnit as cu
import os
from cryptography.fernet import Fernet
import sys
import numpy as np
import threading
import AssembleData as ad
key=b'eQ5jxFcJNYII5Z4vhBtvT-mNiqx64yQEUln1SOoYEDA='
fernet=Fernet(key)
Fernet.generate_key()
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
def remodifyData(data,types,shape):
    data=decb(bytes(data,'utf-8'))

    if(data=='_None'):
        return None
    else:
        #data=bytes(data,'utf-8')
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
        data=np.frombuffer(data,types)
        data.shape=shape

        return data


class S:
    def __init__(self):
        pass

    def send(self,msg):
        print(msg)



class Send:
    start='<!@#$%^&>'
    end='<$)#&$&%>'
    def __init__(self,s):
        self.s=s

        self.fileNames={}
        self.fileSize={}
        self.fileTempSize={}
        self.fileStatus={}

        self.hfileNames={}
        self.hfileSize={}
        self.hfileTempSize={}
        self.hfileStatus={}

        self.function=None


    def sendMsg(self,message):
        message=enc(message)
        data=Send.start+message+Send.end
        data=bytes(data,'utf-8')
        self.s.send(data)

    def send_message(self,message):
        data=ad.assValue(['message'],[message],'MM')
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

    def send_file(self,file,chunk=1024*1024*5):
        fName,size=self.get_file_name(file)
        fn=fName
        #First Stage
        t=str(time.time())
        t=ms.replaceBy_String(t,'.','_')
        fName=t+'-'+fName

        self.fileNames[fName]=fn
        self.fileSize[fName]=size
        self.fileStatus[fName]=0
        self.fileTempSize[fName]=0

        data=ad.assValue(['fName','fsize'],[fName,str(size)],'FF')
        self.sendMsg(data)

        #Second Stage
        file=open(file,'rb')
        while True:
            d=file.read(chunk)
            length=len(d)
            if d==b'':
                break
            self.fileTempSize[fName]=self.fileTempSize[fName]+length
            self.fileStatus[fName]=1

            data=encb(d)
            data=data.decode('utf-8')
            data=ad.assValue(['Data','fName'],[data,fName],'FM')
            self.sendMsg(data)


        #Third Stage

        time.sleep(2)

        data=ad.assValue(['Data','fName'],['End',fName],'FE')

        self.fileStatus[fName]=2
        if self.function is not None:
            self.function(fName)
        self.sendMsg(data)


    def sendHalf_file(self,file,startAt,chunk=1024*1024*5):

        fName,size=self.get_file_name(file)
        fn=fName
        #First Stage
        t=str(time.time())
        t=ms.replaceBy_String(t,'.','_')
        fName=t+'-'+fName

        data=ad.assValue(['fName','fsize'],[fName,str(size)],'HF')
        self.sendMsg(data)

        #Second Stage
        file=open(file,'rb')
        flush=file.read(startAt)
        length=len(flush)

        self.hfileNames[fName]=fn
        self.hfileSize[fName]=size
        self.hfileStatus[fName]=0
        self.hfileTempSize[fName]=length

        del flush
        while True:
            d=file.read(chunk)
            if d==b'':
                break
            self.hfileTempSize[fName]=self.hfileTempSize[fName]+length
            self.hfileStatus[fName]=1
            data=encb(d)
            data=data.decode('utf-8')
            data=ad.assValue(['Data','fName'],[data,fName],'HM')
            self.sendMsg(data)


        #Third Stage

        time.sleep(2)
        self.hfileStatus[fName]=2
        data=ad.assValue(['Data','fName'],['End',fName],'HE')
        self.sendMsg(data)


class Recv:
    start='<!@#$%^&>'
    end='<$)#&$&%>'
    def __init__(self,s,location='C:\\Users\\Bipin\\Desktop\\A\\',chunk=1024*1024*5):
        self.s=s
        self.chunk=chunk
        self.location=location
        try:
            os.makedirs(location)
        except:
            pass
        self.fileNames={}
        self.fileSize={}
        self.fileTempSize={}
        self.fileStatus={}
        self.filef={}

        self.hfileNames={}
        self.hfileSize={}
        self.hfileTempSize={}
        self.hfileStatus={}
        self.hfilef={}

    def saveAllFiles(self):
        d=self.fileStatus
        for  i in d:
            st=d[i]
            if st==1:
                file=self.filef
                file.close()
        d=self.hfileStatus
        for  i in d:
            st=d[i]
            if st==1:
                file=self.hfilef
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


    def handleMessage(self,message):
        pass

    def handleFile(self,data,dtype):
        if dtype=='FF':
            fName=data['fName']
            fsize=data['fsize']
            tName=self.location+fName
            file=open(tName,'wb')
            
            self.fileNames[fName]=tName
            self.filef[fName]=file
            self.fileSize[fName]=fsize
            self.fileTempSize[fName]=0
            self.fileStatus[fName]=0

        elif dtype=='FM':
            d=data['Data']
            d=bytes(d,'utf-8')
            d=decb(d)
            fName=data['fName']

            file=self.filef[fName]

            file.write(d)

            self.fileTempSize[fName]=self.fileTempSize[fName]+len(d)
            self.fileStatus[fName]=1
        elif dtype=='FE':
            d=data['Data']
            fName=data['fName']
            file=self.filef[fName]

            file.close()

            self.fileStatus[fName]=2

        else:
            print("This is An Error Which will never arise")

    def handleHFile(self,data,dtype):
        if dtype=='HF':
            fName=data['fName']
            fsize=data['fsize']
            tName=self.location+fName
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

    def get(self):
        data=''

        while True:

            scond=ms.check_word(data,Recv.end)

            scond=str(scond)

            if(scond!='False'):
                if (Recv.start in data):
                    fdata=ms.find_mid_text(data,Recv.start,Recv.end)
                    fdata=dec(fdata)
                    fdata=ad.deAssValue(fdata)
                    self.seprateData(fdata)

                data=ms.get_rhs_data(data,Recv.end)

            try:
                d=self.s.recv(self.chunk).decode()
            except:
                self.saveAllFiles()
                print("It is Error in connection")
                self.s.close()
            cond=ms.check_word(d,Recv.end)
            scond=str(cond)

            if scond=='False':
                data=data+d

            else:
                temp=d[:cond]
                data=data+temp+Recv.end
                rest=d[cond+len(Recv.end):]

                if(Recv.start in data):
                    fdata=ms.find_mid_text(data,Recv.start,Recv.end)
                    fdata=dec(fdata)
                    fdata=ad.deAssValue(fdata)
                    self.seprateData(fdata)

                data=rest
