#!/usr/bin/env python3

import os
from random import randrange
import random

import chess
import chess.pgn
import numpy as np
import tensorflow as tf


class Loader():

    def __init__(self, gamedata, num_games):

        self.pgn = open(gamedata)   #"data/games.pgn")
        self.num_games = num_games
        self.x_train = []
        self.y_train = []

    def label_from_game(self, game):
        '''
        Return result for game node

        Args:
            game (Game): root node of game

        Returns:
            float: 1 for white win, 0 for black win, 0.5 for draw
        '''
        if game.headers['Result'] == "1-0":
            return 1
        elif game.headers['Result'] == "0-1":
            return -1
        elif game.headers['Result'] == "1/2-1/2":
            return 0

    def features_from_board(self, board):
        '''
        compute features for given position

        Args:
            board (Board): Board object holding position to evaluate

        Returns:
            Array of features
        '''

        num_pawns_b = sum(board.pieces(chess.PAWN, chess.BLACK).tolist())
        num_knights_b = sum(board.pieces(chess.KNIGHT, chess.BLACK).tolist())
        num_bishop_b = sum(board.pieces(chess.BISHOP, chess.BLACK).tolist())
        num_rook_b = sum(board.pieces(chess.ROOK, chess.BLACK).tolist())
        num_queen_b = sum(board.pieces(chess.QUEEN, chess.BLACK).tolist())

        num_pawns_w = sum(board.pieces(chess.PAWN, chess.WHITE).tolist())
        num_knights_w = sum(board.pieces(chess.KNIGHT, chess.WHITE).tolist())
        num_bishop_w = sum(board.pieces(chess.BISHOP, chess.WHITE).tolist())
        num_rook_w = sum(board.pieces(chess.ROOK, chess.WHITE).tolist())
        num_queen_w = sum(board.pieces(chess.QUEEN, chess.WHITE).tolist())

        #features = [num_pawns_b,
        #            num_knights_b,
        #            num_bishop_b,
        #            num_rook_b,
        #            num_queen_b,
        #            num_pawns_w,
        #            num_knights_w,
        #            num_bishop_w,
        #            num_rook_w,
        #            num_queen_w]

        features = [board.pieces(chess.PAWN, chess.WHITE).tolist(),
                    board.pieces(chess.KNIGHT, chess.WHITE).tolist(),
                    board.pieces(chess.BISHOP, chess.WHITE).tolist(),
                    board.pieces(chess.ROOK, chess.WHITE).tolist(),
                    board.pieces(chess.QUEEN, chess.WHITE).tolist(),
                    board.pieces(chess.KING, chess.WHITE).tolist(),
                    board.pieces(chess.PAWN, chess.BLACK).tolist(),
                    board.pieces(chess.KNIGHT, chess.BLACK).tolist(),
                    board.pieces(chess.BISHOP, chess.BLACK).tolist(),
                    board.pieces(chess.ROOK, chess.BLACK).tolist(),
                    board.pieces(chess.QUEEN, chess.BLACK).tolist(),
                    board.pieces(chess.KING, chess.BLACK).tolist()]

        return features

    def features_from_game(self, game):
        '''
        Get features from all positions in a game

        Args:
            game: root node of game

        Returns:
            Array containing features for every position in game
        '''
        game_features = []

        while not game.is_end():
            game_features += [self.features_from_board(game.board())]

            game = game.next()
        return game_features

    def load_games(self):

        counter = 0
        print(f"loading {self.num_games} games")
        while self.pgn and counter < self.num_games:

            print(f"loading game {counter} ...", end="\r")
            game = chess.pgn.read_game(self.pgn)
            counter += 1

            self.y_train += [int(self.label_from_game(game))]
            self.x_train += [self.features_from_game(game)]

        self.y_train = np.array(self.y_train)
        self.x_train = np.array(self.x_train)

        self.y_train *= 2

    def build_triplett(self, node):
        position = node.board()

        rnd_move = random.choice(list(node.board().legal_moves))
        random_move_position = node.board()
        random_move_position.push(rnd_move)

        next_position = node.next().board()

        triplett = [self.features_from_board(position),
                    self.features_from_board(next_position),
                    self.features_from_board(random_move_position)]

        return triplett

    def build_meta(self, node):
        result = self.label_from_game(node.game())
        last = False
        if node.next().is_end():
            last = True
        if node.turn() == chess.WHITE:
            to_move = 1
        elif node.turn() == chess.BLACK:
            to_move = 0
        return last, result, to_move



    def generate_dataset(self):
        counter = 0
        print(f"loading {self.num_games} games")
        while self.pgn and counter < self.num_games:

            print(f"loading game {counter} ...", end="\r")
            game = chess.pgn.read_game(self.pgn)
            counter += 1

            yield 2 * int(self.label_from_game(game)), self.features_from_game(game)

    def load_game(self, game):
        data = []
        meta = []

        while not game.is_end():
            data += [self.build_triplett(game)]
            meta += [self.build_meta(game)]
            game = game.next()

        return data, meta

    def generate_triplett_dataset(self, skip=0):
        dataset = []
        metaset = []
        counter = 0
        print(f"loading {self.num_games} games")

        # REVIEW: Brauche ich nicht ?
        for i in range(skip):
            game = chess.pgn.read_game(self.pgn)

        while self.pgn and counter < self.num_games:

            print(f"loading game {counter} ...", end="\r")
            game = chess.pgn.read_game(self.pgn)
            data, meta = self.load_game(game)
            dataset.extend(data)
            metaset.extend(meta)
            counter += 1

        return dataset, metaset




    def build_dataset(self):
        self.dataset = tf.data.Dataset.from_generator(self.generate_dataset, output_types=(tf.int32, tf.int32))





import numpy as np
import h5py

class HDF5Store(object):
    """
    Simple class to append value to a hdf5 file on disc (usefull for building keras datasets)

    Params:
        datapath: filepath of h5 file
        dataset: dataset name within the file
        shape: dataset shape (not counting main/batch axis)
        dtype: numpy dtype

    Usage:
        hdf5_store = HDF5Store('/tmp/hdf5_store.h5','X', shape=(20,20,3))
        x = np.random.random(hdf5_store.shape)
        hdf5_store.append(x)
        hdf5_store.append(x)

    From https://gist.github.com/wassname/a0a75f133831eed1113d052c67cf8633
    """
    def __init__(self, datapath, dataset, shape, dtype=np.float32, compression="gzip", chunk_len=1):
        self.datapath = datapath
        self.dataset = dataset
        self.shape = shape
        self.i = 0

        with h5py.File(self.datapath, mode='w') as h5f:
            self.dset = h5f.create_dataset(
                dataset,
                shape=(0, ) + shape,
                maxshape=(None, ) + shape,
                dtype=dtype,
                compression=compression,
                chunks=(chunk_len, ) + shape)

    def append(self, values):
        with h5py.File(self.datapath, mode='a') as h5f:
            dset = h5f[self.dataset]
            print(f"Saving {values.shape[0]} values")
            dset.resize((self.i + values.shape[0], ) + self.shape)
            dset[self.i:self.i+values.shape[0]] = [values]
            print(values.shape[0])
            self.i += values.shape[0]
            h5f.flush()
