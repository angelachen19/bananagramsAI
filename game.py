
from pygame import *
import random
import math
from pygame.locals import *
import mmap
from time import sleep
import numpy as np
import tile as tile

# import algos

# Implementation of Bananagrams gameplay adapted from https://github.com/erictdobbs/bananagrams

init()
mixer.init()


class Game:

    def __init__(self, ROWS=17, COLS=17, SIZE=40):
        self.ROWS = ROWS
        self.COLS = COLS
        self.SIZE = SIZE
        self.array = [[tile.Tile(' ')]*self.ROWS for x in range(self.COLS)]
        self.invalid = []
        self.isTesting = True

        self.screenwidth = int(self.SIZE * self.COLS)
        self.screenheight = int(self.SIZE * self.ROWS)
        self.framehor = self.SIZE
        self.framever = self.SIZE

        self.screen = display.set_mode(
            [self.screenwidth + self.framehor*2, self.screenheight + self.framever*5])
        display.set_caption("BANANAGRAMS!")
        self.screen.fill([200, 200, 100])
        self.reset()

    # drawconsole()
    # Draws the portion of the screen below the gameboard, including the
    # game clock.
    def drawconsole(self):
        ROWS = self.ROWS
        COLS = self.COLS
        SIZE = self.SIZE
        framehor = self.framehor
        framever = self.framever

        self.screen.fill([200, 200, 100])
        draw.rect(self.screen, [60, 60, 60], (self.framehor-3, self.framever -
                                              3 + SIZE*(ROWS+1), SIZE*COLS+7, SIZE*2+7), 3)
        draw.rect(self.screen, [60, 60, 60], (framehor, framever +
                                              SIZE*(ROWS+1), SIZE*COLS, SIZE*2), 2)
        myfont = font.SysFont("Courier", 2*SIZE - 3)
        label = myfont.render(str(round(self.gametime, 1)), 1, [0, 0, 0])
        self.screen.blit(label, (framehor + 5, framever + SIZE*(ROWS+1) + 2))

    # drawendscreen()
    # Draws the end screen when player has completed the entire board with all the letters
    def drawendscreen(self):
        SIZE = self.SIZE
        framehor = self.framehor
        framever = self.framever
        for myevent in event.get():
            if myevent.type == QUIT:
                self.done = True
            self.screen.fill('white')
            myfont = font.SysFont("Courier", 30)
            text = myfont.render("BANANAS! You win!",  1, [0, 0, 0])
            text_rect = text.get_rect(
                center=(self.screenwidth/2, self.screenheight/2))
            self.screen.blit(text, text_rect)
            text2 = myfont.render(
                "Your final time was " + str(round(self.gametime, 2)) + ' seconds', 1, [0, 0, 0])
            text_rect2 = text2.get_rect(
                center=(self.screenwidth/2 + 40, self.screenheight/2 + 40))
            self.screen.blit(text2, text_rect2)
            text3 = myfont.render(
                "Press the 'q' key to end the game.",  1, [0, 0, 0])
            text_rect3 = text3.get_rect(
                center=(self.screenwidth/2 + 80, self.screenheight/2 + 80))
            self.screen.blit(text3, text_rect3)
            if myevent.type == KEYDOWN and myevent.key == K_q:
                # quit the game
                print("Player has quit the game.")
                self.done = True
        display.flip()

    # tilecolor(char)
    # Returns a list [R,G,B] based on the character given. This function
    # is deterministic, so any given character will always get the same
    # result.

    def tilecolor(self, char):
        if char == ' ':
            return [200, 200, 100]
        if char == '_':
            return [60, 60, 30]
        value = ord(char) - 65  # range 0 to 25
        return [int(60 * (math.sin(value) + 3)), int(60 * (math.sin(3*value) + 3)), int(60 * (math.sin(5*value) + 3))]

    # drawtile(ii,jj)
    # Draws the cell at (ii,jj) to the screen. Draws the colored tile,
    # the character, and an outline.
    def drawtile(self, ii, jj):
        framehor = self.framehor
        SIZE = self.SIZE
        framever = self.framever
        tile = self.array[ii][jj]
        char = tile.getLetter()
        draw.rect(self.screen, self.tilecolor(char), (framehor +
                                                      ii*SIZE, framever + jj*SIZE, SIZE, SIZE))
        if not char in [' ', '_']:
            myfont = font.SysFont("Times New Roman", SIZE - 3)
            label = myfont.render(char, 1, [0, 0, 0])
            self.screen.blit(label, (framehor + ii*SIZE -
                                     ((myfont.size(char))[0] - SIZE)/2, framever + jj*SIZE + 1))
        draw.rect(self.screen, [60, 60, 60], (framehor + ii *
                                              SIZE, framever + jj*SIZE, SIZE, SIZE), 2)

    # drawgameboard()
    # Draws the gameboard, both the cells in the board and any tile
    # currently held. Colors borders on cells that form an incorrect
    # word.
    def drawgameboard(self):
        global wrongfade
        ROWS = self.ROWS
        COLS = self.COLS
        SIZE = self.SIZE
        framehor = self.framehor
        framever = self.framever
        draw.rect(self.screen, [60, 60, 60], (framehor-3,
                                              framever-3, SIZE*COLS+7, SIZE*ROWS+7), 3)
        for ii in range(COLS):
            for jj in range(ROWS):
                self.drawtile(ii, jj)
        if len(self.invalid) > 0:
            wrongfade -= 1
            if wrongfade < 0:
                wrongfade = 0
            for cell in self.invalid:
                draw.rect(self.screen, [60 + wrongfade, 60, 60], (framehor +
                                                                  cell[0]*SIZE, framever + cell[1]*SIZE, SIZE, SIZE), 2)
                if wrongfade == 0:
                    self.invalid.remove(cell)
        if self.grabbed != ' ':
            draw.rect(self.screen, [60, 60, 60], (framehor + self.mousex + 1 -
                                                  self.offsetx, framever + self.mousey + 1 - self.offsety, SIZE, SIZE), 1)
            draw.rect(self.screen, [60, 60, 60], (framehor + self.mousex + 2 -
                                                  self.offsetx, framever + self.mousey + 2 - self.offsety, SIZE, SIZE), 1)
            draw.rect(self.screen, self.tilecolor(self.grabbed), (framehor + self.mousex -
                                                                  self.offsetx, framever + self.mousey - self.offsety, SIZE, SIZE))
            myfont = font.SysFont("Times New Roman", SIZE - 3)
            label = myfont.render(self.grabbed, 1, [0, 0, 0])
            self.screen.blit(label, (framehor + self.mousex - self.offsetx -
                                     ((myfont.size(self.grabbed))[0] - SIZE)/2, framever + self.mousey + 1 - self.offsety))
            draw.rect(self.screen, [60, 60, 60], (framehor + self.mousex -
                                                  self.offsetx, framever + self.mousey - self.offsety, SIZE, SIZE), 2)

    # blankcoord()
    # Returns a pair (x,y) of a blank cell on the board.
    def blankcoord(self):
        COLS = self.COLS
        ROWS = self.ROWS
        blanks = []
        for ii in range(COLS):
            for jj in range(ROWS):
                if self.array[ii][jj].letter == ' ':
                    blanks.append((ii, jj))
        for jj in range(ROWS):
            if self.array[ii][jj].letter == ' ':
                blanks.append((ii, jj))
        return blanks

    def peelletter(self):
        # global letterbag, grabbed
        if self.letterbag == "":
            self.complete = True
            self.drawendscreen()
            return
        elif len(self.letterbag) == 1:
            self.grabbed = self.letterbag
            self.letterbag = ''
            self.peels += 1
        else:
            self.grabbed = random.choice(self.letterbag)
            self.letterbag.replace(self.grabbed, "", 1)
            # ADDED: Remove an additional random letter to reduce remaining letter pool
            randLetter = random.choice(self.letterbag)
            self.letterbag.replace(randLetter, "", 1)
            self.peels += 1

    def freshletters(self, numletters):
        for ii in range(self.COLS):
            for jj in range(self.ROWS):
                self.array[ii][jj] = tile.Tile(' ')
        self.letterbag = ""
        for ii in range(len(self.letters)):
            self.letterbag += self.letterfreq[ii] * self.letters[ii]
        skipanimation = False
        x = 0
        y = 0
        if self.isTesting:
            for ii in ['C', 'A', 'B', 'Y']:
                letterTile = tile.Tile(ii)
                self.array[x][y] = letterTile
                self.drawconsole()
                self.drawgameboard()
                display.flip()
                if skipanimation == False:
                    sleep(0.15)
                    # soundpop.play()
                for myevent in event.get():
                    if myevent.type == MOUSEBUTTONDOWN or myevent.type == KEYDOWN:
                        skipanimation = True
                if x == self.COLS-1:
                    x = 0
                    y += 1
                else:
                    x += 1
        else:
            for ii in range(numletters):
                character = random.choice(self.letterbag)
                letterTile = tile.Tile(character)
                newletterbag = self.letterbag.replace(character, "", 1)
                self.letterbag = newletterbag
                self.array[x][y] = letterTile
                self.drawconsole()
                self.drawgameboard()
                display.flip()
                if skipanimation == False:
                    sleep(0.15)
                    # soundpop.play()
                for myevent in event.get():
                    if myevent.type == MOUSEBUTTONDOWN or myevent.type == KEYDOWN:
                        skipanimation = True
                if x == self.COLS-1:
                    x = 0
                    y += 1
                else:
                    x += 1

    # getTiles()
    # Returns an array of tuples of (col, row, Tile objects) that are currently on the board
    def getTiles(self):
        currentBoard = []
        for ii in range(self.COLS):
            for jj in range(self.ROWS):
                if self.array[ii][jj].getLetter() != ' ':
                    currentBoard.append((ii, jj, self.array[ii][jj]))
        # test = []
        # for i in range(len(currentBoard)):
        #     test.append(currentBoard[i].getLetter())
        return currentBoard

    # resetBoard()
    # Puts letters back into initial position for player to rebuild board after peeling
    def resetBoard(self):
        currentBoard = []
        for ii in range(self.COLS):
            for jj in range(self.ROWS):
                if self.array[ii][jj].getLetter() != ' ':
                    currentBoard.append(self.array[ii][jj])
        for ii in range(self.COLS):
            for jj in range(self.ROWS):
                self.array[ii][jj] = tile.Tile(' ')
        x = 0
        y = 0
        skipanimation = False
        for ii in range(len(currentBoard)):
            self.array[x][y] = currentBoard[ii]
            self.drawgameboard()
            display.flip()
            if x == self.COLS-1:
                x = 0
                y += 1
            else:
                x += 1
        self.numBoardShuffles += 1

    # reset()
    # Resets the game to initial game state
    def reset(self):
        self.done = False
        self.peels = 0
        self.redos = 0
        self.grabbed = ' '
        self.offsetx = 0
        self.offsety = 0
        self.waitmouse = 0
        self.wrongfade = 0
        self.clock = time.Clock()
        self.gametime = 0.0
        # letterfreq = [13, 3, 3, 6, 18, 3, 4, 3, 12, 2, 2,
        #               5, 3, 8, 11, 3, 2, 9, 6, 9, 6, 3, 3, 2, 3, 2]
        self.letterfreq = [7, 2, 2, 3, 9, 2, 2, 1, 6, 1, 1,
                           2, 2, 4, 6, 2, 1, 4, 3, 4, 3, 1, 1, 1, 1, 1]
        self.letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.letterbag = ""
        for ii in range(len(self.letters)):
            self.letterbag += self.letterfreq[ii] * self.letters[ii]

        self.mousex = 0
        self.mousey = 0
        # If complete is True, the game is completed and there are no more letters to add to the board
        self.complete = False
        self.numBoardShuffles = 0
        self.freshletters(21)

    # checkdictionary(string)
    # Returns TRUE if string is in the dictionary file, or FALSE if not.
    def checkdictionary(self, string):
        if (string + "\n") in (open('dictionary.txt').read()).upper():
            return True
        else:
            return False

    # checkwords()
    # Returns TRUE if the board is in a valid configuration. This requires that:
    #    1) The cursor is not currently holding a tile
    #    2) All sets of tiles are at least 2 tiles long
    #    3) Each set of tiles forms an English word
    # Returns FALSE if any of the above conditions are not met.

    def checkwords(self):
        global wrongfade
        wrongfade = 0
        COLS = self.COLS
        ROWS = self.ROWS
        # for cell in invalid: invalid.remove(cell)
        if self.grabbed != ' ':
            return False
        valid = True

        # This section checks that all cells are part of one contiguous region
        unchecked = []
        neighbors = []
        done = []
        for ii in range(COLS):
            for jj in range(ROWS):
                if not self.array[ii][jj].isBlank and self.array[ii][jj].letter != '_':
                    unchecked.append((ii, jj))
        cell = unchecked.pop(0)
        if unchecked.count((cell[0]+1, cell[1])) != 0:
            neighbors.append((cell[0]+1, cell[1]))
            unchecked.remove((cell[0]+1, cell[1]))
        if unchecked.count((cell[0]-1, cell[1])) != 0:
            neighbors.append((cell[0]-1, cell[1]))
            unchecked.remove((cell[0]-1, cell[1]))
        if unchecked.count((cell[0], cell[1]+1)) != 0:
            neighbors.append((cell[0], cell[1]+1))
            unchecked.remove((cell[0], cell[1]+1))
        if unchecked.count((cell[0], cell[1]-1)) != 0:
            neighbors.append((cell[0], cell[1]-1))
            unchecked.remove((cell[0], cell[1]-1))
        done.append(cell)
        while len(neighbors) != 0:
            cell = neighbors.pop(0)
            if unchecked.count((cell[0]+1, cell[1])) != 0:
                neighbors.append((cell[0]+1, cell[1]))
                unchecked.remove((cell[0]+1, cell[1]))
            if unchecked.count((cell[0]-1, cell[1])) != 0:
                neighbors.append((cell[0]-1, cell[1]))
                unchecked.remove((cell[0]-1, cell[1]))
            if unchecked.count((cell[0], cell[1]+1)) != 0:
                neighbors.append((cell[0], cell[1]+1))
                unchecked.remove((cell[0], cell[1]+1))
            if unchecked.count((cell[0], cell[1]-1)) != 0:
                neighbors.append((cell[0], cell[1]-1))
                unchecked.remove((cell[0], cell[1]-1))
            done.append(cell)

        if len(unchecked) > 0:
            valid = False

        # This section makes sure all formed words are in the dictionary
        for ii in range(COLS):
            for jj in range(ROWS):
                string = ""
                if not self.array[ii][jj].letter in [' ', '_']:
                    if jj == 0 or self.array[ii][jj-1].letter in [' ', '_']:
                        kk = jj
                        while kk != ROWS and not self.array[ii][kk].letter in [' ', '_']:
                            string += self.array[ii][kk].letter
                            kk += 1
                if len(string) > 1:
                    if self.checkdictionary(string) == False or len(string) < 2:
                        kk -= 1
                        valid = False
                        while kk >= jj:
                            self.invalid.append((ii, kk))
                            kk -= 1
                string = ""
                if not self.array[ii][jj].letter in [' ', '_']:
                    if ii == 0 or self.array[ii-1][jj].letter in [' ', '_']:
                        kk = ii
                        while kk != COLS and not self.array[kk][jj].letter in [' ', '_']:
                            string += self.array[kk][jj].letter
                            kk += 1
                if len(string) > 1:
                    if self.checkdictionary(string) == False or len(string) < 2:
                        valid = False
                        kk -= 1
                        while kk >= ii:
                            self.invalid.append((kk, jj))
                            kk -= 1

        if valid == False:
            wrongfade = 195
            return False
        else:
            return True

    # countPlacedTiles()
    # Returns a tuple (placed, not placed) of ints representing the number of placed/not place tiles
    def countPlacedTiles(self):
        placed = 0
        notPlaced = 0
        for ii in range(self.COLS):
            for jj in range(self.ROWS):
                if self.array[ii][jj].getIsPlaced():
                    placed += 1
                else:
                    notPlaced += 1
        return (placed, notPlaced)

    # play()
    # Main game function, includes event handling drawing the game board, and updating
    def play(self):
        framehor = self.framehor
        framever = self.framever
        SIZE = self.SIZE
        ROWS = self.ROWS
        COLS = self.COLS

        if self.gametime == 0:
            self.clock.tick()
            self.gametime += 0.001
        else:
            if not self.complete:
                self.gametime += self.clock.tick()/1000.0
        self.drawconsole()
        self.drawgameboard()
        for myevent in event.get():  # User did something
            try:
                if myevent.type == QUIT:  # If user clicked close
                    self.done = True  # Flag that we are done so we exit this loop
                if myevent.type == MOUSEBUTTONDOWN and self.grabbed == ' ' and self.waitmouse == 0:
                    self.invalid = []
                    self.waitmouse = 1
                    self.mousex = myevent.pos[0] - framehor
                    self.mousey = myevent.pos[1] - framever
                    mousex = self.mousex
                    mousey = self.mousey
                    if self.mousex < 0 or self.mousex > self.screenwidth:
                        continue
                    if self.mousey < 0 or self.mousey > self.screenheight:
                        continue
                    if not self.array[int(mousex/SIZE)][int(mousey/SIZE)] in [' ', '_']:
                        # PICKING UP A TILE
                        self.grabbed = self.array[int(
                            mousex/SIZE)][int(mousey/SIZE)].getLetter()
                        self.array[int(mousex/SIZE)
                                   ][int(mousey/SIZE)].letter = ' '
                        self.offsetx = mousex % SIZE
                        self.offsety = mousey % SIZE
                if myevent.type == MOUSEBUTTONDOWN and self.grabbed != ' ' and self.waitmouse == 0:
                    self.invalid = []
                    self.waitmouse = 1
                    self.mousex = myevent.pos[0] - framehor
                    self.mousey = myevent.pos[1] - framever
                    mousex = self.mousex
                    mousey = self.mousey
                    offsetx = self.offsetx
                    offsety = self.offsety
                    if mousex + SIZE/2 - offsetx < 0 or mousex + SIZE/2 - offsetx > self.screenwidth:
                        continue
                    if mousey + SIZE/2 - offsety < 0 or mousey + SIZE/2 - offsety > self.screenheight:
                        continue
                    if self.array[int((mousex + SIZE/2 - offsetx)/SIZE)][int((mousey + SIZE/2 - offsety)/SIZE)].letter == ' ':
                        self.array[int((mousex + SIZE/2 - offsetx) /
                                       SIZE)][int((mousey + SIZE/2 - offsety)/SIZE)].letter = self.grabbed
                        self.grabbed = ' '
                    elif self.array[int((mousex + SIZE/2 - offsetx)/SIZE)][int((mousey + SIZE/2 - offsety)/SIZE)].letter != '_':
                        temp = self.grabbed
                        self.grabbed = self.array[int((mousex + SIZE/2 - offsetx) /
                                                      SIZE)][int((mousey + SIZE/2 - offsety)/SIZE)].getLetter()
                        self.array[int((mousex + SIZE/2 - offsetx) /
                                       SIZE)][int((mousey + SIZE/2 - offsety)/SIZE)].letter = temp
                if myevent.type == MOUSEMOTION and self.grabbed != ' ':
                    self.mousex = myevent.pos[0] - framehor
                    self.mousey = myevent.pos[1] - framever
                if myevent.type == MOUSEBUTTONUP:
                    self.waitmouse = 0
                if myevent.type == KEYDOWN:
                    self.invalid = []
                    if myevent.key == K_SPACE:
                        # PEEL!
                        # First check that the board is valid
                        if self.checkwords() == True:
                            self.peelletter()
                            if self.complete == True:
                                break
                    if myevent.key == K_BACKSPACE:
                        self.grabbed = ' '
                    if myevent.key == K_r:
                        self.freshletters(21)
                        self.redos += 1
                    if myevent.key == K_LEFT:
                        temp = self.array[0]
                        for ii in range(COLS - 1):
                            self.array[ii] = self.array[ii + 1]
                        self.array[COLS - 1] = temp
                    if myevent.key == K_RIGHT:
                        temp = self.array[COLS - 1]
                        for ii in range(COLS - 1):
                            self.array[COLS - ii -
                                       1] = self.array[COLS - ii - 2]
                        self.array[0] = temp
                    if myevent.key == K_UP:
                        temp = [0]*COLS
                        for ii in range(COLS):
                            temp[ii] = self.array[ii][0]
                        for ii in range(COLS):
                            for jj in range(ROWS - 1):
                                self.array[ii][jj] = self.array[ii][jj+1]
                        for ii in range(COLS):
                            self.array[ii][ROWS-1] = temp[ii]
                    if myevent.key == K_DOWN:
                        temp = [0]*COLS
                        for ii in range(COLS):
                            temp[ii] = self.array[ii][ROWS-1]
                        for ii in range(COLS):
                            for jj in range(ROWS - 1):
                                self.array[ii][ROWS - 1 -
                                               jj] = self.array[ii][ROWS - 2 - jj]
                        for ii in range(COLS):
                            self.array[ii][0] = temp[ii]
                    if myevent.key == K_q:
                        # quit the game
                        print("Player has quit the game.")
                        quit()
                    if myevent.key == K_p:
                        # test: reset
                        self.reset()
                    if myevent.key == K_b:
                        # test: resetBoard
                        self.resetBoard()
                    if myevent.key == K_t:
                        # test: getTiles()
                        self.getTiles()
            except IndexError:
                continue

        display.flip()

    # ---- AI functions -----
    # playAction()
    # Plays the given action on the game board
    # Returns reward, complete, # of peels, score
    def playAction(self, action):
        for myevent in event.get():
            if event.type == QUIT:
                quit()
        reward = 0
        (placed, notPlaced) = self.countPlacedTiles()
        # parse action into correct move
        if action == 0:
            # TODO place tiles
            do = 0
        elif action == 1:  # peel a letter
            if self.checkwords() == True:
                # reward when entire board is complete and valid
                self.peelletter()
                reward += 10
            else:
                reward -= 10
        elif action == 2:  # reshuffle board
            self.resetBoard()
            reward -= 3
            if self.numBoardShuffles > 5:  # max 5 reshuffles, after 5th, reset game
                reward -= 10
                print(
                    'Maximum of 5 reshuffles per game exceeded. Restarting game now...')
                sleep(0.15)
                self.reset()
        elif action == 3:  # reset entire game
            reward -= 10
            self.reset()
            return reward, self.complete, self.peels

        # update GUI
        self.drawgameboard()
        display.flip()
        return reward, self.complete, self.peels


if __name__ == '__main__':
    game = Game()

    # main game loop
    while game.done == False:
        if game.complete:
            game.drawendscreen()
            continue

        game.play()

    quit()
