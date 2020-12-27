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
from maleo.src.gui.dialog.select_classifier_dialog import SelectClassifierDialog
from maleo.src.gui.dialog.module_setting_dialog import ModuleSettingDialog


class ClassifierWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QHBoxLayout(self)

        self.modulePath = "maleo.lib.classification."
        self.moduleName = None

        self.classifierDialog = SelectClassifierDialog(self)
        self.moduleSettingDialog = ModuleSettingDialog(self)

        self.classifierSelectGroup = QGroupBox("Classifier")
        self.classifierSelectLayout = QHBoxLayout()
        self.classifierSelectGroup.setLayout(self.classifierSelectLayout)

        self.selectClassifierButton = QPushButton("Select Classifier")
        self.selectedClassifier = QLineEdit()
        self.settingClassifierButton = QPushButton("Parameters")
        self.selectedClassifier.setReadOnly(True)

        self.selectClassifierButton.clicked.connect(self.selectClassifier)
        self.settingClassifierButton.clicked.connect(self.classifierSettings)

        self.classifierSelectLayout.addWidget(self.selectClassifierButton)
        self.classifierSelectLayout.addWidget(self.selectedClassifier)
        self.classifierSelectLayout.addWidget(self.settingClassifierButton)

        self.layout.addWidget(self.classifierSelectGroup)
        self.setLayout(self.layout)

    def selectClassifier(self):
        self.classifierDialog.show()

    def setClassifier(self, moduleName):
        self.moduleName = moduleName
        self.selectedClassifier.setText(self.moduleName)
        self.setModuleObject(self.moduleName)

    def setDataModel(self, dataModel):
        self.dataModel = dataModel
        self.data = self.dataModel.getData()

    def toggleClassifierWidget(self, toggle):
        self.selectClassifierButton.setEnabled(toggle)
        self.settingClassifierButton.setEnabled(toggle)

    def classifierSettings(self):
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

    def setModuleObject(self, moduleName):
        modulepath = importlib.import_module(self.modulePath + moduleName)
        classname = moduleName.split(".")[1]
        moduleObject = getattr(modulepath, classname)
        self.parent().setModuleObject(moduleObject)

    def setModule(self, module):
        self.module = module
        self.moduleSettings = self.module.getAvailableSettings()

    def updateModuleSetting(self, setting):
        self.moduleSettingValue = setting
        for module, param in self.moduleSettingValue.items():
            self.callModuleFunction(module, param)

    def callModuleFunction(self, name, params):
        name(**params)

    def updateParentDataModel(self):
        self.parent().loadDataModel(self.filePath)
