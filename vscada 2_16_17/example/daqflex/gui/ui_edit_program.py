# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './gui/edit_program.ui'
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

class Ui_ProgramEditDialog(object):
    def setupUi(self, ProgramEditDialog):
        ProgramEditDialog.setObjectName(_fromUtf8("ProgramEditDialog"))
        ProgramEditDialog.resize(400, 300)
        self.verticalLayout = QtGui.QVBoxLayout(ProgramEditDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.textEdit = QtGui.QTextEdit(ProgramEditDialog)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.verticalLayout.addWidget(self.textEdit)
        self.buttonBox = QtGui.QDialogButtonBox(ProgramEditDialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Help|QtGui.QDialogButtonBox.Save)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(ProgramEditDialog)
        QtCore.QMetaObject.connectSlotsByName(ProgramEditDialog)

    def retranslateUi(self, ProgramEditDialog):
        ProgramEditDialog.setWindowTitle(_translate("ProgramEditDialog", "Dialog", None))

