# level1.py

# ---------------------------------
# ROOM LAYOUT (3x3)
# ---------------------------------
# (x, y):
#
# (0,0) open_field     (1,0) pond         (2,0) spike_field
# (0,1) maze_grass     (1,1) lava_entry   (2,1) button_gate
# (0,2) open_field     (1,2) lava_corridor (2,2) lava_arena
#

LEVEL_1_LAYOUT = [
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1],
]


# ---------------------------------
# ROOM TYPES
# ---------------------------------

LEVEL_1_ROOMS = {
    (0,0): "open_field",
    (1,0): "pond",
    (2,0): "spike_field",

    (0,1): "maze_grass",
    (1,1): "lava_entry",
    (2,1): "button_gate",

    (0,2): "open_field",
    (1,2): "lava_corridor",
    (2,2): "lava_arena",
}


# ---------------------------------
# DOOR CONFIG
# type = "wall" | "hole" | "door"
# ---------------------------------

ROOM_DOORS = {

    # -------------------------
    # (0,0) OPEN FIELD (START)
    # → right only
    # -------------------------
    (0,0): {
        "up": "wall",
        "down": "hole",
        "left": "wall",
        "right": "door",
    },

    # -------------------------
    # (1,0) POND
    # → left and right
    # -------------------------
    (1,0): {
        "up": "wall",
        "down": "wall",
        "left": "hole",
        "right": "hole",
    },

    # -------------------------
    # (2,0) SPIKE FIELD
    # → down only
    # -------------------------
    (2,0): {
        "up": "wall",
        "down": "hole",
        "left": "hole",
        "right": "wall",
    },

    # -------------------------
    # (0,1) MAZE GRASS
    # → up and down
    # -------------------------
    (0,1): {
        "up": "door",
        "down": "hole",
        "left": "wall",
        "right": "wall",
    },

    # -------------------------
    # (1,1) LAVA ENTRY
    # → down only
    # -------------------------
    (1,1): {
        "up": "wall",
        "down": "door",
        "left": "wall",
        "right": "hole",
    },

    # -------------------------
    # (2,1) BUTTON GATE
    # ← left is DOOR (locked)
    # ↑ from spike field
    # -------------------------
    (2,1): {
        "up": "hole",
        "down": "wall",
        "left": "door",   # 🔥 main mechanic
        "right": "wall",
    },

    # -------------------------
    # (0,2) OPEN FIELD
    # → up only
    # -------------------------
    (0,2): {
        "up": "hole",
        "down": "wall",
        "left": "wall",
        "right": "wall",
    },

    # -------------------------
    # (1,2) LAVA CORRIDOR
    # → right only
    # -------------------------
    (1,2): {
        "up": "hole",
        "down": "wall",
        "left": "wall",
        "right": "hole",
    },

    # -------------------------
    # (2,2) LAVA ARENA
    # ← entry only
    # -------------------------
    (2,2): {
        "up": "wall",
        "down": "wall",
        "left": "hole",
        "right": "wall",
    },
}


# ---------------------------------
# DIALOGUE CONFIG
# ---------------------------------

