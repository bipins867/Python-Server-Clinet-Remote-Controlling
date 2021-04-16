import math



def inArea(point ,fpoints, h,w):
    xrange=range(fpoints[0]-1,fpoints[0]+h+1)
    yrange=range(fpoints[1]-1,fpoints[1]+w+1)
    
    if(point[0] in xrange and point[1] in yrange):
        return True
    else:
        return False



#Finding The Approximate Value on

#---------------------------------
#---------------------------------
#---------------------------------
#---------------------------------
#---------------------------------
#---------------------------------
def Approximate(old,new,val):
    low=old-val
    high=old+val
    
    if(new<=high and new>=low):
        return True
    else:
        return False

#Clearing stright line obstacles

def straightLineAngles(angles,approx):
    length=len(angles)
    old=180
    for i in range(0,length):
        ang=angles[i]
        ret=Approximate(old,ang,approx)

        if(ret):
            angles[i]=180

# Right Angle formation
def RightAngles(angles,approx):
    length=len(angles)
    old=90
    
    for i in range(0,length):
        ang=angles[i]
        ret=Approximate(old,ang,approx)

        if(ret):
            angles[i]=90
# Making the angles right and straight

def right_linear(angles,approx):
    straightLineAngles(angles,approx)
    RightAngles(angles,approx)


#Angle Detection in three point point1,point2 ,point3

#---------------------------------
#---------------------------------
#---------------------------------
#---------------------------------
#---------------------------------
#---------------------------------
def angleOfPoints(point1,point2,point3):
    #print(point1,"  ",point2,"  ",point3)
    line2=[(point3[0]-point2[0]),(point3[1]-point2[1])]
    line1=[(point1[0]-point2[0]),(point1[1]-point2[1])]


    

    dot=(line1[0]*line2[0]+line1[1]*line2[1])

    modx=math.sqrt(math.pow(line1[0],2)+math.pow(line1[1],2))
    mody=math.sqrt(math.pow(line2[0],2)+math.pow(line2[1],2))

    mod=modx*mody

    ang=0
    
    
            
                
        
    if mod==0:
        ang=90.0
        
    else:
        number=dot/mod
        
        if(number>0):
           
           if(number>1):
                    number=1

        elif(number<0):
                if(number<-1):
                    number=-1
                

        ang=math.acos(number)
        ang=math.degrees(ang)

    return ang


#Calculation of lenth bw two points


def distanceOfPoints(point1,point2,ints=False):
    xlen=point1[0]-point2[0]
    ylen=point1[1]-point2[1]

    distance=math.sqrt(math.pow(xlen,2)+math.pow(ylen,2))
    distance=int(distance)

    return distance

#Calculation of angle by its slops between two lines

#---------------------------------
#---------------------------------
#---------------------------------
#---------------------------------
#---------------------------------
#---------------------------------
#---------------------------------
#---------------------------------
#---------------------------------
#---------------------------------
#---------------------------------
#---------------------------------
#---------------------------------
#---------------------------------
#---------------------------------
#---------------------------------
#---------------------------------
#---------------------------------
def angleOfSlopes(m1,m2):
    angle=0
    num=m1-m2
    den=1+m1*m2
   
    if den==0:
        angle=90.0
    else:
        val=abs(num/den)
        ang=math.atan(val)
        angle=math.degrees(ang)

    return angle

#Testing new Functioin

#---------------------------------
#---------------------------------
#---------------------------------
#---------------------------------
#---------------------------------
#---------------------------------
#---------------------------------
#---------------------------------
#---------------------------------
#---------------------------------
#---------------------------------

