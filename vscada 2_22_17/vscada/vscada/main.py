#!/usr/bin/env python3
import csv
import logging
import os
import socket
import sys

from PyQt4 import QtCore, QtGui

from gui import ui_main_window 
from gui import ui_sensor_edit_dialog
from gui import ui_graph_dialog

from system_input import *
from system_output import *
from system_dialog import *

import pyqtgraph as pg

from lib.mcdaq import mcdaq
from lib.can import lib_can
from lib import magna_control

##################################
# <Temporary Dyno Monitor Code>
##################################

_pollFrequency = 3.0

_demoMode = False

try: 
	_HuffBox = mcdaq.HuffBox()
except:
	print('Huff Box not connected...')
	_demoMode = True

#global time counter
_time = 0

#CAN Stuff
_motorRPM = 0
_motorTemp = 0
_controllerTemp = 0
_rmsCurrent = 0
_capVoltage = 0

_motorThrottle = 0

#PSU
_psu_voltage = 0
_psu_current = 0


_psu_wattage = (_psu_voltage)*(_psu_current) #Richard Diego Added 2/16/17

#Huff Stuff
_strain_guage = 0
_tachometer = 0
_dyno_power = 0
_throttle_value = 0
_load_value = 0

#Testing Huff Stuff - Richard Diego 2/16/17

_testVal = 4095/100

#load_vaue is 0 = max resist, 4095/100 is no resistance; 

#End Testing Huff Stuff

_slopeTorque = 0.366
_offsetTorque = -641.906
#Original Slope: .366; Original Offset: -641.906


_slopeRPM = -4.499
_offsetRPM = 8602.315
#Original Slope: -4.499 ; Original offsetRPM: 9402.315

_pauseCollection = False


#Motor Controller CAN Frame Descriptor 0x601
_mc_descr_1 = [ { 'id': 0, 'name': 'Motor RPM', 'offset': 0, 'length': 2, 'single-bit': False, 'bit': 0 }, { 'id': 1, 'name': 'Motor Temperature', 'offset': 2, 'length': 1, 'single-bit': False, 'bit': 0 }, { 'id': 2, 'name': 'Motor Controller Temperature', 'offset': 3, 'length': 1, 'single-bit': False, 'bit': 0 }, { 'id': 3, 'name': 'Motor Controller RMS Current', 'offset': 4, 'length': 2, 'single-bit': False, 'bit': 0 }, { 'id': 4, 'name': 'Motor Controller Capacitor Voltage', 'offset': 6, 'length': 2, 'single-bit': False, 'bit': 0 } ]

#Motor Controller CAN Frame Descriptor 0x602
_mc_descr_2 = [{ 'id': 5, 'name': 'Stator Frequency', 'offset': 0, 'length': 2, 'single-bit': False, 'bit': 0 }, { 'id': 6, 'name': 'Controller Fault Primary', 'offset': 2, 'length': 1, 'single-bit': False, 'bit': 0 }, { 'id': 7, 'name': 'Controller Fault Secondary', 'offset': 3, 'length': 1, 'single-bit': False, 'bit': 0 }, { 'id': 8, 'name': 'Throttle Input', 'offset': 4, 'length': 1, 'single-bit': False, 'bit': 0 }, { 'id': 9, 'name': 'Brake Input', 'offset': 5, 'length': 1, 'single-bit': False, 'bit': 0 }, { 'id': 9, 'name': 'Economy Bit', 'offset': 6, 'length': 1, 'single-bit': False, 'bit': 0 }, { 'id': 9, 'name': 'Regeneration Bit', 'offset': 6, 'length': 1, 'single-bit': False, 'bit': 1 }, { 'id': 9, 'name': 'Reverse Bit', 'offset': 6, 'length': 1, 'single-bit': False, 'bit': 2 }, { 'id': 9, 'name': 'Brake Light Bit', 'offset': 6, 'length': 1, 'single-bit': False, 'bit': 3 } ]

