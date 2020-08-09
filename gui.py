# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AutoClicker(object):
    def setupUi(self, AutoClicker):
        AutoClicker.setObjectName("AutoClicker")
        AutoClicker.setEnabled(True)
        AutoClicker.resize(383, 136)
        self.centralwidget = QtWidgets.QWidget(AutoClicker)
        self.centralwidget.setObjectName("centralwidget")
        self.ToggleButton = QtWidgets.QPushButton(self.centralwidget)
        self.ToggleButton.setGeometry(QtCore.QRect(10, 10, 111, 101))
        self.ToggleButton.setObjectName("ToggleButton")
        self.PressText = QtWidgets.QLineEdit(self.centralwidget)
        self.PressText.setGeometry(QtCore.QRect(130, 40, 113, 20))
        self.PressText.setObjectName("PressText")
        self.TriggerText = QtWidgets.QLineEdit(self.centralwidget)
        self.TriggerText.setGeometry(QtCore.QRect(260, 40, 113, 20))
        self.TriggerText.setObjectName("TriggerText")
        self.LeftClick = QtWidgets.QCheckBox(self.centralwidget)
        self.LeftClick.setEnabled(True)
        self.LeftClick.setGeometry(QtCore.QRect(130, 60, 81, 21))
        self.LeftClick.setChecked(True)
        self.LeftClick.setObjectName("LeftClick")
        self.RightClick = QtWidgets.QCheckBox(self.centralwidget)
        self.RightClick.setEnabled(True)
        self.RightClick.setGeometry(QtCore.QRect(130, 80, 81, 16))
        self.RightClick.setChecked(False)
        self.RightClick.setObjectName("RightClick")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(140, 20, 47, 13))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(260, 20, 61, 16))
        self.label_2.setObjectName("label_2")
        AutoClicker.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(AutoClicker)
        self.statusbar.setObjectName("statusbar")
        AutoClicker.setStatusBar(self.statusbar)

        self.retranslateUi(AutoClicker)
        QtCore.QMetaObject.connectSlotsByName(AutoClicker)

    def retranslateUi(self, AutoClicker):
        _translate = QtCore.QCoreApplication.translate
        AutoClicker.setWindowTitle(_translate("AutoClicker", "AutoClicker"))
        self.ToggleButton.setText(_translate("AutoClicker", "Toggle"))
        self.PressText.setText(_translate("AutoClicker", "space"))
        self.TriggerText.setText(_translate("AutoClicker", "ctrl+shift"))
        self.LeftClick.setText(_translate("AutoClicker", "Left Click"))
        self.RightClick.setText(_translate("AutoClicker", "Right Click"))
        self.label.setText(_translate("AutoClicker", "Output"))
        self.label_2.setText(_translate("AutoClicker", "Toggle Key"))
