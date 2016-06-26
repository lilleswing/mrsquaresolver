import os
import json
from squares import Board, solve_board

levels_folder = "levels"


def test_set():
    b1 = Board('levels/1.1.in')
    b2 = Board('levels/1.1.in')
    assert b1 == b2
    s = set()
    s.add(b1)
    s.add(b2)
    assert len(s) == 1

def test_solution():
    levels = os.listdir(levels_folder)
    levels = sorted(list(set([".".join(x.split(".")[0:-1]) for x in levels])))
    for f in levels :
        if f in {"5.19", "6.2", "7.10", "9.14", "10.8",
                 "13.6", "13.10", "13.15", "14.10", "14.6", "14.19"}:
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
