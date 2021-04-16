import numpy as np
import NeuralNetwork as nn
import time
import random


trained_input=[[0,0,0,0]]
trained_output=[[0,0]]

n=nn.NeuralNetwork(trained_input,trained_output,2,[4,4],2,1)
n.train_data()

val=0

def universalCondition(input,output):
    global val

    d=nn.sep_listData(output,0,1,0.5)
    
    d1=d[0]
    d2=d[1]

    cond=False

    input=input[0]

    if d1==1 and d2==0:
        if input[0]==1:
            cond=True
        else:
            n.think_and_change([input],[[1,0]])

    elif d1==0 and d2==1:
        if input[1]==1:
            cond=True
        else:
            n.think_and_change([input],[[0,1]])

    elif d1==1 and d2==1:
        if input[2]==1:
            cond=True
        else:
            n.think_and_change([input],[[1,1]])
    else:
        if input[3]==1:
            cond=True
        else:
            n.think_and_change([input],[[0,0]])

    if cond:
        val=val+1
    else:
        val=val-1

    


def hisMovment(input):
    output=n.think_only(input)
    output=output.tolist()[0]
    return output

def initiate_for_one_time():
    rarray=[0,0,0,0]
    r=random.randint(0,3)
    rarray[r]=1

    
    d=[rarray]
    output=hisMovment(d)
   
    universalCondition(d,output)

j=0
while True:
    j=j+1
    for i in range(1000):
        
        initiate_for_one_time()

    print(j,val)
    time.sleep(2)
    
