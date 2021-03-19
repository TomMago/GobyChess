#!/usr/bin/env python3

from textwrap import wrap

from gmpy2 import xmpz

def print_bitboard(board):
    '''
    Print a bitboard
    '''
    board = '{:064b}'.format(board)
    print('\n'.join([' '.join(wrap(line, 1))[::-1] for line in wrap(board, 8)]))


def reverse_bit_scan1(bitboard):
    '''
    Give index of most significant bit of xmpz bitboard

    Args:
        bitboard (xmpz): Input  bitboard

    Returns:
        index of most significant bit (int)
    '''
    length = bitboard.bit_length()
    if length == 0:
        return None
    return length - 1


def index_of_square(square):
    '''
    Index of square

    Args:
        square (String): Square in chess notation e.g. f7

    Returns:
        Int: Index of square in bitboard
    '''
    line = ord(square[0].lower()) - ord('a')
    row = int(square[1])
    idx = 8 * (row - 1) + line
    return idx


def bitboard_of_square(square):
    '''
    Bitboard for square

    Args:
        square (String): Square in chess notation e.g. f7

    Returns:
        xmpz: Bitboard with 1 on respective square
    '''
    idx = index_of_square(square)
    empty_bitboard = xmpz(0b00000000000000000000000000000000000000000000000000000000000000000)
    empty_bitboard[idx] = 1
    return empty_bitboard

def bitboard_from_squares(squares):
    '''
    Bitboard for a string with multiple squares

    Args:
        squares (String): multiple chess squares seperated by whitespace

    Returns:
        xmpz: Bitboard with 1 on respective squares
    '''
    empty_bitboard = xmpz(0b00000000000000000000000000000000000000000000000000000000000000000)
    squares = squares.split()
    for square in squares:
        idx = index_of_square(square)
        empty_bitboard[idx] = 1
    return empty_bitboard

def invert_bitboard(bitboard):
    return (1 << 64) - 1 - bitboard
