#!/usr/bin/env python3

import itertools

from .board import Board

from gmpy2 import popcount, bit_scan1

MATE_SCORE = 100

square_score_table = {
    # pawn
    0: (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
        1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
        0.9, 0.9, 1.1, 1.3, 1.3, 1.1, 0.9, 0.9,
        0.9, 1.0, 1.1, 1.2, 1.2, 1.1, 1.0, 0.9,
        1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
        1.1, 1.2, 1.3, 1.3, 1.3, 1.3, 1.2, 1.1,
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
    # knight
    1: (0.6, 0.9, 0.8, 0.8, 0.8, 0.8, 0.9, 0.6,
        0.7, 0.8, 0.9, 0.9, 0.9, 0.9, 0.8, 0.7,
        0.8, 1.0, 1.0, 1.1, 1.1, 1.0, 1.0, 0.8,
        0.8, 1.0, 1.1, 1.2, 1.2, 1.1, 1.0, 0.8,
        0.9, 1.1, 1.2, 1.2, 1.2, 1.1, 1.1, 0.9,
        0.9, 1.2, 1.3, 1.3, 1.3, 1.3, 1.2, 0.9,
        1.1, 1.2, 1.4, 1.3, 1.3, 1.4, 1.3, 1.1,
        0.9, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.9),
    # bishop
    2: (0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9,
        0.7, 1.1, 1.0, 0.9, 0.9, 1.0, 1.1, 0.7,
        0.9, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.9,
        0.9, 1.1, 1.1, 1.2, 1.2, 1.1, 1.1, 0.9,
        0.9, 1.1, 1.1, 1.2, 1.2, 1.1, 1.1, 0.9,
        0.9, 1.1, 1.2, 1.2, 1.2, 1.2, 1.1, 0.9,
        1.0, 1.1, 1.2, 1.2, 1.2, 1.2, 1.1, 1.0,
        0.9, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.9),
    # rook
    3: (1.0, 1.0, 1.1, 1.1, 1.1, 1.1, 1.0, 1.0,
        0.9, 1.0, 1.1, 1.1, 1.1, 1.1, 1.0, 0.9,
        0.9, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.9,
        0.9, 1.0, 1.0, 1.1, 1.1, 1.0, 1.0, 0.9,
        0.9, 1.0, 1.0, 1.1, 1.1, 1.0, 1.0, 0.9,
        0.9, 1.0, 1.1, 1.1, 1.1, 1.1, 1.0, 0.9,
        1.0, 1.1, 1.2, 1.2, 1.2, 1.2, 1.1, 1.0,
        0.9, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 0.9),
    # queen
    4: (0.9, 1.0, 1.1, 1.1, 1.1, 1.1, 1.0, 0.9,
        0.9, 1.0, 1.1, 1.1, 1.1, 1.1, 1.0, 0.9,
        0.9, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.9,
        0.9, 1.0, 1.0, 1.2, 1.2, 1.0, 1.0, 0.9,
        0.9, 1.0, 1.0, 1.2, 1.2, 1.0, 1.0, 0.9,
        0.9, 1.1, 1.2, 1.2, 1.2, 1.2, 1.0, 0.9,
        1.0, 1.1, 1.2, 1.2, 1.2, 1.2, 1.1, 1.0,
        0.9, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 0.9),
    # king
    5: (1.1, 1.1, 1.1, 1.0, 1.0, 1.1, 1.1, 1.1,
        1.0, 1.0, 1.0, 0.9, 0.9, 1.0, 1.0, 1.0,
        0.9, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.9,
        0.9, 1.0, 1.0, 1.1, 1.1, 1.0, 1.0, 0.9,
        0.9, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.9,
        0.9, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.9,
        1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
        0.9, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.9)}


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
        score += (-1) ** color * popcount(board.pieces[1 - color][piece]) * piece_score[piece]

    return score


def weighted_piece_scores(board):
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
    for piece in range(6):
        # white
        bitboard = board.pieces[1][piece].copy()
        while bitboard:
            square = bit_scan1(bitboard)
            score += piece_score[piece] * square_score_table[piece][square]
            bitboard[square] = 0

        bitboard = board.pieces[0][piece].copy()
        while bitboard:
            square = bit_scan1(bitboard)
            score -= piece_score[piece] * square_score_table[piece][63 - square]
            bitboard[square] = 0

    return score
