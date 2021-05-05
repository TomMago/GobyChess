#!/usr/bin/env python3

from .utils import (bitboard_of_index, forward_bit_scan, invert_bitboard,
                    print_bitboard, reverse_bit_scan, set_bit, unset_bit,
                    get_bit, gen_ones)


def generate_non_sliding():
    """
    Generate Table for non slide move lookup

    Returns:
        dict: dict containing moves for every square for pawn white capture,
              pawn black capture, pawn white move, pawn black move,
              knight and the king
    """
    non_sliding_table = {'pawn white capture': generate_white_pawn_capture(),
                         'pawn black capture': generate_black_pawn_capture(),
                         'pawn white move': generate_white_pawn_move(),
                         'pawn black move': generate_black_pawn_move(),
                         'knight': generate_knight(),
                         'king': generate_king()}

    return non_sliding_table


def generate_white_pawn_move():
    """
    Generate all non capturing pawn moves for white for every sqare

    Returns:
        moves (int array): array of bitboards of moves for all 64 squares
    """
    moves = []
    for i in range(64):
        attack_board = 0
        if i <= 7 or i >= 56:
            pass
        elif i // 8 == 1:
            attack_board = set_bit(attack_board, i + 8)
            attack_board = set_bit(attack_board, i + 16)
        else:
            attack_board = set_bit(attack_board, i + 8)
        moves.append(attack_board)
    return moves


def generate_white_pawn_capture():
    """
    Generate all capturing pawn moves for white for every sqare

    Returns:
        moves (int array): array of bitboards of moves for all 64 squares
    """
    moves = []
    for i in range(64):
        attack_board = 0
        if i < 56:
            if (i % 8) != 0:
                attack_board = set_bit(attack_board, i + 7)
            if (i + 1) % 8 != 0:
                attack_board = set_bit(attack_board, i + 9)
        moves.append(attack_board)
    return moves


def generate_black_pawn_move():
    """
    Generate all non capturing pawn moves for white for every sqare

    Returns:
        moves (int array): array of bitboards of moves for all 64 squares
    """
    moves = []
    for i in range(64):
        attack_board = 0
        if i <= 7 or i >= 56:
            pass
        elif i // 8 == 6:
            attack_board = set_bit(attack_board, i - 8)
            attack_board = set_bit(attack_board, i - 16)
        else:
            attack_board = set_bit(attack_board, i - 8)
        moves.append(attack_board)
    return moves


def generate_black_pawn_capture():
    """
    Generate all capturing pawn moves for white for every sqare

    Returns:
        moves (int array): array of bitboards of moves for all 64 squares
    """
    moves = []
    for i in range(64):
        attack_board = 0
        if i > 7:
            if (i % 8) != 0:
                attack_board = set_bit(attack_board, i - 9)
            if (i + 1) % 8 != 0:
                attack_board = set_bit(attack_board, i - 7)
        moves.append(attack_board)
    return moves


def generate_king():
    """
    Generate all king moves for every square

    Returns:
        moves (int array): array of bitboards of moves for all 64 squares
    """
    moves = []
    for i in range(64):
        attack_board = 0
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


def generate_knight():
    """
    Generate all knight moves for every square

    Returns:
        moves (int array): array of bitboards of moves for all 64 squares
    """
    moves = []
    for i in range(64):
        attack_board = 0

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


def generate_table():
    """
    Generate table of sliding moves in all directions

    Returns:
        move_table (dict): for each direction sliding moves for
                           each square as int bitboard
    """
    move_table = {'east': generate_direction(1),
                  'north': generate_direction(8),
                  'west': generate_direction(-1),
                  'south': generate_direction(-8),
                  'south east': generate_direction(-7),
                  'south west': generate_direction(-9),
                  'north west': generate_direction(7),
                  'north east': generate_direction(9)}

    return move_table


def generate_direction(direction):
    """ Generate sliding moves for every square for certain direction.


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
        Array: int bitboard of moves for each square (length 64)
    """
    directions = []
    for i in range(64):
        field_count = i
        attack_board = 0
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
        elif direction == +1:
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


table = generate_table()
non_sliding = generate_non_sliding()


