#File Insersion


class File:

    def __init__(self,fileName):

        self.fileName=fileName



    def write(self,data):

        f=open(self.fileName,'w')

        data=f.write(data)

        f.close()
        return data


    def append(self,data):

        f=open(self.fileName,'a')

        data=f.write(data)

        f.close()
        return data



    def read(self):
        f=open(self.fileName,'r')

        cond=True
        data=''
        while cond:

            d=f.read(1000000)
            if d=='':
                cond=False
            data=data+d
        return data


    def writeb(self,data):

        f=open(self.fileName,'wb')

        data=f.write(data)

        f.close()
        return data



    def appendb(self,data):

        f=open(self.fileName,'ab')

        data=f.write(data)

        f.close()
        return data



    def readb(self):
        f=open(self.fileName,'rb')

        cond=True
        data=bytes()
        while cond:

            d=f.read(100000)
            if d==b'':
                cond=False
            data=data+d
        return data
