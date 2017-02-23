# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './gui/callibration.ui'
#
# Created: Sat Apr 25 00:31:55 2015
#      by: PyQt4 UI code generator 4.11.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_CalibrationDialog(object):
    def setupUi(self, CalibrationDialog):
        CalibrationDialog.setObjectName(_fromUtf8("CalibrationDialog"))
        CalibrationDialog.resize(350, 400)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(CalibrationDialog.sizePolicy().hasHeightForWidth())
        CalibrationDialog.setSizePolicy(sizePolicy)
        CalibrationDialog.setMinimumSize(QtCore.QSize(350, 400))
        CalibrationDialog.setMaximumSize(QtCore.QSize(350, 400))
        self.verticalLayout = QtGui.QVBoxLayout(CalibrationDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.labelTachCal = QtGui.QLabel(CalibrationDialog)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.labelTachCal.setFont(font)
        self.labelTachCal.setObjectName(_fromUtf8("labelTachCal"))
        self.verticalLayout.addWidget(self.labelTachCal)
        self.hLayoutTachSlope = QtGui.QHBoxLayout()
        self.hLayoutTachSlope.setObjectName(_fromUtf8("hLayoutTachSlope"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.hLayoutTachSlope.addItem(spacerItem)
        self.labelTachSlope = QtGui.QLabel(CalibrationDialog)
        self.labelTachSlope.setObjectName(_fromUtf8("labelTachSlope"))
        self.hLayoutTachSlope.addWidget(self.labelTachSlope)
        self.lineEditTachSlope = QtGui.QLineEdit(CalibrationDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditTachSlope.sizePolicy().hasHeightForWidth())
        self.lineEditTachSlope.setSizePolicy(sizePolicy)
        self.lineEditTachSlope.setMinimumSize(QtCore.QSize(150, 0))
        self.lineEditTachSlope.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEditTachSlope.setObjectName(_fromUtf8("lineEditTachSlope"))
        self.hLayoutTachSlope.addWidget(self.lineEditTachSlope)
        self.verticalLayout.addLayout(self.hLayoutTachSlope)
        self.hLayoutTachOffset = QtGui.QHBoxLayout()
        self.hLayoutTachOffset.setObjectName(_fromUtf8("hLayoutTachOffset"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.hLayoutTachOffset.addItem(spacerItem1)
        self.labelTachOffset = QtGui.QLabel(CalibrationDialog)
        self.labelTachOffset.setObjectName(_fromUtf8("labelTachOffset"))
        self.hLayoutTachOffset.addWidget(self.labelTachOffset)
        self.lineEditTachOffset = QtGui.QLineEdit(CalibrationDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditTachOffset.sizePolicy().hasHeightForWidth())
        self.lineEditTachOffset.setSizePolicy(sizePolicy)
        self.lineEditTachOffset.setMinimumSize(QtCore.QSize(150, 0))
        self.lineEditTachOffset.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEditTachOffset.setObjectName(_fromUtf8("lineEditTachOffset"))
        self.hLayoutTachOffset.addWidget(self.lineEditTachOffset)
        self.verticalLayout.addLayout(self.hLayoutTachOffset)
        spacerItem2 = QtGui.QSpacerItem(20, 5, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem2)
        self.hLayoutTachLCD = QtGui.QHBoxLayout()
        self.hLayoutTachLCD.setObjectName(_fromUtf8("hLayoutTachLCD"))
        self.lcdNumberTachUnits = QtGui.QLCDNumber(CalibrationDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lcdNumberTachUnits.sizePolicy().hasHeightForWidth())
        self.lcdNumberTachUnits.setSizePolicy(sizePolicy)
        self.lcdNumberTachUnits.setMinimumSize(QtCore.QSize(100, 40))
        self.lcdNumberTachUnits.setStyleSheet(_fromUtf8("background-color: white;"))
        self.lcdNumberTachUnits.setSmallDecimalPoint(True)
        self.lcdNumberTachUnits.setNumDigits(5)
        self.lcdNumberTachUnits.setSegmentStyle(QtGui.QLCDNumber.Flat)
        self.lcdNumberTachUnits.setProperty("intValue", 0)
        self.lcdNumberTachUnits.setObjectName(_fromUtf8("lcdNumberTachUnits"))
        self.hLayoutTachLCD.addWidget(self.lcdNumberTachUnits)
        self.labelTachUnits = QtGui.QLabel(CalibrationDialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.labelTachUnits.setFont(font)
        self.labelTachUnits.setObjectName(_fromUtf8("labelTachUnits"))
        self.hLayoutTachLCD.addWidget(self.labelTachUnits)
        self.lcdNumberTachVolts = QtGui.QLCDNumber(CalibrationDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lcdNumberTachVolts.sizePolicy().hasHeightForWidth())
        self.lcdNumberTachVolts.setSizePolicy(sizePolicy)
        self.lcdNumberTachVolts.setMinimumSize(QtCore.QSize(100, 40))
        self.lcdNumberTachVolts.setStyleSheet(_fromUtf8("background-color: white;"))
        self.lcdNumberTachVolts.setSmallDecimalPoint(True)
        self.lcdNumberTachVolts.setNumDigits(5)
        self.lcdNumberTachVolts.setDigitCount(5)
        self.lcdNumberTachVolts.setSegmentStyle(QtGui.QLCDNumber.Flat)
        self.lcdNumberTachVolts.setProperty("value", 0.0)
        self.lcdNumberTachVolts.setProperty("intValue", 0)
        self.lcdNumberTachVolts.setObjectName(_fromUtf8("lcdNumberTachVolts"))
        self.hLayoutTachLCD.addWidget(self.lcdNumberTachVolts)
        self.labelTachVolts = QtGui.QLabel(CalibrationDialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.labelTachVolts.setFont(font)
        self.labelTachVolts.setObjectName(_fromUtf8("labelTachVolts"))
        self.hLayoutTachLCD.addWidget(self.labelTachVolts)
        self.verticalLayout.addLayout(self.hLayoutTachLCD)
        spacerItem3 = QtGui.QSpacerItem(20, 30, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem3)
        self.labelToqueCal = QtGui.QLabel(CalibrationDialog)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.labelToqueCal.setFont(font)
        self.labelToqueCal.setObjectName(_fromUtf8("labelToqueCal"))
        self.verticalLayout.addWidget(self.labelToqueCal)
        self.hLayoutTorqueSlope = QtGui.QHBoxLayout()
        self.hLayoutTorqueSlope.setObjectName(_fromUtf8("hLayoutTorqueSlope"))
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.hLayoutTorqueSlope.addItem(spacerItem4)
        self.labelTorqueSlope = QtGui.QLabel(CalibrationDialog)
        self.labelTorqueSlope.setObjectName(_fromUtf8("labelTorqueSlope"))
        self.hLayoutTorqueSlope.addWidget(self.labelTorqueSlope)
        self.lineEditTorqueSlope = QtGui.QLineEdit(CalibrationDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditTorqueSlope.sizePolicy().hasHeightForWidth())
        self.lineEditTorqueSlope.setSizePolicy(sizePolicy)
        self.lineEditTorqueSlope.setMinimumSize(QtCore.QSize(150, 0))
        self.lineEditTorqueSlope.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEditTorqueSlope.setObjectName(_fromUtf8("lineEditTorqueSlope"))
        self.hLayoutTorqueSlope.addWidget(self.lineEditTorqueSlope)
        self.verticalLayout.addLayout(self.hLayoutTorqueSlope)
        self.hLayoutTorqueOffset = QtGui.QHBoxLayout()
        self.hLayoutTorqueOffset.setObjectName(_fromUtf8("hLayoutTorqueOffset"))
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.hLayoutTorqueOffset.addItem(spacerItem5)
        self.labelTorqueOffset = QtGui.QLabel(CalibrationDialog)
        self.labelTorqueOffset.setObjectName(_fromUtf8("labelTorqueOffset"))
        self.hLayoutTorqueOffset.addWidget(self.labelTorqueOffset)
        self.lineEditTorqueOffset = QtGui.QLineEdit(CalibrationDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditTorqueOffset.sizePolicy().hasHeightForWidth())
        self.lineEditTorqueOffset.setSizePolicy(sizePolicy)
        self.lineEditTorqueOffset.setMinimumSize(QtCore.QSize(150, 0))
        self.lineEditTorqueOffset.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEditTorqueOffset.setObjectName(_fromUtf8("lineEditTorqueOffset"))
        self.hLayoutTorqueOffset.addWidget(self.lineEditTorqueOffset)
        self.verticalLayout.addLayout(self.hLayoutTorqueOffset)
        spacerItem6 = QtGui.QSpacerItem(20, 5, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem6)
        self.hLayouTorqueLCD = QtGui.QHBoxLayout()
        self.hLayouTorqueLCD.setObjectName(_fromUtf8("hLayouTorqueLCD"))
        self.lcdNumberTorqueUnits = QtGui.QLCDNumber(CalibrationDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lcdNumberTorqueUnits.sizePolicy().hasHeightForWidth())
        self.lcdNumberTorqueUnits.setSizePolicy(sizePolicy)
        self.lcdNumberTorqueUnits.setMinimumSize(QtCore.QSize(100, 40))
        self.lcdNumberTorqueUnits.setStyleSheet(_fromUtf8("background-color: white;"))
        self.lcdNumberTorqueUnits.setSmallDecimalPoint(True)
        self.lcdNumberTorqueUnits.setNumDigits(5)
        self.lcdNumberTorqueUnits.setDigitCount(5)
        self.lcdNumberTorqueUnits.setSegmentStyle(QtGui.QLCDNumber.Flat)
        self.lcdNumberTorqueUnits.setProperty("value", 0.0)
        self.lcdNumberTorqueUnits.setProperty("intValue", 0)
        self.lcdNumberTorqueUnits.setObjectName(_fromUtf8("lcdNumberTorqueUnits"))
        self.hLayouTorqueLCD.addWidget(self.lcdNumberTorqueUnits)
        self.labelTorqueUnits = QtGui.QLabel(CalibrationDialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.labelTorqueUnits.setFont(font)
        self.labelTorqueUnits.setObjectName(_fromUtf8("labelTorqueUnits"))
        self.hLayouTorqueLCD.addWidget(self.labelTorqueUnits)
        self.lcdNumberTorqueVolts = QtGui.QLCDNumber(CalibrationDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lcdNumberTorqueVolts.sizePolicy().hasHeightForWidth())
        self.lcdNumberTorqueVolts.setSizePolicy(sizePolicy)
        self.lcdNumberTorqueVolts.setMinimumSize(QtCore.QSize(100, 40))
        self.lcdNumberTorqueVolts.setStyleSheet(_fromUtf8("background-color: white;"))
        self.lcdNumberTorqueVolts.setSmallDecimalPoint(True)
        self.lcdNumberTorqueVolts.setNumDigits(5)
        self.lcdNumberTorqueVolts.setDigitCount(5)
        self.lcdNumberTorqueVolts.setSegmentStyle(QtGui.QLCDNumber.Flat)
        self.lcdNumberTorqueVolts.setProperty("value", 0.0)
        self.lcdNumberTorqueVolts.setProperty("intValue", 0)
        self.lcdNumberTorqueVolts.setObjectName(_fromUtf8("lcdNumberTorqueVolts"))
        self.hLayouTorqueLCD.addWidget(self.lcdNumberTorqueVolts)
        self.labelTorqueVolts = QtGui.QLabel(CalibrationDialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.labelTorqueVolts.setFont(font)
        self.labelTorqueVolts.setObjectName(_fromUtf8("labelTorqueVolts"))
        self.hLayouTorqueLCD.addWidget(self.labelTorqueVolts)
        self.verticalLayout.addLayout(self.hLayouTorqueLCD)
        spacerItem7 = QtGui.QSpacerItem(20, 25, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem7)
        self.buttonBox = QtGui.QDialogButtonBox(CalibrationDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Save)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(CalibrationDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), CalibrationDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), CalibrationDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(CalibrationDialog)

    def retranslateUi(self, CalibrationDialog):
        CalibrationDialog.setWindowTitle(_translate("CalibrationDialog", "Calibration Settings", None))
        self.labelTachCal.setText(_translate("CalibrationDialog", "Tachometer Calibration", None))
        self.labelTachSlope.setText(_translate("CalibrationDialog", "Slope", None))
        self.lineEditTachSlope.setText(_translate("CalibrationDialog", "1.0", None))
        self.labelTachOffset.setText(_translate("CalibrationDialog", "Offset", None))
        self.lineEditTachOffset.setText(_translate("CalibrationDialog", "0.0", None))
        self.labelTachUnits.setText(_translate("CalibrationDialog", "RPM", None))
        self.labelTachVolts.setText(_translate("CalibrationDialog", "ADC", None))
        self.labelToqueCal.setText(_translate("CalibrationDialog", "Torque Calibration", None))
        self.labelTorqueSlope.setText(_translate("CalibrationDialog", "Slope", None))
        self.lineEditTorqueSlope.setText(_translate("CalibrationDialog", "1.0", None))
        self.labelTorqueOffset.setText(_translate("CalibrationDialog", "Offset", None))
        self.lineEditTorqueOffset.setText(_translate("CalibrationDialog", "0.0", None))
        self.labelTorqueUnits.setText(_translate("CalibrationDialog", "N·m", None))
        self.labelTorqueVolts.setText(_translate("CalibrationDialog", "ADC", None))
