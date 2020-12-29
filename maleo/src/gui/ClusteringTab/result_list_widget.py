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

# GUI part Library
from maleo.src.gui.dialog.plot_model_result_dialog import PlotModelResultDialog

class ResultListWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QHBoxLayout(self)

        self.resultListGroup = QGroupBox("Result List")
        self.resultListLayout = QVBoxLayout()
        self.resultListGroup.setLayout(self.resultListLayout)

        self.classifierModel = []
        self.plotModelResultDialog = PlotModelResultDialog(self)

        self.resultList = QListWidget()
        self.resultList.itemSelectionChanged.connect(self.resultChoiceChanged)

        self.resultButtonLayout = QHBoxLayout()
        self.saveModelButton = QPushButton("Save Model")
        # self.loadModelButton = QPushButton("Load Model")
        self.resultButtonLayout.addWidget(self.saveModelButton)
        # self.resultButtonLayout.addWidget(self.loadModelButton)

        self.saveModelButton.clicked.connect(self.saveModel)
        # self.loadModelButton.clicked.connect(self.loadModel)

        self.plotModelResultButton = QPushButton("Plot Model Result")
        self.plotModelResultButton.clicked.connect(self.plotModelResult)

        self.resultListLayout.addWidget(self.resultList)
        self.resultListLayout.addLayout(self.resultButtonLayout)
        self.resultListLayout.addWidget(self.plotModelResultButton)

        self.layout.addWidget(self.resultListGroup)
        self.setLayout(self.layout)

    def resultChoiceChanged(self):
        try:
            self.selectedItem = self.resultList.selectedIndexes()[0]
            self.parent().showClassifierOutput(self.selectedItem.row())
        except Exception as e:
            self.parent().dialog_critical("No choice !"+str(e))

    def plotModelResult(self):
        try:
            if self.selectedItem.row() is not None:
                model = self.classifierModel[self.selectedItem.row()]
                self.plotModelResultDialog.set_history(model.get_history())
                self.plotModelResultDialog.show()
            else:
                self.parent().dialog_critical("No model selected !")
        except Exception as e:
            self.parent().dialog_critical("No model result ! Error : "+str(e))

    def saveModel(self):
        try:
            if self.selectedItem.row() is not None:
                path, _ = QFileDialog.getSaveFileName(self, "Save file", "", "HDF 5 (*.h5)")

                if not path:
                    return
                model = self.classifierModel[self.selectedItem.row()]
                model.save_to_path(path)
            else:
                self.parent().dialog_critical("Cannot save nothing !")
        except Exception as e:
            self.parent().dialog_critical("No model result ! Error : "+str(e))

    def loadModel(self):
        try:
            path, _ = QFileDialog.getOpenFileName(self, "Open file", "", "HDF 5 (*.h5);")
            if path:
                self.parent().loadModel(path)
        except Exception as e:
            self.parent().dialog_critical("No choice !"+str(e))

    def addClassifierResult(self, classifier):
        classifierName = classifier.get_name()
        self.classifierModel.append(classifier)
        self.resultList.addItem(classifierName)

    def openFile(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open file", "", "Dataset (*.csv *.json *.xls *.xlsx)")
        if path:
            self.filePath = path
            self.updateParentDataModel()

    def updateParentDataModel(self):
        self.parent().loadDataModel(self.filePath)