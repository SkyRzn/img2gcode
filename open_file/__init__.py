# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from ui_open_file import Ui_Dialog
from image_loader import ImageLoader
from gerber_loader import GerberLoader

import numpy as np
from time import time #FIXME

class OpenFileDialog(QDialog):
	def __init__(self, filename, parent = None):
		QDialog.__init__(self, parent)
		
		self.imageLoader = None
		self.gerberLoader = None

		self.ui = Ui_Dialog()
		self.ui.setupUi(self)

		self.ui.thresholdSlider.valueChanged.connect(self.redraw)
		self.ui.invertedCheckBox.toggled.connect(self.redraw)
		
		self.ui.progress.setEnabled(False)

		self.timer = QTimer(self)
		self.timer.setInterval(500)
		self.timer.timeout.connect(self.progressUpdate)
		
		fileExt = filename.split('.')[-1]
		
		if fileExt == 'gbr':
			self.ui.imageBox.setVisible(False)
		elif fileExt in ['png', 'bmp', 'jpg']:
			self.ui.gerberBox.setVisible(False)
			self.imageLoader = ImageLoader(self)
			if not self.imageLoader.loadFile(filename):
				self.close()
				
			self.ui.view.setFixedSize(self.imageLoader.width(), self.imageLoader.height())
				
			self.ui.thresholdSlider.setValue(127)

	def redraw(self):
		self.timer.stop()
		
		if self.imageLoader:
			self.imageLoader.stop()
			threshold = self.ui.thresholdSlider.value()
			inverted = self.ui.invertedCheckBox.isChecked()
			
			self.ui.progress.setMaximum(self.imageLoader.height())
			self.ui.progress.setValue(0)
			self.ui.progress.setEnabled(True)
			
			self.imageLoader.redraw(threshold, inverted)
		elif self.gerberLoader:
			pass
		else:
			return
		
		self.timer.start()

	def progressUpdate(self):
		if self.imageLoader:
			progress = self.imageLoader.progress()
		elif self.gerberLoader:
			pass
		else:
			return
		
		if progress < self.imageLoader.height() - 1:
			self.ui.progress.setValue(progress)
		else:
			self.timer.stop()
			self.ui.progress.setValue(0)
			self.ui.progress.setEnabled(False)
			self.ui.view.setPixmap(QPixmap.fromImage(self.imageLoader.image()))
			
	def image(self):
		if self.imageLoader:
			return self.imageLoader.image()
		elif self.gerberLoader:
			return None
		else:
			return None
	
	def closeEvent(self, event): #FIXME
		self.timer.stop()
		self.imageLoader.stop()
		print 'qqqq'
