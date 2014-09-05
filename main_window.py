# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from open_image import OpenImageDialog
from ui_main_window import Ui_MainWindow

from test.scan_image import *
from gerber_parser import Gerber


class MainWindow(QMainWindow):
	def __init__(self, parent = None):
		QMainWindow.__init__(self, parent)

		self.data = None
		self.image = None

		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)

		self.setActions()

		self.g = Gerber()
		self.g.parse('1.gbr')

		rrr = 20

		w = self.g.width()*rrr
		h = self.g.height()*rrr
		print self.g.width()

		im = QImage(int(w), int(h), QImage.Format_RGB32)

		p = QPainter(im)
		pen = QPen()
		pen.setColor(Qt.red)
		p.setPen(pen)
		brush = QBrush(Qt.NoBrush)
		brush.setColor(Qt.red)
		p.setBrush(brush)

		offs = self.g.offset()

		point = QPointF()
		for path in self.g.paths:
			code, apertureCode, coords = path
			aperture = self.g.apertures[apertureCode]

			aptype, sizes = aperture
			#print sizes[0]*rrr

			if code == 1:
				if aptype == 'C':
					pen.setWidth(sizes[0]*rrr)
					pen.setCapStyle(Qt.RoundCap)
					p.setPen(pen)
					brush.setStyle(Qt.NoBrush)
					p.setBrush(brush)
				qpath = QPainterPath(point)

			for x, y in coords:
				x = int((x-offs[0])*rrr)
				y = h - int((y-offs[1])*rrr)
				point = QPointF(x, y)
				if code == 1:
					qpath.lineTo(x, y)
				elif code == 3:
					pen.setWidth(1)
					p.setPen(pen)
					brush.setStyle(Qt.SolidPattern)
					p.setBrush(brush)

					if aptype == 'C':
						p.drawEllipse(QPointF(x, y), sizes[0]*rrr/2, sizes[0]*rrr/2)
					elif aptype == 'R':
						ww = sizes[0]*rrr
						hh = sizes[1]*rrr
						rect = QRectF(x - ww/2, y - hh/2, ww, hh)

						p.drawRect(rect)


			if code == 1:
				p.drawPath(qpath)



		self.ui.view.setPixmap(QPixmap.fromImage(im))

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
