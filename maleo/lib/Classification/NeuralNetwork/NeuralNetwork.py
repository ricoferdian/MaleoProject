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

Copyright (C) 2020 Henrico Aldy Ferdian & Lennia Savitri Azzahra Loviana
Udayana University, Bali, Indonesia
"""

# Third Party Library
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

# Inherit
from maleo.lib.Module import Module

class NeuralNetwork(Module):
    def __init__(self, data, labels, *args):
        super(NeuralNetwork, self).__init__(data, labels)

    def nominalToInteger(self, labels, uniqueLabels):
        for index, data in enumerate(labels):
            labels[index] = uniqueLabels.find(data)
        return np.array(labels)

    def integerToNominal(self, labels, uniqueLabels):
        print("Converting integer labels to integer labels")
        for index, data in enumerate(labels):
            labels[index] = uniqueLabels[data]
        return np.array(labels)

    def preprocessData(self):
        x = self.data.copy()
        y = self.labels.copy()

        x = x.to_numpy()
        y = y.to_numpy()

        if y.dtype.char == 'O':
            sorted = self.labels.value_counts()
            sorted = list(i for i in sorted.keys())
            sorted.sort()
            self.uniqueLabels = ''.join(str(v) for v in sorted)

            y = self.nominalToInteger(y,self.uniqueLabels)

        self.splitDataset(x, y, self.value)