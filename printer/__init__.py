# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from serial import Serial


class Printer(QObject):
	def __init__(self, parent = None):
		QObject.__init__(self, parent)
		self.commands = {}

		self.serial = None
		
	def connect_(self, port, baudrate):
		self.serial = Serial(str(port), baudrate)
		return bool(self.serial)

	def disconnect_(self):
		self.serial.close()

	def cmd(self, cmd):
		cmdLine = self.commands[cmd]
		self.serial.write('%s\n', cmdLine)

	def setLaserCmd(self, on, off):
		self.commands['laserOn'] = on
		self.commands['laserOff'] = off

	def laserOn(self, cmd):
		self.cmd('laserOn')


