import math
import random
import pygame
from entity import Entity
from entities.laser import Laser
from entities.reddie import Reddie

class Boss(Entity):
    def __init__(self, game):
        super().__init__(game.bossAnimSet, "Bossy", 999)
        self.game = game
        self.pos = pygame.Vector2(200,80)
        self.active = False
        self.angle = 0
        self.switchTimer = 60
        self.CW = 1
        self.mag = 1
        self.goToMag = 1.5
        self.spawnTimer = 0
        self.deleteTimer = 300

        self.lasers = [Laser(0.25 * i * math.pi) for i in range(0, 8)]

    def activate(self):
        self.active = True
        self.defaultAnim = 1
        self.changeAnim(1)

    def onDeath(self):
        self.active = False
        self.changeAnim(2)

    def update(self):
        self.renderAnim()
        self.updateEntity()
        if self.mag < self.goToMag:
            self.mag += 0.02
            if self.mag >= self.goToMag:
                self.goToMag = 0.5
        else:
            self.mag -= 0.02
            if self.mag <= self.goToMag:
                self.goToMag = 1.5
        if self.switchTimer <= 0:
            self.CW *= -1
            self.switchTimer = random.randint(300, 600)
        if not self.dead:
            self.pos.y = 80 + math.sin(pygame.time.get_ticks()/500)*5
        else:
            self.deleteTimer -= 1
            self.switchTimer -= 1
            if self.deleteTimer < 0:
                self.active = False
                self.kill()
        if self.active:
            if self.spawnTimer <= 0:
                e = Reddie(self.game, 1, self.game.player, "melee", 0.5)
                self.game.enemy_sprites.add(e)
                self.spawnTimer = 90
            self.spawnTimer -= 1
            self.angle += 0.005 * self.CW * self.mag
            for l in self.lasers:
                l.angle += 0.005 * self.CW * self.mag
                l.update()
        self.rect.center = self.pos

    def drawLasers(self, screen):
        if not self.active:
            return
        for l in self.lasers:
            length = 600
            end = pygame.Vector2(
                self.pos.x + math.cos(l.angle)*length,
                self.pos.y + math.sin(l.angle)*length
            )
            pygame.draw.line(screen, l.color, self.pos, end, 8)

    def checkDashDamage(self, player):
        if not self.active:
            return
        for l in self.lasers:
            if l.hp <= 0: continue
            start = self.pos
            end = pygame.Vector2(
                self.pos.x + math.cos(l.angle)*600,
                self.pos.y + math.sin(l.angle)*600
            )
            line = end - start
            player_vec = player.pos - start
            t = max(0, min(1, player_vec.dot(line) / line.length_squared()))
            closest = start + line * t
            dist = (player.pos - closest).length()
            if dist < 10:
                if player.isDashing:
                    player.invFrames = 15
                    l.hit()
                else:
                    player.takeDamage(1,60)

    def deadCheck(self):
        return all(l.hp <= 0 for l in self.lasers)
