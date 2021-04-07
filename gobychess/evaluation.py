#!/usr/bin/env python3

import itertools

from .board import Board

from gmpy2 import popcount

MATE_SCORE = 100

def piece_scores(board):
    '''
    Calculate board score with only piece values

    Args:
        board (Board): board with position to evaluate

    Returns:
        float: score of current position
    '''
    piece_score = {0: 1, 1: 3, 2: 3, 3: 5, 4: 9, 5: 0}

    if board.is_checkmate():
        return (-1)**board.to_move * MATE_SCORE

    score = 0
    for color, piece in itertools.product(range(2), range(6)):
        score += (-1)**color * popcount(board.pieces[1 - color][piece]) * piece_score[piece]

    return score
