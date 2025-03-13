"""
Run prior to NB:

cd pokemon-showdown
cp config/config-example.js config/config.js
node pokemon-showdown start --no-security
"""

from battle_utils import get_battle_info
from poke_env import RandomPlayer
import numpy as np
import asyncio

team_mew = """
Mew @ Expert Belt
Ability: Synchronize
EVs: 252 SpA / 4 SpD / 252 Spe
Adamant Nature
- Psychic
- Energy Ball
- Surf
"""
team_whis = """
Whiscash @ Heavy-Duty Boots
Ability: Oblivious
EVs: 252 HP / 252 Def / 4 SpD
Relaxed Nature
- Rain Dance
- Dragon Dance
- Tickle
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


NUM_HP_BINS = 4

class TestPlayer(RandomPlayer):
    def choose_move(self, battle):
        # print_teams(battle)
        # print(f"team len: {len(battle.team)}\nopp team len: {len(battle.opponent_team)}")
        if battle.turn == 1:
            print("get_battle_info\n")
            print_teams(battle)
            state = get_battle_info(battle)
            print("\nSTATE")
            print(state)

            stabs = check_stab(battle.active_pokemon)
            print(f"\nactive mon stabs: {stabs}\nactive mon boosts: {battle.active_pokemon.boosts}\n")
            
        if battle.active_pokemon.fainted or not battle.available_moves:
            print(battle.turn)

        

        return super().choose_move(battle)  # Act as a random player
    
class BattleEndTestPlayer(RandomPlayer):
    def choose_move(self, battle):
        print(f"\nTurn #: {battle.turn}")

        # Check if battle is finished
        if battle.finished:
            print("Battle has ended! Observing final state...")
            print(f"Winner: {'Agent' if battle.won else 'Opponent'}")
            print(f"Final State: {battle}")
        return super().choose_move(battle)
    
    async def _handle_battle_message(self, messages):
        """Override battle message handling to detect when a battle ends."""
        await super()._handle_battle_message(messages)  # Let default processing happen

        # Loop through all messages to find the end of battle
        for message in messages:
            if "win" in message:  # "win" event is sent when a battle ends
                print("\n🔥 Battle has ended! Observing final state... 🔥")
                battle_id = message[-1]  # Get the winner name
                print(f"Winner: {battle_id}")

                # Get battle state
                for battle in self.battles.values():
                    if battle.finished:  # Check finished flag
                        print(f"Final State: {battle}")



def print_w_l_results(player):
        for battle_tag, battle in player.battles.items():
            won_txt = "lost"
            if battle.won:
                won_txt = "won"
            print("player 3 played battle: ", battle_tag, " and ", won_txt)

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

def print_battle_report(battle):
    print(f"\nBattle Tag: {battle.battle_tag}")
    print(f"Turn: {battle.turn}")
    print(f"Winner: {'You' if battle.won else 'Opponent' if battle.lost else 'Ongoing'}")
    
    print("\n--- Your Team ---")
    for mon_name, mon in battle.team.items():
        print(f"{mon_name}: {mon.species}, HP: {mon.current_hp_fraction:.2f}, Status: {mon.status}, Moves: {[move for move in mon.moves]}")

    print("\n--- Opponent's Known Pokémon ---")
    for mon_name, mon in battle.opponent_team.items():
        print(f"{mon_name}: {mon.species}, HP: {mon.current_hp_fraction:.2f}, Status: {mon.status}, Moves: {[move for move in mon.moves]}")

    print("\n--- Active Pokémon ---")
    if battle.active_pokemon:
        print(f"Your Active Pokémon: {battle.active_pokemon.species}")
    if battle.opponent_active_pokemon:
        print(f"Opponent's Active Pokémon: {battle.opponent_active_pokemon.species}")


def get_full_battle_obs(battle):
    # Get al observations in battle, huge output
    for key, val in battle.observations.items():
        print(f"Key: {key}\nValues: {val}")

def get_single_battle_obs(battle, turn):
    # Get single observation in battle, small output
    # key is just the turn number with turn 0 being the team preview
    if turn in battle.observations:
        print(battle.observations[turn])
    else:
        print("Key Error: turn not found in battle")

def get_battle_events(battle):
    for t in range(1,battle.turn+1):
        print(f"Turn {t}\n{battle.observations[t].events}")

def print_pokemon_attributes(pokemon):
    """
    Can return all attributes and values of pokemon
    does not know full stats of opponent pokemon
    pokedex attributes such as abilities, types, etc are known
    """
    for att in dir(pokemon):
        print (att, getattr(pokemon,att))

def check_stab(mon):
    """
    mon has type_1, type_2, moves is dict of {move, typing}
    return STAB
    """
    stab = [move.type in mon.types for move in mon.moves.values()]
    return stab + [False] * (4 - len(stab)) # ensure right dimension

async def test_ohko_battle(team_1, team_2, n_battles=1):
    p3 = BattleEndTestPlayer(battle_format="gen8ou", team =
                    """
                    Mew @ Choice Specs
                    Ability: Synchronize
                    EVs: 252 SpA / 252 Spe / 4 HP
                    Timid Nature
                    - Psychic
                    """)
    p4 = RandomPlayer(battle_format="gen8ou", team =
                    """
                    Machop @ Leftovers
                    Ability: No Guard
                    EVs: 4 Atk
                    Hardy Nature
                    - Leer
                    """)

    await p3.battle_against(p4, n_battles=1)
    #print_teams(battle)
    print_w_l_results(p3)

async def test_player_battle(team_1, team_2, n_battles):
    p3 = TestPlayer(battle_format="gen8ou", team = team_1)
    p4 = RandomPlayer(battle_format="gen8ou", team = team_2)

    await p3.battle_against(p4, n_battles=n_battles)
    print_w_l_results(p3)

asyncio.run(test_player_battle(team_1v3test, team_mew, 1))
