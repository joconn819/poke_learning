import pytest
from monsters.pokemon_monster import Pokemon
from monsters.pokemon_data import Natures
from monsters.pokemon_team import PokemonTeam

from poke_env.teambuilder import Teambuilder


class RandomOrderTeam(Teambuilder):
    def __init__(self, poke_team):
        self.poke_team = poke_team

    def yield_team(self):    
        team_string = self.poke_team.get_randomized_team_string()
        self.parsed_team = self.parse_showdown_team(team_string)
        self.packed_team = self.join_team(self.parsed_team)
        return self.packed_team
