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
from maleo.src.utils.DatasetLoader.CSVLoader import CSVLoader
from maleo.src.utils.DatasetLoader.JSONLoader import JSONLoader
from maleo.src.utils.DatasetLoader.ExcelLoader import ExcelLoader
from maleo.src.utils.DatasetLoader.SPSSLoader import SPSSLoader
from maleo.src.utils.DatasetLoader.SASLoader import SASLoader
from maleo.src.utils.DatasetLoader.PickleLoader import PickleLoader
from maleo.src.utils.DatasetLoader.StataLoader import StataLoader

class FileOperationWidget(QWidget):
    def __init__(self, parent, dataModel):
        super(QWidget, self).__init__(parent)
        self.dataModel = dataModel

        self.layout = QHBoxLayout(self)

        self.fileOperationGroup = QGroupBox("File Operation")
        self.fileOperationLayout = QHBoxLayout()
        self.fileOperationGroup.setLayout(self.fileOperationLayout)

        self.openFileButton = QPushButton("Open File")
        self.saveFileButton = QPushButton("Save File")

        self.openFileButton.clicked.connect(self.openFile)
        self.saveFileButton.clicked.connect(self.saveFile)

        self.fileOperationLayout.addWidget(self.openFileButton)
        self.fileOperationLayout.addWidget(self.saveFileButton)

        self.layout.addWidget(self.fileOperationGroup)
        self.setLayout(self.layout)

    def openFile(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open file", "", "Comma Separated Value (*.csv);"+
                                              ";Javascript Object Notation (*.json);"+
                                              ";Excel 2003-2007 Document (*.xls);"+
                                              ";Excel Document (*.xlsx);"+
                                              ";SPSS File (*.sav);"+
                                              ";SAS File (*.sas);"+
                                              ";SAS v7 File (*.sas7bpgm);"+
                                              ";Stata File (*.dta);"+
                                              ";Python Pickle File (*.P);"+
                                                ";Python Pickle File (*.pkl);"+
                                              ";Python Pickle File (*.pickle)")
        if path:
            self.filePath = path
            self.loadDataModel()

    def saveFile(self):
        if not self.dataModel.isEmpty():
            path, _ = QFileDialog.getSaveFileName(self, "Save file", "", "Comma Separated Value (*.csv);"+
                                                  ";Javascript Object Notation (*.json);"+
                                                  ";Excel 2003-2007 Document (*.xls);"+
                                                  ";Excel Document (*.xlsx);"+
                                                  ";SPSS File (*.sav);"+
                                                  ";SAS File (*.sas);"+
                                                  ";SAS v7 File (*.sas7bpgm);"+
                                                  ";Stata File (*.dta);"+
                                                  ";Python Pickle File (*.P);"+
                                                  ";Python Pickle File (*.pkl);"+
                                                  ";Python Pickle File (*.pickle)")
            if path:
                self.filePath = path
                self.saveDataModel()
        else:
            self.parent().dialog_critical("Cannot save nothing !")

    def loadDataModel(self):
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
        print("data",self.dataModel.getData())
        self.parent().dataLoaded()

    def saveDataModel(self):
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