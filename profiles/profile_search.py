#!/usr/bin/env python3

"""
Profile search
"""

import cProfile
import time

import gobychess
from gobychess.evaluation import Evaluator
from gobychess.search import Searcher

board = gobychess.Board()
# board.from_fen("r3k2N/ppp1q1pp/5n2/3Pp3/Q1Bn2b1/2P5/PP1P1bPP/RNB2K1R b q - 2 10")
board.from_fen("r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 4 4")

evaluator = Evaluator()
s = Searcher(evaluator, aim_depth=3)

cProfile.run('evaluation = s.search_negascout(board)')
