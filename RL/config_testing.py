### torch install
"""import torch
x = torch.rand(5, 3)
print(x)"""

### dqn config load
import json

with open("RL_test/config.json", "r") as f:
    config = json.load(f)

learning_rate = config["learning_rate"]
print(learning_rate)