# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from routines.simple_thread import SimpleThread, closeThreads


class AbstractLoader(QObject):
	progress = pyqtSignal(int)
	loaded = pyqtSignal(QImage)
	
	def __init__(self, parent = None):
		QObject.__init__(self, parent)
		self.progress.emit(111)
		
	def load(self, filename):
		self.stop()
		self._load(filename)

	def run(self, options):
		self.stop()
		closeThreads()
		self._run(options, thr_start = True)

	def stop(self):
		closeThreads()


	
	


