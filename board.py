# Copyright 2011 Lawrence Kesteloot

"""Keeps track of the board during a game and provides functions for finding solutions."""

import re
import time

from direction import DIRECTIONS
from solution import Solution
from bag import BLANK
from board_exceptions import BoardError, OutsideError, TooManyBlanksError, InvalidPremiumError, MismatchLetterError

# Premium cells.
# http://en.wikipedia.org/wiki/Scrabble#Scoring
# Legend:
#    T = triple word
#    D = double word
#    t = triple letter
#    d = double letter
#    . = normal
# Whitespace is ignored.
PREMIUM_CELLS = """
T . . d . . . T . . . d . . T
. D . . . t . . . t . . . D .
. . D . . . d . d . . . D . .
d . . D . . . d . . . D . . d
. . . . D . . . . . D . . . .
. t . . . t . . . t . . . t .
. . d . . . d . d . . . d . .
T . . d . . . D . . . d . . T
. . d . . . d . d . . . d . .
. t . . . t . . . t . . . t .
. . . . D . . . . . D . . . .
d . . D . . . d . . . D . . d
. . D . . . d . d . . . D . .
. D . . . t . . . t . . . D .
T . . d . . . T . . . d . . T
"""
# Row-major order.
PREMIUM_CELLS = re.sub(r"\s", "", PREMIUM_CELLS)

