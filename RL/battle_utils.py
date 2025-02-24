import numpy as np

"""

"""

import numpy as np

def get_battle_info(battle):
    """Extracts battle information into a structured state vector."""
    if battle.turn == 1:
        state = []

        # 🏆 Entire Team's HP (Both Sides)
        team_hp = [mon.current_hp_fraction if mon else 0 for mon in battle.team.values()]
        print(f"team hp: {team_hp}")
        opponent_hp = [mon.current_hp_fraction if mon else 0 for mon in battle.opponent_team.values()]
        print(f"opponent hp: {opponent_hp}")
        state.extend(team_hp + opponent_hp)

        # 🏆 One-Hot Encoding of Active Pokémon
        active_team = [1 if mon == battle.active_pokemon else 0 for mon in battle.team.values()]
        print(f"active team: {active_team}")
        active_opponent = [1 if mon == battle.opponent_active_pokemon else 0 for mon in battle.opponent_team.values()]
        print(f"active opponent: {active_opponent}")
        state.extend(active_team + active_opponent)

        # 🏆 Type Effectiveness Against Current Opponent
        move_effectiveness = [battle.opponent_active_pokemon.damage_multiplier(move) 
                            if battle.opponent_active_pokemon else 1.0 for move in battle.available_moves]
        print(f"move effectiveness: {move_effectiveness}")
        state.extend(move_effectiveness)

        # 🏆 Move Base Power (For Available Moves)
        move_base_power = [move.base_power / 100 if move else -1 for move in battle.available_moves]
        print(f"move base power: {move_base_power}")
        state.extend(move_base_power)

        return np.array(state, dtype=np.float32)
    else: return None