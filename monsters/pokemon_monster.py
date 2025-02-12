from .pokemon_data import Stats, Natures
import pypokedex
import random

class Pokemon():
    def __init__(self, name = "", gender = None, held_item = None, ability = None, nature = None, evs = [0] * 6, ivs = [31] * 6, moves = [], tera_type = None):
        self.set_name(name)
        self.set_gender(gender)
        self.set_held_item(held_item)
        self.set_ability(ability)
        self.set_nature(nature)
        self.set_evs(evs)
        self.set_ivs(ivs)
        self.tera_type = tera_type
        self.set_moves(moves)

    def set_from_string(self, poke_string: str):
        lines = poke_string.split("\n")

        if ("(" in lines[0]):
            self.set_gender(lines[0].split("(")[1].split(")")[0])
            self.set_name(lines[0].split("(")[0].strip())
        else:
            self.set_name(lines[0].split("@")[0].strip())
        self.set_held_item(lines[0].split("@")[1].strip())

        moves = []

        for line in lines[1:]:
            if ("Ability" in line):
                self.set_ability(line.split(":")[1].strip())
            elif ("Tera Type" in line):
                self.set_tera_type(line.split(":")[1].strip())
            elif ("EVs" in line):
                evs = [0] * 6
                ev_line = line.split(":")[1].split("/")
                for ev in ev_line:
                    if ("HP" in ev):
                        evs[0] = int(ev.strip().split(" ")[0])
                    elif ("Atk" in ev):
                        evs[1] = int(ev.strip().split(" ")[0])
                    elif ("Def" in ev):
                        evs[2] = int(ev.strip().split(" ")[0])
                    elif ("SpA" in ev):
                        evs[3] = int(ev.strip().split(" ")[0])
                    elif ("SpD" in ev):
                        evs[4] = int(ev.strip().split(" ")[0])
                    elif ("Spe" in ev):
                        evs[5] = int(ev.strip().split(" ")[0])

                self.set_evs(evs)
            elif ("Nature" in line):
                self.set_nature(Natures(line.split("Nature")[0].strip()))

            elif ("IVs" in line):
                ivs = [31] * 6
                iv_line = line.split(":")[1].strip().split("/")
                for iv in iv_line:
                    if ("HP" in iv):
                        ivs[0] = int(iv.strip().split(" ")[0])
                    elif ("Atk" in iv):
                        ivs[1] = int(iv.strip().split(" ")[0])
                    elif ("Def" in iv):
                        ivs[2] = int(iv.strip().split(" ")[0])
                    elif ("SpA" in iv):
                        ivs[3] = int(iv.strip().split(" ")[0])
                    elif ("SpD" in iv):
                        ivs[4] = int(iv.strip().split(" ")[0])
                    elif ("Spe" in iv):
                        ivs[5] = int(iv.strip().split(" ")[0])
                self.set_ivs(ivs)

            elif (line.startswith("-")):
                moves.append(line.split("-")[1].strip())

        self.set_moves(moves)


    def set_name(self, name: str):
        self.name = name.lower()

    def set_gender(self, gender: str):
        if gender is None:
            self.gender = None
        elif (gender.lower() == "m" or gender.lower() == "male"):
            self.gender = "M"
        elif (gender.lower() == "f" or gender.lower() == "female"):
            self.gender = "F"
        else:
            self.gender = None

    def set_held_item(self, held_item: str):
        if held_item is None:
            self.held_item = None
        else:
            self.held_item = held_item.lower()

    def set_ability(self, ability: str):
        if ability is None:
            self.ability = None
        else:
            self.ability = ability.lower()

    def set_nature(self, nature):
        self.nature = nature

    def set_evs(self, evs: list):
        self.evs = evs

    def set_ivs(self, ivs: list):
        self.ivs = ivs

    def set_tera_type(self, tera_type: str):
        self.tera_type = tera_type

    def set_moves(self, moves: list):
        self.moves = [moves.lower() for moves in moves]

    def build_string(self) -> str:
        poke_string = self.name[:10]
        poke_string += " (" + self.name + ")"
        
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
    
    def build_randomized_moveorder_string(self) -> str:
        poke_string = self.name[:10]
        poke_string += " (" + self.name + ")"
        
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

        shuffled_moves = self.moves.copy()
        random.shuffle(shuffled_moves)
        for move in shuffled_moves:
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
        return True
    
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

