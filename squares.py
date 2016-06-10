import copy
import sys

DOWN = (1, 0)
UP = (-1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

OPPOSITE_DIRECTIONS = {
    DOWN: UP,
    UP: DOWN,
    LEFT: RIGHT,
    RIGHT: LEFT
}

HUMAN_READABLE = {
    DOWN: "DOWN",
    UP: "UP",
    LEFT: "LEFT",
    RIGHT: "RIGHT"
}
DIRECTIONS = [DOWN, UP, LEFT, RIGHT]

FILLED = 'f'
MRSQUARE = 's'
CONFUSEDMRSQUARE = 'c'
EMPTY = 'e'
DOWN_SETTER = 'd'
UP_SETTER = 'u'
LEFT_SETTER = 'l'
RIGHT_SETTER = 'r'
WARP = 'w'
DIRECTION_SETTER_SQUARES = {DOWN_SETTER, UP_SETTER, LEFT_SETTER, RIGHT_SETTER}
DIRECTION_SETTER_TO_DIRECTION = {
    DOWN_SETTER: DOWN,
    UP_SETTER: UP,
    LEFT_SETTER: LEFT,
    RIGHT_SETTER: RIGHT
}


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
        return [HUMAN_READABLE[x] for x in path]
    else:
        raise Exception("Unable to solve board")


def update_board(mrsquare, mrsquares, new_board):
    try:
        new_location = mrsquare.row + mrsquare.direction[0], mrsquare.col + mrsquare.direction[1]
        destination = new_board.data[new_location[0]][new_location[1]]
        if destination in {FILLED} or any([x.is_here(new_location) for x in mrsquares]):
            return False

        if destination in {EMPTY}:
            new_board.data[new_location[0]][new_location[1]] = FILLED
            mrsquare.move(mrsquare.direction)
            return True

        if destination in {DIRECTION_SETTER_SQUARES}:
            mrsquare.move(mrsquare.direction)
            mrsquare.set_absolute_direction(DIRECTION_SETTER_TO_DIRECTION[destination])
            return True

        if destination in {WARP}:
            new_location = new_board.warp_destination(new_location)
            mrsquare.row = new_location[0]
            mrsquare.col = new_location[1]
            return True

        raise Exception("What the fuck happened on update")
    except IndexError as e:
        print(e)
        raise e


class MrSquare(object):
    def __init__(self, row, col, is_confused=False):
        self.row = row
        self.col = col
        self.is_confused = is_confused
        self.direction = None

    def move(self, direction):
        self.row += direction[0]
        self.col += direction[1]

    def set_absolute_direction(self, direction):
        self.direction = direction

    def set_direction(self, direction):
        if self.is_confused:
            self.direction = OPPOSITE_DIRECTIONS[direction]
        else:
            self.direction = direction

    def get_direction(self):
        return self.direction

    def is_here(self, square):
        return self.row == square[0] and self.col == square[1]


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
        self._find_warps()

    def _find_mr_squares(self):
        self.mrsquares = list()
        for row in xrange(self.rows):
            for col in xrange(self.cols):
                if self.data[row][col] == MRSQUARE:
                    self.mrsquares.append(MrSquare(row, col))
                    self.data[row][col] = FILLED
                if self.data[row][col] == CONFUSEDMRSQUARE:
                    self.mrsquares.append(MrSquare(row, col, True))
                    self.data[row][col] = FILLED

    def _find_warps(self):
        warps = []
        for row in xrange(self.rows):
            for col in xrange(self.cols):
                if self.data[row][col] == WARP:
                    warps.append((row, col))
        if len(warps) == 0:
            return
        if len(warps) != 2:
            raise Exception("More than two warps!")
        self.warps = {
            warps[0]: warps[1],
            warps[1]: warps[0]
        }

    def warp_destination(self, location):
        return self.warps[location]

    def move(self, direction):
        """
        :param direction:
        :return: any_difference, new_board
        """
        dirty = True
        move_count = 0
        new_board = copy.deepcopy(self)
        for mrsquare in new_board.mrsquares:
            mrsquare.set_direction(direction)
        while dirty:
            to_update_board = copy.deepcopy(new_board)
            dirty = False
            for mrsquare in to_update_board.mrsquares:
                ret_val = update_board(mrsquare, new_board.mrsquares, to_update_board)
                if ret_val:
                    dirty = True
                    move_count += 1
            if dirty:
                new_board = to_update_board
        for mrsquare in new_board.mrsquares:
            mrsquare.set_direction(None)
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
