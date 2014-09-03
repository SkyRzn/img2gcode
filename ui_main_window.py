# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created: Mon Sep  1 17:55:26 2014
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(766, 613)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.scrollArea = QtGui.QScrollArea(self.centralwidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 498, 528))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.verticalLayout = QtGui.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.view = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.view.setText(_fromUtf8(""))
        self.view.setObjectName(_fromUtf8("view"))
        self.verticalLayout.addWidget(self.view)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_2.addWidget(self.scrollArea)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 766, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.dockWidget = QtGui.QDockWidget(MainWindow)
        self.dockWidget.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
        self.dockWidget.setObjectName(_fromUtf8("dockWidget"))
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.gridLayout = QtGui.QGridLayout(self.dockWidgetContents)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.groupBox = QtGui.QGroupBox(self.dockWidgetContents)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_2.addWidget(self.label_2, 2, 0, 1, 1)
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_2.addWidget(self.label_3, 3, 0, 1, 1)
        self.doubleSpinBox = QtGui.QDoubleSpinBox(self.groupBox)
        self.doubleSpinBox.setObjectName(_fromUtf8("doubleSpinBox"))
        self.gridLayout_2.addWidget(self.doubleSpinBox, 2, 1, 1, 1)
        self.doubleSpinBox_2 = QtGui.QDoubleSpinBox(self.groupBox)
        self.doubleSpinBox_2.setObjectName(_fromUtf8("doubleSpinBox_2"))
        self.gridLayout_2.addWidget(self.doubleSpinBox_2, 3, 1, 1, 1)
        self.radioButton = QtGui.QRadioButton(self.groupBox)
        self.radioButton.setObjectName(_fromUtf8("radioButton"))
        self.gridLayout_2.addWidget(self.radioButton, 0, 0, 1, 1)
        self.radioButton_2 = QtGui.QRadioButton(self.groupBox)
        self.radioButton_2.setChecked(True)
        self.radioButton_2.setObjectName(_fromUtf8("radioButton_2"))
        self.gridLayout_2.addWidget(self.radioButton_2, 1, 0, 1, 1)
        self.doubleSpinBox_3 = QtGui.QDoubleSpinBox(self.groupBox)
        self.doubleSpinBox_3.setObjectName(_fromUtf8("doubleSpinBox_3"))
        self.gridLayout_2.addWidget(self.doubleSpinBox_3, 4, 1, 1, 1)
        self.doubleSpinBox_4 = QtGui.QDoubleSpinBox(self.groupBox)
        self.doubleSpinBox_4.setObjectName(_fromUtf8("doubleSpinBox_4"))
        self.gridLayout_2.addWidget(self.doubleSpinBox_4, 5, 1, 1, 1)
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_2.addWidget(self.label, 4, 0, 1, 1)
        self.label_4 = QtGui.QLabel(self.groupBox)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_2.addWidget(self.label_4, 5, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 2)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 2)
        self.dockWidget.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockWidget)
        self.actionFileOpen = QtGui.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("resources/document-open.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionFileOpen.setIcon(icon)
        self.actionFileOpen.setObjectName(_fromUtf8("actionFileOpen"))
        self.menuFile.addAction(self.actionFileOpen)
        self.menubar.addAction(self.menuFile.menuAction())
        self.toolBar.addAction(self.actionFileOpen)
        self.label_2.setBuddy(self.doubleSpinBox)
        self.label_3.setBuddy(self.doubleSpinBox_2)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.radioButton_2, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.doubleSpinBox.setEnabled)
        QtCore.QObject.connect(self.radioButton_2, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.label_2.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar", None))
        self.dockWidget.setWindowTitle(_translate("MainWindow", "Options", None))
        self.groupBox.setTitle(_translate("MainWindow", "Pass", None))
        self.label_2.setText(_translate("MainWindow", "Pretensioning, mm:", None))
        self.label_3.setText(_translate("MainWindow", "Allow gap, mm:", None))
        self.radioButton.setText(_translate("MainWindow", "Bidirectional", None))
        self.radioButton_2.setText(_translate("MainWindow", "Unidirectional", None))
        self.label.setText(_translate("MainWindow", "On waiting, s:", None))
        self.label_4.setText(_translate("MainWindow", "Off waiting, s:", None))
        self.actionFileOpen.setText(_translate("MainWindow", "Open", None))
        self.actionFileOpen.setShortcut(_translate("MainWindow", "Ctrl+O", None))

