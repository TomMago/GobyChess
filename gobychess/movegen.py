#!/usr/bin/env python3

from gmpy2 import bit_scan1, xmpz, bit_clear

from .utils import print_bitboard, reverse_bit_scan1, invert_bitboard, bitboard_of_index


def generate_non_sliding():
    move_table = {'pawn white capture': [], 'pawn black capture': [],
                  'pawn white move': [], 'pawn black move': [],
                  'knight': [], 'king': []}

    move_table['knight'] = generate_knight()
    move_table['king'] = generate_king()
    move_table['pawn white move'] = generate_white_pawn_move()
    move_table['pawn white capture'] = generate_white_pawn_capture()
    move_table['pawn black move'] = generate_black_pawn_move()
    move_table['pawn black capture'] = generate_black_pawn_capture()
    return move_table

def generate_white_pawn_move():
    '''
    Generate all non capturing pawn moves for white for every sqare

    Returns:
        moves (xmpz array): array of bitboards of moves for all 64 squares
    '''
    moves = []
    for i in range(64):
        attack_board = xmpz(0b0000000000000000000000000000000000000000000000000000000000000000)
        if i <= 7 or i >= 56:
            pass
        elif i // 8 == 1:
            attack_board[i + 8] = 1
            attack_board[i + 16] = 1
        else:
            attack_board[i + 8] = 1
        moves.append(attack_board)
    return moves

def generate_white_pawn_capture():
    '''
    Generate all capturing pawn moves for white for every sqare

    Returns:
        moves (xmpz array): array of bitboards of moves for all 64 squares
    '''
    moves = []
    for i in range(64):
        attack_board = xmpz(0b0000000000000000000000000000000000000000000000000000000000000000)
        if i > 7 and i < 56:
            if (i % 8) != 0:
                attack_board[i + 7] = 1
            if (i + 1) % 8 != 0:
                attack_board[i + 9] = 1
        moves.append(attack_board)
    return moves


def generate_black_pawn_move():
    '''
    Generate all non capturing pawn moves for white for every sqare

    Returns:
        moves (xmpz array): array of bitboards of moves for all 64 squares
    '''
    moves = []
    for i in range(64):
        attack_board = xmpz(0b0000000000000000000000000000000000000000000000000000000000000000)
        if i <= 7 or i >= 56:
            pass
        elif i // 8 == 6:
            attack_board[i - 8] = 1
            attack_board[i - 16] = 1
        else:
            attack_board[i - 8] = 1
        moves.append(attack_board)
    return moves

def generate_black_pawn_capture():
    '''
    Generate all capturing pawn moves for white for every sqare

    Returns:
        moves (xmpz array): array of bitboards of moves for all 64 squares
    '''
    moves = []
    for i in range(64):
        attack_board = xmpz(0b0000000000000000000000000000000000000000000000000000000000000000)
        if i > 7 and i < 56:
            if (i % 8) != 0:
                attack_board[i - 9] = 1
            if (i + 1) % 8 != 0:
                attack_board[i - 7] = 1
        moves.append(attack_board)
    return moves



def generate_king():
    '''
    Generate all king moves for every square

    Returns:
        moves (xmpz array): array of bitboards of moves for all 64 squares
    '''
    moves = []
    for i in range(64):
        attack_board = xmpz(0b0000000000000000000000000000000000000000000000000000000000000000)
        if (i + 1) % 8 != 0:
            attack_board[i + 1] = 1
        if i % 8 != 0:
            attack_board[i - 1] = 1
        if (i + 1) % 8 != 0 and (i + 9) <= 63:
            attack_board[i + 9] = 1
        if (i + 1) % 8 != 0 and (i - 7) > 0:
            attack_board[i - 7] = 1
        if (i + 8) <= 63:
            attack_board[i + 8] = 1
        if (i - 8) >= 0:
            attack_board[i - 8] = 1
        if i % 8 != 0 and (i + 7) <= 63:
            attack_board[i + 7] = 1
        if i % 8 != 0 and (i - 9) > 0:
            attack_board[i - 9] = 1
        print(i)
        print_bitboard(attack_board)
        moves.append(attack_board)
    return moves


