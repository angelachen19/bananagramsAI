POINTS = {'a': 1, 'e': 1, 'i': 1, 'o': 1, 'u': 1, 'l': 1, 'n': 1, 's': 1, 't': 1, 'r': 1,
          'd': 2, 'g': 2,
          'b': 3, 'c': 3, 'm': 3, 'p': 3,
          'f': 4, 'h': 4, 'v': 4, 'w': 4, 'y': 4,
          'k': 5,
          'j': 8, 'x': 8,
          'q': 10, 'z': 10
          }


def calculate_score(word):
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


class Node:
    next_id = 0

    def __init__(self):
        self.is_terminal = False
        self.id = Node.next_id
        Node.next_id += 1
        self.children = {}

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
        for key, val in self.children.items():
            out.append(key)
            out.append(str(val.id))
        return "_".join(out)

    def __hash__(self):
        return self.__repr__().__hash__()

    def __eq__(self, other):
        return self.__repr__() == other.__repr__()


def create_dawg(dict):
    pass


def search_dawg():
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
    # the board is empty and you can create any world from tile hand
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
