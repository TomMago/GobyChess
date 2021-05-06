#!/usr/bin/env python3

import csv
import itertools

from .board import Board
from .utils import (forward_bit_scan, gen_ones, get_bit, reverse_bit_scan,
                    unset_bit)


class Evaluator:

    MATE_SCORE = 50000

    piece_score = [82, 337, 365, 477, 1025,  0]

    square_score_table = [
    # pawn
    (0,   0,   0,   0,   0,   0,  0,   0,
     -35,  -1, -20, -23, -15,  24, 38, -22,
     -26,  -4,  -4, -10,   3,   3, 33, -12,
     -27,  -2,  -5,  17,  20,   6, 10, -25,
     -14,  13,   6,  21,  23,  12, 17, -23,
     -6,   7,  26,  31,  65,  56, 25, -20,
     98, 134,  61,  95,  68, 126, 34, -11,
     0,   0,   0,   0,   0,   0,  0,   0),
    # knight
    (-105, -21, -58, -33, -17, -28, -19,  -23,
     -29, -53, -12,  -3,  -1,  18, -14,  -19,
     -23,  -9,  10,  10,  19,  10,  25,  -16,
     -13,   4,  16,  13,  28,  19,  21,   -8,
     -9,  17,  19,  53,  37,  69,  18,   22,
     -47,  60,  37,  65,  84, 129,  73,   44,
     -73, -41,  72,  36,  23,  62,   7,  -17,
     -167, -89, -34, -49,  61, -97, -15, -107),
    # bishop
    (-33,  -3, -14, -21, -13, -12, -39, -21,
     4,  15,  16,   0,   7,  21,  33,   1,
     0,  15,  15,  12,  12,  27,  18,  10,
     -6,  13,  13,  26,  34,  12,  10,   4,
     -4,   5,  19,  50,  37,  37,   7,  -2,
     -16,  37,  43,  40,  35,  50,  37,  -2,
     -26,  16, -18, -13,  30,  59,  18, -47,
     -29,   4, -82, -37, -25, -42,   7,  -8),
    # rook
    (-19, -13,   1,  17, 16,  7, -37, -26,
     -44, -16, -20,  -9, -1, 11,  -6, -71,
     -45, -25, -16, -17,  3,  0,  -5, -33,
     -36, -26, -12,  -1,  9, -7,   6, -23,
     -24, -11,   7,  26, 24, 35,  -8, -20,
     -5,  19,  26,  36, 17, 45,  61,  16,
     27,  32,  58,  62, 80, 67,  26,  44,
     32,  42,  32,  51, 63,  9,  31,  43),
    # queen
    (-1, -18,  -9,  10, -15, -25, -31, -50,
     -35,  -8,  11,   2,   8,  15,  -3,   1,
     -14,   2, -11,  -2,  -5,   2,  14,   5,
     -9, -26,  -9, -10,  -2,  -4,   3,  -3,
     -27, -27, -16, -16,  -1,  17,  -2,   1,
     -13, -17,   7,   8,  29,  56,  47,  57,
     -24, -39,  -5,   1, -16,  57,  28,  54,
     28,   0,  29,  12,  59,  44,  43,  45),
    # king
    (-15,  36,  12, -54,   8, -28,  24,  14,
     1,   7,  -8, -64, -43, -16,   9,   8,
     -14, -14, -22, -46, -44, -30, -15, -27,
     -49,  -1, -27, -39, -46, -44, -33, -51,
     -17, -20, -12, -27, -30, -25, -14, -36,
     -9,  24,   2, -16, -20,   6,  22, -22,
     29,  -1, -20,  -7,  -8,  -4, -38, -29,
     -65,  23,  16, -15, -56, -34,   2,  13)]

    def load_tables(self, square_score_path, piece_score_path):
        '''
        piece square table and piece scores can be load from csv files
        '''
        with open(square_score_path, newline='') as csvfile:
            self.square_score_table = ([list(map(int, i)) for i in csv.reader(csvfile)])
        with open(piece_score_path, newline='') as csvfile:
            self.piece_score = ([list(map(int, i))[0] for i in csv.reader(csvfile)])

    def piece_scores(self, board):
        """
        Calculate board score with only piece values

        Args:
            board (Board): board with position to evaluate

        Returns:
            float: score of current position
        """
        piece_score_sim = [1, 3, 3, 5, 9, 0]

        if board.is_checkmate():
            return (-1) ** board.to_move * self.MATE_SCORE

        score = 0
        for color, piece in itertools.product(range(2), range(6)):
            score += (-1)**color * bin(board.pieces[1 - color][piece]).count("1") * piece_score_sim[piece]

        return score


    def weighted_piece_scores(self, board):
        """
        Calculate board score with only piece values

        Args:
            board (Board): board with position to evaluate


        Returns:
            float: score of current position
        """

        # factor to favor faster mate
        if board.is_checkmate():
            return (-1) ** board.to_move * self.MATE_SCORE * (1 / (1 + board.fullmove_counter / 20) + 1)

        score = 0

        for piece in range(6):
            # white
            bitboard = board.pieces[1][piece]
            while bitboard:
                square = reverse_bit_scan(bitboard)
                score += self.piece_score[piece] + self.square_score_table[piece][square]
                bitboard = unset_bit(bitboard, square)

            # black
            bitboard = board.pieces[0][piece]
            while bitboard:
                square = reverse_bit_scan(bitboard)
                score -= self.piece_score[piece] + self.square_score_table[piece][square ^ 56]
                bitboard = unset_bit(bitboard, square)

        return score


    def eval_move(self, board, move):
        '''
        Evaluate board after move.
        Only relative evaluation to other moves.
        '''
        from_square, to_square, promotion = move
        if board.to_move:
            eval_from = from_square
            eval_to = to_square
        else:
            eval_from = from_square ^ 56
            eval_to = to_square ^ 56
        move_piece = board.piece_on(from_square)
        score = self.square_score_table[move_piece][eval_to] - self.square_score_table[move_piece][eval_to]
        if get_bit(board.all_pieces_color[1 - board.to_move], to_square):
            cap_piece = board.piece_opponent_on(to_square)
            score -= self.piece_score[cap_piece] + self.square_score_table[cap_piece][eval_to]
        if move_piece == 0:
            if not promotion is None:
                score += self.piece_score[promotion] + self.square_score_table[promotion][eval_to]
                score -= self.piece_score[0] + self.square_score_table[0][eval_to]
            if to_square == board.en_passant:
                score -= self.piece_score[0] + self.square_score_table[0][to_square + (-1) ** board.to_move * 8]
        if move_piece == 5 and abs(from_square - to_square) == 2:
            if from_square < to_square:
                score += self.square_score_table[3][eval_from + 1] - self.square_score_table[3][eval_from + 3]
            elif from_square > to_square:
                score += self.square_score_table[3][eval_from - 1] - self.square_score_table[3][eval_from - 4]

        return score
