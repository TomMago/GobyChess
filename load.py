#!/usr/bin/env python3

"""
Create hdf5 dataset from pgn file(s)
"""

import random
import sys

import chess
import h5py
import numpy as np

from gobychess.loader import HDF5Store, Loader

chunk_size = 500
number_games = 4000

l = Loader("data/games.pgn", chunk_size)

shape_data = (3,12,64)
shape_meta = (3,)

hdf5_store_data = HDF5Store('data/data.h5', 'features', shape=shape_data)
hdf5_store_meta = HDF5Store('data/meta.h5', 'features', shape=shape_meta)

for i in range(number_games // chunk_size):
    data, meta = l.generate_triplett_dataset()
    hdf5_store_data.append(np.array(data))
    hdf5_store_meta.append(np.array(meta))
    del data
    del meta

## Test
#f = h5py.File('data/data.h5', 'r')
#dset = f['features']
#
#print(dset.shape)
#
#
#f2 = h5py.File('data/meta.h5', 'r')
#dset2 = f2['features']
#
#print(dset2.shape)
