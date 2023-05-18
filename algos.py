from tile import Tile, POINTS
import game
from pygame import *
from time import sleep

# start of DAWG Implementation from scrabble-solver by aydinschwa on github https://github.com/aydinschwa/Scrabble-Solver/ for DAWG implementation

# the class of the node in DAWG
# TODO build this class out more


class Node:
    next_id = 0

    # what happens when class is initiated
    def __init__(self):
        self.terminal = False
        self.children = {}
        self.id = Node.next_id
        Node.next_id = Node.next_id + 1


def len_overlapping_pref(prev_word, curr_word):
    # find length of overlapping prefix
    len_overlapping_pref = 0
    for l1, l2 in (zip(prev_word, curr_word)):
        if l1 == l2:
            len_overlapping_pref = len_overlapping_pref + 1
        else:
            return len_overlapping_pref
    return len_overlapping_pref


# minimize: iterating from the final node of current word to where the curr word and prev word have the same prefix
def min(curr_node, len_overlapping_pref, checked_nodes, unchecked_nodes):
    len_unchecked_nodes = len(unchecked_nodes)
    for x in range(len_unchecked_nodes-1, len_overlapping_pref-1, -1):
        parent, letter, child = unchecked_nodes[x]
        if child in checked_nodes:
            parent.children[letter] = unchecked_nodes[child]
        else:
            checked_nodes[child] = child
        unchecked_nodes.pop()
        curr_node = parent
    return curr_node


def create_dawg(dictionary):
    root = Node()
    curr_node = root
    prev_word = ""
    checked_nodes = {root: root}
    unchecked_nodes = []

    for word_index, curr_word in enumerate(dictionary):
        len_pref = len_overlapping_pref(prev_word, curr_word)

        # if there are unchecked nodes, minimize ie go back to the pref that is on the dawg alr
        if unchecked_nodes:
            curr_node = min(curr_node, len_pref,
                            checked_nodes, unchecked_nodes)

        # adding the new nodes after nodes already on the dawg
        for l in curr_word[len_pref:]:
            # create a new node
            next_node = Node()
            curr_node.children[l] = next_node
            unchecked_nodes.append((curr_node, l, next_node))
            curr_node = next_node

        # finished checking the entire word
        curr_node.terminal = True
        prev_word = curr_word

    min(curr_node, 0, checked_nodes, unchecked_nodes)
    return root


def is_valid_word(word, curr_node):
    for l in word:
        if l not in curr_node.children:
            return False
        curr_node = curr_node.children[l]

    if curr_node.terminal == True:
        return True
    else:
        return False


def is_prefix(pref, curr_node):
    for l in pref:
        if l not in curr_node.children:
            return False
        curr_node = curr_node.children[l]
    return True
# end of DAWG Implementation from scrabble-solver by aydinschwa on github https://github.com/aydinschwa/Scrabble-Solver/ for DAWG implementation


def score(word):
    """
    Finds the score of a word based on the scrabble system

    Parameters
    =======
    word: string

    Returns
    =======
    score: int
    """
    word = word.lower()
    score = 0
    for i in word:
        score += POINTS[i]
    return score


def get_first_word(tiles, curr_word, valid_words, curr_node):
    """
    return the best word based on a set of tiles

    tiles: list of tile objects
    dawg: points to the root node of our DAWG
    """
    if len(tiles) == 0:
        return get_highest_scoring(valid_words)
    for l in curr_node.children:
        for idx, t in enumerate(tiles):
            letter = t.getLetter()
            if l == letter:
                tiles_copy = tiles[:idx]+tiles[idx+1:]
                next_word = curr_word+letter
                child = curr_node.children[l]
                if child.terminal:
                    valid_words.append(next_word)
                get_first_word(tiles_copy, next_word, valid_words, child)
    return get_highest_scoring(valid_words)


def get_highest_scoring(valid_words):
    opt = ""
    max_score = 0
    for word in valid_words:
        if score(word) >= max_score:
            opt = word
            max_score = score(word)
    return opt


def find_word_and_loc(game, dawg):
    """
    Returns the optimal word's starting index, as (col,row), the optimal word,
    and the direction that the word goes (rightwards -> True, downwards -> False)

    For a word to be playable, it must be connected to the existing tiles on
    the board and it must not overlap with any other words.

    game: Game object
    dawg: node, root of DAWG
    """
    tup = game.getTiles()
    rack = []       # unplayed tiles
    anchors = []    # list of tuples of (col,row,tile) of tiles on the board
    playable = []   # list of tuples of (col,row,word,isHorizontal)
    playable_words = []  # list of words -- makes it easier to find highest scoring one
    for (col, row, tile) in tup:
        if tile.isPlaced:
            anchors.append((col, row, tile))
        else:
            rack.append(tile)
    # try one anchor tile at a time to build our next word
    for col, row, anchor_tile in anchors:
        rack.append(anchor_tile)
        word = get_first_word(rack, "", [], dawg)

        # word needs to contain the anchor to be connected to the board
        anchor_index = word.find(anchor_tile.letter)
        if anchor_index != -1:
            left_empty = True
            right_empty = True
            above_empty = True
            below_empty = True
            for i in range(anchor_index):
                # check that each tile to the left of anchor is blank
                if (col-i-1) < 0 or game.array[col-i-1][row].getLetter() != ' ':
                    left_empty = False
                # check above anchor
                if (row-i-1) < 0 or game.array[col][row-i-1].getLetter() != ' ':
                    above_empty = False
            for j in range(anchor_index+1, len(word)):
                # check to the right of anchor
                if (col+j) >= game.ROWS or game.array[col+j][row].getLetter() != ' ':
                    right_empty = False
                # check below anchor
                if (row+j) >= game.COLS or game.array[col][row+j].getLetter() != ' ':
                    below_empty = False
            isHorizontal = left_empty and right_empty
            isVertical = above_empty and below_empty
            # if word is playable
            if (isHorizontal or isVertical):
                if isHorizontal:
                    playable.append(
                        (col, row, word, True))
                else:
                    playable.append(
                        (col, row-anchor_index, word, False))
                playable_words.append(word)
        rack = rack[:-1]
    opt = get_highest_scoring(playable_words)
    idx = playable_words.index(opt)
    # returns the tuple of the form (col, row, word, isHorizontal) at index idx
    return playable[idx]


def play_word(game, col, row, word, isHorizontal):
    """
    Updates the game board with the word placed on it.

    game: Game object
    col: int, x index where the word begins
    row: int, y index where the word begins
    word: string, word to be played
    isHorizontal: boolean, True->rightward, False->downward
    """
    word_copy = word.lower()
    while word_copy:
        for ii in range(game.COLS):
            for jj in range(game.ROWS):
                tile = game.array[ii][jj]
                letter = tile.getLetter().lower()
                if letter in word_copy:
                    word_copy = word_copy.replace(
                        letter, "")
                    tile.letter = ' '
    for i in range(len(word)):
        tile = Tile(word[i].upper())
        tile.setIsPlaced(True)
        if isHorizontal:
            game.array[col+i][row] = tile
        else:
            game.array[col][row+i] = tile
        game.drawconsole()
        game.drawgameboard()
        display.flip()
        sleep(0.15)
    return game.array


def get_all_words(game, dawg):
    """""

    game: Game object
    dawg: dawg of valid words
    """
    play_word(game, 13, 13, get_first_word(), True)
    while not game.done:
        # TODO - continuous gameplay
        pass
