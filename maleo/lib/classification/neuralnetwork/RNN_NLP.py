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
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np

# Inherit
from maleo.lib.classification.neuralnetwork.neural_network import NeuralNetwork

class RNN_NLP(NeuralNetwork):
    def __init__(self, data, labels, *args):
        super(RNN_NLP, self).__init__(data, labels)
        self.activationFunction = "relu"
        self.name = "Recurrent Neural Network for Natural Language Processing"
        self.set_nlp_params()

    def set_nlp_params(self):
        self.vocab_size = 1000
        self.embedding_dim = 16
        self.max_length = 120
        self.trunc_type = 'post'
        self.padding_type = 'post'
        self.oov_tok = "<OOV>"
        self.training_size = 20000

        self.sentences = self.data
        self.labels = []

    def get_available_settings(self):
        return {
            "setVocabSize": {
                "name": "Ukuran Vocab",
                "params": {
                    "param1": {
                        "type": "DataType.NumericInput",
                        "default": self.vocab_size
                    }
                }
            },
            "setEmbeddingDim": {
                "name": "Embedding Dims",
                "params": {
                    "param1": {
                        "type": "DataType.NumericInput",
                        "default": self.embedding_dim
                    }
                }
            },
            "setMaxLength": {
                "name": "Panjang Karakter",
                "params": {
                    "param1": {
                        "type": "DataType.NumericInput",
                        "default": self.max_length
                    }
                }
            },
            "setTrainingSize": {
                "name": "Ukuran Data Training",
                "params": {
                    "param1": {
                        "type": "DataType.NumericInput",
                        "default": self.training_size
                    }
                }
            },
            "setTruncType": {
                "name": "Tipe Truncation",
                "params": {
                    "param1": {
                        "type": "DataType.DropDown",
                        "options": ["post", "pre"]
                    }
                }
            },
            "setPaddingType": {
                "name": "Tipe Padding",
                "params": {
                    "param1": {
                        "type": "DataType.DropDown",
                        "options": ["post", "pre"]
                    }
                }
            },
            "set_activation_function": {
                "name": "Fungsi Aktivasi",
                "params": {
                    "param1": {
                        "type": "DataType.DropDown",
                        "options": ["sigmoid", "relu"]
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

    def setVocabSize(self, param1=None):
        try:
            self.vocab_size = int(param1)
        except Exception as e:
            print(e)

    def setEmbeddingDim(self, param1=None):
        try:
            self.embedding_dim = int(param1)
        except Exception as e:
            print(e)

    def setMaxLength(self, param1=None):
        try:
            self.max_length = int(param1)
        except Exception as e:
            print(e)

    def setTrainingSize(self, param1=None):
        try:
            self.training_size = int(param1)
        except Exception as e:
            print(e)

    def setTruncType(self, param1=None):
        try:
            self.trunc_type = param1
        except Exception as e:
            print(e)

    def setPaddingType(self, param1=None):
        try:
            self.padding_type = param1
        except Exception as e:
            print(e)

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

    def get_name(self):
        return self.name

    def get_supported_operations(self):
        return "DataType.Numeric", "DataType.Nominal"

    def get_unsupported_operations(self):
        return None

    def set_activation_function(self, param1=None):
        self.activationFunction = param1

    def start_operation(self):
        try:
            self.proc = multiprocessing.Process(target=self.train(), args=())
            self.proc.start()
        except Exception as e:
            print(e)

    def stop_operation(self):
        print("Recurrent Neural Network for Natural Language Processing with Tensorflow stopped")
        sys.stdout = self.originalStdOut
        try:
            self.proc.terminate()
        except Exception as e:
            print(e)

    def set_output_widget(self, output):
        print("Output widget set",output)
        self.outputWidget = output

    def get_sentences(self):
        self.sentences = np.array([])
        for colname in self.data:
            data = self.data[colname].to_numpy()
            self.sentences = np.concatenate((self.sentences, data), axis=0)

    def preprocess_nlp(self):
        print("Preprocessing data")
        self.get_sentences()
        training_sentences = self.sentences[:self.training_size]
        training_labels = self.labels[:self.training_size]

        testing_sentences = self.sentences[self.training_size:]
        testing_labels = self.labels[self.training_size:]

        self.training_labels_final = np.array(training_labels)
        self.testing_labels_final = np.array(testing_labels)

        tokenizer = Tokenizer(num_words=self.vocab_size, oov_token=self.oov_tok)
        tokenizer.fit_on_texts(self.sentences)
        word_index = tokenizer.word_index

        self.train_sequences = tokenizer.texts_to_sequences(training_sentences)
        self.train_padded = pad_sequences(self.train_sequences, padding=self.padding_type, maxlen=self.max_length, truncating=self.trunc_type)

        self.validation_sequences = tokenizer.texts_to_sequences(testing_sentences)
        self.validation_padded = pad_sequences(self.validation_sequences, padding=self.padding_type, maxlen=self.max_length,
                                          truncating=self.trunc_type)

    def train(self):
        self.originalStdOut = sys.stdout
        sys.stdout = self.outputWidget

        print("Recurrent Neural Network for Natural Language Processing with Tensorflow")
        print("Activation Function :",self.activationFunction)
        print("Vocan Size :",self.vocab_size)
        print("Embedding Dims :",self.embedding_dim)
        print("Max Length :",self.max_length)
        print("Truncation Type :",self.trunc_type)
        print("Padding Type :",self.padding_type)
        print("Training Size :",self.training_size)
        print("Num of Epochs :",self.numEpochs)
        print("Batch Size :",self.batchSize)

        print("Dataset :",self.data)
        print("Labels :",self.labels)

        out = self.labels.nunique()
        print("Unique labels : ",out)
        if out==2:
            out = 1

        self.preprocess_nlp()

        # self.ltrain = tf.keras.utils.to_categorical(self.ltrain, out)
        # self.ltest = tf.keras.utils.to_categorical(self.ltest, out)

        print("self.train_padded",self.train_padded)
        print("self.training_labels_final",self.training_labels_final)
        print("self.validation_padded",self.validation_padded)
        print("self.testing_labels_final",self.testing_labels_final)

        self.model = tf.keras.Sequential([
            tf.keras.layers.Embedding(self.vocab_size, self.embedding_dim, input_length=self.max_length),
            tf.keras.layers.Bidirectional(tf.keras.layers.GRU(32)),
            tf.keras.layers.Dense(20, activation=self.activationFunction),
            tf.keras.layers.Dense(10, activation=self.activationFunction),
            tf.keras.layers.Dense(out)
        ])

        self.model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['acc'])
        # self.model.compile(loss=tf.keras.losses.CategoricalCrossentropy(from_logits=True),
        #               optimizer='adam',
        #               metrics=['acc'])
        self.history = self.model.fit(self.train_padded, self.training_labels_final, epochs=self.numEpochs,batch_size=self.batchSize,
                            validation_data=(self.validation_padded, self.testing_labels_final),verbose=1)
        self.model.summary()
        self.stop_operation()
