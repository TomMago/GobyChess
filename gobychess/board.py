#!/usr/bin/env python3

import itertools

from gmpy2 import bit_scan1, xmpz

from .movegen import check_piece_move, color_in_check, gen_queen_moves
from .utils import bitboard_of_square, print_bitboard, bitboard_of_index
import copy


class Board():

    def __init__(self):
        self.pieces = [[], []]
        self.pieces[0] = [xmpz(0b0000000011111111000000000000000000000000000000000000000000000000),
                          xmpz(0b0100001000000000000000000000000000000000000000000000000000000000),
                          xmpz(0b0010010000000000000000000000000000000000000000000000000000000000),
                          xmpz(0b1000000100000000000000000000000000000000000000000000000000000000),
                          xmpz(0b0001000000000000000000000000000000000000000000000000000000000000),
                          xmpz(0b0000100000000000000000000000000000000000000000000000000000000000)]
        self.pieces[1] = [xmpz(0b0000000000000000000000000000000000000000000000001111111100000000),
                          xmpz(0b0000000000000000000000000000000000000000000000000000000001000010),
                          xmpz(0b0000000000000000000000000000000000000000000000000000000000100100),
                          xmpz(0b0000000000000000000000000000000000000000000000000000000010000001),
                          xmpz(0b0000000000000000000000000000000000000000000000000000000000010000),
                          xmpz(0b0000000000000000000000000000000000000000000000000000000000001000)]
        self.to_move = 1
        self.white_kingside = 1
        self.white_queenside = 1
        self.black_kingside = 1
        self.black_queenside = 1
        self.en_passant = None
        self.halfmove_clock = 0
        self.fullmove_counter = 1

        self.all_pieces_color = [xmpz(0b0000000000000000000000000000000000000000000000000000000000000000),
                                 xmpz(0b0000000000000000000000000000000000000000000000000000000000000000)]
        # self.all_pieces_black = xmpz(0b0000000000000000000000000000000000000000000000000000000000000000)
        # self.all_pieces_white = xmpz(0b0000000000000000000000000000000000000000000000000000000000000000)
        self.all_pieces = xmpz(0b0000000000000000000000000000000000000000000000000000000000000000)

        self.update_all_pieces()

    def from_fen(self, fen):
        '''
        Set board to fen position

        Args:
            String containing the fen position
        '''
        words = fen.split()

        if words[1] == 'w':
            self.to_move = 1
        else:
            self.to_move = 0

        if words[2] == '-':
            self.white_kingside = 0
            self.white_queenside = 0
            self.black_kingside = 0
            self.black_queenside = 0
        if 'K' in words[2]:
            self.white_kingside = 1
        else:
            self.white_kingside = 0
        if 'Q' in words[2]:
            self.white_queenside = 1
        else:
            self.white_queenside = 0
        if 'k' in words[2]:
            self.black_kingside = 1
        else:
            self.black_kingside = 0
        if 'q' in words[2]:
            self.black_queenside = 1
        else:
            self.black_queenside = 0

        if words[3] == '-':
            self.en_passant = xmpz(0b0000000000000000000000000000000000000000000000000000000000000000)
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
        board_str = "".join(board_str)

        return "To move: {}\n{}\nEn passent square: \
                {}\nmoves played: {}".format(self.to_move, board_str,
                                             self.en_passant,
                                             self.fullmove_counter)

    def make_move(self, move):
        '''
        Apply move to board

        Args:
            move (Tuple): Tuple containing (square from, square to, pomotion)
        '''
        # check if indices in bound
        square_from, square_to, promotion = move
        if not 0 <= square_from <= 63 or not 0 <= square_to <= 63:
            raise IndexError("Square outside the Board")
        # check if a piece (and which) is on square from
        if not self.all_pieces[square_from]:
            raise ValueError("There is no piece on the square")
        # on what square is it not 0
        piece_to_move = 0
        while not self.pieces[self.to_move][piece_to_move]:
            piece_to_move += 1
        # check if piece can go to square to
        if not check_piece_move(piece_to_move, square_from, square_to, self):
            raise ValueError("Move is not possible")
        # check if color to move afterwards in check
        if self.in_check_after_move(piece_to_move, move):
            raise ValueError("You are in Check!")
        # if pawn
            # if check if on 7th rank
                # check if promotion given
                # apply
            # if pawn did double move
                # update en passant square
            # else set en passant square to empty
        # else:
        # apply
        # change color to move
        # update all pieces
        # update halfmove and fullmove counter
        # update castling rights


        pass

    def gen_moves(self):
        pass

    def update_all_pieces(self):
        '''
        Update the bitboards containing positions of all pieces
        '''
        self.all_pieces = xmpz(0b0000000000000000000000000000000000000000000000000000000000000000)
        self.all_pieces_color[0] = xmpz(0b0000000000000000000000000000000000000000000000000000000000000000)
        self.all_pieces_color[1] = xmpz(0b0000000000000000000000000000000000000000000000000000000000000000)

        for i, j in itertools.product(range(2), range(6)):
            self.all_pieces = self.all_pieces | self.pieces[i][j]

        for i in range(6):
            self.all_pieces_color[1] = self.all_pieces_color[1] | self.pieces[1][i]

        for i in range(6):
            self.all_pieces_color[0] = self.all_pieces_color[0] | self.pieces[0][i]

    def in_check(self):
        return color_in_check(self.to_move, self)

    def in_check_after_move(self, piece_to_move, move):
        square_from, square_to, promotion = move
        tmp_board = Board()
        tmp_board.pieces = copy.deepcopy(self.pieces)
        tmp_board.to_move = self.to_move
        tmp_board.pieces[tmp_board.to_move][piece_to_move][square_from] = 0
        tmp_board.pieces[tmp_board.to_move][piece_to_move][square_to] = 1
        # TODO not needed ?
        for i in range(4):
            tmp_board.pieces[1 - tmp_board.to_move][i][square_to] = 0
        return tmp_board.in_check()

    def test(self):
        #print((bitboard_of_index(24), self.all_pieces, self.all_pieces_color[1]))
        print(color_in_check(0, self))
