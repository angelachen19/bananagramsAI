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

# Referenced


def word_from_start(start, pool, dawg):
    """
    Return the highest scoring word with prefix of `start` and using
    letters from the pool `pool`

    start: letter
    visited: list of letters we tried
    pool: list of letters in hand
    dawg: points to the root node of our DAWG
    """
    best_word = ''
    stack = []
    stack.append((start, dawg))

    while len(stack) > 0:
        curr = stack.pop()  # tuple of a string and node
        curr_node = curr[1]
        for letter in pool:
            if letter not in curr_node.children:
                continue
            letter_node = curr_node.children.get(letter)
            temp = curr[0]+letter  # temporarily append letter
            if is_valid_word(temp, dawg) and score(temp) > score(best_word):
                best_word = temp
            stack.append((letter, letter_node))
    return best_word


# def get_first_word(tiles, dawg):
#     """
#     return the best first word based on a set of tiles

#     tiles: list of tile objects
#     dawg: points to the root node of our DAWG
#     """
#     opt_word = ''
#     highest_score = 0
#     for letter in tiles:
#         pool = tiles.copy().remove(letter)
#         current_best_word = word_from_start(letter, pool, dawg)
#         if score(current_best_word) > highest_score:
#             opt_word = current_best_word
#             highest_score = score(current_best_word)
#     return opt_word


# def get_first_word(tiles, dawg):
#     """
#     return the best first word based on a set of tiles

#     tiles: list of tile objexts
#     dawg: points to the root node of our DAWG
#     """
#     opt_word = ''
#     highest_score = 0
#     curr_node = dawg
#     curr_word = ''

#     for t in enumerate(tiles):
#         letter = get_letter(tiles[t])
#         curr_word = letter
#         tiles_copy = tiles.copy()
#         unused = tiles_copy.remove(letter)
#         for t_2 in enumerate(unused):
#             letter_2 = get_letter(tiles[t_2])
#             if letter_2 in curr_node.children():
#                 curr_word += letter
#                 curr_node = curr_node.children[letter]
#                 unused = unused.remove(letter)
#                 # get_first_word()
#                 if curr_node.terminal and score(curr_word) > highest_score:
#                     opt_word = curr_word
#                     highest_score = score(curr_word)
#     return opt_word


class Node:
    """
    Represents a node in DAWG. Each node has a list of its edges to other nodes
    Nodes are equivalent if they have the same edges leading to the same states. 
    It can be used as a key in a dictionary with the __hash__ and__eq__ 
    functions.
    """
    next_id = 0

    def __init__(self):
        # terminal = a word ends at that location
        self.is_terminal = False
        self.id = Node.next_id
        Node.next_id += 1
        self.edges = {}

    def __str__(self):
        out = [f"Node {self.id}\nChildren:\n"]
        letter_child_dict = self.children.items()
        for letter, child in letter_child_dict:
            out.append(f" {letter} -> {child.id}\n")
        return " ".join(out)

    def __repr__(self):
        out = []
        if self.is_terminal:
            out.append("1")
        else:
            out.append("0")
        for key, val in self.edges.items():
            out.append(key)
            out.append(str(val.id))
        return "_".join(out)

    def __hash__(self):
        return self.__repr__().__hash__()

    def __eq__(self, other):
        return self.__repr__() == other.__repr__()


def create_dawg(dict):
    """
    Create a directed acyclic word graph (DAWG) and output to a textfile
    """
    # create root (parent for tree)
    root = Node()


def search_dawg(word, node):
    """
    Recursively find a word in DAWG, starting from a certain node
    """
    pass


def best_first_word(search_dawg=search_dawg(), calculate_score=calculate_score):
    """
    Finding the best first word given the set of tiles. Best meaning the maximum 
    score based on the scrabble scoring. Here we call on dawg with the seed nodes
    as nothing.

    Parameters
    =======


    Returns
    =======
    new_board: 2D matrix, state of the board with the best first word
    """
    # find the longest word given the seed and set of tiles
    # check if word is in DAWG
    best_word = ''
    highest_score = 0

    # for i in range(len(tiles)):
    #     for j in range(i+1, len(tiles)+1):
    pass


def heuristic(curr_board, tile_pool, best_first_word=best_first_word):
    """
    Completing the curr_board with values from tile_pool with heuristics of 
    best_first_word

    Parameters
    =======
    curr_board: 2D matrix, current state of board
    tile_pool: tiles to draw from

    Returns
    =======
    new_board: 2D matrix, state of the board with the best first word
    """
    pass
