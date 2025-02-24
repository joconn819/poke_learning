from monsters.premade_teams import get_team_1, get_team_2
from team_builders.random_order_team import RandomOrderTeam
from poke_env.player import Player
import torch
from collections import deque
import numpy as np
import random
import torch.nn.functional as F
NUM_HP_BINS = 4

from poke_env.player import RandomPlayer

class NoSwitchRandomPlayer(RandomPlayer):
    def choose_move(self, battle):
        # If the Pokémon can attack, force it to use a move
        if battle.available_moves:
            return self.create_order(random.choice(battle.available_moves))
        
        # Otherwise, switch (only if no valid moves are left)
        return self.choose_random_move(battle)