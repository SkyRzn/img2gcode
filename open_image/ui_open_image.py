# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'open_image.ui'
#
# Created: Tue Sep  2 16:04:52 2014
#      by: PyQt4 UI code generator 4.10.4
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
        Dialog.resize(748, 444)
        self.gridLayout_2 = QtGui.QGridLayout(Dialog)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_2.addWidget(self.buttonBox, 2, 1, 1, 1)
        self.optionsBox = QtGui.QGroupBox(Dialog)
        self.optionsBox.setObjectName(_fromUtf8("optionsBox"))
        self.gridLayout = QtGui.QGridLayout(self.optionsBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.thresholdLabel = QtGui.QLabel(self.optionsBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.thresholdLabel.sizePolicy().hasHeightForWidth())
        self.thresholdLabel.setSizePolicy(sizePolicy)
        self.thresholdLabel.setObjectName(_fromUtf8("thresholdLabel"))
        self.gridLayout.addWidget(self.thresholdLabel, 0, 0, 1, 1)
        self.thresholdSpinBox = QtGui.QSpinBox(self.optionsBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.thresholdSpinBox.sizePolicy().hasHeightForWidth())
        self.thresholdSpinBox.setSizePolicy(sizePolicy)
        self.thresholdSpinBox.setMaximum(255)
        self.thresholdSpinBox.setObjectName(_fromUtf8("thresholdSpinBox"))
        self.gridLayout.addWidget(self.thresholdSpinBox, 0, 2, 1, 1)
        self.thresholdSlider = QtGui.QSlider(self.optionsBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.thresholdSlider.sizePolicy().hasHeightForWidth())
        self.thresholdSlider.setSizePolicy(sizePolicy)
        self.thresholdSlider.setMaximum(255)
        self.thresholdSlider.setOrientation(QtCore.Qt.Horizontal)
        self.thresholdSlider.setObjectName(_fromUtf8("thresholdSlider"))
        self.gridLayout.addWidget(self.thresholdSlider, 0, 1, 1, 1)
        self.invertedCheckBox = QtGui.QCheckBox(self.optionsBox)
        self.invertedCheckBox.setObjectName(_fromUtf8("invertedCheckBox"))
        self.gridLayout.addWidget(self.invertedCheckBox, 1, 0, 1, 1)
        self.gridLayout_2.addWidget(self.optionsBox, 0, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 313, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 1, 1, 1, 1)
        self.progress = QtGui.QProgressBar(Dialog)
        self.progress.setMaximum(100000)
        self.progress.setProperty("value", 24)
        self.progress.setObjectName(_fromUtf8("progress"))
        self.gridLayout_2.addWidget(self.progress, 2, 0, 1, 1)
        self.scrollArea = QtGui.QScrollArea(Dialog)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setAlignment(QtCore.Qt.AlignCenter)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(1, 1, 345, 384))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.verticalLayout = QtGui.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.view = QtGui.QLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.view.sizePolicy().hasHeightForWidth())
        self.view.setSizePolicy(sizePolicy)
        self.view.setText(_fromUtf8(""))
        self.view.setScaledContents(True)
        self.view.setObjectName(_fromUtf8("view"))
        self.verticalLayout.addWidget(self.view)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.scrollArea, 0, 0, 2, 1)
        self.thresholdLabel.setBuddy(self.thresholdSlider)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QObject.connect(self.thresholdSlider, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.thresholdSpinBox.setValue)
        QtCore.QObject.connect(self.thresholdSpinBox, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.thresholdSlider.setValue)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.optionsBox.setTitle(_translate("Dialog", "Options", None))
        self.thresholdLabel.setText(_translate("Dialog", "Threshold:", None))
        self.invertedCheckBox.setText(_translate("Dialog", "Inverted", None))

