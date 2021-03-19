#!/usr/bin/env python3

from gmpy2 import xmpz

import gobychess.movegen as mvg
from gobychess.board import Board
from gobychess.utils import print_bitboard, invert_bitboard

#moveset = xmpz(0b0000000000000000000000000000000000000000000000000000000001001100)
#print(list(yield_moveset(22, moveset)))

board = Board()
board.from_fen("r3k2N/ppp1q1pp/5n2/3Pp3/Q1Bn2b1/2P5/PP1P1bPP/RNB2K1R b q - 2 10")

#print(board)
#print_bitboard(board.all_pieces_white)

#moveset = xmpz(0b0000000000000000000000000000000000000000000000000000000001001100)
#print_bitboard(moveset)
#print()
#print_bitboard(invert_bitboard(moveset))

#print(list(mvg.gen_bishop_moves(board.pieces[0][2], board.all_pieces, board.all_pieces_black)))

mvg.generate_king()
