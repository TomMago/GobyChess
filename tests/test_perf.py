#!/usr/bin/env python3

import unittest

from gmpy2 import xmpz
from gobychess.board import Board


class PerfTests(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.board.from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

    def _perft(self, current_board, depth):
        number_moves = 0
        if not depth:
            return 1
        for move in current_board.gen_legal_moves():
            new_board = current_board.board_copy()
            new_board = new_board.make_generated_move(move)
            number_moves += self._perft(new_board, depth - 1)
        return number_moves

    def test_perft(self):
        self.assertEqual(self._perft(self.board, 1), 20)
        self.assertEqual(self._perft(self.board, 2), 400)
        self.assertEqual(self._perft(self.board, 3), 8902)

        # import time
        # start = time.time()
        # self.assertEqual(self._perft(self.board, 4), 197281)
        # self.assertEqual(self._perft(self.board, 5), 4_865_609)
        # end = time.time()
        # print("time: " + str(end-start))

    def test_perf_pos2(self):
        self.board.from_fen("r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 1 1")
        self.assertEqual(self._perft(self.board, 1), 48)
        self.assertEqual(self._perft(self.board, 2), 2039)
        self.assertEqual(self._perft(self.board, 3), 97862)

    def test_perf_pos3(self):
        self.board.from_fen("8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 1 1")
        self.assertEqual(self._perft(self.board, 1), 14)
        self.assertEqual(self._perft(self.board, 2), 191)
        self.assertEqual(self._perft(self.board, 3), 2812)
