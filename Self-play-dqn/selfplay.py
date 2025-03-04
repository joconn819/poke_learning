"""
Run prior to NB:

cd pokemon-showdown
cp config/config-example.js config/config.js
node pokemon-showdown start --no-security

"""

import torch
import asyncio
from tqdm import tqdm
import matplotlib.pyplot as plt

from poke_env import RandomPlayer
from poke_env.player import Gen8EnvSinglePlayer
from policies import DQN

from selfplayagents import SelfPlayAgent, MaxDamagePlayer

# === Define team ===
team_test = """
Machoke @ Heavy-Duty Boots
Ability: Guts
EVs: 252 HP / 252 Def / 4 SpD
Relaxed Nature
- Brick Break
- Payback
- Rock Slide
- Close Combat

Whiscash @ Leftovers
Ability: Oblivious
EVs: 252 HP / 252 Def / 4 SpD
Relaxed Nature
- Earthquake
- Waterfall
- Ice Beam
- Dragon Dance

Torkoal @ Leftovers
Ability: White Smoke
EVs: 252 HP / 252 Def / 4 SpD
Relaxed Nature
- Flamethrower
- Earth Power
- Rapid Spin
- Stealth Rock
"""

# === Instantiate DQN models ===
state_size = 12
action_size = 6     # [0,4) for moves [4, 6) for switches in 3v3
model_1 = DQN(state_size=state_size, action_size=action_size)
model_2 = DQN(state_size=state_size, action_size=action_size)
shared_model = DQN(state_size=state_size, action_size=action_size)

# === Create agents ===
agent_1 = SelfPlayAgent(model_1, battle_format="gen8ou", team=team_test)
agent_2 = SelfPlayAgent(model_2, battle_format="gen8ou", team=team_test)

# === Training loop ===
num_episodes = 10000
win_rates_agent_1 = []
win_rates_agent_2 = []

async def self_play_training():
    n_won_agent_1 = 0
    n_won_agent_2 = 0

    for episode in tqdm(range(1, num_episodes + 1)):
        await agent_1.battle_against(agent_2, n_battles=1)

        # Update win counters
        if agent_1.n_won_battles > agent_2.n_won_battles:
            n_won_agent_1 += 1
        else:
            n_won_agent_2 += 1

        # Finalize rewards and store transitions
        for battle in agent_1.battles.values():
            agent_1.end_battle(battle)
        for battle in agent_2.battles.values():
            agent_2.end_battle(battle)

        # Train both agents
        agent_1.train(batch_size=32)
        agent_2.train(batch_size=32)

        # Track win rates
        win_rates_agent_1.append(n_won_agent_1 / episode)
        win_rates_agent_2.append(n_won_agent_2 / episode)

        # Reset battles for next round
        agent_1.reset_battles()
        agent_2.reset_battles()

    # # Plot win rates
    # plt.plot(win_rates_agent_1, label="Agent 1 Win Rate")
    # plt.plot(win_rates_agent_2, label="Agent 2 Win Rate")
    # plt.xlabel("Episode")
    # plt.ylabel("Win Rate")
    # plt.title("Self-Play Win Rates Over Time")
    # plt.legend()
    # plt.show()

# === Run the training ===
if __name__ == "__main__":
    asyncio.run(self_play_training())
