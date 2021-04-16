import NeuralNetwork as nn
import numpy as np
import myStringLib as ms
import dbquery as db
import time

mydb=db.genMdb()
mycursor=mydb.cursor()


def mergeData(data):

    data=str(data)

    return data


def restoreBias(data):
    data=ms.trimString(data,' ')
    data=ms.distributeString(data[1:-1],'\n')

    for i in range(len(data)):

        data[i]=ms.trimString(data[i],' ')
        data[i]=ms.distributeString(data[i][1:-1],', ')
        temp=[]

        for k in data[i]:
            temp.append(float(k))

        data[i]=temp


    return data

def restoreWeight(data):
    data=ms.trimString(data,' ')
    data=ms.distributeString(data[1:-1],'], [')

    for i in range(len(data)):
        
        data[i]=ms.trimString(data[i],' ')
        data[i]=ms.removeAllSpaces(data[i],'[')
        data[i]=ms.removeAllSpaces(data[i],']')
        
        data[i]=ms.distributeString(data[i],', ')
        temp=[]

        for k in data[i]:
            temp.append(float(k))

        data[i]=temp


    return data

def genTable(layers):
    columns=['sno','input','output','lr','ob','ow']

    t=[]
    for i in range(layers):
        d=['hb'+str(i),'hw'+str(i)]
        t=t+d
    columns=columns+t

    dtime=str(time.time())
    table=ms.replaceBy_String(dtime,'.')

    cb=db.cb1(mycursor,'abc')

    cb.createTableTextSize(table,columns)
    return table

def assembleData(n):
    trained_input=n.trained_input.tolist()
    trained_output=n.trained_output.tolist()
    hidden_bias=n.hidden_bias
    hidden_weight=n.hidden_weight

    output_bias=n.output_bias.tolist()
    output_weight=n.output_weight.tolist()

    no_of_hidden_layer=n.no_of_hidden_layer
    learning_rate=n.learning_rate

    values=['1',str(trained_input),str(trained_output),str(learning_rate),str(output_bias),str(output_weight)]

    t=[]
    for i in range(no_of_hidden_layer):
        bias=hidden_bias[i].tolist()
        weight=hidden_weight[i].tolist()

        d=[str(bias),str(weight)]
        t=t+d

    values=values+t

    return values

def save(n):
    
    tableName=genTable(n.no_of_hidden_layer)
    values=assembleData(n)

    cb=db.cb1(mycursor,'abc')

    cb.insertDataN(tableName,values)
    mydb.commit()
    return tableName

def update(tableName,n):

    cb=db.cb1(mycursor,'abc')
    cb.deleteData(tableName)
    values=assembleData(n)
    mydb.commit()
    cb.insertDataN(tableName,values)


def restore(tableName):
    cb=db.cb1(mycursor,'abc')
    data=cb.selectAllData(tableName)
    data=data[0]
    trained_input=data[1]
    trained_output=data[2]
    
    learning_rate=data[3]
    output_bias=data[4]
    output_weight=data[5]


    rdata=data[6:]
    hidden_bias=[]
    hidden_weight=[]
    for i in range(0,len(rdata),2):
        hidden_bias.append(rdata[i])
        hidden_weight.append(rdata[i+1])


    trained_input=restoreWeight(trained_input)
    trained_output=restoreWeight(trained_output)
    learning_rate=float(learning_rate)
    output_bias=restoreBias(output_bias)
    output_weight=restoreWeight(output_weight)

    for i in range(len(hidden_bias)):
        hidden_bias[i]=restoreBias(hidden_bias[i])
        hidden_weight[i]=restoreWeight(hidden_weight[i])

  #  return [trained_input,trained_output,learning_rate,output_bias,output_weight,hidden_bias,hidden_weight]
    trained_input=np.array(trained_input)
    trained_output=np.array(trained_output)
    output_bias=np.array(output_bias)
    output_weight=np.array(output_weight)

    length=len(hidden_bias)
    for i in range(length):
        hidden_bias[i]=np.array(hidden_bias[i])
        hidden_weight[i]=np.array(hidden_weight[i])

    ar=[]

    for i in range(length):
        ar.append(len(hidden_bias[i][0]))

    n=nn.NeuralNetwork(trained_input,trained_output,length,ar,2,learning_rate)
    n.train_data()
    n.hidden_bias=hidden_bias
    n.hidden_weight=hidden_weight
    n.output_bias=output_bias
    n.output_weight=output_weight

    n.fp()

    return n

