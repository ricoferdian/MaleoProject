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

# GUI part
from maleo.src.gui.dialog.dataset_editor_dialog import DatasetEditor
from maleo.src.gui.dialog.mysql_connection_dialog import MysqlConnectionDialog


class FileOperationWidget(QWidget):
    def __init__(self, parent, data_model, data_history):
        super(QWidget, self).__init__(parent)

        self.dataModel = data_model
        self.dataHistory = data_history
        self.filePath = None
        self.isUndoConfirmed = False
        self.datasetEditor = DatasetEditor(self, data_model, data_history)
        self.mysqlDialog = MysqlConnectionDialog(self, self.dataModel)

        self.layout = QHBoxLayout(self)

        self.fileOperationGroup = QGroupBox("File Operation")
        self.fileOperationLayout = QHBoxLayout()
        self.fileOperationGroup.setLayout(self.fileOperationLayout)

        self.openDatasetButton = QPushButton("Open Dataset")
        self.openDatabaseButton = QPushButton("Open From Database")
        self.undoOperationButton = QPushButton("Undo Operation")
        self.editDatasetButton = QPushButton("Edit Dataset")
        self.saveDatasetButton = QPushButton("Save Dataset")

        self.openDatasetButton.clicked.connect(self.open_file)
        self.openDatabaseButton.clicked.connect(self._open_database)
        self.undoOperationButton.clicked.connect(self._undo_confirmation)
        self.editDatasetButton.clicked.connect(self._edit_dataset)
        self.saveDatasetButton.clicked.connect(self.save_file)

        self.undoOperationButton.setEnabled(False)
        self.editDatasetButton.setEnabled(False)
        self.saveDatasetButton.setEnabled(False)

        self.fileOperationLayout.addWidget(self.openDatasetButton)
        self.fileOperationLayout.addWidget(self.openDatabaseButton)
        self.fileOperationLayout.addWidget(self.undoOperationButton)
        self.fileOperationLayout.addWidget(self.editDatasetButton)
        self.fileOperationLayout.addWidget(self.saveDatasetButton)

        self.layout.addWidget(self.fileOperationGroup)
        self.setLayout(self.layout)

    def _open_database(self):
        self.mysqlDialog.show()

    def _undo_confirmation(self):
        if self.isUndoConfirmed:
            self._undo_operation()
        else:
            dlg = QMessageBox()
            dlg.setIcon(QMessageBox.Question)
            dlg.setWindowTitle("Confirmation")
            dlg.setText("Are you sure you want to undo the last action ? This action cannot be undone.")
            dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            dlg.setDefaultButton(QMessageBox.No)
            button_yes = dlg.button(QMessageBox.Yes)
            button_yes.setText("Yes")
            button_no = dlg.button(QMessageBox.No)
            button_no.setText("No")
            dlg.exec_()

            if dlg.clickedButton() == button_yes:
                self.isUndoConfirmed = True
                self._undo_operation()

    def _undo_operation(self):
        data = self.dataHistory.pop_past()
        self.dataModel.set_data(data)
        self.parent().data_loaded()

    def _edit_dataset(self):
        if not self.datasetEditor.isVisible():
            self.datasetEditor.show()
        else:
            self.parent().dialog_critical("Editor already running !")

    def load_data(self):
        self.datasetEditor.load_data()
        if self.dataModel.is_empty():
            self.editDatasetButton.setEnabled(False)
            self.saveDatasetButton.setEnabled(False)
        else:
            self.saveDatasetButton.setEnabled(True)
            self.editDatasetButton.setEnabled(True)

        if self.dataHistory.is_past_empty():
            self.undoOperationButton.setEnabled(False)
        else:
            self.undoOperationButton.setEnabled(True)

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

            try:
                self._load_data_model()
            except Exception as e:
                self.parent().dialog_critical("Error exception !\n"+str(e))

    def save_file(self):
        if not self.dataModel.is_empty():
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
                try:
                    self._save_data_model()
                except Exception as e:
                    self.parent().dialog_critical("Error ezception : \n"+str(e))
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
        self.dataModel.set_data(self.dataLoader.getData())
        self.parent().data_loaded()

    def _save_data_model(self):
        if self.filePath.lower().endswith('.csv'):
            self.dataModel.to_csv(self.filePath)
        elif self.filePath.lower().endswith('.json'):
            self.dataModel.to_json(self.filePath)
        elif self.filePath.lower().endswith('.xls'):
            self.dataModel.to_excel(self.filePath)
        elif self.filePath.lower().endswith('.xlsx'):
            self.dataModel.to_excel(self.filePath)
        else:
            self.parent().dialog_critical("Unknown file extension to save !")
