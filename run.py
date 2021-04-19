#!/usr/bin/env python3

import timeit
import time

import gobychess.movegen as mvg
from gobychess.board import Board
from gobychess.utils import print_bitboard, invert_bitboard, bitboard_of_index, perft
#from gobychess.loader import loader
#from gobychess.play import play_game
from gobychess.uci import main

main()