def rook_sliding(square, blockers):
    """
    Generates bitboard of all attack squares for the rook with given blockers

    Args:
        square (int): Index of the square of the rook
        blockers (int): Bitboard of all other pieces on the board

    Returns:
        int: bitboard of attacked squares
    """
    attacks = 0
    attacks |= table['east'][square]
    stops = table['east'][square] & blockers
    if stops:
        idx = forward_bit_scan(stops)
        attacks &= invert_bitboard(table['east'][idx])

    stops = table['north'][square] & blockers
    attacks |= table['north'][square]
    if stops:
        idx = forward_bit_scan(stops)
        attacks &= invert_bitboard(table['north'][idx])

    stops = table['west'][square] & blockers
    attacks |= table['west'][square]
    if stops:
        idx = reverse_bit_scan(stops)
        attacks &= invert_bitboard(table['west'][idx])

    stops = table['south'][square] & blockers
    attacks |= table['south'][square]
    if stops:
        idx = reverse_bit_scan(stops)
        attacks &= invert_bitboard(table['south'][idx])

    return attacks


def bishop_sliding(square, blockers):
    """
    Generates bitboard of all attack squares for the bishop with given blockers

    Args:
        square (int): Index of the square of the rook
        blockers (int): Bitboard of all other pieces on the board

    Returns:
        int: bitboard of attacked squares
    """
    attacks = 0
    attacks |= table['north east'][square]
    stops = table['north east'][square] & blockers
    if stops:
        idx = forward_bit_scan(stops)
        attacks &= invert_bitboard(table['north east'][idx])

    attacks |= table['north west'][square]
    stops = table['north west'][square] & blockers
    if stops:
        idx = forward_bit_scan(stops)
        attacks &= invert_bitboard(table['north west'][idx])

    stops = table['south west'][square] & blockers
    attacks |= table['south west'][square]
    if stops:
        idx = reverse_bit_scan(stops)
        attacks &= invert_bitboard(table['south west'][idx])

    stops = table['south east'][square] & blockers
    attacks |= table['south east'][square]
    if stops:
        idx = reverse_bit_scan(stops)
        attacks &= invert_bitboard(table['south east'][idx])

    return attacks


def queen_sliding(square, blockers):
    """
    Generates bitboard of all attack squares for the queen with given blockers

    Args:
        square (int): Index of the square of the rook
        blockers (int): Bitboard of all other pieces on the board

    Returns:
        int: bitboard of attacked squares
    """
    attacks = rook_sliding(square, blockers) | bishop_sliding(square, blockers)
    return attacks

def yield_moveset(square, moveset):
    """
    yield all moves of a piece from one square to all squares on a bitboard
    """
    while moveset:
        index_to = reverse_bit_scan(moveset)
        yield (square, index_to, None)
        moveset = unset_bit(moveset, index_to)


def yield_promotion_moveset(square, moveset):
    """
    yield all moves of a piece from one square to all squares on a bitboard
    """
    while moveset:
        index_to = reverse_bit_scan(moveset)
        for i in [1, 2, 3, 4]:
            yield (square, index_to, i)
        moveset = unset_bit(moveset, index_to)


def gen_bishop_moves(bishop_bitboard, all_pieces, own_pieces):
    """
    generate bishop moves

    Args:
        bishop_bitboard (int): Bitboard of positions of bishops
        all_pieces (int): Bitboard of all other pieces on the board

    Returns:
        generator for all bishop moves gives 3 tuples (from, to, promote)
    """
    while bishop_bitboard:
        bishop_square = reverse_bit_scan(bishop_bitboard)
        attack_bitboard = bishop_sliding(bishop_square, all_pieces)
        bishop_bitboard = unset_bit(bishop_bitboard, bishop_square)
        moveset = attack_bitboard & invert_bitboard(own_pieces)
        yield from yield_moveset(bishop_square, moveset)


def gen_rook_moves(rook_bitboard, all_pieces, own_pieces):
    """
    generate rook moves

    Args:
        rook_bitboard (int): Bitboard of positions of rooks
        all_pieces (int): Bitboard of all other pieces on the board

    Returns:
        generator for all rook moves gives 3 tuples (from, to, promote)
    """
    while rook_bitboard:
        rook_square = reverse_bit_scan(rook_bitboard)
        attack_bitboard = rook_sliding(rook_square, all_pieces)
        rook_bitboard = unset_bit(rook_bitboard, rook_square)
        moveset = attack_bitboard & invert_bitboard(own_pieces)
        yield from yield_moveset(rook_square, moveset)


