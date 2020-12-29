"""
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

Copyright (C) 2020 Henrico Aldy Ferdian & Lennia Savitri Azzahra Loviana
Udayana University, Bali, Indonesia

This part of python program consist of the fileoperation widget
in preprocessing tab from main GUI application
"""

# PyQt5 GUI Library
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# Python Library
import sys

# Third Party Library


class TestOptionWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QHBoxLayout(self)
        self.testOption = 1

        self.testOptionGroup = QGroupBox("Test Options")
        self.testOptionLayout = QHBoxLayout()
        self.testOptionGroup.setLayout(self.testOptionLayout)

        self.leftTestLayout = QVBoxLayout()

        self.useTrainSetRadioButton = QRadioButton("Use Training Set")
        self.useTrainSetRadioButton.toggle()
        # self.useSuppliedSetRadioButton = QRadioButton("Supplied Dataset")
        # self.useCrossValRadioButton = QRadioButton("Cross Validation")
        self.usePercentageSplitRadioButton = QRadioButton("Percentage Split")
        self.leftTestLayout.addWidget(self.useTrainSetRadioButton)
        # self.leftTestLayout.addWidget(self.useSuppliedSetRadioButton)
        # self.leftTestLayout.addWidget(self.useCrossValRadioButton)
        self.leftTestLayout.addWidget(self.usePercentageSplitRadioButton)

        self.useTrainSetRadioButton.toggled.connect(self.toggleTrainSet)
        # self.useSuppliedSetRadioButton.toggled.connect(self.toggleSuppliedSet)
        # self.useCrossValRadioButton.toggled.connect(self.toggleCrossVal)
        self.usePercentageSplitRadioButton.toggled.connect(self.togglePercentageSplit)

        self.rightTestLayout = QVBoxLayout()

        self.fillerWidget = QPushButton("Already Set")
        self.fillerWidget.setEnabled(False)
        # self.useSuppliedSetButton = QPushButton("Set")
        # self.useSuppliedSetButton.setEnabled(False)
        # self.useCrossValInput = QLineEdit("10")
        # self.useCrossValInput.setEnabled(False)
        self.usePercentageInput = QLineEdit("80")
        self.usePercentageInput.setEnabled(False)
        self.rightTestLayout.addWidget(self.fillerWidget)
        # self.rightTestLayout.addWidget(self.useSuppliedSetButton)
        # self.rightTestLayout.addWidget(self.useCrossValInput)
        self.rightTestLayout.addWidget(self.usePercentageInput)

        self.testOptionLayout.addLayout(self.leftTestLayout)
        self.testOptionLayout.addLayout(self.rightTestLayout)

        self.layout.addWidget(self.testOptionGroup)
        self.setLayout(self.layout)

    def getTestOption(self):
        if self.useTrainSetRadioButton.isChecked():
            self.testValue = 0
            self.testOption = 1
        # elif self.useSuppliedSetRadioButton.isChecked():
        #     if self.filePath:
        #         self.testValue = self.filePath
        #         self.testOption = 2
        #     else:
        #         self.parent().parent().dialog_critical("No file selected !")
        # elif self.useCrossValRadioButton.isChecked():
        #     self.testValue = int(self.useCrossValInput.text())
        #     self.testOption = 3
        elif self.usePercentageSplitRadioButton.isChecked():
            self.testValue = self.usePercentageInput.text()
            self.testOption = 4

        return self.testValue, self.testOption

    def openSuppliedDataset(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open file", "", "Comma Separated Value (*.csv);"+
                                              ";Javascript Object Notation (*.json);"+
                                              ";Excel 2003-2007 Document (*.xls);"+
                                              ";Excel Document (*.xlsx)")
        if path:
            self.filePath = path

    def toggleTestForm(self,enabled):
        # self.useSuppliedSetButton.setEnabled(False)
        # self.useCrossValInput.setEnabled(False)
        self.usePercentageInput.setEnabled(False)
        if enabled:
            enabled.setEnabled(True)

    def toggleTrainSet(self):
        if self.useTrainSetRadioButton.isChecked():
            self.toggleTestForm(None)
            print("useTrainSetRadioButton")

    def toggleTestOptionWidget(self, toggle):
        self.useTrainSetRadioButton.setEnabled(toggle)
        # self.useSuppliedSetRadioButton.setEnabled(toggle)
        # self.useCrossValRadioButton.setEnabled(toggle)
        self.usePercentageSplitRadioButton.setEnabled(toggle)

    # def toggleSuppliedSet(self):
    #     if self.useSuppliedSetRadioButton.isChecked():
    #         self.toggleTestForm(self.useSuppliedSetButton)
    #         print("useSuppliedSetRadioButton")
    #
    # def toggleCrossVal(self):
    #     if self.useCrossValRadioButton.isChecked():
    #         self.toggleTestForm(self.useCrossValInput)
    #         print("useCrossValRadioButton")

    def togglePercentageSplit(self):
        if self.usePercentageSplitRadioButton.isChecked():
            self.toggleTestForm(self.usePercentageInput)
            print("usePercentageSplitRadioButton")
