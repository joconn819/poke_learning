import asyncio
from poke_env.player import RandomPlayer
from poke_env.player.battle_order import BattleOrder, ForfeitBattleOrder
from tests import test_teams as teams
from state_embedding import WeatherTracker, FieldTracker

team_test = """
Mew @ Light Clay
Ability: Synchronize
EVs: 252 HP / 252 Def / 4 SpD
Relaxed Nature
- Reflect
- Stealth Rock
- Spikes
- Rain Dance
"""

opponent_test = """
Machoke @ Leftovers
Ability: Guts
EVs: 252 HP / 252 Def / 4 SpD
Relaxed Nature
- Leer
- Bulk Up
- Focus Energy
"""

class BattleEffectTestPlayer(RandomPlayer):
    def __init__(self, weather_model, field_model, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.weather = weather_model
        self.field = field_model

    def choose_move(self, battle):
        print_len = 10
        self.weather.update_weather(battle)
        self.field.update_field(battle)
        if battle.turn < print_len:
            # Print the battle object for debugging
            print("\nBATTLE STATE:")
            print(f"Turn: {battle.turn}")
            # print(f"Weather: {battle.weather}")
            print(f"Our Entry Hazards: {battle.side_conditions}")
            print(f"Opponent Entry Hazards: {battle.opponent_side_conditions}")
            print(f"Field Effects: {battle.fields}")
            # print(f"Active Pokémon: {battle.active_pokemon.species}")
            # print(f"Opponent Pokémon: {battle.opponent_active_pokemon.species}")
            # print(f"Active Pokémon Boosts: {battle.active_pokemon.boosts}")
            # print(f"Opponent Pokémon Boosts: {battle.opponent_active_pokemon.boosts}")

            # weather_vec = self.weather.get_state_vector()
            # print(f"State weather vector: {weather_vec}")
            field_vec = self.field.get_state_vector()
            print(f"State field vector: {field_vec}")
            print(f"Light screen turns active: {self.field.light_screen}")

        if battle.turn < print_len:
            # Choose a move normally
            return super().choose_move(battle)
        else:
            print(f"Forfeiting on Turn {battle.turn}")

            return ForfeitBattleOrder()

async def run_battle_test():
    player = BattleEffectTestPlayer(battle_format="gen8ou", team=teams.trick_room_test,
                                    weather_model=WeatherTracker(), field_model=FieldTracker())
    opponent = RandomPlayer(battle_format="gen8ou", team=teams.electric_terrain_test)

    await player.battle_against(opponent, n_battles=1)

asyncio.run(run_battle_test())


"""
BATTLE STATE:
Turn: 3
Weather: {<Weather.RAINDANCE: 6>: 2}
Opponent Entry Hazards: {<SideCondition.STEALTH_ROCK: 19>: 1}
Our Entry Hazards: {<SideCondition.SPIKES: 18>: 1, <SideCondition.REFLECT: 16>: 2}
Field Effects: {}
Active Pokémon: mew
Opponent Pokémon: mew
Active Pokémon Boosts: {'accuracy': 0, 'atk': 0, 'def': 0, 'evasion': 0, 'spa': 0, 'spd': 0, 'spe': 0}
Opponent Pokémon Boosts: {'accuracy': 0, 'atk': 0, 'def': 0, 'evasion': 0, 'spa': 0, 'spd': 0, 'spe': 0}

battle.side_conditions
{<SideCondition.SPIKES: 18>: 1, <SideCondition.REFLECT: 16>: 2}
type(battle.side_conditions)
<class 'dict'>
from poke_env.data import GenData
import numpy as np

# Load Gen 8 data
gen_data = GenData.from_gen(8)
p=battle.active_pokemon
p.name
'Mew'
p.name.lower()
'mew'
q=gen_data.pokedex[p.name.lower()]
q
{'abilities': {'0': 'Synchronize'}, 'baseStats': {'atk': 100, 'def': 100, 'hp': 100, 'spa': 100, 'spd': 100, 'spe': 100}, 'color': 'Pink', 'eggGroups': ['Undiscovered'], 'gender': 'N', 'heightm': 0.4, 'name': 'Mew', 'num': 151, 'tags': ['Mythical'], 'types': ['Psychic'], 'weightkg': 4, 'baseSpecies': 'mew'}
"""