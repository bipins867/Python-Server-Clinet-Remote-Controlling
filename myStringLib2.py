import string
import random
import myStringLib as ms
import numpy as np

def get_you_link(data):
        vids=data.findAll('a',attrs={'class':'yt-uix-tile-link'})
        videos=[]
        for v in vids:
                tmp = 'https://www.youtube.com' + v['href']
                videos.append(tmp)
        return videos

                
def get_all_mid_text(data,start,end):
        ddata=ms.distributeString(data,start)
        tdata=[]
        ddata=ddata[1:]
        for i in ddata:
                data=ms.get_lhs_data(i,end)
                data=ms.trimString(data,' ')
                tdata.append(data)
        return tdata


def check_word_2(data,word1,word2):

        f1=ms.check_word(data,word1)
        f2=ms.check_word(data,word2)

        if(f1 is False):

                if(f2 is False):
                        return [False,0]
                else:
                        return [f2,2]
        else:
               if(f2 is False):
                       return [f1,1]
               else:
                        if(f1>f2):
                                return [f2,2]
                        else:
                                return [f1,1]
                


def check_word(data,word):

        if(word in data):
                return data.index(word)
        else:
                return False

def get_lhs_data(data,end):
        index=data.index(end)

        return data[:index]


def get_rhs_data(data,start):
        index=data.index(start)

        len1=len(start)

        return data[index+len1:]



def find_get_text(strings,find,get_length):
        index=strings.index(find)

        data=strings[index+1:index+get_length]

        return data
def find_get_text2(strings,find,start,end):
        index=strings.index(find)
        data=strings[index:]
        index=data.index(end)
        rdata=data[:index]
        index=rdata.index(start)
        data=rdata[index+len(start):]
        data=ms.trimString(data,' ')
        return data

def find_mid_text(data,start,end):

        index1=data.index(start)
        index2=data.index(end)

        len1=len(start)

        rdata=data[index1+len1:index2]

        return rdata
        

def backAfter(num,ran):
        a=range(num-ran,num+ran)
        a=np.array(a)

        return a
        

def trimDisString(data,start,midd,last):
        data=data[start:-last]
        
        data=ms.distributeString(data,midd)
        return data
def genSeqArr(start,length,interval):
        x=[start]

        for i in range(0,length-1):
                x.append(x[len(x)-1]+interval)

        return x
        


def genRandArr(lenAr,length):
        data=[]
        for i in range(0,length):
                r=random.randint(0,len(lenAr)-1)
                d=genRandInt(lenAr[r])
                data.append(d)
        return data

def genRandInt(length,pn=True):
        zero=''
        maxi='9'
        for i in range(1,length):
                zero=zero+'0'
                maxi=maxi+'9'
        zero='1'+zero
        zero=int(zero)
        maxi=int(maxi)
        
        d=random.randint(zero,maxi)

        if(pn):
                c=random.randint(0,1)
                if(c==0):
                        return d
                else:
                        return -d
        else:
                return d

def checkAllA1inA2(a1,a2):

        cond=True

        for i in a1:
                if(i in a2):
                        cond=True
                else:
                        cond=False
                        break


        return cond

def modifySqlResult(result):
        res=result
        
        
        if( res is None or len(res)==0 ):
            return None
        else:
            nres=[]
            if(len(res[0])==1):
                
                for i in res:
                    nres.append(i[0])
                return nres
            else:
                return res
def fromArSetAr(array):

        xset=set(array)
        array=[]
        for i in xset :
                array.append(i)

        return array

def getTimesInAr(array,value):
        count=0
        for i in array:
                if(i==value):
                        count=count+1

        return count

def getCommonTimes(array,times):
        length=len(array)

        ar=[]
        for i in array:
                count=getTimesInAr(array,i)
                if(count==times):
                        ar.append(i)

        return ar


def getCommon(array):
        
        length=len(array)
        ar=[]
        for i in range(0,length):
                for j in range(0,length):
                        if(i==j):
                                continue
                        if(array[i]==array[j]):
                                ar.append(array[j])

        data=fromArSetAr(ar)

        return data


def checkCloserPos(posArr):
    posArr.sort()
    cond=None
    for i in range(0,len(posArr)):
        d=posArr[i]

        if(d-1 in posArr or d+1 in posArr):
            cond= True
            break
        else:
            cond= False

    return cond

def removeDublicate(array):
    sets=set(array)

    array=[]
    for i in sets:
        array.append(i)

    return array

def removeDublMul(mulAr):
    array=[]
    for i in mulAr:
        tup=tuple(i)
        array.append(tup)

    dub=removeDublicate(array)
    data=[]
    for i in dub:
        if(len(i)==1):
            data.append([i[0]])
        else:
            data.append(i)

    return data

