#FileIOManager

import DataShare as ds
import os
import myStringLib as ms
import time



class OperateFiles:

    def __init__(self):
        pass

    def checkFileExist(self,fileName):
        try:
            open(fileName)
            return True
        except:
            return False

    def getFileSize(self,fileName):
        sizes=os.stat(fileName).st_size

        return sizes

    def getActualFileName(self,file):
        dfile=file[::-1]
        index=None
        try:
            index=dfile.index('\\')
        except:
            try:
                index=dfile.index('/')
            except:
                index=None


        if index==None:

            file=ms.replaceBy_String(file,' ','_')
            return file
        else:
            cu=len(file)-(1+index)
            fName=file[cu+1:]
            fName=ms.replaceBy_String(fName,' ','_')
            return fName

    def attachFileWithtime(self,fileName):
        file=self.getActualFileName(fileName)
        t=str(time.time())
        t=ms.replaceBy_String(t,'.','_')
        file=t+'-'+file
        return file

    def calculateFilePercentage(self,fileTempSize,fileActualSize):
        st=fileTempSize/fileActualSize*100
        return st

    def seprateFileWithTime(self,fileName):

        data=ms.distributeString(fileName,'-')

        if len(data)==2:
            t=data[0]
            fName=data[1]
            t=ms.replaceBy_String(t,'_','.')
            t=float(t)
            return [t,fName]
        else:
            return None

    def getFileLocation(self,fileName):
        dfile=file[::-1]
        index=None
        try:
            index=dfile.index('\\')
        except:
            try:
                index=dfile.index('/')
            except:
                index=None


        if index==None:

            loc=os.popen('cd').read()[:-1]
            return loc
        else:
            loc=len(fileName)
            tloc=loc-index
            return fileName[:tloc]

    def getFileNameOnly(self,fileName):
        aFile=self.getActualFileName(fileName)
        tindex=aFile[::-1].index('.')
        ln=len(fileName)-tindex
        return fileName[:ln-1]

    def getFileExtensionOnly(self,fileName):
        aFile=self.getActualFileName(fileName)
        tindex=aFile[::-1].index('.')
        ln=len(fileName)-tindex
        return fileName[ln:]

    def encFile(self,fileName,ext='.xpef'):
        location=self.getFileLocation(fileName)
        actFileName=self.getActualFileName(fileName)
        nameOnly=self.getFileNameOnly(actFileName)

        newLoc=location+nameOnly+ext

        f1=open(fileName,'rb')
        f2=open(newLoc,'wb')

        d=b''

        while True:

            d=f1.read(1024*1024*5)
            if d==b'':
                break
            ed=ds.encb(d)
            f2.write(ed)

        f2.close()
        f1.close()

    def decFile(self,fileName,ext='.txt'):
        location=self.getFileLocation(fileName)
        actFileName=self.getActualFileName(fileName)
        nameOnly=self.getFileNameOnly(actFileName)

        newLoc=location+nameOnly+ext

        f1=open(fileName,'rb')
        f2=open(newLoc,'wb')

        d=b''

        while True:

            d=f1.read(1024*1024*5)
            if d==b'':
                break
            ed=ds.decb(d)
            f2.write(ed)

        f2.close()
        f1.close()

    def deletFile(self,fileName):
        command='del "'+fileName+'"'
        os.popen(command)

    def getByteToMb(self,size):

        size=size/1024
        size=size/1024

        return size

    def getByteToGb(self,size):
        size=self.getByteToMb(size)
        size=size/1024
        return size

if __name__=='__main__':

    op=OperateFiles()

    file='C:\\Users\\Bipin\\Desktop\\king.xpef'


    op.decFile(file,'.tke')
