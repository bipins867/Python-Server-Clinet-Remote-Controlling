#import RControl as rc
import threading
import time

class Controls:

    def __init__(self):

        self.openWindows={}
        self.controlCond={}
        self.funList={}
        self.funFirstOnList={}
        self.funFirstOffList={}
        self.funThread={}
        self.cond={}

        self.funOnStartInstance={}
        self.funOnEndInstance={}
        

    def funOpenWindow(self,userName):
        self.openWindows[userName]=True
        self.controlCond[userName]={}
        self.funThread[userName]={}
        
        
    def funCloseWindow(self,userName):
        self.openWindows[userName]=False
        del self.controlCond[userName]
        del self.funThread[userName]
        
    def funOnSending(self,userName,types):
        self.controlCond[userName][types]=True
        self.cond[types]=True

        self.executeOnStart(types)
        fts=self.funFirstOnList[types]

        threading.Thread(target=fts).start()
        
    def funOffSending(self,userName,types):
        self.controlCond[userName][types]=False
        self.executeOnStop(types)
        fts=self.funFirstOffList[types]
        threading.Thread(target=fts).start()


    def executeOnStart(self,types):
        count=0
        cond=False
        for i in self.controlCond:
            if types in self.controlCond[i]:
                cond=True
                ct=self.controlCond[i][types]
                if ct:
                    count=count+1

        if cond:
            funs=self.funList[types]
            if count>1:
                pass
            else:
                funt=self.funOnStartInstance[types]

                funt()
                def fun():
                    
                    while self.cond[types]:
                        funs()
                t1=threading.Thread(target=fun)
                t1.start()
                self.funThread[types]=t1
            
            
    
    def executeOnStop(self,types):
        count=0
        for i in self.controlCond:
            ct=self.controlCond[i][types]
            if not ct:
                count=count+1

        fun=self.funList[types]
        length=len(self.controlCond)
        if count!=length:
            pass
        else:
            self.cond[types]=False
            funt=self.funOnEndInstance[types]

            funt()

            
if __name__=='__main__':
        
    c=Controls()
    def fun():
            print("")

    def st():
        print("START")

    def of():
        print("OFF")
        
            
    types='kkr'
    c.funList[types]=fun
    c.funFirstOnList[types]=st
    c.funFirstOffList[types]=of

    us1='us1'
    us2='us2'
    c.funOpenWindow(us1)
    c.funOpenWindow(us2)
    def fts():
            c.funOnSending(us1,types)
            c.funOnSending(us2,types)
            
            c.funOffSending(us1,types)
            time.sleep(3)
            c.funOffSending(us2,types)

            
    fts()


        
