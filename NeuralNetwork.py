import numpy as np
import cv2
import subprocess
import NeuralNetwork as nn

class NeuralNetwork:

    def __init__(self,trained_input,trained_output,no_of_hidden_layer,perceptron_Array,times_to_train,learning_rate=1e-3,show_per=False,fl=True,name=None):
        self.times_to_train=times_to_train
        self.trained_input=np.array(trained_input)
        self.trained_output=np.array(trained_output)
        self.no_of_hidden_layer=no_of_hidden_layer
        self.perceptron_Array=perceptron_Array
        self.name=name
        
        self.show_per=show_per
        
        self.hidden_weight=[]
        self.hidden_bias=[]

        self.output_weight=[]
        self.output_bias=[]
        self.learning_rate=learning_rate
        #np.random.seed(1)
        self.fl=fl
        #For training the data

        self.hidden_layer_input=[]
        self.hidden_layer_value=[]
        self.hidden_layer_activation=[]

        self.output_layer_input=[]
        self.output_layer_value=[]
        self.output=[]
        
        self.slope_output=[]
        self.slope_hidden=[]

        self.d_output=[]
        self.d_hidden=[]

        self.E=0
        self.error_hidden=[]

        self.count=0
        self.fitness1=0
        self.fitness2=0
        self.fitness3=0
        
        self.train_first_time()
        self.forward_propogation()
        self.backward_propogation()
    def sigmoid(self,x):

        return 1/(1+np.exp(-x))


    def deravative(self,x):

        return x*(1-x)

    def setAnother(self,n):
        self.hidden_bias=n.hidden_bias
        self.hidden_weight=n.hidden_weight
        self.output_bias=n.output_bias
        self.output_weight=n.output_weight

        self.fp()
        self.bp()
        

    def train_first_time(self):
        self.generate_bias_weight()
        self.fp()
        self.bp()

    def updateDB(self):
        self.fp()
        self.bp()

    def accuracy(self):
        data=self.think_only(self.trained_input)
        data=np.round_(data,2)
        output=self.trained_output
        output=np.round_(output,2)
        acc=np.sum(data)/np.sum(output)
        print("This is falure system")
        return acc*100
        
    def loss(self):
        data=self.think_only(self.trained_input)
        data=np.round_(data,2)
        output=self.trained_output
        output=np.round_(output,2)
        sums=np.sum(output)
        print("This is falure system")
        loss=(sums-np.sum(data))/sums
        return loss*100
    
    def fp(self):
        if(self.no_of_hidden_layer==0):
            self.output_layer_input=np.dot(self.trained_input,self.output_weight)
            self.output_layer_value=self.output_layer_input+self.output_bias
            self.output=self.sigmoid(self.output_layer_value)
            
            
            
        else:

            for i in range(self.no_of_hidden_layer):
               
                if(i==self.no_of_hidden_layer-1):
                    if(self.no_of_hidden_layer==1):
                        self.hidden_layer_input=np.dot(self.trained_input,self.hidden_weight[0])
                        self.hidden_layer_value=self.hidden_layer_input+self.hidden_bias[0]
                        self.hidden_layer_activation.append(self.sigmoid(self.hidden_layer_value))
                    else:
                        
                            
                        self.hidden_layer_input=np.dot(self.hidden_layer_activation[-1],self.hidden_weight[-1])
                        self.hidden_layer_value=self.hidden_layer_input+self.hidden_bias[-1]
                        self.hidden_layer_activation.append(self.sigmoid(self.hidden_layer_value))
                elif(i==0):
                    self.hidden_layer_input=np.dot(self.trained_input,self.hidden_weight[0])
                    self.hidden_layer_value=self.hidden_layer_input+self.hidden_bias[0]
                    self.hidden_layer_activation.append(self.sigmoid(self.hidden_layer_value))
               
                else:
                    self.hidden_layer_input=np.dot(self.hidden_layer_activation[i-1],self.hidden_weight[i])
                    self.hidden_layer_value=self.hidden_layer_input+self.hidden_bias[i]
                    self.hidden_layer_activation.append(self.sigmoid(self.hidden_layer_value))
                    
            self.output_layer_input=np.dot(self.hidden_layer_activation[-1],self.output_weight)
            self.output_layer_value=self.output_layer_input+self.output_bias
            self.output=self.sigmoid(self.output_layer_value)

    def bp(self):
        self.E=self.trained_output-self.output
        self.slope_output=self.deravative(self.output)
        self.d_output=self.E*self.slope_output
        if(self.no_of_hidden_layer==0):

            self.output_weight+=np.dot(self.trained_input.T,self.d_output)*self.learning_rate
            self.output_bias+=np.sum(self.d_output,axis=0,keepdims=True)*self.learning_rate
            
            
        else:

            for i in range(self.no_of_hidden_layer-1,-1,-1):
                slp_hidden=0
                ero_hidden=0
                d_hdn=0
                prev_d_hdn=0
                
                if(i==self.no_of_hidden_layer-1):
                    

                        slp_hidden=self.deravative(self.hidden_layer_activation[i])
                        self.slope_hidden.append(slp_hidden)
                        
                        ero_hidden=np.dot(self.d_output,self.output_weight.T)
                        self.error_hidden.append(ero_hidden)

                        d_hdn=slp_hidden*ero_hidden
                        self.d_hidden.append(d_hdn)
                        prev_d_hdn=d_hdn

                        
                    
                        
                        
                        
                        
                else:
                        slp_hidden=self.deravative(self.hidden_layer_activation[i])
                        self.slope_hidden.append(slp_hidden)
                        
                        ero_hidden=np.dot(self.d_hidden[self.no_of_hidden_layer-2-i],self.hidden_weight[i+1].T)
                        self.error_hidden.append(ero_hidden)

                        d_hdn=slp_hidden*ero_hidden
                        self.d_hidden.append(d_hdn)
                        prev_d_hdn=d_hdn

                        
                
            self.d_hidden=self.d_hidden[::-1]      
            for i in range(self.no_of_hidden_layer):
                
                if(self.no_of_hidden_layer==1):
                    self.hidden_weight[i]+=np.dot(self.trained_input.T,self.d_hidden[i])*self.learning_rate
                    self.hidden_bias[i]+=np.sum(self.d_hidden[i],axis=0,keepdims=True)*self.learning_rate
                    
                elif(self.no_of_hidden_layer-1==i):
                    self.hidden_weight[i]+=np.dot(self.hidden_layer_activation[i-1].T,self.d_hidden[i])*self.learning_rate
                    self.hidden_bias[i]+=np.sum(self.d_hidden[i],axis=0,keepdims=True)*self.learning_rate
                    
                elif(i==0):
                    
                    self.hidden_weight[i]+=np.dot(self.trained_input.T,self.d_hidden[i])*self.learning_rate
                    self.hidden_bias[i]+=np.sum(self.d_hidden[i],axis=0,keepdims=True)*self.learning_rate
                    
                else:
                    self.hidden_weight[i]+=np.dot(self.hidden_layer_activation[i-1].T,self.d_hidden[i])*self.learning_rate
                    self.hidden_bias[i]+=np.sum(self.d_hidden[i],axis=0,keepdims=True)*self.learning_rate
                    

            self.output_weight+=np.dot(self.hidden_layer_activation[-1].T,self.d_output)*self.learning_rate
            self.output_bias+=np.sum(self.d_output,axis=0,keepdims=True)*self.learning_rate
                        
    
    def forward_propogation(self):
        if(self.no_of_hidden_layer==0):
            self.output_layer_input=np.dot(self.trained_input,self.output_weight)
            self.output_layer_value=self.output_layer_input+self.output_bias
            self.output=self.sigmoid(self.output_layer_value)
            
            
            
        else:

            for i in range(self.no_of_hidden_layer):
               
                if(i==self.no_of_hidden_layer-1):
                    if(self.no_of_hidden_layer==1):
                        self.hidden_layer_input=np.dot(self.trained_input,self.hidden_weight[0])
                        self.hidden_layer_value=self.hidden_layer_input+self.hidden_bias[0]
                        self.hidden_layer_activation[i]=(self.sigmoid(self.hidden_layer_value))
                    else:
                        
                            
                        self.hidden_layer_input=np.dot(self.hidden_layer_activation[-2],self.hidden_weight[-1])
                        self.hidden_layer_value=self.hidden_layer_input+self.hidden_bias[-1]
                        self.hidden_layer_activation[i]=(self.sigmoid(self.hidden_layer_value))
                elif(i==0):
                    self.hidden_layer_input=np.dot(self.trained_input,self.hidden_weight[0])
                    self.hidden_layer_value=self.hidden_layer_input+self.hidden_bias[0]
                    self.hidden_layer_activation[i]=(self.sigmoid(self.hidden_layer_value))
               
                else:
                    self.hidden_layer_input=np.dot(self.hidden_layer_activation[i-1],self.hidden_weight[i])
                    self.hidden_layer_value=self.hidden_layer_input+self.hidden_bias[i]
                    self.hidden_layer_activation[i]=(self.sigmoid(self.hidden_layer_value))
                    
            self.output_layer_input=np.dot(self.hidden_layer_activation[-1],self.output_weight)
            self.output_layer_value=self.output_layer_input+self.output_bias
            self.output=self.sigmoid(self.output_layer_value)
    def backward_propogation(self):
        self.E=self.trained_output-self.output
        self.slope_output=self.deravative(self.output)
        self.d_output=self.E*self.slope_output
        if(self.no_of_hidden_layer==0):

            self.output_weight+=np.dot(self.trained_input.T,self.d_output)*self.learning_rate
            self.output_bias+=np.sum(self.d_output,axis=0,keepdims=True)*self.learning_rate
            
            
        else:

            for i in range(self.no_of_hidden_layer-1,-1,-1):
                slp_hdn=0
                eror_hdn=0
                d_hdn=0
                if(self.no_of_hidden_layer-1==i):
                    

                        slp_hdn=self.deravative(self.hidden_layer_activation[i])
                        eror_hdn=np.dot(self.d_output,self.output_weight.T)
                        d_hdn=slp_hdn*eror_hdn
                    
                else:
                        slp_hdn=self.deravative(self.hidden_layer_activation[i])
                        eror_hdn=np.dot(self.d_hidden[i+1],self.hidden_weight[i+1].T)
                        d_hdn=slp_hdn*eror_hdn
                self.d_hidden[i]=d_hdn

            for i in range(self.no_of_hidden_layer):
                
                if(self.no_of_hidden_layer==1):
                    self.hidden_weight[i]+=np.dot(self.trained_input.T,self.d_hidden[i])*self.learning_rate
                    self.hidden_bias[i]+=np.sum(self.d_hidden[i],axis=0,keepdims=True)*self.learning_rate
                    
                elif(self.no_of_hidden_layer-1==i):
                    self.hidden_weight[i]+=np.dot(self.hidden_layer_activation[i-1].T,self.d_hidden[i])*self.learning_rate
                    self.hidden_bias[i]+=np.sum(self.d_hidden[i],axis=0,keepdims=True)*self.learning_rate
                    
                elif(i==0):
                    
                    self.hidden_weight[i]+=np.dot(self.trained_input.T,self.d_hidden[i])*self.learning_rate
                    self.hidden_bias[i]+=np.sum(self.d_hidden[i],axis=0,keepdims=True)*self.learning_rate
                    
                else:
                    self.hidden_weight[i]+=np.dot(self.hidden_layer_activation[i-1].T,self.d_hidden[i])*self.learning_rate
                    self.hidden_bias[i]+=np.sum(self.d_hidden[i],axis=0,keepdims=True)*self.learning_rate
                    

            self.output_weight+=np.dot(self.hidden_layer_activation[-1].T,self.d_output)*self.learning_rate
            self.output_bias+=np.sum(self.d_output,axis=0,keepdims=True)*self.learning_rate
                        


            

    def train_data(self):
        if self.fl:
            data=''
            if self.name ==None:
                data='Nerual_Network Started Training'
            else:
                data='<"'+self.name+'"> is started Training'
            print(data)
        temp=self.times_to_train/10
        inc=temp
        self.count=self.count+1
        #self.train_first_time()
        for i in range(self.times_to_train-1):
            self.count=self.count+1
            if(self.show_per):
                if(i>=temp):
                    data=''
                    if self.name ==None:
                        
                        data='Training '+str(int(i/self.times_to_train*100))+'% completed'
                    else:
                        data='<"'+self.name+'"> Training '+str(int(i/self.times_to_train*100))+'% completed'
                    print(data)
                    temp=temp+inc
            
            self.forward_propogation()
            self.backward_propogation()

        if self.fl:
            
            data=''
            if self.name ==None:
                data='Nerual_Network Completed Training'
            else:
                data='<"'+self.name+'"> is completed Training'
            print(data)
    def think_only(self,trained_input):
        self.fp_think(trained_input)

        return self.output

    def think_and_change(self,trained_input,trained_output):
        self.count=self.count+1
        trained_input=np.array(trained_input)
        trained_output=np.array(trained_output)
        self.fp_think(trained_input)
        self.bp_think(trained_input,trained_output)
        
    
    def fp_think(self,trained_input):
        if(self.no_of_hidden_layer==0):
            self.output_layer_input=np.dot(trained_input,self.output_weight)
            self.output_layer_value=self.output_layer_input+self.output_bias
            self.output=self.sigmoid(self.output_layer_value)
            
            
            
        else:

            for i in range(self.no_of_hidden_layer):
               
                if(i==self.no_of_hidden_layer-1):
                    if(self.no_of_hidden_layer==1):
                        self.hidden_layer_input=np.dot(trained_input,self.hidden_weight[0])
                        self.hidden_layer_value=self.hidden_layer_input+self.hidden_bias[0]
                        self.hidden_layer_activation[i]=(self.sigmoid(self.hidden_layer_value))
                    else:
                        
                            
                        self.hidden_layer_input=np.dot(self.hidden_layer_activation[-2],self.hidden_weight[-1])
                        self.hidden_layer_value=self.hidden_layer_input+self.hidden_bias[-1]
                        self.hidden_layer_activation[i]=(self.sigmoid(self.hidden_layer_value))
                elif(i==0):
                    self.hidden_layer_input=np.dot(trained_input,self.hidden_weight[0])
                    self.hidden_layer_value=self.hidden_layer_input+self.hidden_bias[0]
                    self.hidden_layer_activation[i]=(self.sigmoid(self.hidden_layer_value))
               
                else:
                    self.hidden_layer_input=np.dot(self.hidden_layer_activation[i-1],self.hidden_weight[i])
                    self.hidden_layer_value=self.hidden_layer_input+self.hidden_bias[i]
                    self.hidden_layer_activation[i]=(self.sigmoid(self.hidden_layer_value))
                    
            self.output_layer_input=np.dot(self.hidden_layer_activation[-1],self.output_weight)
            self.output_layer_value=self.output_layer_input+self.output_bias
            self.output=self.sigmoid(self.output_layer_value)
    def bp_think(self,trained_input,trained_output):
        
        self.E=trained_output-self.output
        
        self.slope_output=self.deravative(self.output)
        self.d_output=self.E*self.slope_output
        if(self.no_of_hidden_layer==0):

            self.output_weight+=np.dot(trained_input.T,self.d_output)*self.learning_rate
            self.output_bias+=np.sum(self.d_output,axis=0,keepdims=True)*self.learning_rate
            
            
        else:

            for i in range(self.no_of_hidden_layer-1,-1,-1):
                slp_hdn=0
                eror_hdn=0
                d_hdn=0
                if(self.no_of_hidden_layer-1==i):
                    

                        slp_hdn=self.deravative(self.hidden_layer_activation[i])
                        eror_hdn=np.dot(self.d_output,self.output_weight.T)
                        d_hdn=slp_hdn*eror_hdn
                    
                else:
                        slp_hdn=self.deravative(self.hidden_layer_activation[i])
                        eror_hdn=np.dot(self.d_hidden[i+1],self.hidden_weight[i+1].T)
                        d_hdn=slp_hdn*eror_hdn
                self.d_hidden[i]=d_hdn

            for i in range(self.no_of_hidden_layer):
                
                if(self.no_of_hidden_layer==1):
                    self.hidden_weight[i]+=np.dot(trained_input.T,self.d_hidden[i])*self.learning_rate
                    self.hidden_bias[i]+=np.sum(self.d_hidden[i],axis=0,keepdims=True)*self.learning_rate
                    
                elif(self.no_of_hidden_layer-1==i):
                    self.hidden_weight[i]+=np.dot(self.hidden_layer_activation[i-1].T,self.d_hidden[i])*self.learning_rate
                    self.hidden_bias[i]+=np.sum(self.d_hidden[i],axis=0,keepdims=True)*self.learning_rate
                    
                elif(i==0):
                    
                    self.hidden_weight[i]+=np.dot(trained_input.T,self.d_hidden[i])*self.learning_rate
                    self.hidden_bias[i]+=np.sum(self.d_hidden[i],axis=0,keepdims=True)*self.learning_rate
                    
                else:
                    self.hidden_weight[i]+=np.dot(self.hidden_layer_activation[i-1].T,self.d_hidden[i])*self.learning_rate
                    self.hidden_bias[i]+=np.sum(self.d_hidden[i],axis=0,keepdims=True)*self.learning_rate
                    

            self.output_weight+=np.dot(self.hidden_layer_activation[-1].T,self.d_output)*self.learning_rate
            self.output_bias+=np.sum(self.d_output,axis=0,keepdims=True)*self.learning_rate
                        



    def generate_bias_weight(self):
        if(self.no_of_hidden_layer==len(self.perceptron_Array)):
            for i in range(self.no_of_hidden_layer):
                
                shape=()
                bshape=()
                if(i==0):
                    shape=(len(self.trained_input[0]),self.perceptron_Array[i])
                    bshape=(1,self.perceptron_Array[i])
                else:
                    shape=(self.perceptron_Array[i-1],self.perceptron_Array[i])
                    bshape=(1,self.perceptron_Array[i])
                d=np.random.uniform(low=-1,high=1,size=shape)
                weight=2*d-1
                d=np.random.uniform(low=-1,high=1,size=bshape)
                bias=d
                
                
                self.hidden_weight.append(weight)
                self.hidden_bias.append(bias)
            if(self.no_of_hidden_layer==0):
                d=np.random.uniform(low=-1,high=1,size=(len(self.trained_input[0]),len(self.trained_output[0])))
                
                self.output_weight=2*d-1
                d=np.random.uniform(low=-1,high=1,size=(1,len(self.trained_output[0])))
                self.output_bias=np.random.random((1,len(self.trained_output[0])))
            else:
                d=2*np.random.uniform(low=-1,high=1,size=(self.perceptron_Array[-1],len(self.trained_output[0])))-1
                self.output_weight=2*d-1
                d=np.random.uniform(low=-1,high=1,size=(1,len(self.trained_output[0])))
                self.output_bias=d

        else:
            print('Error :Length of perceptron Array not equal to number of Hidden Layer')
    
