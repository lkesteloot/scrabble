#!/usr/bin/python

"""Test various advanced scoring."""

from board import Board
from dictionary import Dictionary
from direction import HORIZONTAL, VERTICAL
from solution import Solution

def score_test():
    dictionary = Dictionary()
    dictionary.set_words(["HELLO", "COMPUTER", "MILO", "DOG", "DOGS", "MILOS"])

    # Double letter and triple word.
    board = Board()
    solution = Solution(0, 0, HORIZONTAL, "HELLO")
    solution.determine_score(board, dictionary)
    assert solution.score == 27

    # Double letter and triple word twice.
    board = Board()
    solution = Solution(14, 0, HORIZONTAL, "COMPUTER")
    solution.determine_score(board, dictionary)
    # C3 + O1 + M3 + 2*P=6 + U1 + T1 + E1 + R1 = 17
    # 17 * 3 * 3 = 153
    assert solution.score == 153

    # Intersecting word.
    board = Board()
    board.add_word("MILO", Board.MID_ROW, Board.MID_COL - 1, HORIZONTAL)
    solution = Solution(Board.MID_ROW - 1, Board.MID_COL + 2, VERTICAL, "DOG")
    solution.determine_score(board, dictionary)
    # DOG = 5
    assert solution.score == 5

    # Extending perpendicular word.
    board = Board()
    board.add_word("MILO", Board.MID_ROW, Board.MID_COL - 1, HORIZONTAL)
    solution = Solution(Board.MID_ROW - 3, Board.MID_COL + 3, VERTICAL, "DOGS")
    solution.determine_score(board, dictionary)
    # DOGS = 6*2, MILOS = 7
    assert solution.score == 19

    # Pluralizing.
    board = Board()
    solution = Solution(Board.MID_ROW, Board.MID_COL - 1, HORIZONTAL, "DOG")
    solution.determine_score(board, dictionary)
    assert solution.score == 10
    board.add_solution(solution)
    solution = Solution(Board.MID_ROW, Board.MID_COL - 1, HORIZONTAL, "DOGS")
    solution.determine_score(board, dictionary)
    assert solution.score == 6

if __name__ == "__main__":
    score_test()
