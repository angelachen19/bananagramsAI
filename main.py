import string
import random


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

# initialize empty hand dict
hand = dict.fromkeys(string.ascii_lowercase, 0)

# random_tiles: pick num amount of random tiles


def random_tiles(num):
    for x in range(num):
        tile = (random.choices(list(tiles.keys()),
                weights=list(tiles.values())))[0]
        hand[tile] += 1
        tiles[tile] -= 1


def main():
    # get 21 of random letters for your initial hand
    random_tiles(21)
    print(hand)


if __name__ == "__main__":
    main()
