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


class ClassifierOutputWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QHBoxLayout(self)
        self.originalStdout = sys.stdout
        self.isListening = False

        self.classifierOutputGroup = QGroupBox("Classifier Output")
        self.classifierOutputLayout = QHBoxLayout()
        self.classifierOutputGroup.setLayout(self.classifierOutputLayout)

        self.classifierOutput = []

        self.outputWidget = Outputwidget()
        self.outputWidget.setReadOnly(True)

        self.classifierOutputLayout.addWidget(self.outputWidget)

        self.layout.addWidget(self.classifierOutputGroup)
        self.setLayout(self.layout)

    def get_output_widget(self):
        return self.outputWidget

    def show_output(self, index):
        if len(self.classifierOutput)>index and not self.isListening:
            output = self.classifierOutput[index]
            self.outputWidget.setPlainText(output)

    def start_listen_output(self):
        self.outputWidget.setPlainText("")
        self.isListening = True
        # sys.stdout = self.outputWidget
        self.currentIndex = len(self.classifierOutput)
        self.classifierOutput.append("")

    def stop_listen_output(self):
        self.isListening = False
        # sys.stdout = self.originalStdout
        output = self.outputWidget.toPlainText()
        self.classifierOutput[self.currentIndex] = output

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open file", "", "Dataset (*.csv *.json *.xls *.xlsx)")
        if path:
            self.filePath = path
            self.update_parent_data_model()

    def update_parent_data_model(self):
        self.parent().load_data_model(self.filePath)

class Outputwidget(QPlainTextEdit):
    def write(self, txt):
        self.appendPlainText(str(txt))
    def flush(self):
        pass