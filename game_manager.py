import pygame

from storage.animSets import *

def processImage(path, scale):
    unscaled = pygame.image.load(path).convert_alpha()

    newWidth = int(unscaled.get_width() * scale)
    newHeight = int(unscaled.get_height() * scale)

    return pygame.transform.scale(unscaled, (newWidth, newHeight))

def build_animset(animSet, scale=4):
    return {
        **animSet,
        "images": [processImage(path, scale) for path in animSet["img_paths"]]
    }

class Game:
    def __init__(self):
        self.gameTime = 0
        self.friendly_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.healthBar = None
        self.player = None

        self.playerAnimSet = playerAnimSet
        self.enemyAnimSet = enemyAnimSet
        self.miniBossAnimSet = miniBossAnimSet
        self.bossAnimSet = bossAnimSet
        self.healthPackSet = healthPackSet
        self.heartSet = heartSet

        self.buildAnimSets()

    def buildAnimSets(self):
        self.playerAnimSet = build_animset(self.playerAnimSet)
        self.enemyAnimSet = build_animset(self.enemyAnimSet)
        self.miniBossAnimSet = build_animset(self.miniBossAnimSet)
        self.bossAnimSet = build_animset(self.bossAnimSet)
        self.healthPackSet = build_animset(self.healthPackSet)
        self.heartSet = build_animset(self.heartSet)

    def update(self):
        self.friendly_sprites.update()
        self.enemy_sprites.update()

    def draw(self, screen):
        self.friendly_sprites.draw(screen)
        self.enemy_sprites.draw(screen)
