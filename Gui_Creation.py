import tkinter as tk
from tkinter import ttk
from PIL import Image,ImageTk
import cv2
import DataShare as ds
import numpy as np
import Gui_Creation as gc

imgSource=None

def config(label,img,width):
    global imgSource

    h,w=img.shape[:2]

    

def scrollableFrame(fContainer,cheight=200,cwidth=200,color='grey',orient='vertical'):
    container=fContainer
    canvas = tk.Canvas(container,bg=color)
    scrollbar = ttk.Scrollbar(container, orient=orient, command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    #scrollable_frame.pack()
    canvas.configure(yscrollcommand=scrollbar.set)


    

    container.pack()
    canvas.config(height=cheight,width=cwidth)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    return [scrollable_frame,canvas]

def scrollableFrameHorizontal(fContainer,cheight=200,cwidth=200,color='grey',orient='horizontal'):
    container=fContainer
    canvas = tk.Canvas(container,bg=color)
    scrollbar = ttk.Scrollbar(container, orient=orient, command=canvas.xview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    #scrollable_frame.pack()
    canvas.configure(yscrollcommand=scrollbar.set)


    

    container.pack()
    canvas.config(height=cheight,width=cwidth)
    canvas.pack(side="top", fill="both", expand=True)
    scrollbar.pack(side="bottom", fill="x")

    return [scrollable_frame,canvas]

def cvtIntoLabelImage(img):
    
    img=Image.fromarray(img)
    imgtk=ImageTk.PhotoImage(img)

    return imgtk

def cvtBin2Img2(img,types='uint8',shape=(200,200,3),cvt=True,):

                             img=bytes(img,'utf-8')

                             img=ds.decb(img)
                             img=np.frombuffer(img,dtype=types)
                             img.shape=shape
                             #cv2.imwrite('C:\\Users\\Bipin\\Desktop\\kk.jpeg',img)
                             img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
                             #print(img.shape)
                             #cv2.imshow('hi',img)
                             img=Image.fromarray(img)
                             if cvt:
                                imgtk=ImageTk.PhotoImage(img)
                                return imgtk
                             else:
                                return img

def cvtBin2Img1(img):
                             #img=bytes(img[2:-1],'utf-8')

                             img=ds.decb(img)
                             img=np.frombuffer(img,dtype='uint8')
                             img.shape=(200,200,3)
                             #cv2.imwrite('C:\\Users\\Bipin\\Desktop\\kk.jpeg',img)
                             img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
                             #print(img.shape)
                             #cv2.imshow('hi',img)
                             img=Image.fromarray(img)
                             imgtk=ImageTk.PhotoImage(img)

                             return imgtk

def cvtBin2Img(img):
                             img=bytes(img[2:-1],'utf-8')

                             img=ds.decb(img)
                             img=np.frombuffer(img,dtype='uint8')
                             img.shape=(200,200,3)
                             #cv2.imwrite('C:\\Users\\Bipin\\Desktop\\kk.jpeg',img)
                             img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
                             #print(img.shape)
                             #cv2.imshow('hi',img)
                             img=Image.fromarray(img)
                             imgtk=ImageTk.PhotoImage(img)

                             return imgtk
                            
def SearchLabelUser(sf,image,userName='',name='',color='yellow'):
	frame=tk.Frame(sf,height=130,width=300,bg=color)

	label=tk.Label(frame,image=image,width=100,height=100)
	label.place(x=10,y=10)
	l2=tk.Label(frame,text=userName)
	l2.place(x=120,y=10)
	
	l2=tk.Label(frame,text=name)
	l2.place(x=120,y=40)
	btn=tk.Button(frame,text='Hello World')
	btn.place(x=120,y=80)
	frame.pack()

def NotificationLabel(sf,notf,color='yellow'):
    frame=tk.Frame(sf,height=40,width=300,bg=color)
    
    label=tk.Label(frame,text=notf)
    label.place(x=10,y=5)

    frame.pack()
    
