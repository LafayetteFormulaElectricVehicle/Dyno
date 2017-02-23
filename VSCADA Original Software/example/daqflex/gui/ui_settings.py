# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './gui/settings.ui'
#
# Created: Sat Apr 25 00:31:56 2015
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

class Ui_SettingsDialog(object):
    def setupUi(self, SettingsDialog):
        SettingsDialog.setObjectName(_fromUtf8("SettingsDialog"))
        SettingsDialog.resize(350, 175)
        self.verticalLayout = QtGui.QVBoxLayout(SettingsDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.hLayoutPollFreq = QtGui.QHBoxLayout()
        self.hLayoutPollFreq.setObjectName(_fromUtf8("hLayoutPollFreq"))
        self.labelPollFreq = QtGui.QLabel(SettingsDialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.labelPollFreq.setFont(font)
        self.labelPollFreq.setObjectName(_fromUtf8("labelPollFreq"))
        self.hLayoutPollFreq.addWidget(self.labelPollFreq)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hLayoutPollFreq.addItem(spacerItem)
        self.spinBoxFreq = QtGui.QDoubleSpinBox(SettingsDialog)
        self.spinBoxFreq.setDecimals(0)
        self.spinBoxFreq.setMinimum(1.0)
        self.spinBoxFreq.setMaximum(1000.0)
        self.spinBoxFreq.setProperty("value", 10.0)
        self.spinBoxFreq.setObjectName(_fromUtf8("spinBoxFreq"))
        self.hLayoutPollFreq.addWidget(self.spinBoxFreq)
        self.labelFreqUnits = QtGui.QLabel(SettingsDialog)
        self.labelFreqUnits.setObjectName(_fromUtf8("labelFreqUnits"))
        self.hLayoutPollFreq.addWidget(self.labelFreqUnits)
        self.verticalLayout.addLayout(self.hLayoutPollFreq)
        self.hlayoutUnits = QtGui.QHBoxLayout()
        self.hlayoutUnits.setObjectName(_fromUtf8("hlayoutUnits"))
        self.labelUnits = QtGui.QLabel(SettingsDialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.labelUnits.setFont(font)
        self.labelUnits.setObjectName(_fromUtf8("labelUnits"))
        self.hlayoutUnits.addWidget(self.labelUnits)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hlayoutUnits.addItem(spacerItem1)
        self.comboBoxUnits = QtGui.QComboBox(SettingsDialog)
        self.comboBoxUnits.setObjectName(_fromUtf8("comboBoxUnits"))
        self.hlayoutUnits.addWidget(self.comboBoxUnits)
        self.verticalLayout.addLayout(self.hlayoutUnits)
        self.labelOutputFreq = QtGui.QLabel(SettingsDialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.labelOutputFreq.setFont(font)
        self.labelOutputFreq.setObjectName(_fromUtf8("labelOutputFreq"))
        self.verticalLayout.addWidget(self.labelOutputFreq)
        self.hLayoutOutputFreq = QtGui.QHBoxLayout()
        self.hLayoutOutputFreq.setObjectName(_fromUtf8("hLayoutOutputFreq"))
        self.radioButtonChange = QtGui.QRadioButton(SettingsDialog)
        self.radioButtonChange.setChecked(True)
        self.radioButtonChange.setObjectName(_fromUtf8("radioButtonChange"))
        self.hLayoutOutputFreq.addWidget(self.radioButtonChange)
        self.radioButtonRegular = QtGui.QRadioButton(SettingsDialog)
        self.radioButtonRegular.setObjectName(_fromUtf8("radioButtonRegular"))
        self.hLayoutOutputFreq.addWidget(self.radioButtonRegular)
        self.verticalLayout.addLayout(self.hLayoutOutputFreq)
        spacerItem2 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.buttonBox = QtGui.QDialogButtonBox(SettingsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Save)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(SettingsDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), SettingsDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), SettingsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SettingsDialog)

    def retranslateUi(self, SettingsDialog):
        SettingsDialog.setWindowTitle(_translate("SettingsDialog", "Settings", None))
        self.labelPollFreq.setText(_translate("SettingsDialog", "Poll Frequency", None))
        self.labelFreqUnits.setText(_translate("SettingsDialog", "Hz", None))
        self.labelUnits.setText(_translate("SettingsDialog", "Units", None))
        self.labelOutputFreq.setText(_translate("SettingsDialog", "Output Update Frequency", None))
        self.radioButtonChange.setText(_translate("SettingsDialog", "On Value Change", None))
        self.radioButtonRegular.setText(_translate("SettingsDialog", "Regular Inteveral", None))