trained_input=np.array([[0,0,1,1],
                        [0,1,0,0],
                        [1,1,0,0],
                        [1,1,1,1]])

trained_output=np.array([[0,1],
                         [0,0],
                         [1,0],
                         [1,1]])

def cvtMat2Img(mat,size=28):
    mat=np.array(mat)
    mat=mat*255
    arr=[]

    for i in range(0,size*size,size):
        arr.append(mat[i:i+size])

    image=np.array(arr,dtype='uint8')

    

    return image

def resize(img):
    img=cv2.resize(img,(28,28))

    return img


def convert_grayscale(image,grayScale=False):
        gray=''
        if(grayScale):
            gray=image
        else:
            
            gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        gray=gray/255

        return gray

def cvtImg2Mat(image,grayScale=False):
        
        gray=convert_grayscale(image,grayScale)
        gray=gray.tolist()

        array=[]
        for i in gray:
            array=array+i

        return array

#fun ctions

def convert_decimal(binx):
    binx=binx[::-1]

    count=0
    for i  in range(len(binx)):
        data=binx[i]*np.power(2,count)
        count=count+1
        binx[i]=data
    return np.sum(binx)

def sep_data(data,min,max,div):
    if(data<div):
        return min
    else:
        return max

def sep_listData(listd,min,max,div):
    ar=[]
    for i in listd:
        ar.append(sep_data(i,min,max,div))

    return ar

