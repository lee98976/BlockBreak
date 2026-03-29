import pygame

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