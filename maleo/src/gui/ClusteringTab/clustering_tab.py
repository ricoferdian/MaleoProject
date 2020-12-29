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

This part of python program consist of the clustering tab from main GUI application
"""

# PyQt5 GUI Library
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# Python Library
import sys

# Third Party Library

# GUI part Library
from maleo.src.gui.clusteringtab.clustering_widget import ClusteringWidget
from maleo.src.gui.clusteringtab.clustering_output_widget import ClusteringOutputWidget
from maleo.src.gui.clusteringtab.result_list_widget import ResultListWidget
from maleo.src.gui.clusteringtab.test_option_widget import TestOptionWidget
from maleo.src.gui.clusteringtab.module_operation_widget import ModuleOperationWidget
from maleo.src.utils.datasetloader.pandas_datatype_check import PandasDatatypeCheck


class ClusteringTab(QWidget):
    def __init__(self, parent, dataModel, classifierResults, screenHeight, screenWidth):
        super(QWidget, self).__init__(parent)
        self.dataModel = dataModel
        self.module = None

        self.layout = QVBoxLayout(self)

        self.classifierWidget = ClusteringWidget(self)
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
        self.classifierOutputWidget = ClusteringOutputWidget(self)
        self.rightTestLayout.addWidget(self.classifierOutputWidget)

        self.testLayout.addLayout(self.leftTestLayout, stretch=20)
        self.testLayout.addLayout(self.rightTestLayout, stretch=80)

        self.layout.addWidget(self.classifierWidget, stretch=10)
        self.layout.addLayout(self.testLayout, stretch=90)
        self.setLayout(self.layout)

    def load_data(self):
        self.data = self.dataModel.get_data()

        self.attributes = self.data.iloc[:,:-1]
        self.labels = self.data.iloc[:,-1:]

        if not self.dataModel.is_empty():
            self.moduleOperationWidget.setLabelDropDown()
            self.set_clusterer_data(self.attributes, self.labels)
        else:
            self.dialog_critical("No data received !")

    def set_module_object(self, moduleObject):
        self.module = moduleObject("tes", "label")
        self.moduleSettings = self.module.getAvailableSettings()

        self.moduleSupportedOperation = self.module.getSupportedOperations()
        self.moduleUnsupportedOperation = self.module.getUnsupportedOperations()

        self.moduleOperationWidget.updateSupportedOperationType(self.moduleSupportedOperation,self.moduleUnsupportedOperation)
        self.classifierWidget.setModule(self.module)
        self.set_clusterer_data(self.attributes, self.labels)

    def set_clusterer_data(self, data, labels):
        if self.module:
            self.module.set_data(data, labels)

    def get_data(self):
        print("self.parent()",self.parent())

    def set_data(self, index):
        self.attributes = self.data.drop(columns=self.data.columns[index], axis=1)
        self.set_clusterer_data(self.attributes, self.labels)

    def set_label(self, index):
        self.labels = self.data.iloc[:, index]
        self.set_data(index)

    def set_clusterer_model(self):
        print("Set Model")
        # self.classifierModel = ClassifierModel(self.module)

    def start_operation(self):
        value, option =  self.testOptionWidget.getTestOption()

        try:
            value = float(value)

            self.module.setDatasetParam(value, option)
            self.module.setOutputWidget(self.classifierOutputWidget.getOutputWidget())

            self.set_clusterer_model()

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

    def show_clusterer_output(self, classifierIndex):
        self.classifierOutputWidget.showOutput(classifierIndex)

    def stop_operation(self):
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
