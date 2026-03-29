import pygame

class Game:
    def __init__(self):
        self.gameTime = 0
        self.friendly_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.healthPackSet = None  # Assign as needed
        self.heartSet = None
        self.playerAnimSet = None
        self.enemyAnimSet = None
        self.miniBossAnimSet = None
        self.bossAnimSet = None
        self.healthBar = None
        self.player = None
