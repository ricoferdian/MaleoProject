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
from maleo.src.model.clutering_model import ClusteringModel
from maleo.src.utils.datasetloader.pandas_datatype_check import PandasDatatypeCheck


class ClusteringTab(QWidget):
    def __init__(self, parent, dataModel, classifierResults, screenHeight, screenWidth):
        super(QWidget, self).__init__(parent)
        self.dataModel = dataModel
        self.module = None

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(0)

        self.classifierWidget = ClusteringWidget(self)
        self.dataTypeCheck = PandasDatatypeCheck()

        self.testLayout = QHBoxLayout()
        self.testLayout.setSpacing(0)

        self.leftTestLayout = QVBoxLayout()
        self.leftTestLayout.setSpacing(0)
        self.testOptionWidget = TestOptionWidget(self)
        self.moduleOperationWidget = ModuleOperationWidget(self, self.dataModel)
        self.resultListWidget = ResultListWidget(self)
        self.leftTestLayout.addWidget(self.testOptionWidget,stretch=40)
        self.leftTestLayout.addWidget(self.moduleOperationWidget, stretch=20)
        self.leftTestLayout.addWidget(self.resultListWidget,stretch=40)

        self.rightTestLayout = QVBoxLayout()
        self.rightTestLayout.setSpacing(0)
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
            self.moduleOperationWidget.set_label_drop_down()
            self.set_clusterer_data(self.attributes, self.labels)
        else:
            self.dialog_critical("Data is empty !")

    def set_module_object(self, moduleObject):
        self.module = moduleObject("tes", "label")
        self.moduleSettings = self.module.get_available_settings()

        self.moduleSupportedOperation = self.module.get_supported_operations()
        self.moduleUnsupportedOperation = self.module.get_supported_operations()

        self.moduleOperationWidget.update_supported_operation_type(self.moduleSupportedOperation, self.moduleUnsupportedOperation)
        self.classifierWidget.set_module(self.module)
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
        self.clusteringModel = ClusteringModel(self.module)

    def start_operation(self):
        value, option =  self.testOptionWidget.get_test_option()

        try:
            value = float(value)

            self.module.set_dataset_params(value, option)
            self.module.set_output_widget(self.classifierOutputWidget.get_output_widget())

            self.set_clusterer_model()

            self.classifierWidget.toggle_classifier_widget(False)
            self.testOptionWidget.toggle_test_option_widget(False)
            self.resultListWidget.add_classifier_result(self.clusteringModel)
            self.classifierOutputWidget.start_listen_output()

            print("Starting Operation")
            print(self.attributes)
            print(self.labels)

            self.clusteringModel.start()
        except Exception as e:
            self.dialog_critical("Error !"+str(e))

    def show_clusterer_output(self, classifierIndex):
        self.classifierOutputWidget.show_output(classifierIndex)

    def stop_operation(self):
        print("Stopping Operation")
        self.clusteringModel.stop()
        self.classifierOutputWidget.stop_listen_output()
        self.testOptionWidget.toggle_test_option_widget(True)
        self.classifierWidget.toggle_classifier_widget(True)

    def dialog_critical(self, message):
        dlg = QMessageBox(self)
        dlg.setText(message)
        dlg.setIcon(QMessageBox.Critical)
        dlg.show()
