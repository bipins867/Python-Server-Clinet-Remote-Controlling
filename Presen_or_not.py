import cv2
import NeuralNetwork as nn
import numpy as  np

#By the canny edge detector
cap=cv2.VideoCapture(0)

size=4
trained_input=[]
trained_output=[]
c=0
t=0
s=0

while True:

    _,frame=cap.read()


    h,w=frame.shape[:2]
    h=int(h/size)
    w=int(w/size)

    img=cv2.resize(frame,(w,h))
    cv2.imshow('Original',frame)

    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    l1=cv2.Canny(gray,150,150)

    cv2.imshow('L1',l1)
    #l1=gray
    wkey=cv2.waitKey(1)
    
        
    if wkey & 0xff==ord('s'):
        ar=nn.cvtImg2Mat(l1,True)
        trained_input.append(ar)
        trained_output.append([1,0,0])
        s=s+1
        print('s ',s)
        
        
        
        
    if wkey & 0xff==ord('c'):
        ar=nn.cvtImg2Mat(l1,True)
        trained_input.append(ar)
        trained_output.append([0,1,0])
        c=c+1
        print('c ',c)

    if wkey & 0xff==ord('t'):
        ar=nn.cvtImg2Mat(l1,True)
        trained_input.append(ar)
        trained_output.append([0,0,1])
        t=t+1
        print('t ',t)
    
    if wkey & 0xff==ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
print(len(trained_input))
'''
trained_input=np.array(trained_input)
trained_output=np.array(trained_output)

trained_input=np.concatenate((trained_input,trained_input))
trained_output=np.concatenate((trained_output,trained_output))

trained_input=np.concatenate((trained_input,trained_input))
trained_output=np.concatenate((trained_output,trained_output))

trained_input=np.concatenate((trained_input,trained_input))
trained_output=np.concatenate((trained_output,trained_output))

trained_input=np.concatenate((trained_input,trained_input))
trained_output=np.concatenate((trained_output,trained_output))

trained_input=np.concatenate((trained_input,trained_input))
trained_output=np.concatenate((trained_output,trained_output))



print('hi')
i=8
def fun():
    global i
    n=nn.NeuralNetwork(trained_input,trained_output,3,[1000,1000,1000],1000,True)
    n.train_data()
    output=n.output
    print(i)
    i=i+3
    return [n,output]
data=fun()
print(data[1])

'''

input("Train your data")


n=nn.NeuralNetwork(trained_input,trained_output,3,[512,256,128],1000,1e-4,True)
n.train_data()
print(n.output)


input('Want to start testing')



cap=cv2.VideoCapture(0)


while True:

    _,frame=cap.read()


    h,w=frame.shape[:2]
    h=int(h/size)
    w=int(w/size)

    img=cv2.resize(frame,(w,h))
    cv2.imshow('Original',frame)

    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    l1=cv2.Canny(gray,150,150)
    #l1=gray
    #cv2.imshow('L1',l1)
    
    ar=nn.cvtImg2Mat(l1 ,True)

    data=n.think_only(ar)
    data=data[0].tolist()
    maxd=np.max(data)
    index=data.index(maxd)

    if(index==0):
        #s
        print('#1')
    elif(index==1):
        #c
        print('Boy')
    else:
        #t
        print('Without Hand')
    wkey=cv2.waitKey(1)
    
    if wkey & 0xff==ord('q'):
        break


cap.release()
cv2.destroyAllWindows()

