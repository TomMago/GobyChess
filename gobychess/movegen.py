#!/usr/bin/env python3

import numpy as np
from gmpy2 import bit_clear, bit_scan1, xmpz

from .utils import (bitboard_of_index, forward_bit_scan, invert_bitboard,
                    print_bitboard, reverse_bit_scan, set_bit, unset_bit,
                    get_bit)

from numba import njit

@njit
def generate_non_sliding():
    '''
    Generate Table for non slide move lookup

    Returns:
        dict: dict containing moves for every square for pawn white capture,
              pawn black capture, pawn white move, pawn black move,
              knight and the king
    '''
    # non_sliding_table = {'pawn white capture': [], 'pawn black capture': [],
    #               'pawn white move': [], 'pawn black move': [],
    #               'knight': [], 'king': []}
    non_sliding_table = {}


    non_sliding_table['knight'] = np.asarray(generate_knight())
    non_sliding_table['king'] = np.asarray(generate_king())
    non_sliding_table['pawn white move'] = np.asarray(generate_white_pawn_move())
    non_sliding_table['pawn white capture'] = np.asarray(generate_white_pawn_capture())
    non_sliding_table['pawn black move'] = np.asarray(generate_black_pawn_move())
    non_sliding_table['pawn black capture'] = np.asarray(generate_black_pawn_capture())
    return non_sliding_table

@njit
def generate_white_pawn_move():
    '''
    Generate all non capturing pawn moves for white for every sqare

    Returns:
        moves (uint64 array): array of bitboards of moves for all 64 squares
    '''
    #moves = np.array([], dtype=np.uint64)
    moves = []
    for i in range(64):
        attack_board = np.uint64(0b0)
        if i <= 7 or i >= 56:
            pass
        elif i // 8 == 1:
            attack_board = set_bit(attack_board, i + 8)
            attack_board = set_bit(attack_board, i + 16)
        else:
            attack_board = set_bit(attack_board, i + 8)
        moves.append(attack_board)
    return moves

@njit
def generate_white_pawn_capture():
    '''
    Generate all capturing pawn moves for white for every sqare

    Returns:
        moves (uint64 array): array of bitboards of moves for all 64 squares
    '''
    moves = []
    for i in range(64):
        attack_board = np.uint64(0b0)
        if i < 56:
            if (i % 8) != 0:
                attack_board = set_bit(attack_board, i + 7)
            if (i + 1) % 8 != 0:
                attack_board = set_bit(attack_board, i + 9)
        moves.append(attack_board)
    return moves

@njit
def generate_black_pawn_move():
    '''
    Generate all non capturing pawn moves for white for every sqare

    Returns:
        moves (xmpz array): array of bitboards of moves for all 64 squares
    '''
    moves = []
    for i in range(64):
        attack_board = np.uint64(0b0)
        if i <= 7 or i >= 56:
            pass
        elif i // 8 == 6:
            attack_board = set_bit(attack_board, i - 8)
            attack_board = set_bit(attack_board, i - 16)
        else:
            attack_board = set_bit(attack_board, i - 8)
        moves.append(attack_board)
    return moves

@njit
def generate_black_pawn_capture():
    '''
    Generate all capturing pawn moves for white for every sqare

    Returns:
        moves (xmpz array): array of bitboards of moves for all 64 squares
    '''
    moves = []
    for i in range(64):
        attack_board = np.uint64(0b0)
        if i > 7:
            if (i % 8) != 0:
                attack_board = set_bit(attack_board, i - 9)
            if (i + 1) % 8 != 0:
                attack_board = set_bit(attack_board, i - 7)
        moves.append(attack_board)
    return moves

@njit
def generate_king():
    '''
    Generate all king moves for every square

    Returns:
        moves (xmpz array): array of bitboards of moves for all 64 squares
    '''
    moves = []
    for i in range(64):
        attack_board = np.uint64(0b0)
        if (i + 1) % 8 != 0:
            attack_board = set_bit(attack_board, i + 1)
        if i % 8 != 0:
            attack_board = set_bit(attack_board, i - 1)
        if (i + 1) % 8 != 0 and (i + 9) <= 63:
            attack_board = set_bit(attack_board, i + 9)
        if (i + 1) % 8 != 0 and (i - 7) > 0:
            attack_board = set_bit(attack_board, i - 7)
        if (i + 8) <= 63:
            attack_board = set_bit(attack_board, i + 8)
        if (i - 8) >= 0:
            attack_board = set_bit(attack_board, i - 8)
        if i % 8 != 0 and (i + 7) <= 63:
            attack_board = set_bit(attack_board, i + 7)
        if i % 8 != 0 and (i - 9) > 0:
            attack_board = set_bit(attack_board, i - 9)
        moves.append(attack_board)
    return moves