def gen_queen_moves(queen_bitboard, all_pieces, own_pieces):
    """
    generate queen moves

    Args:
        queen_bitboard (int): Bitboard of positions of queens
        all_pieces (int): Bitboard of all other pieces on the board

    Returns:
        generator for all queen moves gives 3 tuples (from, to, promote)
    """
    while queen_bitboard:
        queen_square = reverse_bit_scan(queen_bitboard)
        attack_bitboard = queen_sliding(queen_square, all_pieces)
        queen_bitboard = unset_bit(queen_bitboard, queen_square)
        moveset = attack_bitboard & invert_bitboard(own_pieces)
        yield from yield_moveset(queen_square, moveset)


def gen_pawn_moves_white(pawn_bitboard, board):
    """
    generate pawn moves for white

    Args:
        pawn_bitboard (int): Bitboard of positions of pawns
        board (int): board object

    Returns:
        generator for all pawn moves gives 3 tuples (from, to, promote)
    """
    seventhrow = 0b0000000011111111000000000000000000000000000000000000000000000000
    pawns = pawn_bitboard & invert_bitboard(seventhrow)
    while pawns:
        pawn_square = reverse_bit_scan(pawns)
        if not get_bit(board.all_pieces, pawn_square + 8):
            yield from yield_moveset(pawn_square,
                                     non_sliding['pawn white move'][pawn_square]
                                     & invert_bitboard(board.all_pieces))
        yield from yield_moveset(pawn_square,
                                 non_sliding['pawn white capture'][pawn_square]
                                 & (board.all_pieces_color[0] | board.en_passant))
        pawns = unset_bit(pawns, pawn_square)

    pawns_seventh = pawn_bitboard & seventhrow
    while pawns_seventh:
        pawn_square = reverse_bit_scan(pawns_seventh)
        yield from yield_promotion_moveset(pawn_square,
                                           non_sliding['pawn white move'][pawn_square]
                                           & invert_bitboard(board.all_pieces))
        yield from yield_promotion_moveset(pawn_square,
                                           non_sliding['pawn white capture'][pawn_square]
                                           & board.all_pieces_color[0])
        pawns_seventh = unset_bit(pawns_seventh, pawn_square)


def gen_pawn_moves_black(pawn_bitboard, board):
    """
    generate pawn moves for black

    Args:
        pawn_bitboard (int): Bitboard of positions of pawns
        board (int): board object

    Returns:
        generator for all pawn moves gives 3 tuples (from, to, promote)
    """
    secondrow = 0b0000000000000000000000000000000000000000000000001111111100000000
    pawns = pawn_bitboard & invert_bitboard(secondrow)
    while pawns:
        pawn_square = reverse_bit_scan(pawns)
        if not get_bit(board.all_pieces, pawn_square - 8):
            yield from yield_moveset(pawn_square,
                                     non_sliding['pawn black move'][pawn_square]
                                     & invert_bitboard(board.all_pieces))
        yield from yield_moveset(pawn_square,
                                 non_sliding['pawn black capture'][pawn_square]
                                 & (board.all_pieces_color[1] | board.en_passant))
        pawns = unset_bit(pawns, pawn_square)

    pawns_second = pawn_bitboard & secondrow
    while pawns_second:
        pawn_square = reverse_bit_scan(pawns_second)
        yield from yield_promotion_moveset(pawn_square,
                                           non_sliding['pawn black move'][pawn_square]
                                           & invert_bitboard(board.all_pieces))
        yield from yield_promotion_moveset(pawn_square,
                                           non_sliding['pawn black capture'][pawn_square]
                                           & board.all_pieces_color[1])
        pawns_second = unset_bit(pawns_second, pawn_square)


def gen_knight_moves(knight_bitboard, own_pieces):
    """
    generate knight moves

    Args:
        knight_bitboard (int): Bitboard of positions of knight
        all_pieces (int): Bitboard of own pieces on the board

    Returns:
        generator for all knight moves gives 3 tuples (from, to, None)
    """
    while knight_bitboard:
        knight_square = reverse_bit_scan(knight_bitboard)
        attack_bitboard = non_sliding['knight'][knight_square]
        knight_bitboard = unset_bit(knight_bitboard, knight_square)
        moveset = attack_bitboard & invert_bitboard(own_pieces)
        yield from yield_moveset(knight_square, moveset)


