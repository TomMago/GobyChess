#!/usr/bin/env python3


import timeit

from gmpy2 import xmpz

import gobychess
from gobychess.board import Board


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

#
# t = timeit.Timer(code)
# res = t.repeat(50, 30000)
#
# print("many returns method")
# print("mean: " + str(np.mean(res)))
# print("std: " + str(np.std(res)))

#board.from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
#board.from_fen("r3k2N/ppp1q1pp/5n2/3Pp3/Q1Bn2b1/2P5/PP1P1bPP/RNB2K1R b q - 2 10")

#cProfile.run('perft(board, 3)')

#x = np.bitwise_or(np.uint64(2**bit), np.uint64(2**(bit - 4)))
#gobychess.utils.print_bitboard(x)
#print()
#gobychess.utils.print_bitboard(y)
#print()
#print("0b110101")
#print(gobychess.utils.reverse_bit_scan(x))
#print(gobychess.utils.forward_bit_scan(x))
#print("0b010000")
#print(gobychess.utils.reverse_bit_scan(y))
#print(gobychess.utils.forward_bit_scan(y))
#gobychess.utils.print_bitboard(np.bitwise_and(x,np.bitwise_not(y)))



for i in gobychess.movegen.generate_direction(1):
    gobychess.utils.print_bitboard(i)
    print()
