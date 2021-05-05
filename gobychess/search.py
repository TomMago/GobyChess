#!/usr/bin/env python3

from .evaluation import Evaluator
from .utils import move_from_san, san_from_move


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

    def __init__(self, evaluator, aim_depth=0, manage_time=True):
        self.evaluator = evaluator
        self.manage_time = manage_time
        self.best_move = (None, None, None)
        self.evaluation = 0
        self.aim_depth = aim_depth
        self.wtime = 60000
        self.btime = 60000
        self.winc = 0
        self.binc = 0

    def update_depth(self, to_move, moves_played):
        """
        update the aim_depth for fixed depth searches based on times
        """
        if self.manage_time:
            if to_move == 1:
                time_per_move = self.wtime / 1000 / max(30 - moves_played, 10) + self.winc / 1000
            elif to_move == 0:
                time_per_move = self.btime / 1000 / max(30 - moves_played, 10) + self.binc / 1000

            if time_per_move > 30:
                self.aim_depth = 5
            elif time_per_move > 5:
                self.aim_depth = 4
            elif self.wtime < 1000:
                self.aim_depth = 2
            else:
                self.aim_depth = 3

    def quiescence(self, board, alpha, beta):
        """
        Quiecent search
        """
        stand_pat = (-1)**(1 - board.to_move) * self.evaluator.weighted_piece_scores(board)

        if(stand_pat >= beta):
            return beta

        delta = self.evaluator.piece_score[4]
        if(stand_pat < alpha - delta):
            return alpha

        if(alpha < stand_pat):
            alpha = stand_pat

        for move in sorted(board.gen_quiet_moves(), key=lambda move: self.evaluator.eval_move(board, move)):
            new_board = board.board_copy()
            new_board = new_board.make_generated_move(move)
            score = -self.quiescence(new_board, -beta, -alpha)

            if(score >= beta):
                return beta
            if(score > alpha):
                alpha = score

        return alpha

    def search_negascout(self, board):
        """
        Negascout search
        """
        return self.__negascout(board, self.aim_depth, -10000000, 10000000)

    def __negascout(self, board, depth, alpha, beta):
        if depth == 0:
            return self.quiescence(board, alpha, beta)
            #return (-1)**(1 - board.to_move) * self.evaluator.weighted_piece_scores(board)
        b = beta
        counter = 1

        for move in sorted(board.gen_legal_moves(), key=lambda move: self.evaluator.eval_move(board, move)):

            if counter == 1:
                if depth == self.aim_depth:
                    self.best_move = move

            new_board = board.board_copy()
            new_board = new_board.make_generated_move(move)
            current_eval = -self.__negascout(new_board, depth - 1, -b, -alpha)
            if current_eval > alpha and current_eval < beta and counter > 1:
                current_eval = -self.__negascout(new_board, depth - 1, -beta, -alpha)

            if current_eval > alpha:
                alpha = current_eval
                if depth == self.aim_depth:
                    self.best_move = move

            if alpha >= beta:
                return alpha

            b = alpha + 1
            counter += 1

        return alpha

    def search_min_max(self, board):
        """
        search min max algorithm for positio
        """
        if board.to_move == 1:
            evaluation = self.__min_max_max(board, self.aim_depth)
        if board.to_move == 0:
            evaluation = self.__min_max_min(board, self.aim_depth)
        return evaluation

    def __min_max_max(self, board, depth):
        moves = board.gen_legal_moves()
        if depth == 0 or board.is_checkmate() or board.is_stalemate():
            return self.evaluator.piece_scores(board)
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
            return self.evaluator.piece_scores(board)
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
        """
        alpha beta search for aim_depth
        """
        if board.to_move == 1:
            evaluation = self.__alpha_beta_max(board, self.aim_depth, -10000000, 10000000)
        if board.to_move == 0:
            evaluation = self.__alpha_beta_min(board, self.aim_depth, -10000000, 10000000)
        return evaluation

    def __alpha_beta_max(self, board, depth, alpha, beta):
        moves = board.gen_legal_moves()
        if depth == 0 or board.is_check_or_stalemate():
            return self.evaluator.weighted_piece_scores(board)
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
        if depth == 0 or board.is_check_or_stalemate():
            return self.evaluator.weighted_piece_scores(board)
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
