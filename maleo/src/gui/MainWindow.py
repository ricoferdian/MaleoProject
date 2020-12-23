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

# Data model accross project
from maleo.src.model.DataModel import DataModel
from maleo.src.model.ModelResults import ModelResults
from maleo.src.utils.ProjectLoader.ProjectLoader import ProjectLoader

# Python library
import os

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        global screenWidth
        global screenHeight
        self._want_to_close = False
        self.projectPath = None

        self.dataModel = DataModel(None)
        self.modelResults = ModelResults()
        self.projectLoader = ProjectLoader(self.dataModel, self.modelResults)

        self.mainMenu = self.menuBar()
        self.fileMenu = self.mainMenu.addMenu('File')
        self.editMenu = self.mainMenu.addMenu('Edit')
        self.viewMenu = self.mainMenu.addMenu('View')
        self.searchMenu = self.mainMenu.addMenu('Search')
        self.toolsMenu = self.mainMenu.addMenu('Tools')
        self.helpMenu = self.mainMenu.addMenu('Help')

        self.initFileMenu()

        self.tabs = QTabWidget()
        self.tab1 = PreprocessingTab(self, self.dataModel, screenHeight, screenWidth)
        self.tab2 = ClassificationTab(self, self.dataModel, self.modelResults, screenHeight, screenWidth)
        self.tab3 = ClusteringTab(self, self.dataModel, self.modelResults, screenHeight, screenWidth)
        # self.tab4 = AssociationTab(self, self.dataModel, screenHeight, screenWidth)
        # self.tab5 = AttributeTab(self, self.dataModel, screenHeight, screenWidth)
        self.tab6 = VisualizationTab(self, self.dataModel, self.modelResults, screenHeight, screenWidth)

        self.tabs.resize(500,200)
        self.tabs.addTab(self.tab1, "Preprocessing")
        self.tabs.addTab(self.tab2, "Klasifikasi")
        self.tabs.addTab(self.tab3, "Clustering")
        # self.tabs.addTab(self.tab4, "Asosiasi")
        # self.tabs.addTab(self.tab5, "Pilih Atribut")
        self.tabs.addTab(self.tab6, "Visualisasi")

        self.tabs.setTabEnabled(1,False)
        self.tabs.setTabEnabled(2,False)
        self.tabs.setTabEnabled(3,False)
        self.tabs.setTabEnabled(4,False)
        self.tabs.setTabEnabled(5,False)

        self.tab1.dataLoadedSignal.connect(self.dataLoaded)

        self.setCentralWidget(self.tabs)
        self.update_title()
        self.show()

    def initFileMenu(self):
        openButton = QAction('Open project', self)
        openButton.setStatusTip('Open project')
        openButton.triggered.connect(self.openProject)
        self.fileMenu.addAction(openButton)

        saveButton = QAction('Save Project', self)
        saveButton.setShortcut('Ctrl+S')
        saveButton.setStatusTip('Save project')
        saveButton.triggered.connect(self.saveProject)
        self.fileMenu.addAction(saveButton)

        saveAsButton = QAction('Save Project As', self)
        saveAsButton.setStatusTip('Save project as')
        saveAsButton.triggered.connect(self.saveAsProject)
        self.fileMenu.addAction(saveAsButton)

        exitButton = QAction('Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(self.close)
        self.fileMenu.addAction(exitButton)

    def openProject(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open file", "", "Maleo project files (*.maleo)")
        if path:
            self.projectPath = path
            self.projectLoader.loadProject(path)
            self.tab1.loadData()
            self.dataLoaded()
            self.update_title()

    def saveProject(self):
        if self.projectPath:
            self.projectLoader.saveProject(self.projectPath)
        else:
            self.saveAsProject()

    def saveAsProject(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save file", "", "Maleo project files (*.maleo)")
        if path:
            self.projectPath = path
            self.projectLoader.saveProject(path)
            self.update_title()

    def update_title(self):
        self.setWindowTitle("Maleo Project - %s" % (self.projectPath if self.projectPath else "Untitled"))

    def dataLoaded(self):
        self.tabs.setTabEnabled(1,True)
        self.tabs.setTabEnabled(2,True)
        self.tabs.setTabEnabled(3,True)
        self.tabs.setTabEnabled(4,True)
        self.tabs.setTabEnabled(5,True)

        self.tab2.loadData()
        # self.tab3.loadData()
        # self.tab4.loadData()
        # self.tab5.loadData()
        self.tab6.loadData()

    def closeEvent(self, event):
        self.exitConfirmation()
        if not self._want_to_close:
            event.ignore()

    def exitConfirmation(self):
        dlg = QMessageBox()
        dlg.setIcon(QMessageBox.Question)
        dlg.setWindowTitle("Confirmation")
        dlg.setText("Are you sure you want to quit ?")
        dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        dlg.setDefaultButton(QMessageBox.No)
        buttonYes = dlg.button(QMessageBox.Yes)
        buttonYes.setText("Yes")
        buttonNo = dlg.button(QMessageBox.No)
        buttonNo.setText("No")
        dlg.exec_()

        if dlg.clickedButton() == buttonYes:
            self._want_to_close = True
            qApp.quit()

    def dialog_critical(self, message):
        dlg = QMessageBox(self)
        dlg.setText(message)
        dlg.setIcon(QMessageBox.Critical)
        dlg.show()

def runMainWindow():
    global screenWidth
    global screenHeight

    app = QApplication(sys.argv)
    app.setApplicationName("Maleo Workbench")
    app.setAttribute(Qt.AA_DisableWindowContextHelpButton)

    screen = app.primaryScreen()
    size = screen.size()

    screenWidth = size.width()
    screenHeight = size.height()

    window = MainWindow()
    app.exec_()


# Run main program
if __name__ == '__main__':
    runMainWindow()