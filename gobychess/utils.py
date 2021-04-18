#!/usr/bin/env python3

from textwrap import wrap

import numpy as np
from gmpy2 import xmpz

from numba import njit

@njit
def forward_bit_scan(bitboard):
    i = 0
    while((bitboard >> np.uint64(i)) % 2 == 0):
        i += 1
    return i

@njit
def reverse_bit_scan(bitboard):
    i = 63
    while((bitboard >> np.uint64(i)) % 2 == 0):
        i -= 1
    return i

@njit
def get_bit(bitboard, bit):
    if np.bitwise_and(bitboard, np.uint64(2**bit)) == 0:
        return 0
    return 1


@njit
def unset_bit(bitboard, bit):
    '''
    sets bit at position bit of bitboard to 1
    '''
    return np.bitwise_and(bitboard, np.bitwise_not(np.uint64(2**bit)))

@njit
def set_bit(bitboard, bit):
    '''
    sets bit at position bit of bitboard to 1
    '''
    return np.bitwise_or(bitboard, np.uint64(2**bit))


def print_bitboard(board):
    '''
    Print a bitboard
    '''
    board = '{:064b}'.format(board)
    print('\n'.join([' '.join(wrap(line, 1))[::-1] for line in wrap(board, 8)]))

@njit
def bit_scan(bitboard):
    '''
    forward bitscan
    '''
    a = (2**np.arange(64) & bitboard)
    lead_zeros = 64-a.argmax()-1
    return 63 - lead_zeros

@njit
def bitboard_of_index(index):
    '''
    bitboard from index of square

    Args:
        index (ind): Square index 0 - 64

    Returns:
        xmpz: bitboard with bit at idnex set to 1
    '''
    bitboard = np.uint64(2**index)
    return bitboard

@njit
def index_of_square(square):
    '''
    Index of square

    Args:
        square (String): Square in chess notation e.g. f7

    Returns:
        Int: Index of square in bitboard
    '''
    line = ord(square[0].lower()) - ord('a')
    row = ord(square[1]) - ord('0')
    idx = 8 * (row - 1) + line
    return idx

@njit
def bitboard_of_square(square):
    '''
    Bitboard for square

    Args:
        square (String): Square in chess notation e.g. f7

    Returns:
        xmpz: Bitboard with 1 on respective square
    '''
    idx = index_of_square(square)
    empty_bitboard = np.uint64(2**idx)
    return empty_bitboard


def bitboard_from_squares(squares):
    '''
    Bitboard for a string with multiple squares

    Args:
        squares (String): multiple chess squares seperated by whitespace

    Returns:
        xmpz: Bitboard with 1 on respective squares
    '''
    empty_bitboard = np.uint64(0b0)
    squares = squares.split()
    for square in squares:
        idx = index_of_square(square)
        empty_bitboard = np.uint64(set_bit(empty_bitboard, idx))
    return empty_bitboard


def invert_bitboard(bitboard):
    '''
    Invert a bitboard

    Args:
        bitboard (xmpz): some bitbaord

    Returns
        xmpz: inverted bitboard, 0 and 1 switched for all bits
    '''
    return (1 << 64) - 1 - bitboard


def perft(current_board, depth):
    '''
    calculates number of moves of all branches for given depth

    Args:
        current_board (Board): current position
        depth (int): depth to calcualte

    Returns
        int: number of moves
    '''

    number_moves = 0
    if not depth:
        return 1
    for move in current_board.gen_legal_moves():
        new_board = current_board.board_copy()
        new_board = new_board.make_generated_move(move)
        number_moves += perft(new_board, depth - 1)
    return number_moves
