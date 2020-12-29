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

class TableView(QTableWidget):
    def __init__(self, data, *args):
        QTableWidget.__init__(self, *args)
        self.data = data
        self.setData()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()

    def updateParameter(self, col, row):
        self.setColumnCount(col)
        self.setRowCount(row)

    def updateData(self, data):
        self.data = data
        self.setData()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()

    def setData(self):
        horHeaders = []
        for n, key in enumerate(sorted(self.data.keys())):
            horHeaders.append(key)
            for m, item in enumerate(self.data[key]):
                item_val = self.data[key][item]
                if(isinstance(item_val, QWidget)):
                    newitem = item_val
                    self.setCellWidget(m, n, newitem)
                else:
                    newitem = QTableWidgetItem(str(item_val))
                    self.setItem(m, n, newitem)
        self.setHorizontalHeaderLabels(horHeaders)

    # def get_data(self):
    #     data = []
    #     for row in range(self.rowCount()):
    #         data.append([])
    #         for column in range(self.columnCount()):
    #             index = self.index(row, column)
    #             # We suppose data are strings
    #             data[row].append(str(self.data(index).toString()))
    #     return data
