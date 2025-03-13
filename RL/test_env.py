import gymnasium as gym
import numpy as np
from poke_env.player import RandomPlayer
from poke_env.player.env_player import Gen8EnvSinglePlayer

class PokemonBattleEnv(gym.Env):
    """Gym environment wrapper for Pokémon Showdown using Poke-Env."""

    def __init__(self, battle_format="gen8randombattle"):
        super().__init__()

        # Define action and observation spaces
        self.action_space = gym.spaces.Discrete(4)  # 4 possible moves
        self.observation_space = gym.spaces.Box(low=-1, high=1, shape=(10,), dtype=np.float32)

        # Define players (self-agent and opponent)
        self.agent = GymRLPlayer(battle_format=battle_format)
        self.opponent = RandomPlayer(battle_format=battle_format)

        # Keep track of the battle
        self.battle = None

    def reset(self, seed=None, options=None):
        """Resets the environment for a new battle."""
        self.agent.reset_battles()
        self.opponent.reset_battles()

        # Run a dummy battle to set up Poke-Env
        self.agent.play_against(self.opponent, n_battles=1)

        # Fetch the initialized battle
        self.battle = self.agent.battles[-1]

        # Return initial state
        return self._get_observation(), {}

    def step(self, action):
        """Takes an action, updates the battle, and returns (obs, reward, done, info)."""
        if self.battle is None:
            raise RuntimeError("Battle has not started! Call `reset()` first.")

        # Select move based on action
        available_moves = self.battle.available_moves
        if available_moves and action < len(available_moves):
            move = available_moves[action]
            self.agent._current_battle.register_action(move)

        # Simulate battle step
        self.agent.play_against(self.opponent, n_battles=1)

        # Get updated state and reward
        obs = self._get_observation()
        reward = self.agent.compute_reward(self.battle)
        done = self.battle.finished

        return obs, reward, done, {}

    def _get_observation(self):
        """Encodes the battle state as a Gym-friendly vector."""
        if not self.battle:
            return np.zeros(10)  # Default state if battle isn't initialized

        return np.array([
            self.battle.active_pokemon.current_hp_fraction if self.battle.active_pokemon else -1,
            self.battle.opponent_active_pokemon.current_hp_fraction if self.battle.opponent_active_pokemon else -1,
            *[move.base_power / 100 if move else -1 for move in self.battle.available_moves]
        ])

    def render(self, mode="human"):
        """Prints battle state for debugging."""
        if self.battle:
            print(f"Turn: {self.battle.turn}")
            print(f"Your Pokémon: {self.battle.active_pokemon}")
            print(f"Opponent Pokémon: {self.battle.opponent_active_pokemon}")

    def close(self):
        """Clean up resources (if needed)."""
        pass


class GymRLPlayer(Gen8EnvSinglePlayer):
    """Minimal player class for Gym integration."""
    def choose_move(self, battle):
        """Selects a random move (placeholder for RL agent)."""
        return self.create_order(np.random.choice(battle.available_moves))
