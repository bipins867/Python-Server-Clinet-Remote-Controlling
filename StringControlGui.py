import myStringLib as ms


def breakDownWord(word,limit=30,breakBy='\n'):
    length=len(word)
    st=[]

    for i in range(0,length,limit):
        d=word[i:i+limit]
        st.append(d)

    st=ms.mergeInString(st,breakBy)

    return st

def breakDownData(data,limit=30,breakBy='\n',distBy=' '):
    data=ms.distributeString(data,distBy)

    tdata=[]
    for i in data:
        if(len(i)>limit):
            fd=breakDownWord(i,limit,breakBy)+breakBy+' '
            tdata.append(fd)
        else:
            tdata.append(i+' ')
    tdata=ms.mergeInString(tdata,'')

    return tdata

def shortTheBigData(data,limit=35,repBy='...'):
    length=len(data)
    if length>limit:
        data=data[:7]+repBy+data[-7:]
        return data
    else:
        return data
