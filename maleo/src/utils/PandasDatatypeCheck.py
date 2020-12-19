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

import pandas as pd
from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype
from enum import Enum

class PandasDatatypeCheck():
    def __init__(self, *args):
        self.datatypes = Enum("DataType","Numeric Nominal Unknown")

    def setDataType(self, value):
        self.value = value

    def getType(self):
        return self.datatypes

    def getDataType(self):
        if(is_numeric_dtype(self.value)):
            return self.datatypes.Numeric
        elif(is_string_dtype(self.value)):
            return self.datatypes.Nominal
        else:
            return self.datatypes.Unknown
