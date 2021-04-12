#!/usr/bin/env python3

## TODO/FIXME/NOTE/DEPRECATED/HACK/REVIEW

import copy
import itertools

import numpy as np
from gmpy2 import bit_scan1, xmpz

from . import movegen as mvg
from .utils import bitboard_of_index, bitboard_of_square, print_bitboard


class Board():
    '''
    Class representing the state of a chess game

    Attributes:
        pieces (2x6 array of xmpz): array containing piece bitboard for both colors
        to_move(int): 0 if black to move 1 if white to move
        castling_rights (dict): 1 if allowed to castle, 0 otherwise
        en_passant (xmpz): bitboard of the en passant square
        halfmove_clock (int): counter of halfmoves
        fullmove_clock (int): counter of full moves
    '''
    def __init__(self):
        self.pieces = [[], []]
        self.pieces[0] = [xmpz(0b0),
                          xmpz(0b0),
                          xmpz(0b0),
                          xmpz(0b0),
                          xmpz(0b0),
                          xmpz(0b0)]
        self.pieces[1] = [xmpz(0b0),
                          xmpz(0b0),
                          xmpz(0b0),
                          xmpz(0b0),
                          xmpz(0b0),
                          xmpz(0b0)]
        self.to_move = 1
        self.castling_rights = {'white kingside': 1, 'white queenside': 1,
                                'black kingside': 1, 'black queenside': 1}

        self.en_passant = xmpz(0b0)
        self.halfmove_clock = 0
        self.fullmove_counter = 1

        self.all_pieces_color = [xmpz(0b0),
                                 xmpz(0b0)]
        self.all_pieces = xmpz(0b0)

        self.update_all_pieces()

    def from_fen(self, fen):
        '''
        Set board to fen position

        Args:
            fen (string): string containing the fen position
        '''
        self.pieces[0] = [xmpz(0b0),
                          xmpz(0b0),
                          xmpz(0b0),
                          xmpz(0b0),
                          xmpz(0b0),
                          xmpz(0b0)]
        self.pieces[1] = [xmpz(0b0),
                          xmpz(0b0),
                          xmpz(0b0),
                          xmpz(0b0),
                          xmpz(0b0),
                          xmpz(0b0)]

        words = fen.split()

        if words[1] == 'w':
            self.to_move = 1
        else:
            self.to_move = 0

        if 'K' in words[2]:
            self.castling_rights['white kingside'] = 1
        else:
            self.castling_rights['white kingside'] = 0
        if 'Q' in words[2]:
            self.castling_rights['white queenside'] = 1
        else:
            self.castling_rights['white queenside'] = 0
        if 'k' in words[2]:
            self.castling_rights['black kingside'] = 1
        else:
            self.castling_rights['black kingside'] = 0
        if 'q' in words[2]:
            self.castling_rights['black queenside'] = 1
        else:
            self.castling_rights['black queenside'] = 0

        if words[3] == '-':
            self.en_passant = xmpz(0b0)
        else:
            self.en_passant = bitboard_of_square(words[3])

        self.halfmove_clock = int(words[4])
        self.fullmove_counter = int(words[5])

        rows = words[0].split("/")
        index = 0
        piece_strings = {'p': 0, 'n': 1, 'b': 2, 'r': 3, 'q': 4, 'k': 5}
        for row in rows[::-1]:
            for char in row:
                if char.isdigit():
                    for _ in range(int(char)):
                        for piecetype in range(6):
                            self.pieces[0][piecetype][index] = 0
                            self.pieces[1][piecetype][index] = 0
                        index += 1
                else:
                    color = 0
                    if char.isupper():
                        color = 1
                        char = char.lower()
                    for piecetype in range(6):
                        if piecetype == piece_strings[char]:
                            self.pieces[color][piecetype][index] = 1
                        else:
                            self.pieces[0][piecetype][index] = 0
                            self.pieces[1][piecetype][index] = 0
                    index += 1

        self.update_all_pieces()

    def __str__(self):
        '''
        Print current position
        '''
        board_str = "." * 64
        board_str = list(board_str)

        piece_strings = {0: 'p', 1: 'n', 2: 'b', 3: 'r', 4: 'q', 5: 'k'}

        for i in [0, 1]:
            piece = ""
            for j in range(6):
                piece = piece_strings[j]
                if i == 1:
                    piece = piece.upper()

                for square in range(64):
                    if self.pieces[i][j][square]:
                        board_str[square] = piece

        board_str = "".join(board_str)[::-1]
        board_str = list(board_str)
        for i in range(8):
            x = board_str[i * 8:(i + 1) * 8]
            board_str[i * 8:(i + 1) * 8] = x[::-1]
            board_str[(i + 1) * 8 - 1] += '\n'
        board_str = " ".join(board_str)
        board_str = " " + board_str

        return "To move: {}\n{}\nEn passent square: \
                {}\nmoves played: {}".format(self.to_move, board_str,
                                             self.en_passant,
                                             self.fullmove_counter)

    def make_move(self, move):
        '''
        Apply move to board, check if move is valid

        Args:
            move (tuple): Tuple containing (square from, square to, promotion)
        '''
        # check if indices in bound
        square_from, square_to, promotion = move
        color, piece_to_move = self.piece_on(square_from)
        if not 0 <= square_from <= 63 or not 0 <= square_to <= 63:
            raise IndexError("Square outside the Board")
        # check if a piece (and which) is on square from
        if not self.all_pieces[square_from]:
            raise ValueError("There is no piece on the square")
        # check if piece can go to square to
        if not mvg.check_piece_move(move, self):
            raise ValueError("Move {} is not possible".format(move))
        # check if color to move afterwards in check
        if self.in_check_after_move(move):
            raise ValueError("You are in Check!")

        # update bbs for moving piece
        self.update_piece(self.to_move, piece_to_move, square_from, square_to)

        # check if move is capture:
        if self.all_pieces_color[1 - self.to_move][square_to]:
            for i in range(5):
                self.pieces[1 - self.to_move][i][square_to] = 0
            self.all_pieces_color[1 - self.to_move][square_to] = 0

        # set square of captured pawn
        if self.to_move:
            pawn_square = square_to - 8
        else:
            pawn_square = square_to + 8

        # if move is an en passant capture remove pawn
        if piece_to_move == 0 and self.en_passant[square_to]:
            self.pieces[1 - self.to_move][0][pawn_square] = 0
            self.all_pieces_color[1 - self.to_move][pawn_square] = 0
            self.all_pieces[pawn_square] = 0

        # if pawn double move set en passent square
        if piece_to_move == 0 and abs(square_from - square_to) == 16:
            self.en_passant = bitboard_of_index(pawn_square)
        else:
            self.en_passant = xmpz(0b0)

        # if castles update rook
        if piece_to_move == 5:
            if move == (4, 6, None):
                self.update_piece(1, 3, 7, 5)
            elif move == (4, 2, None):
                self.update_piece(1, 3, 0, 3)
            elif move == (60, 62, None):
                self.update_piece(0, 3, 63, 61)
            elif move == (60, 58, None):
                self.update_piece(0, 3, 56, 59)

        # update castling rights
        self.update_castling_rights(move, piece_to_move)

        # if move is promotion set new piece and remove pawn
        if promotion:
            # REVIEW rather without update of square_to
            self.update_piece(self.to_move, promotion, square_from, square_to)
            self.pieces[self.to_move][0][square_to] = 0

        self.to_move = 1 - self.to_move

        return self


    def make_generated_move(self, move):
        '''
        Apply generated move to board (no check for validity of the move)

        Args:
            move (tuple): Tuple containing (square from, square to, pomotion)
        '''
        square_from, square_to, promotion = move
        color, piece_to_move = self.piece_on(square_from)

        # update bbs for moving piece
        self.update_piece(self.to_move, piece_to_move, square_from, square_to)

        # check if move is capture:
        if self.all_pieces_color[1 - self.to_move][square_to]:
            for i in range(5):
                self.pieces[1 - self.to_move][i][square_to] = 0
            self.all_pieces_color[1 - self.to_move][square_to] = 0

        # set square of captured pawn
        if self.to_move:
            pawn_square = square_to - 8
        else:
            pawn_square = square_to + 8

        # if move is an en passant capture remove pawn
        if piece_to_move == 0 and self.en_passant[square_to]:
            self.pieces[1 - self.to_move][0][pawn_square] = 0
            self.all_pieces_color[1 - self.to_move][pawn_square] = 0
            self.all_pieces[pawn_square] = 0

        # if pawn double move set en passent square
        if piece_to_move == 0 and abs(square_from - square_to) == 16:
            self.en_passant = bitboard_of_index(pawn_square)
        else:
            self.en_passant = xmpz(0b0)

        # if castles update rook
        if piece_to_move == 5:
            if move == (4, 6, None):
                self.update_piece(1, 3, 7, 5)
            elif move == (4, 2, None):
                self.update_piece(1, 3, 0, 3)
            elif move == (60, 62, None):
                self.update_piece(0, 3, 63, 61)
            elif move == (60, 58, None):
                self.update_piece(0, 3, 56, 59)

        # update castling rights
        self.update_castling_rights(move, piece_to_move)

        # if move is promotion set new piece and remove pawn
        if promotion:
            # REVIEW rather without update of square_to
            self.update_piece(self.to_move, promotion, square_from, square_to)
            self.pieces[self.to_move][0][square_to] = 0

        # if self.all_pieces_color[1 - self.to_move][square_to]:
        #     self.halfmove_clock = 0
        # elif piece_to_move == 0:
        #     self.halfmove_clock = 0
        # else:
        #     self.halfmove_clock += 1
        #
        # if not self.to_move:
        #     self.fullmove_counter += 1

        self.to_move = 1 - self.to_move

        return self

    def gen_legal_moves(self):
        '''
        Generates all legal moves for the color to move in the current position

        Returns:
            iterable of the legal moves
        '''
        return itertools.filterfalse(lambda moves: self.in_check_after_move(moves),
                                     mvg.generate_moves(self))

    def update_all_pieces(self):
        '''
        Update the bitboards containing positions of all pieces
        '''
        self.all_pieces = xmpz(0b0)
        self.all_pieces_color[0] = xmpz(0b0)
        self.all_pieces_color[1] = xmpz(0b0)

        for i in range(6):
            self.all_pieces_color[1] |= self.pieces[1][i]

        for i in range(6):
            self.all_pieces_color[0] |= self.pieces[0][i]

        self.all_pieces |= self.all_pieces_color[0]
        self.all_pieces |= self.all_pieces_color[1]

    def piece_on(self, square):
        '''
        Check what piece is on certain square

        Args:
            square (int): square to check for pieces

        Returns:
            (tuple): tuple containing:
                color (int): color of the piece on the square
                piecetype (int): type of the piece on the square
        '''
        for color, piecetype in itertools.product(range(2), range(6)):
            if self.pieces[color][piecetype][square]:
                return color, piecetype
        return None, None

    def board_copy(self):
        '''
        Creates a copy of the board

        Returns:
            Board: Copy of the current board state
        '''
        new_board = Board()
        for color, piecetype in itertools.product(range(2), range(6)):
            new_board.pieces[color][piecetype] = self.pieces[color][piecetype].copy()
        new_board.to_move = self.to_move
        new_board.en_passant = self.en_passant.copy()
        new_board.castling_rights = self.castling_rights.copy()
        new_board.all_pieces = self.all_pieces.copy()
        new_board.all_pieces_color[0] = self.all_pieces_color[0].copy()
        new_board.all_pieces_color[1] = self.all_pieces_color[1].copy()
        return new_board

    def in_check(self):
        '''
        Check if current color to move is in check

        Returns:
            bool: True if color is in check, False otherwise
        '''
        return mvg.color_in_check(self)

    def in_check_after_move(self, move):
        '''
        Apllies a move to check if the color to move is in check afterwards

        Args:
            move (tuple): move given in the form (square_from, square_to, promotion)

        Returns:
            bool: True if check after move, False otherwise
        '''
        square_from, square_to, promotion = move
        color, piece_to_move = self.piece_on(square_from)
        tmp_board = self.board_copy()

        tmp_board.update_piece(tmp_board.to_move, piece_to_move, square_from, square_to)

        # check if capture:
        if tmp_board.all_pieces_color[1 - tmp_board.to_move][square_to]:
            for i in range(5):
                tmp_board.pieces[1 - tmp_board.to_move][i][square_to] = 0
            tmp_board.all_pieces_color[1 - tmp_board.to_move][square_to] = 0

        # if en passant
        if piece_to_move == 0 and tmp_board.en_passant[square_to]:
            if tmp_board.to_move:
                pawn_square = square_to - 8
            else:
                pawn_square = square_to + 8

            tmp_board.pieces[1 - tmp_board.to_move][0][pawn_square] = 0
            tmp_board.all_pieces_color[1 - tmp_board.to_move][pawn_square] = 0
            tmp_board.all_pieces[pawn_square] = 0

        return tmp_board.in_check()

    def update_piece(self, color, piece, square_from, square_to):
        '''
        update position of a piece by setting pieces, all pieces and all pieces color

        Args:
            color (int): color of the piece to update
            piece (int): piecetype of the piece to update
            square_from (int): index of the square the piece is coming from
            square_to (int): index of the square the piece is going to
        '''
        self.pieces[color][piece][square_from] = 0
        self.pieces[color][piece][square_to] = 1

        self.all_pieces[square_from] = 0
        self.all_pieces[square_to] = 1

        self.all_pieces_color[color][square_from] = 0
        self.all_pieces_color[color][square_to] = 1

    def is_checkmate(self):
        '''
        Check if color to move is checkmate

        Returns:
            bool: True if it is Checkmate, False otherwise
        '''
        if self.in_check() and not list(self.gen_legal_moves()):
            return True
        return False

    def is_stalemate(self):
        '''
        Check if color to move is stalemate

        Returns:
            bool: True if stalemate, False otherwise
        '''
        if not self.in_check() and not list(self.gen_legal_moves()):
            return True
        return False

    def update_castling_rights(self, move, piece_to_move):
        '''
        update casltling rights for a given move

        Args:
            move (tuple): Move in the form (square_from, square_to, promotion)
            piece_to_move (int): The piece to move
        '''
        square_from, square_to, promotion = move

        # if king moves update castling rights
        if piece_to_move == 5:
            if self.to_move:
                self.castling_rights['white kingside'] = 0
                self.castling_rights['white queenside'] = 0
            else:
                self.castling_rights['black kingside'] = 0
                self.castling_rights['black queenside'] = 0

        # if rook moves or is captured update castling rights
        if square_from == 0 or square_to == 0:
            self.castling_rights['white queenside'] = 0
        elif square_from == 7 or square_to == 7:
            self.castling_rights['white kingside'] = 0
        elif square_from == 56 or square_to == 56:
            self.castling_rights['black queenside'] = 0
        elif square_from == 63 or square_to == 63:
            self.castling_rights['black kingside'] = 0


    def reset_board(self):
        self.from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
