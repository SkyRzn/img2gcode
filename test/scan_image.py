# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from routines.simple_thread import SimpleThread, closeThreads
import math


resolution = 0.05
gap = 0.5
yInverted = False
laserOn = 'M106'
laserOff = 'M107'
burnSpeed = 600 #mm/min
idleSpeed = 2000 #mm/min

firstPointBurnWait = 0.01 #sec
lastPointBurnWait = 0.001 #sec
lastPointFadeWait = 0.001 #sec

xPretensioning = 0.7
yPretensioning = 0.7



def getPixelChunks(image):
	w = image.width()
	h = image.height()
	rh = h * 0.1

	chains = []

	for y in xrange(h):
		beg = None
		for x in xrange(w):
			if QColor(image.pixel(x, y)).value() == 0:
				if beg == None:
					beg = x
				end = x
				image.setPixel(x, y, Qt.blue)
			else:
				if beg != None:
					chains.append((y, beg, end))
					beg = None

		if beg != None:
			chains.append((y, beg, x))

	return chains

def pic2real(y, beg, end, w, h):
	beg *= resolution
	end *= resolution
	y *= resolution
	if not yInverted:
		y = h * resolution - y
	return (y, beg, end)

def moveTime(x0, y0, x1, y1, speed):
	dx = x1-x0
	dy = y1-y0
	dist = math.sqrt(dx*dx + dy*dy)
	return dist/speed

def get_gcode(pixChains, w, h):
	chunks = []

	chunks.append(('G21; Metric system', None, 0))
	chunks.append(('G90; absolute coords', None, 0))
	chunks.append(('G92 X0 Y0; set position', None, 0))
	chunks.append((laserOff, None, 0))

	curX = 0
	curY = 0
	
	y, beg, end = pixChains[0]
	ry, rbeg, rend = pic2real(y, beg, end, w, h)
	if yPretensioning > 0:
		chunks.append(('G00 X%.3f Y%.3f F%d' % (rbeg, ry+yPretensioning, idleSpeed), None, 0))

	for y, beg, end in pixChains:
		ry, rbeg, rend = pic2real(y, beg, end, w, h)
		t = 0
		gcode = []

		if xPretensioning > 0:
			gcode.append('G00 X%.3f Y%.3f F%d' % (rbeg - xPretensioning, ry, idleSpeed))
			t += moveTime(curX, curY, rbeg - xPretensioning, ry, idleSpeed)


		gcode.append('G00 X%.3f Y%.3f F%d' % (rbeg, ry, idleSpeed))
		t += moveTime(curX, curY, rbeg, ry, idleSpeed)

		gcode.append(laserOn)

		gcode.append('G04 P%d' % (firstPointBurnWait*1000,))
		t += firstPointBurnWait/60

		gcode.append('G01 X%.3f F%d' % (rend, burnSpeed))
		t += moveTime(curX, curY, rend, ry, burnSpeed)

		gcode.append('G04 P%d' % (lastPointBurnWait*1000,))
		t += lastPointBurnWait/60

		gcode.append(laserOff)

		gcode.append('G04 P%d' % (lastPointFadeWait*1000,))
		t += lastPointFadeWait/60

		gcode = '\n'.join(gcode)

		chunks.append((gcode, (y, beg, end), t))

		curX, curY = rend, ry
		
	chunks.append(('M0', None, 0))
	return chunks




