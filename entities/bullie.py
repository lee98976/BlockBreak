import pygame
from pygame.locals import *
import random
import math

from entity import Entity
from storage.gameVars import *
from entities.pickups import HealthPack
from entities.bullieProjectile import BullieProjectile

class Bullie(Entity):
    def __init__(self, game, pos, target):
        super().__init__(game, game.bullieAnimSet, "Bullie", 4, pos)

        self.target = target
        self.state = "idle"

        self.stateTimer = 0
        self.attackCooldown = random.randint(60, 120)

        self.ammo = 1  # goes 1 → 4
        self.maxAmmo = 4

        self.projectileMode = False
        self.isHarmful = True

        self.deleteTimer = 30

        self.changeAnim(0)

    def getDirection(self):
        diff = self.target.pos - self.pos
        if diff.length() == 0:
            return vec(0, 0)
        return diff.normalize()

    def updateState(self, dt=1/DESIGN_FPS):
        frame = dt * DESIGN_FPS
        if self.state == "idle":
            self.attackCooldown -= frame

            # slight drift
            self.vel *= 0.9 ** frame

            if self.attackCooldown <= 0:
                self.state = "telegraph"
                self.stateTimer = 40

        elif self.state == "telegraph":
            # slow to stop
            self.vel *= 0.7 ** frame
            self.stateTimer -= frame

            if self.stateTimer <= 0:
                self.state = "shoot"

        elif self.state == "shoot":
            self.fireProjectile()

            if self.ammo > self.maxAmmo:
                self.state = "self_launch"
                self.stateTimer = 20
            else:
                self.state = "cooldown"
                self.stateTimer = 30

        elif self.state == "cooldown":
            self.vel *= 0.8 ** frame
            self.stateTimer -= frame

            if self.stateTimer <= 0:
                self.state = "telegraph"
                self.stateTimer = 40

        elif self.state == "self_launch":
            self.stateTimer -= frame
            self.vel *= 0.6 ** frame

            if self.stateTimer <= 0:
                self.becomeProjectile()

    def fireProjectile(self):
        direction = self.getDirection()

        spread = 0.2
        direction += vec(random.uniform(-spread, spread), random.uniform(-spread, spread))
        direction = direction.normalize()

        # spawn projectile (reuse Bullie as projectile or separate class later)
        proj = BullieProjectile(self.game, self.pos, direction * 1)
        proj.changeAnim(1 + self.ammo)
        proj.defaultAnim = 1 + self.ammo
        self.game.enemy_sprites.add(proj)

        self.ammo += 1

    def becomeProjectile(self):
        direction = self.getDirection()

        self.projectileMode = True
        self.vel = direction * 2
        self.dead = True # let it delete itself

        self.changeAnim(1)  # reuse projectile anim

    def takeDamage(self, dmg, iFrames=30):
        if self.projectileMode:
            return

        super().takeDamage(dmg, iFrames)

        if self.dead:
            return

        # knockback
        player = self.game.player
        direction = (self.pos - player.pos)

        if direction.length() > 0:
            self.vel += direction.normalize() * 1.5

    def onDeath(self):
        self.game.vfxManager.add_particles(
            pos=self.pos,
            count=18,
            start_color=(255, 120, 40),
            end_color=(180, 30, 10),
            size=2,
            gravity=True,
            floaty=False
        )
        self.isHarmful = False
        self.changeAnim(6)


    def update(self, dt=1/DESIGN_FPS):
        frame = dt * DESIGN_FPS
        if not self.room.discovered or self.game.dialogue.active: return
        self.renderAnim(dt)

        if not self.dead:
            if not self.projectileMode:
                self.updateState(dt)
            else:
                # projectile mode: just move fast
                self.vel *= 0.99 ** frame

            if self.projectileMode:
                self.pos += self.vel * frame
                self.rect.center = self.pos
            else:
                self.updateEntity(dt)

        else:
            self.deleteTimer -= frame
            if self.deleteTimer <= 0:
                if random.random() < 0.3:
                    hp = HealthPack(self.game, self.pos)
                    self.game.friendly_sprites.add(hp)
                self.kill()