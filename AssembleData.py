import KMController as kmc
import RControl as rc
import myStringLib as ms
from cryptography.fernet import Fernet
import DataShare as ds
import AssembleData as ad

key=b'eQ5jxFcJNYII5Z4vhBtvT-mNiqx64yQEUln1SOoYEDA='
fernet=Fernet(key)

def assValue(types,values,info='default',start='~!@#$%$^&',end='@#%12#$@'):
    data='<{0}{1}'.format(info,start)
    tf=''

    if(len(types)>0 and len(values)>0 and len(types)==len(values)):

        for i in range(len(types)):
            typ=types[i]
            val=values[i]
            tf=tf+typ+'{0}{1}{2}'.format(end,val,start)

        data=data+tf+'>'
        
        return data
    else:
        return '< >'

def deAssValue(data,dicts=False,start='~!@#$%$^&',end='@#%12#$@'):
        if(data!='< >'):
            dis=ms.distributeString(data,start)
            info=dis[0][1:]
            types=[]
            values=[]

            for i in range(1,len(dis)-1):
                d=dis[i]

                dd=ms.distributeString(d,end)
                types.append(dd[0])
                values.append(dd[1])

            
            if not dicts:
                
                return [info,types,values]
            else:
                dicts=ad.cvtArr2Dict(types,values)
                return [info,dicts]




        
def cvtArr2Dict(array1,array2):
    if len(array1)==len(array2):
        dicts={}
        for i in range(len(array1)):
            dicts[array1[i]]=array2[i]

        return dicts

def cvtDict2Array(dicts):
    arry1=[]
    arry2=[]

    for i in dicts:
        arry1.append(i)
        arry2.append(dicts[i])

    return [arry1,arry2]


class Dassemble:

    def __init(self):
        pass


    def dAssembler(self,data):
        msg=fernet.decrypt(data)
        msg=msg.decode()

        data=ms.get_rhs_data(msg,'##->')
        atype=ms.get_lhs_data(msg,'##->')
        atype=atype[4:]

        atype=ms.distributeString(atype,'@@##')

        data=data.encode()

        data=fernet.decrypt(data)
        data=data.decode()

        return  atype+[data]
        

class Assemble:

    def __init__(self):
        pass

    def aAssembler(self,data,atype,toSend):
        data=data.encode()
        data=fernet.encrypt(data).decode()
        msg='<-@@{0}@@##{1}##->'.format(atype,toSend)+data
        msg=msg.encode()
        msg=fernet.encrypt(msg)
        return msg
        

    def aData(self,data,toSend):
        return self.aAssembler(data,'Data',toSend)

    def Data(self,data,toSend):
        return self.aData(data,toSend)

    def aSequrity(self,data,toSend):
        return self.aAssembler(data,'Sequrity',toSend)
    
    def Sequrity(self,data,toSend):
        return self.aAssembler(data,'Sequrity',toSend)
    
    def aSystem(self,data,toSend):
        return self.aAssembler(data,'System',toSend)

    def System(self,data,toSend):
        return self.aSystem(data,toSend)

    def aApp(self,data,toSend):
        return self.aAssembler(data,'App',toSend)

    def App(self,data,toSend):
        return self.aApp(data,toSend)
      
    def aError(self,data,toSend):
        return self.aAssembler(data,'Error',toSend)

    def Error(self,data,toSend):
        return self.aError(data,toSend)
    
    def aInfo(self,data,toSend):
        return self.aAssembler(data,'Info',toSend)

    def Info(self,data,toSend):
        return self.aInfo(data,toSend)

    def aAdmin(self,data,toSend):
        return self.aAssembler(data,'Admin',toSend)

    def Admin(self,data,toSend):
        return self.aAdmin(data,toSend)
