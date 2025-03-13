from poke_env.data import GenData
from poke_env.environment.weather import Weather
from poke_env.environment.side_condition import SideCondition
from poke_env.environment.field import Field
import numpy as np

# Hardcoded vector sizes (max + 1 for inactive)
# could be json we load or find in poke-env
MAX_ROCKS_LAYERS        = 2
MAX_SPIKES_LAYERS       = 4
MAX_TOX_SPIKES_LAYERS   = 3
MAX_REFLECT_TURNS       = 8
MAX_LIGHT_SCREEN_TURNS  = 8
MAX_SAFEGUARD_TURNS     = 8
MAX_TAILWIND_TURNS      = 5

### NOTE:
### Code clean up will be necessary, consider helper functions as below once battle functionality is well understood

# could return our side and opponent side together
def get_condition_turn(battle, condition):
    return (battle.turn - battle.side_conditions.get(condition, 0)) if condition in battle.side_conditions else 0
    # return (battle.turn - battle.side_conditions.get(condition, 0)) if condition in battle.side_conditions else 0,
    #         (battle.turn - battle.opponent_side_conditions.get(condition, 0)) if condition in battle.side_conditions else 0

# Load Gen 8 data
gen_data = GenData.from_gen(8)

# Get the move dictionary
move_dict = gen_data.moves  # Contains all moves for Gen 8
NUM_MOVES = len(move_dict)  # Number of moves in Gen 8

def get_move_one_hot(move_name):
    """Returns a one-hot encoding for a move."""
    move_id = move_dict.get(move_name.lower())  # Moves are stored in lowercase
    one_hot = np.zeros(NUM_MOVES)

    if move_id:
        move_index = list(move_dict.keys()).index(move_name.lower())  # Get index
        one_hot[move_index] = 1  # Set corresponding move to 1

    return one_hot

# Track weather effects for state computation
class WeatherTracker:
    def __init__(self):
        self.current_weather = None
        self.weather_duration = 0

    def update_weather(self, battle):
        """Updates the weather state each turn."""
        if battle.weather:
            weather_type, _ = next(iter(battle.weather.items()))

            if self.current_weather != weather_type:
                self.current_weather = weather_type
                self.weather_duration = 0
            else:
                self.weather_duration += 1
        else:
            self.current_weather = None
            self.weather_duration = 0

    def get_state_vector(self):
        """Return weather state vector, sun, rain, sand, hail"""
        weather_vector = np.zeros(8 * 4 + 1)  # 4 Weather types duration and no weather

        if self.current_weather:
            if self.current_weather == Weather.SUNNYDAY:
                weather_vector[self.weather_duration] = 1
            elif self.current_weather == Weather.RAINDANCE:
                weather_vector[8 * 1 + self.weather_duration] = 1
            elif self.current_weather == Weather.SANDSTORM:
                weather_vector[8 * 2 + self.weather_duration] = 1
            elif self.current_weather == Weather.HAIL:
                weather_vector[8 * 3 + self.weather_duration] = 1
        else:
            weather_vector[-1] = 1

        return weather_vector
    

### NOTE:
    ### Also turn specific effects: Wide Guard, Quick Guard (are SideConditions but not accessible in battle object)
        ### Possibly worth checking for VGC

