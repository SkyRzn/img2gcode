# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from open_file import OpenFileDialog
from ui_main_window import Ui_MainWindow

from test.scan_image import *
#from gerber_parser import Gerber


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
		fileDialog = QFileDialog(self, self.tr('Open file'))
		fileDialog.setNameFilters([self.tr('Gerber (*.gbr)'),
									self.tr('Image (*.png *.bmp *.jpg)')])
		#if not fileDialog.exec_():
			#return

		#filename = fileDialog.selectedFiles()[0]

		filename = 'hum_press.gbr'
		filename = 'putin_vor.png'
		fileDialog = OpenFileDialog(filename, self)
		if fileDialog.exec_():
			self.image = fileDialog.image()
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
