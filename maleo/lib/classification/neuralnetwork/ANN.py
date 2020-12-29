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

# Python Library
import multiprocessing
import sys

# Third Party Library
import tensorflow as tf

# Inherit NN module
from maleo.lib.classification.neuralnetwork.neural_network import NeuralNetwork

# Biar nggak nyari GPU
tf.config.set_visible_devices([],'GPU')

class ANN(NeuralNetwork):
    def __init__(self, data, labels, *args):
        super(ANN, self).__init__(data, labels)
        self.activationFunction = "relu"
        self.name = "Artificial Neural Network"

    def getName(self):
        return self.name

    def getSupportedOperations(self):
        return "DataType.Numeric", "DataType.Nominal"

    def getUnsupportedOperations(self):
        return None

    def getAvailableSettings(self):
        return {
                "setActivationFunction":{
                    "name":"Fungsi Aktivasi Hidden Layer",
                    "params":{
                        "param1":{
                                "type":"DataType.DropDown",
                                "options":["relu","sigmoid","hard_sigmoid","elu","tanh","softplus","softmax"]
                            }
                        }
                    },
                "setNumEpochs":{
                    "name":"Jumlah Epochs",
                    "params":{
                        "param1":{
                                "type":"DataType.NumericInput",
                                "default":100
                            }
                        }
                    },
                "setBatchSize":{
                    "name":"Ukuran Batch",
                    "params":{
                        "param1":{
                                "type":"DataType.NumericInput",
                                "default":128
                            }
                        }
                    }
                }

    def setActivationFunction(self, param1=None):
        self.activationFunction = param1

    def setNumEpochs(self, param1=None):
        try:
            self.numEpochs = int(param1)
        except Exception as e:
            print(e)

    def setBatchSize(self, param1=None):
        try:
            self.batchSize = int(param1)
        except Exception as e:
            print(e)

    def startOperation(self):
        try:
            self.proc = multiprocessing.Process(target=self.train(), args=())
            self.proc.start()
        except Exception as e:
            print(e)

    def stopOperation(self):
        print("Artificial Neural Network with Tensorflow stopped")
        sys.stdout = self.originalStdOut
        try:
            self.proc.terminate()
        except Exception as e:
            print(e)

    def setOutputWidget(self, output):
        self.outputWidget = output

    def train(self):
        self.originalStdOut = sys.stdout
        sys.stdout = self.outputWidget

        print("Artificial Neural Network with Tensorflow")
        print("Activation Function :",self.activationFunction)
        print("Num of Epochs :",self.numEpochs)
        print("Batch Size :",self.batchSize)

        print("Dataset :",self.data)
        print("Labels :",self.labels)

        out = self.labels.nunique()

        self.preprocessData()

        self.ltrain = tf.keras.utils.to_categorical(self.ltrain, out)
        self.ltest = tf.keras.utils.to_categorical(self.ltest, out)

        self.model = tf.keras.models.Sequential([
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(out*2, activation=self.activationFunction),
            tf.keras.layers.Dense(out)
        ])

        self.model.compile(loss=tf.keras.losses.CategoricalCrossentropy(from_logits=True),
                      optimizer='adam',
                      metrics=['acc'])

        self.history = self.model.fit(x=self.dtrain,y=self.ltrain,epochs=self.numEpochs,batch_size=self.batchSize,validation_data=(self.dtest,self.ltest), verbose=1)

        self.model.summary()
        self.stopOperation()