import sys
import os

from PySide2 import QtCore, QtGui, QtWidgets

from maya import cmds
from maya import mel
from maya import OpenMayaUI as omui
from shiboken2 import wrapInstance

import wedgit

mayaMainWindowPtr = omui.MQtUtil.mainWindow()
mayaMainWindow = wrapInstance(long(mayaMainWindowPtr), QtWidgets.QWidget)

class WedgitWindow(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(WedgitWindow, self).__init__(*args, **kwargs)

        #Parent widget under Maya main window
        self.setParent(mayaMainWindow)
        self.setWindowFlags(QtCore.Qt.Window)

        #Set object name
        self.setObjectName('WdgWin')
        self.setWindowTitle('Make Wedge')
        self.setGeometry(50, 50, 250, 150)
        self.initUI()
        self.do_connections()

    def initUI(self):

        self.minmax_button = QtWidgets.QPushButton('Min Max', self)
        self.minmax_button.setFixedWidth(80)
        min_label = QtWidgets.QLabel('Minimum Value')
        self.min_value = QtWidgets.QDoubleSpinBox()
        self.min_value.setValue(0.50)
        self.min_value.setSingleStep(0.05)
        max_label = QtWidgets.QLabel('Maximum Value')
        self.max_value = QtWidgets.QDoubleSpinBox()
        self.max_value.setValue(1.50)
        self.max_value.setSingleStep(0.05)
        scale_label = QtWidgets.QLabel('Scale Factor')
        self.scale_factor = QtWidgets.QDoubleSpinBox()
        self.scale_factor.setValue(0.25)
        self.scale_factor.setSingleStep(0.05)
        self.scale_factor.setMinimum(0.05)
        
        minmax_layout = QtWidgets.QHBoxLayout()
        minmax_layout.addWidget(self.minmax_button)
        minmax_layout.addWidget(min_label)
        minmax_layout.addWidget(self.min_value)
        minmax_layout.addWidget(max_label)
        minmax_layout.addWidget(self.max_value)
        minmax_layout.addWidget(scale_label)
        minmax_layout.addWidget(self.scale_factor)
        
        self.startstep_button = QtWidgets.QPushButton('Start Step', self)
        self.startstep_button.setFixedWidth(80)
        start_label = QtWidgets.QLabel('Start Value')
        self.start_value = QtWidgets.QDoubleSpinBox()
        self.start_value.setValue(0.5)
        self.start_value.setSingleStep(0.1)
        step_label = QtWidgets.QLabel('Step Size')
        self.step_size = QtWidgets.QDoubleSpinBox()
        self.step_size.setValue(0.25)
        self.step_size.setSingleStep(0.1)
        count_label = QtWidgets.QLabel('Number of Steps')
        self.step_count = QtWidgets.QSpinBox()
        self.step_count.setValue(3)
        self.step_count.setSingleStep(1)
        self.step_count.setMinimum(0)
        
        startstep_layout = QtWidgets.QHBoxLayout()
        startstep_layout.addWidget(self.startstep_button)
        startstep_layout.addWidget(start_label)
        startstep_layout.addWidget(self.start_value)
        startstep_layout.addWidget(step_label)
        startstep_layout.addWidget(self.step_size)
        startstep_layout.addWidget(count_label)
        startstep_layout.addWidget(self.step_count)
        
        self.wedge_values = QtWidgets.QLineEdit(self)
        self.wedge_values.setFixedHeight(27)
        
        self.nodeattr_button = QtWidgets.QPushButton('Select Attribute', self)
        self.nodeattr_button.setFixedWidth(120)
        self.nodeattr_lineEdit = QtWidgets.QLineEdit()
        self.nodeattr_lineEdit.setFixedHeight(27)
        
        nodeattr_layout = QtWidgets.QHBoxLayout()
        nodeattr_layout.addWidget(self.nodeattr_button)
        nodeattr_layout.addWidget(self.nodeattr_lineEdit)
        
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(minmax_layout)
        main_layout.addLayout(startstep_layout)
        main_layout.addWidget(self.wedge_values)
        main_layout.addLayout(nodeattr_layout)
        self.setLayout(main_layout)


    def do_connections(self):
        self.minmax_button.clicked.connect(self.minmax_clicked)
        self.startstep_button.clicked.connect(self.startstep_clicked)


    def minmax_clicked(self):
        print("minmax clicked")
        #min_value = self.min_value.value()
        minmax_list = wedgit.wedge_minmax(self.min_value.value(), self.max_value.value(), self.scale_factor.value())
        self.wedge_values.setText(", ".join([str(num) for num in minmax_list]))


    def startstep_clicked(self):
        print("startstep clicked")
        startstep_list = wedgit.wedge_startstep(self.start_value.value(), self.step_size.value(), self.step_count.value())
        self.wedge_values.setText(", ".join([str(num) for num in startstep_list]))

