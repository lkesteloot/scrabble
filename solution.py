# Copyright 2011 Lawrence Kesteloot

"""Class for representing possible solutions."""

# How much each letter is worth. Blank tiles are not on this list but are worth zero points.
# http://en.wikipedia.org/wiki/Scrabble_letter_distributions#English
LETTER_SCORE = {
        "A": 1,
        "B": 3,
        "C": 3,
        "D": 2,
        "E": 1,
        "F": 4,
        "G": 2,
        "H": 4,
        "I": 1,
        "J": 8,
        "K": 5,
        "L": 1,
        "M": 3,
        "N": 1,
        "O": 1,
        "P": 3,
        "Q": 10,
        "R": 1,
        "S": 1,
        "T": 1,
        "U": 1,
        "V": 4,
        "W": 4,
        "X": 8,
        "Y": 4,
        "Z": 10,
}

SCRABBLE_BONUS = 50

class Solution(object):
    """Represents a possible solution (and optionally its score)."""

    def __init__(self, row, col, direction, word, word_blank_indices=None, rack_indices=None):
        """A word at a position and direction. word_blank_indices is a list of indices
        in word where blank tiles were used. rack_indices is a list of indices that were
        used in the rack."""
        self.row = row
        self.col = col
        self.direction = direction
        self.word = word
        self.score = None

        # List of indexes into "word" where blanks were used.
        self.word_blank_indices = word_blank_indices or []

        # List of indexes into "rack" where its letters were used.
        self.rack_indices = rack_indices or []

    def __str__(self):
        word = ''
        for i, letter in enumerate(self.word):
            if i in self.word_blank_indices:
                word += letter.lower()
            else:
                word += letter
        s = "%s (%d,%d,%s)" % (word, self.row, self.col, self.direction)
        if self.score:
            s += " = %d" % (self.score,)
        return s

    def determine_score(self, board, dictionary):
        """Sets the score field to the score of the word, or to None if the word is not legal."""

        # Make a copy so we can put our word into it.
        new_board = board.clone()

        # Get a list of letters and extra information about each.
        added_indices = new_board.add_solution(self)

        # A set of indices on the board where a new tile was placed.
        new_squares = set(index for i, row, col, index, ch, is_new in added_indices if is_new)

        score = 0

        def get_word_score(word, row, col, direction):
            """Given a word and direction, compute its score."""

            # Keep track of the multiplier for the whole word.
            word_multiplier = 1

            # Accumulated score for the word.
            word_score = 0

            for dpos, ch in enumerate(found_word):
                letter_row, letter_col = direction.get_relative_position(row, col, dpos, 0)
                index = board.get_index(letter_row, letter_col)

                # If we've added the tile, then we count the letter and word multiplier.
                if index in new_squares:
                    letter_multiplier = board.get_letter_multiplier(index)
                    word_multiplier *= board.get_word_multiplier(index)
                else:
                    # If it was an existing tile, we don't get any multipliers.
                    letter_multiplier = 1

                # zero if the tile is blank
                if new_board.is_blank[index]:
                    letter_multiplier = 0


                word_score += LETTER_SCORE[ch]*letter_multiplier

            return word_score*word_multiplier

        # See if we extended a word.
        row, col, length = new_board.find_edges(self.row, self.col, self.direction)
        found_word = new_board.get_word(row, col, length, self.direction)
        if not dictionary.has_word(found_word):
            self.score = None
            return
        else:
            # Score up the word we put down or extended.
            score += get_word_score(found_word, row, col, self.direction)

        # See if we modified a perpendicular word.
        perpendicular_direction = self.direction.get_perpendicular_direction()
        for i in range(len(self.word)):
            row, col = self.direction.increment(self.row, self.col, i)

            # We only get credit for tiles we added.
            if board.get_index(row, col) in new_squares:
                # Find the extends of the perpendicular word.
                row, col, length = new_board.find_edges(row, col, perpendicular_direction)
                if length > 1:
                    # Get the word itself.
                    found_word = new_board.get_word(row, col, length, perpendicular_direction)

                    # See if it's legit.
                    if not dictionary.has_word(found_word):
                        self.score = None
                        return
                    else:
                        # Score up the word we touched.
                        score += get_word_score(found_word, row, col, perpendicular_direction)

        self.score = score
        if len(self.rack_indices) == 7:
            self.score += SCRABBLE_BONUS

    def get_new_rack(self, rack):
        """Given this solution and the rack it came from, return the rack after the
        tiles were used."""

        return "".join(ch for i, ch in enumerate(rack) if i not in self.rack_indices)
