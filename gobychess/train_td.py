#!/usr/bin/env python3

"""
Try to implement TD-lambda
"""

import sys

import chess
import h5py
import numpy as np
import tensorflow as tf
from tensorflow.math import log, pow, sigmoid

model = tf.keras.Sequential([
  tf.keras.layers.Dense(100, activation=tf.nn.relu, input_shape=(768,)),  # input shape required
  tf.keras.layers.Dropout(0.1),
  tf.keras.layers.Dense(50, activation=tf.nn.relu),
  tf.keras.layers.Dense(1, activation=tf.keras.activations.tanh)
])

model.summary()

f_data = h5py.File('data/data.h5', 'r')
dset_data = f_data['features']

f_meta = h5py.File('data/meta.h5', 'r')
dset_meta = f_meta['features']

f_val_data = h5py.File('data/test_data.h5', 'r')
dset_val_data = f_val_data['features']

f_val_eval = h5py.File('data/test_eval.h5', 'r')
dset_val_eval = f_val_eval['features']


alpha = 1
td_lambda = 0.3
num_epochs = 30
batch_size = 32
dset_size = 250000

def predict(pmodel, position, training):
    y_position = pmodel(position, training=training)

    return y_position

def grad(pmodel, position):
    with tf.GradientTape() as tape:
        pred = predict(pmodel, position, training=True)
    return tape.gradient(pred, pmodel.trainable_variables)

optimizer = tf.keras.optimizers.SGD(learning_rate=0.00001)

fval = h5py.File('data/test.h5', 'r')
dset_val = fval['features']

for epoch in range(num_epochs):

    grads = [0, 0, 0, 0, 0, 0]
    deltaw = [0, 0, 0, 0, 0, 0]
    games = 0
    avg = 0

    for i in range(dset_size):

        position = np.reshape(dset_data[i, 0, :, :], (1, 768))
        next_position = np.reshape(dset_data[i, 1, :, :], (1, 768))
        last = dset_meta[i, 0]
        result = dset_meta[i, 1]

        V_position = model(position)[0]
        if not last:
            V_next_position = model(next_position)[0]
        else:
            V_next_position = result
            avg += result

        gradients = grad(model, position)

        grads = [grads[i] + gradients[i] for i in range(len(gradients))]
        # deltaw = [deltaw[i] + alpha * (V_next_position - V_position) * grads[i] for i in range(len(gradients))]

        delta = [alpha * (V_next_position - V_position) * grads[i] for i in range(len(gradients))]

        optimizer.apply_gradients(zip(delta, model.trainable_variables))

        grads = [td_lambda * grads[i] for i in range(len(gradients))]

        if last:
            # optimizer.apply_gradients(zip(deltaw, model.trainable_variables))
            # deltaw = [(-1) * deltaw[i] for i in range(len(gradients))]
            # optimizer.apply_gradients(zip(deltaw, model.trainable_variables))
            grads = [0, 0, 0, 0, 0, 0]
            deltaw = [0, 0, 0, 0, 0, 0]
            games += 1
            print(f"Trained {games} games, avg: {avg}", end="\r")

    if epoch % 1 == 0:
        test_pos_0 = model(np.reshape(dset_val_data[1], (1, 768)))
        test_pos_1 = model(np.reshape(dset_val_data[8], (1, 768)))
        test_pos_2 = model(np.reshape(dset_val_data[10], (1, 768)))
        mse = tf.reduce_mean(tf.math.pow(model(np.reshape(dset_val_data, (dset_val_data[:].shape[0], 768))) - dset_val_eval[:], 2))
        print("Epoch {:03d}: mse: {}, Test Pos. 0: {}, Test Pos. -1: {}, Test Pos. +1: {}".format(epoch, mse, test_pos_0, test_pos_1, test_pos_2))
