import dawg

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
    # Test
    print(len(checked_nodes))
    return root


def valid_word(word, curr_node):
    for l in word:
        if l not in curr_node.children:
            return False
        curr_node = curr_node.children[l]

    if curr_node.terminal == True:
        return True
    else:
        return False

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
    points_dict = {'a': 1, 'e': 1, 'i': 1, 'o': 1, 'u': 1, 'l': 1, 'n': 1, 's': 1, 't': 1, 'r': 1,
                   'd': 2, 'g': 2,
                   'b': 3, 'c': 3, 'm': 3, 'p': 3,
                   'f': 4, 'h': 4, 'v': 4, 'w': 4, 'y': 4,
                   'k': 5,
                   'j': 8, 'x': 8,
                   'q': 10, 'z': 10
                   }
    for i in word:
        score += points_dict[i]
    return score


def next_best_word(tiles, seed, curr_board, dawg):
    """
    Finding the set of possible next words given the set of tiles in the order 
    highest to lowest score based on the scrabble scoring.

    Parameters
    =======
    tiles: (list) list of letters in hand that can be played
    curr_board: ([[array]]) 2D matrix, will act as the seed
    dawg: dawg

    Returns
    =======
    words: (list) list of strings, where score(word[i]) >= score(word[i+1])
    """
    # find the longest word given the seed and set of tiles
    # check if word is in DAWG
    # best_word = ''
    # highest_score = 0

    # for i in range(len(tiles)):
    #     for j in range(i+1, len(tiles)+1):
    pass

# testing


# def heuristic(curr_board, tile_pool, best_first_word=best_first_word):
#     """
#     Completing the curr_board with values from tile_pool with heuristics of
#     best_first_word

#     Parameters
#     =======
#     curr_board: 2D matrix, current state of board
#     tile_pool: tiles to draw from

#     Returns
#     =======
#     new_board: 2D matrix, state of the board with the best first word
#     """
#     pass
