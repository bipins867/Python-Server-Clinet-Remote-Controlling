

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import pynput.keyboard


if __name__=='__main__':
    

    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setGeometry(100,100,500,500)

    centralWidget=QWidget(win)
    win.setCentralWidget(centralWidget)


    txt=QPlainTextEdit(centralWidget)

    win.show()

    app.exec_()
