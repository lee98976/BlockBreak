import os
import pygame
import copy
import random

from entities.bullie import Bullie
from entities.reddie import Reddie
from entities.player import Player
from entities.miniboss import MiniBoss
from entities.boss import Boss
from ui.dialogueManager import DialogueManager
from ui.healthbar import HealthBar
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
        self.currentLevel = 1

        # manage entities
        self.friendly_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.ui_sprites = pygame.sprite.Group()
        self.interactables = pygame.sprite.Group()

        self.healthBar = None
        self.player = None
        self.boss = None
        self.miniBoss1 = None
        self.miniBoss2 = None
        self.has_boss_activated = False

        # screen shake
        self.screen_shake_offset = vec(0, 0)

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
        self.dialogueAnimSet = dialogueAnimSet

        self.buildAnimSets()

        # dialogue!
        self.dialogue = DialogueManager(self)

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
        self.initialize_entities()

        # TODO FIX HARDCODING, let level handle this later
        self.attach_dialogue_to_room(self.rooms[(0, 2)], [
            {"text": "Hmph..", "speaker": "player"},
            {"text": "Of course that stupid boss ran away to this annoying little hideout.", "speaker": "player"},
            {"text": "If he also brought his reddies over there, I'm so not ready.", "speaker" : "player"},
            {"text": "Use arrow keys to move.", "speaker": "game"},
        ])
        self.attach_dialogue_to_room(self.rooms[(0, 1)], [
            {"text": "Of course.", "speaker": "player"},
            {"text": "Hey! What are you doi--", "speaker": "reddie"},
            {"text": "Shut up you idiots. Actually, I'll make you.", "speaker" : "player"},
            {"text": "Press [X] to dash into enemies.", "speaker": "game"},
        ])
        self.attach_dialogue_to_room(self.rooms[(0, 0)], [
            {"text": "These ranged units are a bit annoying.", "speaker": "player"},
            {"text": "Maybe address me by my name: Bullie!", "speaker": "bullie"},
            {"text": "Cause I shoot bullets, get it?", "speaker" : "bullie"},
            {"text": "No.", "speaker": "player"},
        ])
        self.attach_dialogue_to_room(self.rooms[(2, 0)], [
            {"text": "Spikes too? Bro might be a little scared of me...", "speaker": "player"},
        ])
        self.attach_dialogue_to_room(self.rooms[(2, 1)], [
            {"text": "Did he seriously put the button to his castle on his front door?", "speaker": "player"},
            {"text": "I'm not blind.", "speaker": "player"},
        ])
        self.attach_dialogue_to_room(self.rooms[(1, 1)], [
            {"text": "...", "speaker": "player"}
        ])
        self.attach_dialogue_to_room(self.rooms[(2, 2)], [
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
        ])
        
        self.attach_enemies_to_room(self.rooms[(0, 1)], self.generate_enemies_for_room(self.rooms[(0, 1)], 5, 0))
        self.attach_enemies_to_room(self.rooms[(0, 0)], self.generate_enemies_for_room(self.rooms[(0, 0)], 2, 3))
        self.attach_enemies_to_room(self.rooms[(1, 0)], self.generate_enemies_for_room(self.rooms[(1, 0)], 3, 1))
        self.attach_enemies_to_room(self.rooms[(1, 1)], self.generate_enemies_for_room(self.rooms[(1, 1)], 0, 15))

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
        self.dialogueAnimSet = build_animset(self.dialogueAnimSet)

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

    def update_screen_shake(self):
        if not self.boss or not self.boss.active:
            self.screen_shake_offset = vec(0, 0)
        else:
            self.screen_shake_offset = vec(random.randint(-2, 2), random.randint(-2, 2))

    def initialize_entities(self):
        self.healthBar = HealthBar(self)
        self.player = Player(self, self.healthBar, vec(240, 1450))
        self.friendly_sprites.add(self.player)
        self.healthBar.updateHealth(self.player.hp)

        # self.miniBoss1 = MiniBoss(self, self.player, self.enemy_sprites, vec(120, 120))
        # self.miniBoss2 = MiniBoss(self, self.player, self.enemy_sprites, vec(280, 120))
        # self.enemy_sprites.add(self.miniBoss1)
        # self.enemy_sprites.add(self.miniBoss2)

        # self.boss = Boss(self, vec(200, 80))
        # self.enemy_sprites.add(self.boss)

        start_room = self.get_current_room(self.player)
        if start_room:
            start_room.discovered = True

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

        for y in range(4, 8):
            for x in range(2, 6):
                grid[y][x] = "water"
        
        for y in range(5, 7):
            for x in range(3, 5):
                grid[y][x] = "grass"

        for y in range(8, 12):
            for x in range(6, 12):
                grid[y][x] = "water"

        for y in range(9, 11):
            for x in range(8, 11):
                grid[y][x] = "grass" 
        
        grid[9][7] = "grass"

        grassCoords = [(14, 14), (13, 14), (14, 13), (14, 1), (13, 1), (14, 2), (1, 1), (2, 1), (1, 2), (1, 14), (2, 14), (1, 13)]
        for x, y in grassCoords:
            grid[y][x] = "grass"


        return grid
    
    def pond_room(self):
        grid = self.empty_room("grass")

        for y in range(1, 15):
            for x in range(1, 15):
                grid[y][x] = "water"

        # stepping stone
        grid[7][7] = "empty"
        grid[7][8] = "empty"
        grid[8][7] = "empty"

        grid[4][4] = "empty"
        grid[4][3] = "empty"
        grid[3][4] = "empty"

        grid[12][8] = "empty"

        return grid
    
    def spike_room(self, material):
        grid = self.empty_room(material)

        for x in range(2, 14):
            grid[1][x] = "shortSpike"
            grid[14][x] = "shortSpike"
            grid[x][1] = "shortSpike"
            grid[x][14] = "shortSpike"
        
        grid[14][7] = "empty"
        grid[14][8] = "empty"
        grid[7][1] = "empty"
        grid[8][1] = "empty"

        def genSpikedBlock(x, y):
            for y1 in range(y-1, y+3):
                for x1 in range(x-1, x+3):
                    grid[y1][x1] = "tallSpike"

            for y1 in range(y, y+2):
                for x1 in range(x, x+2):
                    grid[y1][x1] = "blackMetal"
            
            grid[y-1][x-1] = "empty"
            grid[y-1][x+2] = "empty"
            grid[y+2][x-1] = "empty"
            grid[y+2][x+2] = "empty"
        
        genSpikedBlock(6, 3)
        genSpikedBlock(3, 10)
        genSpikedBlock(7, 9)

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
        room.events.append(
            {
                "trigger": "button",
                "action": "open_door",
                "params": {"direction": "left"},
                "done": False
            }
        )

        self.spawn_button(room, 14, 7)

        return room
    
    def attach_dialogue_to_room(self, room, dialogue):
        room.events.append(
            {
                "trigger": "enter",
                "action": "dialogue",
                "params": {
                    "dialogue": dialogue
                },
                "done": False
            }
        )

        return room
    
    def generate_enemies_for_room(self, room, num_reddies=2, num_bullies=1):
        enemies = []

        def random_pos():
            while True:
                x = random.randint(0, 15)
                y = random.randint(0, 15)

                if room.tiles[y][x] == "empty":
                    return vec(
                        room.world_x + x * 32 + 16,
                        room.world_y + y * 32 + 16
                    )

        # --- spawn reddies ---
        for _ in range(num_reddies):
            pos = random_pos()
            r = Reddie(self, 3, self.player, 0.3, pos)
            enemies.append(r)

        # --- spawn bullies ---
        for _ in range(num_bullies):
            pos = random_pos()
            b = Bullie(self, pos, self.player)  # adjust args if needed
            enemies.append(b)

        return enemies

    def attach_enemies_to_room(self, room, enemies):
        room.events.append(
            {
                "trigger": "all_enemies_dead",
                "action": "open_all_doors",
                "done": False
            }
        )

        # spawn enemies
        for i in enemies:
            self.enemy_sprites.add(i)
            room.enemies.append(i)
        
            print(i.pos, i.hp)

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