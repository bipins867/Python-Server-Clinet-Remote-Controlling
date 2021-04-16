#KMController
import pynput.keyboard as keyboard
import pynput.mouse as mouse
import KeyboardKey as kkey
import myStringLib as ms

class Keyboard:

    keys=[]
    start=False
    listener=None
    def __init__(self):

        
        self.cont=keyboard.Controller()

        self.funOnPress={}
        self.funOnRelease={}

        self.keyComb=[]

        self.conKeyComb=[]
        self.funKeyComb={}

        self.execPKeyFun={}
        self.execRKeyFun={}

        self.listenCond=False

        self.init()

    def init(self):

        Keyboard.listener=keyboard.Listener(on_press=self.on_press,on_release=self.on_release)
        Keyboard.listener.start()

    def setKeyComb(self,combArr,funAr):
        self.conKeyComb.append(combArr)
        self.funKeyComb[str(combArr)]=funAr

    def addKeyComb(self,combArr,fun):
        if combArr in self.conKeyComb:
            self.funKeyComb[str(combArr)].append(fun)
        else:
            self.conKeyComb.append(combArr)
            self.funKeyComb[str(combArr)]=[fun]

    def response(self,data):
        index=data.index(':')
        rdata=data[:index]
        key=''
        data=data[index+1:]

        if 'Key.' in data:
            key=kkey.get_def_key(data)
        else:
            key=data

        
        if(rdata=='press'):
            self.press(key)
        else:
            self.release(key)

    def press(self,key):
        try:
            self.cont.press(key)

        except:
            print("Error key entered")

    def release(self,key):
        try:
            self.cont.release(key)

        except:
            print("Error key entered")

    def pr(self,key):
        self.press(key)
        self.release(key)

    def typeString(self,string):
        try:
            self.cont.type(string)
        except:
            print("Error string entered")

    def check_and_convert(self,key):
        tstr=str(key)

        if 'Key.' in tstr:
            return str(key)
        else:
            return key.char
    
    def on_press(self,key):

        #if self.keyPress is None and self.actionPress is None:
        #    pass
        #else:

            ft=self.check_and_convert(key)



            funs=self.funOnPress

            self.keyComb.append(ft)
            self.keyCombChecker()
            for i in funs:
                fun=funs[i]
                if fun is not None:
                    fun(ft)
            data=self.check_and_convert(key)

            if str(data) in self.execPKeyFun:

                fun=self.execPKeyFun[data]
                fun(data)

            if self.listenCond:
                Keyboard.keys.append('press:'+str(data))

    def on_release(self,key):
        data=self.check_and_convert(key)
        funs=self.funOnRelease
        for i in funs:
            fun=funs[i]
            if fun is not None:
                fun(data)
        self.keyComb=[]

        if str(data) in self.execRKeyFun:
                fun=self.execRKeyFun[data]
                fun(data)
        if self.listenCond:

                Keyboard.keys.append('release:'+str(data))

    def keyCombChecker(self):

        if self.keyComb in  self.conKeyComb:
            funAr=self.funKeyComb[str(self.keyComb)]
            for fun in funAr:
                if fun is not None:
                    fun()
            print("KEY COMBINATION IS PRESSED")

    def clear(self):
        Keyboard.keys=[]

    def start(self):
        self.listenCond=True

    def stop(self):
        self.listenCond=False

    def mResume(self):
        self.start()

    def mStart(self):
        self.clear()
        self.start()


    def mPause(self):
        self.stop()

    def mStop(self):
        self.stop()

class Mouse:
    buttons=[]
    start=False
    listener=None
    cont=mouse.Controller()
    def __init__(self,rightCond=True):

        self.rightCond=rightCond
        self.secCond=False
        
        self.prevPos=Mouse.cont.position
        self.currPos=Mouse.cont.position

        self.funOnScroll={}
        self.funOnMove={}
        self.funOnClick={}


    def response(self,data):
        index=data.index(':')
        rdata=data[:index]
        key=''
        data=data[index+1:]

        dis=ms.distributeString(data,',')

        if(rdata=='move'):
            x,y=float(dis[0]),float(dis[1])
            self.move(x,y)

        elif(rdata=='click'):

            b=dis[0]

            if dis[1]=='True':
                pr=True
            else:
                pr=False
            b=kkey.get_def_button(b)
            if(pr):
                self.press(b)
            else:
                self.release(b)
            
        elif(rdata=='scroll'):
            x,dy=int(dis[0]),int(dis[1])
            self.scroll(x,dy)
        
    
    #To Do action
    def setPosition(self,position):
        Mouse.cont.position=position

    def move(self,dx,dy):
        Mouse.cont.move(dx,dy)

    def press(self,button):
        Mouse.cont.press(button)

    def release(self,button):
        Mouse.cont.release(button)

    def click(self,button,times):
        Mouse.cont.click(button,times)

    def scroll(self,x,steps):
        Mouse.cont.scroll(x,steps)
    

    #To Record action
    def on_move(self,x,y):
        self.currPos=(x,y)

        x=self.prevPos[0]-self.currPos[0]
        y=self.prevPos[1]-self.currPos[1]
        x=-x
        y=-y
        data='move:{0},{1}'.format(x,y)
        #print(data)
        args=data
        for i in self.funOnMove:
            fun=self.funOnMove[i]
            if fun is not None:
                fun(args)
        if self.rightCond:
            
            if self.secCond:
                Mouse.buttons.append(data)
        else:
            
            Mouse.buttons.append(data)
            
        self.prevPos=self.currPos

    def on_click(self,x,y,button,pressed):
        data='click:{0},{1}'.format(button,pressed)
        args=data

        for i in self.funOnClick:
            fun=self.funOnClick[i]
            if fun is not None:
                fun(args)
        Mouse.buttons.append(data)
        if self.rightCond:
            if pressed:
                self.secCond=True
            else:
                self.secCond=False

    def on_scroll(self,x,y,dx,dy):
        data='scroll:{0},{1}'.format(dx,dy)
        args=data
        for i in self.funOnScroll:
            fun=self.funOnScroll[i]
            if fun is not None:
                fun(args)
        Mouse.buttons.append(data)


        
    def clear(self):
        Mouse.buttons=[]

    def start(self):
        Mouse.listener=mouse.Listener(on_move=self.on_move,on_click=self.on_click,on_scroll=self.on_scroll)
        Mouse.listener.start()

    def stop(self):
        Mouse.listener.stop()
        

    def mResume(self):
        self.start()

    def mStart(self):
        self.clear()
        self.start()


    def mPause(self):
        self.stop()

    def mStop(self):
        self.stop()
    
if __name__=='__main__':
    k=Keyboard()
    def funP(key):
	    print(f"{key} is presed")


    def funR(key):
	    print(f"{key} is release")


    k.execPKeyFun['Key.f9']=funP
    k.execRKeyFun['Key.f11']=funR


