#!/usr/bin/python

"""Test blank tiles."""

from board import Board
from dictionary import Dictionary
from direction import HORIZONTAL, VERTICAL
from solution import Solution
import unittest

class Test_blank(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dic= Dictionary()
        cls.dic.set_words(["HELLO", "HELL"])
    def test_normal_find(self):
        # Normal find.
        board = Board()
        rack = "HELLOXX"
        solutions = board.generate_solutions(rack, self.dic)
        solution = board.find_best_solution(solutions, self.dic)
        self.assertIsNot(solution, None)
        self.assertEqual(solution.word, "HELLO")

    def test_one_blank_forcing_solution(self):
        # One blank, forcing solution.
        board = Board()
        rack = "HELL?XX"
        solutions = [Solution(7, 3, HORIZONTAL, "HELLO", [3])]
        solution = board.find_best_solution(solutions, self.dic)
        self.assertIsNot(solution, None)
        self.assertEqual(solution.word, "HELLO")
        self.assertEqual(solution.score, 22)

    def test_one_blank_generating_solution(self):
        # One blank, generating solution.
        board = Board()
        rack = "HELL?XX"
        solutions = board.generate_solutions(rack, self.dic)
        solution = board.find_best_solution(solutions, self.dic)
        print rack
        print solution
        board.add_solution(solution)
        print board
        self.assertIsNot(solution, None)
        self.assertEqual(solution.word, "HELLO")
        self.assertEqual(solution.score, 22)

    def test_two_blanks(self):
        # Two blanks.
        board = Board()
        rack = "HEL??XX"
        solutions = board.generate_solutions(rack, self.dic)
        solution = board.find_best_solution(solutions, self.dic)
        print rack
        print solution
        board.add_solution(solution)
        print board
        self.assertIsNot(solution, None)
        self.assertEqual(solution.word, "HELLO")
        self.assertEqual(solution.score, 20)
