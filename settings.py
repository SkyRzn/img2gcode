# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *


QCoreApplication.setApplicationName('Img2Gcode')


settings = QSettings()

sld = settings.value
ssv = settings.setValue

