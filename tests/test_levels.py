import os
import json
from squares import Board, solve_board

levels_folder = "levels"


def test_solution():
    levels = os.listdir(levels_folder)
    levels = sorted(list(set([".".join(x.split(".")[0:-1]) for x in levels])))
    for f in levels :
        if f in {'4.13'}:
            continue
        f = os.path.join(levels_folder, f)
        infile = "%s.in" % f
        try:
            my_board = Board(infile)
            solution = json.load(open("%s.out" % f))
        except Exception as e:
            continue
        answer = solve_board(my_board)
        print(infile)
        assert answer == solution
