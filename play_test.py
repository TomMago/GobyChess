#!/usr/bin/env python3

"""
Script for optimization of engine parameters with genetic methods.
Let different versions of Goby play tournament against each other
and create offsprings of best ones by random variation
TODO:
Debug playing single tournament
automate tournament playing
take top x percent of tournament to create offsprings
"""

import os

import chess
import chess.engine
import chess.pgn
import numpy as np


class Tournament:

    def __init__(self, players, epoch=1, depth=3):
        self.engine_path = "path/to/goby.sh"
        self.players = dict(zip(players, np.zeros(len(players))))
        self.epoch = epoch
        self.depth = depth

    def play_game(self, player1, player2):
        """
        Play game between two players
        loads settings form .csv files
        """
        engine1 = chess.engine.SimpleEngine.popen_uci(self.engine_path)
        engine2 = chess.engine.SimpleEngine.popen_uci(self.engine_path)
        engine1.configure({'evalpath': f'settings/epoch-{self.epoch}/gbch-{self.epoch}-{player1}'})
        engine2.configure({'evalpath': f'settings/epoch-{self.epoch}/gbch-{self.epoch}-{player1}'})
        game = chess.pgn.Game()
        game.headers["Event"] = "gobyfight"
        game.headers["White"] = f"gbch-{self.epoch}-{player1}"
        game.headers["Black"] = f"gbch-{self.epoch}-{player2}"
        board = chess.Board()
        node = game.game()
        while not board.is_game_over():
            result = engine1.play(board, chess.engine.Limit(depth=self.depth))
            board.push(result.move)
            node = node.add_variation(chess.Move.from_uci(result.move.uci()))
            if board.is_game_over():
                break
            result = engine1.play(board, chess.engine.Limit(depth=self.depth))
            board.push(result.move)
            node = node.add_variation(chess.Move.from_uci(result.move.uci()))
        outcome = board.outcome(claim_draw=True).winner
        if outcome:
            self.players[player1] += 1
            print(f"{player1} won agains {player2}")
        elif outcome == False:
            self.players[player2] += 1
            print(f"{player2} won agains {player1}")

        game.headers["Result"] = board.outcome().result()
        engine1.quit()
        engine2.quit()


    def play_tournament(self):
        """
        play full round tournament
        """
        for player1 in self.players:
            for player2 in self.players:
                if not player1 == player2:
                    self.play_game(player1, player2)



def population_from_parents(parents, epoch, offsprings):
    '''
    take list of parent ids, pull files from epoch folder and create fixed number of offsprings from parent population.
    save offsprings in new folder
    '''
    offsprings_per_parent = offsprings // len(parents)
    os.mkdir(os.path.abspath(f"settings/epoch-{epoch + 1}"))
    for i in parents:
        parent_square = np.genfromtxt(f'settings/epoch-{epoch}/gbch-{epoch}-{i}_square.csv', delimiter=",")
        parent_piece = np.genfromtxt(f'settings/epoch-{epoch}/gbch-{epoch}-{i}_piece.csv', delimiter=",")
        np.savetxt(f"settings/epoch-{epoch + 1}/gbch-{epoch + 1}-{i}_square.csv", parent_square, fmt='%i', delimiter=",")
        np.savetxt(f"settings/epoch-{epoch + 1}/gbch-{epoch + 1}-{i}_piece.csv", parent_piece, fmt='%i', delimiter=",")
        for j in range(offsprings_per_parent):
            offspring_square = parent_square + np.random.randint(-2, 2, size=(6, 64))
            offspring_piece = parent_piece + np.random.randint(-2, 2, size=(6,))
            np.savetxt(f"settings/epoch-{epoch + 1}/gbch-{epoch + 1}-{len(parents) + i * offsprings_per_parent + j}_square.csv", offspring_square, fmt='%i', delimiter=",")
            np.savetxt(f"settings/epoch-{epoch + 1}/gbch-{epoch + 1}-{len(parents) + i * offsprings_per_parent + j}_piece.csv", offspring_piece, fmt='%i', delimiter=",")


population_from_parents([0], 0, 10)
tournament = Tournament(range(11), 1, 3)
tournament.play_tournament()
print(tournament.players)

