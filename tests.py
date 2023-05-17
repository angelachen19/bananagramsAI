from algos import *
import unittest

# Check if we get the right number of tiles in hand
# Check if the hand + new tile set = original 144 tile set


class TestAlgos(unittest.TestCase):
    # testing DAWG implementation
    file = open("dictionary.txt", "r")
    data = file.read()
    scrabble_dict = data.split("\n")  # list of valid scrabble words
    test_dawg_root = create_dawg(scrabble_dict)

    def test_dawg_1(self):
        self.assertEqual(valid_word("ZEPPELIN", self.__class__.test_dawg_root),
                         True, "ZEPPELIN is not in DAWG")

    def test_dawg_2(self):
        print(valid_word("MARROWY", self.__class__.test_dawg_root))
        self.assertEqual(valid_word("MARROWY", self.__class__.test_dawg_root),
                         True, "MARROWY is not in DAWG")

    def test_dawg_3(self):
        self.assertEqual(valid_word("BRANTAIL", self.__class__.test_dawg_root),
                         True, "BRANTAIL is not in DAWG")

    def test_dawg_4(self):
        self.assertEqual(valid_word("ACEQUIAS", self.__class__.test_dawg_root),
                         True, "ACEQUIAS is not in DAWG")

    file.close()


if __name__ == "__main__":
    unittest.main()
