#!/usr/bin/env python3

from .board import Board
from .search import Searcher
from .utils import index_of_square, san_from_move

def play_game():
    playing = True

    board = Board()
    board.from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

    color = input("Choose your color: w for white b for black")

    print(board)

    if color == 'w':
        print("You are white, lets go!")
        move_input = input("Enter move (from to promotion): ")
        move_input = move_input.split()
        print(int(index_of_square(move_input[0])), type(int(index_of_square(move_input[0]))))
        print(int(index_of_square(move_input[1])), type(int(index_of_square(move_input[1]))))

        move = (int(index_of_square(move_input[0])),
                int(index_of_square(move_input[1])),
                None)

        board.make_move(move)
    else:
        print("you are black, ill start!")


    while playing:

        print("Im thinking...", end="\r")

        #evalu, engine_move = alpha_beta_search(board, 6, color)
        #evalu, engine_move = simple_min_max(board, 4, color)
        s = Searcher(aim_depth=4)
        s.search_alpha_beta(board)

        engine_move = s.best_move

        print("I do ", san_from_move(engine_move))

        board.make_generated_move(engine_move)

        print(board)

        if board.is_checkmate():
            print("I Won! Better luck next time!")
            playing = False

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




if __name__ == "__main__":
    play_game()