def generate_knight():
    '''
    Generate all knight moves for every square

    Returns:
        moves (xmpz array): array of bitboards of moves for all 64 squares
    '''
    moves = []
    for i in range(64):
        attack_board = xmpz(0b0000000000000000000000000000000000000000000000000000000000000000)

        possible_directions = []
        if i % 8 > 0:
            possible_directions.append(15)
            possible_directions.append(-17)
        if i % 8 > 1:
            possible_directions.append(6)
            possible_directions.append(-10)
        if i % 8 < 7:
            possible_directions.append(17)
            possible_directions.append(-15)
        if i % 8 < 6:
            possible_directions.append(-6)
            possible_directions.append(10)
        for j in possible_directions:
            field = i + j
            if 0 <= field <= 63:
                attack_board[field] = 1
        print(i)
        print_bitboard(attack_board)
        moves.append(attack_board)
    return moves


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
non_sliding = generate_non_sliding()


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
        attacks = attacks & invert_bitboard(table['east'][idx])

    attacks |= table['north'][square]
    if table['north'][square] & blockers:
        idx = bit_scan1(table['north'][square] & blockers)
        attacks = attacks & invert_bitboard(table['north'][idx])

    attacks |= table['west'][square]
    if table['west'][square] & blockers:
        idx = reverse_bit_scan1(table['west'][square] & blockers)
        attacks = attacks & invert_bitboard(table['west'][idx])

    attacks |= table['south'][square]
    if table['south'][square] & blockers:
        idx = reverse_bit_scan1(table['south'][square] & blockers)
        attacks = attacks & invert_bitboard(table['south'][idx])

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
        attacks = attacks & invert_bitboard(table['north east'][idx])

    attacks |= table['north west'][square]
    if table['north west'][square] & blockers:
        idx = bit_scan1(table['north west'][square] & blockers)
        attacks = attacks & invert_bitboard(table['north west'][idx])

    attacks |= table['south west'][square]
    if table['south west'][square] & blockers:
        idx = reverse_bit_scan1(table['south west'][square] & blockers)
        attacks = attacks & invert_bitboard(table['south west'][idx])

    attacks |= table['south east'][square]
    if table['south east'][square] & blockers:
        idx = reverse_bit_scan1(table['south east'][square] & blockers)
        attacks = attacks & invert_bitboard(table['south east'][idx])

    return attacks


def queen_sliding(square, blockers):
    '''
    Generates bitboard of all attack squares for the queen with given blockers

    Args:
        square (int): Index of the square of the rook
        blockers (xmpz): Bitboard of all other pieces on the board

    Returns:
        xmpz bitboard of attacked squares
    '''
    attacks = rook_sliding(square, blockers) | bishop_sliding(square, blockers)

    return attacks


def yield_moveset(square, moveset):
    '''
    yield all moves of a piece from one square to all squares on a bitboard
    '''
    while moveset:
        index_to = bit_scan1(moveset)
        yield (square, index_to, None)
        moveset = moveset.bit_clear(index_to)


def yield_promotion_moveset(square, moveset):
    '''
    yield all moves of a piece from one square to all squares on a bitboard
    '''
    while moveset:
        index_to = bit_scan1(moveset)
        for i in [1, 2, 3, 4]:
            yield (square, index_to, i)
        moveset = moveset.bit_clear(index_to)


def gen_bishop_moves(bishop_bitboard, all_pieces, own_pieces):
    '''
    generate bishop moves

    Args:
        bishop_bitboard (xmpz): Bitboard of positions of bishops
        all_pieces (xmpz): Bitboard of all other pieces on the board

    Returns:
        generator for all bishop moves gives 3 tuples (from, to, promote)
    '''
    while bishop_bitboard:
        bishop_square = bit_scan1(bishop_bitboard)
        attack_bitboard = bishop_sliding(bishop_square, all_pieces)
        bishop_bitboard = bishop_bitboard.bit_clear(bishop_square)
        moveset = attack_bitboard & invert_bitboard(own_pieces)
        yield from yield_moveset(bishop_square, moveset)


