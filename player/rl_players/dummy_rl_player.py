from monsters.premade_teams import get_team_1, get_team_2
from team_builders.random_order_team import RandomOrderTeam
from poke_env.player import Player
import torch
from collections import deque
NUM_HP_BINS = 4


class DummyRLPlayer(Player):
    def __init__(self, model, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = model  # Store DQN model
        
    def choose_move(self, battle):
        # Check battle has started and get hp's
        your_pokemon = battle.active_pokemon
        opponent_pokemon = battle.opponent_active_pokemon

        your_hp = int(NUM_HP_BINS * battle.active_pokemon.current_hp_fraction) / NUM_HP_BINS if your_pokemon else -1
        opponent_hp = int(NUM_HP_BINS * battle.opponent_active_pokemon.current_hp_fraction) / NUM_HP_BINS if opponent_pokemon else -1

        # Get available move powers
        # -1 indicates that the move does not have a base power
        # or is not available
        moves_base_power = -np.ones(4)
        moves_dmg_multiplier = np.ones(4)
        if battle.opponent_active_pokemon:
            for i, move in enumerate(battle.available_moves):
                moves_base_power[i] = (
                    move.base_power / 100
                )  # Simple rescaling to facilitate learning
                if move.type:
                    moves_dmg_multiplier[i] = battle.opponent_active_pokemon.damage_multiplier(move)

        # test if state has worked correctly
        state = np.concatenate(
            [
                moves_base_power,
                moves_dmg_multiplier,
                [your_hp, opponent_hp],
            ]
        )

        # Create state vector
        state = np.concatenate([moves_base_power, moves_dmg_multiplier, [your_hp, opponent_hp]])
        state_tensor = torch.tensor(state, dtype=torch.float32).unsqueeze(0)  # Convert to tensor

        # Get Q-values from DQN
        with torch.no_grad():
            q_values = self.model(state_tensor)

        # "Best" move is just random b/c dqn doesn't train
        best_move_idx = torch.argmax(q_values).item()
        available_moves = battle.available_moves

        # Simple check, doesn't factor pp yet
        if available_moves and best_move_idx < len(available_moves):
            return self.create_order(available_moves[best_move_idx])
        else:
            return self.choose_random_move(battle)  # Fallback if move index is invalid


    def compute_reward(self, battle) -> float:
        pass