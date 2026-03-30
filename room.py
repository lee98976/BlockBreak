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

        self.tile_size = 32
        self.tiles = ["1111111001111111"] + ["1000000000000001" for i in range(6)] + ["0000000000000000" for i in range(2)] + ["1000000000000001" for i in range(6)] + ["1111111001111111"]
        self.wall_rects = self.get_wall_rects()
    
    def draw_tiles(self, screen, camera):
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                rect = self.get_tile_rect(x, y)


                offset = rect.topleft - camera + vec(WIDTH/2, HEIGHT/2)
                screen_rect = pygame.Rect(offset.x, offset.y, rect.width, rect.height)

                if tile == "1": color = (0, 0, 0)
                else: color = (255, 255, 255)
                pygame.draw.rect(screen, color, screen_rect)

    def get_tile_rect(self, x, y):
        return pygame.Rect(
            self.world_x + x * self.tile_size,
            self.world_y + y * self.tile_size,
            self.tile_size,
            self.tile_size
        )
    
    def get_wall_rects(self):
        rects = []
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                if tile == "1":
                    rects.append(self.get_tile_rect(x, y))
        return rects