def gen_king_moves(king_bitboard, own_pieces):
    """
    generate king moves

    Args:
        king_bitboard (int): Bitboard of position of the king
        all_pieces (int): Bitboard of own pieces on the board

    Returns:
        generator for all knight moves gives 3 tuples (from, to, None)
    """
    while king_bitboard:
        king_square = reverse_bit_scan(king_bitboard)
        attack_bitboard = non_sliding['king'][king_square]
        king_bitboard = unset_bit(king_bitboard ,king_square)
        moveset = attack_bitboard & invert_bitboard(own_pieces)
        yield from yield_moveset(king_square, moveset)

def generate_moves(board):
    """
    Generates all pseudo legal moves for the color to move

    yields:
        moves (tuple): all moves in the form (square_from, square_to, promotion)
    """
    if board.to_move:
        yield from gen_pawn_moves_white(board.pieces[board.to_move][0], board)
        if check_white_castle_kingside(board):
            yield 4, 6, None
        if check_white_castle_queenside(board):
            yield 4, 2, None
    else:
        yield from gen_pawn_moves_black(board.pieces[board.to_move][0], board)
        if check_black_castle_kingside(board):
            yield 60, 62, None
        if check_black_castle_queenside(board):
            yield 60, 58, None
    yield from gen_knight_moves(board.pieces[board.to_move][1],
                                board.all_pieces_color[board.to_move])
    yield from gen_bishop_moves(board.pieces[board.to_move][2],
                                board.all_pieces,
                                board.all_pieces_color[board.to_move])
    yield from gen_rook_moves(board.pieces[board.to_move][3],
                              board.all_pieces,
                              board.all_pieces_color[board.to_move])
    yield from gen_queen_moves(board.pieces[board.to_move][4],
                               board.all_pieces,
                               board.all_pieces_color[board.to_move])
    yield from gen_king_moves(board.pieces[board.to_move][5],
                              board.all_pieces_color[board.to_move])

def rook_sliding_quiet(square, blockers):
    """
    Generates bitboard of moves onto blockers for the rook

    Args:
        square (int): Index of the square of the rook
        blockers (int): Bitboard of all other pieces on the board

    Returns:
        int: bitboard of blocked attacked squares
    """
    attacks = 0
    stops = table['east'][square] & blockers
    if stops:
        idx = forward_bit_scan(stops)
        attacks = set_bit(attacks, idx)

    stops = table['north'][square] & blockers
    if stops:
        idx = forward_bit_scan(stops)
        attacks = set_bit(attacks, idx)

    stops = table['west'][square] & blockers
    if stops:
        idx = reverse_bit_scan(stops)
        attacks = set_bit(attacks, idx)

    stops = table['south'][square] & blockers
    if stops:
        idx = reverse_bit_scan(stops)
        attacks = set_bit(attacks, idx)

    return attacks


def bishop_sliding_quiet(square, blockers):
    """
    Generates bitboard of all attacks onto blockers for the bishop

    Args:
        square (int): Index of the square of the rook
        blockers (int): Bitboard of all other pieces on the board

    Returns:
        int: bitboard of attacked blocked squares
    """
    attacks = 0
    stops = table['north east'][square] & blockers
    if stops:
        idx = forward_bit_scan(stops)
        attacks = set_bit(attacks, idx)

    stops = table['north west'][square] & blockers
    if stops:
        idx = forward_bit_scan(stops)
        attacks = set_bit(attacks, idx)

    stops = table['south west'][square] & blockers
    if stops:
        idx = reverse_bit_scan(stops)
        attacks = set_bit(attacks, idx)

    stops = table['south east'][square] & blockers
    if stops:
        idx = reverse_bit_scan(stops)
        attacks = set_bit(attacks, idx)

    return attacks


def queen_sliding_quiet(square, blockers):
    """
    Generates bitboard of all attack blocked squares for the queen

    Args:
        square (int): Index of the square of the rook
        blockers (int): Bitboard of all other pieces on the board

    Returns:
        int: bitboard of attacked blocked squares
    """
    attacks = rook_sliding_quiet(square, blockers) | bishop_sliding_quiet(square, blockers)
    return attacks