@njit
def generate_knight():
    '''
    Generate all knight moves for every square

    Returns:
        moves (xmpz array): array of bitboards of moves for all 64 squares
    '''
    moves = []
    for i in range(64):
        attack_board = np.uint64(0b0)

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
                attack_board = set_bit(attack_board, field)
        moves.append(attack_board)
    return moves

@njit
def generate_table():
    '''
    Generate table of sliding moves in all directions

    Returns:
        move_table (dict): for each direction sliding moves for
                           each square as xmpz bitboard
    '''
    #move_table = {'east': [], 'north': [], 'west': [], 'south': [],
    #              'south east': [], 'south west': [], 'north west': [],
    #              'north east': []}
    move_table = {}

    move_table['east'] = np.asarray(generate_direction(1))
    move_table['north'] = np.asarray(generate_direction(8))
    move_table['west'] = np.asarray(generate_direction(-1))
    move_table['south'] = np.asarray(generate_direction(-8))
    move_table['south east'] = np.asarray(generate_direction(-7))
    move_table['south west'] = np.asarray(generate_direction(-9))
    move_table['north west'] = np.asarray(generate_direction(7))
    move_table['north east'] = np.asarray(generate_direction(9))

    return move_table

@njit
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
        attack_board = np.uint64(0b0)
        attack_board = unset_bit(attack_board, i)

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
            attack_board = set_bit(attack_board, field_count)

        directions.append(attack_board)

    return directions


#table = generate_table()
#non_sliding = generate_non_sliding()

@njit
def rook_sliding(square, blockers, table, non_sliding):
    '''
    Generates bitboard of all attack squares for the rook with given blockers

    Args:
        square (int): Index of the square of the rook
        blockers: Bitboard of all other pieces on the board

    Returns:
        xmpz bitboard of attacked squares
    '''
    attacks = np.uint64(0b0)
    attacks = np.bitwise_or(attacks, table['east'][square])
    if np.bitwise_and(table['east'][square], blockers):
        idx = forward_bit_scan(np.bitwise_and(table['east'][square], blockers))
        attacks = np.uint64(np.bitwise_and(attacks, np.bitwise_not(table['east'][idx])))

    attacks = np.bitwise_or(attacks, table['north'][square])
    if np.bitwise_and(table['north'][square], blockers):
        idx = forward_bit_scan(np.bitwise_and(table['north'][square], blockers))
        attacks = np.bitwise_and(attacks, np.bitwise_not(table['north'][idx]))

    attacks = np.bitwise_or(attacks, table['west'][square])
    if np.bitwise_and(table['west'][square], blockers):
        idx = reverse_bit_scan(table['west'][square] & blockers)
        attacks = np.bitwise_and(attacks, np.bitwise_not(table['west'][idx]))

    attacks = np.bitwise_or(attacks, table['south'][square])
    if np.bitwise_and(table['south'][square], blockers):
        idx = reverse_bit_scan(table['south'][square] & blockers)
        attacks = np.bitwise_and(attacks, np.bitwise_not(table['south'][idx]))

    return attacks

@njit
def bishop_sliding(square, blockers, table, non_sliding):
    '''
    Generates bitboard of all attack squares for the bishop with given blockers

    Args:
        square (int): Index of the square of the rook
        blockers: Bitboard of all other pieces on the board

    Returns:
        xmpz bitboard of attacked squares
    '''
    attacks = np.uint64(0b0)
    attacks |= table['north east'][square]
    if table['north east'][square] & blockers:
        idx = forward_bit_scan(table['north east'][square] & blockers)
        attacks = attacks & np.bitwise_not(table['north east'][idx])

    attacks |= table['north west'][square]
    if table['north west'][square] & blockers:
        idx = forward_bit_scan(table['north west'][square] & blockers)
        attacks = attacks & np.bitwise_not(table['north west'][idx])

    attacks |= table['south west'][square]
    if table['south west'][square] & blockers:
        idx = reverse_bit_scan(table['south west'][square] & blockers)
        attacks = attacks & np.bitwise_not(table['south west'][idx])

    attacks |= table['south east'][square]
    if table['south east'][square] & blockers:
        idx = reverse_bit_scan(table['south east'][square] & blockers)
        attacks = attacks & np.bitwise_not(table['south east'][idx])

    return attacks

