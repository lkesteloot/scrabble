#!/usr/bin/python

"""Test the bag and rack refill."""

from board import Board
from dictionary import Dictionary
from direction import HORIZONTAL, VERTICAL
from solution import Solution
from bag import generate_rack
import unittest
from board_exceptions import *


class Test_exceptions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dic= Dictionary()
        cls.dic.set_words(["ABC", "XYZ"])

    def test_outside(self):
        board = Board()
        board.add_word('AB', 0, 13, HORIZONTAL)
        board = Board()
        with self.assertRaises(OutsideError):
            board.add_word('ABC', 0, 13, HORIZONTAL)
        with self.assertRaises(OutsideError):
            board.add_word('ABC', 13, 0, VERTICAL)

    def test_mismatch(self):
        board = Board()
        board.add_word('AB', 0, 0, HORIZONTAL)
        with self.assertRaises(MismatchLetterError):
            board.add_word('CD', 0,0, VERTICAL)