def gen_bishop_moves_quiet(bishop_bitboard, opponents_pieces, blockers):
    """
    generate capturing bishop moves

    Args:
        bishop_bitboard (int): Bitboard of positions of bishops
        all_pieces (int): Bitboard of all other pieces on the board

    Returns:
        generator for all capturing bishop moves gives 3-tuples (from, to, promote)
    """
    while bishop_bitboard:
        bishop_square = forward_bit_scan(bishop_bitboard)
        attack_bitboard = bishop_sliding_quiet(bishop_square, blockers)
        bishop_bitboard = unset_bit(bishop_bitboard, bishop_square)
        attack_bitboard &= opponents_pieces
        yield from yield_moveset(bishop_square, attack_bitboard)


def gen_rook_moves_quiet(rook_bitboard, opponents_pieces, blockers):
    """
    generate capturing rook moves

    Args:
        rook_bitboard (int): Bitboard of positions of rooks
        all_pieces (int): Bitboard of all other pieces on the board

    Returns:
        generator for all capturing rook moves gives 3-tuples (from, to, promote)
    """
    while rook_bitboard:
        rook_square = forward_bit_scan(rook_bitboard)
        attack_bitboard = rook_sliding_quiet(rook_square, blockers)
        rook_bitboard = unset_bit(rook_bitboard, rook_square)
        attack_bitboard &= opponents_pieces
        yield from yield_moveset(rook_square, attack_bitboard)


def gen_queen_moves_quiet(queen_bitboard, opponents_pieces, blockers):
    """
    generate capturing queen moves

    Args:
        queen_bitboard (int): Bitboard of positions of queens
        all_pieces (int): Bitboard of all other pieces on the board

    Returns:
        generator for all capturing queen moves gives 3-tuples (from, to, promote)
    """
    while queen_bitboard:
        queen_square = forward_bit_scan(queen_bitboard)
        attack_bitboard = queen_sliding_quiet(queen_square, blockers)
        queen_bitboard = unset_bit(queen_bitboard, queen_square)
        attack_bitboard &= opponents_pieces
        yield from yield_moveset(queen_square, attack_bitboard)



def gen_pawn_moves_white_quiet(pawn_bitboard, board):
    """
    generate capturing pawn moves for white

    Args:
        pawn_bitboard (int): Bitboard of positions of pawns
        board (int): board object

    Returns:
        generator for all capturing pawn moves gives 3-tuples (from, to, promote)
    """
    seventhrow = 0b0000000011111111000000000000000000000000000000000000000000000000
    pawns = pawn_bitboard & invert_bitboard(seventhrow)
    while pawns:
        pawn_square = forward_bit_scan(pawns)
        yield from yield_moveset(pawn_square,
                                 non_sliding['pawn white capture'][pawn_square]
                                 & (board.all_pieces_color[0] | board.en_passant))
        pawns = unset_bit(pawns, pawn_square)

    pawns_seventh = pawn_bitboard & seventhrow
    while pawns_seventh:
        pawn_square = forward_bit_scan(pawns_seventh)
        yield from yield_promotion_moveset(pawn_square,
                                           non_sliding['pawn white capture'][pawn_square]
                                           & board.all_pieces_color[0])
        pawns_seventh = unset_bit(pawns_seventh, pawn_square)


def gen_pawn_moves_black_quiet(pawn_bitboard, board):
    """
    generate capturing pawn moves for black

    Args:
        pawn_bitboard (int): Bitboard of positions of pawns
        board (int): board object

    Returns:
        generator for all capturing pawn moves gives 3-tuples (from, to, promote)
    """
    secondrow = 0b0000000000000000000000000000000000000000000000001111111100000000
    pawns = pawn_bitboard & invert_bitboard(secondrow)
    while pawns:
        pawn_square = forward_bit_scan(pawns)
        yield from yield_moveset(pawn_square,
                                 non_sliding['pawn black capture'][pawn_square]
                                 & (board.all_pieces_color[1] | board.en_passant))
        pawns = unset_bit(pawns, pawn_square)

    pawns_second = pawn_bitboard & secondrow
    while pawns_second:
        pawn_square = forward_bit_scan(pawns_second)
        yield from yield_promotion_moveset(pawn_square,
                                           non_sliding['pawn black capture'][pawn_square]
                                           & board.all_pieces_color[1])
        pawns_second = unset_bit(pawns_second, pawn_square)


