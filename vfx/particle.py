from storage.gameVars import *
import random

class Particle:
    def __init__(self, pos, vel, lifetime,
                 start_color, end_color,
                 size=2,
                 gravity=False,
                 floaty=False):

        self.pos = vec(pos)
        self.vel = vec(vel)

        self.lifetime = lifetime
        self.max_lifetime = lifetime

        self.start_color = start_color
        self.end_color = end_color

        self.size = size

        self.gravity = gravity
        self.floaty = floaty

        # small random drift seed
        self.noise_offset = vec(
            random.uniform(-1, 1),
            random.uniform(-1, 1)
        )
    
    def get_color(self):
        t = 1 - (self.lifetime / self.max_lifetime)

        r = int(self.start_color[0] + (self.end_color[0] - self.start_color[0]) * t)
        g = int(self.start_color[1] + (self.end_color[1] - self.start_color[1]) * t)
        b = int(self.start_color[2] + (self.end_color[2] - self.start_color[2]) * t)

        return (r, g, b)

    def apply_float(self, dt=1/DESIGN_FPS):
        # VERY small jitter (pixel-scale)
        jitter = vec(
            random.uniform(-0.3, 0.3),
            random.uniform(-0.3, 0.3)
        )
        self.vel += jitter * dt * DESIGN_FPS * 0.2
    
    def apply_gravity(self, dt=1/DESIGN_FPS):
        if self.gravity:
            self.vel.y += 0.15 * dt * DESIGN_FPS * 0.2
    
    def update(self, dt=1/DESIGN_FPS):
        if self.floaty:
            self.apply_float(dt)

        self.apply_gravity(dt)

        self.pos += self.vel
        self.vel *= 0.96  # damping

        self.lifetime -= dt * DESIGN_FPS
    
    def draw(self, surface, camera):
        screen_pos = self.pos - camera + vec(WIDTH/2, HEIGHT/2)

        # fade
        t = self.lifetime / self.max_lifetime
        alpha = int(255 * t)

        color = self.get_color()

        # create small surface for alpha
        s = pygame.Surface((self.size*2, self.size*2), pygame.SRCALPHA)
        pygame.draw.circle(s, (*color, alpha), (self.size, self.size), self.size)

        surface.blit(s, (screen_pos.x - self.size, screen_pos.y - self.size))