from algos import POINTS


class Tile:
    def __init__(self, letter):
        self.isPlaced = False  # True if tile is placed in valid board
        self.isBlank = True if letter == ' ' else False
        self.letter = letter
        self.points = POINTS[letter.lower()]

    def getLetter(self):
        return self.letter

    # setter for isPlaced
    def setIsPlaced(self, isPlaced):
        self.isPlaced = isPlaced
