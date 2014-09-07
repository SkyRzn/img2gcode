# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import re
from routines.simple_thread import SimpleThread
from abstract_loader import AbstractLoader


class GerberLoader(AbstractLoader):
	def _load(self, filename):
		self._init()
		
		f = open(filename, 'r')
		if not f:
			return False
		self._gerber = f.readlines()
		f.close()
		
		return bool(self._gerber)
	
	def _init(self):
		self.gerber = []
		self.comments = []
		self.zeros = 'L'
		self.mode = 'A' #FIXME
		self.xFormat = (0, 0)
		self.yFormat = (0, 0)
		self.measurementSystem = 0 # 0 - mm, 1 - inch
		self.apertures = {}
		self.paths = [] # (D-code, aperture, visible, [(x,y), ...])
		self.rect = None
		self.visible = True

	@SimpleThread
	def _run(self, resolution):
		

	def parse_gerber(self):
		aperture = None
		path = []
		D = None
		x = y = 0
		for row in self._gerber:
			row = row.strip()
			row = row.strip('*')

			if row.startswith('G04'):
				self.comments.append(row[3:].strip())
			elif row.startswith('%') and row.endswith('%'):
				self._parseHeaderRow(row)
				continue
			elif row.startswith('G54'): # select aperture
				if path:
					self.paths.append((D, aperture, self.visible, path))
					path = []
				r = re.search('D([0-9]+)', row)
				aperture = int(r.groups()[0])
			elif row.startswith('X') or row.startswith('Y'):
				xx = self._getValue(row, 'X')
				if xx != None:
					x = self.convertCoord(xx)
				yy = self._getValue(row, 'Y')
				if yy != None:
					y = self.convertCoord(yy)
				d = self._getValue(row, 'D')
				if d != D:
					if path:
						self.paths.append((D, aperture, self.visible, path))
					path = []
					D = d

				path.append((x, y))

				if D == 3:
					self.paths.append((D, aperture, self.visible, path))
					path = []

				if self.rect == None:
					self.rect = (x, y, x, y)
				else:
					self.rect = (min(x, self.rect[0]),
								min(y, self.rect[1]),
								max(y, self.rect[2]),
								max(y, self.rect[3]))
		if path:
			self.paths.append((D, aperture, self.visible, path))

		return True
	
	def _getValue(self, row, code):
		r = re.search('%s[\+\-0-9]+' % (code), row)
		if not r:
			return None
		try:
			val = int(r.group()[1:])
		except:
			return None
		return val

	def _parseHeaderRow(self, row):
		row = row.strip('%%*')

		if row.startswith('FS'):
			self.zeros = row[2]
			self.mode = row[3]

			r = re.search('X(?P<x>[0-9]{2})Y(?P<y>[0-9]{2})', row)
			self.xFormat = tuple([int(i) for i in r.groupdict()['x']])
			self.yFormat = tuple([int(i) for i in r.groupdict()['y']])
		elif row == 'MOMM':
			self.measurementSystem = 0
		elif row == 'MOIN':
			self.measurementSystem = 1
		elif row.startswith('ADD'):
			r = re.search('ADD(?P<code>[0-9]{1,2})(?P<type>[CR]{1}),(?P<p1>[0-9\.]+)(X(?P<p2>[0-9\.]+)){0,1}(X(?P<p3>[0-9\.]+)){0,1}(X(?P<p4>[0-9\.]+)){0,1}', row)
			data = r.groupdict()
			code = data['code']
			aperture = (data['type'], [])

			for i in range(4):
				val = data['p%d' % (i+1)]
				if val:
					val = float(val)
					if self.measurementSystem:
						val *= 25.4
					aperture[1].append(val)
			self.apertures[int(code)] = aperture
		elif row == 'LPD':
			self.visible = True
		elif row == 'LPC':
			self.visible = False

	def convertCoord(self, x):
		x = float(x)/pow(10, self.xFormat[1])
		if self.measurementSystem:
			x *= 25.4
		return x

	def rasterize(self, resolution):
		#self.g = Gerber()
		#self.g.parse('hum_press.gbr')

		#rrr = 20

		#w = (self.g.width()+10)*rrr
		#h = (self.g.height()+10)*rrr

		#im = QImage(int(w), int(h), QImage.Format_RGB32)
		#im.fill(Qt.white)

		#p = QPainter(im)
		#pen = QPen()
		#pen.setColor(Qt.black)
		#p.setPen(pen)
		#brush = QBrush(Qt.NoBrush)
		#brush.setColor(Qt.black)
		#p.setBrush(brush)

		#offs = self.g.offset()
		#offs = (offs[0]-5, offs[1]-5)

		#point = QPointF()
		#for path in self.g.paths:
			#code, apertureCode, visible, coords = path
			#if code in (1, 3):
				#aperture = self.g.apertures[apertureCode]
				#aptype, sizes = aperture
			##print sizes[0]*rrr

			#if code == 1:
				#if aptype == 'C':
					#pen.setWidth(sizes[0]*rrr)
					#pen.setCapStyle(Qt.RoundCap)
					#p.setPen(pen)
					#brush.setStyle(Qt.NoBrush)
					#p.setBrush(brush)
				#qpath = QPainterPath(point)

			#for x, y in coords:
				#x = int((x-offs[0])*rrr)
				#y = h - int((y-offs[1])*rrr)
				#point = QPointF(x, y)
				#if code == 1:
					#qpath.lineTo(x, y)
				#elif code == 3:
					#if visible:
						#pen.setColor(Qt.black)
						#brush.setColor(Qt.black)
					#else:
						#pen.setColor(Qt.white)
						#brush.setColor(Qt.white)
					#pen.setWidth(1)
					#p.setPen(pen)
					#brush.setStyle(Qt.SolidPattern)
					#p.setBrush(brush)

					#if aptype == 'C':
						#p.drawEllipse(QPointF(x, y), sizes[0]*rrr/2, sizes[0]*rrr/2)
					#elif aptype == 'R':
						#ww = sizes[0]*rrr
						#hh = sizes[1]*rrr
						#rect = QRectF(x - ww/2, y - hh/2, ww, hh)

						#p.drawRect(rect)


			#if code == 1:
				#p.drawPath(qpath)


		#w = im.width()
		#h = im.height()

		#pixChunks = getPixelChunks(im)
		#res = get_gcode(pixChunks, w, h)
		
		#gcode = []
		
		#tt = 0
		#for g, pix, t in res:
			#gcode.append(g)
			#tt += t
		#print 'Time = %d, width = %.2f, height = %.2f' % (tt, w*0.05, h*0.05)
		#gcode = '\n'.join(gcode)
		#f = open('hum_press.gcode', 'w')
		#f.write(gcode)
		#f.close()

		#self.ui.view.setPixmap(QPixmap.fromImage(im))
	

	def width(self):
		return self.rect[2] - self.rect[0]

	def height(self):
		return self.rect[3] - self.rect[1]

	def offset(self):
		return (self.rect[0], self.rect[1])


