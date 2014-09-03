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

		ptr = self.srcImage.constBits()
		ptr.setsize(self.srcImage.byteCount())
		self.srcData = np.array(ptr).reshape(height, width, 4)


		self.data = np.empty((height, width), np.uint8)
		self.viewImage = QImage(self.data.data, width, height, QImage.Format_Indexed8)

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
		self.changeImage_(threshold, inverted, self.srcImage, thr_start = True)


	@SimpleThread
	def changeImage_(self, threshold, inverted, image):
		data = self.data
		h, w = data.shape
		src = self.srcData

		self.setProgress(0, thr_method = 'q')
		self.setProgressMax(h, thr_method = 'q')

		t = time()
		for y in xrange(h):
			self.setProgress(y, thr_method = 'q')
			for x in xrange(w):
				if self.thr_stopFlag:
					return

				val = QColor(image.pixel(x, y)).value()
				if val > threshold:
					data[y][x] = 0x00 if inverted else 0xff
				else:
					data[y][x] = 0xff if inverted else 0x00

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
		return self.data
