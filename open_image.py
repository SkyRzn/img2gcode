# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from ui_open_image import Ui_Dialog
from routines.simple_thread import SimpleThread, closeThreads

import numpy as np
from time import time #FIXME

class OpenImageDialog(QDialog):
	def __init__(self, filename, parent = None):
		QDialog.__init__(self, parent)

		self.ui = Ui_Dialog()
		self.ui.setupUi(self)

		self.srcImage = QImage(filename).convertToFormat(QImage.Format_RGB32)

		width = self.srcImage.width()
		height = self.srcImage.height()

		self.viewImage = QImage(width, height, QImage.Format_RGB32)

		self.ui.view.setFixedSize(self.srcImage.size())

		self.ui.thresholdSlider.valueChanged.connect(self.changeImage)
		self.ui.invertedCheckBox.toggled.connect(self.changeImage)
		self.ui.thresholdSlider.setValue(127)

	def thresholdChanged(self, value):
		changeImage()

	def changeImage(self):
		threshold = self.ui.thresholdSlider.value()
		inverted = self.ui.invertedCheckBox.isChecked()
		closeThreads()
		self.ui.progress.setEnabled(True)
		self.changeImage_(threshold, inverted, self.srcImage, self.viewImage, thr_start = True)


	@SimpleThread
	def changeImage_(self, threshold, inverted, src, dst):
		width = src.width()
		height = src.height()

		ccol = QColor(Qt.white)

		self.setProgress(0, thr_method = 'q')
		self.setProgressMax(height, thr_method = 'q')

		for y in xrange(height):
			self.setProgress(y, thr_method = 'q')
			for x in xrange(width):
				if self.thr_stopFlag:
					return

				col = QColor(src.pixel(x, y))

				if col.value() > threshold:
					val = 0x00 if inverted else 0xff
				else:
					val = 0xff if inverted else 0x00

				col.setRed(val)
				col.setGreen(val)
				col.setBlue(val)
				dst.setPixel(x, y, col.rgb())

		self.imageChanged(thr_method = 'q')

	def imageChanged(self):
		self.ui.progress.setValue(0)
		self.ui.progress.setEnabled(False)
		self.ui.view.setPixmap(QPixmap.fromImage(self.viewImage))

	def setProgressMax(self, value):
		self.ui.progress.setMaximum(value)

	def setProgress(self, value):
		self.ui.progress.setValue(value)

	def result(self):
		return self.viewImage
