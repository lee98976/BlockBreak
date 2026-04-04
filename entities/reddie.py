import pygame
from pygame.locals import *
import random
import math

from entity import Entity
from entities.pickups import HealthPack
from storage.gameVars import *

class Reddie(Entity):
    def __init__(self, game, hp, following, dropChance, pos):
        super().__init__(game, game.enemyAnimSet, "Reddie", hp, pos)

        self.following = following
        self.dropChance = dropChance

        self.isHarmful = True

        # --- STATE SYSTEM ---
        self.state = random.choice(["chase", "circle", "ambush"])
        self.stateTimer = random.randint(120, 240)

        # --- COMBAT ---
        self.stunTimer = 0

        # --- DEATH ---
        self.deleteTimer = 30

    def updateAI(self):
        if self.following is None:
            return

        # direction to player
        diff = self.following.pos - self.pos
        if diff.length() == 0:
            return

        direction = diff.normalize()

        desired = vec(0, 0)

        if self.state == "chase":
            desired = direction * 1.5
        elif self.state == "circle":
            perp = vec(-direction.y, direction.x)
            desired = direction * 0.8 + perp * 1.8
        elif self.state == "ambush":
            # slow tracking
            desired = direction * 0.4

            self.stateTimer -= 1
            if self.stateTimer <= 65:
                desired = direction * 4

        self.vel += (desired - self.vel) * 0.15

        self.vel += vec(random.uniform(-0.1, 0.1), random.uniform(-0.1, 0.1))

    def updateState(self):
        self.stateTimer -= 1

        if self.stateTimer > 0:
            return

        if self.state == "chase":
            self.state = random.choice(["circle", "ambush"])
            self.stateTimer = random.randint(120, 240)

            if self.state == "ambush":
                self.changeAnim(2)  # transform → ambush
                self.defaultAnim = 1  # ambush idle

        elif self.state == "circle":
            self.state = "chase"
            self.stateTimer = random.randint(100, 160)
        elif self.state == "ambush":
            self.state = "chase"
            self.stateTimer = random.randint(180, 260)

            self.changeAnim(3)
            self.defaultAnim = 0

    def takeDamage(self, dmg, iFrames=30):
        super().takeDamage(dmg, iFrames)

        if self.dead:
            return

        # knockback + stun
        player = self.game.player
        direction = (self.pos - player.pos)

        if direction.length() > 0:
            direction = direction.normalize()
            self.vel += direction * 8

        self.stunTimer = 40


    def onDeath(self):
        self.following = None
        self.isHarmful = False
        self.changeAnim(4)

    def update(self):
        self.renderAnim()

        if not self.dead:
            if self.stunTimer > 0:
                self.stunTimer -= 1
                self.vel *= 0.85  
            else:
                self.updateAI()
                self.updateState()

            self.updateEntity()

        else:
            self.deleteTimer -= 1
            if self.deleteTimer <= 0:
                if random.random() < self.dropChance:
                    hp = HealthPack(self.game, self.pos)
                    self.game.friendly_sprites.add(hp)
                self.kill()