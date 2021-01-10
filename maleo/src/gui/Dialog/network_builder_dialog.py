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
from maleo.lib.classification import *
from maleo.lib.module_data_type_param_check import ModuleDataTypeParamCheck
from maleo.src.utils.network_table_view import NetworkTableView


class NetworkBuilderDialog(QDialog):
    def __init__(self, parent, data):
        super(QDialog, self).__init__(parent)

        self.networkData = data

        self.activationFunctions = self.networkData["activations"]
        self.networkLayers = self.networkData["layers"]
        self.network = self.networkData["networks"]

        self.settings = None
        self.moduleDataTypeCheck = ModuleDataTypeParamCheck()

        self.layout = QHBoxLayout()
        self.networkLayout = QVBoxLayout()
        self.buttonLayout = QVBoxLayout()

        self.networkTable = NetworkTableView(self.network, self.networkLayers, self.activationFunctions,
                                             len(self.network), 3)
        self.networkTable.verticalHeader().setVisible(False)
        self.networkTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.networkTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.networkTable.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.networkTable.horizontalHeader().setStretchLastSection(True)

        self.addAboveButton = QPushButton("Add Above")
        self.addAboveButton.clicked.connect(self.add_above)
        self.addBelowButton = QPushButton("Add Below")
        self.addBelowButton.clicked.connect(self.add_below)
        self.deleteButton = QPushButton("Delete")
        self.deleteButton.clicked.connect(self.delete_item)
        self.okButton = QPushButton("Save Network")
        self.okButton.clicked.connect(self.on_ok)

        self.networkLayout.addWidget(self.networkTable)

        self.buttonLayout.addWidget(self.addAboveButton)
        self.buttonLayout.addWidget(self.addBelowButton)
        self.buttonLayout.addWidget(self.deleteButton)
        self.buttonLayout.addWidget(self.okButton)

        self.layout.addLayout(self.networkLayout, stretch=80)
        self.layout.addLayout(self.buttonLayout, stretch=20)

        self.setMinimumSize(600, 400)
        self.setWindowTitle("Neural Network Builder")
        self.setLayout(self.layout)

    def show(self):
        super(QDialog, self).show()

    def get_widget_values(self):
        return self.networkData["networks"]

    def get_values(self, widget):
        if isinstance(widget, QLineEdit):
            return widget.text()
        elif isinstance(widget, QSlider):
            return widget.value()
        elif isinstance(widget, QComboBox):
            return widget.currentText()

    def save_network(self):
        print("SAVING NEW NETWORK")
        new_networks = []

        for row in range(self.networkTable.rowCount()):
            new_layer = {}
            for col in range(self.networkTable.columnCount()):
                widget = self.networkTable.cellWidget(row, col)
                if widget is not None:
                    if col == 1:
                        new_layer["layer"] = self.get_values(widget)
                    if col == 2:
                        new_layer["activation"] = self.get_values(widget)
                    if col == 3:
                        new_layer["units"] = self.get_values(widget)
            new_networks.append(new_layer)

        self.networkData["networks"] = new_networks
        for index, network in enumerate(self.networkData["networks"]):
            self.networkData["networks"][index]["editable"] = True
        self.networkData["networks"][0]["editable"] = False
        self.networkData["networks"][len(self.networkData["networks"])-1]["editable"] = False

        self.networkTable.updateData(self.network, self.networkLayers, self.activationFunctions,
                                     len(self.network), 3)

    def add_network(self, row_index):
        new_layer =

        self.networkData["networks"] = new_networks
        for index, network in enumerate(self.networkData["networks"]):
            self.networkData["networks"][index]["editable"] = True
        self.networkData["networks"][0]["editable"] = False
        self.networkData["networks"][len(self.networkData["networks"])-1]["editable"] = False

        self.networkTable.updateData(self.network, self.networkLayers, self.activationFunctions,
                                     len(self.network), 3)

    def delete_item(self):
        try:
            items = self.networkTable.selectedItems()
            self.selectedRowIndex = int(items[0].text()) - 1
            if self.selectedRowIndex != 0 and self.selectedRowIndex != len(self.network) - 1:
                print("Able to add")
            else:
                self.parent().parent().dialog_critical("Cannot delete input or output layer")
        except Exception as e:
            self.parent().parent().dialog_critical("Error exception :\n" + str(e))

    def add_above(self):
        try:
            items = self.networkTable.selectedItems()
            self.selectedRowIndex = int(items[0].text()) - 1
            if self.selectedRowIndex != 0:
                print("Able to add")
            else:
                self.parent().parent().dialog_critical("Cannot add item above input layer")
        except Exception as e:
            self.parent().parent().dialog_critical("Error exception :\n" + str(e))

    def add_below(self):
        try:
            items = self.networkTable.selectedItems()
            self.selectedRowIndex = int(items[0].text()) - 1
            if self.selectedRowIndex != len(self.network) - 1:
                print("Able to add")
            else:
                self.parent().parent().dialog_critical("Cannot add item below output layer")
        except Exception as e:
            self.parent().parent().dialog_critical("Error exception :\n" + str(e))

    def on_ok(self):
        self.save_network()
        self.close()
