"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

import poc_fifteen_gui


class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction
            print self

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        if self.get_number(target_row, target_col) != 0:
            return False
        else:
            row = target_row
            col = target_col
            while True:
                col += 1
                if col >= self.get_width():
                    col = 0
                    row += 1
                    if row >= self.get_height():
                        break
#                print row, col
#                print self.get_number(row, col), (col + self._width * row)
                if self.get_number(row, col) != (col + self._width * row):
                    return False
        return True

    def position_tile(self, target_row, target_col, tile_pos):
        """
        Return move_string that moves target tile to position of 0
        without moving the tiles whose row > target_row
        """
        move_string = ''
        # Find target tile position
        ver_dis = target_row - tile_pos[0]
        hor_dis = target_col - tile_pos[1]
        # If correct tile is at the left part
        if hor_dis > 0:
            # Move 0 to target tile
            move_string += 'u' * ver_dis + 'l' * hor_dis
            # Move target tile to the position beyond target position
            if tile_pos[0] == 0:
                move_string += 'drrul' * (hor_dis - 1)
            else:
                move_string += 'urrdl' * (hor_dis - 1)
            # Move target tile down
            move_string += 'druld' * ver_dis
        # If correct tile is beyond the target position
        elif hor_dis == 0:
            move_string += 'u' * ver_dis + 'lddru' * (ver_dis - 1) + 'ld'
        # If correct tile is at the right part
        else:
            move_string += 'u' * ver_dis + 'r' * (-hor_dis)
            if tile_pos[0] == 0:
                move_string += 'dllur' * (-1 - hor_dis) + 'dllu'
            else:
                move_string += 'ulldr' * (-1 - hor_dis) + 'ulld'
            move_string += 'druld' * ver_dis
        return move_string

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        assert self.lower_row_invariant(target_row, target_col), 'Fail lower_row_invariant: bad input'
        move_string = ''
        # Find target tile position
        tile_pos = self.current_position(target_row, target_col)
        move_string += self.position_tile(target_row, target_col, tile_pos)

        self.update_puzzle(move_string)
        assert self.lower_row_invariant(target_row, target_col - 1), 'Fail lower_row_invariant: bad output'
        return move_string

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        assert self.lower_row_invariant(target_row, 0), 'Bad Input'
        move_string_1 = 'ur'
        self.update_puzzle(move_string_1)
        move_string_2 = ''
        tile_pos = self.current_position(target_row, 0)
        if self.current_position(target_row, 0) != (target_row, 0):
            move_string_2 += self.position_tile(target_row - 1,  1, tile_pos)
            move_string_2 += 'ruldrdlurdluurddlur'
            self.update_puzzle(move_string_2)

        # Move to right side
        move_string_3 = 'r' * (self.get_width() - 2)
        self.update_puzzle(move_string_3)

        return move_string_1 + move_string_2 + move_string_3


    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        if self.get_number(0, target_col) != 0:
            return False

        tile_list = set((row, col) for row in range(self.get_height()) for
            col in range(self.get_width()))

        # Tile not needed to check
        unsolved_tile_list = set((row, col) for row in range(2)
                              for col in range(target_col))
        tile_list.difference_update(unsolved_tile_list)
        tile_list.remove((0, target_col))

        for tile in tile_list:
            if self.get_number(tile[0], tile[1]) != (tile[1] +
                                                     self.get_width() * tile[0]):
                return False
        return True

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # replace with your code
        if not self.lower_row_invariant(1, target_col):
            return False
        else:
            col = target_col + 1
            while col <= (self.get_width() - 1):
                if self.get_number(0, col) != col:
                    return False
                col += 1
        return True

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        # replace with your code
        return ""

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        # replace with your code
        return ""

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        # replace with your code
        return ""

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        # Move 0 to init pos

        return ""

# Start interactive simulation
#poc_fifteen_gui.FifteenGUI(Puzzle(4, 4))


def test1():
    """
    Test1 - lower_row_invariant
    """
    test_puzzle1 = Puzzle(4, 4, [[4,2,3,7],[8,5,6,10],[9,1,0,11],[12,13,14,15]])
    print "1/True", test_puzzle1.lower_row_invariant(2, 2)
    test_puzzle2 = Puzzle(4, 4, [[4,2,3,7],[8,11,6,10],[9,1,0,5],[12,13,14,15]])
    print "2/False", test_puzzle2.lower_row_invariant(2, 2)
    test_puzzle3 = Puzzle(4, 4, [[4,2,12,7],[8,5,6,10],[9,1,0,11],[3,13,14,15]])
    print "3/False", test_puzzle3.lower_row_invariant(2, 2)
    test_puzzle4 = Puzzle(4, 4, [[4,2,15,7],[8,5,6,10],[9,1,0,11],[12,13,14,3]])
    print "4/False", test_puzzle4.lower_row_invariant(2, 2)
    test_puzzle5 = Puzzle(4, 4, [[4,2,3,7],[8,5,6,0],[9,1,10,11],[12,13,14,15]])
    print "5/False", test_puzzle5.lower_row_invariant(2, 2)
    print "6/False", test_puzzle5.lower_row_invariant(2, 1)


