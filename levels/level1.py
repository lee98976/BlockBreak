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
        "right": "door",
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
        "down": "hole",
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