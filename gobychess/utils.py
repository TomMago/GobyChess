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


def index_of_sqare(square):
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
    idx = index_of_sqare(square)
    empty_bitboard = xmpz(0b00000000000000000000000000000000000000000000000000000000000000000)
    empty_bitboard[idx] = 1
    return empty_bitboard


print_bitboard(bitboard_of_square('f6') | bitboard_of_square('d4'))
print()
print_bitboard(xmpz(0b00000000000000000000000000000100000000000000001001100101100000000))
