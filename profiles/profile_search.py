#!/usr/bin/env python3

import cProfile
import gobychess
from gobychess.search import Searcher

board = gobychess.Board()
#board.from_fen("r3k2N/ppp1q1pp/5n2/3Pp3/Q1Bn2b1/2P5/PP1P1bPP/RNB2K1R b q - 2 10")
board.from_fen("r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 4 4")

s = Searcher(aim_depth=4)


cProfile.run('evaluation = s.search_alpha_beta(board)')
#cProfile.run('evaluation = s.search_bns(board, 0, 10)')
