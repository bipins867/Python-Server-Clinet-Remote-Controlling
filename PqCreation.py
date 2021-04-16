#PyQt5
#Image resize pyqt5
#Cv2 into pixmap
#FrameContainer
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import cv2
import threading



def creFrndListFXpClient(centralWidget,i):

    frame=QFrame(centralWidget)
    frame.setGeometry(0,0,300,110)

    label=QLabel(frame)
    label.move(10,10)
    label.setText("KING IS KING")

    return frame

def scrollBar(centralwidget,x,y,w,h):
        

        verticalLayoutWidget = QWidget(centralwidget)
        
        verticalLayoutWidget.setGeometry(QRect(x,y,w,h))

        gridLayout = QGridLayout(verticalLayoutWidget)
        gridLayout.setContentsMargins(0, 0, 0, 0)

        scrollArea = QScrollArea(verticalLayoutWidget)
        scrollArea.setWidgetResizable(True)

        scrollAreaWidgetContents = QtWidgets.QWidget()
        scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 107, 97))

        gridLayout_2 = QtWidgets.QGridLayout(scrollAreaWidgetContents)

        scrollArea.setWidget(scrollAreaWidgetContents)
        gridLayout.addWidget(scrollArea, 0, 0, 1, 1)
        

        return scrollAreaWidgetContents,gridLayout_2


def scrollBarWithSA(centralwidget,x,y,w,h):
        

        verticalLayoutWidget = QWidget(centralwidget)
        
        verticalLayoutWidget.setGeometry(QRect(x,y,w,h))

        gridLayout = QGridLayout(verticalLayoutWidget)
        gridLayout.setContentsMargins(0, 0, 0, 0)

        scrollArea = QScrollArea(verticalLayoutWidget)
        scrollArea.setWidgetResizable(True)

        scrollAreaWidgetContents = QtWidgets.QWidget()
        scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 107, 97))

        gridLayout_2 = QtWidgets.QGridLayout(scrollAreaWidgetContents)

        scrollArea.setWidget(scrollAreaWidgetContents)
        gridLayout.addWidget(scrollArea, 0, 0, 1, 1)
        

        return scrollAreaWidgetContents,scrollArea,gridLayout_2


def addWidgets(wiz,pos,gridLayout):

    for i,j in zip(wiz,pos):
        gridLayout.addWidget(i,j[0],j[1],1,1)

def addWidget(wiz,pos,gridLayout):
    gridLayout.addWidget(wiz,pos[0],pos[1],1,1)
    

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


if __name__=='__main__':


    app=QApplication(sys.argv)


    mainWindow=QMainWindow()
    mainWindow.setGeometry(100,100,400,400)

    label=QLabel(mainWindow)
    label.setText("KING IS KING")

    label.move(10,10)

    centralwidget = QWidget(mainWindow)
    mainWindow.setCentralWidget(centralwidget)
    saw,gg,gl=scrollBarWithSA(centralwidget,100,100,100,200)
    count=0
    def funClick():
        global count
        label=QLabel(saw)
        label.setText(str(count))
        gl.addWidget(label,count,0)
        count=count+1
    
    
    btnClick=QPushButton(mainWindow)
    btnClick.setText("CLICK")
    btnClick.move(100,100)
    btnClick.clicked.connect(funClick)
    


    mainWindow.show()
    
