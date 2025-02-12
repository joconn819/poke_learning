from monsters.premade_teams import get_team_1, get_team_2
from team_builders.random_order_team import RandomOrderTeam
from poke_env.player import RandomPlayer

class RandomVGCPlayer(RandomPlayer):
    def __init__(self, team):
        super().__init__(battle_format="gen9vgc2025regg", team=team)

    def teampreview(self, battle) -> str:
        return "/team 1234"