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
tf.config.set_visible_devices([], 'GPU')

CONST_LAYERS = ["flatten", "dense"]


class ANN(NeuralNetwork):
    def __init__(self, data, labels, *args):
        super(ANN, self).__init__(data, labels)
        self.name = "Artificial Neural Network"
        self.optimizer = "adam"
        self.networks = [{
            "editable": False,
            "layer": "flatten",
            "units": None,
            "activation": None,
            "type": "InputLayer"
        }, {
            "editable": True,
            "layer": "dense",
            "units": 128,
            "activation": "relu"
        }, {
            "editable": False,
            "layer": "dense",
            "units": "auto",
            "activation": None,
            "type": "OutputLayer"
        }]
        self.model = tf.keras.Sequential()

    def get_name(self):
        return self.name

    def get_supported_operations(self):
        return "DataType.Numeric", "DataType.Nominal"

    def get_unsupported_operations(self):
        return None

    def get_available_settings(self):
        return {
            "set_num_epochs": {
                "name": "Jumlah Epochs",
                "params": {
                    "param1": {
                        "type": "DataType.NumericInput",
                        "default": 100
                    }
                }
            },
            "set_batch_size": {
                "name": "Ukuran Batch",
                "params": {
                    "param1": {
                        "type": "DataType.NumericInput",
                        "default": 128
                    }
                }
            },
            "set_optimizer": {
                "name": "Optimizer",
                "params": {
                    "param1": {
                        "type": "DataType.DropDown",
                        "options": [
                            "adam",
                            "adagrad",
                            "sgd",
                            "rmsprop",
                            "adamax",
                            "ftrl",
                            "nadam"
                        ]
                    }
                }
            },
            "set_neural_network": {
                "name": "Network Builder",
                "params": {
                    "param1": {
                        "type": "DataType.NetworkBuilder",
                        "networks": self.networks,
                        "layers": [
                            "flatten",
                            "dense",
                            "lstm",
                            "lstm_cell",
                            "gru",
                            "gru_cell",
                            "simple_rnn",
                            "simple_rnn_cell"
                        ],
                        "activations": [
                            "default",
                            tf.keras.activations.serialize(tf.keras.activations.sigmoid),
                            tf.keras.activations.serialize(tf.keras.activations.relu),
                            tf.keras.activations.serialize(tf.keras.activations.selu),
                            tf.keras.activations.serialize(tf.keras.activations.elu),
                            tf.keras.activations.serialize(tf.keras.activations.exponential),
                            tf.keras.activations.serialize(tf.keras.activations.hard_sigmoid),
                            tf.keras.activations.serialize(tf.keras.activations.linear),
                            tf.keras.activations.serialize(tf.keras.activations.softmax),
                            tf.keras.activations.serialize(tf.keras.activations.softsign),
                            tf.keras.activations.serialize(tf.keras.activations.softplus),
                            tf.keras.activations.serialize(tf.keras.activations.tanh)
                        ]
                    }
                }
            }
        }

    def set_optimizer(self, param1=None):
        try:
            self.optimizer = param1
        except Exception as e:
            print(e)

    def set_neural_network(self, param1=None):
        try:
            print("NN Params", param1)
            self.networks = param1
        except Exception as e:
            print(e)

    def set_num_epochs(self, param1=None):
        try:
            self.numEpochs = int(param1)
        except Exception as e:
            print(e)

    def set_batch_size(self, param1=None):
        try:
            self.batchSize = int(param1)
        except Exception as e:
            print(e)

    def start_operation(self):
        try:
            self.proc = multiprocessing.Process(target=self.train(), args=())
            self.proc.start()
        except Exception as e:
            print(e)

    def stop_operation(self):
        print("Artificial Neural Network with Tensorflow stopped")
        sys.stdout = self.originalStdOut
        try:
            self.proc.terminate()
        except Exception as e:
            print(e)

    def set_output_widget(self, output):
        self.outputWidget = output

    def build_model(self, layer_str, activation, units, length, index, out):
        if layer_str is None:
            layer_str = "dense"
        if activation is None:
            activation = "relu"
        if units is None:
            units = out

        self.model = tf.keras.Sequential()
        if index == 0:
            self.model.add(tf.keras.layers.Flatten())
        elif index == length - 1:
            self.model.add(tf.keras.layers.Dense(units=out))
        else:
            if layer_str == "dense":
                self.model.add(tf.keras.layers.Dense(units=units, activation=activation))
            elif layer_str == "flatten":
                self.model.add(tf.keras.layers.Flatten())
            elif layer_str == "lstm":
                self.model.add(tf.keras.layers.LSTM(units=units, activation=activation))
            elif layer_str == "lstm_cell":
                self.model.add(tf.keras.layers.LSTMCell(units=units, activation=activation))
            elif layer_str == "gru":
                self.model.add(tf.keras.layers.GRU(units=units, activation=activation))
            elif layer_str == "gru_cell":
                self.model.add(tf.keras.layers.GRUCell(units=units, activation=activation))
            elif layer_str == "simple_rnn":
                self.model.add(tf.keras.layers.SimpleRNN(units=units, activation=activation))
            elif layer_str == "simple_rnn_cell":
                self.model.add(tf.keras.layers.SimpleRNNCell(units=units, activation=activation))

    def train(self):
        self.originalStdOut = sys.stdout
        sys.stdout = self.outputWidget

        print("Artificial Neural Network with Tensorflow")
        print("Networks :", self.networks)
        print("Num of Epochs :", self.numEpochs)
        print("Batch Size :", self.batchSize)
        print("Dataset :", self.data)
        print("Labels :", self.labels)

        out = self.labels.nunique()
        print("Unique Labels :", out)

        print("Building network...")
        try:
            for index, network in enumerate(self.networks):
                layer = network["layer"]
                activation = network["activation"]
                units = network["units"]
                if units is not None and units != "":
                    units = int(units)
                else:
                    units = 1
                self.build_model(layer, activation, units, len(self.networks), index, out)
        except Exception as e:
            print("Error exception", e)

        print("Model Layers :", self.model.layers)

        self.preprocess_data()

        self.ltrain = tf.keras.utils.to_categorical(self.ltrain, out)
        self.ltest = tf.keras.utils.to_categorical(self.ltest, out)

        # self.model = tf.keras.models.Sequential([
        #     tf.keras.layers.Flatten(),
        #     tf.keras.layers.Dense(out * 2, activation='relu'),
        #     tf.keras.layers.Dense(out)
        # ])

        self.model.compile(loss=tf.keras.losses.CategoricalCrossentropy(from_logits=True),
                           optimizer=self.optimizer,
                           metrics=['acc'])

        self.history = self.model.fit(x=self.dtrain, y=self.ltrain, epochs=self.numEpochs, batch_size=self.batchSize,
                                      validation_data=(self.dtest, self.ltest), verbose=1)

        # print("Model Summary :")
        self.model.summary()
        # print("Model Weights :", self.model.weights)
        self.stop_operation()
