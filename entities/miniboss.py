import math
import random
import pygame
from entity import Entity
from entities.reddie import Reddie
from storage.gameVars import vec

class MiniBoss(Entity):
    def __init__(self, game, player, enemy_group, pos):
        super().__init__(game, game.miniBossAnimSet, "MiniBoss", 2, pos)
        self.game = game
        self.player = player
        self.enemy_group = enemy_group
        self.waveSize = 10
        self.deleteTimer = 120
        self.spawnWave()

    def spawnWave(self):
        for i in range(self.waveSize):
            pos = vec(random.randint(int(self.pos.x - 20), int(self.pos.x + 20)), random.randint(int(self.pos.y - 20), int(self.pos.y + 20)))
            e = Reddie(self.game, 1, self.player, "melee", 0.1, pos)
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
