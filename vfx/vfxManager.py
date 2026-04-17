import pygame
import random
from storage.gameVars import *
from vfx.shockWave import *
from vfx.particle import *

class vfxManager():
    def __init__(self, game):
        self.game = game
        self.shockwaves = []
        self.particles = []

    def add_shockwave(self, pos, radius=0, speed=0.5, thickness=14, strength=3):
        self.shockwaves.append(Shockwave(
            pos=pos,
            radius=radius,
            speed=speed,
            thickness=thickness,
            strength=strength
        ))

    def add_particles(self, pos, count=10,
                      start_color=(0, 0, 255), end_color=(0, 150, 255),
                      size=1, gravity=False, floaty=True, posRange=1.5):
        for _ in range(count):
            vel = vec(random.uniform(0, 0), random.uniform(0, 0))

            p = Particle(
                pos=pos + vec(random.uniform(-posRange, posRange), random.uniform(-posRange, posRange)),
                vel=vel,
                lifetime=random.randint(20, 25),
                start_color=start_color,
                end_color=end_color,
                size=size,
                gravity=gravity,
                floaty=floaty
            )

            self.particles.append(p)

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
    
    def update(self, dt=1/DESIGN_FPS):
        # shockwaves
        i = 0
        while i < len(self.shockwaves):
            self.shockwaves[i].update(dt)
            if not self.shockwaves[i].alive:
                self.shockwaves.pop(i)
            else:
                i += 1

        # particles
        i = 0
        while i < len(self.particles):
            p = self.particles[i]
            p.update(dt)

            if p.lifetime <= 0:
                self.particles.pop(i)
            else:
                i += 1

            