#!/usr/bin/env python3

from textwrap import wrap

def gen_ones(bb):
    """
    Generator for getting all the ones in a bitboard
    """
    for i in range(0, bb.bit_length()):
        if bb & (1 << i):
            yield i

def forward_bit_scan(bitboard):
    """
    get least significant bit
    """
    return reverse_bit_scan(bitboard & -bitboard)


def reverse_bit_scan(bitboard):
    """
    get most significant bit
    """
    return bitboard.bit_length() - 1


def get_bit(bitboard, bit):
    """
    get bit of bitboard at position bit
    """
    return (bitboard & (1 << bit)) != 0


def unset_bit(bitboard, bit):
    """
    sets bit at position bit of bitboard to 1
    """
    return bitboard & ~(1 << bit)


def set_bit(bitboard, bit):
    """
    sets bit at position bit of bitboard to 1
    """
    return bitboard | (1 << bit)


def print_bitboard(board):
    """
    Print a bitboard
    """
    board = '{:064b}'.format(board)
    print('\n'.join([' '.join(wrap(line, 1))[::-1] for line in wrap(board, 8)]))


def bitboard_of_index(index):
    """
    bitboard from index of square

    Args:
        index (ind): Square index 0 - 64

    Returns:
        int: bitboard with bit at idnex set to 1
    """
    return (1 << index)


def index_of_square(square):
    """
    Index of square

    Args:
        square (String): Square in chess notation e.g. f7

    Returns:
        Int: Index of square in bitboard
    """
    line = ord(square[0].lower()) - ord('a')
    row = int(square[1])
    idx = 8 * (row - 1) + line
    return idx


def bitboard_of_square(square):
    """
    Bitboard for square

    Args:
        square (String): Square in chess notation e.g. f7

    Returns:
        int: Bitboard with 1 on respective square
    """
    idx = index_of_square(square)
    return 2**idx


def bitboard_from_squares(squares):
    """
    Bitboard for a string with multiple squares

    Args:
        squares (String): multiple chess squares seperated by whitespace

    Returns:
        int: Bitboard with 1 on respective squares
    """
    empty_bitboard = 0
    squares = squares.split()
    for square in squares:
        idx = index_of_square(square)
        empty_bitboard += 2**idx
    return empty_bitboard


def invert_bitboard(bitboard):
    """
    Invert a bitboard

    Args:
        bitboard (xmpz): some bitbaord

    Returns
        int: inverted bitboard, 0 and 1 switched for all bits
    """
    return (1 << 64) - 1 - bitboard


def perft(current_board, depth):
    """
    calculates number of moves of all branches for given depth

    Args:
        current_board (Board): current position
        depth (int): depth to calcualte

    Returns
        int: number of moves
    """
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
    """
    Get san string from move tuple
    """
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
    """
    Get move tuple from san
    """
    from_square = index_of_square(san[0:2])
    to_square = index_of_square(san[2:4])

    if len(san) == 5:
        promotion = promotion_from_char(san[4])
    else:
        promotion = None

    return (from_square, to_square, promotion)
