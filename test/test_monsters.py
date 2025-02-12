import pytest
from ..monsters.pokemon_monster import Pokemon
from ..monsters.pokemon_data import Natures
from ..monsters.pokemon_team import PokemonTeam

def test_charizard():
    charizard = Pokemon(name="charizard", gender="M", held_item="Charizardite X", ability="Blaze", nature=Natures.ADAMANT, evs=[252, 252, 0, 0, 4, 0], ivs=[31, 31, 31, 31, 31, 31], moves=["Flare Blitz", "Dragon Claw", "Heat Wave", "Earthquake"])
    
    assert charizard.name == "charizard"
    assert charizard.gender == "M"
    assert charizard.held_item == "charizardite x"
    assert charizard.ability == "blaze"
    assert charizard.nature == Natures.ADAMANT
    assert charizard.evs == [252, 252, 0, 0, 4, 0]
    assert charizard.ivs == [31, 31, 31, 31, 31, 31]
    assert charizard.moves == ["flare blitz", "dragon claw", "heat wave", "earthquake"]

    assert charizard.check_valid_pokemon()

    charizard.set_ability("Solar Power")

    assert not charizard.check_valid_pokemon()

def test_all_charizard_team():
        charizard = Pokemon(name="charizard", gender="male", held_item="Charizardite X", ability="Blaze", nature=Natures.ADAMANT, evs=[252, 252, 0, 0, 4, 0], ivs=[31, 31, 31, 31, 31, 31], moves=["Flare Blitz", "Dragon Claw", "Heat Wave", "Earthquake"])
        poke_team = PokemonTeam()
        poke_team.add_pokemon(charizard)
        poke_team.add_pokemon(charizard)
        poke_team.add_pokemon(charizard)
        poke_team.add_pokemon(charizard)
        poke_team.add_pokemon(charizard)
        poke_team.add_pokemon(charizard)

        assert poke_team.check_valid_team()
  