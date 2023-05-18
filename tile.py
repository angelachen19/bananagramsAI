
POINTS = {'a': 1, 'e': 1, 'i': 1, 'o': 1, 'u': 1, 'l': 1, 'n': 1, 's': 1, 't': 1, 'r': 1,
          'd': 2, 'g': 2,
          'b': 3, 'c': 3, 'm': 3, 'p': 3,
          'f': 4, 'h': 4, 'v': 4, 'w': 4, 'y': 4,
          'k': 5,
          'j': 8, 'x': 8,
          'q': 10, 'z': 10, ' ': 0
          }


class Tile:
    def __init__(self, letter):
        self.isPlaced = False  # True if tile is placed in valid board
        self.isBlank = True if letter == ' ' else False
        self.letter = letter
        self.points = POINTS[letter.lower()]

    def getLetter(self) -> str:
        return self.letter

    # setter for isPlaced
    def setIsPlaced(self, bool):
        self.isPlaced = bool

    # getter for isPlaced
    def getIsPlaced(self) -> bool:
        return self.isPlaced
