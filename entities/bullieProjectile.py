from entity import *

class BullieProjectile(Entity):
    def __init__(self, game, pos, vel):
        super().__init__(game, game.bullieAnimSet, "BullieProj", 1, pos)

        self.vel = vel
        self.life = 120
        self.isHarmful = True

    def update(self, dt=1/DESIGN_FPS):
        frame = dt * DESIGN_FPS
        self.life -= frame

        if self.life <= 0:
            self.kill()
            return

        # 🔥 manual movement (NO collision)
        self.pos += self.vel * frame
        self.rect.center = self.pos

        self.renderAnim(dt)