#!/usr/bin/env python3

import unittest

from gmpy2 import xmpz

from gobychess.board import Board
import gobychess.movegen as mvg
from gobychess.utils import bitboard_of_square, index_of_square, bitboard_from_squares, print_bitboard


class MovegenTests(unittest.TestCase):
    def __init__(self):
        self.board = Board()

    def set_up(self):
        self.board.from_fen("r3k2N/ppp1q1pp/5n2/3Pp3/Q1Bn2b1/2P5/PP1P1bPP/RNB2K1R b q - 2 10")

    def test_rook_sliding(self):
        square = index_of_square('a8')
        attack_bitboard = bitboard_from_squares('b8 c8 d8 e8 a7')
        gen_attack_bitboard = mvg.rook_sliding(square, self.board.all_pieces)
        self.assertEqual(gen_attack_bitboard, attack_bitboard)

        square = index_of_square('h1')
        attack_bitboard = bitboard_from_squares('g1 f1 h2')
        gen_attack_bitboard = mvg.rook_sliding(square, self.board.all_pieces)
        self.assertEqual(gen_attack_bitboard, attack_bitboard)

        square = index_of_square('a1')
        attack_bitboard = bitboard_from_squares('b1 a2')
        gen_attack_bitboard = mvg.rook_sliding(square, self.board.all_pieces)
        self.assertEqual(gen_attack_bitboard, attack_bitboard)

    def test_bishop_sliding(self):
        square = index_of_square('c4')
        attack_bitboard = bitboard_from_squares('b5 a6 b3 a2 d3 e2 f1 d5')
        gen_attack_bitboard = mvg.bishop_sliding(square, self.board.all_pieces)
        self.assertEqual(gen_attack_bitboard, attack_bitboard)

        square = index_of_square('c1')
        attack_bitboard = bitboard_from_squares('d2 b2')
        gen_attack_bitboard = mvg.bishop_sliding(square, self.board.all_pieces)
        self.assertEqual(gen_attack_bitboard, attack_bitboard)

        square = index_of_square('f2')
        attack_bitboard = bitboard_from_squares('e1 g1 g3 e3 d4 h4')
        gen_attack_bitboard = mvg.bishop_sliding(square, self.board.all_pieces)
        self.assertEqual(gen_attack_bitboard, attack_bitboard)

        square = index_of_square('g4')
        attack_bitboard = bitboard_from_squares('f3 e2 d1 h3 h5 f5 e6 d7 c8')
        gen_attack_bitboard = mvg.bishop_sliding(square, self.board.all_pieces)
        self.assertEqual(gen_attack_bitboard, attack_bitboard)

    def test_gen_bishop_moves(self):
        black_moves = len(list(mvg.gen_bishop_moves(self.board.pieces[0][2],
                                                    self.board.all_pieces,
                                                    self.board.all_pieces_color[0])))

        self.assertEqual(black_moves, 14)

        white_moves = len(list(mvg.gen_bishop_moves(self.board.pieces[1][2],
                                                    self.board.all_pieces,
                                                    self.board.all_pieces_color[1])))

        self.assertEqual(white_moves, 5)

    def test_gen_rook_moves(self):
        black_moves = len(list(mvg.gen_rook_moves(self.board.pieces[0][3],
                                                  self.board.all_pieces,
                                                  self.board.all_pieces_color[0])))

        self.assertEqual(black_moves, 3)

        white_moves = len(list(mvg.gen_rook_moves(self.board.pieces[1][3],
                                                  self.board.all_pieces,
                                                  self.board.all_pieces_color[1])))

        self.assertEqual(white_moves, 1)

    def test_gen_queen_moves(self):
        black_moves = len(list(mvg.gen_queen_moves(self.board.pieces[0][4],
                                                   self.board.all_pieces,
                                                   self.board.all_pieces_color[0])))

        self.assertEqual(black_moves, 9)

        white_moves = len(list(mvg.gen_queen_moves(self.board.pieces[1][4],
                                                   self.board.all_pieces,
                                                   self.board.all_pieces_color[1])))

        self.assertEqual(white_moves, 12)

    def test_gen_knight_moves(self):
        black_moves = len(list(mvg.gen_knight_moves(self.board.pieces[0][1],
                                                    self.board.all_pieces_color[0])))

        self.assertEqual(black_moves, 13)

        white_moves = len(list(mvg.gen_knight_moves(self.board.pieces[1][1],
                                                    self.board.all_pieces_color[1])))

        self.assertEqual(white_moves, 3)

    def test_gen_king_moves(self):
        black_moves = len(list(mvg.gen_king_moves(self.board.pieces[0][5],
                                                  self.board.all_pieces_color[0])))

        self.assertEqual(black_moves, 4)

        white_moves = len(list(mvg.gen_king_moves(self.board.pieces[1][5],
                                                  self.board.all_pieces_color[1])))

        self.assertEqual(white_moves, 4)

    def test_gen_pawn_moves_white(self):
        white_moves = len(list(mvg.gen_pawn_moves_white(self.board.pieces[1][0]
                                                        , self.board)))
        self.assertEqual(white_moves, 9)

    def test_gen_pawn_moves_black(self):
        black_moves = len(list(mvg.gen_pawn_moves_black(self.board.pieces[0][0]
                                                        , self.board)))
        self.assertEqual(black_moves, 11)

    def test_check_piece_move(self):
        self.board.to_move = 1
        self.assertEqual(mvg.check_piece_move((8, 16, None), self.board), True)
        self.assertEqual(mvg.check_piece_move((8, 24, None), self.board), False)
        self.assertEqual(mvg.check_piece_move((9, 25, None), self.board), True)
        self.assertEqual(mvg.check_piece_move((26, 33, None), self.board), True)
        self.assertEqual(mvg.check_piece_move((26, 53, None), self.board), False)
        self.assertEqual(mvg.check_piece_move((7, 6, None), self.board), True)
        self.assertEqual(mvg.check_piece_move((7, 8, None), self.board), False)

        self.board.to_move = 0
        self.assertEqual(mvg.check_piece_move((55, 47, None), self.board), False)
        self.assertEqual(mvg.check_piece_move((55, 39, None), self.board), False)
        self.assertEqual(mvg.check_piece_move((55, 32, None), self.board), False)
        self.assertEqual(mvg.check_piece_move((56, 59, None), self.board), False)
        self.assertEqual(mvg.check_piece_move((56, 53, None), self.board), False)
        self.assertEqual(mvg.check_piece_move((60, 59, None), self.board), True)
        self.assertEqual(mvg.check_piece_move((60, 52, None), self.board), False)

    def test_in_check(self):
        self.assertEqual(self.board.in_check(), True)
        self.board.to_move = 1
        self.assertEqual(self.board.in_check(), False)
        self.board.to_move = 0

    def test_generate_moves(self):
        self.assertEqual(len(list(mvg.generate_moves(self.board))), 54)
        self.board.to_move = 1
        self.assertEqual(len(list(mvg.generate_moves(self.board))), 34)
        self.board.to_move = 0