def makeArrayPair(array1,array2):

    newAr=[]
    for i in array1:
        for j in array2:
            d=i+' '+j
            newAr.append(d)

    return newAr

def makeMulArrayPair(arrays):
    temp=[]

    for i in arrays:

        te=[]
        for  j in i:
            d=ms.replaceBy_String(j,' ','_')
            te.append(d)

        temp.append(te)
        
    arrays=temp
    arr=[]
    first=arrays[0]
    for i in range(1,len(arrays)):
        second=arrays[i]

        first=makeArrayPair(first,second)

    temp=[]
    for i in first:
        t2=[]
        d=ms.distributeString(i,' ')
       
        for i in d:
            t=ms.replaceBy_String(i,'_',' ')

            t2.append(t)
        temp.append(t2)
    return temp
        
    

def genRanStr(length=9):
    low=string.ascii_lowercase
    data=''

    for i in range(0,length):
        r=random.randint(0,2)
        d=''
        if(r==0):
            d=str(random.randint(0,9))
        else:
            t=random.randint(0,25)
            
            d=low[t]
        data=data+d

    return data
    

def space(numOfSpace):
    num=numOfSpace
    sp=''
    for i in range(0,num):
	    sp=sp+' '
    return sp


    
def equalWord(word1,word2,trim=True):
    
    
    if trim:
        
        word1=trimString(word1,' ')
        word2=trimString(word2,' ')
    len1=len(word1)
    len2=len(word2)
    con=[]
    if(len1 ==len2):
        for i in range(0,len1):
            l1=word1[i]
            l2=word2[i]

            
            if(l1==l2):
                con.append('t')
            elif(l1==l2.lower()):
                con.append('t')
            elif(l1==l2.upper()):
                con.append('t')
            else:
                
                con.append('f')
                break
            
    else:
        con.append('f')
    if('f' in con):
        return False
    else:
        return True

def inEqual(word,array):

    con=[]
    for i in array:
        if(equalWord(word,i)):
            con.append('t')
            break
        else:
            con.append('f')
            
    if('t' in con):
        return True
    else:
        return False



def inMultipleEqual(array1,array2):
    con=False
    for i in array1:
        if(ms.inEqual(i,array2)):
            con=True
            break

    return con


def removeAllSpaces(words,agent=' '):

    
    temp=''
    for i in range(0,len(words)):
            if(words[i]==agent):
                    pass
            else:
                    temp=temp+words[i]
    return temp
def trimString(words,agent):
    length=len(words)

    spacear=[]
    temp=''
    for i in range(0,length):

       if(words[i]==agent):
           pass
       else:
            spacear.append(i)
    
    temp=words[spacear[0]:spacear[len(spacear)-1]+1]

    return temp
    

def distributeString(words,agent=' '):
    words=trimString(words,' ')
    length=len(words)
    agentLen=len(agent)
    
    agar=[]
    temp=[]
    if(agent in words):
        
        for i in range(0,length-agentLen):
            if(words[i:i+agentLen]==agent):
                agar.append(i)
            

        for i in range(0,len(agar)):
            if(i==0):
                temp.append(words[0:agar[0]])
                
                if(len(agar)==1):
                    temp.append(words[agar[0]+agentLen:len(words)])
                else:
                    
                    temp.append(words[agar[0]+agentLen:agar[1]])
                
            elif(i==len(agar)-1):
                temp.append(words[agar[len(agar)-1]+agentLen:length])
            else:
                temp.append(words[agar[i]+agentLen:agar[i+1]])
    else:
        temp.append(words)
    newTemp=[]

    for i in temp:
        if(len(i)==0):
            pass
        else:
            
            newTemp.append(i)
    return newTemp



def inRangeString(words,agent1,agent2):
    tem=''
    ind1=words.index(agent1)
    ind2=words.index(agent2)
    temp=words[ind1+1:ind2]
    return temp

def mergeString(word,agent):
    temp=''
    if(len(word)==1):
        temp=word[0]+agent
    else:
        for i in word:
            temp=temp+i+agent

    return temp

def mergeInString(word,agent):
    temp=''
    if(len(word)==1):
        temp=word[0]+agent
    else:
        for i in word:
            temp=temp+i+agent
    temp=temp[:-len(agent)]
    return temp




def sortOut(array1,array2):
    
    newar=array1+array2
    xar=set(newar)

    newar=[]
    for i in xar:
        newar.append(i)

    return newar