def arrayInput(xy):
    point1=[]
    point2=[]
    point3=[]


    p1=p2=d1=d2=d3=0
    length=len(xy)
    temp=int(length/3)
    s=1
    last=xy[length-1]

    newXy=[]
    oldAngle=180
    newAngle=0

    for i in range(3,length-1,3):
       s=s+1
       if(i==3):
           newXy.append(xy[0])
       if(s==temp):
           point1=xy[i-3]
           p1=xy[i-2]
           p2=xy[i-1]
           
           point2=xy[i]
           point3=last
           
           
       else:
            point1=xy[i-3]
            p1=xy[i-2]
            p2=xy[i-1]
           
            point2=xy[i]
            t=i+3
            if(t>length):
                point3=last
            else:
                point3=xy[t]

       d1=distanceOfPoints(point1,p1)
       d2=distanceOfPoints(p1,p2)
       d3=distanceOfPoints(p2,point2)
      # print(point1,"   ",point2,"  ",point3)
       if(d1>10 or d2>10 or d3>10):
           if(d1>10):
                newXy.append(p1)
           elif(d2>10):
                newXy.append(p2)
           elif(d3>10):
               newXy.append(point2)
       angle=angleOfPoints(point1,point2,point3)
       angle=int(angle)
           
       newAngle=angle

       approx=Approximate(oldAngle,newAngle,3)
       
       if(not approx):
           newXy.append(point2)
       
       if(s==temp):
           newXy.append(last)
            
       oldAngle=newAngle
       
    
    return newXy
    
#Removing sortest distances

#---------------------------------
#---------------------------------
#---------------------------------
#---------------------------------
#---------------------------------
#---------------------------------
#---------------------------------
#---------------------------------
#---------------------------------
#---------------------------------
#---------------------------------

def arrayElement(xy):

    lenght=len(xy)
    
    newXy=xy
    temp=[]
    last=lenght-1  
    point1=point2=point3=0
    
    for i in range(0,last):
        if(i==last-1):
            point1=xy[i]
            point2=xy[i+1]
        else:
            point1=xy[i]
            point2=xy[i+1]
        
        distance=distanceOfPoints(point1,point2)
        distance=int(distance)
        
        
        if (distance  <1.5):
            
            temp.append(point1)
            
    
    lenOfTemp=len(temp)
    
    for i in range(0,lenOfTemp):
        el=temp[i]
        newXy.remove(el)
        
    
    
#Alfa Testing now started
#---------------------------------
#---------------------------------
#---------------------------------
#---------------------------------
#---------------------------------
#---------------------------------
#---------------------------------
#---------------------------------
#---------------------------------
#---------------------------------
#---------------------------------
def alfaTesting(xy):
    oldAngle=180
    newAngle=0
    point1=point2=point3=[]
    newAngles=[]
    ang=0
    length=len(xy)
    
    first=xy[0]
    last=xy[length-1]
    for i in range(0,length):
        if(i==0):
            point1=last
            point3=xy[i+1]
        if(i==length-1):
            point1=xy[i-1]
            point3=first
        else:
            point1=xy[i-1]
            point3=xy[i+1]
        
        
        point2=xy[i]
        
        num=point2[1]-point1[1]
        den=point2[0]-point1[0]
        angle=int(angleOfPoints(point1,point2,point3))
        
        x1=point1[0]
        y1=point1[1]

        x2=point2[0]
        y2=point2[1]
        x=y=0
        x3=point3[0]
        y3=point3[1]

        if(den==0):
            
            if(y1>y2):
                
                if(x3<x2):
                   ang=360-angle 
                elif(x3>x2):
                    ang=angle
            elif(y1<y2):
                
                if(x3>x2):
                   ang=360-angle 
                elif(x3<x2):
                    ang=angle

        else:
            m=num/den
            
            if(m==0):
                
                if(x1>x2):
                    if(y3<y2):
                       ang=angle 

                    elif(y3>y2):
                        ang=360-angle
                    

                elif(x1<x2):
                    if(y3>y2):
                       ang=angle 

                    elif(y3<y2):
                        ang=360-angle
            else:
                y=y2-m*(x2-x3)
                x=x3
                
                nang=angleOfPoints((x3,y3),(x,y),(x2,y2))
                #-------------------------------------------------------
                if(y1>y2 and x1>x2):
                     
                    if(x3<=x2):
                        if(nang>=90):
                            ang=angle

                        elif(nang<90):
                            ang=360-angle

                    elif(x3>x2):
                        if(nang<90):
                            ang=angle

                        elif(nang>=90):
                            ang=360-angle
                #----------------------------------------------------------
                if(y1<y2 and x1<x2):
                    
                     
                    if(x3>=x2):
                        if(nang>=90):
                            ang=angle

                        elif(nang<90):
                            ang=360-angle

                    elif(x3<x2):
                        if(nang<90):
                            ang=angle

                        elif(nang>=90):
                            ang=360-angle  
                #---------------------------------------------------------
                if(y1<y2 and x1>x2):

                    
                    if(x3>=x2):
                        if(nang>=90):
                            ang=angle

                        elif(nang<90):
                            ang=360-angle

                    elif(x3<x2):
                        if(nang<90):
                            ang=angle

                        elif(nang>=90):
                            ang=360-angle
                #---------------------------------------------------------
                if(y1>y2 and x1<x2):
                    
                    if(x3<=x2):
                        if(nang>=90):
                            ang=angle

                        elif(nang<90):
                            ang=360-angle

                    elif(x3>x2):
                        if(nang<90):
                            ang=angle

                        elif(nang>=90):
                            ang=360-angle
            
        

        
        
        #print(point1,"   ",point2,"    ",point3,"   ",angle,"     Now   ",ang)
        newAngles.append(ang)
        #print("-----------------------------------------------------------------")
    return newAngles
