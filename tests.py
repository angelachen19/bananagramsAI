from algos import *
from tile import Tile
from game import Game
import unittest

# Check if we get the right number of tiles in hand
# Check if the hand + new tile set = original 144 tile set


class TestAlgos(unittest.TestCase):
    # testing DAWG implementation
    file = open("dictionary.txt", "r")
    data = file.read()
    scrabble_dict = data.split("\n")  # list of valid scrabble words
    test_dawg_root = create_dawg(scrabble_dict)
    file.close()

    def test_is_valid_1(self):
        self.assertEqual(is_valid_word("ZEPPELIN", self.__class__.test_dawg_root),
                         True, "ZEPPELIN is not in DAWG")

    def test_is_valid_2(self):
        print(is_valid_word("MARROWY", self.__class__.test_dawg_root))
        self.assertEqual(is_valid_word("MARROWY", self.__class__.test_dawg_root),
                         True, "MARROWY is not in DAWG")

    def test_is_valid_3(self):
        self.assertEqual(is_valid_word("BRANTAIL", self.__class__.test_dawg_root),
                         True, "BRANTAIL is not in DAWG")

    def test_is_valid_4(self):
        self.assertEqual(is_valid_word("ACEQUIAS", self.__class__.test_dawg_root),
                         True, "ACEQUIAS is not in DAWG")

    def test_is_prefix_1(self):
        self.assertEqual(is_prefix("AAHE", self.__class__.test_dawg_root),
                         True, "AAHE is not a prefix")

    def test_is_prefix_2(self):
        self.assertEqual(is_prefix("KOBOL", self.__class__.test_dawg_root),
                         True, "KOBOL is not a prefix")

    def test_is_prefix_3(self):
        self.assertEqual(is_prefix("PRODDE", self.__class__.test_dawg_root),
                         True, "PRODDE is not a prefix")

    # Testing first word
    tile_A = Tile("A")
    tile_B = Tile("B")
    tile_C = Tile("C")
    tile_D = Tile("D")
    tile_E = Tile("E")
    tile_F = Tile("F")
    tile_G = Tile("G")
    tile_H = Tile("H")
    tiles_1 = [tile_A, tile_B, tile_C, tile_D]
    tiles_2 = [tile_E, tile_F, tile_G, tile_H]
    tiles_3 = [tile_A, tile_B, tile_C, tile_D, tile_E, tile_F, tile_G, tile_H]

    def test_get_first_word1(self):
        self.assertEqual(get_first_word(self.__class__.tiles_1, "", [], self.__class__.test_dawg_root), "CAB",
                         get_first_word(self.__class__.tiles_1, "", [], self.__class__.test_dawg_root) + "not equal to CAB")

    def test_get_first_word2(self):
        self.assertEqual(get_first_word(self.__class__.tiles_2, "", [], self.__class__.test_dawg_root), "FEH",
                         get_first_word(self.__class__.tiles_2, "", [], self.__class__.test_dawg_root) + " is not equal to FEH")

    def test_get_first_word3(self):
        self.assertEqual(get_first_word(self.__class__.tiles_3, "", [], self.__class__.test_dawg_root), "CHAFED",
                         get_first_word(self.__class__.tiles_3, "", [], self.__class__.test_dawg_root) + " is not equal to CHAFED")

    # test find_word_and_loc
    # test play_word
    def test_play_word1(self):
        game = Game()
        play_word(game, 8, 8, 'CAY', True)
        output = find_word_and_loc(game, self.__class__.test_dawg_root)
        self.assertEqual(output[0], 10, str(output[0]) + ' is not 10')
        self.assertEqual(output[1], 7, str(output[1]) + ' is not 7')
        self.assertEqual(output[2], 'BY', output[2] + ' is not BY')
        self.assertEqual(output[3], False, str(
            output[3]) + ' is not False (vertical)')
        play_word(game, output[0], output[1], output[2], output[3])


if __name__ == "__main__":
    unittest.main()
