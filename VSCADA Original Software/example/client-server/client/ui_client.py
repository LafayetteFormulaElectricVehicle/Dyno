# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'client.ui'
#
# Created: Wed Mar 11 18:46:29 2015
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

class Ui_ClientDemo(object):
    def setupUi(self, ClientDemo):
        ClientDemo.setObjectName(_fromUtf8("ClientDemo"))
        ClientDemo.resize(172, 172)
        ClientDemo.setMinimumSize(QtCore.QSize(172, 172))
        ClientDemo.setMaximumSize(QtCore.QSize(16777215, 172))
        self.centralwidget = QtGui.QWidget(ClientDemo)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.hLayout1 = QtGui.QHBoxLayout()
        self.hLayout1.setObjectName(_fromUtf8("hLayout1"))
        self.label1 = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label1.setFont(font)
        self.label1.setObjectName(_fromUtf8("label1"))
        self.hLayout1.addWidget(self.label1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hLayout1.addItem(spacerItem)
        self.lcd1 = QtGui.QLCDNumber(self.centralwidget)
        self.lcd1.setMinimumSize(QtCore.QSize(0, 32))
        self.lcd1.setNumDigits(3)
        self.lcd1.setSegmentStyle(QtGui.QLCDNumber.Flat)
        self.lcd1.setObjectName(_fromUtf8("lcd1"))
        self.hLayout1.addWidget(self.lcd1)
        self.verticalLayout.addLayout(self.hLayout1)
        self.hLayout2 = QtGui.QHBoxLayout()
        self.hLayout2.setObjectName(_fromUtf8("hLayout2"))
        self.label2 = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label2.setFont(font)
        self.label2.setObjectName(_fromUtf8("label2"))
        self.hLayout2.addWidget(self.label2)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hLayout2.addItem(spacerItem1)
        self.lcd2 = QtGui.QLCDNumber(self.centralwidget)
        self.lcd2.setMinimumSize(QtCore.QSize(0, 32))
        self.lcd2.setNumDigits(3)
        self.lcd2.setSegmentStyle(QtGui.QLCDNumber.Flat)
        self.lcd2.setObjectName(_fromUtf8("lcd2"))
        self.hLayout2.addWidget(self.lcd2)
        self.verticalLayout.addLayout(self.hLayout2)
        self.hLayout3 = QtGui.QHBoxLayout()
        self.hLayout3.setObjectName(_fromUtf8("hLayout3"))
        self.label3 = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label3.setFont(font)
        self.label3.setObjectName(_fromUtf8("label3"))
        self.hLayout3.addWidget(self.label3)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hLayout3.addItem(spacerItem2)
        self.lcd3 = QtGui.QLCDNumber(self.centralwidget)
        self.lcd3.setMinimumSize(QtCore.QSize(0, 32))
        self.lcd3.setNumDigits(3)
        self.lcd3.setSegmentStyle(QtGui.QLCDNumber.Flat)
        self.lcd3.setObjectName(_fromUtf8("lcd3"))
        self.hLayout3.addWidget(self.lcd3)
        self.verticalLayout.addLayout(self.hLayout3)
        self.hLayout4 = QtGui.QHBoxLayout()
        self.hLayout4.setObjectName(_fromUtf8("hLayout4"))
        self.label4 = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label4.setFont(font)
        self.label4.setObjectName(_fromUtf8("label4"))
        self.hLayout4.addWidget(self.label4)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hLayout4.addItem(spacerItem3)
        self.lcd4 = QtGui.QLCDNumber(self.centralwidget)
        self.lcd4.setMinimumSize(QtCore.QSize(0, 32))
        self.lcd4.setNumDigits(3)
        self.lcd4.setSegmentStyle(QtGui.QLCDNumber.Flat)
        self.lcd4.setObjectName(_fromUtf8("lcd4"))
        self.hLayout4.addWidget(self.lcd4)
        self.verticalLayout.addLayout(self.hLayout4)
        ClientDemo.setCentralWidget(self.centralwidget)

        self.retranslateUi(ClientDemo)
        QtCore.QMetaObject.connectSlotsByName(ClientDemo)

    def retranslateUi(self, ClientDemo):
        ClientDemo.setWindowTitle(_translate("ClientDemo", "Client Demo", None))
        self.label1.setText(_translate("ClientDemo", "Sensor 1", None))
        self.label2.setText(_translate("ClientDemo", "Sensor 2", None))
        self.label3.setText(_translate("ClientDemo", "Sensor 3", None))
        self.label4.setText(_translate("ClientDemo", "Sensor 4", None))

