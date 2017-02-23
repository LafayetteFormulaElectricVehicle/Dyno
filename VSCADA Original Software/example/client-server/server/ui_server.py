# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'server.ui'
#
# Created: Wed Apr  1 16:52:14 2015
#      by: PyQt4 UI code generator 4.11.3
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

class Ui_ServerDemo(object):
    def setupUi(self, ServerDemo):
        ServerDemo.setObjectName(_fromUtf8("ServerDemo"))
        ServerDemo.resize(350, 172)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ServerDemo.sizePolicy().hasHeightForWidth())
        ServerDemo.setSizePolicy(sizePolicy)
        ServerDemo.setMinimumSize(QtCore.QSize(350, 172))
        ServerDemo.setMaximumSize(QtCore.QSize(16777215, 172))
        self.centralwidget = QtGui.QWidget(ServerDemo)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.hLayout1 = QtGui.QHBoxLayout()
        self.hLayout1.setObjectName(_fromUtf8("hLayout1"))
        self.label1 = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label1.setFont(font)
        self.label1.setObjectName(_fromUtf8("label1"))
        self.hLayout1.addWidget(self.label1)
        self.slider1 = QtGui.QSlider(self.centralwidget)
        self.slider1.setMaximum(99)
        self.slider1.setOrientation(QtCore.Qt.Horizontal)
        self.slider1.setObjectName(_fromUtf8("slider1"))
        self.hLayout1.addWidget(self.slider1)
        self.lcd1 = QtGui.QLCDNumber(self.centralwidget)
        self.lcd1.setMinimumSize(QtCore.QSize(0, 32))
        self.lcd1.setNumDigits(3)
        self.lcd1.setSegmentStyle(QtGui.QLCDNumber.Flat)
        self.lcd1.setObjectName(_fromUtf8("lcd1"))
        self.hLayout1.addWidget(self.lcd1)
        self.verticalLayout_2.addLayout(self.hLayout1)
        self.hLayout2 = QtGui.QHBoxLayout()
        self.hLayout2.setObjectName(_fromUtf8("hLayout2"))
        self.label2 = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label2.setFont(font)
        self.label2.setObjectName(_fromUtf8("label2"))
        self.hLayout2.addWidget(self.label2)
        self.slider2 = QtGui.QSlider(self.centralwidget)
        self.slider2.setMaximum(99)
        self.slider2.setOrientation(QtCore.Qt.Horizontal)
        self.slider2.setObjectName(_fromUtf8("slider2"))
        self.hLayout2.addWidget(self.slider2)
        self.lcd2 = QtGui.QLCDNumber(self.centralwidget)
        self.lcd2.setMinimumSize(QtCore.QSize(0, 32))
        self.lcd2.setNumDigits(3)
        self.lcd2.setSegmentStyle(QtGui.QLCDNumber.Flat)
        self.lcd2.setObjectName(_fromUtf8("lcd2"))
        self.hLayout2.addWidget(self.lcd2)
        self.verticalLayout_2.addLayout(self.hLayout2)
        self.hLayout3 = QtGui.QHBoxLayout()
        self.hLayout3.setObjectName(_fromUtf8("hLayout3"))
        self.label3 = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label3.setFont(font)
        self.label3.setObjectName(_fromUtf8("label3"))
        self.hLayout3.addWidget(self.label3)
        self.slider3 = QtGui.QSlider(self.centralwidget)
        self.slider3.setMaximum(99)
        self.slider3.setOrientation(QtCore.Qt.Horizontal)
        self.slider3.setObjectName(_fromUtf8("slider3"))
        self.hLayout3.addWidget(self.slider3)
        self.lcd3 = QtGui.QLCDNumber(self.centralwidget)
        self.lcd3.setMinimumSize(QtCore.QSize(0, 32))
        self.lcd3.setNumDigits(3)
        self.lcd3.setSegmentStyle(QtGui.QLCDNumber.Flat)
        self.lcd3.setObjectName(_fromUtf8("lcd3"))
        self.hLayout3.addWidget(self.lcd3)
        self.verticalLayout_2.addLayout(self.hLayout3)
        self.hLayout4 = QtGui.QHBoxLayout()
        self.hLayout4.setObjectName(_fromUtf8("hLayout4"))
        self.label4 = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label4.setFont(font)
        self.label4.setObjectName(_fromUtf8("label4"))
        self.hLayout4.addWidget(self.label4)
        self.slider4 = QtGui.QSlider(self.centralwidget)
        self.slider4.setMaximum(99)
        self.slider4.setOrientation(QtCore.Qt.Horizontal)
        self.slider4.setObjectName(_fromUtf8("slider4"))
        self.hLayout4.addWidget(self.slider4)
        self.lcd4 = QtGui.QLCDNumber(self.centralwidget)
        self.lcd4.setMinimumSize(QtCore.QSize(0, 32))
        self.lcd4.setNumDigits(3)
        self.lcd4.setSegmentStyle(QtGui.QLCDNumber.Flat)
        self.lcd4.setObjectName(_fromUtf8("lcd4"))
        self.hLayout4.addWidget(self.lcd4)
        self.verticalLayout_2.addLayout(self.hLayout4)
        ServerDemo.setCentralWidget(self.centralwidget)

        self.retranslateUi(ServerDemo)
        QtCore.QMetaObject.connectSlotsByName(ServerDemo)

    def retranslateUi(self, ServerDemo):
        ServerDemo.setWindowTitle(_translate("ServerDemo", "Server Demo", None))
        self.label1.setText(_translate("ServerDemo", "Sensor 1", None))
        self.label2.setText(_translate("ServerDemo", "Sensor 2", None))
        self.label3.setText(_translate("ServerDemo", "Sensor 3", None))
        self.label4.setText(_translate("ServerDemo", "Sensor 4", None))

