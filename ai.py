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


def best_first_word(curr_board, letter, calculate_score=calculate_score):
    """
    Finding the best first word given the set of characters. Best meaning the maximum 
    score based on the scrabble scoring.

    Parameters
    =======
    curr_board: 2D matrix, current state of board
    letter: string, letter peeled

    Returns
    =======
    new_board: 2D matrix, state of the board with the best first word
    """
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
