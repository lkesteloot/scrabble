#!/usr/bin/python

"""Test blank tiles."""

from board import Board
from dictionary import Dictionary
from direction import HORIZONTAL, VERTICAL
from solution import Solution

def blank_test():
    dictionary = Dictionary()
    dictionary.set_words(["HELLO", "HELL"])

    # Normal find.
    board = Board()
    rack = "HELLOXX"
    solutions = board.generate_solutions(rack, dictionary)
    solution = board.find_best_solution(solutions, dictionary)
    assert solution and solution.word == "HELLO"

    # One blank, forcing solution.
    board = Board()
    rack = "HELL?XX"
    solutions = [Solution(7, 3, HORIZONTAL, "HELLO", [3])]
    solution = board.find_best_solution(solutions, dictionary)
    assert solution and solution.word == "HELLO" and solution.score == 22

    # One blank, generating solution.
    board = Board()
    rack = "HELL?XX"
    solutions = board.generate_solutions(rack, dictionary)
    solution = board.find_best_solution(solutions, dictionary)
    print rack
    print solution
    board.add_solution(solution)
    print board
    assert solution and solution.word == "HELLO" and solution.score == 22

    # Two blanks.
    board = Board()
    rack = "HEL??XX"
    solutions = board.generate_solutions(rack, dictionary)
    solution = board.find_best_solution(solutions, dictionary)
    print rack
    print solution
    board.add_solution(solution)
    print board
    assert solution and solution.word == "HELLO" and solution.score == 20

if __name__ == "__main__":
    blank_test()
