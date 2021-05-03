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

    def __init__(self, aim_depth=0, manage_time=True):
        self.manage_time = manage_time
        self.best_move = (None, None, None)
        self.evaluation = 0
        self.aim_depth = aim_depth
        self.wtime = 6000
        self.btime = 6000
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

            if time_per_move > 15:
                self.aim_depth = 5
            elif time_per_move > 2:
                self.aim_depth = 4
            elif self.wtime < 2000:
                self.aim_depth = 2
            else:
                self.aim_depth = 3

    def search_min_max(self, board):
        """
        search simple min max algorithm for position
        """
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
        """
        alpha beta search for aim_depth
        """
        if board.to_move == 1:
            evaluation = self.__alpha_beta_max(board, self.aim_depth, -100000, 100000)
        if board.to_move == 0:
            evaluation = self.__alpha_beta_min(board, self.aim_depth, -100000, 100000)
        return evaluation

    def __alpha_beta_max(self, board, depth, alpha, beta):
        moves = board.gen_legal_moves()
        if depth == 0 or board.is_check_or_stalemate():
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
        if depth == 0 or board.is_check_or_stalemate():
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

    def bns_alpha_beta(self, board, alpha, beta):
        '''
        Trying to implement bns search
        '''
        if board.to_move == 1:
            evaluation = self.__alpha_beta_max(board, self.aim_depth, alpha, beta)
        if board.to_move == 0:
            evaluation = self.__alpha_beta_min(board, self.aim_depth, alpha, beta)
        return evaluation

    def nextGuess(self, alpha, beta, subtreeCount):
        '''
        update test value
        '''
        return alpha + (beta - alpha) * (subtreeCount - 1) / subtreeCount

    def search_bns(self, board, alpha, beta):
        subtreeCount = sum(1 for _ in board.gen_legal_moves())

        test = self.nextGuess(alpha, beta, subtreeCount)
        betterCount = 0
        for move in board.gen_legal_moves():
            new_board = board.board_copy()
            new_board = new_board.make_generated_move(move)

            bestVal = -self.bns_alpha_beta(board, -test, -(test - 1))

            if bestVal >= test:
                betterCount = betterCount + 1
                self.bestNode = move

        if betterCount == subtreeCount:
            # reduce beta
            beta = test
        elif 1 < betterCount < subtreeCount:
            subtreeCount = betterCount
            alpha = test
        elif betterCount == 0:
            # and alpha-beta range is reduced to 1 ??
            betterCount == 1
            pass


        while not (beta - alpha) < 2 or betterCount == 1:
            test = self.nextGuess(alpha, beta, subtreeCount)
            betterCount = 0
            for move in board.gen_legal_moves():
                new_board = board.board_copy()
                new_board = new_board.make_generated_move(move)

                bestVal = -self.bns_alpha_beta(board, -test, -(test - 1))

                if bestVal >= test:
                    betterCount = betterCount + 1
                    self.bestNode = move

                if betterCount == subtreeCount:
                    # reduce beta
                    beta = test
                elif 1 < betterCount < subtreeCount:
                    subtreeCount = betterCount
                    alpha = test
                elif betterCount == 0:
                    # and alpha-beta range is reduced to 1 ??
                    break
