#RControl
print("Loading RControl")
import os
import numpy as np
import cv2
import pyautogui
import pyaudio
import psutil
import myStringLib as ms
import threading
from cryptography.fernet import Fernet
import KMController as km
print("Loading Completed")

key=b'eQ5jxFcJNYII5Z4vhBtvT-mNiqx64yQEUln1SOoYEDA='
fernet=Fernet(key)


class Controls:

    

    def __init__(self):
        self.sysinfo=''
        self.cond=False

        self.cap=None
        self.stream=None
        self.mouse=km.Mouse()


    #Camera Processing
    camFrame=None
    cap=None
    runCam=False

    def camStart(self,num=0):
        Controls.runCam=True
        Controls.cap=cv2.VideoCapture(num)

    def dStart(self):
        Controls.runCam=True
        t1=threading.Thread(target=self.capture)
        t1.start()

    def dPause(self):
        Controls.runCam=False

    def dStop(self):
        Controls.runCam=False
        self.off_camera(Controls.cap)
        

    def capture(self):
        while True:
            if not Controls.runCam:
                break
            try:
                frame=self.get_cam_frame(Controls.cap)
                Controls.camFrame=cv2.resize(frame,(250,250))
            except:
                pass
    
    def get_cam_frame(self,cap,size=(100,80),smooth=False):
        r,frame=cap.read()
        if frame is not None:
            frame=cv2.resize(frame,size)
            if smooth:
                kernal=np.ones([3,3],np.float32)/25
                frame=cv2.filter2D(frame,-1,kernal)
            Controls.camFrame=frame

            return frame

    def on_camera(self,cam=0):
        cap=cv2.VideoCapture(cam)

        Controls.cap=cap
        
        return cap

    def off_camera(self,cap):
        if cap is None:
            pass
        else:
            cap.release()

    def show_image(self,image,winName='Hello'):
        cv2.imshow(winName,image)
        
    
    #Mic Processing

    micFrame=None
    micStream=None
    runMic=False

    def miStart(self):
        Controls.micStream=True
        Controls.micStream=self.on_mic()

    def micStart(self):
        Controls.runMic=True
        t1=threading.Thread(target=self.micCapture)
        t1.start()

    def micPause(self):
        Controls.runMic=False

    def micStop(self):
        Controls.runMic=False
        self.off_mic(Controls.micStream)
        

    def micCapture(self):
        while True:
            if not Controls.runMic:
                break
            Controls.micFrame=self.get_mic_frame(Controls.micStream)
    
    
    def play_audio(self,stream,frame):
        stream.write(frame)
    
    def get_mic_frame(self,stream,frame=1024):
        d=stream.read(frame)
        return d

    def on_mic(self,channels=1,rate=5000,input=True,output=True):
        p=pyaudio.PyAudio()
        stream=p.open(format=pyaudio.paInt16,channels=channels,rate=rate,input=input,output=output)
        Controls.micStream=stream
        return stream

    def off_mic(self,stream):
        if stream is None:
            pass
        else:
            stream.close()

    #Screen Shot processing
    screenFrame=None
    runScreen=False
    screenSize=(600,300)
    def start(self):
        Controls.runScreen=True

        t1=threading.Thread(target=self.scrcapture)
        t1.start()

    def scrcapture(self):
        while True:
            if not Controls.runScreen:
                break
            frame=self.get_screen_shot(size=Controls.screenSize)
            Controls.screenFrame=frame

    def stop(self):
        Controls.runScreen=False
    
    def get_screen_shot(self,size=(510,300),r=False):
        image=pyautogui.screenshot()
        pos=self.mouse.cont.position
        image= np.array(image)
        rt=10
        image=cv2.rectangle(image,(pos[0]-rt,pos[1]-rt),(pos[0]+rt,pos[1]+rt),(255,0,0),-1)
        if(not r):
            image=cv2.resize(image,size)
        image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        Controls.screenFrame=image
        return image

    #Command Line Command Executioins

    def execute_command(self,command,vreturn=True):

        p=os.popen(command).read()

        if(vreturn):
            return p


   

    def battery_info(self):
        battery=psutil.sensors_battery()
        plugged=battery.power_plugged
        percent=battery.percent
        return [plugged,percent]

    def system_info(self):
        if(self.cond):
            return self.sysinfo
        else:
            p=os.popen('systeminfo').read()
            self.cond=True
            self.sysinfo=p
            return p

    def tasklist_info(self):
        p=os.popen('tasklist').read()
        return p

    def system_name(self):
        data=os.popen('hostname').read()
        return data
    
    def task_kill(self,taskName):
        command='taskkill /f /im {0}'.format(taskName)
        p=os.popen(command).read()
        return p

    def task_kill_chil(self,taskName):
        command='taskkill /t /im {0}'.format(taskName)
        p=os.popen(command).read()
        return p

    def task_kill_pid(self,pidNo):
        command='taskkill /PID {0}'.format(pidNo)
        p=os.popen(command).read()

        return p

class Response:

    def __init__(self):
        pass


    def gen_mic_res(self,frame):
        data=fernet.encrypt(frame)

        return data

    def cvt_mic_res(self,data):
        data=fernet.decrypt(data)
        return data

    def gen_cam_res(self,frame):
        dtype=frame.dtype
        shape=frame.shape
        data=frame.tobytes()

        data=fernet.encrypt(data)

        ddata=str(dtype)+':'+str(shape)+':'+data.decode()

        return ddata

    def cvt_cam_res(self,data):
        dis=ms.distributeString(data,':')
        dtype,shape,data=dis

        shape=shape[1:-1]
        disshape=ms.distributeString(shape,',')

        data=data.encode()
        data=fernet.decrypt(data)

        if(disshape==[]):
            shape=shape[:-1]
            shape=int(shape)
            shape=(shape,)

        else:
            df=[]
            for i in disshape:
                df.append(int(i))

            df=tuple(df)
            shape=df

        data=np.frombuffer(data,dtype)
        data.shape=shape
        return data
            
        
        



class Cv2Tk:

    def __init__(self,label,img):

        self.label=label
        self.img=img
        self.cond=True



    def show_frame(self):
        frame=self.img
        frame = cv2.flip(frame, 1)
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        self.label.imgtk = imgtk
        self.label.configure(image=imgtk)
        if(self.cond):
            self.label.after(10, self.show_frame)


    def stop_showing(self):
        self.cond=False


    def start_showing(self,label):
        self.cond=True
        
