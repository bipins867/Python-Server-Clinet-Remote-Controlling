import myStringLib as ms
import StatementControl as stc
import re


types=['NM','CL','SL','WS','SB']

def isNum(char):
    if len(char)==1:
        p=ord(char)
        if p in range(48,58):
            return True
        else:
            return False

def isCapLetter(char):
    if len(char)==1:
        p=ord(char)
        if p in range(65,91):
            return True
        else:
            return False

def isSmallLetter(char):
    if len(char)==1:
        p=ord(char)
        if p in range(97,123):
            return True
        else:
            return False

def isSpace(char):
    if len(char)==1:
        if ord(char)==32:
            return True
        else:
            return False

def is_(char):
    if len(char)==1:
        if ord(char)==95:
            return True
        else:
            return False

def isSymbol(char):
    if len(char)==1:

        od=ord(char)

        if od>122:
            return True
        elif od>=0 and od<48:
            return True
        elif od>=58 and od<65:
            return True
        elif od>=91 and od<97:
            return True
        else:
            return False

def getTypeOfCharacter(char):

    if len(char)==1:
        if stc.isNum(char):
            return types[0]
        elif stc.isCapLetter(char):
            return types[1]
        elif stc.isSmallLetter(char):
            return types[2]
        elif stc.isSpace(char):
            return types[3]
        else:
            return types[4]

def isLetter(char):
    if len(char)==1:
        if isCapLetter(char) or isSmallLetter(char):
            return True
        else:
            return False


def isNumPresent(data):
    pattern='\d'

    if(re.search(pattern,data)):
        return True
    else:
        return False

def checkUser(data):
    pattern="[a-zA-Z0-9]"

    if re.match(pattern,data):
        return True
    else:
        return False

class LineEditControl:

    def __init__(self):
        pass

    def checkUserName(self,userName):
        txt=''
        if len(userName)>20 or len(userName)<3:
            txt="UserName length must be in range [3-20]"
        elif not(re.search('[a-zA-Z0-9]',userName)):
            txt='UserName must contain at least 1 letter'
        elif re.search('[^a-zA-Z0-9_]',userName):
            txt='UserName must not contain special character Except "_"'
        else:
            txt=True

        return txt

    def checkUserPassword(self,userPass):
        txt=''

        if len(userPass)>30 or len(userPass)<5:
            txt="Password length must be in range [5-30]"
        else:
            txt=True

        return txt

    def checkSequrityQuestion(self,seqQ):
        txt=''

        if len(seqQ)>50 or len(seqQ)<5:
            txt="SeqQ length must be in range [5-30]"
        else:
            txt=True

        return txt

    def checkSequrityAnswer(self,seqA):
        txt=''

        if len(seqA)>50 or len(seqA)<5:
            txt="SeqA length must be in range [5-20]"
        else:
            txt=True

        return txt

    def checkName(self,name):
        txt=''

        if len(name)>25 or len(name)<3:
            txt="Name length must be in range [3-25]"
        else:
            txt=True

        return txt

    def checkIdentity(self,data):
        txt=''

        if len(data)>20 or len(data)<1:
            txt="Identity length must be in range [1-20]"
        else:
            txt=True

        return txt

    def checkPNumber(self,name):
        txt=''

        if len(name)>15 or len(name)<5:
            txt="Number length must be in range [5-15]"
        elif (re.search('[^0-9+]',name)):
            txt='Number must contain only digits'
        else:
            if '+' in name:
                if name[0]!='+':
                    txt='Number symbol "+" must be in begening'
                else:
                    txt=True
            else:
                txt=True


        return txt

    def checkEmail(self,email):
        pattern='^[a-zA-Z0-9]+[\._]?[a-zA-Z0-9]+[@]\w+[.]\w{2,3}$'

        if (re.search(pattern,email)):
            return True
        else:
            return "Enter Valid Email"

    def checkDob(self,dob):
        pattern='\d{2,2}(\/)\d{2,2}(\/)\d{2,4}$'

        if (re.search(pattern,dob)):
            return True
        else:
            return "Enter Valid Date of birth in dd/mm/yyyy format"

    def checkDiscription(self,data):

        txt=''

        if len(data)==0:
            txt="Please Enter Something in discription...."
        else:
            txt=True

        return txt

    def checkGroupName(self,groupName):
        txt=''
        if len(groupName)>25 or len(groupName)<3:
            txt="GroupName length must be in range [3-25]"
        elif not(re.search('[a-zA-Z0-9]',groupName)):
            txt='GroupName must contain at least 1 letter'
        elif re.search('[^a-zA-Z0-9_]',groupName):
            txt='GroupName must not contain special character Except "_"'
        else:
            txt=True

        return txt

    def checkMeetingId(self,id,length=6):
        if len(id)!=length:
            txt=f"Id length must be {length}"
        elif (re.search('[^0-9]',id)):
            txt='Id must contain only digits'
        else:
            txt=True


        return txt

if __name__=='__main__':
    lec=LineEditControl()
    while True:
        data=input()
        print(lec.checkDob(data))
