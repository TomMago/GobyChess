#!/usr/bin/env python3

from .board import Board
from .utils import move_from_san, san_from_move
from .search import Searcher

def main():

    board = Board()

    while True:
        command = input()

        if command == 'quit':
            break

        elif command == 'uci':
            print("id name GobyChess")
            print("id author Tom Magorsch")
            print("uciok")

        elif command == 'isready':
            print("readyok")

        elif command == 'ucinewgame':
            board.reset_board()

        elif command.startswith('position'):
            words = command.split(' ')

            moves_position = command.find('moves')

            if words[1] == 'fen':
                if moves_position >= 0:
                    fen_string = command[:moves_position]
                else:
                    fen_string = command

                fen = fen_string.split(' ', 2)[2]

                board.from_fen(fen)


            if words[1] == 'startpos':
                board.reset_board()

            if moves_position >= 0:
                moves = command[moves_position:].split()[1:]
            else:
                moves = []

            for move in moves:
                board.make_generated_move(move_from_san(move))

        elif command.startswith('go'):
            s = Searcher(aim_depth=4)
            evaluation = s.search_alpha_beta(board)
            #evaluation, best_move = simple_min_max(board)
            print(f'bestmove {san_from_move(s.best_move)}')

        else:
            pass


if __name__ == "__main__":
    main()
