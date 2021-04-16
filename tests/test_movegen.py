#!/usr/bin/env python3

from gmpy2 import xmpz

import pytest

import numpy as np

from gobychess.board import Board
import gobychess.movegen as mvg
from gobychess.utils import bitboard_of_square, index_of_square, bitboard_from_squares, print_bitboard

@pytest.fixture
def set_board():
    board = Board()
    board.from_fen("r3k2N/ppp1q1pp/5n2/3Pp3/Q1Bn2b1/2P5/PP1P1bPP/RNB2K1R b q - 2 10")
    table = mvg.generate_table()
    non_sliding = mvg.generate_non_sliding()
    return board, table, non_sliding


def test_rook_sliding(set_board):
    square = index_of_square('a8')
    attack_bitboard = bitboard_from_squares('b8 c8 d8 e8 a7')
    gen_attack_bitboard = mvg.rook_sliding(square, np.uint64(set_board[0].all_pieces), set_board[1], set_board[2])
    assert gen_attack_bitboard == attack_bitboard

    square = index_of_square('h1')
    attack_bitboard = bitboard_from_squares('g1 f1 h2')
    gen_attack_bitboard = mvg.rook_sliding(square, np.uint64(set_board[0].all_pieces), set_board[1], set_board[2])
    assert gen_attack_bitboard == attack_bitboard

    square = index_of_square('a1')
    attack_bitboard = bitboard_from_squares('b1 a2')
    gen_attack_bitboard = mvg.rook_sliding(square, np.uint64(set_board[0].all_pieces), set_board[1], set_board[2])
    assert gen_attack_bitboard == attack_bitboard


def test_bishop_sliding(set_board):
    square = index_of_square('c4')
    attack_bitboard = bitboard_from_squares('b5 a6 b3 a2 d3 e2 f1 d5')
    gen_attack_bitboard = mvg.bishop_sliding(square, np.uint64(set_board[0].all_pieces), set_board[1], set_board[2])
    assert gen_attack_bitboard == attack_bitboard

    square = index_of_square('c1')
    attack_bitboard = bitboard_from_squares('d2 b2')
    gen_attack_bitboard = mvg.bishop_sliding(square, np.uint64(set_board[0].all_pieces), set_board[1], set_board[2])
    assert gen_attack_bitboard == attack_bitboard

    square = index_of_square('f2')
    attack_bitboard = bitboard_from_squares('e1 g1 g3 e3 d4 h4')
    gen_attack_bitboard = mvg.bishop_sliding(square, np.uint64(set_board[0].all_pieces), set_board[1], set_board[2])
    assert gen_attack_bitboard == attack_bitboard

    square = index_of_square('g4')
    attack_bitboard = bitboard_from_squares('f3 e2 d1 h3 h5 f5 e6 d7 c8')
    gen_attack_bitboard = mvg.bishop_sliding(square, np.uint64(set_board[0].all_pieces), set_board[1], set_board[2])
    assert gen_attack_bitboard == attack_bitboard


## def test_gen_bishop_moves(set_board):
##     black_moves = len(list(mvg.gen_bishop_moves(set_board.pieces[0][2],
##                                                 set_board.all_pieces,
##                                                 set_board.all_pieces_color[0])))
##
##     assert black_moves == 14
##
##     white_moves = len(list(mvg.gen_bishop_moves(set_board.pieces[1][2],
##                                                 set_board.all_pieces,
##                                                 set_board.all_pieces_color[1])))
##
##     assert white_moves == 5
##
## def test_gen_rook_moves(set_board):
##     black_moves = len(list(mvg.gen_rook_moves(set_board.pieces[0][3],
##                                               set_board.all_pieces,
##                                               set_board.all_pieces_color[0])))
##
##     assert black_moves == 3
##
##     white_moves = len(list(mvg.gen_rook_moves(set_board.pieces[1][3],
##                                               set_board.all_pieces,
##                                               set_board.all_pieces_color[1])))
##
##     assert white_moves == 1
##
## def test_gen_queen_moves(set_board):
##     black_moves = len(list(mvg.gen_queen_moves(set_board.pieces[0][4],
##                                                set_board.all_pieces,
##                                                set_board.all_pieces_color[0])))
##
##     assert black_moves == 9
##
##     white_moves = len(list(mvg.gen_queen_moves(set_board.pieces[1][4],
##                                                set_board.all_pieces,
##                                                set_board.all_pieces_color[1])))
##
##
##     assert white_moves == 12
##
## def test_gen_knight_moves(set_board):
##     black_moves = len(list(mvg.gen_knight_moves(set_board.pieces[0][1],
##                                                 set_board.all_pieces_color[0])))
##
##     assert black_moves == 13
##
##     white_moves = len(list(mvg.gen_knight_moves(set_board.pieces[1][1],
##                                                 set_board.all_pieces_color[1])))
##
##
##     assert white_moves == 3
##
## def test_gen_king_moves(set_board):
##     black_moves = len(list(mvg.gen_king_moves(set_board.pieces[0][5],
##                                               set_board.all_pieces_color[0])))
##
##     assert black_moves == 4
##
##     white_moves = len(list(mvg.gen_king_moves(set_board.pieces[1][5],
##                                               set_board.all_pieces_color[1])))
##
##     assert white_moves == 4
##
##
## def test_gen_pawn_moves_white(set_board):
##     white_moves = len(list(mvg.gen_pawn_moves_white(set_board.pieces[1][0],
##                                                     set_board)))
##     assert white_moves == 9
##
##
## def test_gen_pawn_moves_black(set_board):
##     black_moves = len(list(mvg.gen_pawn_moves_black(set_board.pieces[0][0],
##                                                     set_board)))
##     assert black_moves == 11
##
## def test_check_piece_move(set_board):
##     set_board.to_move = 1
##     assert mvg.check_piece_move(0, 8, 16, set_board) == True
##     assert mvg.check_piece_move(0, 8, 24, set_board) == False
##     assert mvg.check_piece_move(0, 9, 25, set_board) == True
##     assert mvg.check_piece_move(2, 26, 33, set_board) == True
##     assert mvg.check_piece_move(2, 26, 53, set_board) == False
##     assert mvg.check_piece_move(3, 7, 6, set_board) == True
##     assert mvg.check_piece_move(3, 7, 8, set_board) == False
##
##     set_board.to_move = 0
##     assert mvg.check_piece_move(0, 55, 47, set_board) == True
##     assert mvg.check_piece_move(0, 55, 39, set_board) == True
##     assert mvg.check_piece_move(0, 55, 32, set_board) == False
##     assert mvg.check_piece_move(3, 56, 59, set_board) == True
##     assert mvg.check_piece_move(3, 56, 53, set_board) == False
##     assert mvg.check_piece_move(5, 60, 59, set_board) == True
##     assert mvg.check_piece_move(5, 60, 52, set_board) == False
##
## def test_in_check(set_board):
##     assert set_board.in_check() == True
##     set_board.to_move = 1
##     assert set_board.in_check() == False
##     set_board.to_move = 0
##
## def test_generate_moves(set_board):
##     assert len(list(mvg.generate_moves(set_board))) == 54
##     set_board.to_move = 1
##     assert len(list(mvg.generate_moves(set_board))) == 34
##     set_board.to_move = 0
