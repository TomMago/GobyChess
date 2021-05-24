#!/usr/bin/env python3

## TODO/FIXME/NOTE/DEPRECATED/HACK/REVIEW

import copy
import itertools

from . import movegen as mvg
from .utils import (bitboard_of_index, bitboard_of_square, get_bit,
                    print_bitboard, set_bit, unset_bit, forward_bit_scan)


class Board:
    """
    Class representing the state of a chess game

    Attributes:
        pieces (2x6 array of int): array containing piece bitboard for both colors
        to_move(int): 0 if black to move 1 if white to move
        castling_rights (dict): 1 if allowed to castle, 0 otherwise
        en_passant (int): bitboard of the en passant square
        halfmove_clock (int): counter of halfmoves
        fullmove_clock (int): counter of full moves
    """

    def __init__(self):
        self.pieces = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]

        self.to_move = 1
        self.castling_rights = {'white kingside': 1, 'white queenside': 1,
                                'black kingside': 1, 'black queenside': 1}

        self.en_passant = 0
        self.halfmove_clock = 0
        self.fullmove_counter = 1

        self.all_pieces_color = [0, 0]
        self.all_pieces = 0

    def from_fen(self, fen):
        """
        Set board to fen position

        Args:
            fen (string): string containing the fen position
        """
        self.pieces = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]

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
            self.en_passant = 0
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
                            self.pieces[0][piecetype] = unset_bit(self.pieces[0][piecetype], index)
                            self.pieces[1][piecetype] = unset_bit(self.pieces[1][piecetype], index)
                        index += 1
                else:
                    color = 0
                    if char.isupper():
                        color = 1
                        char = char.lower()
                    for piecetype in range(6):
                        if piecetype == piece_strings[char]:
                            self.pieces[color][piecetype] = set_bit(self.pieces[color][piecetype], index)
                        else:
                            self.pieces[0][piecetype] = unset_bit(self.pieces[0][piecetype], index)
                            self.pieces[1][piecetype] = unset_bit(self.pieces[1][piecetype], index)
                    index += 1

        self.update_all_pieces()

    def __str__(self):
        """
        Print current position
        """
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
                    if get_bit(self.pieces[i][j], square):
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
        """
        Apply move to board, check if move is valid

        Args:
            move (tuple): Tuple containing (square from, square to, promotion)
        """
        # check if indices in bound
        square_from, square_to, promotion = move
        piece_to_move = self.piece_on(square_from)
        if not 0 <= square_from <= 63 or not 0 <= square_to <= 63:
            raise IndexError("Square outside the Board")

        # check if a piece is on square from
        if not get_bit(self.all_pieces, square_from):
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
        if get_bit(self.all_pieces_color[1 - self.to_move], square_to):
            self.pieces[1 - self.to_move] = [unset_bit(piece, square_to) for piece in self.pieces[1 - self.to_move]]
            self.all_pieces_color[1 - self.to_move] = unset_bit(self.all_pieces_color[1 - self.to_move], square_to)

        # set square of captured pawn
        if self.to_move:
            pawn_square = square_to - 8
        else:
            pawn_square = square_to + 8

        # if move is an en passant capture remove pawn
        if piece_to_move == 0 and get_bit(self.en_passant, square_to):
            self.pieces[1 - self.to_move][0] = unset_bit(self.pieces[1 - self.to_move][0], pawn_square)
            self.all_pieces_color[1 - self.to_move] = unset_bit(self.all_pieces_color[1 - self.to_move], pawn_square)
            self.all_pieces = unset_bit(self.all_pieces, pawn_square)

        # if pawn double move set en passent square
        if piece_to_move == 0 and abs(square_from - square_to) == 16:
            self.en_passant = bitboard_of_index(pawn_square)
        else:
            self.en_passant = 0

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
            self.pieces[self.to_move][0] = unset_bit(self.pieces[self.to_move][0], square_to)

        self.to_move = 1 - self.to_move

        return self

    def make_generated_move(self, move):
        """
        Apply generated move to board (no check for validity of the move)

        Args:
            move (tuple): Tuple containing (square from, square to, pomotion)
        """
        square_from, square_to, promotion = move
        piece_to_move = self.piece_on(square_from)
        opponent = 1 - self.to_move

        # update bbs for moving piece
        self.update_piece(self.to_move, piece_to_move, square_from, square_to)

        # check if move is capture:
        if get_bit(self.all_pieces_color[opponent], square_to):
            self.pieces[opponent] = [unset_bit(piece, square_to) for piece in self.pieces[opponent]]
            self.all_pieces_color[opponent] = unset_bit(self.all_pieces_color[opponent], square_to)

        # set square of captured pawn
        if self.to_move:
            pawn_square = square_to - 8
        else:
            pawn_square = square_to + 8

        # if move is an en passant capture remove pawn
        if piece_to_move == 0 and get_bit(self.en_passant, square_to):
            self.pieces[opponent][0] = unset_bit(self.pieces[opponent][0], pawn_square)
            self.all_pieces_color[opponent] = unset_bit(self.all_pieces_color[opponent], pawn_square)
            self.all_pieces = unset_bit(self.all_pieces, pawn_square)

        # if pawn double move set en passent square
        if piece_to_move == 0 and abs(square_from - square_to) == 16:
            self.en_passant = bitboard_of_index(pawn_square)
        else:
            self.en_passant = 0

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
            self.update_piece(self.to_move, promotion, square_from, square_to)
            self.pieces[self.to_move][0] = unset_bit(self.pieces[self.to_move][0], square_to)

        if not self.to_move:
            self.fullmove_counter += 1

        self.to_move = opponent

        return self

    def gen_legal_moves(self):
        """
        Generates all legal moves for the color to move in the current position

        Returns:
            iterable of the legal moves
        """
        return itertools.filterfalse(self.in_check_after_move,
                                     mvg.generate_moves(self))

    def gen_quiet_moves(self):
        """
        Generates only capturing moves

        Returns:
            iterable of the legal moves
        """
        return itertools.filterfalse(self.in_check_after_move,
                                     mvg.generate_quiet_moves(self))

    def update_all_pieces(self):
        """
        Update the bitboards containing positions of all pieces
        """
        self.all_pieces = 0
        self.all_pieces_color = [0, 0]

        for i in range(6):
            self.all_pieces_color[1] |= self.pieces[1][i]
            self.all_pieces_color[0] |= self.pieces[0][i]

        self.all_pieces |= self.all_pieces_color[0]
        self.all_pieces |= self.all_pieces_color[1]

    def piece_on(self, square):
        """
        Check what piece is on certain square

        Args:
            square (int): square to check for pieces

        Returns:
            piece (int): type of the piece on the square
        """
        iterator = (p for p in range(6) if get_bit(self.pieces[self.to_move][p],
                                                   square))
        piece = next(iterator, None)
        return piece

    def piece_opponent_on(self, square):
        """
        Check what piece is on certain square

        Args:
            square (int): square to check for pieces

        Returns:
            piece (int): type of the piece on the square
        """
        iterator = (p for p in range(6) if get_bit(self.pieces[1 - self.to_move][p],
                                                   square))
        piece = next(iterator, None)
        return piece

    def board_copy(self):
        """
        Creates a copy of the board

        Returns:
            Board: Copy of the current board state
        """
        new_board = Board()
        new_board.pieces = [row[:] for row in self.pieces]
        new_board.to_move = self.to_move
        new_board.en_passant = self.en_passant
        new_board.castling_rights = self.castling_rights.copy()
        new_board.all_pieces = self.all_pieces
        new_board.all_pieces_color = self.all_pieces_color.copy()
        new_board.fullmove_counter = self.fullmove_counter
        return new_board

    def in_check(self):
        """
        Check if current color to move is in check

        Returns:
            bool: True if color is in check, False otherwise
        """
        return mvg.color_in_check(self)

    def in_check_after_move(self, move):
        """
        Apllies a move to check if the color to move is in check afterwards

        Args:
            move (tuple): move given in the form (square_from, square_to, promotion)

        Returns:
            bool: True if check after move, False otherwise
        """
        square_from, square_to, _ = move
        piece_to_move = self.piece_on(square_from)
        tmp_board = self.board_copy()
        opponent = 1 - tmp_board.to_move



        tmp_board.update_piece(tmp_board.to_move, piece_to_move, square_from, square_to)

        # check if capture:
        if get_bit(tmp_board.all_pieces_color[opponent], square_to):
            tmp_board.pieces[opponent] = [unset_bit(piece, square_to)
                                          for piece in self.pieces[opponent]]
            tmp_board.all_pieces_color[opponent] = unset_bit(tmp_board.all_pieces_color[opponent], square_to)

        # if en passant
        if piece_to_move == 0 and get_bit(tmp_board.en_passant, square_to):
            if tmp_board.to_move:
                pawn_square = square_to - 8
            else:
                pawn_square = square_to + 8

            tmp_board.pieces[opponent][0] = unset_bit(tmp_board.pieces[opponent][0], pawn_square)
            tmp_board.all_pieces_color[opponent] = unset_bit(tmp_board.all_pieces_color[opponent], pawn_square)
            tmp_board.all_pieces = unset_bit(tmp_board.all_pieces, pawn_square)

        return tmp_board.in_check()

    def update_piece(self, color, piece, square_from, square_to):
        """
        update position of a piece by setting pieces, all pieces and all pieces color

        Args:
            color (int): color of the piece to update
            piece (int): piecetype of the piece to update
            square_from (int): index of the square the piece is coming from
            square_to (int): index of the square the piece is going to
        """
        self.pieces[color][piece] = unset_bit(self.pieces[color][piece], square_from)
        self.pieces[color][piece] = set_bit(self.pieces[color][piece], square_to)

        self.all_pieces = unset_bit(self.all_pieces, square_from)
        self.all_pieces = set_bit(self.all_pieces, square_to)

        self.all_pieces_color[color] = unset_bit(self.all_pieces_color[color], square_from)
        self.all_pieces_color[color] = set_bit(self.all_pieces_color[color], square_to)

    def is_checkmate(self):
        """
        Check if color to move is checkmate

        Returns:
            bool: True if it is Checkmate, False otherwise
        """
        if self.in_check() and not next(self.gen_legal_moves(), False):
            return True
        return False

    def is_stalemate(self):
        """
        Check if color to move is stalemate

        Returns:
            bool: True if stalemate, False otherwise
        """
        if not self.in_check() and not next(self.gen_legal_moves(), False):
            return True
        return False

    def is_check_or_stalemate(self):
        """
        Check if color to move is check or stalemate (no legal moves)

        Returns:
            bool: True if no legal moves, False otherwise
        """
        if not next(self.gen_legal_moves(), False):
            return True
        return False

    def update_castling_rights(self, move, piece_to_move):
        """
        update castling rights for a given move

        Args:
            move (tuple): Move in the form (square_from, square_to, promotion)
            piece_to_move (int): The piece to move
        """
        square_from, square_to, _ = move

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
        if square_from == 7 or square_to == 7:
            self.castling_rights['white kingside'] = 0
        if square_from == 56 or square_to == 56:
            self.castling_rights['black queenside'] = 0
        if square_from == 63 or square_to == 63:
            self.castling_rights['black kingside'] = 0

    def reset_board(self):
        """
        Set board to starting fen
        """
        self.from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
