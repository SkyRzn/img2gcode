# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from routines.simple_thread import SimpleThread, closeThreads
import math


resolution = 0.1
gap = 0.5
yInverted = False
laserOn = 'M106'
laserOff = 'M107'
burnSpeed = 300 #mm/min
idleSpeed = 3000 #mm/min

firstPointBurnWait = 0.2 #sec
lastPointBurnWait = 0.1 #sec
lastPointFadeWait = 0.1 #sec

xPretensioning = 0.7
yPretensioning = 0.7



def getPixelChunks(data):
	h, w = data.shape
	rh = h * 0.1

	chains = []

	for y in xrange(h):
		beg = None
		for x in xrange(w):
			if data[y][x] == 0:
				if beg == None:
					beg = x
				end = x
				data[y][x] = 0x88
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

	chunks.append('G21; Metric system', None)
	chunks.append('G90; absolute coords', None)

	curX = 0
	curY = 0

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

		gcode = '\n'.gcode

		chunks.append((gcode, (y, beg, end), t))

		curX, curY = rend, ry
	return chunks