def oddOut(array1,array2):
    newar=[]
    
    if(array1==None):
        
        return array2
    else:
        for i in array2:
            if(inEqual(i,array1)):
                pass
            else:
                newar.append(i)

        return newar

def makePair(array1,array2):
    newar=[]

    for i in array1:
        for j in array2:
            st=str(i)+'_'+str(j)
            newar.append(st)

    xar=set(newar)
    newar=[]
    for i in xar:
        newar.append(i)

    return newar
def makeArrayFromTuple(tuples):
    arr=[]
    for i in tuples:
        arr.append(i)

    return arr

def makeDictionary(data):

    dic={}

    for i in data:
        dic.__setitem__(i[0].lower(),i[1].lower())

    return dic

def returnRandomFromArray(array):
    length=len(array)

    r=random.randint(0,length-1)

    return array[r]

def slashMakerDataIdentity(data,identity):
    
    if(data is None):
        merge=ms.mergeString(identity,'/')
        return merge
    elif(len(data) ==0):
        merge=ms.mergeString(identity,'/')
        return merge
    else:
        dis=ms.distributeString(data,'/')
        sort=ms.sortOut(dis,identity)
        mergeData=ms.mergeString(sort,'/')
        return mergeData


def slashAddData(data1,data2):

    if(data1 is None or len(data1) ==0):
        merge=ms.mergeString(identity,'/')
        return merge
    else:
        dis=ms.distributeString(data1,'/')

        newAr=dis+[data2]

        xyset=set(newAr)

        newAr=[]
        for i in xyset:
            newAr.append(i)
        mer=ms.mergeString(newAr,'/')
        return mer




def checkArrayEquality(array1,array2):
    val=False
    for i in array1:
        con=ms.inEqual(i,array2)
        if(con):
            val=True
            break
    return val


def commonOut(array1,array2):
    val=None

    for i in array1:
        for j in array2:
            if(ms.equalWord(i,j)):
                val=i
                break

    return val


def commonAllOut(array1,array2):
    val=[]

    for i in array1:
        if(ms.inEqual(i,array2)):
            val.append(i)

    if(len(val)==0):
        return None
    else:
        return val


def getWordPos(sentence,agentWord):
    dis=ms.distributeString(sentence,' ')

    array=[]
        
    for i in range(0,len(dis)):
        if(ms.equalWord(dis[i],agentWord)):
            array.append(i)

    if(len(array) ==0):
        return None
    else:
        return array

     
def mergeInsideString(string,pos,agent):
    length=len(string)
    sen=''

    for i in  range(0,length):
        if(i==pos):
            sen=string[i-1]+'_'+string[i]+'_'+string[i+1]
            
    pre=string[0:pos-1]
    
    mergePre=ms.mergeInString(pre,' ')
    post=string[pos+2:]
    
    mergePost=ms.mergeInString(post,' ')
    newString=mergePre+' '+sen+' '+mergePost

    dis=ms.trimString(newString,' ')
    dis=ms.distributeString(dis,' ')

    return dis

def mergeInsideLeftString(string,pos,agent):
    length=len(string)
    sen=''

    for i in  range(0,length):
        if(i==pos):
            sen=string[i-1]+'_'+string[i]
            
    pre=string[0:pos-1]
    
    mergePre=ms.mergeInString(pre,' ')
    post=string[pos+1:]
    
    mergePost=ms.mergeInString(post,' ')
    newString=mergePre+' '+sen+' '+mergePost

    dis=ms.trimString(newString,' ')
    dis=ms.distributeString(dis,' ')

    return dis
    
    
def replaceBy_String(string,word,agent='_'):
    
    dis=ms.distributeString(string,word)

    data=ms.mergeInString(dis,agent)
    return data

def replaceEqualPosition(remPos,fromPos):
    pos=[]
    for i in remPos:
        if(i in fromPos):
            fromPos.remove(i)


    return fromPos

def checkNumDiff(num1,num2,diff=1):
    dif=num1-num2
    if(diff==abs(dif)):
        return True
    else:
        return False

def nameFormation(sentence):
    dis=ms.distributeString(sentence)
    upper=string.ascii_uppercase

    na=[]
    sen=''
    
    for i in range(0,len(dis)-1):
        first=False
        second=False
        if(dis[i][0] in upper):
            first=True

        if(dis[i+1][0] in upper):
            second=True


        if(first and second):
            sen=sen+dis[i]+'__?'
        else:
            sen=sen+dis[i]+' '

    sen=sen+dis[len(dis)-1]


    return sen
  
def modifySentence(sentence):

    return '_a '+sentence+' a_'

def removeSentence(sentence):
    return sentence[3:len(sentence)-3]
