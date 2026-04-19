# level2.py - Example level 2

LEVEL_2_LAYOUT = [
    [1, 1],
    [1, 1],
]

LEVEL_2_ROOMS = {
    (0,0): "open_field",
    (1,0): "spike_field",
    (0,1): "maze_grass",
    (1,1): "lava_entry",
}

LEVEL_2_DOORS = {
    (0,0): {"up": "wall", "down": "hole", "left": "wall", "right": "hole"},
    (1,0): {"up": "wall", "down": "hole", "left": "hole", "right": "wall"},
    (0,1): {"up": "hole", "down": "wall", "left": "wall", "right": "wall"},
    (1,1): {"up": "hole", "down": "wall", "left": "wall", "right": "wall"},
}

LEVEL_2_DIALOGUES = {
    (0,0): [{"text": "Welcome to level 2!", "speaker": "game"}],
}

LEVEL_2_ENEMIES = {
    (0,0): (3, 1),
    (1,0): (2, 2),
}

LEVEL_2_DATA = {
    "layout": LEVEL_2_LAYOUT,
    "rooms": LEVEL_2_ROOMS,
    "doors": LEVEL_2_DOORS,
    "dialogues": LEVEL_2_DIALOGUES,
    "enemies": LEVEL_2_ENEMIES,
    "player_spawn": [60, 100],
}