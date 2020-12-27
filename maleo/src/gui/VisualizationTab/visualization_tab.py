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


class VisualizationTab(QWidget):
    def __init__(self, parent, data_model, model_results, screen_height, screen_width):
        super(QWidget, self).__init__(parent)
        self.data = None
        self.dataModel = data_model

        self.layout = QGridLayout(self)

        self.widthWidget = 4

        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')

        self.visualizationWidgets = []

        self.setLayout(self.layout)

    def load_data(self):
        self.data = self.dataModel.getData()
        if not self.dataModel.isEmpty():
            try:
                self.plot()
            except Exception as e:
                self.dialog_critical("Error exception "+str(e))
        else:
            self.dialog_critical("No data received !")

    def plot(self):
        for widget in self.visualizationWidgets:
            self.layout.removeWidget(widget)
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

            bar = pg.BarGraphItem(x=x, height=y, width=0.1, brush='b', pen=pg.mkPen('b', width=0.1))

            plot.addItem(bar)
            plot.setTitle(column)
            # plot.setLabel('left', 'Value')
            # plot.setLabel('bottom', 'Range')

            self.visualizationWidgets.append(plot)
            self.layout.addWidget(plot, row, col)

            col += 1
            if col == 4:
                col = 0
                row += 1

    def dialog_critical(self, message):
        dlg = QMessageBox(self)
        dlg.setText(message)
        dlg.setIcon(QMessageBox.Critical)
        dlg.show()
