#!/usr/bin/env python3

from textwrap import wrap

from gmpy2 import xmpz


def print_bitboard(board):
    '''
    Print bitboard
    '''
    board = '{:064b}'.format(board)
    print('\n'.join([' '.join(wrap(line, 1))[::-1] for line in wrap(board, 8)]))


def generate_table():
    '''
    0 east
    1 south
    2 west
    3 north
    4 south east
    5 south west
    6
    '''
    table = {'east': [], 'north': [], 'west': [], 'south': [],
             'south east': [], 'south west': [], 'north west': [], 'north east': []}

    table['east'] = generate_direction(1)
    table['north'] = generate_direction(8)
    table['west'] = generate_direction(-1)
    table['south'] = generate_direction(-8)
    table['south east'] = generate_direction(-7)
    table['south west'] = generate_direction(-9)
    table['north west'] = generate_direction(7)
    table['north east'] = generate_direction(9)


    return table


def generate_direction(direction):
    '''
  noWe         nort         noEa
          +7    +8    +9
              \  |  /
  west    -1 <-  0 -> +1    east
              /  |  \
          -9    -8    -7
  soWe         sout         soEa

    '''
    directions = []
    for i in range(64):
        field_count = i
        attack_board = xmpz(0b0000000000000000000000000000000000000000000000000000000000000000)
        attack_board[i] = 1

        if(direction == +8):
            condition = lambda x: x < 56
        if(direction == -1):
            condition = lambda x: x % 8 != 0
        if(direction == -8):
            condition = lambda x: x > 7
        if(direction == +1):
            condition = lambda x: (x + 1) % 8 != 0
        if(direction == -7):
            condition = lambda x: (x > 7 and (x + 1) % 8 != 0)
        if(direction == -9):
            condition = lambda x: (x > 7 and x % 8 != 0)
        if(direction == 7):
            condition = lambda x: (x < 56 and x % 8 != 0)
        if(direction == 9):
            condition = lambda x: (x < 56 and (x + 1) % 8 != 0)

        while condition(field_count):
            field_count += direction
            attack_board[field_count] = 1

        directions.append(attack_board)

        #print_bitboard(attack_board)
        #print("===================")

    return directions



table = generate_table()

print_bitboard(table['south east'][13])