def gen_knight_moves_quiet(knight_bitboard, opponent_pieces):
    """
    generate capturing knight moves

    Args:
        knight_bitboard (int): Bitboard of positions of knight
        all_pieces (int): Bitboard of own pieces on the board

    Returns:
        generator for all capturing knight moves gives 3-tuples (from, to, None)
    """
    while knight_bitboard:
        knight_square = forward_bit_scan(knight_bitboard)
        attack_bitboard = non_sliding['knight'][knight_square] & opponent_pieces
        knight_bitboard = unset_bit(knight_bitboard, knight_square)
        yield from yield_moveset(knight_square, attack_bitboard)


def gen_king_moves_quiet(king_bitboard, opponent_pieces):
    """
    generate capturing king moves

    Args:
        king_bitboard (int): Bitboard of position of the king
        all_pieces (int): Bitboard of own pieces on the board

    Returns:
        generator for all capturing knight moves gives 3-tuples (from, to, None)
    """
    while king_bitboard:
        king_square = forward_bit_scan(king_bitboard)
        attack_bitboard = non_sliding['king'][king_square] & opponent_pieces
        king_bitboard = unset_bit(king_bitboard, king_square)
        yield from yield_moveset(king_square, attack_bitboard)


def generate_quiet_moves(board):
    """
    Generates all pseudo legal capturing moves for the color to move

    yields:
        moves (tuple): all moves in the form (square_from, square_to, promotion)
    """
    if board.to_move:
        yield from gen_pawn_moves_white_quiet(board.pieces[board.to_move][0], board)
    else:
        yield from gen_pawn_moves_black_quiet(board.pieces[board.to_move][0], board)
    yield from gen_knight_moves_quiet(board.pieces[board.to_move][1],
                                      board.all_pieces_color[1 - board.to_move])
    yield from gen_bishop_moves_quiet(board.pieces[board.to_move][2],
                                      board.all_pieces_color[1 - board.to_move],
                                      board.all_pieces)
    yield from gen_rook_moves_quiet(board.pieces[board.to_move][3],
                                    board.all_pieces_color[1 - board.to_move],
                                    board.all_pieces)
    yield from gen_queen_moves_quiet(board.pieces[board.to_move][4],
                                     board.all_pieces_color[1 - board.to_move],
                                     board.all_pieces)
    yield from gen_king_moves_quiet(board.pieces[board.to_move][5],
                                    board.all_pieces_color[1 - board.to_move])


def check_piece_move(move, board):
    """
    Check if move for piece is valid

    Args:
        piecetype (int): Type of piece to move
        from_square (int): Index of square the piece is standing on
        to_square (int): Index of square the piece should move to
        board (Board): Board object

    Returns:
        bool: True if move is possible, False if not
    """
    if move in board.gen_legal_moves():
        return True
    return False


def color_in_check(board):
    """
    checks if color to move is in check.

    Returns:
        bool: True if color to move is in check, False otherwise
    """
    king_square = forward_bit_scan(board.pieces[board.to_move][5])

    opponent_color = 1 - board.to_move

    if non_sliding['king'][king_square] & board.pieces[opponent_color][5]:
        return True
    if non_sliding['knight'][king_square] & board.pieces[opponent_color][1]:
        return True
    if bishop_sliding(king_square, board.all_pieces) & board.pieces[opponent_color][2]:
        return True
    if rook_sliding(king_square, board.all_pieces) & board.pieces[opponent_color][3]:
        return True
    if queen_sliding(king_square, board.all_pieces) & board.pieces[opponent_color][4]:
        return True
    if board.to_move:
        if non_sliding['pawn white capture'][king_square] & board.pieces[opponent_color][0]:
            return True
    else:
        if non_sliding['pawn black capture'][king_square] & board.pieces[opponent_color][0]:
            return True
    return False


