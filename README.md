# bananagramsAI
This is a project for CS 4701: Practicum in Artificial Intelligence. Our project is to build an AI that can solve Bananagrams, a game similar to Scrabble where you must build a valid, connected word board as fast as possible. Players start with 21 letter tiles and once they incorporate all of them into a valid board, they "peel" a random new letter tile from the pile and must incorporate the letter into their existing board. For full instructions for the game, please visit [here](https://bananagrams.com/blogs/news/how-to-play-bananagrams-instructions-for-getting-started).

## How to Play
To start the gameplay, use the command `python3 game.py`

To move tiles around on the board, click on the letter you wish to move and then click on the square you would like to move it to.

You can shift the position of the game board by using the arrow keys.

If you want to refresh your tiles completely, press `r`.

To peel, press `spacebar`. If there is an invalid combination of letters, they will highlight in red. If the board is valid, you will "peel" a new letter, which you can then place on the board.
## Resources

The Scrabble dictionary we will be using: <https://github.com/fogleman/TWL06.git>

python3.7 -m venv cs4701-env

source cs4300-env/bin/activatesource cs4701-env/bin/activate

pip install -r requirements.txt
