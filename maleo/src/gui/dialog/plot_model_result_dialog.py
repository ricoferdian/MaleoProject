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

# Third Party Library
import pyqtgraph as pg

from random import random


class PlotModelResultDialog(QDialog):
    def __init__(self, parent):
        super(QDialog, self).__init__(parent)
        self.layout = QGridLayout()
        self.history = None
        self.acc = None
        self.val_acc = None
        self.loss = None
        self.val_loss = None
        self.epochs = None

        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')

        self.accPlotWidget = pg.PlotWidget()
        self.lossPlotWidget = pg.PlotWidget()

        self.accPlotWidget.addLegend()

        self.trainAccPlot = self.accPlotWidget.plot([], [], pen=pg.mkPen('r', width=3), name="Training accuracy")
        self.valAccPlot = self.accPlotWidget.plot([], [], pen=pg.mkPen('b', width=3), name="Validation accuracy")

        self.accPlotWidget.setTitle("Training and validation accuracy")
        self.accPlotWidget.setLabel('left', 'Accuracy')
        self.accPlotWidget.setLabel('bottom', 'Epochs')

        self.lossPlotWidget.addLegend()

        self.trainLossPlot = self.lossPlotWidget.plot([], [], pen=pg.mkPen('r', width=3), name="Training loss")
        self.valLossPlot = self.lossPlotWidget.plot([], [], pen=pg.mkPen('b', width=3), name="Validation loss")

        self.lossPlotWidget.setTitle("Training and validation loss")
        self.lossPlotWidget.setLabel('left', 'Loss')
        self.lossPlotWidget.setLabel('bottom', 'Epochs')

        self.layout.addWidget(self.accPlotWidget, 0, 0)
        self.layout.addWidget(self.lossPlotWidget, 0, 1)
        self.setLayout(self.layout)

    def set_history(self, history):
        self.history = history

    def plot(self):
        self.acc = self.history.history['acc']
        self.val_acc = self.history.history['val_acc']
        self.loss = self.history.history['loss']
        self.val_loss = self.history.history['val_loss']

        self.epochs = range(len(self.acc))

        self.plot_acc()
        self.plot_loss()

    def plot_acc(self):
        self.trainAccPlot.setData(self.epochs, self.acc)
        self.valAccPlot.setData(self.epochs, self.val_acc)

    def show(self):
        super(QDialog, self).show()
        self.plot()

    def plot_loss(self):
        self.trainLossPlot.setData(self.epochs, self.loss)
        self.valLossPlot.setData(self.epochs, self.val_loss)
