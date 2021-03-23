#!/usr/bin/env python3

import unittest

from gmpy2 import xmpz

from gobychess.board import Board
from gobychess.utils import bitboard_of_square, print_bitboard, index_of_square


class BoardTests(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.board.from_fen("r3k2N/ppp1q1pp/5n2/3Pp3/Q1Bn2b1/2P5/PP1P1bPP/RNB2K1R b q - 2 10")

    def test_from_fen(self):
        self.assertEqual(self.board.to_move, 0)
        self.assertEqual(self.board.white_kingside, 0)
        self.assertEqual(self.board.white_queenside, 0)
        self.assertEqual(self.board.black_kingside, 0)
        self.assertEqual(self.board.black_queenside, 1)
        self.assertEqual(self.board.en_passant, xmpz(0))
        self.assertEqual(self.board.halfmove_clock, 2)
        self.assertEqual(self.board.fullmove_counter, 10)
        self.assertEqual(self.board.pieces[0][0],
                         xmpz(0b00000000011000111000000000001000000000000000000000000000000000000))
        self.assertEqual(self.board.pieces[0][1],
                         bitboard_of_square('f6') | bitboard_of_square('d4'))
        self.assertEqual(self.board.pieces[0][2],
                         bitboard_of_square('f2') | bitboard_of_square('g4'))
        self.assertEqual(self.board.pieces[0][3],
                         bitboard_of_square('a8'))
        self.assertEqual(self.board.pieces[0][4],
                         bitboard_of_square('e7'))
        self.assertEqual(self.board.pieces[0][5],
                         bitboard_of_square('e8'))

        self.assertEqual(self.board.pieces[1][0],
                         xmpz(0b00000000000000000000000000000100000000000000001001100101100000000))
        self.assertEqual(self.board.pieces[1][1],
                         bitboard_of_square('b1') | bitboard_of_square('h8'))
        self.assertEqual(self.board.pieces[1][2],
                         bitboard_of_square('c4') | bitboard_of_square('c1'))
        self.assertEqual(self.board.pieces[1][3],
                         bitboard_of_square('a1') | bitboard_of_square('h1'))
        self.assertEqual(self.board.pieces[1][4],
                         bitboard_of_square('a4'))
        self.assertEqual(self.board.pieces[1][5],
                         bitboard_of_square('f1'))

    def test_in_check_after_move(self):
        self.assertEqual(self.board.in_check_after_move((52, 51, None)), False)
        self.assertEqual(self.board.in_check_after_move((52, 53, None)), True)
        self.assertEqual(self.board.in_check_after_move((60, 59, None)), False)
        self.assertEqual(self.board.in_check_after_move((60, 51, None)), True)


    def test_make_moves(self):
        test_board = Board()
        test_board.from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        test_board.make_move((index_of_square('e2'), index_of_square('e4'), None))
        self.assertEqual(test_board.to_move, 0)
        self.assertEqual(test_board.en_passant, 20)
        self.assertEqual(test_board.piece_on(28), (1, 0))
        self.assertEqual(test_board.piece_on(12), (None, None))
        self.assertEqual(test_board.fullmove_counter, 1)
        self.assertEqual(test_board.halfmove_clock, 0)
        test_board.make_move((index_of_square('e7'), index_of_square('e5'), None))