#!/usr/bin/env python3


import unittest

from gobychess.board import Board
#from gobychess.evaluation import piece_scores


class EvalTest(unittest.TestCase):
    def test_piece_scores(self):
        test_board = Board()
        test_board.from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
