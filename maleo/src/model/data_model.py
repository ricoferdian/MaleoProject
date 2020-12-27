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

This part of python program consist of the visualization tab from main GUI application
"""

class DataModel():
    def __init__(self,data, *args):
        self.data = data
        self.relation = "None"

    def setData(self, data):
        self.data = data

    def getShape(self):
        return self.data.shape

    def setRelation(self, relation):
        self.relation = relation

    def getRelation(self):
        return self.relation

    def isEmpty(self):
        if self.data is not None:
            return self.data.empty
        return True

    def getData(self):
        return self.data

    def toExcel(self, path, index=False):
        self.data.to_excel(path, index=index)

    def toCSV(self, path, index=False):
        self.data.to_csv(path, index=index)

    def toJSON(self, path, index=False):
        self.data.to_json(path, index=index)

    def removeColumn(self,indexes):
        if len(self.data.columns):
            self.data.drop(columns=[self.data.columns[index] for index in indexes], axis=1,inplace=True)