def check_white_castle_kingside(board):
    """
    check if white can castle kingside

    Args:
        board (Board): current board

    Returns:
        bool: if castling is possible
    """

    if not board.castling_rights['white kingside']:
        return False

    if get_bit(board.all_pieces, 5) == 1 or get_bit(board.all_pieces, 6) == 1:
        return False

    if board.in_check():
        return False

    tmp_board = board.board_copy()

    for i in [5, 6]:

        tmp_board.pieces[1][5] = unset_bit(tmp_board.pieces[1][5], i-1)
        tmp_board.pieces[1][5] = set_bit(tmp_board.pieces[1][5], i)

        tmp_board.all_pieces = unset_bit(tmp_board.all_pieces, i-1)
        tmp_board.all_pieces = set_bit(tmp_board.all_pieces, i)

        tmp_board.all_pieces_color[1] = unset_bit(tmp_board.all_pieces_color[1], i-1)
        tmp_board.all_pieces_color[1] = set_bit(tmp_board.all_pieces_color[1], i)

        if tmp_board.in_check():
            return False

    return True


def check_white_castle_queenside(board):
    """
    check if white can castle queenside

    Args:
        board (Board): current board

    Returns:
        bool: if castling is possible
    """

    if not board.castling_rights['white queenside']:
        return False

    if get_bit(board.all_pieces, 3) == 1 or get_bit(board.all_pieces, 2) == 1 or get_bit(board.all_pieces, 1) == 1:
        return False

    if board.in_check():
        return False

    tmp_board = board.board_copy()

    for i in [3, 2]:
        tmp_board.pieces[1][5] = unset_bit(tmp_board.pieces[1][5], i+1)
        tmp_board.pieces[1][5] = set_bit(tmp_board.pieces[1][5], i)

        tmp_board.all_pieces = unset_bit(tmp_board.all_pieces, i+1)
        tmp_board.all_pieces = set_bit(tmp_board.all_pieces, i)

        tmp_board.all_pieces_color[1] = unset_bit(tmp_board.all_pieces_color[1], i+1)
        tmp_board.all_pieces_color[1] = set_bit(tmp_board.all_pieces_color[1], i)

        if tmp_board.in_check():
            return False

    return True


def check_black_castle_kingside(board):
    """
    check if black can castle kingside

    Args:
        board (Board): current board

    Returns:
        bool: if castling is possible
    """
    if not board.castling_rights['black kingside']:
        return False

    if get_bit(board.all_pieces, 61) == 1 or get_bit(board.all_pieces, 62) == 1:
        return False

    if board.in_check():
        return False

    tmp_board = board.board_copy()

    for i in [61, 62]:

        tmp_board.pieces[0][5] = unset_bit(tmp_board.pieces[0][5], i-1)
        tmp_board.pieces[0][5] = set_bit(tmp_board.pieces[0][5], i)

        tmp_board.all_pieces = unset_bit(tmp_board.all_pieces, i-1)
        tmp_board.all_pieces = set_bit(tmp_board.all_pieces, i)

        tmp_board.all_pieces_color[0] = unset_bit(tmp_board.all_pieces_color[0], i-1)
        tmp_board.all_pieces_color[0] = set_bit(tmp_board.all_pieces_color[0], i)

        if tmp_board.in_check():
            return False

    return True


def check_black_castle_queenside(board):
    """
    check if black can castle queenside

    Args:
        board (Board): current board

    Returns:
        bool: if castling is possible
    """
    if not board.castling_rights['black queenside']:
        return False

    if get_bit(board.all_pieces, 59) == 1 or get_bit(board.all_pieces, 58) == 1 or get_bit(board.all_pieces, 57) == 1:
        return False

    if board.in_check():
        return False

    tmp_board = board.board_copy()

    for i in [59, 58]:

        tmp_board.pieces[0][5] = unset_bit(tmp_board.pieces[0][5], i+1)
        tmp_board.pieces[0][5] = set_bit(tmp_board.pieces[0][5], i)

        tmp_board.all_pieces = unset_bit(tmp_board.all_pieces, i+1)
        tmp_board.all_pieces = set_bit(tmp_board.all_pieces, i)

        tmp_board.all_pieces_color[0] = unset_bit(tmp_board.all_pieces_color[0], i+1)
        tmp_board.all_pieces_color[0] = set_bit(tmp_board.all_pieces_color[0], i)

        if tmp_board.in_check():
            return False

    return True
