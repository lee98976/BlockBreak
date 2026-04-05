import os
import pygame
import copy
import random

from generation.room import Room
from storage.gameVars import *
from storage.animSets import *
from storage.imageUtility import *
from generation.tileHandler import *
from generation.door import *
from generation.button import *
from levels.level1 import *

def build_animset(animSet, scale=4):
    return {
        **animSet,
        "images": [processImage(path, scale) for path in animSet["img_paths"]]
    }

class Game:
    def __init__(self, screen):
        self.gameTime = 0

        self.screen = screen

        # manage entities
        self.friendly_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.ui_sprites = pygame.sprite.Group()
        self.interactables = pygame.sprite.Group()

        self.healthBar = None
        self.player = None

        # preload all images to save memory
        self.playerAnimSet = playerAnimSet
        self.enemyAnimSet = enemyAnimSet
        self.bullieAnimSet = bullieAnimSet
        self.miniBossAnimSet = miniBossAnimSet
        self.bossAnimSet = bossAnimSet
        self.healthPackSet = healthPackSet
        self.heartSet = heartSet
        self.buttonSet = buttonSet
        self.doorSet = doorSet
        self.dashTrailSet = dashTrailSet
        self.diagonalDashTrailSet = diagonalDashTrailSet

        self.buildAnimSets()

        # tile sets!
        self.tileHandler = TileHandler(self)

        self.tile_properties = {
            "empty": {"collide": False},

            "grass": {"collide": True},
            "water": {"collide": False, "slow": 0.5},
            "lava": {"collide": False, "damage": 1},

            "shortSpike": {
                "collide": True,
                "damage": 1,
                "depth": 10
            },
            "tallSpike": {
                "collide": True,
                "damage": 1,
                "depth": 26
            },

            "blackMetal": {"collide": True},
            "rustedBlack": {"collide": True},
        }

        # world generation!
        self.world_layout = [
            [1,1,1],
            [1,1,1],
            [1,1,1],
        ]

        # written by putting functions within list so that they can be recalled again and again in order to recreate deep copies
        self.ROOM_TYPES = [self.maze_room]

        # room generation!
        self.rooms = {}
        self.room_width = WIDTH
        self.room_height = HEIGHT

        self.build_rooms()

        # camera!
        self.camera = vec(0, 0)
        self.camera_lerp = 0.1  # smoothing strength
        self.camera_max_offset = 300 # used to be 120
    
    def buildAnimSets(self):
        self.playerAnimSet = build_animset(self.playerAnimSet)
        self.enemyAnimSet = build_animset(self.enemyAnimSet)
        self.bullieAnimSet = build_animset(self.bullieAnimSet)
        self.miniBossAnimSet = build_animset(self.miniBossAnimSet)
        self.bossAnimSet = build_animset(self.bossAnimSet)
        self.healthPackSet = build_animset(self.healthPackSet)
        self.heartSet = build_animset(self.heartSet)
        self.buttonSet = build_animset(self.buttonSet)
        self.doorSet = build_animset(self.doorSet)
        self.dashTrailSet = build_animset(self.dashTrailSet)
        self.diagonalDashTrailSet = build_animset(self.diagonalDashTrailSet)

    def get_current_room(self, entity):
        px, py = entity.pos

        room_x = int(px // self.room_width)
        room_y = int(py // self.room_height)

        return self.rooms.get((room_x, room_y))
    
    def get_room_center(self):
        room = self.get_current_room(self.player)
        if not room:
            return pygame.Vector2(0, 0)

        return pygame.Vector2(
            room.world_x + room.width / 2,
            room.world_y + room.height / 2
        )
    
    def get_camera_target(self):
        center = self.get_room_center()
        player_pos = self.player.pos

        offset = player_pos - center

        # clamp offset (this is your "edge push")
        offset.x = max(-self.camera_max_offset, min(self.camera_max_offset, offset.x))
        offset.y = max(-self.camera_max_offset, min(self.camera_max_offset, offset.y))

        return center + offset * 0.25
    
    def update_camera(self):
        target = self.get_camera_target()
        self.camera += (target - self.camera) * self.camera_lerp

    def get_doors(self, x, y):
        h = len(self.world_layout)
        w = len(self.world_layout[0])

        return {
            "up":    y > 0 and self.world_layout[y-1][x] == 1,
            "down":  y < h-1 and self.world_layout[y+1][x] == 1,
            "left":  x > 0 and self.world_layout[y][x-1] == 1,
            "right": x < w-1 and self.world_layout[y][x+1] == 1,
        }
    
    def carve_doors(self, grid, doors):
        DOOR_POS = [7, 8]
        DOOR_DEPTH = 1
        size = 16

        def carve(condition, positions):
            if condition:
                for x, y in positions:
                    grid[y][x] = "empty"

        # UP
        carve(
            doors["up"]["type"] in ["hole", "door"],
            [(x, y) for y in range(DOOR_DEPTH) for x in DOOR_POS]
        )

        # DOWN
        carve(
            doors["down"]["type"] in ["hole", "door"],
            [(x, y) for y in range(size - DOOR_DEPTH, size) for x in DOOR_POS]
        )

        # LEFT
        carve(
            doors["left"]["type"] in ["hole", "door"],
            [(x, y) for x in range(DOOR_DEPTH) for y in DOOR_POS]
        )

        # RIGHT
        carve(
            doors["right"]["type"] in ["hole", "door"],
            [(x, y) for x in range(size - DOOR_DEPTH, size) for y in DOOR_POS]
        )

        return grid
    
    def empty_room(self, material):
        return [[material if x==0 or y==0 or x==15 or y==15 else "empty"
                for x in range(16)] for y in range(16)]
    
    def open_field_room(self, material):
        grid = self.empty_room(material)

        # random small rocks (use walls)
        for _ in range(8):
            x = random.randint(2, 13)
            y = random.randint(2, 13)
            grid[y][x] = material

        return grid
    
    def pond_room(self):
        grid = self.empty_room("grass")

        for y in range(5, 10):
            for x in range(5, 10):
                grid[y][x] = "water"

        # stepping stone
        grid[7][7] = "empty"

        return grid
    
    def spike_room(self, material):
        grid = self.empty_room(material)

        for x in range(3, 13):
            if x % 2 == 0:
                grid[6][x] = "shortSpike"
                grid[10][x] = "tallSpike"

        return grid
    
    def maze_room_material(self, material):
        grid = self.empty_room(material)

        for x in range(2, 14, 2):
            for y in range(2, 14):
                grid[y][x] = material

        return grid
    
    def lava_entry_room(self):
        grid = self.empty_room("blackMetal")

        for x in range(4, 12):
            grid[8][x] = "lava"

        return grid
    
    def lava_corridor_room(self):
        grid = self.empty_room("blackMetal")

        for y in range(2, 14):
            grid[y][7] = "lava"
            grid[y][8] = "lava"

        return grid
    
    def lava_arena_room(self):
        grid = self.empty_room("blackMetal")

        # lava ring
        for x in range(4, 12):
            grid[4][x] = "lava"
            grid[11][x] = "lava"

        for y in range(4, 12):
            grid[y][4] = "lava"
            grid[y][11] = "lava"

        return grid

    def nature_showcase_room(self):
        size = 16
        grid = self.empty_room("grass")

        # --- WATER POND (organic blob) ---
        pond = [
            (5,5),(6,5),(7,5),(8,5),(9,5),
            (5,6),(6,6),(7,6),(8,6),(9,6),
            (5,7),(6,7),(7,7),(8,7),(9,7),
            (6,8),(7,8),(8,8)
        ]

        for x, y in pond:
            grid[y][x] = "water"

        # --- HOLES INSIDE WATER ---
        grid[7][8] = "empty"

        # --- SECOND SMALL POND ---
        for x, y in [(11,3),(12,3),(11,4)]:
            grid[y][x] = "water"

        # --- LAVA FLOW (curved path) ---
        lava_path = [
            (2,12),(3, 12), (3,11),(4, 11),(4,10),(5,10)
        ]

        for x, y in lava_path:
            grid[y][x] = "lava"


        return grid


    def structure_showcase_room(self):
        size = 16
        grid = self.empty_room("blackMetal")

        # --- BLACK STRUCTURE (top-left block) ---
        for y in range(2,6):
            for x in range(2,6):
                grid[y][x] = "blackMetal"

        # --- RUSTED STRUCTURE (top-right L-shape) ---
        for x in range(10,14):
            grid[2][x] = "rustedBlack"
        for y in range(2,7):
            grid[y][13] = "rustedBlack"

        # --- METAL STRUCTURE (center square with hole) ---
        for y in range(6,11):
            for x in range(6,11):
                grid[y][x] = "blackMetal"

        # hole
        grid[8][8] = "empty"

        # --- SMALL METAL PILLAR (bottom-left) ---
        grid[12][3] = "blackMetal"
        grid[13][3] = "blackMetal"

        # --- RUSTED LINE (bottom horizontal) ---
        for x in range(7,13):
            grid[13][x] = "rustedBlack"

        return grid
    
    def maze_room(self):
        grid = self.empty_room("blackMetal")
        for x in range(2, 14, 2):
            for y in range(2, 14):
                grid[y][x] = "blackMetal"
        return grid
    
    def attach_button_to_room(self, room):
        # --- event ---
        room.events = [
            {
                "trigger": "button",
                "action": "open_door",
                "params": {"direction": "left"},
                "done": False
            }
        ]

        self.spawn_button(room, 14, 7)

        return room

    def build_rooms(self):
        height = len(LEVEL_1_LAYOUT)
        width = len(LEVEL_1_LAYOUT[0])

        self.world_layout = [[1 for _ in range(width)] for _ in range(height)]

        for y in range(height):
            for x in range(width):
                room_type = LEVEL_1_ROOMS.get((x, y), "empty")

                room = Room(self, x, y, self.room_width, self.room_height)

                door_config = ROOM_DOORS.get((x, y))
                if door_config:
                    for d in ["up", "down", "left", "right"]:
                        room.doors[d]["type"] = door_config.get(d, "wall")
                else:
                    auto = self.get_doors(x, y)
                    for d in auto:
                        room.doors[d]["type"] = "hole" if auto[d] else "wall"

                # --- choose generator ---
                if room_type == "open_field":
                    grid = self.open_field_room("grass")

                elif room_type == "pond":
                    grid = self.pond_room()

                elif room_type == "spike_field":
                    grid = self.spike_room("grass")

                elif room_type == "maze_grass":
                    grid = self.maze_room_material("grass")

                elif room_type == "button_gate":
                    grid = self.empty_room("grass")
                    room = self.attach_button_to_room(room)

                elif room_type == "lava_entry":
                    grid = self.lava_entry_room()

                elif room_type == "lava_corridor":
                    grid = self.lava_corridor_room()

                elif room_type == "lava_arena":
                    grid = self.lava_arena_room()

                else:
                    grid = self.empty_room("grass")

                # --- apply tiles ---
                if grid:
                    grid = self.carve_doors(grid, room.doors)
                    room.update_tiles(grid)

                # --- entities ---
                self.spawn_doors(room)


                room.update_door_rects()
                self.rooms[(x, y)] = room

    def spawn_doors(self, room):
        TILE = 32

        door_positions = {
            "up": [(7,0),(8,0)],
            "down": [(7,15),(8,15)],
            "left": [(0,7),(0,8)],
            "right": [(15,7),(15,8)],
        }

        for direction, positions in door_positions.items():
            if room.doors[direction]["type"] != "door":
                continue

            for tx, ty in positions:
                world_pos = (
                    room.world_x + tx * TILE + TILE // 2,
                    room.world_y + ty * TILE + TILE // 2
                )

                door = Door(self, room, world_pos, direction)
                self.interactables.add(door)
    
    def spawn_button(self, room, tx, ty):
        TILE = 32

        world_pos = (
            room.world_x + tx * TILE + TILE // 2,
            room.world_y + ty * TILE + TILE // 2
        )

        button = Button(self, room, world_pos)
        self.interactables.add(button)