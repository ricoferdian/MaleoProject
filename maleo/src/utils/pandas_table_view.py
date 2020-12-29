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


class PandasTableView(QTableWidget):
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

    def deleteRow(self, row_index):
        self.removeRow(row_index)

    def appendRow(self, new_row):
        self.data = self.data.append(new_row, ignore_index=True)
        row_count = self.rowCount()
        self.setRowCount(row_count + 1)
        for i, data in enumerate(new_row.values()):
            data_item = QTableWidgetItem(str(data))
            self.setItem(row_count, i, data_item)

    def setItemData(self, row, col, value):
        data_item = QTableWidgetItem(str(value))
        self.setItem(row, col, data_item)

    def setData(self):
        horHeaders = []
        verHeaders = [str(i + 1) for i in range(self.columnCount() * self.rowCount())]
        for i, column in enumerate(self.data):
            horHeaders.append(column)
            for j, data in enumerate(self.data[column]):
                data_item = QTableWidgetItem(str(data))
                self.setItem(j, i, data_item)
        self.setHorizontalHeaderLabels(horHeaders)
        self.setVerticalHeaderLabels(verHeaders)
