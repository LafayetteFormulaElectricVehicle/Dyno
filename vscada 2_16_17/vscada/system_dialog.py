from PyQt4 import QtCore, QtGui

from gui import ui_main_window 
from gui import ui_sensor_edit_dialog
from gui import ui_graph_dialog

import main

import pyqtgraph as pg


#  *********************** SYSTEM DIALOGS AND WARNING MESSAGE WINDOWS *********************
# *****************************************************************************************
# Brings up the graphing window to display the graphed values of an input sensor

class GraphDialogIn(QtGui.QDialog, ui_graph_dialog.Ui_Dialog):
	
	epoch_start_time = None
	time = []
	y = []
	
	def __init__(self, mainWin):
		QtGui.QDialog.__init__(self)
		self.setupUi(self)
		self.window = mainWin
		self.initGraph()

	def initGraph(self):
		#set graph background to white
		pg.setConfigOption('background', 'w')
		pg.setConfigOption('foreground', 'k')

		#TODO: change this, get name from tree
		measurand_str = str(self.window.treeWidget_inputMeasurands.selectedItems()[0].text(0))
		unit_str = str(self.window.treeWidget_inputMeasurands.selectedItems()[0].\
					   text(self.window.input_header_labels.index('Units')))
		graph_title = '<h1>' + measurand_str.capitalize() + ' Graph</h1>'
		self.graphicsView.setTitle("<h1>%s</h1>" % graph_title)
		self.graphicsView.setLabels(title=graph_title, left=unit_str, bottom='Time (s)')
		self.graphicsView.showButtons()

	def updateGraph(self, _epoch_time, _y):
		"""Add a new value to the graph"""
		if self.epoch_start_time == None:
			epoch_start_time = _epoch_time
			self.time = [0]
			self.y = [_y]
		else:
			self.time.append(_epoch_time - epoch_start_time)
			self.y.append(_y)
		
		self.graphicsView.plot(self.time, self.y)
