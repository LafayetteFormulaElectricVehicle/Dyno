from PyQt4 import QtCore, QtGui

from gui import ui_main_window 
from gui import ui_sensor_edit_dialog
from gui import ui_graph_dialog


#  *************************** ADD, MODIFY and DELETE for output hardwares ****************
# *****************************************************************************************

class HardwareOutput(QtGui.QDialog, ui_sensor_edit_dialog.Ui_Dialog):
			
	def __init__(self, mainWin): 
		QtGui.QWidget.__init__(self) 
		self.setupUi(self)
		self.window = mainWin
		
		self.buttonBox_OkCancel.button(QtGui.QDialogButtonBox.Ok).clicked.connect(self.add)
		self.validator = QtGui.QIntValidator(0,1000)

	def add(self):
		sensorCategory = self.comboBox_systemType.currentText()
		sensorName = self.lineEdit_sensorName.text()
		canID =  self.lineEdit_canID.text()

		# sensorID = self.lineEdit_sensorID.text()
				
		slope = self.lineEdit_slope.text()
		offset = self.lineEdit_offset.text()
		
		sensorUnit = self.comboBox_sensorUnits.currentText()
		sensorType = self.comboBox_sensorType.currentText()

		samplingRate = self.lineEdit_samplingRate.text()
		overwritePeroid = self.lineEdit_overWritePeroid.text() 
		value = self.lineEdit_value.text()
		defaultValue = self.lineEdit_defaultValue.text()
		
		tree = self.window.treeWidget_hardwareOutput
		item = QtGui.QTreeWidgetItem()
		item.setText(0, sensorName)
		item.setText(1, sensorType)
		item.setText(2, value )
		item.setText(3, defaultValue)
		item.setText(4, canID)

		tree.addTopLevelItem(item)

class ModifySensorOut(QtGui.QDialog, ui_sensor_edit_dialog.Ui_Dialog):
			
	def __init__(self, mainWin): 
		QtGui.QWidget.__init__(self) 
		self.setupUi(self)
		self.window = mainWin
		
		item = self.window.treeWidget_hardwareOutput.currentItem()
		self.lineEdit_sensorName.setText(item.text(0))
		self.lineEdit_value.setText(item.text(2))
		self.lineEdit_defaultValue.setText(item.text(3))
		index = self.comboBox_sensorType.findText(item.text(1))

		# print(index)
		self.comboBox_sensorType.setCurrentIndex(index)

		self.lineEdit_sensorName.setDisabled(1)
		self.lineEdit_canID.setDisabled(1)
		self.lineEdit_sensorID.setDisabled(1)
		
		self.buttonBox_OkCancel.button(QtGui.QDialogButtonBox.Ok).clicked.connect(self.modify)


	def modify(self):
		item = self.window.treeWidget_hardwareOutput.currentItem()
		
		sensorType = self.comboBox_sensorType.currentText()
		value = self.lineEdit_value.text()
		defaultValue = self.lineEdit_defaultValue.text()

		item.setText(1, sensorType)
		item.setText(2, value)
		item.setText(3, defaultValue)
