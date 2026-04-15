import pygame

from storage.gameVars import DESIGN_FPS, FPS

class Laser:
    def __init__(self, angle):
        self.angle = angle
        self.hp = 3
        self.color = (255,0,0)
        self.cooldown = 0

    def hit(self):
        if self.cooldown > 0:
            return
        if self.hp > 0:
            self.hp -= 1
            self.cooldown = 20
            if self.hp <= 0:
                self.color = (0,0,255)

    def update(self, dt=1/DESIGN_FPS):
        if self.cooldown > 0:
            self.cooldown -= dt * DESIGN_FPS
