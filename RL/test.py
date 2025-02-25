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

def print_pokemon_attributes(pokemon):
    """
    Can return all attributes and values of pokemon
    does not know full stats of opponent pokemon
    pokedex attributes such as abilities, types, etc are known
    """
    for att in dir(pokemon):
        print (att, getattr(pokemon,att))

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

asyncio.run(test_ohko_battle(team_mew, team_1v3test, 1))
