#MathS

import math


def getAngle(p1,p2):
    pi=22/7

    x1=p1[0]
    y1=p1[1]

    x2=p2[0]
    y2=p2[1]
    
    return round(math.atan2(y2-y1,x2-x1)*180/pi,2)

def checkPrime(x):
	l2=int(x/2)
	cond=True
	for i in range(2,l2+1):
		#print(i,x,i%x)
		if x%i==0:
			cond=False
			break
	return cond
