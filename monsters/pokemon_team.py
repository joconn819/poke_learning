from .pokemon_monster import Pokemon

class PokemonTeam():
    def __init__(self):
        self.team = []
        self.team_size = 6

    def add_pokemon(self, pokemon):
        if len(self.team) < self.team_size:
            self.team.append(pokemon)
        else:
            raise ValueError("Team is full!")

    def get_team_string(self) -> str:
        team_string = ""
        for pokemon in self.team:
            team_string += pokemon.build_string() + "\n"
        return team_string
    
    def check_valid_team(self) -> bool:
        for pokemon in self.team:
            if not pokemon.check_valid_pokemon():
                return False
        return True