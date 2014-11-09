#!/usr/bin/python

"""Test the bag and rack refill."""

from board import Board
from dictionary import Dictionary
from direction import HORIZONTAL, VERTICAL
from solution import Solution
from bag import generate_rack
import unittest


class Test_rack(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dic= Dictionary()
        cls.dic.set_words(["ABC", "XYZ"])

    def test_rack(self):

        board = Board()
        rack = ""
        bag = ["A", "B", "C", "D", "E", "F", "G"]
        rack = generate_rack(rack, bag)
        self.assertEqual(len(bag), 0)
        solutions = board.generate_solutions(rack, self.dic)
        solution = board.find_best_solution(solutions, self.dic)
        self.assertIsNot(solution, None)
        self.assertEqual(solution.word, "ABC")
        rack = solution.get_new_rack(rack)
        self.assertEqual(set(rack), set(["D", "E", "F", "G"]))

        # Add more.
        bag.extend(["X", "Y", "Z"])
        rack = generate_rack(rack, bag)
        self.assertEqual(len(bag), 0)
        solutions = board.generate_solutions(rack, self.dic)
        solution = board.find_best_solution(solutions, self.dic)
        self.assertIsNot(solution.word, None)
        self.assertEqual(solution.word, "XYZ")
        rack = solution.get_new_rack(rack)
        self.assertEqual(set(rack), set(["D", "E", "F", "G"]))

        rack = generate_rack(rack, bag)
        self.assertEqual(set(rack), set(["D", "E", "F", "G"]))
