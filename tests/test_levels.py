import os
import json
from squares import Board, solve_board

levels_folder = "levels"


def test_solution():
    levels = os.listdir(levels_folder)
    levels = set([".".join(x.split(".")[0:-1]) for x in levels])
    for f in levels:
        f = os.path.join(levels_folder, f)
        infile = "%s.in" % f
        my_board = Board(infile)
        solution = json.load(open("%s.out" % f))
        assert solve_board(my_board) == solution
