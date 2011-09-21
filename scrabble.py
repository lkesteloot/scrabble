#!/usr/bin/python

# Copyright 2011 Lawrence Kesteloot

"""Generates a Scrabble board and finds words to add."""

from board import Board
from dictionary import Dictionary
from bag import generate_rack, get_full_bag

DICTIONARY_FILENAME = "dictionary"

def main():
    # Load the dictionary.
    dictionary = Dictionary.load(DICTIONARY_FILENAME)
    board = Board()

    # Keep track of the winning solution at each round.
    winners = []

    # List of letters we can still pick from.
    bag = get_full_bag()

    # Rack starts out empty.
    rack = ""

    # Keep playing until we're out of tiles or solutions.
    while True:
        # Fill up our rack.
        print "Bag: %s" % "".join(bag)
        rack = generate_rack(rack, bag)
        if not rack:
            break

        # Get a list of possible solutions. These aren't all necessarily legal.
        solutions = board.generate_solutions(rack, dictionary)

        # Weed out the illegal solutions and score the rest, returning the
        # highest-scoring solution.
        solution = board.find_best_solution(solutions, dictionary)
        if solution:
            print "Winner: %s" % solution

            # Play the winning solution.
            board.add_solution(solution)
            winners.append((rack, solution))

            # Deplete the rack of the used tiles.
            rack = solution.get_new_rack(rack)
        else:
            # Should put letters back in bag.
            break
        print board

    print "Winners:"
    for rack, winner in winners:
        print "    %s: %s" % (rack, winner)

if __name__ == "__main__":
    main()
