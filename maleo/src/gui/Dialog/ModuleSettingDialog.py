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
import json
import os.path as path

# Third Party Library

# Classifier Module Library
from maleo.lib.Classification import *
from maleo.lib.ModuleDataTypeParamCheck import ModuleDataTypeParamCheck

class ModuleSettingDialog(QDialog):
    def __init__(self, parent):
        super(QDialog, self).__init__(parent)

        self.layout = QVBoxLayout()

        self.settings = None
        self.moduleDataTypeCheck = ModuleDataTypeParamCheck()

        self.btnJalankan = QPushButton("OK")
        self.btnJalankan.clicked.connect(self.OnOk)

        self.setLayout(self.layout)

    def setSettings(self, settings):
        self.settings = settings

    def show(self):
        super(QDialog, self).show()
        self.drawSettingWidget()

    def drawSettingWidget(self):
        if self.settings:
            self.moduleDataType = self.moduleDataTypeCheck.getType()
            self.settingWidgets = []
            self.settingParam = {}
            try:
                cidx = 0
                for function, attrs in self.settings.items():
                    params = {}

                    settingGroup = QGroupBox(attrs["name"])
                    settingLayout = QHBoxLayout()
                    settingGroup.setLayout(settingLayout)
                    for param, setting in attrs["params"].items():
                        params[param] = {"value":None,"widgetindex":cidx}

                        self.moduleDataTypeCheck.setDataType(setting["data"]["type"])
                        dataType = self.moduleDataTypeCheck.getDataType()
                        settingLayout.addWidget(self.drawWidget(dataType, setting["data"]))
                    self.settingWidgets.append(settingGroup)
                    self.layout.addWidget(self.settingWidgets[cidx])

                    self.settingParam[function] = params
                    cidx += 1
                self.layout.addWidget(self.btnJalankan)
            except Exception as e:
                self.close()
                self.parent().parent().dialog_critical("Error !\n"+str(e))
        else:
            self.close()
            self.parent().parent().dialog_critical("System error, settings not set !")

    def clearSettingWidget(self):
        self.layout.removeWidget(self.btnJalankan)
        for settingWidget in self.settingWidgets:
            self.layout.removeWidget(settingWidget)
            settingWidget.deleteLater()
            settingWidget = None
        self.settingWidgets = []

    def drawWidget(self, dataType, data):
        if dataType==self.moduleDataType.NumericInput:
            return self.drawInputWidget(dataType, data)
        elif dataType==self.moduleDataType.TextInput:
            return self.drawInputWidget(dataType, data)
        elif dataType==self.moduleDataType.NumericSlider:
            return self.drawSliderWidget(dataType, data)
        elif dataType==self.moduleDataType.DropDown:
            return self.drawDropDownWidget(dataType, data)
        elif dataType==self.moduleDataType.BooleanDropDown:
            return self.drawBooleanDropDownWidget(dataType, data)
        else:
            return self.drawInputWidget(dataType, data)

    def drawInputWidget(self, dataType, data):
        input = QLineEdit()
        if data["default"]:
            input.setText(str(data["default"]))
        return input

    def drawSliderWidget(self, dataType, data):
        slider = QSlider()
        slider.setOrientation(Qt.Horizontal)
        slider.setTickPosition(QSlider.TicksBelow)
        try:
            slider.setTickInterval(1)
            slider.setMinimum(data["min"])
            slider.setMaximum(data["max"])
        except Exception as e:
            self.parent().parent().dialog_critical("No slider minimum and maximum value !")
        return slider

    def drawDropDownWidget(self, dataType, data):
        combo = QComboBox()
        options = data["options"]
        for option in options:
            combo.addItem(option)
        return combo

    def drawBooleanDropDownWidget(self, dataType, data):
        combo = QComboBox()
        combo.addItem("True")
        combo.addItem("False")
        return combo

    def getChildWidget(self, parent):
        if isinstance(parent, QGroupBox) or isinstance(parent,QLayout):
            if parent.children():
                childwidgets = []
                for child in parent.children():
                    widget = self.getChildWidget(child)
                    if widget is not None:
                        childwidgets.append(widget)
                if len(childwidgets):
                    return childwidgets
        else:
            return parent

    def getWidgetValues(self):
        widgetValue = {}

        cidx = 0
        for settingWidget in self.settingWidgets:
            widgets = self.getChildWidget(settingWidget)
            if widgets:
                for widget in widgets:
                    widgetValue[cidx] = self.getValues(widget)
                    cidx += 1
        try:
            for function, settingParam in self.settingParam.items():
                for params, widgetParam in settingParam.items():
                    value = widgetValue[widgetParam["widgetindex"]]
                    self.settingParam[function][params] = value
            self.parent().updateModuleSetting(self.settingParam)
        except Exception as e:
            self.parent().parent().dialog_critical("Error exception !\n",e)

    def getValues(self, widget):
        if isinstance(widget, QLineEdit):
            return widget.text()
        elif isinstance(widget, QSlider):
            return widget.value()
        elif isinstance(widget, QComboBox):
            return widget.currentText()

    def OnOk(self):
        self.getWidgetValues()
        self.close()

    def closeEvent(self, event):
        self.clearSettingWidget()