#DataShare
import time
import socket
import myStringLib as ms
#import myStringLib2 as ms2
import ControlUnit as cu
import os
from cryptography.fernet import Fernet
import sys
import numpy as np
import DataShare1234ButOriginal as ds
import threading

key=b'eQ5jxFcJNYII5Z4vhBtvT-mNiqx64yQEUln1SOoYEDA='
fernet=Fernet(key)
def prepSend(data):
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


class Recv:


    def __init__(self,location='C:\\Users\\Bipin\\Documents\\DataStorage\\',chunk=1024*1024,function1=None,function2=None,args1=None,container=None):
        try:
            os.makedirs(location)
        except:
            print("It is error")

        self.file_status=dict()

        self.files=dict()
        self.filef=dict()
        self.flsize=dict()
        self.chunk=chunk
        self.location=location
        self.message=''
        self.tmessage=dict()

        self.count_mess=0

        self.function1=function1
        self.args1=args1
        self.function2=function2

        self.container=container

        self.frame={}

    def get_chunk(self,chunk=5):
        message=self.tmessage
        dmessage=[]
        length=len(message)

        if(length>0):

            if(length<chunk):
                for i in message:
                    dmessage.append(message[i])
                    del self.tmessage[i]
            else:
                temp=0

                for  i in message:
                    if(temp>chunk):
                        break
                    dmessage.append(message([i]))
                    temp=temp+1
                    del self.tmessage[i]
        else:
            return []


    def get_total_file(self):
        files=[]
        for i in self.files:
            files.append(i)

        return files

    def get_file_and_size(self):
        return self.files


    def get_curr_chunk(self,fName):

        if(fName in self.flsize):
            return [self.flsize[fName],self.files[fName]]
        else:
            return None

    def recv_message(self,msg,start,end):

        #Clear
       msg= ms.find_mid_text(msg,start,end)
       msg=fernet.decrypt(msg.encode()).decode()

       if msg=='-----':
           pass
       else:

            self.count_mess=self.count_mess+1
            self.tmessage[self.count_mess]=msg

    def get_mb(self,size):

        size=size/1024
        size=size/1024

        return size

    def get_kb(self,size):
        return size/1024

    def recv_file_f(self,data,end):
        #Clear
        location=self.location
        t=time.time()
        t=ms.replaceBy_String(str(t),'.')
        hinte='^%&@f__@&*s_'
        hints='@->@n!~_'

        hint='*&@->'+end
        size=ms.find_mid_text(data,hinte,hint)
        fName=ms.find_mid_text(data,hints,hinte)
        file=location+t+'_'+fName
        print(file)
        f=open(file,'wb')

        self.file_status[file]=True

        self.flsize[fName]=0
        size=int(size)
        mb=self.get_mb(size)
        if(mb>5):
            self.chunk=1024*1024
        else:
            self.chunk=1024

        data="File :"+fName+" Size :"+str(size)
        self.alert_message(data)
        return [f,size]


    def recv_file_s(self,file,data,end,fName):
        #Clear




        startd='^%&@s__@%*&->'
        rdata=ms.find_mid_text(data,startd,end)

        rdata=bytes(rdata,'utf-8')
        rdata=fernet.decrypt(rdata)
        length=len(rdata)
        self.flsize[fName]=self.flsize[fName]+length


        file.write(rdata)

        return file

    def recv_file_e(self,file,fName):

        #Clear
        file.close()
        self.files.pop(fName)
        self.filef.pop(fName)
        self.file_status[file]=True
        self.flsize.pop(fName)

    def dis_data(self,data,start,end):

        types=self.identify_data(data)
        if(types=='f'):
            sst=self.recv_file(data,start,end)
        else:
            sst=self.recv_message(data,start,end)

    def get(self,s,start,end='<-$-__(@#%^&*)__-$->'):
        t1='<-@-$$##-M-##$$__&*-__{0}__-*&-@->'.format(start)
        t2='<-@-$$##-F-##$$__&*-__{0}__-*&-@->'.format(start)
        data=''

        while True:

            #print("________________________________________________")
            cond=ms.check_word(data,end)
            #print(cond)
            #print(cond,ms2.check_word(data,end))
            scond=str(cond)

            if(scond!='False'):

                if(t1 in data):
                    self.dis_data(data,t1,end)
                else:
                    self.dis_data(data,t2,end)

                data=ms.get_rhs_data(data,end)

            d=s.recv(self.chunk).decode()

            #print(d)
            cond=ms.check_word(d,end)

            scond=str(cond)

            if(scond=='False'):

                data=data+d

            else:

                temp=d[:cond]
                data=data+temp+end
                rest=d[cond+len(end):]

                #Identifying And sending procedure
                if(t1 in data):
                    self.dis_data(data,t1,end)
                else:
                    self.dis_data(data,t2,end)

                data=rest



    def send(data,a,b):
        print(data)