@njit
def queen_sliding(square, blockers, table, non_sliding):
    '''
    Generates bitboard of all attack squares for the queen with given blockers

    Args:
        square (int): Index of the square of the rook
        blockers (xmpz): Bitboard of all other pieces on the board

    Returns:
        xmpz bitboard of attacked squares
    '''

    attacks = rook_sliding(square, blockers, table, non_sliding) | bishop_sliding(square, blockers, table, non_sliding)
    return attacks

@njit
def yield_moveset(square, moveset):
    '''
    yield all moves of a piece from one square to all squares on a bitboard
    '''
    moves = []
    while moveset:
        index_to = forward_bit_scan(moveset)
        #yield (square, index_to, None)
        moves.append((square, index_to, 100))
        moveset = unset_bit(moveset, index_to)
    return moves

@njit
def yield_promotion_moveset(square, moveset):
    '''
    yield all moves of a piece from one square to all squares on a bitboard
    '''
    moves = []
    while moveset:
        index_to = forward_bit_scan(moveset)
        for i in [1, 2, 3, 4]:
            moves.append((square, index_to, i))
        moveset = unset_bit(moveset, index_to)
    return moves

@njit
def gen_bishop_moves(bishop_bitboard, all_pieces, own_pieces, table, non_sliding):
    '''
    generate bishop moves

    Args:
        bishop_bitboard (xmpz): Bitboard of positions of bishops
        all_pieces (xmpz): Bitboard of all other pieces on the board

    Returns:
        generator for all bishop moves gives 3 tuples (from, to, promote)
    '''
    moves = []
    while bishop_bitboard:
        bishop_square = forward_bit_scan(bishop_bitboard)
        attack_bitboard = bishop_sliding(bishop_square, all_pieces, table, non_sliding)
        bishop_bitboard = unset_bit(bishop_bitboard, bishop_square)
        moveset = attack_bitboard & np.bitwise_not(own_pieces)
        moves.extend(yield_moveset(bishop_square, moveset))
    return moves

@njit
def gen_rook_moves(rook_bitboard, all_pieces, own_pieces, table, non_sliding):
    '''
    generate rook moves

    Args:
        rook_bitboard (xmpz): Bitboard of positions of rooks
        all_pieces (xmpz): Bitboard of all other pieces on the board

    Returns:
        generator for all rook moves gives 3 tuples (from, to, promote)
    '''
    moves = []
    while rook_bitboard:
        rook_square = forward_bit_scan(rook_bitboard)
        attack_bitboard = rook_sliding(rook_square, all_pieces, table, non_sliding)
        rook_bitboard = unset_bit(rook_bitboard, rook_square)
        moveset = attack_bitboard & np.bitwise_not(own_pieces)
        moves.extend(yield_moveset(rook_square, moveset))
    return moves

@njit
def gen_queen_moves(queen_bitboard, all_pieces, own_pieces, table, non_sliding):
    '''
    generate queen moves

    Args:
        queen_bitboard (xmpz): Bitboard of positions of queens
        all_pieces (xmpz): Bitboard of all other pieces on the board

    Returns:
        generator for all queen moves gives 3 tuples (from, to, promote)
    '''
    moves = []
    while queen_bitboard:
        queen_square = forward_bit_scan(queen_bitboard)
        attack_bitboard = queen_sliding(queen_square, all_pieces, table, non_sliding)
        queen_bitboard = unset_bit(queen_bitboard, queen_square)
        moveset = attack_bitboard & np.bitwise_not(own_pieces)
        moves.extend(yield_moveset(queen_square, moveset))
    return moves

