#TrialJarvisDataBase

import dbquery2 as db
import time
import myStringLib as ms


mydb=db.genMdb()
cursor=mydb.cursor()
cb=db.cb1(cursor,'jar')
class DataBase:

    def __init__(self):
        pass


    def inputData(self,time,data):
        #The data must be in single row
        cb.insertDataN('timedata',[time,data[0],data[1],data[2],data[3]])
        
        mydb.commit()

    def deleteAllRecord(self):
        cb.deleteData('timedata')
        mydb.commit()

    def selectByType(self,typeVal,typeIn='_T1'):
        data=cb.selectAllCheckData('timedata',typeIn,typeVal)
        data=ms.modifySqlResult(data)
        return data
    
    def select1Data(self,time,_TimeInfo='_TimeInfo'):
        data=cb.selectAllCheckData('timedata',_TimeInfo,time)
        data=ms.modifySqlResult(data)
        return data

    def selectRangeData(self,time,r1,r2,_TimeInfo='_TimeInfo'):
        data=cb.selectRangeData('timedata',_TimeInfo,r1,r2)
        data=ms.modifySqlResult(data)
        return data
    
    def selectIntersection(self,values):
        val=[]
        for i in values:
            val.append(set(i))

        first=val[0]
        for i in range(1,len(val)):
            cur=val[i]
            ints=first.intersection(cur)
            if ints=={}:
                break
            first=ints

        if ints=={}:
            return None
        else:
            return first

    def restoreStatus(self,data):
        d=[]
        for i in range(len(data)):
            d.append(float(i))
d=DataBase()
