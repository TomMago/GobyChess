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
#pgn = open("data/games.pgn")
#for _ in range(100000):
#    game = chess.pgn.read_game(pgn)
#    if 'Variant' in game.headers:
#        print(game.headers['Variant'])


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
              l.features_from_board(chess.Board("r1bqkb1r/pppp1ppp/2n2n2/1B2p3/4P3/5N2/PPPP1PPP/RNBQ1RK1 b kq - 5 4")),
              l.features_from_board(chess.Board("r1bqk2r/ppppbppp/5n2/1B2R3/8/8/PPPP1PPP/RNBQ2K1 w kq - 1 8")),
              l.features_from_board(chess.Board("r1bqkb1r/pppp2pp/8/1B2np2/4n3/2N5/PPPP1PPP/R1BQR1K1 b kq - 1 7")),
              l.features_from_board(chess.Board("r1bqkb1r/pppp1ppp/5n2/4n3/4P3/2N5/PPPP1PPP/R1BQKB1R w KQkq - 0 5")),
              l.features_from_board(chess.Board("r1bqkbnr/pp1ppp1p/2n3p1/1Bp5/4P3/2N5/PPPP1PPP/R1BQK1NR w KQkq - 0 4")),
              l.features_from_board(chess.Board("r1bq1rk1/p2pppbp/2p3p1/4P3/3P4/5N2/P1P2PPP/R1BQ1RK1 w - - 1 11")),
              l.features_from_board(chess.Board("r1bq1r2/3pp1bk/2p3pp/p3Pp2/2QP4/B4N2/P1P2PPP/1R2R1K1 b - - 1 15")),
              l.features_from_board(chess.Board("r2q1r2/3pp1bk/2p3pp/p3Pp2/2bP3P/B4N2/P1P2PP1/1R2R1K1 w - - 0 17")),
              l.features_from_board(chess.Board("r1b2r2/3pp1bk/1pp3pp/4Pp2/2QP4/5N2/P1P2PPP/2B1R1K1 w - - 0 16")),
              l.features_from_board(chess.Board("r2k1b1r/pbpp2p1/1n5p/n3p2Q/4P3/8/PPPP1PPP/RNB1K2R w KQ - 2 10")),
              l.features_from_board(chess.Board("r1bq1rk1/p1p3pp/2pb1p2/3pn3/1P6/P1NB2B1/2P2PPP/R2QR1K1 b - - 2 14")),
              l.features_from_board(chess.Board("r1bq1rk1/p1pp1ppp/2p2n2/2B5/4P3/2N5/PPP2PPP/R2QKB1R b KQ - 0 8")),
              l.features_from_board(chess.Board("2kr2nr/pppb1pbp/2np4/8/3PP1q1/2N3B1/PPP1BQPP/3R1RK1 b - - 12 13")),
              l.features_from_board(chess.Board("r4rk1/1ppb1pq1/3p4/p5pp/P1BPPn2/6NP/1P3PP1/R2QR1K1 b - - 2 22")),
              l.features_from_board(chess.Board("rn1qkb1r/ppp2ppp/4pn2/5bN1/2B1p3/2N5/PPPPQPPP/R1B1K2R b KQkq - 1 6")),
              l.features_from_board(chess.Board("r1b1Bb1r/ppp1p1pp/2n1kn2/8/4p3/8/PPPP1PPP/RNBQK2R w KQ - 0 8")),
              l.features_from_board(chess.Board("r1b1kbnr/ppppqppp/2n5/4P3/5B2/5N2/PPP1PPPP/RN1QKB1R b KQkq - 4 4")),
              l.features_from_board(chess.Board("N1bk1bnr/pp1p1ppp/8/3qn3/8/5N2/PPP1PPPP/R3KB1R w KQ - 0 10")),
              l.features_from_board(chess.Board("r2q1rk1/p6p/2Qbp3/5pp1/8/2P2N2/P2P1PPP/R1B2RK1 b - - 0 15")),
              l.features_from_board(chess.Board("r3kb1r/pp1q1ppp/2n1pP2/1B1p4/6Q1/2N2N2/PPP2PPP/R1B2RK1 b kq - 0 10")),
              l.features_from_board(chess.Board("r2qkb1r/ppp1nppp/2n1p3/4P3/2Pp3P/5P2/PPQ2P2/RNB1K2R b KQkq - 0 10")),
              l.features_from_board(chess.Board("rn2k2r/1p3ppp/p7/2p5/6b1/1P2PN2/P1PQB1PP/q3K2R w Kkq - 0 13")),
              l.features_from_board(chess.Board("r1bqk1nr/p1p2ppp/2p5/2p5/4P3/8/PPP2PPP/RN1QKB1R w KQkq - 0 8")),
              l.features_from_board(chess.Board("r1bqkb1r/ppp2ppp/2n2n2/3pp2P/8/P2P1N2/1PP2PP1/RNBQKB1R w KQkq - 0 7")),
              l.features_from_board(chess.Board("rnbqk2r/ppppnppp/8/4N3/4P3/N7/PPPP1PPP/R1BQKB1R b KQkq - 0 4")),
              l.features_from_board(chess.Board("r1b1kb1r/pp1p1ppp/P1n1pn2/q1p5/4P3/8/1PPP1PPP/1NBQKBNR w Kkq - 0 6")),
              l.features_from_board(chess.Board("4k3/p1r4p/1p4p1/8/8/4P1P1/1P1RN2P/3K4 w - - 0 1")),
              l.features_from_board(chess.Board("2k5/6qp/1p4p1/8/r6P/4P1P1/1P1RN1K1/8 w - - 0 1")),
              l.features_from_board(chess.Board("4k3/2np1p2/2n3p1/8/2P5/6P1/1P1B1B2/3K4 w - - 0 1")),
              l.features_from_board(chess.Board("r3k3/3p1p2/4nn2/6p1/2P5/1P4P1/2BB4/4K3 w - - 0 1")),
              l.features_from_board(chess.Board("r4r1k/p1p1q1pp/1pbp1n2/5b2/2BQ4/2N1B3/1PP3PP/2KR3R w Kq - 0 1")),
              l.features_from_board(chess.Board("r2q1rk1/3bppbp/p1np1np1/1pp5/4P3/PBNP1N1P/1PP2PP1/R1B1QRK1 w - - 1 12")) ])

y = np.array([0, 0, 0, -3, -2, 0, 0, 1, -12, 6, 7.2, -0.9, 4.9, -1.7, 0.5, -1.1, 9, 1.3, -12, 5, 8, -8, -7.8, 2.7, -2.4, +6, -7.5, +5, -6, +0.8, -6, -2.7, 0])
y = np.reshape(y, [33,1])

shape = (12,64)
hdf5_store = HDF5Store('data/test_data.h5', 'features', shape=shape)
hdf5_store.append(x)

shape = (1,)
hdf5_store2 = HDF5Store('data/test_eval.h5', 'features', shape=shape)
hdf5_store2.append(y)

f = h5py.File('data/test_data.h5', 'r')
dset = f['features']
print(dset[:].shape)

f = h5py.File('data/test_eval.h5', 'r')
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