try:
	_psu_control = magna_control.PowerSupplyControl('/dev/ttyUSB0', 19200)
except:
	print('cannot connect to psu')

#reference csv header value
_csv_header = ['time','dyno_rpm','dyno_torque','dyno_power','dyno_throttle','dyno_load','can_mc_rpm','can_mc_current','can_mc_voltage','can_mc_temp','can_m_temp','can_mc_throttle', 'psu_volt', 'psu_cur']

#RAM logging structure
_data = []

#Graphing Arrays
_time_x = []
_pwr_y = []
_torq_y = []
_rpm_y = []
_volt_y = []
_cur_y = []
_watts_y = []

def _append_temp_data(row):
	'''
	Appends data to the in-memory data storage block (_data)
	'''
	global _data
	_data.append(row)

#Inspired by: http://stackoverflow.com/questions/2819791/how-can-i-redirect-the-logger-to-a-wxpython-textctrl-using-a-custom-logging-hand
#And also: http://stackoverflow.com/questions/24469662/how-to-redirect-logger-output-into-pyqt-text-widget
class pyQTLogHandler(logging.Handler):
	"""
	Comment ME!
	"""
	widget_list = None
	
	def __init__(self, _widget_list=None, _level=logging.DEBUG):
		"""
		Comment Here...
		"""
		logging.Handler.__init__(self)
		self.widget_list = _widget_list
		self.level = _level

	def emit(self, _record):
		"""
		Emit a record
		"""
		try:
			record = self.format(_record)
			#print(self.format(_record))
			if _record.levelname == "CRITICAL":
				self.widget_list['CRITICAL'].appendPlainText(record)
				
			elif _record.levelname == "ERROR":
				self.widget_list['ERROR'].appendPlainText(record)
				
			elif _record.levelname == "WARNING":
				self.widget_list['WARNING'].appendPlainText(record)
				
			elif _record.levelname == "INFO":
				self.widget_list['INFO'].appendPlainText(record)
				
			elif _record.levelname == "DEBUG":
				self.widget_list['DEBUG'].appendPlainText(record)
			else:
				print(self.format(_record))
		except:
			print('LOGGER ERROR!!! PANIC!!! RUN FOR THE HILLS!!!')

class GuiUpdateThread(QtCore.QThread):
	'''
	GUI Update Thread
	
	This thread is responsible for updating the UI elements at a regular
	frequency determined by the global variable _pollFrequency. The system is
	updated every 1/_pollFrequency seconds.
	'''
	
	def run(self):
		global _pauseCollection
		global _time
		global _pwr_y
		global _torq_y
		global _rpm_y
		global _psu_voltage
		global _psu_current

		while(True):
			self.msleep(1000 / _pollFrequency)
			_time += 1 / _pollFrequency
			try: 
				volt = _psu_control.get_voltage() 
				curr = _psu_control.get_current()
				_psu_voltage = volt
				_psu_current = curr
			except:
				logger.error('unable to read from power supply')
			if not _pauseCollection:
				#update GUI
				self.emit(QtCore.SIGNAL('update()'))
				
				#generate data row
				row = [
						_time , 
						_tachometer,
						_strain_guage,
						_dyno_power,
						_throttle_value,
						_load_value,
						_motorRPM,
						_rmsCurrent,
						_capVoltage,
						_controllerTemp,
						_motorTemp,
						_motorThrottle,
						_psu_voltage,
						_psu_current ] 
				
				#append data to RAM
				_append_temp_data(row)
				
				#update time array
				_time_x.append(_time)
				
				#dyno power graph data
				_pwr_y.append(_dyno_power)
				
				#dyno torque data
				_torq_y.append(_strain_guage)
				
				#motor controller rpm graph data
				_rpm_y.append(_motorRPM/100)
				
				#psu graph
				_volt_y.append(_psu_voltage)
				_cur_y.append(_psu_current)
				



