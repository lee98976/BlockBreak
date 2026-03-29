import pygame
from pygame.locals import *
import sys
import random

from entity import Entity
from entities.pickups import HealthPack
from gameVars import *

class Reddie(Entity):
    def __init__(self, game, animSet, hp, following, attackType, dropChance):
        super().__init__(animSet, "Reddie", hp)
        self.game = game
        self.pos = vec(random.randint(50,350), random.randint(200,400))
        self.following = following
        self.attackType = attackType
        self.attackCooldown = 0
        self.switchTimer = 120
        self.deleteTimer = 30
        self.dropChance = dropChance
        self.isHarmful = True

        self.behavior = random.choice(["chase","circle","ambush"])
        self.attackTimer = random.randint(40,320)

    def posUpdate(self):
        if self.following is None:
            return

        dif = self.following.pos - self.pos

        if dif.length() == 0:
            return

        direction = dif.normalize()

        if self.behavior == "chase":
            self.pos += direction * 1.4
            if self.switchTimer < 0:
                if random.random() < 0.5:
                    self.switchTimer = random.randint(120,320)
                    self.behavior = "circle"
                else:
                    self.switchTimer = random.randint(200,400)
                    self.behavior = "ambush"
        elif self.behavior == "circle":
            perp = vec(-direction.y, direction.x)
            self.pos += direction * 1
            self.pos += perp * 2
            if self.switchTimer < 0:
                self.switchTimer = random.randint(100, 150)
                self.behavior = "chase"
        elif self.behavior == "ambush":
            self.pos += direction * 0.3
            self.attackTimer -= 1

            if self.attackTimer <= 0:
                self.pos += direction * 3
                if self.attackTimer < -40:
                    self.attackTimer = random.randint(120,320)
            
            if self.switchTimer < 0:
                self.switchTimer = random.randint(400, 450)
                self.behavior = "chase"
        
        self.pos += vec(random.uniform(-0.3,0.3), random.uniform(-0.3,0.3))

    def attack(self):
        if self.attackCooldown <= 0:
            if self.attackType == "ranged":
                self.attackCooldown = 50

    def onDeath(self):
        self.following = None
        self.dead = True
        self.isHarmful = False
        self.changeAnim(1)

    def update(self):
        self.renderAnim()
        self.updateEntity()

        if not self.dead:
            self.posUpdate()
            self.attack()
        else:
            self.deleteTimer -= 1
            if self.deleteTimer <= 0:
                if random.random() < self.dropChance:
                    hp = HealthPack(self.game.healthPackSet, self.pos)
                    self.game.friendly_sprites.add(hp)
                self.kill()
        
        self.switchTimer -= 1
        self.attackCooldown -= 1
        self.rect.center = self.pos