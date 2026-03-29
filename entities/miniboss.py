import math
import pygame
from entity import Entity
from entities.reddie import Reddie

class MiniBoss(Entity):
    def __init__(self, game, animSet, player, enemy_group, x):
        super().__init__(animSet, "MiniBoss", 2)
        self.game = game
        self.player = player
        self.enemy_group = enemy_group
        self.pos = pygame.Vector2(x,120)
        self.waveSize = 10
        self.deleteTimer = 120
        self.spawnWave()

    def spawnWave(self):
        for i in range(self.waveSize):
            e = Reddie(self.game, self.game.enemyAnimSet, 1, self.player, "melee", 0.1)
            self.enemy_group.add(e)

    def takeDamage(self, dmg):
        if any(isinstance(e, Reddie) and not e.dead for e in self.enemy_group):
            return
        super().takeDamage(dmg)
        if not self.dead:
            self.spawnWave()

    def onDeath(self):
        self.changeAnim(1)

    def update(self):
        if not self.dead:
            self.pos.x += math.sin(pygame.time.get_ticks()/400)*0.3
        else:
            self.deleteTimer -= 1
            if self.deleteTimer <= 0:
                self.kill()
        self.renderAnim()
        self.updateEntity()
        self.rect.center = self.pos
