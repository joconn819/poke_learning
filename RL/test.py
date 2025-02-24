from battle_utils import get_battle_info
from poke_env import RandomPlayer

team_mew = """
Mew @ Expert Belt
Ability: Synchronize
EVs: 252 SpA / 4 SpD / 252 Spe
Adamant Nature
- Psychic
- Energy Ball
- Surf

Machoke @ Heavy-Duty Boots
Ability: Guts
EVs: 252 HP / 252 Def / 4 SpD
Relaxed Nature
- Leer
- Bulk Up
- Focus Energy
"""
team_1v3test = """
Machoke @ Heavy-Duty Boots
Ability: Guts
EVs: 252 HP / 252 Def / 4 SpD
Relaxed Nature
- Leer
- Bulk Up
- Focus Energy

Whiscash @ Heavy-Duty Boots
Ability: Oblivious
EVs: 252 HP / 252 Def / 4 SpD
Relaxed Nature
- Rain Dance
- Dragon Dance
- Tickle

Torkoal @ Heavy-Duty Boots
Ability: White Smoke
EVs: 252 HP / 252 Def / 4 SpD
Relaxed Nature
- Curse
- Iron Defense
"""

import numpy as np
import asyncio


NUM_HP_BINS = 4

class TestPlayer(RandomPlayer):
    def choose_move(self, battle):
        print_teams(battle)
        if battle.turn == 1:
            print("get_battle_info\n")
            state = get_battle_info(battle)
            print("state\n")
            print(state)

        return super().choose_move(battle)  # Act as a random player

def print_teams(battle):
    print("Your Team:")
    for key, value in battle.team.items():  # `items()` gives both key and value
        print(f"{key}: {value}")

    # for mon_name, mon in battle.team.items():
    #     print(f"- {mon_name}: HP {mon.current_hp_fraction:.2f}, Status: {mon.status}")

    # Print all opponent Pokémon (only those seen so far)
    print("Opponent Team (Known Pokémon):")
    for key, value in battle.opponent_team.items():
        print(f"{key}: {value}")

def print_pokemon_attributes(pokemon):
    """
    Can return all attributes and values of pokemon
    does not know full stats of opponent pokemon
    pokedex attributes such as abilities, types, etc are known
    """
    for att in dir(pokemon):
        print (att, getattr(pokemon,att))


async def test_player_battle(team_1, team_2, n_battles):
    p3 = TestPlayer(battle_format="gen8ou", team = team_1)
    p4 = RandomPlayer(battle_format="gen8ou", team = team_2)

    await p3.battle_against(p4, n_battles=n_battles)

    for battle_tag, battle in p3.battles.items():
        won_txt = "lost"
        if battle.won:
            won_txt = "won"
        print("player 3 played battle: ", battle_tag, " and ", won_txt)

asyncio.run(test_player_battle(team_mew, team_1v3test, 1))