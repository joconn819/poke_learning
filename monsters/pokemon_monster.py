from .pokemon_data import Stats, Natures
import pypokedex

class Pokemon():
    def __init__(self, name = "", gender = None, held_item = None, ability = None, nature = None, evs = [0] * 6, ivs = [31] * 6, moves = [None] * 4):
        self.name = name.lower()
        self.gender = gender
        self.held_item = held_item.lower()
        self.ability = ability.lower()
        self.nature = nature
        self.evs = evs
        self.ivs = ivs
        self.moves = [move.lower() for move in moves]

    def set_name(self, name: str):
        self.name = name

    def set_gender(self, gender: str):
        self.gender = gender

    def set_held_item(self, held_item: str):
        self.held_item = held_item

    def set_ability(self, ability: str):
        self.ability = ability

    def set_nature(self, nature):
        self.nature = nature

    def set_evs(self, evs: list):
        self.evs = evs

    def set_ivs(self, ivs: list):
        self.ivs = ivs

    def set_moves(self, moves: list):
        self.moves = moves

    def build_string(self) -> str:
        poke_string = self.name
        
        if self.gender is not None:
            poke_string += " (" + self.gender + ")"
        
        if self.held_item is not None:
            poke_string += " @ " + self.held_item

        poke_string += "\n"

        poke_string += "Ability: " + self.ability + "\n" 

        poke_string += "EVs: "
        first_ev = True
        for i in range(len(self.evs)):
            if self.evs[i] != 0:
                if first_ev:
                    poke_string += str(self.evs[i]) + " " + Stats[i]
                    first_ev = False
                else:
                    poke_string += " / " + str(self.evs[i]) + " " + Stats[i]
        poke_string += "\n"

        poke_string += self.nature.value + " Nature\n"
        
        if not(all(iv == 31 for iv in self.ivs)):
            poke_string += "IVs: "
            first_iv = True
            for i in range(len(self.ivs)):
                if self.ivs[i] != 31:
                    if first_iv:
                        poke_string += str(self.ivs[i]) + " " + Stats[i]
                        first_iv = False
                    else:
                        poke_string += " / " + str(self.ivs[i]) + " " + Stats[i]
            poke_string += "\n"

        for move in self.moves:
            poke_string += "- " + move + "\n"
 
        return poke_string[:-1]
    
    def check_valid_pokemon(self) -> bool:
        valid_name = self.check_valid_pokemon_name()
        if not valid_name:
            print("Invalid Pokemon name: " + self.name)
            return False
        pokedex_pokemon = pypokedex.get(name = self.name)

        if not self.check_valid_ability(pokedex_pokemon):
            print("Invalid ability: " + self.ability)
            return False
        
        if not self.check_valid_moves(pokedex_pokemon):
            print("Invalid moves: " + str(self.moves))
            return False

        return True

    def check_valid_pokemon_name(self) -> bool:
        try:
            pokedex = pypokedex.get(name = self.name)
        except pypokedex.PyPokedexHTTPError as e:
            return False
        except Exception as e:
            raise e
        return True
    
    def check_valid_ability(self, pokedex_pokemon) -> bool:
        for ability in pokedex_pokemon.abilities:
            if ability.name == self.ability:
                return True
        return False
    
    def check_valid_moves(self, pokedex_pokemon) -> bool:
        for move in self.moves:
            formatted_move = move.replace(" ", "-")
            move_found = False
            for pokedex_move in pokedex_pokemon.moves['scarlet-violet']:
                if pokedex_move.name == formatted_move:
                    move_found = True
                    break
            if not move_found:
                print("Move not found: " + move)
                return False
        return True

