from monsters.premade_teams import get_team_1, get_team_2
from team_builders.random_order_team import RandomOrderTeam
from poke_env.player import Player
import torch
from collections import deque
import numpy as np
import random
import torch.nn.functional as F
NUM_HP_BINS = 4

# Testing simple RL player
# add dqn model to player class

class SuperEffectiveRLPlayer(Player):
    def __init__(self, model, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prev_opponent_hp = 1.0 # cludge
        self.last_move_used = None  # cludge
        self.model = model
        self.memory = deque(maxlen=10000)  # Experience replay buffer
        self.gamma = 0.5
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=0.01)
        
    def choose_move(self, battle):
        available_moves = battle.available_moves

        if available_moves:
            # Get the best move based on Q-values
            state = self.get_state_vector(battle)
            state_tensor = torch.tensor(state, dtype=torch.float32).unsqueeze(0)
            with torch.no_grad():
                q_values = self.model(state_tensor)
            
            best_move_idx = torch.argmax(q_values).item()
            if best_move_idx < len(available_moves):
                chosen_move = available_moves[best_move_idx]
                self.last_move_used = chosen_move  # Store the move
                return self.create_order(chosen_move)
            else: 
                return self.choose_random_move(battle) # cludge
        
        return self.choose_random_move(battle)
        
    def get_state_vector(self, battle):
        ### Convert battle info to state vector
        # State info is very simple atm
        # move bp, type effectiveness, and hp values
        your_pokemon = battle.active_pokemon
        opponent_pokemon = battle.opponent_active_pokemon

        your_hp = int(NUM_HP_BINS * battle.active_pokemon.current_hp_fraction) / NUM_HP_BINS if your_pokemon else -1
        opponent_hp = int(NUM_HP_BINS * battle.opponent_active_pokemon.current_hp_fraction) / NUM_HP_BINS if opponent_pokemon else -1

        moves_base_power = -np.ones(4)
        moves_dmg_multiplier = np.ones(4)

        if battle.opponent_active_pokemon:
            for i, move in enumerate(battle.available_moves):
                moves_base_power[i] = move.base_power / 100
                if move.type:
                    moves_dmg_multiplier[i] = battle.opponent_active_pokemon.damage_multiplier(move)

        # print(f"State: {np.concatenate([moves_base_power, moves_dmg_multiplier, [your_hp, opponent_hp]])}")
        return np.concatenate([moves_base_power, moves_dmg_multiplier, [your_hp, opponent_hp]])

    def train(self, batch_size=32):
        ###Updates the DQN model using stored experience
        if len(self.memory) < batch_size:
            return  # Don't train until we have enough experiences

        batch = random.sample(self.memory, batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)

        states = torch.tensor(np.array(states), dtype=torch.float32)
        actions = torch.tensor(np.array(actions), dtype=torch.int64).unsqueeze(1)
        rewards = torch.tensor(np.array(rewards), dtype=torch.float32).unsqueeze(1)
        next_states = torch.tensor(np.array(next_states), dtype=torch.float32)
        dones = torch.tensor(np.array(dones), dtype=torch.float32).unsqueeze(1)

        # Compute current Q-values
        q_values = self.model(states).gather(1, actions)

        # Compute next Q-values using target network
        with torch.no_grad():
            next_q_values = self.model(next_states).max(1)[0].unsqueeze(1)

        target_q_values = rewards + (self.gamma * next_q_values * (1 - dones))

        # Compute loss and update model
        loss = F.mse_loss(q_values, target_q_values)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

    def compute_reward(self, battle):
        reward = 0

        if battle.opponent_active_pokemon:
            damage_dealt = self.prev_opponent_hp - battle.opponent_active_pokemon.current_hp_fraction
            reward += np.power(damage_dealt * 10, 2)

            # # Reward super-effective moves using stored last move
            # if self.last_move_used and battle.opponent_active_pokemon:
            #     move_effectiveness = battle.opponent_active_pokemon.damage_multiplier(self.last_move_used)
            #     if move_effectiveness > 1.0:
            #         reward += 35
            #     else:
            #         reward -= 25  # Penalize weak moves

        if battle.won and self.prev_opponent_hp > .75:
            reward += 100
        elif battle.won and self.prev_opponent_hp > .35:
            reward += 50

        self.prev_opponent_hp = battle.opponent_active_pokemon.current_hp_fraction if battle.opponent_active_pokemon else 1.0
        return reward

