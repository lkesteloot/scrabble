Scrabble
========

Copyright 2011 Lawrence Kesteloot. Not affiliated with Hasbro or Scrabble.

This is a program to automatically play Scrabble. Run with:

    % python scrabble.py

It will start with a blank board and populate it with words from a single rack.
It will keep going until the bag of tiles is empty or no word can be laid out.

The algorithm is as follows:

1. Pre-process dictionary by taking each word and adding it to a dict where the
    key is the alphabetized unique letters in the word and the value is a list
    of words. For example "HELLO" would be added to the list for the key "EHLO".

2. For each line (row or column), take the union of the rack letters and all
    letters already on that line. Remove duplicates and alphabetize. This is
    the list of usable letters.

3. Find all subsets of usable letters. Look up each subset in the dict created
    in step 1.

4. For each word in the lists looked up, try every position in the line to see
    if it can fit. It can fit if every letter in the word is either already
    on the board or can come from the rack. Add these to the list of possible
    solutions. (A solution is a word along with its position and orientation.)

5. For each possible solution, score it and see if it's a legal move. (It may
    be illegal if a perpendicular word isn't in the dictionary.)

6. Pick the solution with the highest score.

To handle blank tiles we modify the above as follows:

1. Create two other pre-processed dicts from the dictionary. They're similar
    to the original except with one or two letters removed from the key, respectively.
    So we add the word "HELLO" to the list for the key "EHLO" in the first dict.
    In the second dict we add "HELLO" to the lists for the keys "HLO", "ELO", "EHO",
    and "EHL". Finally in the third dict we add "HELLO" to the lists for the
    keys "LO", "HO", "HL", "EO", "EL", and "EH". These are the words we can
    create if our rack contains the given letters plus one or two blank tiles.

2. The rest of the algorithm is mostly unchanged, except which dictionary we use
    for lookups. This is determined by how many blanks we have in the rack (zero,
    one, or two).

3. When laying out possible solutions, if we're missing a letter in the word,
    we can use a blank tile.

4. If the blank tile replace a letter present more than one time in the word we
    generate all the solutions for each indice.

5. When placing the chosen solution on the board, put down a tile with the real
    letter (not the blank tile), but keep track of the fact that it was a blank
    so we can highlight it when displaying the board and score it zero for the
    next turn.