#t='<-@-$$##-M-##$$__&*-__{0}__-*&-@->'.format(start)
#end='<-$-__(@#%^&*)__-$->'



    def identify_data(self,data):
        #Clear
        start='<-@-$$##-'
        end='-##$$__'
        try:
            txt=ms.find_mid_text(data,start,end)

        except:
            print('--------------------------------------------------------=')
            print(data)
            sys.exit(0)

        if(txt=='M'):
            return 's'
        else:
            return 'f'

    def recv_file(self,data,start,end):


        sdata='__-*&-@->@n!~_'
        edata='^%&@'
        fName=ms.find_mid_text(data,sdata,edata)



        edata='__@'

        fse=ms.find_mid_text(data,fName+'^%&@',edata)

        if(fse=='f'):

            ft=self.recv_file_f(data,end)
            self.files[fName]=ft[1]
            self.filef[fName]=ft[0]
            if self.function1 is not None:
                self.frame[fName]=self.function1(self.container,fName)
        elif fse=='s':
            ftfs=self.filef[fName]
            ft=self.recv_file_s(ftfs,data,end,fName)
            self.filef[fName]=ft
            if self.function2 is not None:
                self.function2(self.frame[fName],self.flsize[fName]+length,self.files[fName])

        else:
            self.alert_message(fName)

            fil=self.filef[fName]
            self.recv_file_e(fil,fName)

            if self.function2 is not None:
                self.function2(self.frame[fName],self.flsize[fName]+length,self.files[fName],True)




    def message(self,stringVar):
        stringVar.set(message)

    def alert_message(self,message):
        print(message)
        print("Alert")
        self.message=message



class S:
    def __init__(self):
        pass

    def send(self,msg):
        print(msg)


class Send:

    def __init__(self):
        self.files=dict()
        self.flsize=dict()
        self.file_status=dict()

    def get_total_file(self):
        files=[]
        for i in self.files:
            files.append(i)

        return files

    def get_file_and_size(self):
        return self.files


    def get_curr_chunk(self,fName):

        if(fName in self.flsize):
            return [self.flsize[fName],self.files[fName]]
        else:
            return None



    def send_message(self,s,msg,start,end='<-$-__(@#%^&*)__-$->'):
        msg=msg.encode()
        msg=fernet.encrypt(msg)
        t='<-@-$$##-M-##$$__&*-__{0}__-*&-@->'.format(start)
        start=t
        msg=start+msg.decode()+end
        msg=bytes(msg,'utf-8')
        s.send(msg)

    def get_file_name(self,file):
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
            return file
        else:
            cu=len(file)-(1+index)
            fName=file[cu+1:]
            fName=ms.replaceBy_String(fName,' ')
            return fName

    def send_file(self,s,file,start,end='<-$-__(@#%^&*)__-$->',chunk=5*1024*1024,function=None,args=None):
        def fun(s,file,start,end,chunk,function,args):

            tstart=start
            tend=end

            t='<-@-$$##-F-##$$__&*-__{0}__-*&-@->'.format(start)
            start=t
            stat=os.stat(file)
            size=stat.st_size

            fName=self.get_file_name(file)
            self.file_status[file]=True
            data='@n!~_'+fName+'^%&@f__@&*s_'+str(size)+'*&@->'
            self.files[fName]=size
            self.flsize[fName]=0
            start=bytes(start,'utf-8')
            end=bytes(end,'utf-8')
            data=bytes(data,'utf-8')

            wdata=start+data+end


            s.send(wdata)


            #Now second part for sending the data
            data='@n!~_'+fName+'^%&@s__@%*&->'
            data=bytes(data,'utf-8')
            f=open(file,'rb')
            data=start+data


            while True:
                d=f.read(chunk)
                length=len(d)
                self.flsize[fName]=self.flsize[fName]+length
                if function is not None:
                    function(args,self.flsize[fName]+length,size)
                if(d==b''):
                    self.file_status[file]=False
                    break
                d=fernet.encrypt(d)

                rdata=data+d+end

                s.send(rdata)


            data='@n!~_'+fName+'^%&@e__@*%&->---END---'
            data=bytes(data,'utf-8')
            wdata=start+data+end
            s.send(wdata)
            time.sleep(2)

            self.send_message(s,'-----',tstart,tend)
            if function is not None:
                function(args,self.flsize[fName]+length,size,True)
            self.files.pop(fName)
            self.flsize.pop(fName)
        threading.Thread(target=fun,args=(s,file,start,end,chunk,function,args)).start()