def test_position_tile():
    """
    Test position_tile
    """
    # Case 1
    print 'Case 1'
    test_puzzle = Puzzle(4, 4, [[11,4,2,7],[8,5,6,10],[9,0,3,1],[12,13,14,15]])
    print test_puzzle
    string = test_puzzle.position_tile(2, 1, (2, 3))
    test_puzzle.update_puzzle(string)
    # Case 2
    print 'Case 2'
    test_puzzle = Puzzle(4, 4, [[11,4,2,7],[8,5,6,10],[9,0,3,1],[12,13,14,15]])
    print test_puzzle
    string = test_puzzle.position_tile(2, 1, (1, 3))
    test_puzzle.update_puzzle(string)
    # Case 3
    print 'Case 3'
    test_puzzle = Puzzle(4, 4, [[11,4,2,7],[8,0,6,10],[9,5,3,1],[12,13,14,15]])
    print test_puzzle
    string = test_puzzle.position_tile(1, 1, (0, 3))
    test_puzzle.update_puzzle(string)
    

def test2():
    """
    Test2 - solve_interior_tile
    """
    # Case 1
    print '--------1--------'
    test_puzzle1 = Puzzle(4, 4, [[11,4,2,7],[8,5,6,10],[9,1,3,0],[12,13,14,15]])
    print test_puzzle1
    test_puzzle1.solve_interior_tile(2, 3)

    # Case 2
    print '--------2--------'
    test_puzzle2 = Puzzle(4, 4, [[9,4,2,7],[8,5,6,10],[11,1,3,0],[12,13,14,15]])
    print test_puzzle2
    test_puzzle2.solve_interior_tile(2, 3)

    # Case 3
    print '--------3--------'
    test_puzzle3 = Puzzle(4, 4, [[9,4,2,11],[8,5,6,10],[7,1,3,0],[12,13,14,15]])
    print test_puzzle3
    test_puzzle3.solve_interior_tile(2, 3)

    # Case 4
    print '--------4--------'
    test_puzzle4 = Puzzle(4, 4, [[9,4,2,5],[8,11,6,10],[7,1,3,0],[12,13,14,15]])
    print test_puzzle4
    test_puzzle4.solve_interior_tile(2, 3)

    # Case 5
    print '--------5--------'
    test_puzzle5 = Puzzle(4, 4, [[3,4,2,5],[8,1,6,9],[7,0,10,11],[12,13,14,15]])
    print test_puzzle5
    test_puzzle5.solve_interior_tile(2, 1)

    # Case 6
    print '--------6--------'
    test_puzzle5 = Puzzle(4, 4, [[3,4,2,9],[8,1,6,5],[7,0,10,11],[12,13,14,15]])
    print test_puzzle5
    test_puzzle5.solve_interior_tile(2, 1)

    # Case 7
    print '--------7--------'
    test_puzzle = Puzzle(3, 3, [[8, 7, 6], [5, 4, 3], [2, 1, 0]])
    test_puzzle.solve_interior_tile(2, 2)


def test3():
    """
    Test 3 - solve_col0_tile
    """
    # Case 1
    print 'Case 1'
    test_puzzle = Puzzle(4, 4, [[11,4,2,7],[8,5,6,10],[9,12,3,1],[0,13,14,15]])
    print test_puzzle
    test_puzzle.solve_col0_tile(3)

    # Case 2
    print 'Case 2'
    test_puzzle = Puzzle(4, 4, [[11,4,2,7],[8,5,6,10],[12,9,3,1],[0,13,14,15]])
    print test_puzzle
    test_puzzle.solve_col0_tile(3)

    # Case 3
    print 'Case 3'
    test_puzzle = Puzzle(4, 4, [[11,4,2,12],[8,5,6,10],[7,9,3,1],[0,13,14,15]])
    print test_puzzle
    test_puzzle.solve_col0_tile(3)


def test_row0_invariant():
    """
    Test 4 - row0_invariant
    """
    test_puzzle = Puzzle(3, 3, [[0, 1, 2], [3, 4, 5], [6, 7, 8]])
    print test_puzzle
    print test_puzzle.row0_invariant(0)
    
    test_puzzle = Puzzle(4, 4, [[4, 2, 0, 3], [5, 1, 6, 7], [8,9,10,11], [12,13,14,15]])
    print test_puzzle.row0_invariant(2)
#test1()
#test2()
#test_position_tile()
#test3()
test_row0_invariant()
