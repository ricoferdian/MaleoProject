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
from maleo.src.gui.dialog.network_builder_dialog import NetworkBuilderDialog

# Classifier Module Library
from maleo.lib.classification import *
from maleo.lib.module_data_type_param_check import ModuleDataTypeParamCheck


class ModuleSettingDialog(QDialog):
    def __init__(self, parent):
        super(QDialog, self).__init__(parent)

        self.layout = QVBoxLayout()

        self.settings = None
        self.moduleDataTypeCheck = ModuleDataTypeParamCheck()

        self.okButton = QPushButton("OK")
        self.okButton.clicked.connect(self.on_ok)

        self.setLayout(self.layout)

    def set_settings(self, settings):
        self.settings = settings

    def show(self):
        super(QDialog, self).show()
        self.draw_setting_widget()

    def draw_setting_widget(self):
        if self.settings:
            self.moduleDataType = self.moduleDataTypeCheck.getType()
            self.settingWidgets = []
            self.widgetTypeIndex = {}
            self.settingParam = {}
            try:
                cidx = 0
                for function, attrs in self.settings.items():
                    params = {}

                    setting_group = QGroupBox(attrs["name"])
                    setting_layout = QHBoxLayout()
                    setting_group.setLayout(setting_layout)
                    for param, setting in attrs["params"].items():
                        params[param] = {"value": None, "widgetindex": cidx}

                        self.moduleDataTypeCheck.setDataType(setting["data"]["type"])
                        data_type = self.moduleDataTypeCheck.getDataType()
                        setting_layout.addWidget(self.draw_widget(data_type, setting["data"], cidx))

                    self.settingWidgets.append(setting_group)
                    self.layout.addWidget(self.settingWidgets[cidx])

                    self.settingParam[function] = params
                    cidx += 1
                self.layout.addWidget(self.okButton)
            except Exception as e:
                self.close()
                self.parent().parent().dialog_critical("Error exception : \n" + str(e))
        else:
            self.close()
            self.parent().parent().dialog_critical("System error, settings not set !")

    def clear_setting_widget(self):
        self.layout.removeWidget(self.okButton)
        for setting_widget in self.settingWidgets:
            self.layout.removeWidget(setting_widget)
            setting_widget.deleteLater()
            setting_widget = None
        self.settingWidgets = []

    def draw_widget(self, data_type, data, cidx):
        if data_type == self.moduleDataType.NumericInput:
            self.widgetTypeIndex[cidx] = "NumericInput"
            return self.draw_input_widget(data_type, data)
        elif data_type == self.moduleDataType.TextInput:
            self.widgetTypeIndex[cidx] = "TextInput"
            return self.draw_input_widget(data_type, data)
        elif data_type == self.moduleDataType.NumericSlider:
            self.widgetTypeIndex[cidx] = "NumericSlider"
            return self.draw_slider_widget(data_type, data)
        elif data_type == self.moduleDataType.DropDown:
            self.widgetTypeIndex[cidx] = "DropDown"
            return self.draw_drop_down_widget(data_type, data)
        elif data_type == self.moduleDataType.BooleanDropDown:
            self.widgetTypeIndex[cidx] = "BooleanDropDown"
            return self.draw_boolean_drop_down_widget(data_type, data)
        elif data_type == self.moduleDataType.NetworkBuilder:
            self.widgetTypeIndex[cidx] = "NetworkBuilder"
            return self.draw_builder_button(data_type, data)
        else:
            return self.draw_input_widget(data_type, data)

    def draw_builder_button(self, data_type, data):
        network_builder_btn = QPushButton("Build")
        network_builder_btn.clicked.connect(self.build_network)
        self.networkBuilder = NetworkBuilderDialog(self, data)
        return network_builder_btn

    def build_network(self):
        print("GOING TO BUILD NN")
        self.networkBuilder.show()

    def get_built_network(self):
        print("GET BUILT NETWORKS")
        return self.networkBuilder.get_widget_values()

    def draw_input_widget(self, data_type, data):
        input_widget = QLineEdit()
        if data["default"]:
            input_widget.setText(str(data["default"]))
        return input_widget

    def draw_slider_widget(self, data_type, data):
        slider_widget = QSlider()
        slider_widget.setOrientation(Qt.Horizontal)
        slider_widget.setTickPosition(QSlider.TicksBelow)
        slider_widget.setTickInterval(1)
        try:
            slider_widget.setMinimum(data["min"])
            slider_widget.setMaximum(data["max"])
        except Exception as e:
            self.parent().parent().dialog_critical("No slider minimum and maximum value. Exception : " + str(e))
        return slider_widget

    def draw_drop_down_widget(self, data_type, data):
        combo_widget = QComboBox()
        options = data["options"]
        for option in options:
            combo_widget.addItem(option)
        return combo_widget

    def draw_boolean_drop_down_widget(self, data_type, data):
        combo_widget = QComboBox()
        combo_widget.addItem("True")
        combo_widget.addItem("False")
        return combo_widget

    def get_child_widget(self, parent):
        if isinstance(parent, QGroupBox) or isinstance(parent, QLayout):
            if parent.children():
                childwidgets = []
                for child in parent.children():
                    widget = self.get_child_widget(child)
                    if widget is not None:
                        childwidgets.append(widget)
                if len(childwidgets):
                    return childwidgets
        else:
            return parent

    def get_widget_values(self):
        widget_value = {}

        cidx = 0
        for settingWidget in self.settingWidgets:
            widgets = self.get_child_widget(settingWidget)
            if widgets:
                for widget in widgets:
                    print("widget",widget)
                    if self.widgetTypeIndex[cidx] == "NetworkBuilder":
                        widget_value[cidx] = self.get_built_network()
                    else:
                        widget_value[cidx] = self.get_values(widget)
                    cidx += 1
        try:
            for function, settingParam in self.settingParam.items():
                for params, widgetParam in settingParam.items():
                    value = widget_value[widgetParam["widgetindex"]]
                    self.settingParam[function][params] = value
            self.parent().update_module_setting(self.settingParam)
        except Exception as e:
            self.parent().parent().dialog_critical("Error exception : \n" + str(e))

    def get_values(self, widget):
        if isinstance(widget, QLineEdit):
            return widget.text()
        elif isinstance(widget, QSlider):
            return widget.value()
        elif isinstance(widget, QComboBox):
            return widget.currentText()

    def on_ok(self):
        self.get_widget_values()
        self.close()

    def closeEvent(self, event):
        self.clear_setting_widget()
