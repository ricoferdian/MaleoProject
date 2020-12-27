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

preprocessingtab
Copyright (C) 2020 Henrico Aldy Ferdian & Lennia Savitri Azzahra Loviana
Udayana University, Bali, Indonesia

This part of python program consist of the preprocessing tab from main GUI application
"""

# PyQt5 GUI Library
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# Python Library
import os

# Third Party Library

# GUI part Library
from maleo.src.gui.preprocessingtab.file_operation_widget import FileOperationWidget
from maleo.src.gui.preprocessingtab.data_attribute_widget import DataAttributeWidget
from maleo.src.gui.preprocessingtab.current_relation_widget import CurrentRelationWidget
from maleo.src.gui.preprocessingtab.select_attribute_widget import SelectAttributeWidget


class PreprocessingTab(QWidget):
    dataLoadedSignal = pyqtSignal()

    def __init__(self, parent, data_model, screen_height, screen_width):
        super(QWidget, self).__init__(parent)
        self.dataModel = data_model

        self.layout = QVBoxLayout(self)

        self.fileOperationWidget = FileOperationWidget(self, self.dataModel)
        self.attributeLayout = QHBoxLayout()
        self.leftAttributeLayout = QVBoxLayout()

        self.currentRelationWidget = CurrentRelationWidget(self, self.dataModel)
        self.dataAttributeWidget = DataAttributeWidget(self, self.dataModel)
        self.leftAttributeLayout.addWidget(self.currentRelationWidget)
        self.leftAttributeLayout.addWidget(self.dataAttributeWidget)

        self.rightAttributeLayout = QVBoxLayout()
        self.selectAttributeWidget = SelectAttributeWidget(self, self.dataModel)
        self.rightAttributeLayout.addWidget(self.selectAttributeWidget)

        self.attributeLayout.addLayout(self.leftAttributeLayout, stretch=50)
        self.attributeLayout.addLayout(self.rightAttributeLayout, stretch=50)

        self.layout.addWidget(self.fileOperationWidget, stretch=10)
        self.layout.addLayout(self.attributeLayout, stretch=90)

        self.setLayout(self.layout)

    def load_data(self):
        self.currentRelationWidget.load_data()
        self.dataAttributeWidget.load_data()
        self.selectAttributeWidget.load_data()

    def data_loaded(self):
        self.dataLoadedSignal.emit()
        self.currentRelationWidget.load_data()
        self.dataAttributeWidget.load_data()
        self.selectAttributeWidget.load_data()

    def change_selected_attribute(self, items):
        self.selectAttributeWidget.update_widget(items)

    def dialog_critical(self, message):
        dlg = QMessageBox(self)
        dlg.setText(message)
        dlg.setIcon(QMessageBox.Critical)
        dlg.show()
