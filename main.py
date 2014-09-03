#!/usr/bin/python

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import sys


app = QApplication(sys.argv)
QTextCodec.setCodecForCStrings(QTextCodec.codecForName('UTF-8'))


from main_window import MainWindow


mainWindow = MainWindow()
mainWindow.setGeometry(QRect(100, 100, 400, 400))
mainWindow.show()
app.exec_()


