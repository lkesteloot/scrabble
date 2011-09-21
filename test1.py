#!/usr/bin/python

"""Test that it's okay to just be adjacent to a word, you don't have to actually
use up any existing letters."""

from board import Board
from dictionary import Dictionary
from direction import HORIZONTAL

def test1():
    dictionary = Dictionary()
    dictionary.set_words(["OOZ", "OOZS", "PROSAIC", "PROC", "CC"])
    board = Board()

    # With this bug we'll get "PROC" but we want "PROSAIC" (where the S is the plural
    # of "OOS"), which is longer.
    board.add_word("OOZ", Board.SIZE/2, Board.SIZE/2 - 2, HORIZONTAL)
    board.add_word("CC", Board.SIZE/2 + 1, Board.SIZE/2 - 2, HORIZONTAL)

    rack = "PROSAIC"
    solutions = board.generate_solutions(rack, dictionary)
    solution = board.find_best_solution(solutions, dictionary)
    if solution:
        print "Winner: %s" % solution
        board.add_solution(solution)
    print board

if __name__ == "__main__":
    test1()