def edgeDetection(xy,angles):
    length=len(xy)
    newXy=[]
    
    for i in range(0,length):
        ang=angles[i]

        if(ang != 180):
            
            
            newXy.append((xy[i],angles[i]))
    return newXy
def linearEdgeDetection(xy):
    point1=point2=point3=[]
    newXy=[]
    point1=xy[len(xy)-1][0]
    point2=xy[0][0]
    oldAngle=0
    length=len(xy)
    newXy.append(xy[0][0])
    
    for i in range(1,length):
        point3=xy[i][0]
        ang=xy[i][1]
        angle=int(angleOfPoints(point1,point2,point3))

        ret=Approximate(oldAngle,angle,2)
        dis=perDisFromLine(point1,point3,point2)
        print(point1,"  ",point3,"  ",point2,"  ",angle)       
        if(not ret):
           newXy.append(point3)
           point1=point2
           point2=point3
        oldAngle=angle
    return newXy

#Perpndicular Distance from the line

def disDetection(xy):
    length=len(xy)
    
    point1=[]
    point2=[]
    point3=[]

    newXy=[]
    array=[]
    first=xy[0][0]
    last=xy[len(xy)-1][0]
    temp=0

    
    for i in range(0,length-1):
        point1=xy[i][0]
        point2=xy[i+1][0]
        
        #point3=xy[i+1][0]
        
        dis=distanceOfPoints(point1,point2)
        if(dis<15):
            if(i==0):
                array.append(point1)
            else:
                array.append(point2)
            
        else:
            
            newXy.append(array)
            
            array=[]
            array.append(point2)

    array=[]
        
    dis1=distanceOfPoints(first,last)
    #newXy[0][0]=first
    array.append(first)
    newXy[0]=array
    array=[]
    if(dis1>10):
        array.append(last)
        newXy.append(array)

    return newXy
    

def perDisFromLine(point1,point2,point3):
    
    x,y=point1
    p,q=point2
    a,b=point3
    
    num=(p-x)*(x-a)+(q-y)*(y-b)
    den=math.pow((p-x),2)+math.pow((q-y),2)
    lamda=-num/den

    s=x+lamda*(p-x)
    t=y+lamda*(q-y)

    distance=distanceOfPoints(point3,(s,t))
    return distance


#Beta Testing started from here        

def pointsSimalarToLine(xy):
    length=len(xy)


    for i in range(0,length-2):
        point1=xy[0]
        

