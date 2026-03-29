import pygame
from pygame.locals import *

from animatedObject import AnimatedObject, processImage
from gameVars import *

class HealthPack(AnimatedObject):
    def __init__(self, animSet, pos):
        super().__init__(animSet)
        self.pos = vec(pos)

    def update(self):
        self.renderAnim()
        self.rect.center = self.pos