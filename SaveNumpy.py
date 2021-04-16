import NeuralNetwork as nn
import os
import numpy as np
import shutil
import time


path='C:\\Python\\Numpy_Database\\'


def save(n,show=False,update=False,fName=None):
    if not update:
        fName=time.time()
        fName=str(fName)
    else:
        location=path+fName
        shutil.rmtree(location)
    os.mkdir(path+fName)
    location=path+fName+'\\'
    if show:
        print("Data saving started")
    hidden_bias=n.hidden_bias
    hidden_weight=n.hidden_weight

    hb=[]
    hw=[]
    for i in hidden_bias:
        k=i.tolist()
        
        hb.append(k)
    for i in hidden_weight:
        k=i.tolist()
      
        hw.append(k)
    
    np.save(location+'aInput',n.trained_input)
    np.save(location+'bOutput',n.trained_output)
    np.save(location+'cLr',n.learning_rate)
    np.save(location+'dHidden_bias',hb)
    np.save(location+'eHidden_weight',hw)
    np.save(location+'fOuptut_bias',n.output_bias)
    np.save(location+'gOutput_weight',n.output_weight)
    if show:
        
        print("Data saving completed")
   
    return fName

def update(fName,n):
    save(n,update=True,fName=fName)

def restore(fName,show=False):
    location=path+fName
    fName=os.listdir(location)
    tfName=[]
    for i in fName:
        tfName.append(location+'\\'+i)
    fName=tfName
    if show:
        print("Data is started loading from database")
    trained_input=np.load(fName[0],allow_pickle=True)
    trained_output=np.load(fName[1],allow_pickle=True)
    learning_rate=np.load(fName[2],allow_pickle=True)
    hidden_bias=np.load(fName[3],allow_pickle=True)
    hidden_weight=np.load(fName[4],allow_pickle=True)
    output_bias=np.load(fName[5],allow_pickle=True)
    output_weight=np.load(fName[6],allow_pickle=True)

    if show:
        print("Data loading completed")
        print("Now serielizing the data")

    length=len(hidden_bias)
    array=[]
    for i in range(length):
        array.append(len(hidden_bias[i][0]))
    n=nn.NeuralNetwork(trained_input,trained_output,length,array,2,learning_rate,fl=False)
    n.train_data()
    
    hidden_bias=hidden_bias.tolist()
    hidden_weight=hidden_weight.tolist()
    hb=[]
    hw=[]
    
    for i in hidden_bias:
        
        hb.append(np.array(i))
    for i in hidden_weight:
        
        hw.append(np.array(i))
    

    n.hidden_bias=hb
    n.hidden_weight=hw
    n.output_bias=output_bias
    n.output_weight=output_weight

    n.fp()
    if show:
        print("Data restoring completed")

    return n
    
