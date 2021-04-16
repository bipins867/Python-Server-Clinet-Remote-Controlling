#Tserver
import ControlUnit as cu
import DataShare as ds
import cv2
import tkinter as tk
import Gui_Creation as gc
import threading
import AssembleData as ad
import RControl as rc

con=rc.Controls()

c=cu.create_server('localhost')
print("Server Started")
s,addr=c.accept()
print("Server is connected")

send=ds.Send()

cap=cv2.VideoCapture(0)

size=(600,500)

def fun():
    while True:
        #_,frame=cap.read()
        frame=con.get_screen_shot(size)
        #frame=cv2.resize(frame,size)
        data=ds.prepSend(frame)

        d=ad.assValue(['data','type','shape'],data)

        send.send_message(s,d,'bipin')
        

print("Server is sending Data")
threading.Thread(target=fun).start()
