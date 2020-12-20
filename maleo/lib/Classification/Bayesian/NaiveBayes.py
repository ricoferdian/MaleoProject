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

# Inherit
from maleo.lib.Module import Module

class NaiveBayes(Module):
    def __init__(self, data, labels, *args):
        super(NaiveBayes, self).__init__(data, labels)

    def getAvailableSettings(self):
        return {
                "setParamOne":{
                    "name":"Sensitivitas",
                    "params":{
                        "param1":{
                                "type":"DataType.NumericInput",
                                "default":0.5
                            }
                        }
                    },
                "setParamTwo":{
                    "name":"Threshold",
                    "params":{
                        "param1":{
                                "type":"DataType.NumericSlider",
                                "min":10,
                                "max":20
                            }
                        }
                    },
                "setParamThree":{
                    "name":"Data Numerik ?",
                    "params":{
                        "param1":{
                                "type":"DataType.BooleanDropDown",
                            }
                        }
                    }
                }

    def setParamOne(self, param1=None):
        print("data",self.data)
        print("labels",self.labels)
        print("Bayes Set Param One")
        print("param1",param1)

    def setParamTwo(self, param1=None):
        print("Bayes Set Param One")
        print("param1",param1)

    def setParamThree(self, param1=None):
        print("Bayes Set Param One")
        print("param1",param1)