LEVEL_1_DIALOGUES = {
    (0, 2): [
        {"text": "Hmph..", "speaker": "player"},
        {"text": "Of course that stupid boss ran away to this annoying little hideout.", "speaker": "player"},
        {"text": "If he also brought his reddies over there, I'm so not ready.", "speaker" : "player"},
        {"text": "Use arrow keys to move.", "speaker": "game"},
    ],
    (0, 1): [
        {"text": "Of course.", "speaker": "player"},
        {"text": "Hey! What are you doi--", "speaker": "reddie"},
        {"text": "Shut up you idiots. Actually, I'll make you.", "speaker" : "player"},
        {"text": "Press [X] to dash into enemies.", "speaker": "game"},
    ],
    (0, 0): [
        {"text": "These ranged units are a bit annoying.", "speaker": "player"},
        {"text": "Maybe address me by my name: Bullie!", "speaker": "bullie"},
        {"text": "Cause I shoot bullets, get it?", "speaker" : "bullie"},
        {"text": "No.", "speaker": "player"},
    ],
    (2, 0): [
        {"text": "Spikes too? Bro might be a little scared of me...", "speaker": "player"},
    ],
    (2, 1): [
        {"text": "Did he seriously put the button to his castle on his front door?", "speaker": "player"},
        {"text": "I'm not blind.", "speaker": "player"},
    ],
    (1, 1): [
        {"text": "...", "speaker": "player"}
    ],
    (2, 2): [
        {"speaker": "player", "text": "Wait... this is the place."},
        {"speaker": "player", "text": "He was supposed to be here."},

        {"speaker": "reddie", "text": "Uh... about that."},
        {"speaker": "reddie", "text": "He kinda... left."},

        {"speaker": "player", "text": "...He WHAT?"},

        {"speaker": "bullie", "text": "Yeah, he said something about..."},
        {"speaker": "bullie", "text": "'not being ready for this build'."},

        {"speaker": "player", "text": "...You're kidding."},

        {"speaker": "reddie", "text": "Nope. He ran that way."},

        {"speaker": "player", "text": "Great. Of course he ran through the metal walls."},
        {"speaker": "player", "text": "Welp. I guess I gotta wait until the beta build comes out in April 12..."},
        
        {"text": "Hey.", "speaker": "game"},
        {"text": "Thanks for watching.", "speaker": "game"},

        {"text": "This project started out as merely an game for AP CSP.", "speaker": "game"},
        {"text": "However, I noticed the potential in this game, and sought out to develop it.", "speaker": "game"},

        {"text": "From the ground up in Pygame, I developed every single system.", "speaker": "game"},
        {"text": "From things like animations, rendering, room events, dialogue, enemies, game mechanics,", "speaker": "game"},
        {"text": "I have essentially created an entire game engine.", "speaker": "game"},

        {"text": "Even something as simple as enemy movement required hundreds of lines to create.", "speaker": "game"},
        {"text": "I utilized the well known algorithm A* to calculate pretty decent paths between two locations.", "speaker": "game"},

        {"text": "Rooms track their own state, events, and progression.", "speaker": "game"},
        {"text": "That’s how things like buttons and doors are able to work together.", "speaker": "game"},

        {"text": "I also built the tile system from the ground up.", "speaker": "game"},
        {"text": "I had to figure out how to tile, and what kind of tiles to use.", "speaker": "game"},
        {"text": "They are all handdrawn, by the way.", "speaker": "game"},
        {"text": "Note: Currently, I have five types of tiles", "speaker": "game"},
        {"text": "But real games have so much more. It's going to be a long time before becoming a true 2D developer...", "speaker": "game"},

        {"text": "Overall, a lot of this was challenging, and many bugs arose.", "speaker": "game"},
        {"text": "But, the fun of the game is what made me strive to continue development.", "speaker": "game"},

        {"text": "If there’s one thing I’m proud of,", "speaker": "game"},
        {"text": "it’s that this is one of the first games I've developed", "speaker": "game"},
        {"text": "to be robust and allow further additions easily.", "speaker": "game"},

        {"text": "Thanks. Jacob Lee", "speaker": "game"},
    ],
}


# ---------------------------------
# ENEMY CONFIG
# (room_coords): (num_reddies, num_bullies)
# ---------------------------------

LEVEL_1_ENEMIES = {
    (0, 1): (5, 0),
    (0, 0): (2, 3),
    (1, 0): (3, 1),
    (1, 1): (0, 15),
}


# ---------------------------------
# LEVEL DATA STRUCTURE
# ---------------------------------

LEVEL_1_DATA = {
    "layout": LEVEL_1_LAYOUT,
    "rooms": LEVEL_1_ROOMS,
    "doors": ROOM_DOORS,
    "dialogues": LEVEL_1_DIALOGUES,
    "enemies": LEVEL_1_ENEMIES,
    "player_spawn": [60, 362],
}