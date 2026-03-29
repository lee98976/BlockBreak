import pygame
from pygame.locals import *
import sys

from entity import Entity
from gameVars import *

class Player(Entity):
    def __init__(self, animSet, healthBar):
        super().__init__(animSet, "Player", 5)
        self.pos = vec(200, 200)
        self.despawnTime = 300

        self.isDashing = False
        self.dashFrames = 0
        self.dashVector = vec(0, 0)
        self.lastInput = K_UP

        self.healthBar = healthBar

    def posUpdate(self):
        self.change = vec(0,0)

        if self.isDashing:
            self.change = self.dashVector
            self.dashVector *= 0.94
        else:
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[K_LEFT]:
                self.lastInput = K_LEFT
                self.change.x = -2
            if pressed_keys[K_RIGHT]:
                self.lastInput = K_RIGHT
                self.change.x = 2
            if pressed_keys[K_UP]:
                self.lastInput = K_UP
                self.change.y = -2
            if pressed_keys[K_DOWN]:
                self.lastInput = K_DOWN
                self.change.y = 2

        self.pos += self.change

    def dash(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_x] and self.dashFrames < -5 and not self.isDashing:
            self.changeAnim(1)
            self.isDashing = True
            self.dashFrames = 13
            self.dashVector = vec(0,0)
            dashSpeed = 12

            if pressed_keys[K_LEFT]:
                self.dashVector.x = -dashSpeed
            if pressed_keys[K_RIGHT]:
                self.dashVector.x = dashSpeed
            if pressed_keys[K_UP]:
                self.dashVector.y = -dashSpeed
            if pressed_keys[K_DOWN]:
                self.dashVector.y = dashSpeed

            if pressed_keys[K_LEFT] or pressed_keys[K_RIGHT] or pressed_keys[K_UP] or pressed_keys[K_DOWN]:
                return

            if self.lastInput == K_LEFT:
                self.dashVector.x = -dashSpeed
            if self.lastInput == K_RIGHT:
                self.dashVector.x = dashSpeed
            if self.lastInput == K_UP:
                self.dashVector.y = -dashSpeed
            if self.lastInput == K_DOWN:
                self.dashVector.y = dashSpeed

    def onDeath(self):
        self.changeAnim(2)
    
    def updateHealthBar(self):
        self.healthBar.updateHealth(self.hp)

    def update(self):
        self.renderAnim()

        if not self.dead:
            self.updateEntity()
            self.posUpdate()
            self.dash()
            self.rect.center = self.pos
            self.dashFrames -= 1
        else:
            self.despawnTime -= 1
            if self.despawnTime <= 0:
                pygame.quit()
                sys.exit()

        if self.dashFrames <= 0:
            self.isDashing = False