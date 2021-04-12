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


def bitboard_of_index(index):
    '''
    bitboard from index of square

    Args:
        index (ind): Square index 0 - 64

    Returns:
        xmpz: bitboard with bit at idnex set to 1
    '''
    empty_bitboard = xmpz(0b0)
    empty_bitboard[index] = 1
    return empty_bitboard


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
    empty_bitboard = xmpz(0b0)
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
    empty_bitboard = xmpz(0b0)
    squares = squares.split()
    for square in squares:
        idx = index_of_square(square)
        empty_bitboard[idx] = 1
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


def promotion_from_char(piece_char):
    piecetype_chars = {'n': 1, 'b': 2, 'r': 3, 'q': 4}
    return piecetype_chars[piece_char]

def promotion_from_piecetype(piecetype):
    piecetypes = {1: 'n', 2: 'b', 3: 'r', 4: 'q'}
    return piecetypes[piecetype]

def san_from_move(move):
    square_from, square_to, promotion = move

    string = ""

    row_from = str(square_from // 8 + 1)
    line_from = chr(ord('a') + (square_from % 8))

    row_to = str(square_to // 8 + 1)
    line_to = chr(ord('a') + (square_to % 8))


    string += line_from
    string += row_from
    string += line_to
    string += row_to

    if promotion:
        string += promotion_from_piecetype(promotion)


    return string


def move_from_san(san):
    from_square = index_of_square(san[0:2])
    to_square = index_of_square(san[2:4])

    if len(san) == 5:
        promotion = promotion_from_char(san[4])
    else:
        promotion = None

    return (from_square, to_square, promotion)