@njit
def gen_pawn_moves_white(pawn_bitboard, board, table, non_sliding):
    '''
    generate pawn moves for white

    Args:
        pawn_bitboard (xmpz): Bitboard of positions of pawns
        board (xmpz): board object

    Returns:
        generator for all pawn moves gives 3 tuples (from, to, promote)
    '''
    moves = []
    seventhrow = np.uint64(0b0000000011111111000000000000000000000000000000000000000000000000)
    pawns = pawn_bitboard & np.bitwise_not(seventhrow)
    while pawns:
        pawn_square = forward_bit_scan(pawns)
        if not get_bit(board.all_pieces, pawn_square + 8):
            moves.extend(yield_moveset(pawn_square,
                                       non_sliding['pawn white move'][pawn_square]
                                       & np.bitwise_not(board.all_pieces)))
        moves.extend(yield_moveset(pawn_square,
                                   non_sliding['pawn white capture'][pawn_square]
                                   & (board.all_pieces_color[0] | board.en_passant)))
        pawns = unset_bit(pawns, pawn_square)

    pawns_seventh = pawn_bitboard & seventhrow
    while pawns_seventh:
        pawn_square = forward_bit_scan(pawns_seventh)
        moves.extend(yield_promotion_moveset(pawn_square,
                                             non_sliding['pawn white move'][pawn_square]
                                             & np.bitwise_not(board.all_pieces)))
        moves.extend(yield_promotion_moveset(pawn_square,
                                             non_sliding['pawn white capture'][pawn_square]
                                             & board.all_pieces_color[0]))
        pawns_seventh = unset_bit(pawns_seventh, pawn_square)
    return moves


@njit
def gen_pawn_moves_black(pawn_bitboard, board, table, non_sliding):
    '''
    generate pawn moves for black

    Args:
        pawn_bitboard (xmpz): Bitboard of positions of pawns
        board (xmpz): board object

    Returns:
        generator for all pawn moves gives 3 tuples (from, to, promote)
    '''
    moves = []
    secondrow = np.uint64(0b0000000000000000000000000000000000000000000000001111111100000000)
    pawns = pawn_bitboard & np.bitwise_not(secondrow)
    while pawns:
        pawn_square = forward_bit_scan(pawns)
        if not get_bit(board.all_pieces, pawn_square - 8):
            moves.extend(yield_moveset(pawn_square,
                                       non_sliding['pawn black move'][pawn_square]
                                       & np.bitwise_not(board.all_pieces)))
        moves.extend(yield_moveset(pawn_square,
                                   non_sliding['pawn black capture'][pawn_square]
                                   & (board.all_pieces_color[1] | board.en_passant)))
        pawns = unset_bit(pawns, pawn_square)

    pawns_second = pawn_bitboard & secondrow
    while pawns_second:
        pawn_square = forward_bit_scan(pawns_second)
        moves.extend(yield_promotion_moveset(pawn_square,
                                             non_sliding['pawn black move'][pawn_square]
                                             & np.bitwise_not(board.all_pieces)))
        moves.extend(yield_promotion_moveset(pawn_square,
                                             non_sliding['pawn black capture'][pawn_square]
                                             & board.all_pieces_color[1]))
        pawns_second = unset_bit(pawns_second, pawn_square)
    return moves

@njit
def gen_knight_moves(knight_bitboard, own_pieces, table, non_sliding):
    '''
    generate knight moves

    Args:
        knight_bitboard (xmpz): Bitboard of positions of knight
        all_pieces (xmpz): Bitboard of own pieces on the board

    Returns:
        generator for all knight moves gives 3 tuples (from, to, None)
    '''
    moves = []
    while knight_bitboard:
        knight_square = forward_bit_scan(knight_bitboard)
        attack_bitboard = non_sliding['knight'][knight_square]
        knight_bitboard = unset_bit(knight_bitboard, knight_square)
        moveset = attack_bitboard & np.bitwise_not(own_pieces)
        moves.extend(yield_moveset(knight_square, moveset))
    return moves

@njit
def gen_king_moves(king_bitboard, own_pieces, table, non_sliding):
    '''
    generate king moves

    Args:
        king_bitboard (xmpz): Bitboard of position of the king
        all_pieces (xmpz): Bitboard of own pieces on the board

    Returns:
        generator for all knight moves gives 3 tuples (from, to, None)
    '''
    moves = []
    while king_bitboard:
        king_square = forward_bit_scan(king_bitboard)
        attack_bitboard = non_sliding['king'][king_square]
        king_bitboard = unset_bit(king_bitboard ,king_square)
        moveset = attack_bitboard & np.bitwise_not(own_pieces)
        moves.extend(yield_moveset(king_square, moveset))
    return moves


