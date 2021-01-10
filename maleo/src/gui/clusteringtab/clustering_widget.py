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
import importlib

# Third Party Library

# GUI part Library
from maleo.src.gui.dialog.select_clusterer_dialog import SelectClustererDialog
from maleo.src.gui.dialog.module_setting_dialog import ModuleSettingDialog
from maleo.src.gui.dialog.network_builder_dialog import NetworkBuilderDialog


class ClusteringWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QHBoxLayout(self)

        self.modulePath = "maleo.lib.clustering."
        self.moduleName = None

        self.classifierDialog = SelectClustererDialog(self)
        self.moduleSettingDialog = ModuleSettingDialog(self)

        self.classifierSelectGroup = QGroupBox("Clusterer")
        self.classifierSelectLayout = QHBoxLayout()
        self.classifierSelectGroup.setLayout(self.classifierSelectLayout)

        self.selectClassifierButton = QPushButton("Select Clusterer")
        self.selectedClassifier = QLineEdit()
        self.settingClassifierButton = QPushButton("Parameters")
        self.selectedClassifier.setReadOnly(True)

        self.selectClassifierButton.clicked.connect(self.select_classifier)
        self.settingClassifierButton.clicked.connect(self.classifier_settings)

        self.classifierSelectLayout.addWidget(self.selectClassifierButton)
        self.classifierSelectLayout.addWidget(self.selectedClassifier)
        self.classifierSelectLayout.addWidget(self.settingClassifierButton)

        self.layout.addWidget(self.classifierSelectGroup)
        self.setLayout(self.layout)

    def select_classifier(self):
        self.classifierDialog.show()

    def set_classifier(self, moduleName):
        self.moduleName = moduleName
        self.selectedClassifier.setText(self.moduleName)
        self.set_module_object(self.moduleName)

    def set_data_model(self, dataModel):
        self.dataModel = dataModel
        self.data = self.dataModel.get_data()

    def toggle_classifier_widget(self, toggle):
        self.selectClassifierButton.setEnabled(toggle)
        self.settingClassifierButton.setEnabled(toggle)

    def classifier_settings(self):
        if self.moduleName and self.moduleSettings:
            self.settings = {
                getattr(self.module, function): {
                    "params":{param: {"data": data, "value": None} for param, data in attr["params"].items()},
                    "name": attr["name"],
                }
                for function, attr in self.moduleSettings.items()
            }
            self.moduleSettingDialog.set_settings(self.settings)
            self.moduleSettingDialog.show()
        elif self.moduleName:
            self.parent().dialog_critical("No settings available !")
        else:
            self.parent().dialog_critical("No selected modules !")

    def set_module_object(self, moduleName):
        modulepath = importlib.import_module(self.modulePath + moduleName)
        classname = moduleName.split(".")[1]
        moduleObject = getattr(modulepath, classname)
        self.parent().set_module_object(moduleObject)

    def set_module(self, module):
        self.module = module
        self.moduleSettings = self.module.get_available_settings()

    def update_module_setting(self, setting):
        self.moduleSettingValue = setting
        for module, param in self.moduleSettingValue.items():
            self.call_module_function(module, param)

    def call_module_function(self, name, params):
        name(**params)

    def update_parent_data_model(self):
        self.parent().load_data_model(self.filePath)
