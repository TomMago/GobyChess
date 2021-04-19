'''
Perft test cases, positions 1-6 taken from https://www.chessprogramming.org/Perft_Results
'''

import unittest

from gmpy2 import xmpz
from gobychess.board import Board
from gobychess.utils import index_of_square, print_bitboard, bitboard_of_index
import gobychess.movegen as mvg
import time


class PerftTests(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.board.from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        self.table = mvg.generate_table()
        self.non_sliding = mvg.generate_non_sliding()

    def _perft(self, current_board, depth):
        number_moves = 0
        if not depth:
            return 1
        for move in current_board.gen_legal_moves(self.table, self.non_sliding):
            new_board = current_board.board_copy()
            new_board = new_board.make_generated_move(move)
            number_moves += self._perft(new_board, depth - 1)
        return number_moves

    def test_perft(self):
        self.assertEqual(self._perft(self.board, 1), 20)
        self.assertEqual(self._perft(self.board, 2), 400)
        self.assertEqual(self._perft(self.board, 3), 8902)
        self.assertEqual(self._perft(self.board, 4), 197_281)
    #     #self.assertEqual(self._perft(self.board, 5), 4_865_609)
    #
    def test_perft_pos2(self):
        self.board.from_fen("r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 1 1")
        self.assertEqual(self._perft(self.board, 1), 48)
        self.assertEqual(self._perft(self.board, 2), 2039)
        self.assertEqual(self._perft(self.board, 3), 97_862)
    #     #self.assertEqual(self._perft(self.board, 4), 4_085_603)
    #
    def test_perft_pos3(self):
        self.board.from_fen("8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 1 1")
        self.assertEqual(self._perft(self.board, 1), 14)
        self.assertEqual(self._perft(self.board, 2), 191)
        self.assertEqual(self._perft(self.board, 3), 2812)
        self.assertEqual(self._perft(self.board, 4), 43_238)
    #     #self.assertEqual(self._perft(self.board, 5), 674_624)
    #     #self.assertEqual(self._perft(self.board, 6), 11_030_083)
    #
    def test_perft_pos4(self):
        self.board.from_fen("r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1")
        self.assertEqual(self._perft(self.board, 1), 6)
        self.assertEqual(self._perft(self.board, 2), 264)
        self.assertEqual(self._perft(self.board, 3), 9467)
        #self.assertEqual(self._perft(self.board, 4), 422_333)
        # self.assertEqual(self._perft(self.board, 5), 15_833_292)
    #
    def test_perft_pos5(self):
        self.board.from_fen("rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8")
        self.assertEqual(self._perft(self.board, 1), 44)
        self.assertEqual(self._perft(self.board, 2), 1486)
        self.assertEqual(self._perft(self.board, 3), 62_379)
    #     #self.assertEqual(self._perft(self.board, 4), 2_103_487)
    #     #self.assertEqual(self._perft(self.board, 5), 89_941_194)
    #
    def test_perft_pos6(self):
        self.board.from_fen("r4rk1/1pp1qppp/p1np1n2/2b1p1B1/2B1P1b1/P1NP1N2/1PP1QPPP/R4RK1 w - - 0 10")
        self.assertEqual(self._perft(self.board, 1), 46)
        self.assertEqual(self._perft(self.board, 2), 2079)
        self.assertEqual(self._perft(self.board, 3), 89_890)
    #     #self.assertEqual(self._perft(self.board, 4), 3_894_594)
    #
    def test_perft_pos7(self):
        self.board.from_fen("8/8/3rk3/8/8/2N1K3/8/8 w - - 0 1")
        self.assertEqual(self._perft(self.board, 1), 13)
        self.assertEqual(self._perft(self.board, 2), 205)
        self.assertEqual(self._perft(self.board, 3), 2250)
        self.assertEqual(self._perft(self.board, 4), 40097)
