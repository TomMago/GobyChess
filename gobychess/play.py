#!/usr/bin/env python3

from .board import Board
from .search import simple_min_max
from .utils import print_move, index_of_square

def play_game():
    playing = True

    board = Board()
    board.from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

    print("You are white, lets start:")
    print(board)

    while playing:
        move_input = input("Enter move (from to promotion): ")
        move_input = move_input.split()
        print(int(index_of_square(move_input[0])), type(int(index_of_square(move_input[0]))))
        print(int(index_of_square(move_input[1])), type(int(index_of_square(move_input[1]))))

        move = (int(index_of_square(move_input[0])),
                int(index_of_square(move_input[1])),
                None)

        board.make_move(move)

        if board.is_checkmate():
            print("You Won! Congratulations!")
            playing = False

        print(board)

        print("Im thinking...", end="\r")

        evalu, engine_move = simple_min_max(board, 3)

        print("I do ", print_move(engine_move))

        board.make_generated_move(engine_move)

        print(board)

        if board.is_checkmate():
            print("I Won! Better luck next time!")
            playing = False


if __name__ == "__main__":
    play_game()
