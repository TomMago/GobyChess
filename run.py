#!/usr/bin/env python3

import timeit

from gmpy2 import xmpz

import gobychess.movegen as mvg
from gobychess.board import Board
from gobychess.utils import print_bitboard, invert_bitboard, bitboard_of_index
from gobychess.loader import loader
from gobychess.play import play_game
from gobychess.uci import main

main()

