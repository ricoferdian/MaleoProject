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

DatasetEditor
Copyright (C) 2020 Henrico Aldy Ferdian & Lennia Savitri Azzahra Loviana
Udayana University, Bali, Indonesia

This part of python program consist of the file operation widget
in preprocessing tab from main GUI application
"""

# PyQt5 GUI Library
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# Third Party Library

# Data operation
from maleo.src.model.data_history import DataHistory

# GUI Table View Pandas Library
from maleo.src.utils.pandas_table_view import PandasTableView

# Utility library
import maleo.src.utils.number_conversion as nconvert
from maleo.src.utils.datasetloader.pandas_datatype_check import PandasDatatypeCheck


class DatasetEditor(QDialog):
    def __init__(self, parent, data_model, parent_history):
        super(QDialog, self).__init__(parent)
        self.dataModel = data_model
        self.data = None
        self.dataTypeCheck = PandasDatatypeCheck()
        self.isUndoConfirmed = False

        self.dataHistory = DataHistory()
        self.parentHistory = parent_history

        self.layout = QVBoxLayout()
        self.btnLayout = QHBoxLayout()

        self.addInstanceButton = QPushButton("Add Instance")
        self.undoButton = QPushButton("Undo")
        self.saveButton = QPushButton("Save")
        self.cancelButton = QPushButton("Cancel")

        self.addInstanceButton.clicked.connect(self._add_instance)
        self.undoButton.clicked.connect(self._undo_confirmation)
        self.saveButton.clicked.connect(self.on_ok)
        self.cancelButton.clicked.connect(self.on_cancel)

        self.btnLayout.addWidget(self.addInstanceButton)
        self.btnLayout.addWidget(self.undoButton)
        self.btnLayout.addWidget(self.saveButton)
        self.btnLayout.addWidget(self.cancelButton)

        self.undoButton.setEnabled(False)

        self.dataAttributeTable = PandasTableView({}, 0, 0)
        self.dataAttributeTable.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.dataAttributeTable.setEditTriggers(QAbstractItemView.DoubleClicked)
        self.dataAttributeTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.dataAttributeTable.setContextMenuPolicy(Qt.CustomContextMenu)

        self.dataAttributeTable.customContextMenuRequested.connect(self.showContextMenu)
        self.dataAttributeTable.cellChanged.connect(self._data_changed)

        self.layout.addWidget(self.dataAttributeTable)
        self.layout.addLayout(self.btnLayout)

        self.setMinimumSize(600, 400)
        self.setWindowTitle("Maleo Editor")
        self.setLayout(self.layout)

    def showContextMenu(self, pos):
        menu = QMenu()
        clear_action = menu.addAction("Undo")
        add_instance = menu.addAction("Add Instance")
        delete_instance = menu.addAction("Delete Selected Instance")
        delete_all_instance = menu.addAction("Delete ALL Selected Instance")

        if self.dataHistory.is_empty():
            clear_action.setEnabled(False)
        else:
            clear_action.setEnabled(True)

        action = menu.exec_(self.mapToGlobal(pos))

        if action == clear_action:
            self._undo_confirmation()
        elif action == add_instance:
            self._add_instance()
        elif action == delete_instance:
            self._delete_instances(False)
        elif action == delete_all_instance:
            self._delete_instances(True)

    def _delete_instances(self, is_all):
        selected_rows = self.dataAttributeTable.selectionModel().selectedRows()
        num_deleted_row = 0
        for selected_row in selected_rows:
            row = selected_row.row()
            self.dataHistory.append_data({"row": row, "col": "all_deletion", "value": self.data})

            self.data.drop(index=row - num_deleted_row, axis=0, inplace=True)
            self.data.reset_index(inplace=True, drop=True)
            self.dataAttributeTable.deleteRow(row - num_deleted_row)

            num_deleted_row += 1
            if not is_all:
                break
        self.update_status()

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

    def update_status(self):
        if self.dataHistory.is_empty():
            self.undoButton.setEnabled(False)
        else:
            self.undoButton.setEnabled(True)

    def _undo_operation(self):
        data = self.dataHistory.pop_data()
        self.update_status()
        self._setTableItemData(data["row"], data["col"], data["value"])

    def _setTableItemData(self, row, col, value):
        if col == "all_insertion":
            self.dataAttributeTable.cellChanged.disconnect()
            self.dataAttributeTable.deleteRow(row)
            self.dataAttributeTable.cellChanged.connect(self._data_changed)
        elif col == "all_deletion":
            self.dataAttributeTable.cellChanged.disconnect()
            self.dataAttributeTable.appendRow(value)
            self.dataAttributeTable.cellChanged.connect(self._data_changed)
        else:
            self.dataAttributeTable.cellChanged.disconnect()
            self.dataAttributeTable.setItemData(row, col, value)
            self.dataAttributeTable.cellChanged.connect(self._data_changed)

    def show(self):
        super(QDialog, self).show()
        self.data = self.dataModel.get_copy()
        try:
            self._show_table()
        except Exception as e:
            self.parent().parent().dialog_critical("Error exception !"+str(e))

    def _show_table(self):
        if not self.dataModel.is_empty():
            self._draw_table(self.data, self.data.shape[0], self.data.shape[1])
        else:
            self._draw_table({}, 0, 0)

    def _draw_table(self, data, row, col):
        self.dataAttributeTable.updateParameter(col, row)
        self.dataAttributeTable.cellChanged.disconnect()
        self.dataAttributeTable.updateData(data)
        self.dataAttributeTable.cellChanged.connect(self._data_changed)
        self.dataAttributeTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def _append_table_row(self, new_row):
        row_count = self.dataAttributeTable.rowCount()
        self.dataHistory.append_data({"row": row_count, "col": "all_insertion", "value": None})
        self.update_status()

        self.data = self.data.append(new_row, ignore_index=True)
        self.dataAttributeTable.cellChanged.disconnect()
        self.dataAttributeTable.appendRow(new_row)
        self.dataAttributeTable.cellChanged.connect(self._data_changed)

    def _data_changed(self, row, col):
        changed_column = self.data.iloc[:, col]
        self.dataTypeCheck.setDataType(changed_column)
        self.dataType = self.dataTypeCheck.getDataType()

        item = self.dataAttributeTable.item(row, col).text()

        if self.dataType == self.dataTypeCheck.getType().Numeric:
            if nconvert.is_num(item):
                self.dataHistory.append_data({"row": row, "col": col, "value": self.data.iat[row, col].copy()})
                self.data.iat[row, col] = nconvert.str_to_num(item)
                self.update_status()
            else:
                self.parent().parent().dialog_critical("Cannot update numeric column by nominal value !")
                self.dataAttributeTable.setItemData(row, col, self.data.iat[row, col])

        elif self.dataType == self.dataTypeCheck.getType().Nominal:
            if not nconvert.is_num(item):
                self.dataHistory.append_data({"row": row, "col": col, "value": self.data.iat[row, col].copy()})
                self.data.iat[row, col] = item
                self.update_status()
            else:
                self.parent().parent().dialog_critical("Cannot update nominal column by numeric value !")
                self.dataAttributeTable.setItemData(row, col, self.data.iat[row, col])

        else:
            self.parent().parent().dialog_critical("Column datatype is unknown !")
            print("This col item is unknown")

    def _add_instance(self):
        new_row = {}
        for column in self.data.columns:
            changed_column = self.data.loc[:, column]
            self.dataTypeCheck.setDataType(changed_column)
            self.dataType = self.dataTypeCheck.getDataType()

            if self.dataType == self.dataTypeCheck.getType().Numeric:
                new_row[column] = 0
            elif self.dataType == self.dataTypeCheck.getType().Nominal:
                new_row[column] = ""
            else:
                new_row[column] = ""
        self._append_table_row(new_row)

    def on_ok(self):
        self.parentHistory.append_data(self.dataModel.get_copy())
        self.dataModel.set_data(self.data)
        self.parent().parent().data_loaded()
        self.close()

    def on_cancel(self):
        self.close()