class CanMonitorThread(QtCore.QThread):
	'''
	CAN Bus Monitor Thread
	
	This thread is responsible fro regularly polling the CAN Bus, and 
	determining if new data is available for consuption.
	'''
	can_dev = None
		
	def run(self):
		#FIXME put in init?
		try:
			self.can_dev = lib_can.CANDataHandler('can0')
		except:
			print('Cannot Connect to CAN device')
			return
		
		#global variables
		global _motorRPM
		global _motorTemp
		global _controllerTemp
		global _rmsCurrent
		global _capVoltage
		
		while(True):
			#receive all available frames
			while(self.can_dev.recv_frame()):
				pass
			
			#Motor Controller 0x601
			if self.can_dev.frame_available(1537):
				recv = self.can_dev.recv_data_frame(1537, _mc_descr_1)
				_motorRPM = recv[0]['value'] * 1
				_motorTemp = recv[1]['value'] * 1
				_controllerTemp = recv[2]['value'] * 1
				_rmsCurrent = recv[3]['value'] * 0.1
				_capVoltage = recv[4]['value'] * 0.1
				#print(recv)
				
			#Motor Controller 0x602
			if self.can_dev.frame_available(1538):
				recv = self.can_dev.recv_data_frame(1538, _mc_descr_2)
				_motorThrottle = recv[3]['value'] * 1
				#print(recv)
				
			#FIXME, required to prevent program from eating up cpu
			#use blocking recv func?
			self.msleep(100)
	

##################################
# </Temporary Dyno Monitor Code>
##################################
logger = None

