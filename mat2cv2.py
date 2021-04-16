import cv2
import matplotlib.pyplot as plt
import numpy as np
import time
import pyaudio
import threading
import RControl as rc
import tkinter as tk
import Gui_Creation as gc

con=rc.Controls()
stream=con.on_mic()
#import warnings
fig=plt.figure()
#warnings.filterwarnings("error")


def genGraph(x):
    #t1=time.time()
    fs=0.01
    x=x/1000
    Time = np.linspace(0, len(x) / (1/fs), num=len(x))
    x=plt.plot(Time,x)[0]
    plt.ylim(-20,20)
    #plt.xlim(-10,100)
    x.figure.canvas.draw()
    
    img = np.frombuffer(x.figure.canvas.tostring_rgb(), dtype=np.uint8)
    img  = img.reshape(x.figure.canvas.get_width_height()[::-1] + (3,))
    plt.clf()
    #t2=time.time()-t1
    #print(t2)
    return img

class f:
	frame=None
	def __init__(self):
		self.show()
		#threading.Thread(target=self.show).start()


	def show(self):
		while True:
			frame=np.frombuffer(stream.read(1024),dtype='int16')

			frame=np.frombuffer(frame,dtype='int16')
			frame.shape=(1024,2)
			sframe=genGraph(frame)
			
			if sframe is None:
				continue
			#sframe=cv2.resize(sframe,(1300,500))
			cv2.imshow("Frame",sframe)
			
			
			if cv2.waitKey(1) & 0xff==ord('q'):
				break
a=f()
