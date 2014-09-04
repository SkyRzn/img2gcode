# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from open_image import OpenImageDialog
from ui_main_window import Ui_MainWindow

from test.scan_image import *

class MainWindow(QMainWindow):
	def __init__(self, parent = None):
		QMainWindow.__init__(self, parent)

		self.data = None
		self.image = None

		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)

		self.setActions()

	def setActions(self):
		self.ui.actionFileOpen.triggered.connect(self.fileOpen)

	def fileOpen(self):
		fileDialog = QFileDialog(self, self.tr('Open image'))
		fileDialog.setNameFilter(self.tr('Images (*.png *.bmp *.jpg)'))
		#if not fileDialog.exec_():
			#return

		filename = fileDialog.selectedFiles()[0]

		filename = '1.png'
		#imageDialog = OpenImageDialog('/home/sky/IMG_18082014_102838.png', self)
		#imageDialog = OpenImageDialog('/home/sky/6ZaxbTIkbl8.jpg', self)
		imageDialog = OpenImageDialog(filename, self)
		if imageDialog.exec_():
			self.image = imageDialog.result()
			self.ui.view.setPixmap(QPixmap.fromImage(self.image))

			w = self.image.width()
			h = self.image.height()

			pixChunks = getPixelChunks(self.image)

			res = get_gcode(pixChunks, w, h)

			t = 0
			for gcode, pix, t1 in res:
				print t1, pix, gcode
				t+= t1
			print h*0.1, w*0.1, t

			self.ui.view.setPixmap(QPixmap.fromImage(self.image))