def gen_rook_moves(rook_bitboard, all_pieces, own_pieces):
    '''
    generate rook moves

    Args:
        rook_bitboard (xmpz): Bitboard of positions of rooks
        all_pieces (xmpz): Bitboard of all other pieces on the board

    Returns:
        generator for all rook moves gives 3 tuples (from, to, promote)
    '''
    while rook_bitboard:
        rook_square = bit_scan1(rook_bitboard)
        attack_bitboard = rook_sliding(rook_square, all_pieces)
        rook_bitboard = rook_bitboard.bit_clear(rook_square)
        moveset = attack_bitboard & invert_bitboard(own_pieces)
        yield from yield_moveset(rook_square, moveset)


def gen_queen_moves(queen_bitboard, all_pieces, own_pieces):
    '''
    generate queen moves

    Args:
        queen_bitboard (xmpz): Bitboard of positions of queens
        all_pieces (xmpz): Bitboard of all other pieces on the board

    Returns:
        generator for all queen moves gives 3 tuples (from, to, promote)
    '''
    while queen_bitboard:
        queen_square = bit_scan1(queen_bitboard)
        attack_bitboard = queen_sliding(queen_square, all_pieces)
        queen_bitboard = queen_bitboard.bit_clear(queen_square)
        moveset = attack_bitboard & invert_bitboard(own_pieces)
        yield from yield_moveset(queen_square, moveset)


def gen_pawn_moves_white(pawn_bitboard, board):
    seventhrow = xmpz(0b0000000011111111000000000000000000000000000000000000000000000000)
    pawns = pawn_bitboard & invert_bitboard(seventhrow)
    while(pawns):
        pawn_square = bit_scan1(pawns)
        yield from yield_moveset(pawn_square,
                                 non_sliding['pawn white move'][pawn_square]
                                 & invert_bitboard(board.all_pieces))
        yield from yield_moveset(pawn_square,
                                 non_sliding['pawn white capture'][pawn_square]
                                 & (board.all_pieces_black | board.en_passant))
        pawns = pawns.bit_clear(pawn_square)

    pawns_seventh = pawn_bitboard & seventhrow
    while(pawns_seventh):
        pawn_square = bit_scan1(pawns_seventh)
        yield from yield_promotion_moveset(pawn_square,
                                           non_sliding['pawn white move'][pawn_square]
                                           & invert_bitboard(board.all_pieces))
        yield from yield_promotion_moveset(pawn_square,
                                           non_sliding['pawn white capture'][pawn_square]
                                           & board.all_pieces_black)
        pawns_seventh = pawns_seventh.bit_clear(pawn_square)


def gen_pawn_moves_black(pawn_bitboard, board):
    secondrow = xmpz(0b0000000000000000000000000000000000000000000000001111111100000000)
    pawns = pawn_bitboard & invert_bitboard(secondrow)
    while(pawns):
        pawn_square = bit_scan1(pawns)
        yield from yield_moveset(pawn_square,
                                 non_sliding['pawn black move'][pawn_square]
                                 & invert_bitboard(board.all_pieces))
        yield from yield_moveset(pawn_square,
                                 non_sliding['pawn black capture'][pawn_square]
                                 & (board.all_pieces_white | board.en_passant))
        pawns = pawns.bit_clear(pawn_square)

    pawns_second = pawn_bitboard & secondrow
    while(pawns_second):
        pawn_square = bit_scan1(pawns_second)
        yield from yield_promotion_moveset(pawn_square,
                                           non_sliding['pawn black move'][pawn_square]
                                           & invert_bitboard(board.all_pieces))
        yield from yield_promotion_moveset(pawn_square,
                                           non_sliding['pawn black capture'][pawn_square]
                                           & board.all_pieces_white)
        pawns_second = pawns_second.bit_clear(pawn_square)
