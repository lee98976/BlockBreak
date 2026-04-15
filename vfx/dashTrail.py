from entity import *
import math

class DashTrail(Entity):
    def __init__(self, game, owner, diagonal=False):
        anim = game.diagonalDashTrailSet if diagonal else game.dashTrailSet
        super().__init__(game, anim, "dashTrail", 1, owner.pos)

        self.life = 20
        self.owner = owner
        self.diagonal = diagonal

        self.rotation = -math.degrees(math.atan2(self.owner.dashVector.y, self.owner.dashVector.x))
        if (self.diagonal): self.rotation -= 45
        self.pos = self.owner.pos
        self.changeAnim(0)

    def update(self, dt=1/DESIGN_FPS):
        frame = dt * DESIGN_FPS
        self.life -= frame
        

        self.pos = self.owner.pos
        self.rect.center = self.pos

        if self.life <= 0:
            self.kill()
            return

        self.renderAnim(dt)