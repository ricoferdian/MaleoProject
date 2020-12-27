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

# Python libraries
import tempfile
import os
import pickle
import zipfile


class ProjectLoader:
    def __init__(self, data_model, model_results):
        self.path = None
        self.tempdir = None
        self.dataModel = data_model
        self.classifier = model_results.getClassifierModules()
        self.clusterer = model_results.getClustererModules()

    def set_classifier(self, classifier):
        self.classifier = classifier

    def set_clusterer(self, clusterer):
        self.clusterer = clusterer

    def load_project(self, path):
        try:
            self.path = path
            if self.path:
                self._read_zip_file()
        except Exception as e:
            print("Error exception : ", e)

    def _read_zip_file(self):
        archive = zipfile.ZipFile(self.path, "r")
        pickle_dataframe = archive.open("dataframe.pkl")
        data = pickle.load(pickle_dataframe)
        self.dataModel.setData(data)

    def save_project(self, path):
        try:
            self.path = path
            self.tempdir = tempfile.mkdtemp(prefix="maleoProject")

            if self.path:
                self._temp_dataframe()
                self._write_zip_file()

        except Exception as e:
            print("Error exception : ", e)

    def _write_zip_file(self):
        zipf = zipfile.ZipFile(self.path, "w", zipfile.ZIP_DEFLATED)

        for root, dirs, files in os.walk(self.tempdir):
            for file in files:
                zipf.write(os.path.join(root, file), file)

        zipf.close()

    def _temp_dataframe(self):
        if not self.dataModel.isEmpty():
            with open(os.path.join(self.tempdir, "dataframe.pkl"), 'wb') as output:
                pickle.dump(self.dataModel.getData(), output, pickle.HIGHEST_PROTOCOL)
