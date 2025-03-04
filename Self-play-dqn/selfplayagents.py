from poke_env.player import Player
from poke_env.player import Gen8EnvSinglePlayer
import torch
from collections import deque
import numpy as np
import random
import torch.nn.functional as F

class SelfPlayAgent(Player):
    def __init__(self, model, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.NUM_HP_BINS = 5
        self.epsilon = 0.75
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.997
        self.model = model
        self.memory = deque(maxlen=10000)
        self.gamma = 0.9    # not in use yet
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=0.001)
        self.trajectory = []  # Stores (s, a) during battle
        self.prev_state = None
        self.prev_action = None

    def choose_move(self, battle):
        state = self.get_state(battle)
        state_tensor = torch.tensor(state, dtype=torch.float32).unsqueeze(0)

        # simple epsilon-greedy exploration, no idea if this is appropriate
        if random.random() < self.epsilon:
            with torch.no_grad():
                q_values = self.model(state_tensor)

            action_idx = torch.argmax(q_values).item()
        else:
            ### Seriously ugly hack
            action_idx = random.randrange(len(battle.available_moves+battle.available_switches))

        # Handle our active mon faintings
        if battle.active_pokemon.fainted or not battle.available_moves:
            if battle.available_switches:
                chosen_switch = random.choice(battle.available_switches)
                # store the forced switch as an action
                # currently will cause break since it is out of bounds, should just be in state maybe
                #self.prev_action = -1
                return self.create_order(chosen_switch)

        # If out of remaining mons, do not allow switches
        if len(battle.available_switches) == 0:
            if action_idx > 3:
                action_idx = np.mod(action_idx, 4)

        # Handle move actions
        if action_idx < 4:
            if len(battle.available_moves) > action_idx:
                chosen_action = battle.available_moves[action_idx]
            else:
                chosen_action = random.choice(battle.available_moves)
            order = self.create_order(chosen_action)

        # Handle switch actions
        else:
            switch_index = action_idx - 4
            if len(battle.available_switches) > switch_index:
                chosen_action = battle.available_switches[switch_index]
            else:
                chosen_action = random.choice(battle.available_switches)
            order = self.create_order(chosen_action)

        # --- Record (s, a, s') transitions ---
        if self.prev_state is not None:
            self.trajectory.append((self.prev_state, self.prev_action, state))

        # Update for next turn
        self.prev_state = state
        self.prev_action = action_idx
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)

        return order


    def get_state(self, battle):
        ### Convert battle info to state vector
        # State info is very simple atm
        # move bp, type effectiveness, and hp values, number fainted pokemon
        your_pokemon = battle.active_pokemon
        opponent_pokemon = battle.opponent_active_pokemon

        your_hp = int(self.NUM_HP_BINS * battle.active_pokemon.current_hp_fraction) / self.NUM_HP_BINS if your_pokemon else -1
        opponent_hp = int(self.NUM_HP_BINS * battle.opponent_active_pokemon.current_hp_fraction) / self.NUM_HP_BINS if opponent_pokemon else -1
        num_fainted = int(sum(1 for mon in battle.team.values() if mon.fainted))
        opp_num_fainted = int(sum(1 for mon in battle.opponent_team.values() if mon.fainted))

        moves_base_power = -np.ones(4)
        moves_dmg_multiplier = np.ones(4)

        if battle.opponent_active_pokemon:
            for i, move in enumerate(battle.available_moves):
                moves_base_power[i] = move.base_power / 100
                if move.type:
                    moves_dmg_multiplier[i] = battle.opponent_active_pokemon.damage_multiplier(move)

        return np.concatenate([moves_base_power, moves_dmg_multiplier, [your_hp, opponent_hp, num_fainted, opp_num_fainted]])

    def end_battle(self, battle):
        final_reward = 1 if battle.won else -1
        for (s, a, s_next) in self.trajectory:
            self.memory.append((s, a, final_reward, s_next))

        self.trajectory.clear()
        self.prev_state = None
        self.prev_action = None

    def train(self, batch_size = 32):
        if len(self.memory) < batch_size:
            return
        batch = random.sample(self.memory, batch_size)
        states, actions, rewards, next_states = zip(*batch)

        states = torch.tensor(np.array(states), dtype=torch.float32)
        actions = torch.tensor(np.array(actions), dtype=torch.int64).unsqueeze(1)
        rewards = torch.tensor(np.array(rewards), dtype=torch.float32).unsqueeze(1)
        next_states = torch.tensor(np.array(next_states), dtype=torch.float32)

        q_values = self.model(states).gather(1, actions)
        with torch.no_grad():
            next_q_values = self.model(next_states).max(1)[0].unsqueeze(1)

        target_q = rewards + self.gamma * next_q_values

        loss = F.mse_loss(q_values, target_q)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()


### Testing partner
from poke_env.player import Player

# From poke-env docs

class MaxDamagePlayer(Player):
    def choose_move(self, battle):
        # Chooses a move with the highest base power when possible
        if battle.available_moves:
            # Iterating over available moves to find the one with the highest base power
            best_move = max(battle.available_moves, key=lambda move: move.base_power)
            # Creating an order for the selected move
            return self.create_order(best_move)
        else:
            # If no attacking move is available, perform a random switch
            # This involves choosing a random move, which could be a switch or another available action
            return self.choose_random_move(battle)