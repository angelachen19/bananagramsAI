import string

# create dictionary for initial pool of all 144 letter tiles in bananagrams
tiles = {}
tiles.update(dict.fromkeys(['j', 'k', 'q', 'x', 'z'], 2))
tiles.update(dict.fromkeys(
    ['b', 'c', 'f', 'h', 'm', 'p', 'v', 'w', 'y'], 3))
tiles['g'] = 4
tiles['l'] = 5
tiles.update(dict.fromkeys(['d', 's', 'u'], 6))
tiles['n'] = 8
tiles.update(dict.fromkeys(['t', 'r'], 9))
tiles['o'] = 11
tiles['i'] = 12
tiles['a'] = 13
tiles['e'] = 18

# get 21 of random letters for your initial hand