class FieldTracker:
    def __init__(self):
        ### NOTE:
        ### Naming scheme almost seems to flip between hazards and buffs, 
        ### a 1 in our half means something good for us

        self.rocks = False              # We have stealth rocks active on OPPONENT'S side
        self.opp_rocks = False          # Stealth rocks are active on OUR side
        self.spikes = 0                 # Num layers of spikes on OPPONENT'S side
        self.opp_spikes = 0             # Num layers of spikes on OUR side
        self.tox_spikes = 0             # Num layers of toxic spikes on OPPONENT'S side
        self.opp_tox_spikes = 0         # Num layers of spikes on OUR side
        self.web = 0                    # We have sticky web active on OPPONENT'S side
        self.opp_web = 0                # Sticky web is active on OUR side
        self.hazards = None
        self.reflect = 0                # Num turns reflect has been active
        self.opp_reflect = 0            # Num turns opponent reflect has been active
        self.light_screen = 0           # Num turns light screen has been active
        self.opp_light_screen = 0       # Num turns opponent light screen has been active
        self.safeguard = 0              # Num turns safeguard has been active
        self.opp_safeguard = 0          # Num turns opponent safeguard has been active
        self.tailwind = 0               # Num turns tailwind has been active
        self.opp_tailwind = 0           # Num turns opponent tailwind has been active
        self.aur_veil = 0               # Num turns aurora veil has been active
        self.opp_aur_veil = 0           # Num turns opponent aurora veil has been active
        self.buffs = None
        self.trick_room = 0             # Num turns trick room has been active
        self.wonder_room = 0            # Num turns wonder room has been active
        self.magic_room = 0             # Num turns magic room has been active
        self.rooms = None
        self.electric_terrain = 0           # Num turns electric terrain has been active
        self.grassy_terrain = 0              # Num turns grassy terrain has been active
        self.misty_terrain = 0              # Num turns misty terrain has been active
        self.psychic_terrain = 0            # Num turns psychi terrain has been active
        self.terrains = None
        self.field = None

    def update_field(self, battle):
        """Updates the field state each turn."""
        # Might need to be better done as direct embedding (however... possible..?)
        # or as switch statements with one direct call, not sure what's fastest.
        
        ### Entry Hazards
        # int(SideCondition.STEALTH_ROCK in battle.side_conditions)
        self.rocks = battle.side_conditions.get(SideCondition.SPIKES, 0)
        self.opp_rocks = 2 + battle.opponent_side_conditions.get(SideCondition.SPIKES, 0)

        self.spikes = battle.side_conditions.get(SideCondition.SPIKES, 0)
        self.opp_spikes = 4 + battle.opponent_side_conditions.get(SideCondition.SPIKES, 0)

        self.tox_spikes = battle.side_conditions.get(SideCondition.TOXIC_SPIKES, 0)
        self.opp_tox_spikes = 3 + battle.opponent_side_conditions.get(SideCondition.TOXIC_SPIKES, 0)

        self.web = battle.side_conditions.get(SideCondition.STICKY_WEB, 0)
        self.opp_web = 2 + battle.opponent_side_conditions.get(SideCondition.STICKY_WEB, 0)

        ### Screens
        # possible improvement (look/speed?) to code by, e.g.:
        # clean_compute = int(battle.side_conditions.get(SideCondition.SAFEGUARD, 0) > 0) * (battle.turn - battle.side_conditions.get(SideCondition.SAFEGUARD, 0))
        # or using function:
        # player or us, opp = get_condition_turn(battle, SideCondition.SAFEGUARD)

        # Light Screen
        if battle.side_conditions.get(SideCondition.LIGHT_SCREEN):
            self.light_screen = battle.turn - battle.side_conditions.get(SideCondition.LIGHT_SCREEN, 0)
        else:
            self.light_screen = 0
        if battle.opponent_side_conditions.get(SideCondition.LIGHT_SCREEN):
            self.opp_light_screen = battle.turn - battle.opponent_side_conditions.get(SideCondition.LIGHT_SCREEN, 0)
        else:
            self.opp_light_screen = 0

        # Reflect   
        if battle.side_conditions.get(SideCondition.REFLECT):
            self.reflect = battle.turn - battle.side_conditions.get(SideCondition.REFLECT, 0)
        else:
            self.reflect = 0
        if battle.opponent_side_conditions.get(SideCondition.REFLECT):
            self.opp_reflect = battle.turn - battle.opponent_side_conditions.get(SideCondition.REFLECT, 0)
        else:
            self.opp_reflect = 0
        
        # Safeguard
        if battle.side_conditions.get(SideCondition.SAFEGUARD):
            self.safeguard = battle.turn - battle.side_conditions.get(SideCondition.SAFEGUARD, 0)
        else:
            self.safeguard = 0
        if battle.opponent_side_conditions.get(SideCondition.SAFEGUARD):
            self.opp_safeguard = battle.turn - battle.opponent_side_conditions.get(SideCondition.SAFEGUARD, 0)
        else:
            self.opp_reflect = 0

        # Tailwind
        if battle.side_conditions.get(SideCondition.TAILWIND):
            self.tailwind = battle.turn - battle.side_conditions.get(SideCondition.TAILWIND, 0)
        else:
            self.tailwind = 0
        if battle.opponent_side_conditions.get(SideCondition.TAILWIND):
            self.opp_tailwind = battle.turn - battle.opponent_side_conditions.get(SideCondition.TAILWIND, 0)
        else:
            self.opp_tailwind = 0

        # Aurora Veil   
        if battle.side_conditions.get(SideCondition.AURORA_VEIL):
            self.aur_veil = battle.turn - battle.side_conditions.get(SideCondition.AURORA_VEIL, 0)
        else:
            self.aur_veil = 0
        if battle.opponent_side_conditions.get(SideCondition.AURORA_VEIL):
            self.opp_aur_veil = battle.turn - battle.opponent_side_conditions.get(SideCondition.AURORA_VEIL, 0)
        else:
            self.opp_aur_veil = 0

        ### Field Statues (terrains, rooms)
        # Trick Room
        if battle.fields.get(Field.TRICK_ROOM):
            self.trick_room = battle.turn - battle.fields.get(Field.TRICK_ROOM, 0)
        else:
            self.trick_room = 0
        
        # Wonder Room
        if battle.fields.get(Field.WONDER_ROOM):
            self.wonder_room = battle.turn - battle.fields.get(Field.WONDER_ROOM, 0)
        else:
            self.wonder_room = 0
        
        # Magic Room
        if battle.fields.get(Field.MAGIC_ROOM):
            self.magic_room = battle.turn - battle.fields.get(Field.MAGIC_ROOM, 0)
        else:
            self.magic_room = 0

        # Electric Terrain
        if int(Field.ELECTRIC_TERRAIN in battle.fields):
            self.electric_terrain = battle.turn - battle.fields.get(Field.ELECTRIC_TERRAIN, 0)
        else:
            self.electric_terrain = 0
        
        # Grassy Terrain
        if int(Field.GRASSY_TERRAIN in battle.fields):
            self.grassy_terrain = battle.turn - battle.fields.get(Field.GRASSY_TERRAIN, 0)
        else:
            self.grassy_terrain = 0

        # Misty Terrain
        if int(Field.MISTY_TERRAIN in battle.fields):
            self.misty_terrain = battle.turn - battle.fields.get(Field.MISTY_TERRAIN, 0)
        else:
            self.misty_terrain = 0
        
        # Psychic Terrain
        if int(Field.PSYCHIC_TERRAIN in battle.fields):
            self.psychic_terrain = battle.turn - battle.fields.get(Field.PSYCHIC_TERRAIN, 0)
        else:
            self.psychic_terrain = 0

    def get_state_vector(self):
        """Stores:         
        Rocks:              0 1 (us, opponent)
        Spikes:             0 1 2 3 layers (us, opponent)
        Toxic Spikes:       0 1 2 layers (us, opponent)
        Sticky Web:         0 1 (us, opponent)
        Reflect:            one hot # turns (us, opponent) [idx 0 means inactive]
        Light Screen:       one hot # turns (us, opponent) [idx 0 means inactive]
        Safeguard:          one hot # turns (us, opponent) [idx 0 means inactive]
        Tailwind:           one hot # turns (us, opponent) [idx 0 means inactive]
        Aurora Veil:        one hot # turns (us, opponent) [idx 0 means inactive]
        Trick Room:         one hot # turns (us, opponent) [idx 0 means inactive]
        Wonder Room:        one hot # turns (us, opponent) [idx 0 means inactive]
        Magic Room:         one hot # turns (us, opponent) [idx 0 means inactive]
        Electric Terrain:   one hot # turns (us, opponent) [idx 0 means inactive]
        Grassy Terrain:     one hot # turns (us, opponent) [idx 0 means inactive]
        Misty Terrain:      one hot # turns (us, opponent) [idx 0 means inactive]
        Psychic Terrain:    one hot # turns (us, opponent) [idx 0 means inactive]
        """

        ### NOTE:
        ### Might be good to hard code offsets once we're sure or access poke-env's values
        ### see example values above
        ### Below is cautiously coded, faster implementation later

        ### Entry hazards
        rocks, spikes, tox_spikes = np.zeros(4), np.zeros(8), np.zeros(6)
        rocks[self.rocks] = 1
        rocks[self.opp_rocks] = 1
        spikes[self.spikes] = 1
        spikes[self.opp_spikes] = 1
        tox_spikes[self.tox_spikes] = 1
        tox_spikes[self.opp_tox_spikes] = 1
        self.hazards = np.concatenate((rocks, spikes, tox_spikes))

        # Buffs
        reflect, light_screen, safeguard, tailwind, aur_veil = np.zeros(2*8), np.zeros(2*8), np.zeros(2*8), np.zeros(2*5), np.zeros(2*6)
        reflect[self.reflect] = 1
        reflect[8 + self.opp_reflect] = 1
        light_screen[self.light_screen] = 1
        light_screen[8 + self.opp_light_screen] = 1
        safeguard[self.safeguard] = 1
        safeguard[8 + self.opp_safeguard] = 1
        tailwind[self.tailwind] = 1
        tailwind[5 + self.opp_tailwind] = 1
        aur_veil[self.aur_veil] = 1
        aur_veil[6 + self.opp_aur_veil] = 1
        self.buffs = np.concatenate((light_screen, reflect, safeguard, tailwind, aur_veil))

        # Rooms
        trick_room, wonder_room, magic_room = np.zeros(6), np.zeros(6), np.zeros(6)
        trick_room[self.trick_room] = 1
        wonder_room[self.wonder_room] = 1
        magic_room[self.magic_room] = 1
        self.rooms = np.concatenate((trick_room, wonder_room, magic_room))

        # Terrains
        electric_ter, grass_ter, misty_ter, psychic_ter = np.zeros(7), np.zeros(7), np.zeros(7), np.zeros(7)
        electric_ter[self.electric_terrain] = 1
        grass_ter[self.grassy_terrain] = 1
        misty_ter[self.misty_terrain] = 1
        psychic_ter[self.psychic_terrain] = 1
        self.terrains = np.concatenate((electric_ter, grass_ter, misty_ter, psychic_ter))

        # return np.concatenate((self.hazards, self.buffs, self.rooms, self.terrains))
        return self.terrains
        
    def entry_hazard_test(self):
        assert int(sum(self.hazards)) == 6, f"Expected 6, but got {sum(self.hazards)}"
        print("Corrent number of entry hazards!")


