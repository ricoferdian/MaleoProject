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

This part of python program consist of the main GUI application
"""

# PyQt5 GUI Library
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# Python Library
import sys

# Third Party Library

# GUI part Library
from maleo.src.gui.PreprocessingTab.PreprocessingTab import PreprocessingTab
from maleo.src.gui.VisualizationTab.VisualizationTab import VisualizationTab
from maleo.src.gui.ClusteringTab.ClusteringTab import ClusteringTab
from maleo.src.gui.AttributeTab.AttributeTab import AttributeTab
from maleo.src.gui.AssociationTab.AssociationTab import AssociationTab
from maleo.src.gui.ClassificationTab.ClassificationTab import ClassificationTab

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        global screenWidth
        global screenHeight

        self.tabs = QTabWidget()

        self.tab1 = PreprocessingTab(self, screenHeight, screenWidth)
        self.tab2 = ClassificationTab(self, screenHeight, screenWidth)
        self.tab3 = ClusteringTab(self, screenHeight, screenWidth)
        self.tab4 = AssociationTab(self, screenHeight, screenWidth)
        self.tab5 = AttributeTab(self, screenHeight, screenWidth)
        self.tab6 = VisualizationTab(self, screenHeight, screenWidth)

        self.tabs.resize(300,200)
        self.tabs.addTab(self.tab1, "Preprocessing")
        self.tabs.addTab(self.tab2, "Klasifikasi")
        self.tabs.addTab(self.tab3, "Clustering")
        self.tabs.addTab(self.tab4, "Asosiasi")
        self.tabs.addTab(self.tab5, "Pilih Atribut")
        self.tabs.addTab(self.tab6, "Visualisasi")

        self.tab1.dataModelSignal.connect(self.updateDataModel)

        self.setCentralWidget(self.tabs)
        self.show()

    def updateDataModel(self, dataModel):
        self.dataModel = dataModel
        self.data = self.dataModel.getData()
        self.header = self.dataModel.getHeaders()

# Run main program
if __name__ == '__main__':
    global screenWidth
    global screenHeight

    app = QApplication(sys.argv)
    app.setApplicationName("Maleo Workbench")

    screen = app.primaryScreen()
    size = screen.size()

    screenWidth = size.width()
    screenHeight = size.height()

    window = MainWindow()
    app.exec_()