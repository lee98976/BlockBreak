import pygame
from animatedObject import AnimatedObject

class Heart(AnimatedObject):
    def __init__(self, animSet, pos):
        super().__init__(animSet)
        self.pos = pygame.Vector2(pos)
        self.on = True
        self.defaultAnim = 1
        self.changeAnim(2)
    
    def turnOn(self):
        self.on = True
        self.changeAnim(3)
        self.defaultAnim = 1
    def turnOff(self):
        self.on = False
        self.changeAnim(2)
        self.defaultAnim = 0
    
    def update(self):
        self.renderAnim()
        self.rect.center = self.pos
