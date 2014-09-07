# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from ui_open_image import Ui_Dialog
from routines.simple_thread import SimpleThread, closeThreads

import numpy as np
from time import time #FIXME

class ImageLoader(QObject):
	def __init__(self, parent = None):
		QObject.__init__(self, parent)
		
		self._width = 0
		self._height = 0
		self._progress = 0

	def loadFile(self, filename):
		try:
			self.srcImage = QImage(filename).convertToFormat(QImage.Format_RGB32)
			self._width = self.srcImage.width()
			self._height = self.srcImage.height()
		except:
			return False
		
		self.dstImage = QImage(self._width, self._height, QImage.Format_RGB32)
		
		return True

	def redraw(self, threshold, inverted):		
		closeThreads()
		self._redraw(threshold, inverted, self.srcImage, self.dstImage, thr_start = True)

	@SimpleThread
	def _redraw(self, threshold, inverted, src, dst):
		width = self._width
		height = self._height

		ccol = QColor(Qt.white)

		for y in xrange(height):
			self._updateProgress(y, thr_method = 'q')
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
	
	def stop(self):
		closeThreads()

	def _updateProgress(self, progress):
		self._progress = progress
		
	def image(self):
		return self.dstImage
	
	def width(self):
		return self._width
	
	def height(self):
		return self._height

	def progress(self):
		return self._progress
	
	


