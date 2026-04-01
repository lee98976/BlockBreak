import pygame
from storage.gameVars import *

class Room:
    def __init__(self, x, y, width, height):
        self.grid_pos = (x, y)

        self.width = width
        self.height = height

        self.world_x = x * width
        self.world_y = y * height

        self.rect = pygame.Rect(self.world_x, self.world_y, width, height)

        self.enemies = pygame.sprite.Group()
        self.interactables = []

        self.completed = False

        # self.tiles = [
        #     ["blackMetal","blackMetal","blackMetal","blackMetal","blackMetal","blackMetal","blackMetal","empty","empty","blackMetal","blackMetal","blackMetal","blackMetal","blackMetal","blackMetal","blackMetal"],

        #     ["blackMetal","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","blackMetal"],
        #     ["blackMetal","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","blackMetal"],
        #     ["blackMetal","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","blackMetal"],
        #     ["blackMetal","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","blackMetal"],
        #     ["blackMetal","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","blackMetal"],
        #     ["blackMetal","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","blackMetal"],

        #     ["empty","empty","empty","empty","empty","empty","empty","blackMetal","blackMetal","empty","empty","empty","empty","empty","empty","empty"],
        #     ["empty","empty","empty","empty","empty","empty","empty","blackMetal","blackMetal","empty","empty","empty","empty","empty","empty","empty"],

        #     ["blackMetal","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","blackMetal"],
        #     ["blackMetal","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","blackMetal"],
        #     ["blackMetal","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","blackMetal"],
        #     ["blackMetal","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","blackMetal"],
        #     ["blackMetal","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","blackMetal"],
        #     ["blackMetal","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","blackMetal"],

        #     ["blackMetal","blackMetal","blackMetal","blackMetal","blackMetal","blackMetal","blackMetal","empty","empty","blackMetal","blackMetal","blackMetal","blackMetal","blackMetal","blackMetal","blackMetal"],
        # ]

        # # for collision purposes
        # self.wall_rects = self.get_wall_rects()
        self.tiles = []
        self.wall_rects = []

    def update_tiles(self, tiles):
        self.tiles = tiles
        self.wall_rects = self.get_wall_rects()

    def get_tile_rect(self, x, y):
        return pygame.Rect(
            self.world_x + x * 32,
            self.world_y + y * 32,
            32,
            32
        )
    
    def get_wall_rects(self):
        rects = []
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                if tile != "empty":
                    rects.append(self.get_tile_rect(x, y))
        return rects