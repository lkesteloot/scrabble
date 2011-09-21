#!/usr/bin/python

"""Test the bag and rack refill."""

from board import Board
from dictionary import Dictionary
from direction import HORIZONTAL, VERTICAL
from solution import Solution
from bag import generate_rack

def rack_test():
    dictionary = Dictionary()
    dictionary.set_words(["ABC", "XYZ"])

    board = Board()
    rack = ""
    bag = ["A", "B", "C", "D", "E", "F", "G"]
    rack = generate_rack(rack, bag)
    assert len(bag) == 0
    solutions = board.generate_solutions(rack, dictionary)
    solution = board.find_best_solution(solutions, dictionary)
    assert solution and solution.word == "ABC"
    rack = solution.get_new_rack(rack)
    assert set(rack) == set(["D", "E", "F", "G"])

    # Add more.
    bag.extend(["X", "Y", "Z"])
    rack = generate_rack(rack, bag)
    assert len(bag) == 0
    solutions = board.generate_solutions(rack, dictionary)
    solution = board.find_best_solution(solutions, dictionary)
    assert solution and solution.word == "XYZ"
    rack = solution.get_new_rack(rack)
    assert set(rack) == set(["D", "E", "F", "G"])

    rack = generate_rack(rack, bag)
    assert set(rack) == set(["D", "E", "F", "G"])

if __name__ == "__main__":
    rack_test()
