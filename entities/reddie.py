import pygame
from pygame.locals import *
import sys
import random

from entity import Entity
from entities.pickups import HealthPack
from storage.gameVars import *

class Reddie(Entity):
    def __init__(self, game, hp, following, attackType, dropChance):
        super().__init__(game, game.enemyAnimSet, "Reddie", hp)
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
        self.vel = vec(0, 0)

        if self.following is None:
            return

        dif = self.following.pos - self.pos

        if dif.length() < 0.3:
            return

        direction = dif.normalize()

        if self.behavior == "chase":
            self.vel += direction * 1.4
            if self.switchTimer < 0:
                if random.random() < 0.5:
                    self.switchTimer = random.randint(120,320)
                    self.behavior = "circle"
                else:
                    self.switchTimer = random.randint(200,400)
                    self.behavior = "ambush"
        elif self.behavior == "circle":
            perp = vec(-direction.y, direction.x)
            self.vel += direction * 1
            self.vel += perp * 2
            if self.switchTimer < 0:
                self.switchTimer = random.randint(100, 150)
                self.behavior = "chase"
        elif self.behavior == "ambush":
            self.vel += direction * 0.3
            self.attackTimer -= 1

            if self.attackTimer <= 0:
                self.vel += direction * 3
                if self.attackTimer < -40:
                    self.attackTimer = random.randint(120,320)
            
            if self.switchTimer < 0:
                self.switchTimer = random.randint(400, 450)
                self.behavior = "chase"
        
        self.vel += vec(random.uniform(-0.3,0.3), random.uniform(-0.3,0.3))

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

        if not self.dead:
            self.posUpdate()
            self.attack()
            self.updateEntity()
        else:
            self.deleteTimer -= 1
            if self.deleteTimer <= 0:
                if random.random() < self.dropChance:
                    hp = HealthPack(self.game, self.pos)
                    self.game.friendly_sprites.add(hp)
                self.kill()
        
        self.switchTimer -= 1
        self.attackCooldown -= 1