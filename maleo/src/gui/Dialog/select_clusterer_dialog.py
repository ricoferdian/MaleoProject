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


class SelectClustererDialog(QDialog):
    def __init__(self, parent):
        super(QDialog, self).__init__(parent)
        self.selectedModule = None

        self.libPath = path.abspath(path.join(__file__, "../../../../lib"))

        with open(self.libPath+"/ModuleList.json") as f:
            self.moduleList = json.load(f)["clustering"]

        self.layout = QVBoxLayout()

        self.moduleListWidget = QListWidget()

        self.okButton = QPushButton("OK")
        self.okButton.clicked.connect(self.on_ok)

        self.layout.addWidget(self.moduleListWidget)
        self.layout.addWidget(self.okButton)

        self.setLayout(self.layout)

    def show(self):
        super(QDialog, self).show()
        self.draw_module_list()

    def draw_module_list(self):
        self.moduleListWidget.clear()
        for key, modules in self.moduleList.items():
            for module in modules:
                self.moduleListWidget.addItem(key+"."+module)

    def on_ok(self):
        current_item = self.moduleListWidget.currentItem()
        print("currentItem", current_item)
        if current_item:
            self.selectedModule = current_item.text()
            self.parent().set_classifier(self.selectedModule)
        else:
            self.parent().parent().dialog_critical("No module selected ! Selecting last modules")
        self.close()
