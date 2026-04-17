import pygame
from storage.gameVars import *
from vfx.shockWave import *

class vfxManager():
    def __init__(self, game):
        self.game = game
        self.shockwaves = []

    def add_shockwave(self, pos):
        self.shockwaves.append(Shockwave(pos))

    def apply_shockwaves(self, surface):
        w, h = surface.get_size()
        result = pygame.Surface((w, h))

        for y in range(h):
            for x in range(w):

                # start with original position
                sx, sy = x, y

                ring_intensity = 0

                for wave in self.shockwaves:
                    screen_center = vec(w // 2, h // 2)
                    screen_pos = (wave.pos - self.game.camera) + screen_center

                    cx = screen_pos.x
                    cy = screen_pos.y

                    dx = x - cx
                    dy = y - cy
                    dist = (dx*dx + dy*dy) ** 0.5

                    diff = dist - wave.radius
                    if abs(diff) > wave.thickness:
                        continue

                    if dist == 0:
                        continue
                    

                    if abs(diff) < wave.thickness:
                        ring_intensity += (wave.thickness - abs(diff)) / wave.thickness * wave.strength * 30

                    force = (wave.thickness - abs(diff)) / wave.thickness
                    force *= wave.strength

                    # BACKWARD sampling
                    sx -= dx / dist * force
                    sy -= dy / dist * force

                ix = int(sx)
                iy = int(sy)

                if 0 <= ix < w and 0 <= iy < h:
                    color = surface.get_at((ix, iy))

                    if ring_intensity > 0:
                        t = min(1, ring_intensity / 255)

                        # blend toward blue
                        r = int(color.r * (1 - t))
                        g = int(color.g * (1 - t))
                        b = int(color.b * (1 - t) + 255 * t)

                        color = (r, g, b)

                    result.set_at((x, y), color)
                else:
                    result.set_at((x, y), (0, 0, 0))

        return result
    
    def update(self):
        i = 0
        while i < len(self.shockwaves):
            self.shockwaves[i].update()
            if not self.shockwaves[i].alive:  self.shockwaves.pop(i)
            else: i += 1

            