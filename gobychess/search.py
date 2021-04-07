#!/usr/bin/env python3

from .evaluation import piece_scores


def simple_min_max(board, depth):
    evaluation = search_max(board, depth, depth)
    return evaluation


def search_max(board, depth, aim_depth):
    moves = board.gen_legal_moves()
    if depth == 0 or not moves:
        return piece_scores(board), (None, None, None)
    max_eval = -10000
    best_move = (None, None, None)
    for move in moves:
        new_board = board.board_copy()
        new_board = new_board.make_generated_move(move)
        current_eval = search_min(new_board, depth - 1, aim_depth)
        if current_eval > max_eval:
            max_eval = current_eval
            if depth == aim_depth:
                best_move = move
    return max_eval, best_move


def search_min(board, depth, aim_depth):

    moves = board.gen_legal_moves()
    if depth == 0 or not moves:
        return piece_scores(board)
    min_eval = 10000
    for move in moves:
        new_board = board.board_copy()
        new_board = new_board.make_generated_move(move)
        current_eval, current_best_move = search_max(new_board, depth - 1, aim_depth)
        if current_eval < min_eval:
            min_eval = current_eval
    return min_eval
