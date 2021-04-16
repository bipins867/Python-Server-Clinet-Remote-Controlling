import ControlUnit as cu
import threading
import random
import AssembleData as ad
import DataShare as ds
import XprtLoginControl as xlc
import cv2
import time
import numpy as np
xc=xlc.Controller()
ass=ad.Assemble()
dAssemble=ad.Dassemble()


s=cu.client_connect('localhost',4445)
send=ds.Send()

def dataCvt(data):
        userName='Bipin'
        type='Camera'
        data=np.array(data)

        shape=str(data.shape)
        types=str(data.dtype)
        actData=bytes(data)


        actData=ds.encb(actData)


        actData=actData.decode()


        data=ad.assValue(['userName',type.lower()+'Data',type.lower()+'Type',type.lower()+'Shape'],[userName,actData,types,shape],'_'+type)


        data=ass.aData(data,userName)


        data=data.decode()
        send.send_message(s,data,'bipin')


data=ad.assValue(['userName','userPass'],['Suraj','Suraj'],'login')
data=ass.aSequrity(data,'user')
data=data.decode()
send.send_message(s,data,'bipin')

def startSending():
    cap=cv2.VideoCapture(0)
    while True:
            _,Frame=cap.read()
            h,w=Frame.shape[:2]
            h=int(h/4)
            w=int(w/4)
            Frame=cv2.resize(Frame,(w,h))
            #Frame=cv2.resize(Frame,(300,200))
            t1=time.time()
            dataCvt(Frame)
            t2=time.time()
            print(t2-t1)