def convert_binary(x,base=10):

        data="{0:b}".format(x)
        length=base-len(data)
        zeros=''
        for i in range(length):
            zeros=zeros+'0'

        data=zeros+data

        arr=[]
        for i in data:
            if(i=='0'):
                arr.append(0)
            else:
                arr.append(1)

        return arr



#Math
def inRangeQuad(pos1,pos2,c_pos):
    try:
        
        xy=c_pos
        cond1=False
        cond2=False
        
        if xy[0]>=pos1[0] and xy[0]<=pos2[0]:
            cond1=True

        if xy[1]>=pos1[1] and xy[1]<=pos2[1]:
            cond2=True
        

        if cond1 and cond2:
            return True
        else:
            return False
    except:
        print('___________________')
        print(c_pos)
        return False

def cutImg(img,pos1,pos2):
    x,y=pos1
    pos1=y,x
    x,y=pos2
    pos2=y,x
    imgs=img[pos1[0]:pos2[0],pos1[1]:pos2[1]]

    return imgs

def idontknowmyname(img,cellSize):
	h,w=img.shape[:2]
	cw=int(w/cellSize[0])
	ch=int(h/cellSize[1])
	dis=distributeScreen((w,h),(cw,ch))
	img2=img.copy()
	
	for i in dis:
            
	    img2=cv2.rectangle(img2,i[0],i[1],(0,255,0),1)
	    print(i)
	cv2.imshow("Hello World", img2)
