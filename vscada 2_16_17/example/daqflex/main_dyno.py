#!/usr/bin/env python3
import sys
#import mcdaq
import lib.lib_can

from PyQt4 import QtGui, QtCore
from gui.ui_main_dyno import Ui_DynoMainWindow
from gui.ui_callibration import Ui_CalibrationDialog
from gui.ui_settings import Ui_SettingsDialog
from gui.ui_program import Ui_ProgramDialog
from gui.ui_edit_program import Ui_ProgramEditDialog

import pyqtgraph as pg
import numpy as np

_pollFrequency = 3.0

_demoMode = False

try: 
	_HuffBox = mcdaq.HuffBox()
except:
	print('Demo Mode')
	_demoMode = True


_slopeTorque = 0.366
_offsetTorque = -641.906

_slopeRPM = -4.499
_offsetRPM = 9402.315

_motorRPM = 0
_motorTemp = 0
_controllerTemp = 0
_rmsCurrent = 0
_capVoltage = 0

_pauseCollection = False

class SensorValueThread(QtCore.QThread):
	def run(self):
		global _pauseCollection
		while(True):
			self.msleep(1000 / _pollFrequency)
			if not _pauseCollection:
				self.emit(QtCore.SIGNAL('update()'))


_mc_descr = [{'name': 'Motor RPM', 'bit-offset': 0, 'bit-length': 2, 'single-bit': False }, { 'name': 'Motor Temp', 'bit-offset': 2, 'bit-length': 1, 'single-bit': False }, { 'name': 'Controller Temp', 'bit-offset': 3, 'bit-length': 1, 'single-bit': False }, { 'name': 'RMS Current', 'bit-offset': 4, 'bit-length': 2, 'single-bit': False }, { 'name': 'Capacitor Voltage', 'bit-offset': 6, 'bit-length': 2, 'single-bit': False }]

class CANBusMonitorThread(QtCore.QThread):
	can_dev = None
	def run(self):
		global _motorRPM
		global _motorTemp
		global _controllerTemp
		global _rmsCurrent
		global _capVoltage
		self.can_dev = lib.lib_can.CANDataHandler()
		while(True):
			recv = self.can_dev.recv_data_frame(1537, _mc_descr)
			_motorRPM = recv[0]['value'] * 1
			_motorTemp = recv[1]['value'] * 1
			_controllerTemp = recv[2]['value'] * 1
			_rmsCurrent = recv[3]['value'] * 0.1
			_capVoltage = recv[4]['value'] * 0.1
			
