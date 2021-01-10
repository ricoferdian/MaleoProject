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
import numpy as np

class Module():
    def __init__(self, data, labels):
        self.data = data
        self.labels = labels
        self.split = 1.0

    def set_data(self, data, labels):
        self.data = data
        self.labels = labels

    def _splitDataset(self, x, y, train_percent):
        x = np.array(x).astype(np.float32)
        y = np.array(y).astype(np.float32)

        if train_percent != 0:
            length = len(y)
            split = int(length * (train_percent / 100))
            self.dtrain = x[:split]
            self.ltrain = y[:split]
            self.dtest = x[split:]
            self.ltest = y[split:]
        else:
            self.dtrain = x
            self.ltrain = y
            self.dtest = x
            self.ltest = y

    def set_split(self, value):
        self.split = float(value)

    def process(self):
        print("classification process")
        print("Data",self.data)
        print("Label",self.labels)

    def get_results(self):
        print("Getting Result")
        return "Result tes"

    def get_available_settings(self):
        return None

    def set_dataset_params(self, value, option):
        print("value",value)
        print("option",option)
        self.value = value
        self.option = option