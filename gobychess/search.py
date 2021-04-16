#!/usr/bin/env python3

from .evaluation import piece_scores, weighted_piece_scores


class Searcher:
    """
    Searcher Object can execute different searches with given settings

    Searcher stores current best move in best move variable best_move
    Searcher tries to optimize score of position for color to move.
    Score is absolute, meaning negative values are good for black,
    while positive are good for white.
    Therefore the search will try to minimize the score if black is to move
    and maximize it otherwise.
    """

    def __init__(self, aim_depth=0):
        self.best_move = (None, None, None)
        self.evaluation = 0
        self.aim_depth = aim_depth

    def search_min_max(self, board):
        if board.to_move == 1:
            evaluation = self.__min_max_max(board, self.aim_depth)
        if board.to_move == 0:
            evaluation = self.__min_max_min(board, self.aim_depth)
        return evaluation

    def __min_max_max(self, board, depth):
        moves = board.gen_legal_moves()
        if depth == 0 or board.is_checkmate() or board.is_stalemate():
            return piece_scores(board)
        max_eval = -10000
        for move in moves:
            new_board = board.board_copy()
            new_board = new_board.make_generated_move(move)
            current_eval = self.__min_max_min(new_board, depth - 1)
            if current_eval > max_eval:
                max_eval = current_eval
                if depth == self.aim_depth:
                    self.best_move = move
        return max_eval

    def __min_max_min(self, board, depth):
        moves = board.gen_legal_moves()
        if depth == 0 or board.is_checkmate() or board.is_stalemate():
            return piece_scores(board)
        min_eval = 10000
        for move in moves:
            new_board = board.board_copy()
            new_board = new_board.make_generated_move(move)
            current_eval = self.__min_max_max(new_board, depth - 1)
            if current_eval < min_eval:
                min_eval = current_eval
                if depth == self.aim_depth:
                    self.best_move = move
        return min_eval

    def search_alpha_beta(self, board):
        if board.to_move == 1:
            evaluation = self.__alpha_beta_max(board, self.aim_depth, -100000, 100000)
        if board.to_move == 0:
            evaluation = self.__alpha_beta_min(board, self.aim_depth, -100000, 100000)
        return evaluation

    def __alpha_beta_max(self, board, depth, alpha, beta):
        moves = board.gen_legal_moves()
        if depth == 0 or board.is_checkmate() or board.is_stalemate():
            return weighted_piece_scores(board)
        max_eval = alpha
        for move in moves:
            new_board = board.board_copy()
            new_board = new_board.make_generated_move(move)
            current_eval = self.__alpha_beta_min(new_board, depth - 1,
                                                 max_eval, beta)
            if current_eval > max_eval:
                max_eval = current_eval
                if depth == self.aim_depth:
                    self.best_move = move
                if max_eval >= beta:
                    break

        return max_eval

    def __alpha_beta_min(self, board, depth, alpha, beta):
        moves = board.gen_legal_moves()
        if depth == 0 or board.is_checkmate() or board.is_stalemate():
            return weighted_piece_scores(board)
        min_eval = beta
        for move in moves:
            new_board = board.board_copy()
            new_board = new_board.make_generated_move(move)
            current_eval = self.__alpha_beta_max(new_board, depth - 1,
                                                 alpha, min_eval)
            if current_eval < min_eval:
                min_eval = current_eval
                if depth == self.aim_depth:
                    self.best_move = move
                if min_eval <= alpha:
                    break

        return min_eval
