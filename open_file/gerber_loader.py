# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from gerber_parser import GerberParser
from routines.simple_thread import SimpleThread
from abstract_loader import AbstractLoader
import math


class GerberLoader(AbstractLoader):
	def __init__(self, parent = None):
		AbstractLoader.__init__(self, parent)

		self._parser = GerberParser(self)

	def _load(self, filename):
		f = open(filename, 'r')
		if not f:
			return False
		self._gerber = f.read()
		f.close()

		return bool(self._gerber)

	@SimpleThread
	def _run(self, resolution):
		self._parser.progress.connect(self._progress)
		if self._parser.run(self._gerber, self):
			self.rasterize(resolution)

	def rasterize(self, resolution):
		width = (self._parser.width()) / resolution
		height = (self._parser.height()) / resolution
		offs = self._parser.offset()
		path = self._parser.path()
		pathCount = len(path)

		im = QImage(int(width), int(height), QImage.Format_RGB32)
		print width, height
		im.fill(Qt.white)

		p = QPainter(im)

		pen = QPen()
		pen.setColor(Qt.black)

		brush = QBrush()
		brush.setColor(Qt.black)

		prevPoint = QPointF(0, 0)
		point = QPointF(0, 0)
		qpath = QPainterPath()
		aperture = None

		for i, row in enumerate(path):
			code, value = row

			if aperture:
				aptype, apdata = aperture

			if code == 'C':
				x = (value[0] - offs[0]) / resolution
				y = height - (value[1] - offs[1]) / resolution
				point = QPointF(x, y)

			elif code == 'V':
				pen.setColor(Qt.black if value else Qt.white)
				brush.setColor(Qt.black if value else Qt.white)

			elif code == 'D':
				if value == 1 and aperture:
					pen.setWidth(apdata[0] / resolution)
					pen.setCapStyle(Qt.RoundCap if aptype == 'C' else Qt.SquareCap)
					p.setPen(pen)

					brush.setStyle(Qt.NoBrush)
					p.setBrush(brush)

					p.drawLine(prevPoint, point)

				elif value == 3 and aperture:
					pen.setWidth(1)
					p.setPen(pen)

					brush.setStyle(Qt.SolidPattern)
					p.setBrush(brush)

					if aptype in ('C', 'R', 'P'):
						w = apdata[0] / resolution / 2
						h = apdata[1] / resolution / 2 if len(apdata) > 1 else 0

					if aptype == 'C':
						p.drawEllipse(QPointF(x, y), w, w)
					elif aptype == 'R':
						p.drawRect(QRectF(x - w, y - h, w * 2, h * 2))
					elif aptype == 'P':
						p.drawEllipse(QPointF(x, y), w, w)
						#self.drawNSidePolygon(p, QPointF(x, y), w, w)
					elif aptype == 'M':
						code, rect, coords = apdata
						if code == 4:
							mpoints = []
							for mx, my in coords:
								mx = mx / resolution
								my = -my / resolution
								mpoints.append(QPointF(x + mx, y + my))
							p.drawPolygon(*mpoints)

				if value > 3:
					aperture = self._parser.aperture(value)
				else:
					prevPoint = point

			self._progress(50 + i*50/pathCount, thr_method = 'q')

		p.drawPath(qpath)

		self._loaded(im, thr_method = 'q')

	def drawNSidePolygon(self, painter, size, rotation, offset):
		n = len(coords)
		brush.setColor(Qt.red)
		p.setBrush(brush)
		points = []
		for i, coord in enumerate(coords):
			x = math.sin((i/n + rotation/360.0) * 2 * math.pi) * size + offset[0]
			y = math.cos((i/n + rotation/360.0) * 2 * math.pi) * size + offset[1]
			points.append(QPointF(x, y))
		p.drawPolygon(*points)
		brush.setColor(Qt.black)
		p.setBrush(brush)

	def _progress(self, val):
		self.progress.emit(val)

	def _loaded(self, image):
		self.loaded.emit(image)

	def width(self):
		return self._width

	def height(self):
		return self._height