class Window(QtGui.QMainWindow, ui_main_window.Ui_MainWindow):
	'''
	VSCADA Main Window Class
	
	This is the main VSCADA program/window.
	'''
	
	#CAN Monitor Thread
	can_monitor = None
	
	#GUI Update Thread
	gui_update = None
	
	def __init__(self):
		QtGui.QWidget.__init__(self)
		self.setupUi(self)

		global logger
		
		logger_widgets = {
			"INFO": self.plainTextEditMsgs, 
			"ERROR": self.plainTextEditErr,
			"WARNING": self.plainTextEditWarn,
			"DEBUG": self.plainTextEditDebug
		}
		
		logger = logging.getLogger(__name__)
		handler = pyQTLogHandler(logger_widgets)
		handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
		logger.addHandler(handler)
		logger.setLevel(logging.DEBUG)
		logger.info("LFEV Dynamometer Program Started!")
		
		#overwrite old csv, write header
		_append_temp_data(_csv_header)
		
		#connect Qt signals
		# ***************** Menu Bar Signals ****************************
		#config->settings show settings dialog
		QtCore.QObject.connect(
				self.actionSettings,
				QtCore.SIGNAL('triggered()'),
				self.showSettingsDialog)	
		
		QtCore.QObject.connect(
				self.actionSave,
				QtCore.SIGNAL('triggered()'),
				self.actionSaveTriggered)	
		
		#file-exit action
		QtCore.QObject.connect(
				self.actionExit,
				QtCore.SIGNAL('triggered()'),
				self.close)	
		

		# ***************** Dyno Window *********************************
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
		
		#clear data button click
		QtCore.QObject.connect(
				self.buttonClearData,
				QtCore.SIGNAL('clicked()'),
				self.buttonClearDataClicked)	
		
		# ***************** PSU TAB*********************************
		
		QtCore.QObject.connect(
				self.spinBoxPSUVoltage,
				QtCore.SIGNAL('valueChanged(double)'),
				self.spinBoxPSUVoltageChanged)	
		QtCore.QObject.connect(
				self.spinBoxPSUCurrent,
				QtCore.SIGNAL('valueChanged(double)'),
				self.spinBoxPSUCurrentChanged)	
		QtCore.QObject.connect(
				self.buttonPSUOn,
				QtCore.SIGNAL('clicked()'),
				self.buttonPSUOnClicked)	
		QtCore.QObject.connect(
				self.buttonPSUOff,
				QtCore.SIGNAL('clicked()'),
				self.buttonPSUOffClicked)	
		# ***************** Measurands Inputs ****************************
		# *******************  Rules    *************************************
		
		self.initGraph(self.dynoDataPlot, 'Dyno Graph', 'Units', 'Time (seconds)')
		self.initGraph(self.psuDataPlot, 'Power Supply Graph', 'Units', 'Time (seconds)')
		
		self.gui_update = GuiUpdateThread()
		self.can_monitor = CanMonitorThread()
		
		self.gui_update.start()
		self.can_monitor.start()
		
		QtCore.QObject.connect(
				self.gui_update,
				QtCore.SIGNAL('update()'),
				self.guiUpdate)
		self.initPSUButtons()
	
	def spinBoxPSUVoltageChanged(self, value):
		'''
		Power Supply Voltage Control Spin Box Changed
		'''
		try:
			_psu_control.set_voltage(value)
		except:
			logging.error('unable to set PSU voltage')
		
	def spinBoxPSUCurrentChanged(self, value):
		'''
		Power Supply Current Control Spin Box Changed
		'''
		try:
			_psu_control.set_current(value)
		except:
			logging.error('unable to set PSU current')
	
	def initPSUButtons(self):
		try:
			psu_state = _psu_control.get_state()
			self.buttonPSUOn.setDisabled(not psu_state)
			self.buttonPSUOff.setDisabled(psu_state)
		except:
			print('PSU not connected')
			self.buttonPSUOn.setDisabled(False)
			self.buttonPSUOff.setDisabled(False)

	def initGraph(self, widget, _title, _left, _bottom):
		'''
		Instantiates a pyqtgraph
		'''
		widget.setLabels(
				title = '<h1>' + _title + '</h1>',
				left = _left,
				bottom = _bottom)
		widget.addLegend()
		widget.showButtons()
	
	def updateGraph(self, widget, data_set):
		#clear old graph data
		widget.clear()
		widget.plotItem.legend.items = []
		widget.plot([], [], clear=True)
		
		#write each new line
		for line in data_set:
			_name = line['name']
			_pen = line['pen']
			_x = line['x']
			_y = line['y']
			widget.plot(_x, _y, pen=_pen, name=_name)
		
	def actionSaveTriggered(self):
		cur_dir = os.path.dirname(os.path.realpath(__file__))
		fileName = QtGui.QFileDialog.getSaveFileName(self, 'Save Collected Data', cur_dir, 'Text CSV Data File (*.csv)') 
		
		print(fileName)
		#if dialog returns file name, write data to csv
		if fileName:
			with open(fileName, 'w') as fd:
				for row in _data:
					csv_writer = csv.writer(fd)
					csv_writer.writerow(row)
			print('file written')

		
	def guiUpdate(self):
		global _strain_guage
		global _tachometer
		global _dyno_power
		global _throttle_value
		global _load_value 

		#Dyno Box
		if not _demoMode:
			#input
			_strain_guage = (_HuffBox.get_strain_guage()*_slopeTorque + _offsetTorque) / 2.5
			
			
			
			#_tachometer = _HuffBox.get_tachometer()*_slopeRPM + _offsetRPM
			#This is the original Tachometer value calculated by offsets at the top of the file
			
			_tachometer = _psu_wattage
			#I am reusing this text box to show the voltage and current of the system
			#Currently the current and voltage obtained by the system are not correct of 2_16_17
			
			
			
			
			#dyno power 
			#power = (_strain_guage) * (_tachometer) / 5252
			#curtis-dyno power
			_dyno_power = (_strain_guage) * (_motorRPM) / 5252
			
		
			#gui
			self.lcdNumberTorque.display(_strain_guage)
			self.lcdNumberTach.display(_tachometer)
			self.lcdNumberPower.display(_dyno_power)
			
			_throttle_value = self.hSliderThrottle.value()*4095/100
			#This is the Throttle Control Bar
			
			
			#_load_value = _testVal - self.hSliderLoad.value()*4095/100
			_load_value = self.hSliderLoad.value()*4095/100 #OriginalLoadValue
			#This is the Resistance/Solenoid Control Bar
			
			
			_HuffBox.set_throttle(_throttle_value)
			_HuffBox.set_load_valve(_load_value)

		
		#CAN Bus
		self.lcdNumberTachCAN.display(_motorRPM)
		self.lcdNumberCurrent.display(_rmsCurrent)
		self.lcdNumberVoltage.display(_capVoltage)
		self.lcdNumberMCTemp.display(_controllerTemp)
		self.lcdNumberMTemp.display(_motorTemp)

		#PSU
		self.label.setText(str(_psu_voltage))
		self.label_2.setText(str(_psu_current))
		
		#Set System Outputs (Dyno Box)
		dyno_plot_lines = [
				{'name': 'Power (hp)', 'pen': (0, 3), 'x': _time_x, 'y': _pwr_y },
				{'name': 'Torque (lb ft)', 'pen': (1, 3), 'x': _time_x, 'y': _torq_y},
				{'name': 'Speed (rpm x100)', 'pen': (2, 3), 'x': _time_x, 'y': _rpm_y}
		]
		
		psu_plot_lines = [
				{'name': 'Volts (V)', 'pen': (0, 2), 'x': _time_x, 'y': _volt_y},
				{'name': 'Current (A)', 'pen': (1, 2), 'x': _time_x, 'y': _cur_y}
		]
				
		self.updateGraph(self.dynoDataPlot, dyno_plot_lines)
		self.updateGraph(self.psuDataPlot, psu_plot_lines)

	def showSettingsDialog(self):
		"""Show the Dynamometer Settings Dialog"""
		dialog = SettingsDialog(self)
		dialog.exec_()
	
	def buttonEmergencyClicked(self):
		"""Emergency Stop, cut throttle and load"""
		self.hSliderThrottle.setValue(0);
		self.hSliderLoad.setValue(0);
				
	def buttonPauseDataClicked(self):
		"""Pause Data Collection by setting global flag"""
		global _pauseCollection
		_pauseCollection = self.buttonPauseData.isChecked()
		
	def buttonClearDataClicked(self):
		"""Pause Data Collection by setting global flag"""
		ret = QtGui.QMessageBox.warning(self, 
				'Clear Collection Data?',
				'<h2>You are about to clear all collected data. \r\n </h2>'
				'Any collected data will be lost. Are you sure you want to clear all data?', QtGui.QMessageBox.Ok, QtGui.QMessageBox.Cancel)
		#clear data only if user says 'Ok'
		if ret == QtGui.QMessageBox.Ok:
			global _data
			global _time
			global _time_x
			global _pwr_y
			global _torq_y
			global _rpm_y
			global _volt_y
			global _cur_y
			global _watts_y
			
			#clear local data storage
			_data = []
			_append_temp_data(_csv_header)
			_time = 0
			
			#clear graph data
			_time_x = []
			_pwr_y = []
			_torq_y = []
			_rpm_y = []
			_volt_y = []
			_cur_y = []
			_watts_y = []
			self.updateGraph(self.dynoDataPlot, dyno_plot_lines)
			self.updateGraph(self.psuDataPlot, psu_plot_lines)
	
	def buttonPSUOnClicked(self):
		_psu_control.set_state(True)
		self.buttonPSUOn.setDisabled(True)
		self.buttonPSUOff.setDisabled(False)
		
	def buttonPSUOffClicked(self):
		_psu_control.set_state(False)
		self.buttonPSUOff.setDisabled(True)
		self.buttonPSUOn.setDisabled(False)
				
if __name__ == "__main__":
	pg.setConfigOption('background', 'w')
	pg.setConfigOption('foreground', 'k')
	app = QtGui.QApplication(sys.argv)
	
	window = Window()
	# window.populateData_systemInput(file_name)

	window.show()
	sys.exit(app.exec_())
