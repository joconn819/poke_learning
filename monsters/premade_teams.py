from .pokemon_monster import Pokemon
from .pokemon_team import PokemonTeam

def get_team_1():
    calyrex_ice = Pokemon()
    calyrex_ice.set_from_string("""Calyrex-Ice @ Clear Amulet \nAbility: As One (Glastrier)  \nTera Type: Fairy  \nEVs: 252 HP / 116 Atk / 4 Def / 20 SpD / 116 Spe  \nAdamant Nature  \n- Glacial Lance  \n- High Horsepower  \n- Protect  \n- Trick Room  """)
    
    landorus = Pokemon()
    landorus.set_from_string("""Landorus @ Life Orb  \nAbility: Sheer Force  \nTera Type: Water  \nEVs: 244 HP / 4 Def / 124 SpA / 4 SpD / 132 Spe  \nModest Nature  \nIVs: 0 Atk  \n- Earth Power  \n- Sludge Bomb  \n- Sandsear Storm  \n- Protect  """)
    
    amoonguss = Pokemon()
    amoonguss.set_from_string("""Amoonguss (F) @ Covert Cloak  \nAbility: Regenerator  \nLevel: 50  \nTera Type: Fairy  \nEVs: 244 HP / 156 Def / 108 SpD  \nRelaxed Nature  \nIVs: 0 Atk / 0 Spe  \n- Pollen Puff  \n- Spore  \n- Protect  \n- Rage Powder  """)
    
    urshifu = Pokemon()
    urshifu.set_from_string("""Urshifu-Rapid-Strike @ Mystic Water  \nAbility: Unseen Fist  \nTera Type: Water  \nEVs: 204 HP / 188 Atk / 20 Def / 4 SpD / 92 Spe  \nAdamant Nature  \n- Surging Strikes  \n- Taunt  \n- Close Combat  \n- Detect  """)
    
    roaring_moon = Pokemon()
    roaring_moon.set_from_string("""Roaring Moon @ Booster Energy  \nAbility: Protosynthesis  \nTera Type: Flying  \nEVs: 148 HP / 84 Atk / 116 Def / 4 SpD / 156 Spe  \nJolly Nature  \n- Knock Off  \n- Acrobatics  \n- Protect  \n- Tailwind  """)
    
    ogerpon = Pokemon()
    ogerpon.set_from_string("""Ogerpon-Hearthflame @ Hearthflame Mask  \nAbility: Mold Breaker  \nTera Type: Fire  \nEVs: 220 HP / 12 Atk / 252 Def / 4 SpD / 20 Spe  \nImpish Nature  \n- Ivy Cudgel  \n- Horn Leech  \n- Follow Me  \n- Spiky Shield """)
    
    poke_team = PokemonTeam()
    poke_team.add_pokemon(calyrex_ice)
    poke_team.add_pokemon(landorus)
    poke_team.add_pokemon(amoonguss)
    poke_team.add_pokemon(urshifu)
    poke_team.add_pokemon(roaring_moon)
    poke_team.add_pokemon(ogerpon)

    return poke_team

def get_team_2():
    miraidon = Pokemon()
    miraidon.set_from_string("""Miraidon @ Choice Specs  \nAbility: Hadron Engine  \nLevel: 50  \nTera Type: Fairy  \nEVs: 44 HP / 4 Def / 244 SpA / 12 SpD / 204 Spe  \nModest Nature  \n- Electro Drift  \n- Draco Meteor  \n- Volt Switch  \n- Dazzling Gleam""")

    whimsicott = Pokemon()
    whimsicott.set_from_string("""Whimsicott @ Covert Cloak  \nAbility: Prankster  \nLevel: 50  \nTera Type: Dark  \nEVs: 236 HP / 164 SpD / 108 Spe  \nTimid Nature  \nIVs: 0 Atk  \n- Moonblast  \n- Tailwind  \n- Light Screen  \n- Encore""")

    urshifu = Pokemon()
    urshifu.set_from_string("""Urshifu-Rapid-Strike @ Focus Sash  \nAbility: Unseen Fist  \nLevel: 50  \nTera Type: Water  \nEVs: 252 Atk / 4 SpD / 252 Spe  \nAdamant Nature  \n- Surging Strikes  \n- Close Combat  \n- Aqua Jet  \n- Protect""")

    ogerpon = Pokemon()
    ogerpon.set_from_string("""Ogerpon-Hearthflame (F) @ Hearthflame Mask  \nAbility: Mold Breaker  \nLevel: 50  \nTera Type: Fire  \nEVs: 188 HP / 76 Atk / 52 Def / 4 SpD / 188 Spe  \nAdamant Nature  \n- Ivy Cudgel  \n- Wood Hammer  \n- Follow Me  \n- Spiky Shield""")

    farigiraf = Pokemon()
    farigiraf.set_from_string("""Farigiraf @ Electric Seed  \nAbility: Armor Tail  \nLevel: 50  \nTera Type: Water  \nEVs: 204 HP / 164 Def / 4 SpA / 108 SpD / 28 Spe  \nBold Nature  \nIVs: 6 Atk  \n- Foul Play  \n- Psychic Noise  \n- Trick Room  \n- Helping Hand""")

    iron_hands = Pokemon()
    iron_hands.set_from_string("""Iron Hands @ Assault Vest  \nAbility: Quark Drive  \nLevel: 50  \nTera Type: Bug  \nEVs: 76 HP / 180 Atk / 12 Def / 236 SpD  \nBrave Nature  \nIVs: 0 Spe  \n- Drain Punch  \n- Low Kick  \n- Wild Charge  \n- Fake Out""")

    poke_team = PokemonTeam()
    poke_team.add_pokemon(miraidon)
    poke_team.add_pokemon(whimsicott)
    poke_team.add_pokemon(urshifu)
    poke_team.add_pokemon(ogerpon)
    poke_team.add_pokemon(farigiraf)
    poke_team.add_pokemon(iron_hands)

    return poke_team