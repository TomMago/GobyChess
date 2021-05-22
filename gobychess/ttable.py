#!/usr/bin/env python3

ttable = {}

def board_entry(board, evaluation, best_move, occurances):
    """
    make entry for position with evaluation, best move, occurances
    """
    ttable[tuple(board.pieces[0]+board.pieces[1]+[board.to_move])] = (evaluation, best_move, occurances)