def check_piece_move(piecetype, from_square, to_square, board):
    '''
    Check if move for piece is valid

    Args:
        piecetype (int): Type of piece to move
        from_square (int): Index of square the piece is standing on
        to_square (int): Index of square the piece should move to
        board (Board): Board object

    Returns:
        bool: True if move is possible, False if not
    '''
    piece_bitboard = bitboard_of_index(from_square)
    if piecetype == 0 and board.to_move == 0:
        if (from_square, to_square, None) in gen_pawn_moves_black(piece_bitboard, board):
            return True
        if (from_square, to_square, 1) in gen_pawn_moves_black(piece_bitboard, board):
            return True
    if piecetype == 0 and board.to_move == 1:
        if (from_square, to_square, None) in gen_pawn_moves_white(piece_bitboard, board):
            return True
        if (from_square, to_square, 1) in gen_pawn_moves_black(piece_bitboard, board):
            return True
    if piecetype == 1 and (from_square, to_square, None) in gen_knight_moves(piece_bitboard, board.all_pieces_color[board.to_move]):
        return True
    if piecetype == 2 and (from_square, to_square, None) in gen_bishop_moves(piece_bitboard,
                                                                             board.all_pieces,
                                                                             board.all_pieces_color[board.to_move]):
        return True
    if piecetype == 3 and (from_square, to_square, None) in gen_rook_moves(piece_bitboard,
                                                                           board.all_pieces,
                                                                           board.all_pieces_color[board.to_move]):
        return True
    if piecetype == 4 and (from_square, to_square, None) in gen_queen_moves(piece_bitboard,
                                                                            board.all_pieces,
                                                                            board.all_pieces_color[board.to_move]):
        return True
    if piecetype == 5 and (from_square, to_square, None) in gen_king_moves(piece_bitboard,
                                                                           board.all_pieces_color[board.to_move]):
        return True
    return False

@njit
def generate_moves(board, table, non_sliding):
    '''
    Generates all pseudo legal moves for the color to move

    yields:
        moves (tuple): all moves in the form (square_from, square_to, promotion)
    '''
    moves = []
    if board.to_move:
        moves.extend(gen_pawn_moves_white(board.pieces[board.to_move][0], board, table, non_sliding))
        if check_white_castle_kingside(board, table, non_sliding):
            moves.append((4, 6, 100))
        if check_white_castle_queenside(board, table, non_sliding):
            moves.append((4, 2, 100))
    else:
        moves.extend(gen_pawn_moves_black(board.pieces[board.to_move][0], board, table, non_sliding))
        if check_black_castle_kingside(board, table, non_sliding):
            moves.append((60, 62, 100))
        if check_black_castle_queenside(board, table, non_sliding):
            moves.append((60, 58, 100))
    moves.extend(gen_knight_moves(board.pieces[board.to_move][1],
                                  board.all_pieces_color[board.to_move], table, non_sliding))
    moves.extend(gen_bishop_moves(board.pieces[board.to_move][2],
                                board.all_pieces,
                                  board.all_pieces_color[board.to_move], table, non_sliding))
    moves.extend(gen_rook_moves(board.pieces[board.to_move][3],
                              board.all_pieces,
                                board.all_pieces_color[board.to_move], table, non_sliding))
    moves.extend(gen_queen_moves(board.pieces[board.to_move][4],
                               board.all_pieces,
                                 board.all_pieces_color[board.to_move], table, non_sliding))
    moves.extend(gen_king_moves(board.pieces[board.to_move][5],
                                board.all_pieces_color[board.to_move], table, non_sliding))
    return moves

@njit
def color_in_check(board, table, non_sliding):
    '''
    checks if color to move is in check.

    Returns:
        bool: True if color to move is in check, False otherwise
    '''
    king_square = forward_bit_scan(board.pieces[board.to_move][5])

    opponent_color = 1 - board.to_move

    if non_sliding['king'][king_square] & board.pieces[opponent_color][5]:
        return True
    if non_sliding['knight'][king_square] & board.pieces[opponent_color][1]:
        return True
    if bishop_sliding(king_square, board.all_pieces, table, non_sliding) & board.pieces[opponent_color][2]:
        return True
    if rook_sliding(king_square, board.all_pieces, table, non_sliding) & board.pieces[opponent_color][3]:
        return True
    if queen_sliding(king_square, board.all_pieces, table, non_sliding) & board.pieces[opponent_color][4]:
        return True
    if board.to_move:
        if non_sliding['pawn white capture'][king_square] & board.pieces[opponent_color][0]:
            return True
    else:
        if non_sliding['pawn black capture'][king_square] & board.pieces[opponent_color][0]:
            return True
    return False

