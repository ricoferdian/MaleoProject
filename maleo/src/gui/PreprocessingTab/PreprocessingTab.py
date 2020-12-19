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

PreprocessingTab
Copyright (C) 2020 Henrico Aldy Ferdian & Lennia Savitri Azzahra Loviana
Udayana University, Bali, Indonesia

This part of python program consist of the preprocessing tab from main GUI application
"""

# PyQt5 GUI Library
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# Python Library
import sys

# Third Party Library

# GUI part Library
from maleo.src.gui.PreprocessingTab.FileOperationWidget import FileOperationWidget
from maleo.src.gui.PreprocessingTab.DataAttributeWidget import DataAttributeWidget
from maleo.src.gui.PreprocessingTab.CurrentRelationWidget import CurrentRelationWidget
from maleo.src.gui.PreprocessingTab.SelectAttributeWidget import SelectAttributeWidget

# Data operation
from maleo.src.utils.CSVLoader import CSVLoader
from maleo.src.model.CSVDataModel import CSVDataModel

class PreprocessingTab(QWidget):
    # Untuk return datamodel CSV
    dataModelSignal = pyqtSignal(CSVDataModel)

    def __init__(self, parent, screenHeight, screenWidth):
        super(QWidget, self).__init__(parent)

        self.layout = QVBoxLayout(self)

        self.fileOperationWidget = FileOperationWidget(self)

        self.attributeLayout = QHBoxLayout()

        self.leftAttributeLayout = QVBoxLayout()
        self.currentRelationWidget = CurrentRelationWidget(self)
        self.dataAttributeWidget = DataAttributeWidget(self)
        self.leftAttributeLayout.addWidget(self.currentRelationWidget)
        self.leftAttributeLayout.addWidget(self.dataAttributeWidget)

        self.rightAttributeLayout = QVBoxLayout()
        self.selectAttributeWidget = SelectAttributeWidget(self)
        self.rightAttributeLayout.addWidget(self.selectAttributeWidget)

        self.attributeLayout.addLayout(self.leftAttributeLayout, stretch=50)
        self.attributeLayout.addLayout(self.rightAttributeLayout, stretch=50)

        self.layout.addWidget(self.fileOperationWidget, stretch=10)
        self.layout.addLayout(self.attributeLayout, stretch=90)
        self.setLayout(self.layout)

    def changeSelectedAttribute(self, items, data):
        self.selectAttributeWidget.updateWidget(items, data)

    def changeDataAttributeParent(self):
        return None

    def loadDataModel(self, filename):
        self.csvLoader = CSVLoader(filename)
        self.data = self.csvLoader.getData()

        self.dataModel = CSVDataModel(self.data)

        self.updateDataAttributeModel(self.dataModel)
        self.updateParentDataModel(self.dataModel)

    def notifyModelChange(self, dataModel):
        self.dataModel = dataModel
        self.updateDataAttributeModel(self.dataModel)
        self.updateParentDataModel(self.dataModel)

    def updateParentDataModel(self, dataModel):
        self.dataModelSignal.emit(dataModel)

    def updateDataAttributeModel(self, dataModel):
        self.dataAttributeWidget.loadData(dataModel)