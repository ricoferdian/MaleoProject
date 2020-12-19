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

# Third Party Library

class FileOperationWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QHBoxLayout(self)

        self.fileOperationGroup = QGroupBox("File Operation")
        self.fileOperationLayout = QHBoxLayout()
        self.fileOperationGroup.setLayout(self.fileOperationLayout)

        self.openFileButton = QPushButton("Open File")
        self.saveFileButton = QPushButton("Save File")

        self.openFileButton.clicked.connect(self.openFile)

        self.fileOperationLayout.addWidget(self.openFileButton)
        self.fileOperationLayout.addWidget(self.saveFileButton)

        self.layout.addWidget(self.fileOperationGroup)
        self.setLayout(self.layout)

    def openFile(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open file", "", "Comma Separated Value (*.csv)")
        if path:
            self.filePath = path
            self.updateParentDataModel()

    def updateParentDataModel(self):
        self.parent().loadDataModel(self.filePath)