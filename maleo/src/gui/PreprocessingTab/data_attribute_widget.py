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

DataAttributeWidget
Copyright (C) 2020 Henrico Aldy Ferdian & Lennia Savitri Azzahra Loviana
Udayana University, Bali, Indonesia

This part of python program consist of the fileoperation widget
in preprocessing tab from main GUI application
"""

# PyQt5 GUI Library
from PyQt5.QtWidgets import *

# Python Library

# Third Party Library


# GUI Table View Library
from maleo.src.utils.datasetloader.table_view import TableView


class DataAttributeWidget(QWidget):
    def __init__(self, parent, data_model):
        super(QWidget, self).__init__(parent)
        self.dataModel = data_model
        self.data = None
        self.header = None

        self.layout = QHBoxLayout(self)

        self.dataAttributeGroup = QGroupBox("Attributes")
        self.dataAttributeLayout = QVBoxLayout()
        self.dataAttributeGroup.setLayout(self.dataAttributeLayout)

        self.dataAttributeButtons = QHBoxLayout()

        self.btnSelectAllAttribute = QPushButton("Select All")
        self.btnSelectNoneAttribute = QPushButton("Select None")
        self.btnSelectInvertAttribute = QPushButton("Select Invert")

        self.btnSelectAllAttribute.clicked.connect(self.select_all)
        self.btnSelectNoneAttribute.clicked.connect(self.select_none)
        self.btnSelectInvertAttribute.clicked.connect(self.select_invert)

        self.dataAttributeButtons.addWidget(self.btnSelectAllAttribute)
        self.dataAttributeButtons.addWidget(self.btnSelectNoneAttribute)
        self.dataAttributeButtons.addWidget(self.btnSelectInvertAttribute)

        self.dataAttributeTable = TableView({}, 0, 0)
        self.dataAttributeTable.verticalHeader().setVisible(False)
        self.dataAttributeTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.dataAttributeTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.dataAttributeTable.itemSelectionChanged.connect(self.change_selected_attribute_parent)

        self.btnRemoveAttribute = QPushButton("Remove Attribute")
        self.btnRemoveAttribute.clicked.connect(self.remove_attribute)

        self.dataAttributeLayout.addLayout(self.dataAttributeButtons)
        self.dataAttributeLayout.addWidget(self.dataAttributeTable)
        self.dataAttributeLayout.addWidget(self.btnRemoveAttribute)

        self.layout.addWidget(self.dataAttributeGroup)
        self.setLayout(self.layout)

    def change_selected_attribute_parent(self):
        items = self.dataAttributeTable.selectedItems()
        self.parent().changeSelectedAttribute(items)

    def load_data(self):
        self.data = self.dataModel.getData()
        self.header = list(self.data.columns)

        if len(self.header):
            self.header = {"Name": {i: self.header[i] for i in range(len(self.header))}}
            first_key = next(iter(self.header.keys()))
            self.header[" No"] = {i: i+1 for i in range(len(self.header[first_key]))}
            self.header["."] = {i: QCheckBox() for i in range(len(self.header[first_key]))}

            self.draw_table(self.header, len(self.header[first_key]), len(self.header))
        else:
            self.draw_table({}, 0, 0)

    def draw_table(self, data, row, col):
        self.dataAttributeTable.updateParameter(col, row)
        self.dataAttributeTable.updateData(data)
        self.dataAttributeTable.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.dataAttributeTable.horizontalHeader().setStretchLastSection(True)

    def select_all(self):
        for row in range(self.dataAttributeTable.rowCount()):
            self.dataAttributeTable.cellWidget(row, 1).setChecked(True)

    def select_none(self):
        for row in range(self.dataAttributeTable.rowCount()):
            self.dataAttributeTable.cellWidget(row, 1).setChecked(False)

    def select_invert(self):
        for row in range(self.dataAttributeTable.rowCount()):
            item = self.dataAttributeTable.cellWidget(row, 1)
            if item.isChecked():
                item.setChecked(False)
            else:
                item.setChecked(True)

    def remove_attribute(self):
        indexes = []
        for row in range(self.dataAttributeTable.rowCount()):
            item = self.dataAttributeTable.cellWidget(row, 1)
            if item.isChecked():
                index = int(self.dataAttributeTable.item(row, 0).text())-1
                indexes.append(index)
        if len(list(self.data.columns)) == len(indexes):
            self.parent().dialog_critical("Cannot remove all attributes from data !")
        else:
            self.dataModel.removeColumn(indexes)
            self.parent().dataLoaded()
