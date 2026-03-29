import pygame
from pygame.locals import *

from storage.animatedObject import AnimatedObject
from storage.gameVars import *

class Entity(AnimatedObject):
    def __init__(self, animSet, name, hp):
        super().__init__(animSet)
        self.hp = hp
        self.name = name
        self.invFrames = 0
        self.dead = False

    def takeDamage(self, dmg, iFrames=30):
        if (self.invFrames > 0 and dmg > 0) or self.dead:
            return
        print(f"{self.name} hit! HP: {self.hp}")
        self.hp -= dmg
        self.invFrames = iFrames

        self.updateHealthBar()

        if self.hp <= 0:
            self.dead = True
            self.onDeath()

    def onDeath(self):
        pass
    
    def updateHealthBar(self):
        pass

    def updateEntity(self):
        self.clampPosition()
        if self.invFrames > 0:
            self.invFrames -= 1
    
    def clampPosition(self):
        self.pos.x = max(0, min(self.pos.x, WIDTH - 20))
        self.pos.y = max(0, min(self.pos.y, HEIGHT - 20))