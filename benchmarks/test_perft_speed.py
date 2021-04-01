#!/usr/bin/env python3

import gobychess

DEPTH = 3
ROUNDS = 30

def test_perft_base(benchmark):
    board = gobychess.Board()
    board.from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    benchmark.pedantic(
        gobychess.utils.perft,
        args=(board, DEPTH),
        rounds=ROUNDS,
        iterations=1
    )
