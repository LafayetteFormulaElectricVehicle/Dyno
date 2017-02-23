# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './gui/program.ui'
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

class Ui_ProgramDialog(object):
    def setupUi(self, ProgramDialog):
        ProgramDialog.setObjectName(_fromUtf8("ProgramDialog"))
        ProgramDialog.resize(455, 364)
        self.verticalLayout_4 = QtGui.QVBoxLayout(ProgramDialog)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.labelProgramList = QtGui.QLabel(ProgramDialog)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.labelProgramList.setFont(font)
        self.labelProgramList.setObjectName(_fromUtf8("labelProgramList"))
        self.verticalLayout_4.addWidget(self.labelProgramList)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.vLayoutProgramList = QtGui.QVBoxLayout()
        self.vLayoutProgramList.setObjectName(_fromUtf8("vLayoutProgramList"))
        self.listWidget = QtGui.QListWidget(ProgramDialog)
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        item = QtGui.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtGui.QListWidgetItem()
        self.listWidget.addItem(item)
        self.vLayoutProgramList.addWidget(self.listWidget)
        self.horizontalLayout_2.addLayout(self.vLayoutProgramList)
        self.vLayoutButtons = QtGui.QVBoxLayout()
        self.vLayoutButtons.setSpacing(5)
        self.vLayoutButtons.setMargin(10)
        self.vLayoutButtons.setObjectName(_fromUtf8("vLayoutButtons"))
        self.buttonDelete = QtGui.QPushButton(ProgramDialog)
        self.buttonDelete.setObjectName(_fromUtf8("buttonDelete"))
        self.vLayoutButtons.addWidget(self.buttonDelete)
        self.buttonRename = QtGui.QPushButton(ProgramDialog)
        self.buttonRename.setObjectName(_fromUtf8("buttonRename"))
        self.vLayoutButtons.addWidget(self.buttonRename)
        self.buttonEdit = QtGui.QPushButton(ProgramDialog)
        self.buttonEdit.setObjectName(_fromUtf8("buttonEdit"))
        self.vLayoutButtons.addWidget(self.buttonEdit)
        spacerItem = QtGui.QSpacerItem(120, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.vLayoutButtons.addItem(spacerItem)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vLayoutButtons.addItem(spacerItem1)
        self.buttonRun = QtGui.QPushButton(ProgramDialog)
        self.buttonRun.setObjectName(_fromUtf8("buttonRun"))
        self.vLayoutButtons.addWidget(self.buttonRun)
        self.horizontalLayout_2.addLayout(self.vLayoutButtons)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.buttonBox = QtGui.QDialogButtonBox(ProgramDialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout_4.addWidget(self.buttonBox)

        self.retranslateUi(ProgramDialog)
        QtCore.QMetaObject.connectSlotsByName(ProgramDialog)

    def retranslateUi(self, ProgramDialog):
        ProgramDialog.setWindowTitle(_translate("ProgramDialog", "Dialog", None))
        self.labelProgramList.setText(_translate("ProgramDialog", "Program List", None))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        item = self.listWidget.item(0)
        item.setText(_translate("ProgramDialog", "Program 1", None))
        item = self.listWidget.item(1)
        item.setText(_translate("ProgramDialog", "Program 2", None))
        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.buttonDelete.setText(_translate("ProgramDialog", "Delete", None))
        self.buttonRename.setText(_translate("ProgramDialog", "Rename", None))
        self.buttonEdit.setText(_translate("ProgramDialog", "Edit...", None))
        self.buttonRun.setText(_translate("ProgramDialog", "Run", None))

