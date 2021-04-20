#!/usr/bin/env python3

import itertools

from .board import Board
from .utils import forward_bit_scan, reverse_bit_scan, unset_bit

MATE_SCORE = 100

square_score_table = {

    #pawn
    0: (1.00, 1.  , 1.  , 1.  , 1.  , 1.  , 1.  , 1.  ,
        0.77, 0.99, 0.87, 0.85, 0.9 , 1.16, 1.25, 0.85,
        0.83, 0.97, 0.97, 0.93, 1.02, 1.02, 1.22, 0.92,
        0.82, 0.99, 0.97, 1.08, 1.11, 1.04, 1.07, 0.83,
        0.91, 1.09, 1.04, 1.14, 1.15, 1.08, 1.11, 0.85,
        0.96, 1.05, 1.17, 1.21, 1.43, 1.37, 1.17, 0.87,
        1.65, 1.89, 1.41, 1.63, 1.45, 1.84, 1.23, 0.93,
        1.00, 1.  , 1.  , 1.  , 1.  , 1.  , 1.  , 1.),
    #knight
    1: (0.65, 0.93, 0.81, 0.89, 0.94, 0.91, 0.94, 0.92,
        0.9 , 0.82, 0.96, 0.99, 1.  , 1.06, 0.95, 0.94,
        0.92, 0.97, 1.04, 1.03, 1.06, 1.06, 1.08, 0.95,
        0.96, 1.01, 1.05, 1.04, 1.09, 1.06, 1.07, 0.97,
        0.97, 1.06, 1.06, 1.18, 1.12, 1.23, 1.06, 1.07,
        0.84, 1.2 , 1.12, 1.22, 1.28, 1.43, 1.24, 1.15,
        0.76, 0.86, 1.24, 1.12, 1.08, 1.21, 1.02, 0.94,
        0.44, 0.7 , 0.89, 0.84, 1.2 , 0.68, 0.95, 0.64),
    #bishop
    2: (0.89, 0.99, 0.95, 0.93, 0.96, 0.96, 0.87, 0.93,
        1.01, 1.05, 1.05, 1.  , 1.02, 1.07, 1.11, 1.  ,
        1.  , 1.05, 1.05, 1.02, 1.02, 1.09, 1.06, 1.03,
        0.98, 1.04, 1.04, 1.09, 1.11, 1.04, 1.03, 1.01,
        0.99, 1.02, 1.06, 1.17, 1.12, 1.12, 1.02, 0.99,
        0.95, 1.12, 1.14, 1.13, 1.12, 1.17, 1.12, 0.99,
        0.91, 1.05, 0.94, 0.96, 1.1 , 1.2 , 1.06, 0.84,
        0.9 , 1.01, 0.73, 0.88, 0.92, 0.86, 1.02, 0.97),
    #rook
    3: (0.96, 0.97, 1.  , 1.03, 1.03, 1.01, 0.93, 0.95,
        0.91, 0.97, 0.96, 0.98, 1.  , 1.02, 0.99, 0.86,
        0.91, 0.95, 0.97, 0.97, 1.01, 1.  , 0.99, 0.93,
        0.93, 0.95, 0.98, 1.  , 1.02, 0.99, 1.01, 0.95,
        0.95, 0.98, 1.01, 1.05, 1.05, 1.07, 0.98, 0.96,
        0.99, 1.04, 1.05, 1.07, 1.03, 1.09, 1.12, 1.03,
        1.05, 1.06, 1.12, 1.12, 1.16, 1.13, 1.05, 1.09,
        1.06, 1.08, 1.06, 1.1 , 1.13, 1.02, 1.06, 1.09),

    #queen
    4: ( 1.  , 0.98, 0.99, 1.01, 0.98, 0.97, 0.97, 0.94,
         0.96, 0.99, 1.01, 1.  , 1.01, 1.02, 1.  , 1.  ,
         0.98, 1.  , 0.99, 1.  , 0.99, 1.  , 1.02, 1.01,
         0.99, 0.97, 0.99, 0.99, 1.  , 1.  , 1.  , 1.  ,
         0.97, 0.97, 0.98, 0.98, 1.  , 1.02, 1.  , 1.  ,
         0.99, 0.98, 1.01, 1.01, 1.03, 1.06, 1.05, 1.06,
         0.97, 0.96, 0.99, 1.  , 0.98, 1.06, 1.03, 1.06,
         0.97, 1.  , 1.03, 1.01, 1.07, 1.05, 1.05, 1.05),
    #king
    5: ( 0.99, 1.02, 1.01, 0.97, 1.  , 0.99, 1.01, 1.01,
         1.  , 1.  , 1.  , 0.97, 0.98, 0.99, 1.  , 1.  ,
         0.99, 0.99, 0.99, 0.98, 0.98, 0.98, 0.99, 0.99,
         0.98, 1.  , 0.99, 0.98, 0.98, 0.98, 0.98, 0.97,
         0.99, 0.99, 0.99, 0.99, 0.98, 0.99, 0.99, 0.98,
         1.  , 1.01, 1.  , 0.99, 0.99, 1.  , 1.01, 0.99,
         1.01, 1.  , 0.99, 1.  , 1.  , 1.  , 0.98, 0.99,
         0.97, 1.01, 1.01, 0.99, 0.97, 0.98, 1.  , 1.01)

}

def piece_scores(board):
    """
    Calculate board score with only piece values

    Args:
        board (Board): board with position to evaluate

    Returns:
        float: score of current position
    """
    piece_score = {0: 1, 1: 3, 2: 3, 3: 5, 4: 9, 5: 0}

    if board.is_checkmate():
        return (-1) ** board.to_move * MATE_SCORE

    score = 0
    for color, piece in itertools.product(range(2), range(6)):
        #score += (-1)**color * popcount(board.pieces[1 - color][piece]) * piece_score[piece]
        pass

    return score


def weighted_piece_scores(board):
    """
    Calculate board score with only piece values

    Args:
        board (Board): board with position to evaluate

    Returns:
        float: score of current position
    """
    piece_score = {0: 1, 1: 3, 2: 3, 3: 5, 4: 9, 5: 20}

    if board.is_checkmate():
        return (-1) ** board.to_move * MATE_SCORE

    score = 0
    for piece in range(6):
        # white
        bitboard = board.pieces[1][piece]
        while bitboard:
            square = forward_bit_scan(bitboard)
            score += piece_score[piece] * square_score_table[piece][square]
            bitboard = unset_bit(bitboard, square)

        bitboard = board.pieces[0][piece]
        while bitboard:
            square = forward_bit_scan(bitboard)
            score -= piece_score[piece] * square_score_table[piece][63 - square]
            bitboard = unset_bit(bitboard, square)

    return score
