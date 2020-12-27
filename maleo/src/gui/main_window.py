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
from maleo.src.gui.preprocessingtab.preprocessing_tab import PreprocessingTab
from maleo.src.gui.visualizationtab.visualization_tab import VisualizationTab
from maleo.src.gui.clusteringtab.clustering_tab import ClusteringTab
from maleo.src.gui.attributetab.attribute_tab import AttributeTab
from maleo.src.gui.associationtab.association_tab import AssociationTab
from maleo.src.gui.classificationtab.classification_tab import ClassificationTab

# Data object model accross project
from maleo.src.model.data_model import DataModel
from maleo.src.model.model_results import ModelResults
from maleo.src.utils.projectloader.project_loader import ProjectLoader


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

        self.__init_file_menu()

        self.tabs = QTabWidget()
        self.tab1 = PreprocessingTab(self, self.dataModel, screenHeight, screenWidth)
        self.tab2 = ClassificationTab(self, self.dataModel, self.modelResults, screenHeight, screenWidth)
        self.tab3 = ClusteringTab(self, self.dataModel, self.modelResults, screenHeight, screenWidth)
        # self.tab4 = associationtab(self, self.data_model, screen_height, screen_width)
        # self.tab5 = attributetab(self, self.data_model, screen_height, screen_width)
        self.tab6 = VisualizationTab(self, self.dataModel, self.modelResults, screenHeight, screenWidth)

        self.tabs.resize(500, 200)
        self.tabs.addTab(self.tab1, "Preprocessing")
        self.tabs.addTab(self.tab2, "Klasifikasi")
        self.tabs.addTab(self.tab3, "Clustering")
        # self.tabs.addTab(self.tab4, "Asosiasi")
        # self.tabs.addTab(self.tab5, "Pilih Atribut")
        self.tabs.addTab(self.tab6, "Visualisasi")

        self.tabs.setTabEnabled(1, False)
        self.tabs.setTabEnabled(2, False)
        self.tabs.setTabEnabled(3, False)
        self.tabs.setTabEnabled(4, False)
        self.tabs.setTabEnabled(5, False)

        self.tab1.dataLoadedSignal.connect(self.data_loaded)

        self.setCentralWidget(self.tabs)
        self._update_title()
        self.show()

    def __init_file_menu(self):
        open_button = QAction('Open project', self)
        open_button.setStatusTip('Open project')
        open_button.triggered.connect(self._open_project)
        self.fileMenu.addAction(open_button)

        save_button = QAction('Save Project', self)
        save_button.setShortcut('Ctrl+S')
        save_button.setStatusTip('Save project')
        save_button.triggered.connect(self._save_project)
        self.fileMenu.addAction(save_button)

        save_as_button = QAction('Save Project As', self)
        save_as_button.setStatusTip('Save project as')
        save_as_button.triggered.connect(self._save_as_project)
        self.fileMenu.addAction(save_as_button)

        exit_button = QAction('Exit', self)
        exit_button.setShortcut('Ctrl+Q')
        exit_button.setStatusTip('Exit application')
        exit_button.triggered.connect(self.close)
        self.fileMenu.addAction(exit_button)

    def _open_project(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open file", "", "Maleo project files (*.maleo)")
        if path:
            self.projectPath = path
            self.projectLoader.load_project(path)
            self.tab1.load_data()
            self.data_loaded()
            self._update_title()

    def _save_project(self):
        if self.projectPath:
            self.projectLoader.save_project(self.projectPath)
        else:
            self._save_as_project()

    def _save_as_project(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save file", "", "Maleo project files (*.maleo)")
        if path:
            self.projectPath = path
            self.projectLoader.save_project(path)
            self._update_title()

    def _update_title(self):
        self.setWindowTitle("Maleo Project - %s" % (self.projectPath if self.projectPath else "Untitled"))

    def data_loaded(self):
        self.tabs.setTabEnabled(1, True)
        self.tabs.setTabEnabled(2, True)
        self.tabs.setTabEnabled(3, True)
        self.tabs.setTabEnabled(4, True)
        self.tabs.setTabEnabled(5, True)

        self.tab2.loadData()
        # self.tab3.load_data()
        # self.tab4.load_data()
        # self.tab5.load_data()
        self.tab6.load_data()

    def closeEvent(self, event):
        self._exit_confirmation()
        if not self._want_to_close:
            event.ignore()

    def _exit_confirmation(self):
        dlg = QMessageBox()
        dlg.setIcon(QMessageBox.Question)
        dlg.setWindowTitle("Confirmation")
        dlg.setText("Are you sure you want to quit ?")
        dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        dlg.setDefaultButton(QMessageBox.No)
        button_yes = dlg.button(QMessageBox.Yes)
        button_yes.setText("Yes")
        button_no = dlg.button(QMessageBox.No)
        button_no.setText("No")
        dlg.exec_()

        if dlg.clickedButton() == button_yes:
            self._want_to_close = True
            qApp.quit()

    def dialog_critical(self, message):
        dlg = QMessageBox(self)
        dlg.setText(message)
        dlg.setIcon(QMessageBox.Critical)
        dlg.show()


def run_main_window():
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
    run_main_window()
