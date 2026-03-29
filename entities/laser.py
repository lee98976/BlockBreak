import pygame

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

    def update(self):
        if self.cooldown > 0:
            self.cooldown -= 1
