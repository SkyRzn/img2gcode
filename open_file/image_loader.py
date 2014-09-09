# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from abstract_loader import AbstractLoader
from routines.simple_thread import SimpleThread


class ImageLoader(AbstractLoader):
	def _load(self, filename):
		self._srcImage = QImage(filename).convertToFormat(QImage.Format_RGB32)
		return bool(self._srcImage)

	@SimpleThread
	def _run(self, options):
		threshold, inverted = options
		width = self._srcImage.width()
		height = self._srcImage.height()
		src = self._srcImage
		dst = QImage(width, height, QImage.Format_RGB32)

		ccol = QColor(Qt.white)
		for y in xrange(height):
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

			self._progress(y*100/height, thr_method = 'q')

		self._loaded(dst, thr_method = 'q')
		
	def _progress(self, val):
		self.progress.emit(val)

	def _loaded(self, image):
		self.loaded.emit(image)


	


