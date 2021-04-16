#XprtLoginControl

import myStringLib as ms


class Controller:

    def __init__(self):
        pass


    def checkUserName(self,name):
        cond=True
        if(len(name)>5 and len(name)<=20):    
            for i in name:
                if (i<='Z' and i>='A') or (i<='z' and i>='a') or(i<='9' and i>='0') or i=='_':
                    cond=True
                else:
                    cond=False
                    break
        else:
            cond=False
        return cond

    def checkUserPass(self,password):
        

        if(len(password)>6 and len(password)<=35):
            return True
        else:
            return False

    def checkImage(self,image):
        pass

    def checkName(self,name):
        cond=True
        if(len(name)>2 and len(name)<=20):    
            for i in name:
                if (i<='Z' and i>='A') or (i<='z' and i>='a') or i==' ':
                    cond=True
                else:
                    cond=False
                    break
        else:
            cond=False
        return cond

    def checkSeqQ(self,ques):
        if(len(ques)>8 and len(ques)<=100):
            return True
        else:
            return False

    def checkSeqA(self,ans):
        if(len(ans)>8 and len(ans)<=100):
            return True
        else:
            return False
    

    def checkTextMessage(self,message):
        if(len(ques)>0 ):
            return True
        else:
            return False

    
