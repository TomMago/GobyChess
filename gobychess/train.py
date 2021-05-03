#!/usr/bin/env python3
import sys

import chess
import h5py
import numpy as np
import tensorflow as tf
from tensorflow.math import log, sigmoid, pow


model = tf.keras.Sequential([
  tf.keras.layers.Dense(100, activation=tf.nn.relu, input_shape=(768,)),  # input shape required
  tf.keras.layers.Dense(50, activation=tf.nn.relu),
  tf.keras.layers.Dense(1)
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

batch_size = 32
num_batches = dset_data.shape[0] // batch_size
training_samples = num_batches * batch_size
kappa = 10

def loss(pmodel, pposition, pnext_position, prandom_position, last, result, to_move, training):

    y_position = pmodel(pposition, training=training)
    y_next_position = pmodel(pnext_position, training=training)
    y_random_position = pmodel(prandom_position, training=training)
    last = tf.cast(last, dtype=bool)

    y_next_position = tf.where(tf.reshape(last, [32,1]),
                               tf.reshape(result, [32,1]),
                               tf.reshape(y_next_position, [32, 1]))

    return -(tf.reduce_mean(log(sigmoid(tf.cast(tf.reshape(tf.math.pow(-1, to_move), [32, 1]), dtype=tf.float32) * (y_random_position - y_next_position)))
                            + kappa * log(sigmoid(- y_position + y_next_position))
                            + kappa * log(sigmoid(y_position - y_next_position))))


def grad(pmodel, pposition, pnext_position, prandom_position, last, result, to_move):
    with tf.GradientTape() as tape:
        loss_val = loss(pmodel, pposition, pnext_position, prandom_position, last, result, to_move, training=True)
    return loss_val, tape.gradient(loss_val, pmodel.trainable_variables)


optimizer = tf.keras.optimizers.SGD(learning_rate=0.01)


# # Keep results for plotting
train_loss_results = []
train_accuracy_results = []

num_epochs = 30

fval = h5py.File('data/test.h5', 'r')
dset_val = fval['features']

for epoch in range(num_epochs):
    epoch_loss_avg = tf.keras.metrics.Mean()

    for i in range(num_batches):


        print(f"Batch: {i}", end="\r")
        position = np.reshape(dset_data[i:i+batch_size, 0, :, :], (batch_size, 768))
        next_position = np.reshape(dset_data[i:i+batch_size, 1, :, :], (batch_size, 768))
        random_position = np.reshape(dset_data[i:i+batch_size, 2, :, :], (batch_size, 768))
        last = dset_meta[i:i+batch_size, 0]
        result = dset_meta[i:i+batch_size, 1]
        to_move = dset_meta[i:i+batch_size, 2]

        loss_value, grads = grad(model, position, next_position, random_position, last, result, to_move)


        epoch_loss_avg.update_state(loss_value)  # Add current batch loss

        optimizer.apply_gradients(zip(grads, model.trainable_variables))

        #print(f"Trained {num_game} games", end="\r")

    # End epoch
    train_loss_results.append(epoch_loss_avg.result())

    if epoch % 1 == 0:
        mse = tf.reduce_mean(tf.math.pow(model(np.reshape(dset_val_data, (dset_val_data[:].shape[0], 768))) - dset_val_eval[:], 2))
        print("Epoch {:03d}: Loss: {:.3f}: mse: {}".format(epoch, epoch_loss_avg.result(), mse))
