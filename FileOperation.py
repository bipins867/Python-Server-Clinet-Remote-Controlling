#FileOperation

from cryptography.fernet import Fernet
import myStringLib as ms
import os
import zipfile as zf

key=b'eQ5jxFcJNYII5Z4vhBtvT-mNiqx64yQEUln1SOoYEDA='
fernet=Fernet(key)



def all_folder(folder,arP=[],arF=[]):

    if(os.path.isdir(folder)):
        arP.append(folder)
        dirs=os.listdir(folder)
        tdir=[]
        for i in dirs:
            tdir.append(folder+'\\'+i)

        for i in tdir:
            all_folder(i,arP,arF)

    else:
        arF.append(folder)

def get_file_name(file):
        dfile=file[::-1]
        file=ms.replaceBy_String(file,'/','\\')
        
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
            return [index,file]
        else:
            cu=len(file)-(1+index)
            fName=file[cu+1:]
            fName=ms.replaceBy_String(fName,' ')
            return [index,fName]

def get_mb(size):

        size=size/1024
        size=size/1024

        return size



def encrypt_File(file,dstFile):
    f=open(file,'rb')
    size=os.stat(file)
    size=size.st_size
    size=get_mb(size)
    data=b''

    chunk=0
    if(size<3):
        chunk=1024
    elif(size<50):
        chunk=1024*1024
    elif(size<500):
        chunk=1024*1024*10
    else:
        chunk=1024*1024*50
    print(file,round(size,4),'.mb')
    d=f.read(chunk)
    while True:
        if d==b'':
            break
        data=data+d
        d=f.read(chunk)
    data=fernet.encrypt(data)
    f.close()

    f=open(dstFile,'wb')

    f.write(data)
    f.close()


def dencrypt_File(file,dstFile):
    f=open(file,'rb')
    size=os.stat(file)
    size=size.st_size
    size=get_mb(size)
    data=b''

    chunk=0
    if(size<3):
        chunk=1024
    elif(size<50):
        chunk=1024*1024
    elif(size<500):
        chunk=1024*1024*10
    else:
        chunk=1024*1024*50
    print(file,round(size,4),'.mb')
    d=f.read(chunk)
    while True:
        if d==b'':
            break
        data=data+d
        d=f.read(chunk)
    data=fernet.dencrypt(data)
    f.close()

    f=open(dstFile,'wb')

    f.write(data)
    f.close()

def create_Folder_Zip(folder,fileZip):
    fNames=get_file_name(folder)
    if fNames is None:
        tName=fNames
    else:
        tName=folder[:len(folder)-len(fNames[1])]
        
        os.chdir(tName)
    def zipdir(path, ziph):
    # ziph is zipfile handle
        for root, dirs, files in os.walk(path):
            for file in files:
                ziph.write(os.path.join(root, file))
    zipf=zf.ZipFile(fileZip,'w')
    zipdir(fNames[1],zipf)
    zipf.close()
    

def extract_Zip(fileZip,folder):
    with zf.ZipFile(fileZip) as zps:
        zps.extractall(folder)

        
