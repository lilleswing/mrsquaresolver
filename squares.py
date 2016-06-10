import copy
import sys

DOWN = (1, 0)
UP = (-1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)
HUMAN_READABLE = {
    DOWN: "DOWN",
    UP: "UP",
    LEFT: "LEFT",
    RIGHT: "RIGHT"
}
DIRECTIONS = [DOWN, UP, LEFT, RIGHT]

FILLED = 'f'
MRSQUARE = 'd'
EMPTY = 'e'


def display_board(my_board):
    for line in my_board.data:
        print "".join(line)
    print("")


def display_solution(board, path):
    display_board(board)
    for direction in path:
        print("Moving %s" % HUMAN_READABLE[direction])
        ignored, board = board.move(direction)
        display_board(board)
    print([HUMAN_READABLE[x] for x in path])


def solve_board(board):
    def solve_board_helper(my_board, move_list):
        if my_board.is_solved():
            return True, move_list
        for direction in DIRECTIONS:
            is_different, new_board = my_board.move(direction)
            if not is_different:
                continue
            retval, new_path = solve_board_helper(new_board, move_list + [direction])
            if retval:
                return True, new_path
        return False, []

    is_solved, path = solve_board_helper(board, [])
    if is_solved:
        display_solution(board, path)
    else:
        raise Exception("Unable to solve board")


def update_board(mrsquare, direction, new_board):
    try:
        new_location = mrsquare.row + direction[0], mrsquare.col + direction[1]
        destination = new_board.data[new_location[0]][new_location[1]]
        if destination in {FILLED}:
            return False

        if destination in {EMPTY}:
            new_board.data[new_location[0]][new_location[1]] = FILLED
            mrsquare.move(direction)
            return True
        raise Exception("What the fuck happened on update")
    except IndexError as e:
        print(e)
        raise e


class MrSquare(object):
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def move(self, direction):
        self.row += direction[0]
        self.col += direction[1]


class Board(object):
    def __init__(self, filename):
        self.data = [list(x.strip()) for x in open(filename).readlines()]
        self.rows = len(self.data)
        self.cols = len(self.data[0])
        filler = ['f'] * self.cols
        self.data.insert(0, filler)
        self.data.append(filler)
        self.data = [['f'] + x + ['f'] for x in self.data]
        self.rows += 2
        self.cols += 2
        self._find_mr_squares()

    def _find_mr_squares(self):
        self.mrsquares = list()
        for row in xrange(self.rows):
            for col in xrange(self.cols):
                if self.data[row][col] == MRSQUARE:
                    self.mrsquares.append(MrSquare(row, col))
                    self.data[row][col] = FILLED

    def move(self, direction):
        """
        :param direction:
        :return: any_difference, new_board
        """
        dirty = True
        move_count = 0
        new_board = copy.deepcopy(self)
        while dirty:
            to_update_board = copy.deepcopy(new_board)
            dirty = False
            for mrsquare in to_update_board.mrsquares:
                ret_val = update_board(mrsquare, direction, to_update_board)
                if ret_val:
                    dirty = True
                    move_count += 1
            if dirty:
                new_board = to_update_board
        return move_count != 0, new_board

    def is_solved(self):
        for row in xrange(self.rows):
            for col in xrange(self.cols):
                if self.data[row][col] == EMPTY:
                    return False
        return True

    def __eq__(self, other):
        return self.data == other.data


def main():
    my_board = Board(sys.argv[1])
    solve_board(my_board)


if __name__ == "__main__":
    main()
