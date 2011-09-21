# Copyright 2011 Lawrence Kesteloot

import random

# http://en.wikipedia.org/wiki/Scrabble_letter_distributions#English
LETTERS = """\
AAAAAAAAAB\
BCCDDDDEEE\
EEEEEEEEEF\
FGGGHHIIII\
IIIIIJKLLL\
LMMNNNNNNO\
OOOOOOOPPQ\
RRRRRRSSSS\
TTTTTTUUUU\
VVWWXYYZ??\
"""

BLANK = "?"

def get_full_bag():
    """Returns a list of letters in the whole bag."""

    return list(LETTERS)

def generate_rack(rack, bag):
    """Given an existing rack (string) and a bag (list of letters), returns a new
    rack with a full 7 letters. The bag is modified in-place to remove the letters."""

    # Put random letters at the front.
    random.shuffle(bag)

    # Figure out how many letters we need.
    needed_letters = 7 - len(rack)

    # Fill up the rack.
    rack += "".join(bag[:needed_letters])

    # Remove from the bag.
    del bag[:needed_letters]

    print "Rack: %s" % rack

    return rack
