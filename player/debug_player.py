from monsters.premade_teams import get_team_1, get_team_2
from team_builders.random_order_team import RandomOrderTeam
from poke_env.player import RandomPlayer

NUM_HP_BINS = 4

class DebugPlayer(RandomPlayer):
    def choose_move(self, battle):
        # Print turn number
        print(f"Turn: {battle.turn}")

        # Print available moves
        print(f"Available moves: {[move.id for move in battle.available_moves]}")

        # Check battle has started
        your_pokemon = battle.active_pokemon
        opponent_pokemon = battle.opponent_active_pokemon
 
        # Extract key battle info
        state = {
            #"turn": battle.turn,
            "your_hp": int(NUM_HP_BINS * battle.active_pokemon.current_hp_fraction) / NUM_HP_BINS if your_pokemon else None,
            "your_status": battle.active_pokemon.status if your_pokemon else None,
            "your_moves": [move.id for move in battle.available_moves] if your_pokemon else None,
            "opponent_hp": int(NUM_HP_BINS * battle.opponent_active_pokemon.current_hp_fraction) / NUM_HP_BINS if opponent_pokemon else None,
            "opponent_status": battle.opponent_active_pokemon.status if opponent_pokemon else None
        }

        # Get type effectiveness
        moves_dmg_multiplier = np.ones(4)
        if battle.opponent_active_pokemon:
            for i, move in enumerate(battle.available_moves):
                if move.type:
                    moves_dmg_multiplier[i] = battle.opponent_active_pokemon.damage_multiplier(move)

        # Print the state info
        # print(f"State: {state}")

        return super().choose_move(battle)  # Act as a random player