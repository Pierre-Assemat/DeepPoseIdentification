# -*- coding: utf-8 -*-

import tflearn
import pickle
import pandas as pd
import numpy as np

from __future__ import division, print_function, absolute_import
from sklearn.model_selection import train_test_split


class Training():

    def __init__(self, data):
        # Data loading and preprocessing
        if (data):
            dataset = data
        else:
            dataset = pd.read_pickle('data.pkl')
        # Remove extra data in dataset such as "source"
        # TODO: Update it with new column images size
        self.X = np.array(dataset)[:, :-4]
        self.y = np.array(dataset)[:, -1]

    def buildNN(hiddenLayerNumber=2):
        # Building deep neural network
        input_layer = tflearn.input_data(shape=[None, 54])
        dense = tflearn.fully_connected(input_layer, 54, activation='relu',
                                        regularizer='L2', weight_decay=0.001)
        for i in range(hiddenLayerNumber):
            dropout = tflearn.dropout(dense, 0.8)
            dense = tflearn.fully_connected(dropout, 54, activation='relu',
                                            regularizer='L2', weight_decay=0.001)

        dropout = tflearn.dropout(dense, 0.8)
        softmax = tflearn.fully_connected(dropout, 2, activation='softmax')

        # Regression using SGD with learning rate decay and Top-3 accuracy
        sgd = tflearn.SGD(learning_rate=0.1, lr_decay=0.96, decay_step=1000)
        top_k = tflearn.metrics.Top_k(1)
        net = tflearn.regression(softmax, optimizer=sgd, metric=top_k,
                                loss='categorical_crossentropy')
        return net

    def train(net):
        #split data between train and test
        X, testX, Y, testY = train_test_split(self.X, self.y, test_size=.2, random_state=42)
        Y = np.array(pd.get_dummies(Y))
        testY = np.array(pd.get_dummies(testY))

        # Training
        model = tflearn.DNN(net, tensorboard_verbose=0)
        model.fit(self.X, self.Y, n_epoch=20, validation_set=(self.testX, self.testY), show_metric=True, run_id="dense_model")

