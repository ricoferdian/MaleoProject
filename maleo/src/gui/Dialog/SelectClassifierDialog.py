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
from maleo.lib.Classification import *

class SelectClassifierDialog(QDialog):
    def __init__(self, parent):
        super(QDialog, self).__init__(parent)

        self.libPath = path.abspath(path.join(__file__, "../../../../lib"))

        with open(self.libPath+"/ModuleList.json") as f:
            self.moduleList = json.load(f)["Classification"]

        self.layout = QVBoxLayout()

        self.moduleListWidget = QListWidget()

        self.btnJalankan = QPushButton("OK")
        self.btnJalankan.clicked.connect(self.OnOk)

        self.layout.addWidget(self.moduleListWidget)
        self.layout.addWidget(self.btnJalankan)

        self.setLayout(self.layout)

    def show(self):
        super(QDialog, self).show()
        self.drawModuleList()

    def drawModuleList(self):
        self.moduleListWidget.clear()
        for key, modules in self.moduleList.items():
            for module in modules:
                self.moduleListWidget.addItem(key+"."+module)

    def OnOk(self):
        currentItem = self.moduleListWidget.currentItem()
        print("currentItem",currentItem)
        if currentItem:
            self.selectedModule = currentItem.text()
            self.parent().setClassifier(self.selectedModule)
        else:
            self.parent().parent().dialog_critical("No module selected ! Selecting last modules")
        self.close()