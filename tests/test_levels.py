import os
import json
from squares import *


def test_solution():
    files = ['sample', 'sample2']
    for f in files:
        f = os.path.join("levels", f)
        infile = "%s.in" % f
        my_board = Board(infile)
        solution = json.load(open("%s.out" % f))
        assert solve_board(my_board) == solution
