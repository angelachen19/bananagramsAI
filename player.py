from game import Game
import numpy as np
from collections import deque
import random
import torch
from model import DQN, Trainer
import helpers
import tile as tile

# Referenced https://www.youtube.com/watch?v=L8ypSXwyBds&t=3607s&ab_channel=freeCodeCamp.org tutorial

MAX_MEM = 100_000
BATCH_SIZE = 1000
LR = 0.001


class Player:

    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.numGames = 0
        self.redos = 0
        self.peels = 0
        self.failures = 0
        self.successes = 0
        self.gameTime = 0
        # memory is a list of tuples
        self.memory = deque(maxlen=MAX_MEM)
        # discount factor (value of future reward compared to current reward)
        self.gamma = gamma
        self.alpha = alpha  # learning rate
        self.epsilon = epsilon  # exploration rate
        self.model = DQN()
        self.trainer = Trainer(self.model, lr=LR, gamma=self.gamma)

        # possible actions and their associated meaning
        self.actions = [0, 1, 2, 3]
        self.actionsDict = {
            0: 'place_tiles',
            1: 'peel',
            2: 'reset_board',
            3: 'reset_game'
        }

    # State is the state of the board represented as an array of Tile objects
    def getState(self, game):
        return game.array

    def remember(self, state, action, reward, nextState, done):
        self.memory.append((state, action, reward, nextState, done))

    def trainLongMem(self):
        if len(self.memory) > BATCH_SIZE:
            subSample = random.sample(self.memory, BATCH_SIZE)
        else:
            subSample = self.memory

        states, actions, rewards, nextStates, dones = zip(*subSample)
        self.trainer.trainStep(states, actions, rewards, nextStates, dones)

    def trainShortMem(self, state, action, reward, nextState, done):
        self.trainer.trainStep(state, action, reward, nextState, done)

    def action(self, state):
        # exploration (random moves)
        self.epsilon = 80 - self.numGames
        if random.randint(0, 200) < self.epsilon:
            move = random.choice(self.actions)
        else:
            initState = torch.tensor(state, dtype=torch.float)
            prediction = self.model(initState)
            move = torch.argmax(prediction).item()

        return move


def stateToTensor(game, state):
    tensor = [[0]*game.ROWS for x in range(game.COLS)]
    for ii in range(game.COLS):
        for jj in range(game.ROWS):
            tensor[ii][jj] = ord(state[ii][jj].getLetter())
    return tensor

# def tensorToState(tensor):
#     self.array = [[tile.Tile(' ')]*self.ROWS for x in range(self.COLS)]


def train():
    agent = Player()
    game = Game()
    plot_shuffles = []
    numSuccesses = 0
    numResets = 0
    plot_times = []
    loss = 0.0
    record = 0
    while True:
        oldState = stateToTensor(game, agent.getState(game))

        # get action
        move = agent.action(oldState)

        # perform move and get new state

        reward, done, shuffles, time = game.playAction(move)
        newState = stateToTensor(game, agent.getState(game))

        # train short mem
        agent.trainShortMem(oldState, move, reward, newState, done)

        # remember
        agent.remember(oldState, move, reward, newState, done)

        if done:
            # train long memory and plot
            numResets = game.resets

            game.reset()
            agent.numGames += 1
            agent.trainLongMem()

            if shuffles < record:
                record = shuffles
                agent.model.save()

            print('Game', agent.numGames, '# of Tile Shuffles',
                  shuffles, 'Time Completed', time)

            plot_shuffles.append(shuffles)
            plot_times.append(time)
            helpers.plot_resets(plot_shuffles)
            helpers.plot_gametime(plot_times)

            completion = numSuccesses/agent.numGames
            print('Completion Rate for {} is {}%'.format(
                agent.numGames, completion))


if __name__ == '__main__':
    train()
