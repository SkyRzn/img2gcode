# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from ui_open_file import Ui_Dialog
from image_loader import ImageLoader
from gerber_loader import GerberLoader


class OpenFileDialog(QDialog):
	def __init__(self, filename, parent = None):
		QDialog.__init__(self, parent)
		
		self.ui = Ui_Dialog()
		self.ui.setupUi(self)

		self.ui.thresholdSlider.valueChanged.connect(self.redraw)
		self.ui.invertedCheckBox.toggled.connect(self.redraw)
		
		self.ui.progress.setEnabled(False)

		fileExt = filename.split('.')[-1]
		
		if fileExt == 'gbr':
			self.ui.imageBox.setVisible(False)
		elif fileExt in ['png', 'bmp', 'jpg']:
			self.ui.gerberBox.setVisible(False)
			self._loader = ImageLoader(self)
			if not self._loader.load(filename):
				self.close() #FIXME
				
			self.ui.thresholdSlider.setValue(127)
			
		self._loader.progress.connect(self.ui.progress.setValue)
		self._loader.loaded.connect(self._loaded)

	def redraw(self):
		self._loader.stop()
		
		if type(self._loader) == ImageLoader:
			threshold = self.ui.thresholdSlider.value()
			inverted = self.ui.invertedCheckBox.isChecked()
			
		self.ui.progress.setValue(0)
		self.ui.progress.setEnabled(True)
		
		self._loader.run((threshold, inverted))
		
	def _loaded(self, image):
		self._image = image
		self.ui.view.setFixedSize(image.size())
		self.ui.view.setPixmap(QPixmap.fromImage(image))
		
		
	def image(self):
		return self._image
	
	def closeEvent(self, event): #FIXME
		print 'qqqq'
