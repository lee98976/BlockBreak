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

    # ========================
    # 🎯 HELPERS
    # ========================
    def getDirection(self):
        diff = self.target.pos - self.pos
        if diff.length() == 0:
            return vec(0, 0)
        return diff.normalize()

    # ========================
    # 🔄 STATE MACHINE
    # ========================
    def updateState(self):
        if self.state == "idle":
            self.attackCooldown -= 1

            # slight drift
            self.vel *= 0.9

            if self.attackCooldown <= 0:
                self.state = "telegraph"
                self.stateTimer = 40

        elif self.state == "telegraph":
            # slow to stop
            self.vel *= 0.7
            self.stateTimer -= 1

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
            self.vel *= 0.8
            self.stateTimer -= 1

            if self.stateTimer <= 0:
                self.state = "telegraph"
                self.stateTimer = 40

        elif self.state == "self_launch":
            self.stateTimer -= 1
            self.vel *= 0.6

            if self.stateTimer <= 0:
                self.becomeProjectile()

    # ========================
    # 🔫 SHOOTING
    # ========================
    def fireProjectile(self):
        direction = self.getDirection()

        # animation based on ammo
        self.changeAnim(1 + self.ammo)

        # spawn projectile (reuse Bullie as projectile or separate class later)
        proj = BullieProjectile(self.game, self.pos, direction * 4)
        self.game.enemy_sprites.add(proj)

        self.ammo += 1

    # ========================
    # 💥 SELF LAUNCH
    # ========================
    def becomeProjectile(self):
        direction = self.getDirection()

        self.projectileMode = True
        self.vel = direction * 8

        self.changeAnim(1)  # reuse projectile anim

    # ========================
    # 💥 DAMAGE
    # ========================
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
            self.vel += direction.normalize() * 6

    # ========================
    # ☠️ DEATH
    # ========================
    def onDeath(self):
        self.isHarmful = False
        self.changeAnim(6)

    # ========================
    # 🔄 UPDATE
    # ========================
    def update(self):
        self.renderAnim()

        if not self.dead:
            if not self.projectileMode:
                self.updateState()
            else:
                # projectile mode: just move fast
                self.vel *= 0.99

            self.updateEntity()

        else:
            self.deleteTimer -= 1
            if self.deleteTimer <= 0:
                if random.random() < 0.3:
                    hp = HealthPack(self.game, self.pos)
                    self.game.friendly_sprites.add(hp)
                self.kill()