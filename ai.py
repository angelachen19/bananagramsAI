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
    pass


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
