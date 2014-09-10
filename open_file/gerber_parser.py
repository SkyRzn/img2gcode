# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import re


class GerberParser(QObject):
	progress = pyqtSignal(int)

	def __init__(self, parent = None):
		QObject.__init__(self, parent)

	def init(self):
		self.gerber = []
		self.comments = []
		self.zeros = 'L'
		self.mode = 'A' #FIXME
		self.xFormat = (0, 0)
		self.yFormat = (0, 0)
		self.measurementSystem = 0 # 0 - mm, 1 - inch
		self._macroses = {}
		self._apertures = {}
		self.rect = None

		self._path = [] # (code, (x, y))
		#	codes:
		#	C - coords
		#	D - apperture
		#	V - visibility

	def run(self, gerber, parent):
		self.init()

		gerber = self.prepareGerber(gerber)

		x = y = 0
		aperture = None
		rowCount = len(gerber)
		for i, row in enumerate(gerber):
			if row.startswith('G04'):
				self.comments.append(row[3:].strip())
				continue

			if row.startswith('%'):
				self._parseHeaderRow(row)
				continue

			xx = self._getValue(row, 'X')
			if xx != None:
				x = self.convertCoord(xx)
			yy = self._getValue(row, 'Y')
			if yy != None:
				y = self.convertCoord(yy)
			if xx != None or yy != None:
				self._path.append(('C', (x, y)))

			apCode = 0
			r = re.search('D([0-9]+)', row)
			if r:
				apCode = int(r.groups()[0])
				self._path.append(('D', apCode))
				if apCode > 3:
					aperture = self.aperture(apCode)

			apSize = 0
			if apCode in (1, 3) and aperture:
				code, sizes = aperture
				apSize = sizes[0]

			if self.rect == None:
				self.rect = (x - apSize, y - apSize, x + apSize, y + apSize)
			else:
				self.rect = (min(x - apSize, self.rect[0]),
							min(y - apSize, self.rect[1]),
							max(x + apSize, self.rect[2]),
							max(y + apSize, self.rect[3]))
			parent._progress(i*50/rowCount, thr_method = 'q')

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
		row = row.strip('%*')

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
		elif row.startswith('AM'):
			r = re.search('AM(?P<name>[^\*]+)\*(?P<code>[0-9]+),(?P<value>.*)', row)
			if not r:
				print 'Macros parsing error: "%s"' % (row)
				return
			data = r.groupdict()
			name = data['name']
			code = int(data['code'])
			val = data['value']

			#print name, code, val
			if code == 4:
				val = val.split(',')
				on = int(val.pop(0))
				count = int(val.pop(0))
				coords = []
				first = True
				for i in range(count + 1):
					x = float(val.pop(0))
					y = float(val.pop(0))
					if self.measurementSystem:
						x *= 25.4
						y *= 25.4
					coords.append((x, y))
					if first:
						rect = (x, y, x, y)
						first = False
					else:
						rect = (min(x, rect[0]),
								min(y, rect[1]),
								max(x, rect[2]),
								max(y, rect[3]))

				rot = float(val.pop(0))
				if rot != 0:
					print 'Polygon rotation %.2f do not support: "%s"' % (rot, name)
				self._macroses[name] = (code, rect, coords)

		elif row.startswith('ADD'):
			r = re.search('ADD(?P<code>[0-9]{1,2})(?P<type>[CRP]{1}),(?P<p1>[0-9\.]+)(X(?P<p2>[0-9\.]+)){0,1}(X(?P<p3>[0-9\.]+)){0,1}(X(?P<p4>[0-9\.]+)){0,1}', row)
			if not r:
				r = re.search('ADD(?P<code>[0-9]{1,2})(?P<name>.+)', row)
				if not r:
					print 'Apperture parsing error: "%s"' % (row)
					return

			data = r.groupdict()
			code = data['code']
			name = data.get('name')
			macros = None
			if name:
				macros = self._macroses.get(name)
				if not macros:
					print 'Apperture macros "%s" not found' % (name)
					return
				aperture = ('M', macros)
			else:
				aperture = (data['type'], [])

				for i in range(4):
					val = data['p%d' % (i+1)]
					if val:
						val = float(val)
						if self.measurementSystem:
							val *= 25.4
						aperture[1].append(val)
			self._apertures[int(code)] = aperture
		elif row == 'LPD':
			self._path.append('V', True)
		elif row == 'LPC':
			self._path.append('V', False)

	def convertCoord(self, x):
		x = float(x)/pow(10, self.xFormat[1])
		if self.measurementSystem:
			x *= 25.4
		return x

	def width(self):
		return self.rect[2] - self.rect[0]

	def height(self):
		return self.rect[3] - self.rect[1]

	def offset(self):
		return (self.rect[0], self.rect[1])

	def path(self):
		return self._path

	def aperture(self, code):
		aperture = self._apertures.get(code)
		if not aperture:
			print 'Unknown aperture %d' % (code)
		return aperture

	def prepareGerber(self, gerber):
		gerber = gerber.replace('\r', '')
		gerber = gerber.replace('\n', '')

		gLen = len(gerber)

		res = []

		i = 0
		while i < gLen:
			if gerber[i] == '%':
				end = gerber.find('%', i+1)
				if end > 0:
					res.append(gerber[i:end+1].strip())
				else:
					print 'Parsing error 1'
					break
			else:
				end = gerber.find('*', i+1)
				if end > 0:

					res.append(gerber[i:end+1].strip())
				else:
					print 'Parsing error 2'
					break
			i = end + 1

		return res

