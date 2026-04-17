
from storage.gameVars import *

class Shockwave:
    def __init__(self, pos):
        self.pos = vec(pos)
        self.radius = 0
        self.speed = 0.5
        self.thickness = 12
        self.strength = 3
        self.alive = True

    def update(self):
        self.radius += self.speed
        self.strength *= 0.92
        self.thickness *= 0.9

        if self.strength < 0.1:
            self.alive = False