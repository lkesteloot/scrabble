#!/usr/bin/python

"""Test simple scoring."""

from board import Board
from dictionary import Dictionary

def test2():
    dictionary = Dictionary()
    dictionary.set_words(["KISSED"])
    board = Board()
    rack = "KISSEDQ"
    solutions = board.generate_solutions(rack, dictionary)
    solution = board.find_best_solution(solutions, dictionary)
    if solution:
        print "Winner: %s" % solution
        board.add_solution(solution)
    print board
    assert solution and solution.score == 32

if __name__ == "__main__":
    test2()
