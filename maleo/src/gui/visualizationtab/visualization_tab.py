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
import pyqtgraph as pg

# Third Party Library
import numpy as np

from maleo.src.utils.datasetloader.pandas_datatype_check import PandasDatatypeCheck


class VisualizationTab(QWidget):
    def __init__(self, parent, data_model, model_results, screen_height, screen_width):
        super(QWidget, self).__init__(parent)
        self.data = None
        self.dataModel = data_model

        self.dataTypeCheck = PandasDatatypeCheck()

        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)

        self.actionLayout = QHBoxLayout()
        self.actionLayout.setSpacing(0)

        self.selectLabelDropDown = QComboBox()
        self.selectLabelDropDown.currentIndexChanged.connect(self.labelSelectionChanged)
        self.actionLayout.addWidget(self.selectLabelDropDown)

        self.graphLayout = QGridLayout(self)
        self.graphLayout.setSpacing(0)

        self.widthWidget = 4

        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')

        self.visualizationWidgets = []

        self.layout.addLayout(self.actionLayout)
        self.layout.addLayout(self.graphLayout)

        self.setLayout(self.layout)

    def set_label_drop_down(self):
        self.selectLabelDropDown.clear()
        self.headers = list(self.data.columns)
        for index in range(len(self.headers)):
            label_data = self.data.iloc[:, index]
            self.dataTypeCheck.setDataType(label_data)
            dataType = self.dataTypeCheck.getDataType()

            self.selectLabelDropDown.addItem("("+str(dataType)+") "+self.headers[index])

    def labelSelectionChanged(self, i):
        self.labels = self.data.iloc[:, i]

    def load_data(self):
        self.data = self.dataModel.get_data()
        if not self.dataModel.is_empty():
            try:
                self.set_label_drop_down()
                self.plot()
            except Exception as e:
                self.dialog_critical("Error exception "+str(e))
        else:
            self.dialog_critical("Data is empty !")

    def plot(self):
        for widget in self.visualizationWidgets:
            self.graphLayout.removeWidget(widget)
            widget.deleteLater()
            widget = None
        self.visualizationWidgets = []

        row = 0
        col = 0
        for column in self.data:
            plot = pg.PlotWidget()

            value = self.data[column].value_counts()
            x = [i for i in value.keys()]
            y = [j for i, j in value.items()]
            if np.array(x).dtype.char == 'U':
                x = [i for i in range(len(x))]

            bar = pg.BarGraphItem(x=x, height=y, width=0.1, brush='b', pen=pg.mkPen('b', width=1))

            plot.addItem(bar)
            plot.setTitle(column)
            # plot.set_label('left', 'Value')
            # plot.set_label('bottom', 'Range')

            self.visualizationWidgets.append(plot)
            self.graphLayout.addWidget(plot, row, col)

            col += 1
            if col == 4:
                col = 0
                row += 1

    def dialog_critical(self, message):
        dlg = QMessageBox(self)
        dlg.setText(message)
        dlg.setIcon(QMessageBox.Critical)
        dlg.show()
