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

from maleo.src.utils.datasetloader.pandas_datatype_check import PandasDatatypeCheck

class ModuleOperationWidget(QWidget):
    def __init__(self, parent, dataModel):
        super(QWidget, self).__init__(parent)
        self.dataModel = dataModel
        self.layout = QHBoxLayout(self)
        self.supported = []
        self.unsupported = []

        self.moduleOperationGroup = QGroupBox("Clustering Operation")
        self.moduleOperationLayout = QVBoxLayout()
        self.moduleOperationGroup.setLayout(self.moduleOperationLayout)

        self.dataTypeCheck = PandasDatatypeCheck()

        self.selectLabelDropDown = QComboBox()
        self.selectLabelDropDown.currentIndexChanged.connect(self.label_selection_changed)

        self.buttonOperationLayout = QHBoxLayout()
        self.startOperationButton = QPushButton("Start")
        self.stopOperationButton = QPushButton("Stop")
        self.buttonOperationLayout.addWidget(self.startOperationButton)
        self.buttonOperationLayout.addWidget(self.stopOperationButton)

        self.startOperationButton.clicked.connect(self.start_operation)
        self.stopOperationButton.clicked.connect(self.stop_operation)

        self.moduleOperationLayout.addWidget(self.selectLabelDropDown)
        self.moduleOperationLayout.addLayout(self.buttonOperationLayout)

        self.startOperationButton.setEnabled(False)
        self.stopOperationButton.setEnabled(False)

        self.layout.addWidget(self.moduleOperationGroup)
        self.setLayout(self.layout)

    def start_operation(self):
        self.selectLabelDropDown.setEnabled(False)
        self.startOperationButton.setEnabled(False)
        self.stopOperationButton.setEnabled(True)
        self.parent().start_operation()

    def stop_operation(self):
        self.selectLabelDropDown.setEnabled(True)
        self.startOperationButton.setEnabled(True)
        self.stopOperationButton.setEnabled(False)
        self.parent().stop_operation()

    def update_supported_operation_type(self, supported, unsupported):
        self.supported = supported
        self.unsupported = unsupported
        if self.selectLabelDropDown.currentIndex()<len(self.headerIndex) and self.selectLabelDropDown.currentIndex()>=0:
            self.label_selection_changed(self.selectLabelDropDown.currentIndex())

    def label_selection_changed(self, i):
        self.stopOperationButton.setEnabled(False)
        self.startOperationButton.setEnabled(False)
        if i >= 0 and i<len(self.headerIndex):
            if str(self.headerIndex[i]["data_type"]) in self.supported:
                self.startOperationButton.setEnabled(True)
                self.parent().set_label(i)

    def set_label_drop_down(self):
        self.data = self.dataModel.get_data()
        self.selectLabelDropDown.clear()
        self.headers = list(self.data.columns)
        self.headerIndex = {}
        for index in range(len(self.headers)):
            selectedData = self.data.iloc[:, index]
            self.dataTypeCheck.setDataType(selectedData)
            dataType = self.dataTypeCheck.getDataType()

            self.headerIndex[index] = {"name":self.headers[index],"data_type":dataType}

            self.selectLabelDropDown.addItem("("+str(dataType)+") "+self.headers[index])