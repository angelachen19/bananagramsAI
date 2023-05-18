from tile import Tile, POINTS
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
    return the best first word based on a set of tiles

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
