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
import json
import os.path as path

# Third Party Library
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import pyqtgraph as pg

from random import random

class PlotModelResultDialog(QDialog):
    def __init__(self, parent):
        super(QDialog, self).__init__(parent)
        layout = QGridLayout()

        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')

        # self.accFigure = Figure()
        # self.lossFigure = Figure()
        #
        # self.accCanvas = FigureCanvas(self.accFigure)
        # self.lossCanvas = FigureCanvas(self.lossFigure)
        #
        # layout.addWidget(self.accCanvas, 0, 0)
        # layout.addWidget(self.lossCanvas, 0, 1)


        self.accPlot = pg.PlotWidget()
        self.lossPlot = pg.PlotWidget()

        layout.addWidget(self.accPlot, 0, 0)
        layout.addWidget(self.lossPlot, 0, 1)
        self.setLayout(layout)

    def setHistory(self, history):
        self.history = history

    def plot(self):
        self.acc = self.history.history['acc']
        self.val_acc = self.history.history['val_acc']
        self.loss = self.history.history['loss']
        self.val_loss = self.history.history['val_loss']

        self.epochs = range(len(self.acc))

        self.plotAcc()
        self.plotLoss()

    def plotAcc(self):
        self.accPlot.addLegend()
        self.accPlot.plot(self.epochs, self.acc, pen=pg.mkPen('r', width=3), name="Training accuracy")
        self.accPlot.plot(self.epochs, self.val_acc, pen=pg.mkPen('b', width=3), name="Training accuracy")
        self.accPlot.setTitle("Training and validation accuracy")
        self.accPlot.setLabel('left', 'Accuracy')
        self.accPlot.setLabel('bottom', 'Epochs')

    def show(self):
        super(QDialog, self).show()
        self.plot()

    def plotLoss(self):
        self.lossPlot.addLegend()
        self.lossPlot.plot(self.epochs, self.loss, pen=pg.mkPen('r', width=3), name="Training loss")
        self.lossPlot.plot(self.epochs, self.val_loss, pen=pg.mkPen('b', width=3), name="Training loss")
        self.lossPlot.setTitle("Training and validation accuracy")
        self.lossPlot.setLabel('left', 'Loss')
        self.lossPlot.setLabel('bottom', 'Epochs')