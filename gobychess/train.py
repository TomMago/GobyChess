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

#print(dset[0][0].shape)
#print(np.reshape(dset[0][0], (1,768)).shape)
#print(model(np.reshape(dset[0][0], (1,768))))

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

#data = np.array(dset[:])

def loss(pmodel, pposition, pnext_position, prandom_position, last, result, to_move, training):
    # training=training is needed only if there are layers with different
    # behavior during training versus inference (e.g. Dropout).
    y_position = pmodel(pposition, training=training)
    y_next_position = pmodel(pnext_position, training=training)
    y_random_position = pmodel(prandom_position, training=training)

    last = tf.cast(last, dtype=bool)

    y_next_position = tf.where(tf.reshape(last, [32,1]),
                               tf.reshape(result, [32,1]),
                               tf.reshape(y_next_position, [32, 1]))


    #print("______________________________")
    #print((y_random_position - y_next_position))
    #print("============================")
    #print(log(sigmoid(tf.math.pow(-1, to_move) * (y_random_position - y_next_position))))

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
    #epoch_accuracy = tf.keras.metrics.SparseCategoricalAccuracy()

    #for i in range(num_batches):
    for i in range(1):


    # Training loop - using batches of 32

        print(f"Batch: {i}", end="\r")
        position = np.reshape(dset_data[i:i+batch_size, 0, :, :], (batch_size, 768))
        next_position = np.reshape(dset_data[i:i+batch_size, 1, :, :], (batch_size, 768))
        random_position = np.reshape(dset_data[i:i+batch_size, 2, :, :], (batch_size, 768))
        last = dset_meta[i:i+batch_size, 0]
        result = dset_meta[i:i+batch_size, 1]
        to_move = dset_meta[i:i+batch_size, 2]

        loss_value, grads = grad(model, position, next_position, random_position, last, result, to_move)

        # Track progress
        epoch_loss_avg.update_state(loss_value)  # Add current batch loss
        # Compare predicted label to actual label
        # training=True is needed only if there are layers with different
        # behavior during training versus inference (e.g. Dropout).
        #epoch_accuracy.update_state(y, model(x, training=True))

        optimizer.apply_gradients(zip(grads, model.trainable_variables))

        #print(f"Trained {num_game} games", end="\r")
        # End epoch
    train_loss_results.append(epoch_loss_avg.result())
        #train_accuracy_results.append(epoch_accuracy.result())

    if epoch % 1 == 0:
        mse = tf.reduce_mean(tf.math.pow(model(np.reshape(dset_val_data, (dset_val_data[:].shape[0], 768))) - dset_val_eval[:], 2))
        print("Epoch {:03d}: Loss: {:.3f}: mse: {}".format(epoch, epoch_loss_avg.result(), mse))



#print(dset[0][0].shape)
#print(np.reshape(dset[0][0], (1,768)).shape)

print(model(np.reshape(dset_val[0], (1, 768))))
print()
print(model(np.reshape(dset_val[1], (1, 768))))
print()
print(model(np.reshape(dset_val[2], (1, 768))))
print()
print(model(np.reshape(dset_val[3], (1, 768))))
