import myStringLib as ms

class Assembler:

    def __init__(self):
        pass








def check_user_name(name):

    def check(data):
        c=True
        for i in data:
            if((i>='a' and i<='z') or (i>='A' and i<='Z')\
               or i=='_' or \
               (i>=str(0) and i<=str(9))):
                pass
            else:
                c=False

        return c
    #Length 30
    #capital or small letter
    #Use of _ only

    length=len(name)

    if(length<=30 and length>=4):
        cond=check(name)

        if cond:
            return True
        else:
            return False
            
    else:
        return False

def check_password(passw):
    #1Capital
    #1Small
    #1Symbol
    #1Number
    #len =6

    length=len(passw)
    if length>=6:
        return True

    else:
        return False
