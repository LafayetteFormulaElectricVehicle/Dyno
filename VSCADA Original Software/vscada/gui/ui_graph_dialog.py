# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './src/graph-dialog.ui'
#
# Created by: PyQt4 UI code generator 4.11.1
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(486, 351)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/general/img/lafayette.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.verticalLayout_3 = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.graphicsView = PlotWidget(Dialog)
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        self.verticalLayout_3.addWidget(self.graphicsView)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Graph", None))

from pyqtgraph import PlotWidget
import icon_rc
