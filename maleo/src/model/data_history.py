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

# Python library
from collections import deque


class DataHistory():
    def __init__(self, *args):
        self.dataStack = deque()

    def append_data(self, data):
        self.dataStack.append(data)

    def pop_data(self):
        return self.dataStack.pop()

    def is_empty(self):
        if self.dataStack:
            return False
        return True

    def get_data(self):
        return self.dataStack
