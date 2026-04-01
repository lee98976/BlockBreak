import os
import pygame
import copy
import random

from room import Room
from storage.gameVars import *
from storage.animSets import *
from storage.imageUtility import *
from tileHandler import *

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

        self.healthBar = None
        self.player = None

        # preload all images to save memory
        self.playerAnimSet = playerAnimSet
        self.enemyAnimSet = enemyAnimSet
        self.miniBossAnimSet = miniBossAnimSet
        self.bossAnimSet = bossAnimSet
        self.healthPackSet = healthPackSet
        self.heartSet = heartSet

        self.buildAnimSets()

        # tile sets!
        self.tileHandler = TileHandler(self)

        # world generation!
        self.world_layout = [
            [1,1,1],
            [1,1,1],
            [1,1,1],
        ]
        self.ROOM_TYPES = [self.empty_room, self.pillar_room, self.split_room, self.arena_room]

        # room generation!
        self.rooms = {}
        self.room_width = WIDTH
        self.room_height = HEIGHT

        self.build_rooms()

        # camera!
        self.camera = vec(0, 0)
        self.camera_lerp = 0.1  # smoothing strength
        self.camera_max_offset = 120
    
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

    def buildAnimSets(self):
        self.playerAnimSet = build_animset(self.playerAnimSet)
        self.enemyAnimSet = build_animset(self.enemyAnimSet)
        self.miniBossAnimSet = build_animset(self.miniBossAnimSet)
        self.bossAnimSet = build_animset(self.bossAnimSet)
        self.healthPackSet = build_animset(self.healthPackSet)
        self.heartSet = build_animset(self.heartSet)

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
        DOOR_POS = [7, 8, 9, 10]  # fixed positions
        DOOR_DEPTH = 2
        size = 16

        # --- TOP ---
        if doors["up"]:
            for y in range(DOOR_DEPTH):
                for x in DOOR_POS:
                    grid[y][x] = "empty"

        # --- BOTTOM ---
        if doors["down"]:
            for y in range(size - DOOR_DEPTH, size):
                for x in DOOR_POS:
                    grid[y][x] = "empty"

        # --- LEFT ---
        if doors["left"]:
            for x in range(DOOR_DEPTH):
                for y in DOOR_POS:
                    grid[y][x] = "empty"

        # --- RIGHT ---
        if doors["right"]:
            for x in range(size - DOOR_DEPTH, size):
                for y in DOOR_POS:
                    grid[y][x] = "empty"

        return grid
    
    def empty_room(self):
        return [["blackMetal" if x==0 or y==0 or x==15 or y==15 else "empty"
                for x in range(16)] for y in range(16)]
    
    def pillar_room(self):
        grid = self.empty_room()

        for y in range(6,10):
            for x in range(6,10):
                grid[y][x] = "blackMetal"

        return grid
    
    def split_room(self):
        grid = self.empty_room()

        for y in range(16):
            grid[y][8] = "blackMetal"

        return grid
    
    def arena_room(self):
        grid = self.empty_room()

        # small center obstacle
        for y in range(7,9):
            for x in range(7,9):
                grid[y][x] = "blackMetal"

        return grid

    def build_rooms(self):
        for x in range(3):
            for y in range(3):
                room = Room(x, y, self.room_width, self.room_height)

                # if self.world_layout[y][x] == 0:
                #     continue

                # pick a room design
                grid = random.choice(self.ROOM_TYPES)()

                # carve doors
                doors = self.get_doors(x, y)
                grid = self.carve_doors(grid, doors)
                room.update_tiles(grid)

                self.rooms[(x, y)] = room