class Board(object):
    """Stores a board during a game."""

    # Number of squares on a side.
    SIZE = 15

    # The coordinates of the center (starting) square.
    MID_ROW = SIZE/2
    MID_COL = SIZE/2

    # Number of squares on the board.
    CELL_COUNT = SIZE*SIZE

    def __init__(self):
        # Row-major order. None for empty cell.
        self.cells = [None] * self.CELL_COUNT

        # Row-major order. Whether the tile was a blank when the tile was played.
        self.is_blank = [False] * self.CELL_COUNT

    def clone(self):
        """Returns a clone of this board. The clone does not share any data
        with the original."""

        board = Board()
        board.cells = self.cells[:]
        board.is_blank = self.is_blank[:]
        return board

    @classmethod
    def get_index(cls, row, col):
        """Given the row and column of a square (0-based), returns the index into the
        arrays (also 0-based)."""

        return row*cls.SIZE + col

    @staticmethod
    def get_letter_multiplier(index):
        """Return the letter multiplier (e.g, double and triple letter score)
        for the given square."""

        ch = PREMIUM_CELLS[index]
        if ch == "d":
            return 2
        elif ch == "t":
            return 3
        else:
            return 1

    @staticmethod
    def get_word_multiplier(index):
        """Return the word multiplier (e.g, double and triple word score)
        for the given square."""

        ch = PREMIUM_CELLS[index]
        if ch == "D":
            return 2
        elif ch == "T":
            return 3
        else:
            return 1

    def is_empty(self):
        """Whether the whole board is empty. We only check the middle cell since the first
        word must go through it."""
        return not self.cells[self.get_index(self.MID_ROW, self.MID_COL)]

    def add_word(self, word, row, col, direction, word_blank_indices=None):
        """Add the given word at the location and direction. If
        word_blank_indices is a list, then it tells the indices within "word"
        where a blank was used. Returns a list of tuples, one for each letter:
        (index in word, row, column, index, character, whether square was
        blank)."""

        added_indices = []

        for word_index, ch in enumerate(word):
            if not (col < self.SIZE and row < self.SIZE):
                raise OutsideError()
            index = self.get_index(row, col)

            # Double-check that word can fit here.
            if not (self.cells[index] is None or self.cells[index] == ch):
                raise MismatchLetterError()
            added_indices.append((word_index, row, col, index, ch, self.cells[index] is None))
            self.cells[index] = ch
            if word_blank_indices and word_index in word_blank_indices:
                self.is_blank[index] = True
            row, col = direction.increment(row, col)

        return added_indices

    def add_solution(self, solution):
        """Adds the given solution to the board. See add_word() for a description
        of the returned value."""

        return self.add_word(solution.word, solution.row, solution.col,
                solution.direction, solution.word_blank_indices)

    def try_word(self, word, rack, row, col, direction):
        """Whether a word can fit at the given location with the given rack.
        If it can fit, returns a tuple of (number of "rack"'s letters that were
        used, list of indices within "word" where a blank was used, and
        a list of indices within "rack" that were used). If it cannot fit,
        returns (-1, None, None)."""

        # Number of tiles from "rack" that were used.
        rack_used_count = 0

        # Indices within "word" where a blank was used.
        word_blank_indices = []

        # Indices within "rack" that were used.
        rack_used_indices = []

        # Try each letter of the word.
        for word_index, ch in enumerate(word):
            if col >= self.SIZE:
                return -1, None, None
            if row >= self.SIZE:
                return -1, None, None
            index = self.get_index(row, col)
            cell = self.cells[index]
            if cell is None:
                # If the cell is empty, then we must use a letter from the rack.
                rack_index = rack.find(ch)
                if rack_index >= 0:
                    # We have the letter.
                    rack_used_count += 1
                    # Remove it from the rack.
                    rack = rack[:rack_index] + "!" + rack[rack_index + 1:]
                    rack_used_indices.append(rack_index)
                else:
                    # See if we have a blank we can use.
                    rack_index = rack.find(BLANK)
                    if rack_index >= 0:
                        rack_used_count += 1
                        # Remove the blank from the rack.
                        rack = rack[:rack_index] + "!" + rack[rack_index + 1:]
                        rack_used_indices.append(rack_index)
                        word_blank_indices.append(word_index)
                    else:
                        # We have no tile for this square.
                        return -1, None, None
            else:
                # See if it matches the existing letter.
                if cell != ch:
                    return -1, None, None

            row, col = direction.increment(row, col)

        return rack_used_count, word_blank_indices, rack_used_indices

    def find_edges(self, row, col, direction):
        """Start at row,col and go in direction and its opposite until we run off the
        board or find the last continuous tile. Returns (row,col,length) where length
        is the number of letters."""

        # Find start.
        while True:
            # Move in reverse until we go too far.
            row, col = direction.decrement(row, col)

            # See if we went too far.
            if row < 0 or row >= self.SIZE \
                    or col < 0 or col >= self.SIZE \
                    or not self.cells[self.get_index(row, col)]:

                # Back up one.
                row, col = direction.increment(row, col)
                break
        else:
            # Can't get here.
            raise BoardError()

        # Go forward until we've gone too far.
        for length in range(1, self.SIZE + 1):
            end_row, end_col = direction.increment(row, col, length)

            # See if we've gone too far.
            if end_row < 0 or end_row >= self.SIZE \
                    or end_col < 0 or end_col >= self.SIZE \
                    or not self.cells[self.get_index(end_row, end_col)]:

                return (row, col, length)

        # Can't get here.
        raise BoardError()

    def get_word(self, row, col, length, direction):
        """Return the word at the location and with the given length."""

        word = ""

        for i in range(length):
            index = self.get_index(row, col)
            word += self.cells[index]
            row, col = direction.increment(row, col)

        return word

    def is_relative_cell_empty(self, row, col, direction, dpos, dline):
        """Check a relative cell to see if it's empty. The dpos is along the direction
        and dline is perpendicular to it."""

        # Find the relative position.
        other_row, other_col = direction.get_relative_position(row, col, dpos, dline)

        return other_row >= 0 and other_row < Board.SIZE \
                and other_col >= 0 and other_col < Board.SIZE \
                and self.cells[Board.get_index(other_row, other_col)]

    def has_neighboring_cell(self, row, col, direction, length):
        """Returns whether the word has any cells along its length, just to the side
        of it, that are taken."""

        for i in range(length):
            if self.is_relative_cell_empty(row, col, direction, i, 1) \
                    or self.is_relative_cell_empty(row, col, direction, i, -1):

                return True

        return False

    def generate_solutions(self, rack, dictionary):
        """Generates a list of solutions for the given rack. Not all solutions are legal."""

        print "Generating solutions..."
        solutions = []
        before = time.time()

        # For each direction.
        for direction in DIRECTIONS:
            # Try every line (row or column).
            for line in range(Board.SIZE):
                # Add solutions along this line to the list.
                self.generate_solutions_in_line(rack, dictionary, line, direction, solutions)

        after = time.time()
        elapsed = after - before
        print "    Time: %.1fs (%d words/second)" % (elapsed, len(dictionary.words)/elapsed)

        return solutions

    def generate_solutions_in_line(self, rack, dictionary, line, direction, solutions):
        """Given a rack and line (row or column) add possible solutions to the list.
        Not all solutions will be legal; they're only guaranteed to fit."""

        # Figure out what letters we have. We take the union of the letters in our rack
        # and those in the line.
        available_letters = set(rack)
        available_letters.discard(BLANK)
        for pos in range(Board.SIZE):
            row, col = direction.get_absolute_position(pos, line)
            ch = self.cells[Board.get_index(row, col)]
            if ch:
                available_letters.add(ch)
        available_letters = "".join(sorted(available_letters))

        # Get the list of words that can be made with this set of letters, taking into
        # account any blanks in the rack.
        blank_count = rack.count(BLANK)
        if blank_count == 0:
            letters_map = dictionary.letters_map
        elif blank_count == 1:
            letters_map = dictionary.letters_map_one_blank
        elif blank_count == 2:
            letters_map = dictionary.letters_map_two_blanks
        else:
            raise TooManyBlanksError()

        # Try each word to see if it can fit physically. We try every combination of
        # available letters.
        possible_words = set()

        # Keep track of which letter we're using for this combination.
        used = [False]*len(available_letters)

        # How many combinations we tried.
        combinations = 0
        while True:
            combinations += 1

            # Put together the word for this combination of letters.
            word = ""
            for i, is_used in enumerate(used):
                if is_used:
                    word += available_letters[i]
            if word:
                # Add the words that can be made with this subset of letters.
                possible_words.update(letters_map[word])

            # Increment the combination.
            for j in range(len(used)):
                if not used[j]:
                    used[j] = True
                    break
                else:
                    used[j] = False
            else:
                break

        print "    Line %d: %s (%d combinations, %d words)" % (
                line, available_letters, combinations, len(possible_words))

        # Try each word.
        for word in possible_words:
            # Try each position in the line.
            for pos in range(Board.SIZE - len(word) + 1):
                # Get the absolute position given our relative position.
                row, col = direction.get_absolute_position(pos, line)

                # See if this word will physically fit and how much of our rack we're using.
                rack_used_count, word_blank_indices, rack_used_indices = self.try_word(word,
                        rack, row, col, direction)

                # If the board is empty, then we must use the middle square.
                if self.is_empty():
                    # Get the extent of our word.
                    first_row = row
                    first_col = col
                    last_row = first_row + direction.drow*(len(word) - 1)
                    last_col = first_col + direction.dcol*(len(word) - 1)

                    # See if the extent covers the middle square.
                    is_valid = rack_used_count == len(word) \
                            and first_row <= Board.MID_ROW \
                            and last_row >= Board.MID_ROW \
                            and first_col <= Board.MID_COL \
                            and last_col >= Board.MID_COL
                else:
                    # If all of the letters came from our rack, then that's allowed only
                    # if we're touching another existing letter on the board. Don't need to
                    # check the front and back of the word, that's checked separately since,
                    # if the full thing is a word, that'll be generated also.
                    if rack_used_count == len(word):
                        is_valid = self.has_neighboring_cell(row, col, direction, len(word))
                    else:
                        # Otherwise we must have used at least one letter from our rack.
                        is_valid = rack_used_count > 0

                if is_valid:
                    # Add to our list of solutions.
                    solutions.append(Solution(row, col, direction, word,
                        word_blank_indices, rack_used_indices))
                    # if blanks, try others possible indices on same letter
                    # ABa / aBA
                    for i, indice in enumerate(word_blank_indices):
                        wb = word[indice]
                        for match in re.finditer(wb, word):
                            if match != indice:
                                wbi = list(word_blank_indices)
                                wbi[i] = match.start()
                                solutions.append(Solution(row, col, direction, word,
                                    wbi, rack_used_indices))


    def find_best_solution(self, solutions, dictionary):
        """Given a list of possible solutions, score them and find the best one. Also
        eliminate invalid solutions (e.g., those that make illegal perpendicular words)."""

        best_solution = None

        for solution in solutions:
            solution.determine_score(self, dictionary)

            if solution.score > 0 and \
                    (best_solution is None or solution.score > best_solution.score):

                best_solution = solution

        return best_solution

    def __str__(self):
        """Return a string representation of the board, suitable for human viewing.
        Uses colors to highlight various squares."""

        rows = []
        for row in range(self.SIZE):
            cols = []
            for col in range(self.SIZE):
                index = self.get_index(row, col)
                cell = self.cells[index]

                cell_string = cell if cell else " "
                if self.is_blank[index]:
                    cell_string = cell.lower()

                if PREMIUM_CELLS[index] == ".":
                    background_color = 47
                    foreground_color = 30
                elif PREMIUM_CELLS[index] == "D":
                    background_color = 101
                    foreground_color = 30
                elif PREMIUM_CELLS[index] == "T":
                    background_color = 41
                    foreground_color = 30
                elif PREMIUM_CELLS[index] == "d":
                    background_color = 106
                    foreground_color = 30
                elif PREMIUM_CELLS[index] == "t":
                    background_color = 44
                    foreground_color = 37
                else:
                    raise InvalidPremiumError()

                if self.is_blank[index]:
                    background_color = 43
                    foreground_color = 30

                # 256-color Xterm code is \033[38;5;Xm or 48 for background.
                # We're using 8-color mode here.
                cell_string = u"\u001b[%d;%dm %s \u001b[0m" % (
                        background_color, foreground_color, cell_string)

                cols.append(cell_string)
            rows.append("".join(cols))
        return "\n".join(rows)

if __name__ == "__main__":
    # List all colors.
    for i in range(256):
        print u"%d: \u001b[%dmABCDEFGH\u001b[0m" % (i, i)
