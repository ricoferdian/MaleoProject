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

CurrentRelationWidget
Copyright (C) 2020 Henrico Aldy Ferdian & Lennia Savitri Azzahra Loviana
Udayana University, Bali, Indonesia

This part of python program consist of the CurrentRelationWidget widget
in preprocessing tab from main GUI application
"""

# PyQt5 GUI Library
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# Python Library
import sys

# Third Party Library

class CurrentRelationWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QHBoxLayout(self)

        self.currentRelationGroup = QGroupBox("Current Relation")
        self.currentRelationLayout = QHBoxLayout()
        self.currentRelationGroup.setLayout(self.currentRelationLayout)

        self.leftRelationLayout = QVBoxLayout()
        self.rightRelationLayout = QVBoxLayout()

        self.relationLabel = QLabel("Relation :")
        self.instancesLabel = QLabel("Instances :")
        self.attributesLabel = QLabel("Attributes :")
        self.sumWeightsLabel = QLabel("Sum Weights :")

        self.leftRelationLayout.addWidget(self.relationLabel)
        self.leftRelationLayout.addWidget(self.instancesLabel)

        self.rightRelationLayout.addWidget(self.attributesLabel)
        self.rightRelationLayout.addWidget(self.sumWeightsLabel)

        self.currentRelationLayout.addLayout(self.leftRelationLayout)
        self.currentRelationLayout.addLayout(self.rightRelationLayout)

        self.layout.addWidget(self.currentRelationGroup)
        self.setLayout(self.layout)