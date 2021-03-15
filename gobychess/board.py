#!/usr/bin/env python3

from gmpy2 import xmpz

from utils import generate_table, print_bitboard


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
        self.en_passent = None
        self.halfmove_clock = 0
        self.fullmove_clock = 1


    def from_fen(self, fen):
        words = fen.split()

        self.to_move = words[1]

        if words[2] == '-':
            self.white_kingside = 0
            self.white_queenside = 0
            self.black_kingside = 0
            self.black_queenside = 0
        if 'K' in words[2]:
            self.white_kingside = 1
        if 'Q' in words[2]:
            self.white_queenside = 1
        if 'k' in words[2]:
            self.black_kingside = 1
        if 'q' in words[2]:
            self.black_queenside = 1

        if words[3] == '-':
            self.en_passent = None
        else:
            self.en_passent = words[3]

        self.halfmove_clock = words[4]
        self.fullmove_counter = words[5]

        print(words)

    def __str__(self):
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
            board_str[i * 8 - 1] += '\n'
        board_str = "".join(board_str)

        return "To move: {}\n{}\nEn passent square: {}\nmoves played: {}".format(self.to_move, board_str, self.en_passent, self.fullmove_counter)

    def gen_moves(self):
        pass



bo = Board()

bo.from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
print()
print()
print()
print(str(bo))