@njit
def check_white_castle_kingside(board, table, non_sliding):
    '''check if black can castle kingside

    Args:
        board (Board): current board

    Returns:
        bool: if castling is possible
    '''

    if not board.castling_white_kingside:
        return False

    if get_bit(board.all_pieces, 5) == 1 or get_bit(board.all_pieces, 6) == 1:
        return False

    if board.in_check(table, non_sliding):
        return False

    tmp_board = board.board_copy()

    for i in [5, 6]:

        tmp_board.pieces[1][5] = unset_bit(tmp_board.pieces[1][5], i-1)
        tmp_board.pieces[1][5] = set_bit(tmp_board.pieces[1][5], i)

        tmp_board.all_pieces = unset_bit(tmp_board.all_pieces, i-1)
        tmp_board.all_pieces = set_bit(tmp_board.all_pieces, i)

        tmp_board.all_pieces_color[1] = unset_bit(tmp_board.all_pieces_color[1], i-1)
        tmp_board.all_pieces_color[1] = set_bit(tmp_board.all_pieces_color[1], i)

        if tmp_board.in_check(table, non_sliding):
            return False

    return True

@njit
def check_white_castle_queenside(board, table, non_sliding):
    '''check if black can castle kingside

    Args:
        board (Board): current board

    Returns:
        bool: if castling is possible
    '''

    if not board.castling_white_queenside:
        return False

    if get_bit(board.all_pieces, 3) == 1 or get_bit(board.all_pieces, 2) == 1 or get_bit(board.all_pieces, 1) == 1:
        return False

    if board.in_check(table, non_sliding):
        return False

    tmp_board = board.board_copy()

    for i in [3, 2]:
        tmp_board.pieces[1][5] = unset_bit(tmp_board.pieces[1][5], i+1)
        tmp_board.pieces[1][5] = set_bit(tmp_board.pieces[1][5], i)

        tmp_board.all_pieces = unset_bit(tmp_board.all_pieces, i+1)
        tmp_board.all_pieces = set_bit(tmp_board.all_pieces, i)

        tmp_board.all_pieces_color[1] = unset_bit(tmp_board.all_pieces_color[1], i+1)
        tmp_board.all_pieces_color[1] = set_bit(tmp_board.all_pieces_color[1], i)

        if tmp_board.in_check(table, non_sliding):
            return False

    return True

@njit
def check_black_castle_kingside(board, table, non_sliding):
    '''check if black can castle kingside

    Args:
        board (Board): current board

    Returns:
        bool: if castling is possible
    '''
    if not board.castling_black_kingside:
        return False

    if get_bit(board.all_pieces, 61) == 1 or get_bit(board.all_pieces, 62) == 1:
        return False

    if board.in_check(table, non_sliding):
        return False

    tmp_board = board.board_copy()

    for i in [61, 62]:

        tmp_board.pieces[0][5] = unset_bit(tmp_board.pieces[0][5], i-1)
        tmp_board.pieces[0][5] = set_bit(tmp_board.pieces[0][5], i)

        tmp_board.all_pieces = unset_bit(tmp_board.all_pieces, i-1)
        tmp_board.all_pieces = set_bit(tmp_board.all_pieces, i)

        tmp_board.all_pieces_color[0] = unset_bit(tmp_board.all_pieces_color[0], i-1)
        tmp_board.all_pieces_color[0] = set_bit(tmp_board.all_pieces_color[0], i)

        if tmp_board.in_check(table, non_sliding):
            return False

    return True

@njit
def check_black_castle_queenside(board, table, non_sliding):
    '''check if black can castle kingside

    Args:
        board (Board): current board

    Returns:
        bool: if castling is possible
    '''
    if not board.castling_black_queenside:
        return False

    if get_bit(board.all_pieces, 59) == 1 or get_bit(board.all_pieces, 58) == 1 or get_bit(board.all_pieces, 57) == 1:
        return False

    if board.in_check(table, non_sliding):
        return False

    tmp_board = board.board_copy()

    for i in [59, 58]:
        tmp_board.pieces[0][5] = unset_bit(tmp_board.pieces[0][5], i+1)
        tmp_board.pieces[0][5] = set_bit(tmp_board.pieces[0][5], i)

        tmp_board.all_pieces = unset_bit(tmp_board.all_pieces, i+1)
        tmp_board.all_pieces = set_bit(tmp_board.all_pieces, i)

        tmp_board.all_pieces_color[0] = unset_bit(tmp_board.all_pieces_color[0], i+1)
        tmp_board.all_pieces_color[0] = set_bit(tmp_board.all_pieces_color[0], i)

        if tmp_board.in_check(table, non_sliding):
            return False

    return True
