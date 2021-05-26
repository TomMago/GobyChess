#!/usr/bin/env python3

"""
Script for optimization of engine parameters with genetic methods.
Let different versions of Goby play tournament against each other
and create offsprings of best ones by random variation
"""

import logging
import os
import time

import chess
import chess.engine
import chess.pgn
import numpy as np
import multiprocessing

# Enable debug logging.
# logging.basicConfig(level=logging.DEBUG)

DEPTH = 2
BESTCOUNT = 4
CHILDREN = 10
EPOCHS = 5
VARIATION = 6


class Tournament:

    def __init__(self, players, epoch=1, depth=3):
        self.engine_path = os.path.abspath("goby.sh")
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
        engine2.configure({'evalpath': f'settings/epoch-{self.epoch}/gbch-{self.epoch}-{player2}'})
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
            result = engine2.play(board, chess.engine.Limit(depth=self.depth))
            board.push(result.move)
            node = node.add_variation(chess.Move.from_uci(result.move.uci()))
        outcome = board.outcome(claim_draw=True).winner
        if outcome:
            #self.players[player1] += 1
            ret = player1
            print(f"{player1} won agains {player2}", end="\r")
        elif outcome == False:
            #self.players[player2] += 1
            ret = player2
            print(f"{player2} won agains {player1}", end="\r")
        elif outcome == None:
            #self.players[player1] += 0.5
            #self.players[player2] += 0.5
            ret = -player2
            print(f"{player1} vs {player2} ended in a draw", end="\r")
        game.headers["Result"] = board.outcome().result()
        print(game, file=open(os.path.abspath("games.pgn"), "a+"), end="\n\n")
        engine1.quit()
        engine2.quit()
        return ret

    def play_tournament(self):
        """
        play full round tournament
        """
        pool = multiprocessing.Pool(4)
        for player1 in self.players:
            opponents = []
            for player2 in self.players:
                if not player1 == player2:
                    #self.play_game(player1, player2)
                    opponents.append((player1, player2))

            res = pool.starmap(self.play_game, opponents)

            for player in res:
                if player < 0:
                    self.players[player1] += 0.5
                    self.players[abs(player)] += 0.5
                else:
                    self.players[player] += 1
            print(self.players)


    def getbest(self, bestcount):
        sort = sorted(self.players.items(), key=lambda x: x[1], reverse=True)
        best = [i[0] for i in sort[:bestcount]]
        return best




class Optimization:

    def __init__(self, depth, bestcount, children, epochs, variation):
        self.depth = depth
        self.bestcount = bestcount
        self.children = children
        self.epochs = epochs
        self.variation = variation
        self.runningid = 1

    def population_from_parents(self, parents, epoch, offsprings):
        '''
        take list of parent ids, pull files from epoch folder and create fixed number of offsprings from parent population.
        save offsprings in new folder
        '''
        offsprings_per_parent = offsprings // len(parents)
        os.mkdir(os.path.abspath(f"settings/epoch-{epoch + 1}"))
        children = []
        children.extend(parents)
        for i in parents:
            parent_square = np.genfromtxt(f'settings/epoch-{epoch}/gbch-{epoch}-{i}_square.csv', delimiter=",")
            parent_piece = np.genfromtxt(f'settings/epoch-{epoch}/gbch-{epoch}-{i}_piece.csv', delimiter=",")
            np.savetxt(f"settings/epoch-{epoch + 1}/gbch-{epoch + 1}-{i}_square.csv", parent_square, fmt='%i', delimiter=",")
            np.savetxt(f"settings/epoch-{epoch + 1}/gbch-{epoch + 1}-{i}_piece.csv", parent_piece, fmt='%i', delimiter=",")
            for j in range(offsprings_per_parent):
                offspring_square = parent_square + np.random.randint(-VARIATION, self.variation, size=(6, 64))
                offspring_piece = parent_piece + np.random.randint(-VARIATION, self.variation, size=(6,))
                np.savetxt(f"settings/epoch-{epoch + 1}/gbch-{epoch + 1}-{self.runningid}_square.csv", offspring_square, fmt='%i', delimiter=",")
                np.savetxt(f"settings/epoch-{epoch + 1}/gbch-{epoch + 1}-{self.runningid}_piece.csv", offspring_piece, fmt='%i', delimiter=",")
                children.append(self.runningid)
                self.runningid += 1

        return children

    def play_epoch(self, parents, epoch, children):
        print(f"Epoch {epoch + 1}:")
        children = self.population_from_parents(parents, epoch, children)
        print("created ", len(children), f" children in /settings/epoch-{epoch + 1}")
        tournament = Tournament(children, epoch + 1, DEPTH)
        tournament.play_tournament()
        print(sorted(tournament.players.items(), key=lambda x: x[1], reverse=True))
        best = tournament.getbest(BESTCOUNT)
        print("best: ", best)
        print(f"End Epoch {epoch + 1}:")
        return best


if __name__ == "__main__":
    best = [0]
    opt = Optimization(DEPTH, BESTCOUNT, CHILDREN, EPOCHS, VARIATION)
    for epoch in range(EPOCHS):
        best = opt.play_epoch(best, epoch, CHILDREN)
