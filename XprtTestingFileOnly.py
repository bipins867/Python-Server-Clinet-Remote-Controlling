import TestingDataSharePh1 as ds
import myStringLib as ms
import AssembleData as ad
import FileIOManager as fm

op=fm.OperateFiles()

class FileControl:

    def __init__(self,c):
        self.c=c

        self.sWindow=[]

        self.sWinSend={}
        self.sWinRecv={}

        self.files={}




    def getSetWindow(self,sWin):
        if sWin not in self.sWindow:
            self.sWindow.append(sWin)
            self.sWinSend[sWin]=[]
            self.sWinRecv[sWin]=[]

    def onSendStart(self,sWin,fileName):

        self.setSendFile(sWin,fileName)

    def onSendEnd(self,sWin,fileName):

        if fileName in self.sWinSend[sWin]:
            self.sWinSend[sWin].remove(fileName)
            del self.files[fileName]

    def onRecvStart(self,sWin,fileName):
        self.setRecvFile(sWin,fileName)

    def onRecvEnd(self,sWin,fileName):
        if fileName in self.sWinRecv[sWin]:
            self.sWinRecv[sWin].remove(fileName)
            del self.files[fileName]

    def getAllFilesOfSend(self,sWin):
        if sWin in self.sWinSend:
            return self.sWinSend[sWin]

    def getAllFilesOfRecv(self,sWin):
        if sWin in self.sWinRecv:
            return self.sWinRecv[sWin]

    def setSendFile(self,sWin,fileName):

        self.sWinSend[sWin].append(fileName)

        self.files[fileName]='s'


    def setRecvFile(self,sWin,fileName):
        self.sWinRecv[sWin].append(fileName)
        self.files[fileName]='r'

    def isFileSend(self,sWin,fileName):
        if fileName in self.sWinSend[sWin]:
            return True
        else:
            return False


    def isFileRecv(self,sWin,fileName):
        if fileName in self.sWinRecv[sWin]:
            return True
        else:
            return False

    def getFileSttr(self,fileName):

        if fileName in self.files:
            return self.files[fileName]


    def getSendFileFlow(self,fileName):
        if fileName in self.c.send.fileFlow:
            return self.c.send.fileFlow[fileName]

    def getSendFileTempSize(self,fileName):
        if fileName in self.c.send.fileTempSize:
            return self.c.send.fileTempSize[fileName]

    def getSendFileSize(self,fileName):
        if fileName in self.c.send.fileSize:
            return self.c.send.fileSize[fileName]

    def getRecvFileSize(self,fileName):
        if fileName in self.c.recv.fileSize:
            return self.c.recv.fileSize[fileName]

    def getRecvFileTempSize(self,fileName):
        if fileName in self.c.recv.fileTempSize:
            return self.c.recv.fileTempSize[fileName]

    def getRecvFileStatus(self,fileName):
        if fileName in self.c.recv.fileStatus:
            return self.c.recv.fileStatus[fileName]

    def removeDublFromArray(self,array):
        if array is not None:
            ass=set(array)
            ar=[]
            [ar.append(i) for i in ass]
            return ar
