#Variables
import threading 



class Var:

    def __init__(self,var,func):
        self.var=var
        self.func=func

        self.dvar=var
        self.t1=None
        

    def alert(self):
        self.fun()
        self.var=self.dvar

    def check(self):
        while True:
            if(self.dvar.get()!=self.var.get()):
                self.alert()


    def start(self):
        self.t1=threading.Thread(target=self.check)
        self.t1.start()

    def stop(self):
        self.t1.stop()