"""
Turn: 19
Opponent Entry Hazards: {<SideCondition.TOXIC_SPIKES: 22>: 2, <SideCondition.STEALTH_ROCK: 19>: 3, <SideCondition.SPIKES: 18>: 2}
Our Entry Hazards: {<SideCondition.STEALTH_ROCK: 19>: 2}
State weather vector: [0. 1. 0. 1. 1. 0. 0. 0. 0. 0. 1. 0. 1. 0. 0. 0. 0. 1.]
"""

"""
MORE FIELD EFFECTS
https://pokemondb.net/move/group/multi-target
https://pokemondb.net/pokebase/291654/what-are-all-the-field-effects
"""

"""
for k, v in battle.side_conditions.items():
    if k == SC.STEALTH_ROCK: print('t')
    else: print('f')

battle.side_conditions
{<SideCondition.STEALTH_ROCK: 19>: 3, <SideCondition.LIGHT_SCREEN: 11>: 17}
 battle.side_conditions.get(SideCondition.STEALTH_ROCK,0)
3
 battle.side_conditions.get(SideCondition.STEALTH_ROCK)
3
battle.opponent_side_conditions
{<SideCondition.TOXIC_SPIKES: 22>: 2, <SideCondition.STEALTH_ROCK: 19>: 2, <SideCondition.SPIKES: 18>: 3}
battle.opponent_side_conditions.get(SideCondition.SPIKES)
3

avoid for loops by just

if battle.side_conditions.get(SideCondition.CONDITION):
    # put the right 1 in the vector

possible side conditions
    UNKNOWN = auto()
x    AURORA_VEIL = auto()
    CRAFTY_SHIELD = auto()
    FIRE_PLEDGE = auto()
    G_MAX_CANNONADE = auto()
    G_MAX_STEELSURGE = auto()
    G_MAX_VINE_LASH = auto()
    G_MAX_VOLCALITH = auto()
    G_MAX_WILDFIRE = auto()
    GRASS_PLEDGE = auto()
x    LIGHT_SCREEN = auto()
    LUCKY_CHANT = auto()
    MATBLOCK = auto()
    MIST = auto()
    QUICK_GUARD = auto()
x    REFLECT = auto()
x    SAFEGUARD = auto()
x    SPIKES = auto()
x    STEALTH_ROCK = auto()
x    STICKY_WEB = auto()
x    TAILWIND = auto()
x    TOXIC_SPIKES = auto()
    WATER_PLEDGE = auto()
    WIDE_GUARD = auto()
"""

"""
class Field(Enum):
    Enumeration, represent a non null field in a battle.

    UNKNOWN = auto()
x    ELECTRIC_TERRAIN = auto()
x    GRASSY_TERRAIN = auto()
    GRAVITY = auto()
    HEAL_BLOCK = auto()
x    MAGIC_ROOM = auto()
x    MISTY_TERRAIN = auto()
    MUD_SPORT = auto()
    MUD_SPOT = auto()
x    PSYCHIC_TERRAIN = auto()
x    TRICK_ROOM = auto()
    WATER_SPORT = auto()
x    WONDER_ROOM = auto()
"""