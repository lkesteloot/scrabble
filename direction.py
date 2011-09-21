# Copyright 2011 Lawrence Kesteloot

class Direction(object):
    """Represents a direction (vertical or horizontal)."""

    def __init__(self, drow, dcol):
        """The parameters are the delta rows and delta columns. One is 1 and the other
        is zero."""

        self.drow = drow
        self.dcol = dcol

    def increment(self, row, col, distance=1):
        """Return a (row,col) pair based on the given pair and a distance and
        this direction."""

        return row + self.drow*distance, col + self.dcol*distance

    def decrement(self, row, col, distance=1):
        """Return a (row,col) pair based on the given pair and a distance and
        the opposite of this direction."""

        return row - self.drow*distance, col - self.dcol*distance

    def get_perpendicular_direction(self):
        """Given horizontal, returns vertical and vice versa."""

        return Direction(self.dcol, self.drow)

    def get_absolute_position(self, pos, line):
        """Given a line (in the orthogonal axis) and position (in the axis of this
        direction) returns a (row,col) pair for the absolute square position."""

        return self.drow*pos + self.dcol*line, self.dcol*pos + self.drow*line

    def get_relative_position(self, row, col, dpos, dline):
        """Same as get_absolute_position() but relative to the given position."""

        return row + self.drow*dpos + self.dcol*dline, \
               col + self.dcol*dpos + self.drow*dline

    def __str__(self):
        """Returns a short label for this direction."""

        return "H" if self == HORIZONTAL else "V"

# Constants representing deltas in the two directions.
HORIZONTAL = Direction(0, 1)
VERTICAL = Direction(1, 0)

# All known directions.
DIRECTIONS = [HORIZONTAL, VERTICAL]
