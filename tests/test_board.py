#!/usr/bin/env python3

import unittest

from gmpy2 import xmpz
from gobychess.board import Board
from gobychess.utils import (bitboard_of_index, bitboard_of_square,
                             index_of_square, print_bitboard, move_from_san)


import pytest




class BoardTests(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.board.from_fen("r3k2N/ppp1q1pp/5n2/3Pp3/Q1Bn2b1/2P5/PP1P1bPP/RNB2K1R b q - 2 10")

    def test_from_fen(self):
        self.assertEqual(self.board.to_move, 0)
        self.assertEqual(self.board.castling_rights['white kingside'], 0)
        self.assertEqual(self.board.castling_rights['white queenside'], 0)
        self.assertEqual(self.board.castling_rights['black kingside'], 0)
        self.assertEqual(self.board.castling_rights['black queenside'], 1)
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
        #print("e2e4")
        test_board.make_generated_move((index_of_square('e2'), index_of_square('e4'), None))
        self.assertEqual(test_board.to_move, 0)
        #self.assertEqual(test_board.en_passant, 20)
        self.assertEqual(test_board.piece_on(28), (1, 0))
        self.assertEqual(test_board.piece_on(12), (None, None))
        self.assertEqual(test_board.fullmove_counter, 1)
        self.assertEqual(test_board.halfmove_clock, 0)


        test_board = Board()
        test_board.from_fen("rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8")
        test_board.make_generated_move((index_of_square('a2'), index_of_square('a3'), None))
        test_board.make_generated_move((index_of_square('f2'), index_of_square('h1'), None))
        print(len(list(test_board.gen_legal_moves())))
        print(list(test_board.gen_legal_moves()))
        #moves = list(test_board.gen_legal_moves())
        #for move in moves:
        #    print(move)
        #    print_bitboard(bitboard_of_index(move[0]) | bitboard_of_index(move[1]))
        #    print()
        #print(len(list(test_board.gen_legal_moves())))
        #self.assertEqual(0, 1)

    def test_in_check(self):
        test_board = Board()
        test_board.from_fen("r3k2N/ppp1q1pp/5n2/3Pp3/Q1Bn2b1/2P5/PP1P1bPP/RNB2K1R b q - 2 10")
        self.assertEqual(test_board.in_check(), True)
        test_board.make_generated_move((index_of_square('c7'), index_of_square('c6'), None))
        self.assertEqual(test_board.in_check(), False)
        test_board.make_generated_move((index_of_square('c4'), index_of_square('b3'), None))
        self.assertEqual(test_board.in_check(), False)
        test_board.make_generated_move((index_of_square('g4'), index_of_square('e2'), None))
        self.assertEqual(test_board.in_check(), True)

    def test_is_checkmate(self):
        test_board = Board()
        test_board.from_fen("r3k2N/ppp1q1pp/5n2/3Pp3/Q1Bn2b1/2P5/PP1P1bPP/RNB2K1R b q - 2 10")
        self.assertEqual(test_board.is_checkmate(), False)
        test_board.make_generated_move((index_of_square('c7'), index_of_square('c6'), None))
        self.assertEqual(test_board.is_checkmate(), False)
        test_board.make_generated_move((index_of_square('c4'), index_of_square('b3'), None))
        test_board.make_generated_move((index_of_square('f6'), index_of_square('e4'), None))
        test_board.make_generated_move((index_of_square('a2'), index_of_square('a3'), None))
        test_board.make_generated_move((index_of_square('g4'), index_of_square('e2'), None))
        self.assertEqual(test_board.is_checkmate(), True)
        test_board.from_fen("r1bqkbnr/1ppp1ppp/p1n5/4p3/2B1P3/5Q2/PPPP1PPP/RNB1K1NR w KQkq - 0 4")
        self.assertEqual(test_board.is_checkmate(), False)
        test_board.make_generated_move((index_of_square('f3'), index_of_square('f7'), None))
        self.assertEqual(test_board.is_checkmate(), True)

    def test_is_stalemate(self):
        test_board = Board()
        test_board.from_fen("8/8/8/8/3k4/q7/2K5/8 w - - 0 1")
        self.assertEqual(test_board.is_stalemate(), False)
        test_board.make_generated_move((index_of_square('c2'), index_of_square('b1'), None))
        self.assertEqual(test_board.is_stalemate(), False)
        test_board.make_generated_move((index_of_square('d4'), index_of_square('c3'), None))
        self.assertEqual(test_board.is_stalemate(), True)


    def test_make_move(self):
        test_board = Board()
        test_board.from_fen("r3k2N/ppp1q1pp/5n2/3Pp3/Q1Bn2b1/2P5/PP1P1bPP/RNB2K1R b q - 2 10")
        with pytest.raises(IndexError):
            test_board.make_move((60, 68, None))
        with pytest.raises(ValueError):
            test_board.make_move((index_of_square('f7'), index_of_square('d7'), None))
        with pytest.raises(ValueError):
            test_board.make_move((index_of_square('e8'), index_of_square('d7'), None))
        with pytest.raises(ValueError):
            test_board.make_move((index_of_square('f6'), index_of_square('e4'), None))
        with pytest.raises(ValueError):
            test_board.make_move((index_of_square('e8'), index_of_square('g8'), None))
        test_board.make_move((index_of_square('c7'), index_of_square('c6'), None))
        with pytest.raises(ValueError):
            test_board.make_move((index_of_square('a1'), index_of_square('a3'), None))


    def test_move_from_san(self):
        self.assertEqual(move_from_san('e1e2'), (4, 12, None))
        self.assertEqual(move_from_san('c4b5'), (26, 33, None))
        self.assertEqual(move_from_san('e7e8q'), (52, 60, 4))
        self.assertEqual(move_from_san('d7d8r'), (51, 59, 3))
        self.assertEqual(move_from_san('c7c8b'), (50, 58, 2))
        self.assertEqual(move_from_san('b7b8n'), (49, 57, 1))
