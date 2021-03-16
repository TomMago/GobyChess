#!/usr/bin/env python3

from gmpy2 import bit_scan1, xmpz

from .utils import print_bitboard, reverse_bit_scan1

def generate_table():
    '''
    Generate table of sliding moves in all directions

    Returns:
        move_table (dict): for each direction sliding moves for
                           each square as xmpz bitboard
    '''
    move_table = {'east': [], 'north': [], 'west': [], 'south': []
                  , 'south east': [], 'south west': [], 'north west': [], 'north east': []}

    move_table['east'] = generate_direction(1)
    move_table['north'] = generate_direction(8)
    move_table['west'] = generate_direction(-1)
    move_table['south'] = generate_direction(-8)
    move_table['south east'] = generate_direction(-7)
    move_table['south west'] = generate_direction(-9)
    move_table['north west'] = generate_direction(7)
    move_table['north east'] = generate_direction(9)

    return move_table


def generate_direction(direction):
    ''' Generate sliding moves for every square for certain direction.


        noWe         nort         noEa
                +7    +8    +9
                    \  |  /
        west    -1 <-  0 -> +1    east
                    /  |  \
                -9    -8    -7
        soWe         sout         soEa

    Args:
        direction (int): Direction to generate see top diagram

    Returns:
        Array: xmpz bitboard of moves for each square (length 64)
    '''
    directions = []
    for i in range(64):
        field_count = i
        attack_board = xmpz(0b0000000000000000000000000000000000000000000000000000000000000000)
        attack_board[i] = 0

        if direction == +8:
            def condition(field):
                return field < 56
        elif direction == -1:
            def condition(field):
                return field % 8 != 0
        elif direction == -8:
            def condition(field):
                return field > 7
        elif direction == +1 :
            def condition(field):
                return (field + 1) % 8 != 0
        elif direction == -7:
            def condition(field):
                return field > 7 and (field + 1) % 8 != 0
        elif direction == -9:
            def condition(field):
                return field > 7 and field % 8 != 0
        elif direction == 7:
            def condition(field):
                return field < 56 and field % 8 != 0
        elif direction == 9:
            def condition(field):
                return field < 56 and (field + 1) % 8 != 0

        while condition(field_count):
            field_count += direction
            attack_board[field_count] = 1

        directions.append(attack_board)

    return directions


table = generate_table()


def rook_sliding(square, blockers):
    '''
    Generates bitboard of all attack squares for the rook with given blockers

    Args:
        square (int): Index of the square of the rook
        blockers: Bitboard of all other pieces on the board

    Returns:
        xmpz bitboard of attacked squares
    '''

    attacks = table['east'][square]
    if table['east'][square] & blockers:
        idx = bit_scan1(table['east'][square] & blockers)
        attacks = attacks & ((1 << 64) - 1 - table['east'][idx])

    attacks |= table['north'][square]
    if table['north'][square] & blockers:
        idx = bit_scan1(table['north'][square] & blockers)
        attacks = attacks & ((1 << 64) - 1 - table['north'][idx])

    attacks |= table['west'][square]
    if table['west'][square] & blockers:
        idx = reverse_bit_scan1(table['west'][square] & blockers)
        attacks = attacks & ((1 << 64) - 1 - table['west'][idx])

    attacks |= table['south'][square]
    if table['south'][square] & blockers:
        idx = reverse_bit_scan1(table['south'][square] & blockers)
        attacks = attacks & ((1 << 64) - 1 - table['south'][idx])

    return attacks


def bishop_sliding(square, blockers):
    '''
    Generates bitboard of all attack squares for the bishop with given blockers

    Args:
        square (int): Index of the square of the rook
        blockers: Bitboard of all other pieces on the board

    Returns:
        xmpz bitboard of attacked squares
    '''
    attacks = table['north east'][square]
    if table['north east'][square] & blockers:
        idx = bit_scan1(table['north east'][square] & blockers)
        attacks = attacks & ((1 << 64) - 1 - table['north east'][idx])

    attacks |= table['north west'][square]
    if table['north west'][square] & blockers:
        idx = bit_scan1(table['north west'][square] & blockers)
        attacks = attacks & ((1 << 64) - 1 - table['north west'][idx])

    attacks |= table['south west'][square]
    if table['south west'][square] & blockers:
        idx = reverse_bit_scan1(table['south west'][square] & blockers)
        attacks = attacks & ((1 << 64) - 1 - table['south west'][idx])

    attacks |= table['south east'][square]
    if table['south east'][square] & blockers:
        idx = reverse_bit_scan1(table['south east'][square] & blockers)
        attacks = attacks & ((1 << 64) - 1 - table['south east'][idx])

    return attacks


def queen_sliding(square, blockers):
    '''
    Generates bitboard of all attack squares for the queen with given blockers

    Args:
        square (int): Index of the square of the rook
        blockers: Bitboard of all other pieces on the board

    Returns:
        xmpz bitboard of attacked squares
    '''
    attacks = rook_sliding(square, blockers) | bishop_sliding(square, blockers)

    return attacks






# blockers = xmpz(0b0000000000000000000000000000000000000000000000000000000000000000)
# blockers[21] = 1
# blockers[23] = 1
#
#
#
# empty = xmpz(0b0000000000000000000000000000000000000000000000000000000000000000)
#
# print_bitboard(blockers)
# print()
#
# # print_bitboard(rook_sliding(17, blockers))
# # print()
# # print_bitboard(rook_sliding(45, blockers))
# # print()
# # print_bitboard(rook_sliding(7, blockers))
# # print()
# # print_bitboard(rook_sliding(22, blockers))
#
# # print_bitboard(bishop_sliding(28, blockers))
# # print()
# # print_bitboard(bishop_sliding(45, blockers))
# # print()
# # print_bitboard(bishop_sliding(7, blockers))
# # print()
# # print_bitboard(bishop_sliding(22, blockers))
#
# print_bitboard(queen_sliding(28, blockers))
# print()
# print_bitboard(queen_sliding(45, blockers))
# print()
# print_bitboard(queen_sliding(7, blockers))
# print()
# print_bitboard(queen_sliding(22, blockers))
#
#

#rook_sliding(17, empty, blockers)
#print()
#rook_sliding(17, blockers, empty)
