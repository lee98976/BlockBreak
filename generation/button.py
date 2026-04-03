import pygame
from entity import *

class Button(Entity):
    def __init__(self, game, room, pos):
        super().__init__(game, game.buttonSet, "button", 3, pos)

        self.room = room

        self.max_hp = 3
        self.activated = False

        self.changeAnim(0)


    def takeDamage(self, dmg, iFrames=10):
        # ONLY accept dash damage
        if not self.game.player.isDashing:
            return

        if self.activated:
            return

        oldHp = self.hp
        super().takeDamage(dmg, iFrames)

        if (oldHp == self.hp): return

        if (self.game.player.vel != vec(0, 0)):
            direction = self.game.player.vel.normalize()
            
            self.game.player.vel += -direction * 30
            self.game.player.dashFrames = 6
            self.game.player.isDashing = False

            print(self.game.player.vel)

        self.updateAnim()
        print("button hp:", self.hp)

        if self.hp <= 0:
            self.activate()
        

    def updateAnim(self):
        stage = self.max_hp - self.hp
        stage = min(stage, 3)
        self.changeAnim(stage)

    def activate(self):
        self.activated = True
        self.changeAnim(3)
        self.room.trigger_event("button")

    def update(self):
        self.updateEntity()
        self.renderAnim()