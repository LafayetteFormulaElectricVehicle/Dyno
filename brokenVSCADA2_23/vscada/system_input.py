from PyQt4 import QtCore, QtGui

from gui import ui_main_window 
from gui import ui_sensor_edit_dialog
from gui import ui_graph_dialog

from lib.sql import lib_sql
DATABASE_NAME = '/data/sql/sensor.db'

# ********************** INPUT Sensor ADD, MODIDFY and DELETE ****************
# ****************************************************************************

class AddSensorIn(QtGui.QDialog, ui_sensor_edit_dialog.Ui_Dialog):
			
	def __init__(self, mainWin): 
		QtGui.QWidget.__init__(self) 
		self.setupUi(self)
		self.window = mainWin
		self.lineEdit_value.setDisabled(1)
		self.lineEdit_defaultValue.setDisabled(1)
		self.buttonBox_OkCancel.button(QtGui.QDialogButtonBox.Ok).clicked.connect(self.add)
		self.validator = QtGui.QIntValidator(0,1000)

	def add(self):
		sensorCategory = self.comboBox_systemType.currentText()
		sensorName = self.lineEdit_sensorName.text()
		canID =  self.lineEdit_canID.text()
		#slope = self.lineEdit_slope.text()
		offset = self.lineEdit_offset.text()
		sensorUnit = self.comboBox_sensorUnits.currentText()
		sensorType = self.comboBox_sensorType.currentText()
		samplingRate = self.lineEdit_samplingRate.text()
		overwritePeroid = self.lineEdit_overWritePeroid.text() 

		# list of fields of sensor  
		sensorDict = {
			'sensorCategory': sensorCategory, 
			'sensorName':sensorName,
			'sensorUnit':sensorUnit,
			'sensorType':sensorType,
			# 'addressOffset':addressOffset,
			# 'byteSize':byteSize,
			'canID':canID,
			'slope':slope,
			'offset':offset,
			'samplingRate':samplingRate,
			'overwritePeroid': overwritePeroid }

		#  call method in main window to add a new sensro 
		

		result = self.window.db.add_sensor(
			canID,
			sensorType,
			1,
			2,
			sensorName,
			sensorUnit
			)

		if result['query_status'] == 'success':
			self.window.addInputSensor(sensorDict)
		else:
			print(result['query_status'] , ": ", result['reason'])

# modify the input sensors and measurands
class ModifySensorIn(QtGui.QDialog, ui_sensor_edit_dialog.Ui_Dialog):
			
	def __init__(self, mainWin): 
		QtGui.QWidget.__init__(self) 
		self.setupUi(self)
		self.window = mainWin
		self.lineEdit_sensorName.setDisabled(1)
		self.lineEdit_canID.setDisabled(1)
		self.lineEdit_sensorID.setDisabled(1)
		self.comboBox_systemType.setEnabled(False)
		self.comboBox_sensorType.setEnabled(False)
		
		item = self.window.treeWidget_inputMeasurands.currentItem()

		self.lineEdit_sensorName.setText(item.text(0))  
		self.lineEdit_value.setText(item.text(1))
		self.lineEdit_defaultValue.setText(item.text(3))
						
		index = self.comboBox_sensorType.findText(item.text(4))
		self.comboBox_sensorType.setCurrentIndex(index)
		self.lineEdit_canID.setText(item.text(5))
		self.lineEdit_slope.setText(item.text(6))
		self.lineEdit_offset.setText(item.text(7))
		self.lineEdit_samplingRate.setText(item.text(8))
		self.lineEdit_overWritePeroid.setText(item.text(9))

		self.buttonBox_OkCancel.button(QtGui.QDialogButtonBox.Ok).clicked.connect(self.modify)


	def modify(self):
		item = self.window.treeWidget_inputMeasurands.currentItem()
		self.lineEdit_sensorName.setText(item.text(0))
		slope = self.lineEdit_slope.text()
		offset = self.lineEdit_offset.text()
		
	def popUp(self):
		print("nothing is there")
