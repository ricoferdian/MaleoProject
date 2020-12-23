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

from maleo.src.utils.DatasetLoader.PandasDatatypeCheck import *
from maleo.src.utils.DatasetLoader.TableView import TableView

class SelectAttributeWidget(QWidget):
    def __init__(self, parent, dataModel):
        super(QWidget, self).__init__(parent)
        self.dataModel = dataModel

        self.layout = QHBoxLayout(self)
        self.dataTypeCheck = PandasDatatypeCheck()

        self.selectedAttributeGroup = QGroupBox("Selected Attribute")
        self.selectedAttributeLayout = QVBoxLayout()
        self.selectedAttributeGroup.setLayout(self.selectedAttributeLayout)

        self.labelLayout = QHBoxLayout()
        self.leftLabeLayout = QVBoxLayout()
        self.rightLabelLayout = QVBoxLayout()

        self.nameLabel = QLabel()
        self.nameLabel.setText("Name")
        self.missingLabel = QLabel()
        self.missingLabel.setText("Missing")
        self.typeLabel = QLabel()
        self.typeLabel.setText("Type")
        self.uniqueLabel = QLabel()
        self.uniqueLabel.setText("Unique")

        self.leftLabeLayout.addWidget(self.nameLabel)
        self.leftLabeLayout.addWidget(self.missingLabel)

        self.rightLabelLayout.addWidget(self.typeLabel)
        self.rightLabelLayout.addWidget(self.uniqueLabel)

        self.labelLayout.addLayout(self.leftLabeLayout)
        self.labelLayout.addLayout(self.rightLabelLayout)

        self.dataAttributeTable = TableView({},0,0)
        self.dataAttributeTable.verticalHeader().setVisible(False)
        self.dataAttributeTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.dataAttributeTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.selectedAttributeLayout.addLayout(self.labelLayout, stretch=10)
        self.selectedAttributeLayout.addWidget(self.dataAttributeTable, stretch=90)

        self.layout.addWidget(self.selectedAttributeGroup)
        self.setLayout(self.layout)

    def loadData(self):
        self.data = self.dataModel.getData()

    def updateWidget(self, values):
        if len(values):
            self.selectedRowIndex = int(values[0].text())-1
            self.selectedData = self.data.iloc[:, self.selectedRowIndex]

            self.dataTypeCheck.setDataType(self.selectedData)
            self.dataType = self.dataTypeCheck.getDataType()

            self.changeLabel(self.selectedData)
            self.changeTable(self.selectedData)

    def changeLabel(self, data):
        self.dataShape = data.shape

        nullCount = data.isnull().sum()
        nullPercent = 0
        if nullCount != 0:
            nullPercent = (data.isnull().sum()*self.dataShape[0])/100

        self.nameLabel.setText("Name : "+data.name)
        self.missingLabel.setText("Missing : "+str(nullCount)+" ("+str(nullPercent)+"%)")
        self.typeLabel.setText("Type : "+str(self.dataType))
        self.uniqueLabel.setText("Unique : "+str(data.nunique()))

    def changeTable(self, data):
        # print(data.describe())
        if self.dataType == self.dataTypeCheck.getType().Numeric:
            tableData = {
                "Statistic":{
                    0:"Minimum",
                    1:"Maximum",
                    2:"Mean",
                    3: "Standard Deviation"
                },
                "Value":{
                    0:data.min(),
                    1:data.max(),
                    2:data.mean(),
                    3:data.std(),
                }
            }
            self.drawTable(tableData,4,2)
        elif self.dataType == self.dataTypeCheck.getType().Nominal:
            uniqueLabels = data.value_counts()
            tableData = {
                " Label":{
                    i:label for label,i in zip(uniqueLabels.keys(),range(len(uniqueLabels)))
                },
                "Count":{
                    i:uniqueLabels[value] for value,i in zip(uniqueLabels.keys(),range(len(uniqueLabels)))
                },
                "Weight":{
                    i:float(uniqueLabels[value]) for value,i in zip(uniqueLabels.keys(),range(len(uniqueLabels)))
                }
            }
            self.drawTable(tableData,len(uniqueLabels),3)
        else:
            print("Unknown")

    def drawTable(self,data,row, col):
        self.dataAttributeTable.updateParameter(col,row)
        self.dataAttributeTable.updateData(data)
        self.dataAttributeTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

