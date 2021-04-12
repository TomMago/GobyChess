#!/usr/bin/env python3

import timeit

from gmpy2 import xmpz

import gobychess.movegen as mvg
from gobychess.board import Board
from gobychess.utils import print_bitboard, invert_bitboard, bitboard_of_index
from gobychess.search import simple_min_max
from gobychess.loader import loader
from gobychess.play import play_game
from gobychess.uci import main

main()


#play_game()



# board = Board()
# board.from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
# import time
# start = time.time()
#
# print(perft(board, 4))
#
# end = time.time()
#
# print("time: ", end - start)
#
# code = '''
# from gobychess.board import Board
# from gobychess.utils import perft
#
# board = Board()
# board.from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
# perft(board, 1)
# '''

#timeit.timeit(code)



# board = Board()
# board.from_fen("2r1r1k1/1b1n1ppp/pp1p1b2/3Pp3/P1q1N3/1Q4P1/1P2NPBP/R4R1K w - - 0 18")
# evalu, move = simple_min_max(board, 3)
# print(evalu)
# print_move(move)
# print()
# board.from_fen("r1b4k/ppp1n1pp/8/N2Qp2q/3bP1n1/3P3P/PP4P1/R1B2R1K w - - 5 18")
# evalu, move = simple_min_max(board, 3)
# print(evalu)
# print_move(move)
# print()
# board.from_fen("8/5pkp/p2q2p1/3pr3/2pQ4/P1P3PP/1P3P2/3R1K2 w - - 2 27")
# evalu, move = simple_min_max(board, 3)
# print(evalu)
# print_move(move)
# print()
# board.from_fen("rnb1kb1r/pp2pppp/2pp4/3q4/5B2/3QPN2/3N1PPP/2R2RK1 w kq - 0 15")
# evalu, move = simple_min_max(board, 3)
# print(evalu)
# print_move(move)
