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

class ClassifierModel():
    def __init__(self,classifier, *args):
        self.classifier = classifier

    def set_module(self, classifier):
        self.classifier = classifier

    def get_name(self):
        return self.classifier.get_name()

    def save_to_path(self, path):
        self.classifier.save_to_path(path)

    def get_model(self):
        return self.classifier

    def get_history(self):
        return self.classifier.get_history()

    def start(self):
        self.classifier.start_operation()

    def stop(self):
        self.classifier.stop_operation()