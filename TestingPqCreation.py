#Testing PqCreation
#Cv2 into pixmap
#FrameContainer
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import cv2
import time

image=cv2.imread('C:\\Users\\Bipin\\Desktop\\Capture.jpg')
app=QApplication(sys.argv)



def cv2toPqImage(image):
    h,w,c=image.shape
    byt=3*w

    image =QtGui.QImage(image.data,w,h,byt,QtGui.QImage.Format_RGB888).rgbSwapped()
    return QtGui.QPixmap.fromImage(image)


def resizePqImage(image,size,condR=False):
    pixmap = image
    if not condR:
        pixmap_resized = pixmap.scaled(size[0], size[1])

    else:
        pixmap_resized = pixmap.scaled(size[0], size[1],QtCore.Qt.KeepAspectRatio)

        
    return pixmap_resized

lb=cv2toPqImage(image)

mainWindow=QMainWindow()
mainWindow.setGeometry(100,100,400,400)

label=QLabel(mainWindow)
lb=resizePqImage(lb,(100,100),True)
label.setPixmap(lb)
label.adjustSize()
label.move(10,10)






    
mainWindow.show()    
