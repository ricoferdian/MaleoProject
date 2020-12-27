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
from PyQt5.QtWidgets import *

# Python Library
import os

# Third Party Library

# Data operation
from maleo.src.utils.datasetloader.csv_loader import CSVLoader
from maleo.src.utils.datasetloader.json_loader import JSONLoader
from maleo.src.utils.datasetloader.excel_loader import ExcelLoader
from maleo.src.utils.datasetloader.spss_loader import SPSSLoader
from maleo.src.utils.datasetloader.sas_loader import SASLoader
from maleo.src.utils.datasetloader.pickle_loader import PickleLoader
from maleo.src.utils.datasetloader.stata_loader import StataLoader


class FileOperationWidget(QWidget):
    def __init__(self, parent, data_model):
        super(QWidget, self).__init__(parent)
        self.dataModel = data_model
        self.filePath = None

        self.layout = QHBoxLayout(self)

        self.fileOperationGroup = QGroupBox("File Operation")
        self.fileOperationLayout = QHBoxLayout()
        self.fileOperationGroup.setLayout(self.fileOperationLayout)

        self.openFileButton = QPushButton("Open Dataset File")
        self.saveFileButton = QPushButton("Save Dataset File")

        self.openFileButton.clicked.connect(self.open_file)
        self.saveFileButton.clicked.connect(self.save_file)

        self.fileOperationLayout.addWidget(self.openFileButton)
        self.fileOperationLayout.addWidget(self.saveFileButton)

        self.layout.addWidget(self.fileOperationGroup)
        self.setLayout(self.layout)

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open file", "", "Comma Separated Value (*.csv);" +
                                              ";Javascript Object Notation (*.json);" +
                                              ";Excel 2003-2007 Document (*.xls);" +
                                              ";Excel Document (*.xlsx);" +
                                              ";SPSS File (*.sav);" +
                                              ";SAS File (*.sas);" +
                                              ";SAS v7 File (*.sas7bpgm);" +
                                              ";Stata File (*.dta);" +
                                              ";Python Pickle File (*.P);" +
                                              ";Python Pickle File (*.pkl);" +
                                              ";Python Pickle File (*.pickle)")
        if path:
            self.filePath = path
            self._load_data_model()

    def save_file(self):
        if not self.dataModel.isEmpty():
            path, _ = QFileDialog.getSaveFileName(self, "Save file", "", "Comma Separated Value (*.csv);" +
                                                  ";Javascript Object Notation (*.json);" +
                                                  ";Excel 2003-2007 Document (*.xls);" +
                                                  ";Excel Document (*.xlsx);" +
                                                  ";SPSS File (*.sav);" +
                                                  ";SAS File (*.sas);" +
                                                  ";SAS v7 File (*.sas7bpgm);" +
                                                  ";Stata File (*.dta);" +
                                                  ";Python Pickle File (*.P);" +
                                                  ";Python Pickle File (*.pkl);" +
                                                  ";Python Pickle File (*.pickle)")
            if path:
                self.filePath = path
                self._save_data_model()
        else:
            self.parent().dialog_critical("Cannot save nothing !")

    def _load_data_model(self):
        self.filename = os.path.splitext(os.path.basename(self.filePath))[0]

        if self.filePath.lower().endswith('.csv'):
            self.dataLoader = CSVLoader(self.filePath)
        elif self.filePath.lower().endswith('.json'):
            self.dataLoader = JSONLoader(self.filePath)
        elif self.filePath.lower().endswith('.xls'):
            self.dataLoader = ExcelLoader(self.filePath)
        elif self.filePath.lower().endswith('.xlsx'):
            self.dataLoader = ExcelLoader(self.filePath)
        elif self.filePath.lower().endswith('.xlsx'):
            self.dataLoader = ExcelLoader(self.filePath)
        elif self.filePath.lower().endswith('.sas'):
            self.dataLoader = SASLoader(self.filePath)
        elif self.filePath.lower().endswith('.sas7bpgm'):
            self.dataLoader = SASLoader(self.filePath)
        elif self.filePath.lower().endswith('.sav'):
            self.dataLoader = SPSSLoader(self.filePath)
        elif self.filePath.lower().endswith('.dta'):
            self.dataLoader = StataLoader(self.filePath)
        elif self.filePath.lower().endswith('.P'):
            self.dataLoader = PickleLoader(self.filePath)
        elif self.filePath.lower().endswith('.pkl'):
            self.dataLoader = PickleLoader(self.filePath)
        elif self.filePath.lower().endswith('.pickle'):
            self.dataLoader = PickleLoader(self.filePath)
        else:
            self.dialog_critical("Unknown file extension to load !")
            return

        self.dataLoader.loadData()
        self.dataModel.setData(self.dataLoader.getData())
        print("data", self.dataModel.getData())
        self.parent().dataLoaded()

    def _save_data_model(self):
        if self.filePath.lower().endswith('.csv'):
            self.dataModel.toCSV(self.filePath)
        elif self.filePath.lower().endswith('.json'):
            self.dataModel.toJSON(self.filePath)
        elif self.filePath.lower().endswith('.xls'):
            self.dataModel.toExcel(self.filePath)
        elif self.filePath.lower().endswith('.xlsx'):
            self.dataModel.toExcel(self.filePath)
        else:
            self.parent().dialog_critical("Unknown file extension to save !")
