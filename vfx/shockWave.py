from storage.gameVars import *

class Shockwave:
    def __init__(self, pos, radius=0, speed=0.5, thickness=14, strength=3):
        self.pos = vec(pos)
        self.radius = radius
        self.speed = speed
        self.thickness = thickness
        self.strength = strength
        self.alive = True

    def update(self, dt=1/DESIGN_FPS):
        self.radius += self.speed
        self.strength *= 0.92
        self.thickness *= 0.9

        if self.strength < 0.1:
            self.alive = False