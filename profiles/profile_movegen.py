#!/usr/bin/env python3
import cProfile
import gobychess

board = gobychess.Board()
board.from_fen("r3k2N/ppp1q1pp/5n2/3Pp3/Q1Bn2b1/2P5/PP1P1bPP/RNB2K1R b q - 2 10")

cProfile.run('gobychess.utils.perft(board, 3)')
