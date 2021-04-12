#!/usr/bin/env python3

from .evaluation import piece_scores


def simple_min_max(board, depth, color):
    if color == 1:
        evaluation, best_move = search_max(board, depth, depth)
    if color == 0:
        evaluation, best_move = search_min(board, depth, depth)
    return evaluation, best_move

def search_max(board, depth, aim_depth):
    moves = board.gen_legal_moves()
    best_move = (None, None, None)
    if depth == 0 or board.is_checkmate() or board.is_stalemate():
        return piece_scores(board), best_move
    max_eval = -10000
    for move in moves:
        new_board = board.board_copy()
        new_board = new_board.make_generated_move(move)
        current_eval, current_best_move = search_min(new_board, depth - 1, aim_depth)
        if current_eval > max_eval:
            max_eval = current_eval
            if depth == aim_depth:
                best_move = move
    return max_eval, best_move


def search_min(board, depth, aim_depth):
    moves = board.gen_legal_moves()
    best_move = (None, None, None)
    if depth == 0 or board.is_checkmate() or board.is_stalemate():
        return piece_scores(board), best_move
    min_eval = 10000
    for move in moves:
        new_board = board.board_copy()
        new_board = new_board.make_generated_move(move)
        current_eval, current_best_move = search_max(new_board, depth - 1, aim_depth)
        if current_eval < min_eval:
            min_eval = current_eval
            if depth == aim_depth:
                best_move = move
    return min_eval, best_move


def alpha_beta_search(board, depth, color):
    if color == 'b':
        evaluation, best_move = alpha_beta_max(board, depth, depth, -10000, 10000)
    if color == 'w':
        evaluation, best_move = alpha_beta_min(board, depth, depth, -10000, 10000)
    return evaluation, best_move


def alpha_beta_max(board, depth, aim_depth, alpha, beta):
    moves = board.gen_legal_moves()
    best_move = (None, None, None)
    if depth == 0 or not moves:
        return piece_scores(board), best_move
    max_eval = alpha
    for move in moves:
        new_board = board.board_copy()
        new_board = new_board.make_generated_move(move)
        current_eval, current_best_move = alpha_beta_min(board, depth - 1,
                                                         aim_depth, max_eval, beta)
        if current_eval > max_eval:
            max_eval = current_eval
            if depth == aim_depth:
                best_move = move
            if max_eval >= beta:
                break

    return max_eval, best_move


def alpha_beta_min(board, depth, aim_depth, alpha, beta):
    moves = board.gen_legal_moves()
    best_move = (None, None, None)
    if depth == 0 or not moves:
        return piece_scores(board), best_move
    min_eval = beta
    for move in moves:
        new_board = board.board_copy()
        new_board = new_board.make_generated_move(move)
        current_eval, current_best_move = alpha_beta_max(board, depth - 1,
                                                         aim_depth, alpha, min_eval)
        if current_eval < min_eval:
            min_eval = current_eval
            #if depth == aim_depth:
            #    best_move = move
            if min_eval <= alpha:
                break

    return min_eval, best_move
