import pygame
from pygame.locals import *
import sys

from entity import Entity
from storage.gameVars import *

class Player(Entity):
    def __init__(self, game, healthBar):
        super().__init__(game, game.playerAnimSet, "Player", 5)
        self.pos = vec(200, 200)
        self.despawnTime = 300

        self.isDashing = False
        self.dashFrames = 0
        self.dashVector = vec(0, 0)
        self.lastInput = K_UP

        self.healthBar = healthBar

    def posUpdate(self):
        self.vel = vec(0,0)

        if self.isDashing:
            self.vel = self.dashVector
            self.dashVector *= 0.94
        else:
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[K_LEFT]:
                self.lastInput = K_LEFT
                self.vel.x = -2
            if pressed_keys[K_RIGHT]:
                self.lastInput = K_RIGHT
                self.vel.x = 2
            if pressed_keys[K_UP]:
                self.lastInput = K_UP
                self.vel.y = -2
            if pressed_keys[K_DOWN]:
                self.lastInput = K_DOWN
                self.vel.y = 2


    def dash(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_x] and self.dashFrames < -5 and not self.isDashing:
            self.changeAnim(1)
            self.isDashing = True
            self.dashFrames = 13
            self.dashVector = vec(0,0)
            dashSpeed = 12

            if pressed_keys[K_LEFT]:
                self.dashVector.x = -1
            if pressed_keys[K_RIGHT]:
                self.dashVector.x = 1
            if pressed_keys[K_UP]:
                self.dashVector.y = -1
            if pressed_keys[K_DOWN]:
                self.dashVector.y = 1

            if pressed_keys[K_LEFT] or pressed_keys[K_RIGHT] or pressed_keys[K_UP] or pressed_keys[K_DOWN]:
                self.dashVector = self.dashVector.normalize() * dashSpeed
                return

            if self.lastInput == K_LEFT:
                self.dashVector.x = -1
            if self.lastInput == K_RIGHT:
                self.dashVector.x = 1
            if self.lastInput == K_UP:
                self.dashVector.y = -1
            if self.lastInput == K_DOWN:
                self.dashVector.y = 1
            
            self.dashVector = self.dashVector.normalize() * dashSpeed

    def onDeath(self):
        self.changeAnim(2)
    
    def updateHealthBar(self):
        self.healthBar.updateHealth(self.hp)

    def update(self):
        self.renderAnim()

        self.lastRoom = self.game.get_current_room(self)
        if not self.dead:
            self.posUpdate()
            self.dash()
            self.updateEntity()
            self.dashFrames -= 1
        else:
            self.despawnTime -= 1
            if self.despawnTime <= 0:
                pygame.quit()
                sys.exit()

        if self.dashFrames <= 0:
            self.isDashing = False

    
    # def clampPosition(self):
    #     if not self.lastRoom:
    #         return

    #     half_w = self.rect.width / 2
    #     half_h = self.rect.height / 2

    #     self.pos.x = max(
    #         self.lastRoom.rect.left + half_w,
    #         min(self.lastRoom.rect.right - half_w, self.pos.x)
    #     )

    #     self.pos.y = max(
    #         self.lastRoom.rect.top + half_h,
    #         min(self.lastRoom.rect.bottom - half_h, self.pos.y)
    #     )