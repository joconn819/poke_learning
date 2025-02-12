import pytest
from monsters.pokemon_monster import Pokemon
from monsters.pokemon_data import Natures
from monsters.pokemon_team import PokemonTeam

from poke_env.teambuilder import Teambuilder


class AllCharizard(Teambuilder):


    def yield_team(self):
        charizard = Pokemon(name="charizard", gender="M", held_item="Assault Vest", ability="Blaze", nature=Natures.ADAMANT, evs=[252, 252, 0, 0, 4, 0], ivs=[31, 31, 31, 31, 31, 31], moves=["Flare Blitz", "Dragon Claw", "Heat Wave", "Earthquake"])
        poke_team = PokemonTeam()
        for _ in range(1):
            poke_team.add_pokemon(charizard) 

        parsed_team = self.parse_showdown_team(poke_team.get_team_string())

        packed_team = self.join_team(parsed_team)

        return packed_team
