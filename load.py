#!/usr/bin/env python3

import random

import chess
import numpy as np

from gobychess.loader import Loader, HDF5Store
import h5py

import sys



#print(np.array(l.features_from_board(chess.pgn.read_game(l.pgn).board())).shape)
#print(np.array(l.features_from_game(chess.pgn.read_game(l.pgn))).shape)

#print(np.array(l.generate_triplett_dataset()).shape)


# test


#print(np.array(data).shape)
#print(np.array(meta).shape)

chunk_size = 500
number_games = 4000

l = Loader("data/games.pgn", chunk_size)

#shape_data = (3,12,64)
#shape_meta = (3,)
#
#hdf5_store_data = HDF5Store('data/data.h5', 'features', shape=shape_data)
#hdf5_store_meta = HDF5Store('data/meta.h5', 'features', shape=shape_meta)
#
##from guppy import hpy
##h=hpy()
#
#
#for i in range(number_games // chunk_size):
#    data, meta = l.generate_triplett_dataset()
#    hdf5_store_data.append(np.array(data))
#    hdf5_store_meta.append(np.array(meta))
#    del data
#    del meta

x = np.array([l.features_from_board(chess.Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")),
              l.features_from_board(chess.Board("rnbk1b1r/ppp2ppp/4pN2/8/8/8/PPPP1PPP/R1BQKBNR w KQ - 1 6")),
              l.features_from_board(chess.Board("rnbqkbnr/ppp3pp/4Pp2/8/8/8/PPPP1PPP/RNBQKBNR w KQkq - 0 4")),
              l.features_from_board(chess.Board("r1bqkbnr/pppp1ppp/n7/4p3/4P3/8/PPPP1PPP/RNBQK1NR w KQkq - 0 3"))])#

shape = (12,64)
hdf5_store = HDF5Store('data/test.h5', 'features', shape=shape)
hdf5_store.append(x)

f = h5py.File('data/test.h5', 'r')
dset = f['features']
print(dset[:].shape)


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
