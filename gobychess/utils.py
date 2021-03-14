#!/usr/bin/env python3

from textwrap import wrap

from gmpy2 import xmpz, bit_scan1,  bit_clear

EMPTY = xmpz(0b0000000000000000000000000000000000000000000000000000000000000000)

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
        attack_board[i] = 0

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


blockers = xmpz(0b0000000000000000000000000000000000000000000000000000000000000000)
blockers[21] = 1
blockers[23] = 1


def blocker_computation(square, blockers_opposite, blockers_own, direction):
    collision_opposite = table[direction][square] & blockers_opposite
    collision_own = table[direction][square] & blockers_own
    if(direction in ['east', 'north east', 'north', 'north west']):
        idx_opposite = bit_scan1(collision_opposite) if bit_scan1(collision_opposite) else 66
        idx_own = bit_scan1(collision_own) if bit_scan1(collision_own) else 66
    if(direction in ['west', 'south west', 'south', 'south east']):
        idx_opposite = reverse_bit_scan1(collision_opposite) if reverse_bit_scan1(collision_opposite) else 66
        idx_own = reverse_bit_scan1(collision_own) if reverse_bit_scan1(collision_own) else 66

    # print("=====================")
    # print_bitboard(collision_opposite)
    # print("=====================")
    # print_bitboard(collision_own)
    # print("=====================")
    # print(idx_opposite)
    # print(idx_own)

    if idx_opposite == 66 and idx_own == 66:
        blocked = xmpz(0b0000000000000000000000000000000000000000000000000000000000000000)
    elif idx_opposite < idx_own:
        idx = idx_opposite
        blocked = table[direction][idx]
        #print("opp: " + str(idx))
    else:
        idx = idx_own - 1
        blocked = table[direction][idx]
        #print("own" + str(idx))

    blocked = (1 << 64) - 1 - blocked
    movement = table[direction][square] & blocked
    return movement


def rook_sliding(square, blockers_opposite, blockers_own):

    pass


def reverse_bit_scan1(bitboard):
    length = bitboard.bit_length()
    if length == 0:
        return None
    else:
        return length - 1


empty = xmpz(0b0000000000000000000000000000000000000000000000000000000000000000)

print_bitboard(blockers)
print()
print_bitboard(blocker_computation(17, blockers, empty, 'east'))
print()
print_bitboard(blocker_computation(17, blockers, empty, 'north'))
print()
print_bitboard(blocker_computation(17, blockers, empty, 'west'))
print()
print_bitboard(blocker_computation(17, blockers, empty, 'south'))



#rook_sliding(17, empty, blockers)
#print()
#rook_sliding(17, blockers, empty)
