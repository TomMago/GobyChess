#!/usr/bin/env python3

import itertools

from gmpy2 import xmpz

from .movegen import generate_table
from .utils import print_bitboard, bitboard_of_square


class Board():

    def __init__(self):
        self.sliding_table = generate_table()
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
        self.to_move = 'w'
        self.white_kingside = 1
        self.white_queenside = 1
        self.black_kingside = 1
        self.black_queenside = 1
        self.en_passant = None
        self.halfmove_clock = 0
        self.fullmove_counter = 1

        self.all_pieces_black = xmpz(0b0000000000000000000000000000000000000000000000000000000000000000)
        self.all_pieces_white = xmpz(0b0000000000000000000000000000000000000000000000000000000000000000)
        self.all_pieces = xmpz(0b0000000000000000000000000000000000000000000000000000000000000000)

        self.update_all_pieces()

    def from_fen(self, fen):
        '''
        Set board to fen position

        Args:
            String containing the fen position
        '''
        words = fen.split()

        self.to_move = words[1]

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
                    for i in range(int(char)):
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
                                             self.en_passant, self.fullmove_counter)

    def gen_moves(self):
        pass

    def update_all_pieces(self):
        self.all_pieces = xmpz(0b0000000000000000000000000000000000000000000000000000000000000000)
        self.all_pieces_black = xmpz(0b0000000000000000000000000000000000000000000000000000000000000000)
        self.all_pieces_white = xmpz(0b0000000000000000000000000000000000000000000000000000000000000000)

        for i, j in itertools.product(range(2), range(6)):
            self.all_pieces = self.all_pieces | self.pieces[i][j]

        for i in range(6):
            self.all_pieces_white = self.all_pieces_white | self.pieces[1][i]

        for i in range(6):
            self.all_pieces_black = self.all_pieces_black | self.pieces[0][i]
