#!/usr/bin/env python3

import timeit

from gmpy2 import xmpz

import gobychess.movegen as mvg
from gobychess.board import Board
from gobychess.utils import print_bitboard, invert_bitboard, bitboard_of_index

#moveset = xmpz(0b0000000000000000000000000000000000000000000000000000000001001100)
#print(list(yield_moveset(22, moveset)))

#board = Board()
#board.from_fen("r3k2N/ppp1q1pp/5n2/3Pp3/Q1Bn2b1/2P5/PP1P1bPP/RNB2K1R b q - 2 10")

#print(board)
#print_bitboard(board.all_pieces_white)

#moveset = xmpz(0b0000000000000000000000000000000000000000000000000000000001001100)
#print_bitboard(moveset)
#print()
#print_bitboard(invert_bitboard(moveset))

#print(list(mvg.gen_bishop_moves(board.pieces[0][2], board.all_pieces, board.all_pieces_black)))

#print(len(list(board.gen_legal_moves())))
#print(list(board.gen_legal_moves()))


# code = '''
# from gobychess.board import Board
# board = Board()
# board.from_fen("r3k2N/ppp1q1pp/5n2/3Pp3/Q1Bn2b1/2P5/PP1P1bPP/RNB2K1R b q - 2 10")
# board.in_check()
# '''
#
# import numpy as np
#
# t = timeit.Timer(code)
# res = t.repeat(50, 30000)
#
# print("many returns method")
# print("mean: " + str(np.mean(res)))
# print("std: " + str(np.std(res)))

def perft(current_board, depth):
        number_moves = 0
        if not depth:
            return 1
        for move in current_board.gen_legal_moves():
            new_board = current_board.board_copy()
            new_board = new_board.make_generated_move(move)
            number_moves += perft(new_board, depth - 1)
        return number_moves

import cProfile

board = Board()
board.from_fen("r3k2N/ppp1q1pp/5n2/3Pp3/Q1Bn2b1/2P5/PP1P1bPP/RNB2K1R b q - 2 10")

cProfile.run('perft(board, 4)')
