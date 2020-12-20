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
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# Python Library
import sys

# Third Party Library

class ResultListWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QHBoxLayout(self)

        self.resultListGroup = QGroupBox("Result List")
        self.resultListLayout = QVBoxLayout()
        self.resultListGroup.setLayout(self.resultListLayout)

        self.classifierModel = []

        self.resultList = QListWidget()
        self.resultList.itemSelectionChanged.connect(self.resultChoiceChanged)

        # self.showResultButton = QPushButton("Show Output")
        # self.showResultButton.clicked.connect(self.showOutput)

        self.resultListLayout.addWidget(self.resultList)
        # self.resultListLayout.addWidget(self.showResultButton)

        self.layout.addWidget(self.resultListGroup)
        self.setLayout(self.layout)

    def resultChoiceChanged(self):
        try:
            selectedItem = self.resultList.selectedIndexes()[0]
            self.parent().showClassifierOutput(selectedItem.row())
        except Exception as e:
            self.parent().dialog_critical("No choice !"+str(e))

    def showOutput(self):
        print("Showing output")

    def addClassifierResult(self, classifier):
        classifierName = classifier.getName()
        self.classifierModel.append(classifier)
        self.resultList.addItem(classifierName)

    def openFile(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open file", "", "Dataset (*.csv *.json *.xls *.xlsx)")
        if path:
            self.filePath = path
            self.updateParentDataModel()

    def updateParentDataModel(self):
        self.parent().loadDataModel(self.filePath)