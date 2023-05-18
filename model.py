import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os


class DQN(nn.Module):
    def __init__(self):
        super(DQN, self).__init__()

        self.conv1 = nn.Sequential(nn.Linear(17, 8), nn.ReLU())
        self.conv2 = nn.Sequential(nn.Linear(8, 4), nn.ReLU())
        self.conv3 = nn.Sequential(nn.Linear(4, 1))
        self._weights()

    def _weights(self):
        for m in self.modules():
            if isinstance(m, nn.Linear):
                nn.init.xavier_uniform_(m.weight)
                nn.init.constant_(m.bias, 0)

    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.conv3(x)

        return x

    def save(self, fileName='model.pth'):
        modelFolderPath = './model'
        if not os.path.exists(modelFolderPath):
            os.makedirs(modelFolderPath)
        fileName = os.path.join(modelFolderPath, fileName)
        torch.save(self.state_dict(), fileName)


class Trainer:
    def __init__(self, model, lr, gamma):
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.loss = nn.MSELoss()

    def get_loss(self):
        return self.loss

    def trainStep(self, state, action, reward, nextState, done):
        state = torch.tensor(state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)
        nextState = torch.tensor(nextState, dtype=torch.float)
        lenDone = 1
        if len(state.shape) == 1:
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done, )
            lenDone = 2

        # predicted Q values w/ current state
        prediction = self.model(state)

        target = prediction.clone()
        for i in range(lenDone):
            newQ = reward
            if not done:
               # Qnew = r + y * max(next predicted Q val)
                newQ = reward + self.gamma * \
                    torch.max(self.model(nextState))

            target[i][torch.argmax(action).item()] = newQ

        # loss function
        self.optimizer.zero_grad()
        l = self.loss(target, prediction)
        l.backward()

        self.optimizer.step()
