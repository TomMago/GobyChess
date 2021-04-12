#!/usr/bin/env python3

import os
from random import randrange

import chess
import chess.pgn
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf


class loader():

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
            return 0
        elif game.headers['Result'] == "1/2-1/2":
            return 0.5

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

        features = [num_pawns_b,
                    num_knights_b,
                    num_bishop_b,
                    num_rook_b,
                    num_queen_b,
                    num_pawns_w,
                    num_knights_w,
                    num_bishop_w,
                    num_rook_w,
                    num_queen_w]

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

    def generate_dataset(self):

        counter = 0
        print(f"loading {self.num_games} games")
        while self.pgn and counter < self.num_games:

            print(f"loading game {counter} ...", end="\r")
            game = chess.pgn.read_game(self.pgn)
            counter += 1

            yield 2 * int(self.label_from_game(game)), self.features_from_game(game)


    def build_dataset(self):
        self.dataset = tf.data.Dataset.from_generator(self.generate_dataset, output_types=(tf.int32, tf.int32))
