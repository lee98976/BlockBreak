import pygame
from pygame.locals import *

from storage.animatedObject import AnimatedObject
from storage.gameVars import *

class HealthPack(AnimatedObject):
    def __init__(self, game, pos):
        super().__init__(game.healthPackSet)
        self.pos = vec(pos)

    def update(self, dt=1/DESIGN_FPS):
        self.renderAnim(dt)
        self.rect.center = self.pos