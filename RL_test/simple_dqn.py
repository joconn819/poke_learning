import torch
import torch.nn as nn

# Very basic agent
# state_size and action_size are fixed for early testing

class DQN(nn.Module):
    def __init__(self, state_size = 11, action_size = 4):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(state_size, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, action_size)

    def forward(self, state):
        x = torch.relu(self.fc1(state))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)
