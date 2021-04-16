#jks
import NeuralNetwork as nn
import random
import time

def fun(ar):
    s=sum(ar)
    if s>=1:
        return True
    else:
        return False


def genRandom():
    a=[random.randint(0,1),random.randint(0,1)]
    return a


life=True

count=1
while life:
    count=count+1
    r=genRandom()
    print(r,fun(r))
    if count==1000:
        life=False

    time.sleep(0.5)
    
