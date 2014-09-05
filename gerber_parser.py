# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import re


class Gerber:
	def __init__(self):
		pass

	def parse(self, filename):
		self._init()

		if not self._loadFile(filename):
			return False

		return self._parse()

	def _init(self):
		self.gerber = []
		self.comments = []
		self.zeros = 'L'
		self.mode = 'A' #FIXME
		self.xFormat = (0, 0)
		self.yFormat = (0, 0)
		self.measurementSystem = 0 # 0 - mm, 1 - inch
		self.apertures = {}
		self.paths = [] # (aperture, [(x,y), ...])
		self.rect = None

	def _loadFile(self, filename):
		f = open(filename, 'r')
		if not f:
			return False
		self.gerber = f.readlines()
		f.close()
		if not self.gerber:
			self.gerber = []
			return False
		return True

	def _parse(self):

		aperture = None
		path = []
		D = None
		for row in self.gerber:
			row = row.strip()
			row = row.strip('*')

			if row.startswith('G04'):
				self.comments.append(row[3:].strip())
			elif row.startswith('%') and row.endswith('%'):
				self._parseHeaderRow(row)
				continue
			elif row.startswith('G54'): # select aperture
				if path:
					self.paths.append((D, aperture, path))
					path = []
				r = re.search('D([0-9]+)', row)
				aperture = int(r.groups()[0])
			elif row.startswith('X'):
				r = re.search('X(?P<x>[\+\-0-9]+)Y(?P<y>[\+\-0-9]+)D(?P<d>[0-9]+)', row)
				x, y = self.convertCoords(r.groupdict()['x'], r.groupdict()['y'])
				d = int(r.groupdict()['d'])
				if d != D:
					if path:
						self.paths.append((D, aperture, path))
					path = []
					D = d

				path.append((x, y))

				if D == 3:
					self.paths.append((D, aperture, path))
					path = []

				if self.rect == None:
					self.rect = (x, y, x, y)
				else:
					self.rect = (min(x, self.rect[0]),
								min(y, self.rect[1]),
								max(y, self.rect[2]),
								max(y, self.rect[3]))
		if path:
			self.paths.append((D, aperture, path))

		return True

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

	def convertCoords(self, sx, sy):
		xneg = (sx[0] == '-')
		yneg = (sy[0] == '-')
		sx = sx.strip('+-')
		sy = sy.strip('+-')

		lx = sum(self.xFormat)
		ly = sum(self.yFormat)
		if self.zeros == 'L':
			sx = sx.rjust(lx, '0')
			sy = sy.rjust(ly, '0')
		elif self.zeros == 'T':
			sx = sx.ljust(lx, '0')
			sy = sy.ljust(ly, '0')

		if self.zeros != 'D':
			sx = sx[:self.xFormat[0]] + '.' + sx[self.xFormat[0]:]
			sy = sy[:self.yFormat[0]] + '.' + sy[self.yFormat[0]:]

		x = float(sx)
		if xneg:
			x = -x
		y = float(sy)
		if yneg:
			y = -y

		if self.measurementSystem:
			print '!!!!!!!!!!!!!'
			x *= 25.4
			y *= 25.4

		return (x, y)

	def width(self):
		return self.rect[2] - self.rect[0]

	def height(self):
		return self.rect[3] - self.rect[1]

	def offset(self):
		return (self.rect[0], self.rect[1])


