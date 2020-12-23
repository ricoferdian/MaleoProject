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

MainWindow
Copyright (C) 2020 Henrico Aldy Ferdian & Lennia Savitri Azzahra Loviana
Udayana University, Bali, Indonesia

This part of python program consist of the fileoperation widget
in preprocessing tab from main GUI application
"""

# PyQt5 GUI Library
from PyQt5.QtWidgets import *

# Python Library

# Third Party Library

from maleo.src.utils.DatasetLoader.PandasDatatypeCheck import PandasDatatypeCheck

class ModuleOperationWidget(QWidget):
    def __init__(self, parent, dataModel):
        super(QWidget, self).__init__(parent)
        self.dataModel = dataModel
        self.layout = QHBoxLayout(self)
        self.supported = []
        self.unsupported = []

        self.moduleOperationGroup = QGroupBox("Classification Operation")
        self.moduleOperationLayout = QVBoxLayout()
        self.moduleOperationGroup.setLayout(self.moduleOperationLayout)

        self.dataTypeCheck = PandasDatatypeCheck()

        self.selectLabelDropDown = QComboBox()
        self.selectLabelDropDown.currentIndexChanged.connect(self.labelSelectionChanged)

        self.buttonOperationLayout = QHBoxLayout()
        self.startOperationButton = QPushButton("Start")
        self.stopOperationButton = QPushButton("Stop")
        self.buttonOperationLayout.addWidget(self.startOperationButton)
        self.buttonOperationLayout.addWidget(self.stopOperationButton)

        self.startOperationButton.clicked.connect(self.startOperation)
        self.stopOperationButton.clicked.connect(self.stopOperation)

        self.moduleOperationLayout.addWidget(self.selectLabelDropDown)
        self.moduleOperationLayout.addLayout(self.buttonOperationLayout)

        self.startOperationButton.setEnabled(False)
        self.stopOperationButton.setEnabled(False)

        self.layout.addWidget(self.moduleOperationGroup)
        self.setLayout(self.layout)

    def startOperation(self):
        self.selectLabelDropDown.setEnabled(False)
        self.startOperationButton.setEnabled(False)
        self.stopOperationButton.setEnabled(True)
        self.parent().startOperation()

    def stopOperation(self):
        self.selectLabelDropDown.setEnabled(True)
        self.startOperationButton.setEnabled(True)
        self.stopOperationButton.setEnabled(False)
        self.parent().stopOperation()

    def updateSupportedOperationType(self, supported, unsupported):
        self.supported = supported
        self.unsupported = unsupported
        if self.selectLabelDropDown.currentIndex()<len(self.headerIndex) and self.selectLabelDropDown.currentIndex()>=0:
            self.labelSelectionChanged(self.selectLabelDropDown.currentIndex())

    def labelSelectionChanged(self, i):
        self.stopOperationButton.setEnabled(False)
        self.startOperationButton.setEnabled(False)
        if i >= 0 and i<len(self.headerIndex):
            if str(self.headerIndex[i]["dataType"]) in self.supported:
                self.startOperationButton.setEnabled(True)
                self.parent().setLabel(i)

    def setLabelDropDown(self):
        self.data = self.dataModel.getData()
        self.selectLabelDropDown.clear()
        self.headers = list(self.data.columns)
        self.headerIndex = {}
        for index in range(len(self.headers)):
            selectedData = self.data.iloc[:, index]
            self.dataTypeCheck.setDataType(selectedData)
            dataType = self.dataTypeCheck.getDataType()

            self.headerIndex[index] = {"name":self.headers[index],"dataType":dataType}

            self.selectLabelDropDown.addItem("("+str(dataType)+") "+self.headers[index])