#378,598

def distributeScreen(screen_size,cell_size):
    #Screen Size w,h
    #cell_size w,h
    c,r=cell_size
    c,r=r,c
    h,w=screen_size

    #h=h-int(h/10)
    #w=w-int(w/10)
    
    points=[]
    
    for j in range(0,w,int(w/c)):
        
        for i in range(0,h,int(h/r)):
            x=i+int(h/r)
            y=j+int(w/c)
            if x>h or y>w:
                continue
            #print(i,j,'\t',(i+int(w/c),int(h/r)+j))
            points.append([(i,j),(x,y)])
            
    
    return points



def prepareRange(screen_size,cell_size,points):
    activePos=[]
    
    
    spoints=distributeScreen(screen_size,cell_size)
    for i in points:

        for j in spoints:
            
            if j in activePos:
                continue
            cond=inRangeQuad(j[0],j[1],i)
            if cond:
                activePos.append(j)

    return activePos



def check_prime(x):
    half=int(x/2)
    count=0
    
    
    for i in range(1,half+1):
        if(x%i==0):

            count+=1
    if(x==0 or x==1):
        return False
    
    elif count>1:
        return False
    else:
        return True

def genWholeBin(length):

    total_val=pow(2,length)

    back=total_val/2
    val=[]
    cond=False
    ccount=0
    for i in range(length):
        data=[]
        for j in range(total_val):
            #print(ccount,back)
            if ccount==back:
                cond=not cond
                ccount=0

                

            if cond:
                data.append(1)
            else:
                data.append(0)
            ccount=ccount+1
            
        
        ccount=0
        back=back/2
        val.append(data)

    temp=[]
    for i in range(total_val):
        d=[]
        for j in range(length):
           d.append(val[j][i])
        temp.append(d)

    temp.sort()
    return temp


def genComb2(st1,st2):
    ar=[]
    for i in st1:
        for j in st2:
            ar.append(i+j)
            print(i+j)
    return ar

def genRandComb(string,length):

   
    if length==1:
        st=[]
        for i in string:
            st.append(i)

        return st
    else:
        first=string
        second=string
        third=''
        for i in range(1,length):
            third=genComb2(first,second)
            
            first=third
        return third

def genWhRandComb(strings,length):
    
        
    
    
    st=[]
    for i in range(1,length+1):
        data=genRandComb(strings,i)
        for j in data:
            st.append(j)

    return st
def label_img(img,pos,size,label):
    img=cv2.rectangle(img,pos,(pos[0]+size[0],pos[1]+size[1]),(255,0,0),1)
    img=cv2.putText(img,label,pos,1,1,(0,255,0),1)
    return img

def clear():
    print("ONLY WORKS IN COMMAND LINE")
    subprocess.call("cls",shell=True)

