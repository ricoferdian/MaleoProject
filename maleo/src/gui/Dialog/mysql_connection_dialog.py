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

# Classifier Module Library
from maleo.src.utils.datasetloader.mysql_loader import MysqlLoader


class MysqlConnectionDialog(QDialog):
    def __init__(self, parent, data_model):
        super(QDialog, self).__init__(parent)
        self.dataModel = data_model
        self.dataLoader = MysqlLoader()

        self.layout = QVBoxLayout()
        self.formLayout = QHBoxLayout()
        self.leftLayout = QVBoxLayout()
        self.rightLayout = QVBoxLayout()

        self.usernameLabel = QLabel("Username")
        self.passwordLabel = QLabel("Password")
        self.hostLabel = QLabel("Host")
        self.databaseLabel = QLabel("Database")
        self.queryLabel = QLabel("Query")

        self.leftLayout.addWidget(self.usernameLabel)
        self.leftLayout.addWidget(self.passwordLabel)
        self.leftLayout.addWidget(self.hostLabel)
        self.leftLayout.addWidget(self.databaseLabel)
        self.leftLayout.addWidget(self.queryLabel)

        self.username = QLineEdit("root")
        self.password = QLineEdit("")
        self.password.setEchoMode(QLineEdit.EchoMode.PasswordEchoOnEdit)
        self.host = QLineEdit("localhost")
        self.database = QLineEdit("*")
        self.query = QLineEdit()

        self.rightLayout.addWidget(self.username)
        self.rightLayout.addWidget(self.password)
        self.rightLayout.addWidget(self.host)
        self.rightLayout.addWidget(self.database)
        self.rightLayout.addWidget(self.query)

        self.formLayout.addLayout(self.leftLayout)
        self.formLayout.addLayout(self.rightLayout)

        self.connectButton = QPushButton("Connect")
        self.connectButton.clicked.connect(self.on_connect)
        self.closeButton = QPushButton("Close")
        self.closeButton.clicked.connect(self.on_ok)

        self.layout.addLayout(self.formLayout)
        self.layout.addWidget(self.connectButton)
        self.layout.addWidget(self.closeButton)

        self.setMinimumSize(400,200)
        self.setLayout(self.layout)

    def on_connect(self):
        username = self.username.text()
        password = self.password.text()
        host = self.host.text()
        database = self.database.text()
        query = self.query.text()

        self.dataLoader.setConnection(username, password, host, database)
        self.dataLoader.loadData(query)

        self.dataModel.set_data(self.dataLoader.getData())
        self.parent().parent().data_loaded()
        self.close()

    def on_ok(self):
        self.close()
