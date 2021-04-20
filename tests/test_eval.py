#!/usr/bin/env python3


import unittest

from gobychess.board import Board
from gobychess.evaluation import piece_scores

class EvalTest(unittest.TestCase):
    def test_piece_scores(self):
        test_board = Board()
        test_board.from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        #self.assertEqual(piece_scores(test_board), 0)
        #test_board.from_fen("rnbqkbnr/ppp1pppp/8/3P4/8/8/PPPP1PPP/RNBQKBNR b KQkq - 0 2")
        #self.assertEqual(piece_scores(test_board), 1)
        #test_board.from_fen("rnb1kbnr/pp2pppp/8/qp6/8/2N2N2/PPPP1PPP/R1BQK2R w KQkq - 0 6")
        #self.assertEqual(piece_scores(test_board), -3)
        #test_board.from_fen("rn2kbnr/pp1bpppp/8/B3q1N1/2Q5/8/PPP2PPP/R4K1R b kq - 4 11")
        #self.assertEqual(piece_scores(test_board), -6)
        #test_board.from_fen("rn2kbnr/1p1bpQpp/p7/B3q1N1/8/8/PPP2PPP/R4K1R b kq - 0 12")
        #self.assertEqual(piece_scores(test_board), 100)
