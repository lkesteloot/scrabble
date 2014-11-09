#!/usr/bin/python

"""Test various advanced scoring."""

from board import Board
from dictionary import Dictionary
from direction import HORIZONTAL, VERTICAL
from solution import Solution
import unittest



class Test_score(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dic = Dictionary()
        cls.dic.set_words(["HELLO", "COMPUTER", "MILO", "DOG", "DOGS", "MILOS"])

    def test_double_letter_triple_word(self):

        # Double letter and triple word.
        board = Board()
        solution = Solution(0, 0, HORIZONTAL, "HELLO")
        solution.determine_score(board, self.dic)
        self.assertEqual(solution.score, 27)

    def test_double_letter_triple_word_twice(self):
        # Double letter and triple word twice.
        board = Board()
        solution = Solution(14, 0, HORIZONTAL, "COMPUTER")
        solution.determine_score(board, self.dic)
        # C3 + O1 + M3 + 2*P=6 + U1 + T1 + E1 + R1 = 17
        # 17 * 3 * 3 = 153
        self.assertEqual(solution.score, 153)

    def test_intersecting_word(self):
        # Intersecting word.
        board = Board()
        board.add_word("MILO", Board.MID_ROW, Board.MID_COL - 1, HORIZONTAL)
        solution = Solution(Board.MID_ROW - 1, Board.MID_COL + 2, VERTICAL, "DOG")
        solution.determine_score(board, self.dic)
        # DOG = 5
        self.assertEqual(solution.score, 5)

    def test_extending_perpendicular_word(self):
        # Extending perpendicular word.
        board = Board()
        board.add_word("MILO", Board.MID_ROW, Board.MID_COL - 1, HORIZONTAL)
        solution = Solution(Board.MID_ROW - 3, Board.MID_COL + 3, VERTICAL, "DOGS")
        solution.determine_score(board, self.dic)
        # DOGS = 6*2, MILOS = 7
        self.assertEqual(solution.score, 19)

    def test_pluralizing(self):
        # Pluralizing.
        board = Board()
        solution = Solution(Board.MID_ROW, Board.MID_COL - 1, HORIZONTAL, "DOG")
        solution.determine_score(board, self.dic)
        self.assertEqual(solution.score, 10)
        board.add_solution(solution)
        solution = Solution(Board.MID_ROW, Board.MID_COL - 1, HORIZONTAL, "DOGS")
        solution.determine_score(board, self.dic)
        self.assertEqual(solution.score, 6)

    def test_cross_with_blank(self):
        dic = Dictionary()
        dic.set_words(["SA","JETS"])

        board = Board()
        board.add_word('JET', 5, 4, VERTICAL)
        sol= Solution(8, 4, HORIZONTAL, 'SA', []) 
        sol.determine_score(board, dic)
        self.assertEqual(sol.score, 13)
        sol= Solution(8, 4, HORIZONTAL, 'SA', [0]) 
        sol.determine_score(board, dic)
        self.assertEqual(sol.score, 11)
        board.add_solution(sol)

    def test_two_letter_one_blank(self):
        dic = Dictionary()
        dic.set_words(["DUCE","EGRUGEAI"])

        board = Board()
        board.add_word('DUCE', 7, 4, HORIZONTAL)
        print board
        sol= Solution(7, 7, VERTICAL, 'EGRUGEAI', [1]) 
        sol.determine_score(board, dic)
        print sol
        sol= Solution(7, 7, VERTICAL, 'EGRUGEAI', [4]) 
        sol.determine_score(board, dic)
        print sol

        solutions = board.generate_solutions('RUIAG?E', dic)
        print '\n'.join([str(s) for s in solutions])
        solution = board.find_best_solution(solutions, dic)
        print solution
        self.assertEqual(solution.score, 80)