class DynoMainWindow(QtGui.QMainWindow, Ui_DynoMainWindow):
	#sensor value update thread
	sensorThread = None
	
	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		self.setupUi(self)
		self.connectSignals()
		self.initGraph()
		self.startInputThread()
	
	def startInputThread(self):
		self.sensorThread = SensorValueThread()
		self.canThread = CANBusMonitorThread()
		
		QtCore.QObject.connect(
				self.sensorThread,
				QtCore.SIGNAL('update()'),
				self.updateDynoSensorValues)	

		self.canThread.start()
		self.sensorThread.start()

	def initGraph(self):
		#set graph background to white
		pg.setConfigOption('background', 'w')
		pg.setConfigOption('foreground', 'k')
		
		#x = np.arange(10)
		#y = np.random.normal(size=10)
		#print('X: ', x[-1:])
		#print('Y: ', y)
		#self.graphicsView.plot(x, y, pen=1)  ## setting pen=(i,3) automaticaly creates three different-colored pens
		self.graphicsView.setTitle("<h1>Motor Torque Curve</h1>")
		self.graphicsView.setLabels(title='<h1>Motor Torque Curve</h1>', left='Power (hp)', bottom='Time (Seconds)')
		self.graphicsView.showButtons()

	def connectSignals(self):
		"""Connect all Qt Signals and Slots in DynoMainWindow"""
		#throttle slider-spinbox connection
		QtCore.QObject.connect(
				self.hSliderThrottle,
				QtCore.SIGNAL('valueChanged(int)'),
				self.spinBoxThrottle.setValue)	
		QtCore.QObject.connect(
				self.spinBoxThrottle,
				QtCore.SIGNAL('valueChanged(double)'),
				self.hSliderThrottle.setValue)	
		#load solenoid slider-spinbox connection
		QtCore.QObject.connect(
				self.hSliderLoad,
				QtCore.SIGNAL('valueChanged(int)'),
				self.spinBoxLoad.setValue)	
		QtCore.QObject.connect(
				self.spinBoxLoad,
				QtCore.SIGNAL('valueChanged(double)'),
				self.hSliderLoad.setValue)	
		
		#config->calibrate show calibration dialog
		QtCore.QObject.connect(
				self.actionCallibrate,
				QtCore.SIGNAL('triggered()'),
				self.showCalibrationDialog)	
		
		#config->settings show settings dialog
		QtCore.QObject.connect(
				self.actionSettings,
				QtCore.SIGNAL('triggered()'),
				self.showSettingsDialog)	
		
		#config->settings show settings dialog
		QtCore.QObject.connect(
				self.actionRunProgram,
				QtCore.SIGNAL('triggered()'),
				self.showProgramEditDialog)	
		
		#config->settings show settings dialog
		QtCore.QObject.connect(
				self.actionProgramManage,
				QtCore.SIGNAL('triggered()'),
				self.showProgramDialog)	
		
		#file-exit action
		QtCore.QObject.connect(
				self.actionExit,
				QtCore.SIGNAL('triggered()'),
				self.close)	
		
		#emergency button click
		QtCore.QObject.connect(
				self.buttonEmergency,
				QtCore.SIGNAL('clicked()'),
				self.buttonEmergencyClicked)	
				
		#pause button click
		QtCore.QObject.connect(
				self.buttonPauseData,
				QtCore.SIGNAL('clicked()'),
				self.buttonPauseDataClicked)	
				
	def updateDynoSensorValues(self):
		#print(integer)
		#if not _demoMode:
		#strain_guage = _HuffBox.get_strain_guage()*_slopeTorque + _offsetTorque
		#tachometer = _HuffBox.get_tachometer()*_slopeRPM + _offsetRPM
		#power = (strain_guage) * (tachometer) / 5252
		
		#Dyno Box
		#self.lcdNumberTorque.display(strain_guage)
		#self.lcdNumberTach.display(tachometer)
		#self.lcdNumberPower.display(power)
		
		#CAN Bus
		self.lcdNumberTachCAN.display(_motorRPM)
		self.lcdNumberCurrent.display(_rmsCurrent)
		self.lcdNumberVoltage.display(_capVoltage)
		self.lcdNumberMCTemp.display(_controllerTemp)
		self.lcdNumberMTemp.display(_motorTemp)
		
		#Set System Outpus (Dyno Box)
		#throttle_value = self.hSliderThrottle.value()*4095/100
		#load_value = self.hSliderLoad.value()*4095/100
		#_HuffBox.set_throttle(throttle_value)
		#_HuffBox.set_load_valve(load_value)
		#self.updateGraph(power)
		
	x = []	
	y = []	
	def updateGraph(self, _y):
		"""Add a new value to the graph"""
		if not self.x:
			
			self.x = [1/_pollFrequency]
			self.y = [_y]
		else:
			self.x.append(self.x[-1:][0] + 1/_pollFrequency)
			self.y.append(_y)
		
		self.graphicsView.plot(self.x, self.y)
	
	def showCalibrationDialog(self):
		"""Show the Dynamometer Calibration Dialog"""
		
		dialog = CalibrationDialog(self)
		dialog.show()
	
	def showSettingsDialog(self):
		"""Show the Dynamometer Settings Dialog"""
		
		dialog = SettingsDialog(self)
		dialog.exec_()
	
	def showProgramDialog(self):
		"""Show the Dynamometer Settings Dialog"""
		
		dialog = ProgramDialog(self)
		dialog.exec_()
	
	def showProgramEditDialog(self):
		"""Show the Dynamometer Settings Dialog"""
		
		dialog = ProgramEditDialog(self)
		dialog.exec_()

		
	def buttonEmergencyClicked(self):
		"""Emergency Stop, cut throttle and load"""
		self.hSliderThrottle.setValue(0);
		self.hSliderLoad.setValue(0);
				
	def buttonPauseDataClicked(self):
		"""Pause Data Collection by setting global flag"""
		global _pauseCollection
		_pauseCollection = self.buttonPauseData.isChecked()
		
				
class CalibrationDialog(QtGui.QDialog, Ui_CalibrationDialog):
	def __init__(self,parent=None):
		QtGui.QDialog.__init__(self,parent)
		self.setupUi(self)
		
class SettingsDialog(QtGui.QDialog, Ui_SettingsDialog):
	def __init__(self,parent=None):
		QtGui.QDialog.__init__(self,parent)
		self.setupUi(self)
		
class ProgramDialog(QtGui.QDialog, Ui_ProgramDialog):
	def __init__(self,parent=None):
		QtGui.QDialog.__init__(self,parent)
		self.setupUi(self)
		
class ProgramEditDialog(QtGui.QDialog, Ui_ProgramEditDialog):
	def __init__(self,parent=None):
		QtGui.QDialog.__init__(self,parent)
		self.setupUi(self)
		
	
if __name__ == "__main__":
	pg.setConfigOption('background', 'w')
	pg.setConfigOption('foreground', 'k')
	
	app = QtGui.QApplication(sys.argv)
	window = DynoMainWindow()
	window.show()
	sys.exit(app.exec_())
