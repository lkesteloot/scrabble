# Copyright 2011 Lawrence Kesteloot

"""Loads the dictionary and performs various lookups."""

import collections

from board import Board

class Dictionary(object):
    """Stores a dictionary for word lookups. All words are in upper case, are
    Scrabble-suitable (no hyphens, no proper nouns, etc.), and are 15 or fewer
    letters."""

    def __init__(self):
        # List of words in no particular order.
        self.words = []

        # From string of sorted unique letters to list of words. For example, the word
        # "JELLO" would be in the list of words with the key "EJLO".
        self.letters_map = collections.defaultdict(list)

        # Same as above, but with one letter removed in the key. The word "JELLO" would
        # appear in the list for the keys "JLO", "ELO", "EJO", and "EJL". This
        # is for looking up words when you have one blank tile.
        self.letters_map_one_blank = collections.defaultdict(list)

        # Same as above, but with two letters removed in the key. The word "JELLO" would
        # appear in the list for the keys "LO", "JO", "JL", "EO", "EL", and "EJ".
        # This is for looking up words when you have two blank tiles.
        self.letters_map_two_blanks = collections.defaultdict(list)

        # Set of all words for quick lookup.
        self.word_set = set()

    @staticmethod
    def load(filename):
        """Load the dictionary from a file. The file must be whitespace-separated words.
        Creates the data structures."""

        print "Loading dictionary..."
        dictionary = Dictionary()
        print "    Loading file..."
        whole_file = file(filename).read().upper()
        print "    Splitting file..."
        words = whole_file.split()
        print "    Removing unsuitable words..."
        words = dictionary.remove_unsuitable_words(words)
        print "    Building data structures..."
        dictionary.set_words(words)

        print "    Loaded %d words" % len(dictionary.words)
        print "    Unique letter size:"
        print "        No blanks: %d" % len(dictionary.letters_map)
        print "        One blank: %d" % len(dictionary.letters_map_one_blank)
        print "        Two blanks: %d" % len(dictionary.letters_map_two_blanks)

        return dictionary

    def set_words(self, words):
        """Given a list of upper-case words, generates the internal data structures."""

        self.words = words
        self.generate_letter_maps()
        self.word_set = set(self.words)

    @staticmethod
    def remove_unsuitable_words(words):
        """Remove words that can't be used in Scrabble, such as those with hyphens
        and those larger than the size of the board."""

        max_length = Board.SIZE
        return [word for word in words if word and "-" not in word and len(word) <= max_length]

    def generate_letter_maps(self):
        """Generate the maps from the used letters to the list of words."""

        word_count = len(self.words)
        last_percent = 0

        # Do no-blank words.
        for i, word in enumerate(self.words):
            letters = "".join(sorted(set(word)))
            self.letters_map[letters].append(word)

            # Do one-blank words.
            for subword in self.remove_one_letter(letters):
                self.letters_map_one_blank[subword].append(word)

            # Do two-blank words.
            for subword in self.remove_two_letters(letters):
                self.letters_map_two_blanks[subword].append(word)

            # Show progress information.
            percent = int(i*100/word_count)
            if percent/10 != last_percent/10:
                print "    %d%%" % percent
                last_percent = percent

    def has_word(self, word):
        """Returns whether the word is valid for Scrabble."""
        return word in self.word_set

    @staticmethod
    def remove_one_letter(word):
        """Returns a sequence of words from "word" with each letter missing."""
        for i in range(len(word)):
            yield word[:i] + word[i + 1:]

    @staticmethod
    def remove_two_letters(word):
        """Returns a sequence of words from "word" with pairs of letters missing."""
        for i in range(len(word) - 1):
            first_part = word[:i]
            for j in range(i + 1, len(word)):
                yield first_part + word[i + 1:j] + word[j + 1:]
