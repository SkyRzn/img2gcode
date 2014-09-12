# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from open_file import OpenFileDialog
from ui_main_window import Ui_MainWindow

from test.scan_image import *
from routines.simple_thread import SimpleThread, closeThreads


STATE_INIT = 0
STATE_LOADED = 1
STATE_BUILDED = 2


class MainWindow(QMainWindow):
	progressSignal = pyqtSignal(int)
	def __init__(self, parent = None):
		QMainWindow.__init__(self, parent)

		self.data = None
		self.image = None

		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)

		self.setActions()

		self.setState(STATE_INIT)

	def setState(self, state):
		#if state == STATE_INIT:
			#self.ui.actionBuild.setEnabled(False)
		#elif state == STATE_LOADED:
			#self.ui.actionBuild.setEnabled(True)

		self.state = state


	def setActions(self):
		self.ui.actionFileOpen.triggered.connect(self.fileOpen)
		self.ui.actionBuild.triggered.connect(self.build)

	def fileOpen(self):
		fileDialog = QFileDialog(self, self.tr('Open file'))
		fileDialog.setNameFilters([self.tr('Gerber (*.gbr)'),
									self.tr('Image (*.png *.bmp *.jpg)')])
		#if not fileDialog.exec_():
			#return

		#filename = fileDialog.selectedFiles()[0]

		filename = 'bot_layer.png'
		filename = '1.gbr'
		fileDialog = OpenFileDialog(filename, self)
		if fileDialog.exec_():
			self.image = fileDialog.image()
			self.ui.view.setPixmap(QPixmap.fromImage(self.image))
			self.setState(STATE_LOADED)

	def build(self):
		self.progress = QProgressDialog(self) #.tr('Building'), self.tr('Cancel'))
		self.progress.setRange(0, 100)
		self.progressSignal.connect(self.progress.setValue)
		print 111
		self._build(thr_start = True)
		self.progress.exec_()
		print 222

	@SimpleThread
	def _build(self):
		self.updatePrtogress(10, thr_method = 'q')
		pixChunks = getPixelChunks(self.image)
		self.updatePrtogress(20, thr_method = 'q')

		w = self.image.width()
		h = self.image.height()

		res = get_gcode(pixChunks, w, h)
		self.updatePrtogress(30, thr_method = 'q')

		t = 0
		for gcode, pix, t1 in res:
			#print t1, pix, gcode
			t+= t1
		print h*0.1, w*0.1, t
		self.updatePrtogress(100, thr_method = 'q')

	def updatePrtogress(self, val):
		self.progressSignal.emit(val)


