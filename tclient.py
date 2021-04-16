#TClient
import ControlUnit as cu
import DataShare as ds
import cv2
import tkinter as tk
import Gui_Creation as gc
import threading
import AssembleData as ad

print("Client is waiting")
s=cu.client_connect('localhost')
print("Client is connected")
recv=ds.Recv()

threading.Thread(target=recv.get,args=(s,'bipin')).start()
r=tk.Tk()
r.geometry('1000x600')
label=tk.Label(r,width=1000,height=600,bg='green')
label.place(x=10,y=10)
imgs={}
def fun():
    count=1
    global imgs
    while True:

        if count in recv.tmessage:
            msg=recv.tmessage[count]
            del recv.tmessage[count]
            count=count+1
            dtype,wType,values=ad.deAssValue(msg)

            info=ad.cvtArr2Dict(wType,values)
            data=info['data']
            types=info['type']
            shape=info['shape']
            
            d=ds.remodifyData(data,types,shape)
            d=cv2.resize(d,(1000,600))
            d=cv2.cvtColor(d,cv2.COLOR_BGR2RGB)
            img=gc.cvtIntoLabelImage(d)
            imgs[count]=img
            label.config(image=imgs[count])
            

print("Client is recving")
threading.Thread(target=fun).start()
r.mainloop()
