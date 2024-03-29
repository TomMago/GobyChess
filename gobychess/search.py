#!/usr/bin/env python3

from .evaluation import Evaluator
from .utils import move_from_san, san_from_move
from .ttable import ttable, board_entry
import time

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
        self.past_positions = set()
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


    def search_iter(self, board):
        MAXDEPTH = 40
        depth = 1
        start_time = time.time()
        round_time = time.time()
        if board.to_move == 1:
            movetime = self.wtime / 1000 / max(30 - board.fullmove_counter, 10) + self.winc / 1000
        elif board.to_move == 0:
            movetime = self.btime / 1000 / max(30 - board.fullmove_counter, 10) + self.binc / 1000

        while depth <= MAXDEPTH and round_time - start_time < movetime / 2:
            self.aim_depth = depth
            self.s__negascout_tt(board, depth, -100000000, 100000000)
            print(f"info depth {depth}")
            depth += 1
            round_time = time.time()

    def search_negascout_tt(self, board):
        self.s__negascout_tt(board, self.aim_depth, -100000000, 100000000, first=False)

    def s__negascout_tt(self, board, depth, alpha, beta, first=True):

        storage = 1

        if not first and tuple(board.pieces[0]+board.pieces[1]+[board.to_move]) in self.past_positions:
            return 0

        tt_lookup = ttable.get(tuple(board.pieces[0]+board.pieces[1]+[board.to_move]))
        if tt_lookup and tt_lookup[2] >= depth:
            if tt_lookup[1] == 0:
                return tt_lookup[0]
            elif tt_lookup[1] == 1:
                alpha = max(alpha, tt_lookup[0])
            elif tt_lookup[1] == 2:
                beta = min(beta, tt_lookup[0])

            if alpha >= beta:
                return tt_lookup[0]

        if depth == 0 or board.is_check_or_stalemate():
            return self.quiescence(board, alpha, beta)

        for move in sorted(board.gen_legal_moves(), key=lambda move: self.evaluator.eval_move(board, move)):

            new_board = board.board_copy()
            new_board = new_board.make_generated_move(move)

            current_eval = -self.__negascout(new_board, depth - 1, -alpha - 1, -alpha, False)
            if current_eval > alpha and current_eval < beta:
                current_eval = -self.__negascout(new_board, depth - 1, -beta, -current_eval, False)

            if current_eval >= beta:
                ttable[tuple(board.pieces[0]+board.pieces[1]+[board.to_move])] = (beta, 2, depth)
                return current_eval


            if current_eval > alpha:
                alpha = current_eval
                storage = 0
                if depth == self.aim_depth:
                    self.best_move = move

            #if alpha >= beta:
            #    break

        ttable[tuple(board.pieces[0]+board.pieces[1]+[board.to_move])] = (alpha, storage, depth)

        return alpha

    def search_negamax_tt(self, board):
        self.__negamax_tt(board, self.aim_depth, -100000000, 100000000)

    def __negamax_tt(self, board, depth, alpha, beta, first=True):

        if not first and tuple(board.pieces[0]+board.pieces[1]+[board.to_move]) in self.past_positions:
            return 0

        a = alpha
        tt_lookup = ttable.get(tuple(board.pieces[0]+board.pieces[1]+[board.to_move]))
        if tt_lookup and tt_lookup[2] >= depth:
            if tt_lookup[1] == 0:
                return tt_lookup[0]
            elif tt_lookup[1] == 1:
                alpha = max(alpha, tt_lookup[0])
            elif tt_lookup[1] == 2:
                beta = min(beta, tt_lookup[0])

            if alpha >= beta:
                return tt_lookup[0]


        if depth ==0 or board.is_check_or_stalemate():
            return self.quiescence(board, alpha, beta)

        val = -100000000

        for move in sorted(board.gen_legal_moves(), key=lambda move: self.evaluator.eval_move(board, move)):

            new_board = board.board_copy()
            new_board = new_board.make_generated_move(move)
            val = max(val, -self.__negamax_tt(new_board, depth - 1, -beta, -alpha, first=False))

            if val > alpha:
                alpha = val
                if depth == self.aim_depth:
                    self.best_move = move

            if alpha >= beta:
                break

        if val <= a:
            ttable[tuple(board.pieces[0]+board.pieces[1]+[board.to_move])] = (val, 2, depth)
        elif val >= beta:
            ttable[tuple(board.pieces[0]+board.pieces[1]+[board.to_move])] = (val, 1, depth)
        else:
            ttable[tuple(board.pieces[0]+board.pieces[1]+[board.to_move])] = (val, 0, depth)

        return val


    def search_negascout(self, board):
        """
        Negascout search
        """
        print(f"info depth {self.aim_depth}")
        return self.__negascout(board, self.aim_depth, -10000000, 10000000)

    def __negascout(self, board, depth, alpha, beta, first=True):

        if not first and tuple(board.pieces[0]+board.pieces[1]+[board.to_move]) in self.past_positions:
            return 0

        if depth == 0 or board.is_check_or_stalemate():
            return self.quiescence(board, alpha, beta)
            #return (-1)**(1 - board.to_move) * self.evaluator.weighted_piece_scores(board)
        b = beta
        counter = 1
        current_eval = 0
        for move in sorted(board.gen_legal_moves(), key=lambda move: self.evaluator.eval_move(board, move)):

            if counter == 1:
                if depth == self.aim_depth:
                    self.best_move = move

            new_board = board.board_copy()
            new_board = new_board.make_generated_move(move)
            current_eval = -self.__negascout(new_board, depth - 1, -b, -alpha, False)
            if current_eval > alpha and current_eval < beta and counter > 1:
                current_eval = -self.__negascout(new_board, depth - 1, -beta, -alpha, False)

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
