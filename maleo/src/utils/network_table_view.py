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

This part of python program consist of the visualization tab from main GUI application
"""

# PyQt5 GUI Library
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# Python Library
import sys


# Third Party Library

class NetworkTableView(QTableWidget):
    def __init__(self, data, layers, activations, row, col, *args):
        QTableWidget.__init__(self, *args)
        self.data = data
        self.availLayers = layers
        self.availActivation = activations
        self.setColumnCount(col + 1)
        self.setRowCount(row)
        self.setData()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()

    def updateParameter(self, col, row):
        self.setColumnCount(col + 1)
        self.setRowCount(row)

    def updateData(self, data, layers, activations, row, col):
        self.data = data
        self.availLayers = layers
        self.availActivation = activations
        self.setColumnCount(col + 1)
        self.setRowCount(row)
        self.setData()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()

    def setData(self):
        self.editableIndex = []
        networkLayerIndex = 0
        activationFuncIndex = 0
        horHeaders = ["No", "Layer", "Activation", "Units"]
        for i, network in enumerate(self.data):
            self.setItem(i, 0, QTableWidgetItem(str(i + 1)))

            layerWidget = QComboBox()
            for j, layer in enumerate(self.availLayers):
                layerWidget.addItem(layer)
                if network["layer"] == layer:
                    networkLayerIndex = j

            layerWidget.setCurrentIndex(networkLayerIndex)
            self.setCellWidget(i, 1, layerWidget)

            activationWidget = QComboBox()
            for j, activation in enumerate(self.availActivation):
                activationWidget.addItem(activation)
                if network["activation"] == activation:
                    activationFuncIndex = j

            activationWidget.setCurrentIndex(activationFuncIndex)
            self.setCellWidget(i, 2, activationWidget)

            unitsCount = QLineEdit()
            if network["units"] != "auto" and network["units"] is not None:
                unitsCount.setText(str(network["units"]))
            self.setCellWidget(i, 3, unitsCount)

            if network["editable"] is not True:
                layerWidget.setEnabled(False)
                activationWidget.setEnabled(False)
                unitsCount.setEnabled(False)
        print("horHeaders", horHeaders)
        self.setHorizontalHeaderLabels(horHeaders)
