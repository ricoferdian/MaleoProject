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

ClassificationTab
Copyright (C) 2020 Henrico Aldy Ferdian & Lennia Savitri Azzahra Loviana
Udayana University, Bali, Indonesia

This part of python program consist of the classification tab from main GUI application
"""

# PyQt5 GUI Library
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# Python Library

# Third Party Library

# GUI part Library
from maleo.src.gui.ClassificationTab.ClassifierWidget import ClassifierWidget
from maleo.src.gui.ClassificationTab.ClassifierOutputWidget import ClassifierOutputWidget
from maleo.src.gui.ClassificationTab.ResultListWidget import ResultListWidget
from maleo.src.gui.ClassificationTab.TestOptionWidget import TestOptionWidget
from maleo.src.gui.ClassificationTab.ModuleOperationWidget import ModuleOperationWidget
from maleo.src.utils.PandasDatatypeCheck import PandasDatatypeCheck

# Module
from maleo.src.model.ClassifierModel import ClassifierModel

class ClassificationTab(QWidget):
    def __init__(self, parent, dataModel, screenHeight, screenWidth):
        super(QWidget, self).__init__(parent)
        self.dataModel = dataModel
        self.module = None

        self.layout = QVBoxLayout(self)

        self.classifierWidget = ClassifierWidget(self)
        self.dataTypeCheck = PandasDatatypeCheck()

        self.testLayout = QHBoxLayout()

        self.leftTestLayout = QVBoxLayout()
        self.testOptionWidget = TestOptionWidget(self)
        self.moduleOperationWidget = ModuleOperationWidget(self, self.dataModel)
        self.resultListWidget = ResultListWidget(self)
        self.leftTestLayout.addWidget(self.testOptionWidget,stretch=40)
        self.leftTestLayout.addWidget(self.moduleOperationWidget, stretch=20)
        self.leftTestLayout.addWidget(self.resultListWidget,stretch=40)

        self.rightTestLayout = QVBoxLayout()
        self.classifierOutputWidget = ClassifierOutputWidget(self)
        self.rightTestLayout.addWidget(self.classifierOutputWidget)

        self.testLayout.addLayout(self.leftTestLayout, stretch=20)
        self.testLayout.addLayout(self.rightTestLayout, stretch=80)

        self.layout.addWidget(self.classifierWidget, stretch=10)
        self.layout.addLayout(self.testLayout, stretch=90)
        self.setLayout(self.layout)

    def loadData(self):
        self.data = self.dataModel.getData()

        self.attributes = self.data.iloc[:,:-1]
        self.labels = self.data.iloc[:,-1:]

        if not self.dataModel.isEmpty():
            self.moduleOperationWidget.setLabelDropDown()
            self.setClassifierData(self.attributes, self.labels)
        else:
            self.dialog_critical("No data received !")

    def setModuleObject(self, moduleObject):
        self.module = moduleObject("tes", "label")
        self.moduleSettings = self.module.getAvailableSettings()

        self.moduleSupportedOperation = self.module.getSupportedOperations()
        self.moduleUnsupportedOperation = self.module.getUnsupportedOperations()

        self.moduleOperationWidget.updateSupportedOperationType(self.moduleSupportedOperation,self.moduleUnsupportedOperation)
        self.classifierWidget.setModule(self.module)
        self.setClassifierData(self.attributes, self.labels)

    def setClassifierData(self, data, labels):
        if self.module:
            self.module.setData(data, labels)

    def getData(self):
        print("self.parent()",self.parent())

    def setData(self, index):
        self.attributes = self.data.drop(columns=self.data.columns[index], axis=1)
        self.setClassifierData(self.attributes, self.labels)

    def setLabel(self, index):
        self.labels = self.data.iloc[:, index]
        self.setData(index)

    def setClassifierModel(self):
        self.classifierModel = ClassifierModel(self.module)

    def startOperation(self):
        value, option =  self.testOptionWidget.getTestOption()

        try:
            value = float(value)

            self.module.setDatasetParam(value, option)
            self.module.setOutputWidget(self.classifierOutputWidget.getOutputWidget())

            self.setClassifierModel()

            self.classifierWidget.toggleClassifierWidget(False)
            self.testOptionWidget.toggleTestOptionWidget(False)
            self.resultListWidget.addClassifierResult(self.classifierModel)
            self.classifierOutputWidget.startListenOutput()

            print("Starting Operation")
            print(self.attributes)
            print(self.labels)

            self.classifierModel.start()
        except Exception as e:
            self.dialog_critical("Error !"+str(e))

    def showClassifierOutput(self, classifierIndex):
        self.classifierOutputWidget.showOutput(classifierIndex)

    def stopOperation(self):
        print("Stopping Operation")
        self.classifierModel.stop()
        self.classifierOutputWidget.stopListenOutput()
        self.testOptionWidget.toggleTestOptionWidget(True)
        self.classifierWidget.toggleClassifierWidget(True)

    def dialog_critical(self, message):
        dlg = QMessageBox(self)
        dlg.setText(message)
        dlg.setIcon(QMessageBox.Critical)
        dlg.show()

