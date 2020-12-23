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
import os

# Third Party Library

# GUI part Library
from maleo.src.gui.PreprocessingTab.FileOperationWidget import FileOperationWidget
from maleo.src.gui.PreprocessingTab.DataAttributeWidget import DataAttributeWidget
from maleo.src.gui.PreprocessingTab.CurrentRelationWidget import CurrentRelationWidget
from maleo.src.gui.PreprocessingTab.SelectAttributeWidget import SelectAttributeWidget

class PreprocessingTab(QWidget):
    dataLoadedSignal = pyqtSignal()
    def __init__(self, parent, dataModel, screenHeight, screenWidth):
        super(QWidget, self).__init__(parent)
        self.dataModel = dataModel

        self.layout = QVBoxLayout(self)

        self.fileOperationWidget = FileOperationWidget(self, self.dataModel)
        self.attributeLayout = QHBoxLayout()
        self.leftAttributeLayout = QVBoxLayout()

        self.currentRelationWidget = CurrentRelationWidget(self, self.dataModel)
        self.dataAttributeWidget = DataAttributeWidget(self, self.dataModel)
        self.leftAttributeLayout.addWidget(self.currentRelationWidget)
        self.leftAttributeLayout.addWidget(self.dataAttributeWidget)

        self.rightAttributeLayout = QVBoxLayout()
        self.selectAttributeWidget = SelectAttributeWidget(self, self.dataModel)
        self.rightAttributeLayout.addWidget(self.selectAttributeWidget)

        self.attributeLayout.addLayout(self.leftAttributeLayout, stretch=50)
        self.attributeLayout.addLayout(self.rightAttributeLayout, stretch=50)

        self.layout.addWidget(self.fileOperationWidget, stretch=10)
        self.layout.addLayout(self.attributeLayout, stretch=90)

        self.setLayout(self.layout)

    def loadData(self):
        self.currentRelationWidget.loadData()
        self.dataAttributeWidget.loadData()
        self.selectAttributeWidget.loadData()

    def dataLoaded(self):
        self.dataLoadedSignal.emit()
        self.currentRelationWidget.loadData()
        self.dataAttributeWidget.loadData()
        self.selectAttributeWidget.loadData()

    def changeSelectedAttribute(self, items):
        self.selectAttributeWidget.updateWidget(items)

    def dialog_critical(self, message):
        dlg = QMessageBox(self)
        dlg.setText(message)
        dlg.setIcon(QMessageBox.Critical)
        dlg.show()