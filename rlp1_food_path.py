import numpy as np
import NeuralNetwork as nn
import time
import random

length=4

trained_input=[[1,0,0,0],
               [0,1,0,0],
               [0,0,1,0],
               [0,0,0,1]]

trained_output=trained_input

nFood=nn.NeuralNetwork(trained_input,trained_output,2,[4,4],2,1)
nPath=nn.NeuralNetwork(trained_input,trained_output,2,[4,4],2,1)

nFood.train_data()
nPath.train_data()

energy_level=2 #0=Low and 1,2, half and 3 is full of energy


def generateMovmentCondition():
    a=[0,0,0,0]

    r1=random.randint(0,1)
    r2=random.randint(2,3)

    a[r1]=1
    a[r2]=1

    return a

def hisMovement(input):
    global energy_level
    out=[]
    mv=0
    if energy_level<=0  :
        out=nFood.think_only(input)
        #print("FOOD ONLY")
        mv=0
    elif energy_level>=3:
        out=nPath.think_only(input)
        mv=1
        #print("PATH ONLY")
    else:
        r=random.randint(0,1)

        if r==0:
            mv=2
            out=nFood.think_only(input)
        else:
            mv=3
            out=nPath.think_only(input)
        #print("s!2k ",mv)
    out=out.tolist()[0]
    return [out,mv]
    

def universalCondition(input,output):
    global energy_level
    mv=output[1]
    output=output[0]
    d=nn.sep_listData(output,0,1,0.5)
    maxd=max(d)
    index=d.index(maxd)
    
    ot=[]
    if mv==0 or mv==2:
        ins=input
        #print(ins)
        #Food Upgradation
        
        if ins[2]==1:
            if index==2:
                energy_level=energy_level+1
                ot=[0,0,1,0]
            else:
                energy_level=energy_level-1
                ot=[0,0,1,0]
            
        elif ins[3]==1:
            if index==3:
                energy_level=energy_level+1
                ot=[0,0,0,1]
            else:
                energy_level=energy_level-1
                ot=[0,0,0,1]
        nFood.think_and_change([input],[ot])
    else:
        ins=input
        #print(ins)
        energy_level=energy_level-1
        #Path Upgradation
        if ins[0]==1:
            if index==0:
                ot=[1,0,0,0]
            else:
                ot=[1,0,0,0]
            
        elif ins[1]==1:
            if index==1:
                ot=[0,1,0,0]
            else:
                ot=[0,1,0,0]

        nPath.think_and_change([input],[ot])
    #print("move :-",mv)


def initiate_first_movment():
    global energy_level
    a=generateMovmentCondition()
    
    output=hisMovement(a)
    #print("Energy Level:-",energy_level)
    

    universalCondition(a,output)
