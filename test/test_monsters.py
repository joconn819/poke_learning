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

def test_pokemon_from_string():
    string = """Calyrex-Ice @ Clear Amulet \nAbility: As One (Glastrier)  \nTera Type: Fairy  \nEVs: 252 HP / 116 Atk / 4 Def / 20 SpD / 116 Spe  \nAdamant Nature  \n- Glacial Lance  \n- High Horsepower  \n- Protect  \n- Trick Room  """
    
    calyrex_ice = Pokemon()
    calyrex_ice.set_from_string(string)

    assert calyrex_ice.name == "calyrex-ice"
    assert calyrex_ice.held_item == "clear amulet"
    assert calyrex_ice.ability == "as one (glastrier)"
    assert calyrex_ice.tera_type == "Fairy"
    assert calyrex_ice.evs == [252, 116, 4, 0, 20, 116]
    assert calyrex_ice.nature == Natures.ADAMANT
    assert calyrex_ice.moves == ["glacial lance", "high horsepower", "protect", "trick room"]

  